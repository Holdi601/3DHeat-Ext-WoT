"""
A World of Tanks replay (.wotreplay) as rows: every vehicle's position over
time, and every kill where it happened.

What the file holds (see `bigworld` for the container):

- The first JSON block, written when the battle began: the map (`mapName`,
  `mapDisplayName`), the client version, the recording player and vehicle, and
  the roster - `vehicles`, keyed by each vehicle's entity id, with the
  player's `name`, `team` (1 or 2) and `vehicleType` (`nation:tank`, e.g.
  `ussr:R144_K_91`).
- The second block, when the recording lasted to the end of the battle: the
  results. Per vehicle `lifeTime` (whole seconds from the start of the battle),
  `killerID`, `deathReason` (-1: survived), `kills`, `damageDealt`; per match
  `duration`, `winnerTeam`, `arenaUniqueID`.
- The packet stream: the position updates of every vehicle the recording
  client was told about - its own team always, an enemy only while spotted -
  about ten times a second, in metres (x east, y up, z north), with the hull's
  heading.

Deaths are not read from the stream (the packets that announce them are
numbered differently with every patch); they come from the results. A death's
time is the battle's start on the replay's clock plus the victim's `lifeTime`,
so it is good to about a second; its place is where the victim was last seen
by then, when that was within five seconds (else, on newer clients, the place
the results give, without a height). The battle's start is the first moment any vehicle moves - nothing
moves during the countdown. A recording that stopped before the end (the
player left the battle) has no results, and so positions and no deaths.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from . import bigworld as bw

#: The key World of Tanks enciphers its replays' packet streams with, as the
#: community tools that read them have published since 2013.
KEY = bytes.fromhex("DE72BEA0DE04BEB1DEFEBEEFDEADBEEF")

#: How a viewer should read the table. See docs/data-formats.md of 3DHeat.
HINTS = {
    "version": 1,
    "kind": "wot-replay",
    "game": "World of Tanks",
    # BigWorld's world: x east, y up, z north - left-handed, so Z is flipped to keep the map unmirrored.
    "axes": {"up": "y", "flipX": False, "flipY": False, "flipZ": True, "scale": 1},
    # A tank is about seven metres long.
    "entity": {"size": 7},
    "columns": {
        "x": "x",
        "y": "y",
        "z": "z",
        "time": "time",
        "timeUnit": "seconds",
        "personId": "player",
        "teamId": "team",
        "sessionId": "match",
        "lookMode": "vector",
        "dirX": "dirX",
        "dirY": "dirY",
        "dirZ": "dirZ",
        "extra": ["event", "vehicle", "type", "own", "battleTime", "other", "reason", "map"],
    },
}

#: Every column of the table, in order, with its kind: f (float), i (small int), s (text).
COLUMNS = {
    "match": "s", "map": "s", "time": "d", "battleTime": "f", "event": "s",
    "player": "s", "team": "s", "vehicle": "s", "type": "s", "own": "i",
    "x": "f", "y": "f", "z": "f", "dirX": "f", "dirY": "f", "dirZ": "f",
    "other": "s", "reason": "s", "entity": "l",
}  # fmt: skip


@dataclass
class Match:
    name: str
    map: str
    rows: dict[str, list] = field(default_factory=lambda: {c: [] for c in COLUMNS})
    summary: dict[str, Any] = field(default_factory=dict)

    def add(self, **row: Any) -> None:
        for c in COLUMNS:
            self.rows[c].append(row.get(c))


def _results(blocks: list[Any]) -> tuple[dict, dict, dict]:
    """The results block's three parts, when there is one: results, vehicles as at the end, frags."""
    if len(blocks) > 1 and isinstance(blocks[1], list):
        parts = list(blocks[1]) + [{}, {}, {}]
        return tuple(p if isinstance(p, dict) else {} for p in parts[:3])  # type: ignore[return-value]
    return {}, {}, {}


def _vehicle_results(results: dict) -> dict[int, dict]:
    out = {}
    for vid, v in (results.get("vehicles") or {}).items():
        v = v[0] if isinstance(v, list) and v else v
        if isinstance(v, dict):
            try:
                out[int(vid)] = v
            except ValueError:
                continue
    return out


def _version(head: dict) -> str:
    v = str(head.get("clientVersionFromExe") or "")
    if not v:
        m = re.search(r"v\.([\d.]+)", str(head.get("clientVersionFromXml") or ""))
        v = m.group(1) if m else ""
    return v.replace(", ", ".").replace(",", ".")


def read(buf: bytes, name: str = "replay") -> Match:
    """A replay's bytes as a match. `name` is used when the file has no match id of its own."""
    rep = bw.read_replay(buf, KEY)
    head = rep.header
    if not head:
        raise ValueError("the replay has no readable header")
    results, end_roster, _frags = _results(rep.blocks)
    common = results.get("common") or {}
    vres = _vehicle_results(results)
    roster: dict[int, dict] = {}
    # The header's roster, then the results' for vehicles it leaves out (some modes list only the own team).
    for source in (head.get("vehicles") or {}, end_roster):
        for vid, v in source.items():
            try:
                if isinstance(v, dict):
                    roster.setdefault(int(vid), dict(v))
            except (TypeError, ValueError):
                continue
    match_id = str(results.get("arenaUniqueID") or "") or name
    map_id = str(head.get("mapName") or "unknown")
    m = Match(name=match_id, map=map_id)

    idx = bw.index(rep.stream)
    kind = bw.find_position_type(rep.stream, idx)
    all_tracks = bw.tracks(rep.stream, kind, idx) if kind is not None else {}
    tracks = {e: t for e, t in all_tracks.items() if e in roster}
    start = bw.battle_start(tracks)
    me = str(head.get("playerName") or "")

    def who(vid: int) -> dict[str, Any]:
        v = roster.get(vid, {})
        return {
            "player": str(v.get("name") or v.get("fakeName") or f"vehicle {vid}"),
            "team": str(v.get("team", "")),
            "vehicle": str(v.get("vehicleType") or ""),
            "type": "tank",
            "own": 1 if me and v.get("name") == me else 0,
            "entity": vid,
        }

    # Deaths, from the results: when, and where the victim was last seen by then.
    deaths: dict[int, float] = {}
    kills: list[dict[str, Any]] = []
    for vid, r in vres.items():
        if r.get("deathReason", -1) in (-1, None) or vid not in roster:
            continue
        life = r.get("lifeTime")
        t = start + float(life) + 0.5 if start is not None and isinstance(life, (int, float)) else None
        if t is not None:
            deaths[vid] = t
        killer = r.get("killerID") or 0
        kill: dict[str, Any] = {
            "time": round(t, 2) if t is not None else None,
            "victim": who(vid)["player"],
            "killer": who(int(killer))["player"] if killer else None,
            "reason": r.get("deathReason"),
        }
        i = _fresh(tracks.get(vid), t)
        if i is not None:
            track = tracks[vid]
            kill.update(x=float(track.x[i]), y=float(track.y[i]), z=float(track.z[i]))
        else:
            # Never seen near its death: newer clients give the place on the map (x, z), whole metres.
            pos = (end_roster.get(str(vid)) or {}).get("position")
            if isinstance(pos, list) and len(pos) == 2 and -30000 < pos[0] < 30000:
                kill.update(x=float(pos[0]), z=float(pos[1]))
        kills.append(kill)

    # Positions, until a vehicle's death.
    for vid, t in sorted(tracks.items()):
        w = who(vid)
        end = deaths.get(vid, math.inf)
        keep = t.time <= end
        for tt, x, y, z, yaw in zip(t.time[keep], t.x[keep], t.y[keep], t.z[keep], t.yaw[keep]):
            m.add(match=match_id, map=map_id, time=float(tt), battleTime=_bt(tt, start), event="position",
                  x=x, y=y, z=z, dirX=math.sin(yaw), dirY=0.0, dirZ=math.cos(yaw), **w)

    # Each death twice, as the 3DHeat CS2 tables have it: "death" where the victim fell, "kill" where the killer stood.
    for vid, r in vres.items():
        t = deaths.get(vid)
        if t is None:
            continue
        killer = int(r.get("killerID") or 0)
        victim_w, killer_w = who(vid), who(killer) if killer in roster else None
        vt = tracks.get(vid)
        i = _fresh(vt, t)
        if i is not None:
            m.add(match=match_id, map=map_id, time=t, battleTime=_bt(t, start), event="death",
                  x=vt.x[i], y=vt.y[i], z=vt.z[i], other=killer_w["player"] if killer_w else None,
                  reason=str(r.get("deathReason")), **victim_w)
        kt = tracks.get(killer) if killer_w else None
        k = _fresh(kt, t)
        if killer_w and k is not None and killer != vid:
            m.add(match=match_id, map=map_id, time=t, battleTime=_bt(t, start), event="kill",
                  x=kt.x[k], y=kt.y[k], z=kt.z[k], other=victim_w["player"], reason=str(r.get("deathReason")),
                  **killer_w)

    players = []
    for vid, v in sorted(roster.items(), key=lambda kv: (str(kv[1].get("team")), str(kv[1].get("name")))):
        r = vres.get(vid, {})
        t = tracks.get(vid)
        players.append({
            "name": v.get("name"),
            "team": v.get("team"),
            "vehicle": v.get("vehicleType"),
            "entity": vid,
            "own": bool(me and v.get("name") == me),
            "clan": v.get("clanAbbrev") or None,
            "samples": int(len(t.time)) if t is not None else 0,
            "kills": r.get("kills"),
            "damageDealt": r.get("damageDealt"),
            "survived": None if not r else r.get("deathReason", -1) == -1,
            "lifeTime": r.get("lifeTime"),
        })  # fmt: skip
    m.summary = {
        "format": "heat3d-wot-match",
        "version": 1,
        "game": "World of Tanks",
        "match": match_id,
        "map": map_id,
        "mapName": head.get("mapDisplayName"),
        "clientVersion": _version(head),
        "recorded": head.get("dateTime"),
        "player": me or None,
        "vehicle": head.get("playerVehicle"),
        "battleType": head.get("battleType"),
        "gameplay": head.get("gameplayID"),
        "server": head.get("serverName"),
        "duration": common.get("duration"),
        "winnerTeam": common.get("winnerTeam"),
        "complete": bool(results),
        "truncated": rep.truncated,
        "battleStart": round(start, 2) if start is not None else None,
        "recordingSeconds": round(float(idx["time"].max()), 2) if len(idx) else 0.0,
        "positionPacket": kind,
        "hz": bw.rate(tracks),
        "positions": int(sum(1 for e in m.rows["event"] if e == "position")),
        "units": "metres; x east, y up, z north",
        "players": players,
        "kills": kills,
    }
    return m


#: How old the last sighting may be for it to stand for where someone was at a death.
FRESH_SECONDS = 5.0


def _fresh(track: bw.Track | None, t: float | None) -> int | None:
    """The sample of `track` that says where it was at `t`: the last one by then, if it is recent."""
    if track is None or t is None:
        return None
    i = track.at(t + 0.5)
    return i if i is not None and t - track.time[i] <= FRESH_SECONDS else None


def _bt(t: float, start: float | None) -> float | None:
    return float(t) - start if start is not None else None


def read_file(path: str | Path) -> Match:
    p = Path(path)
    return read(p.read_bytes(), name=p.stem)
