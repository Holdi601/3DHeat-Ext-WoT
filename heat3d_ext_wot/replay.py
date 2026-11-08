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

Everything else in the stream - health changes, shots, tracers, explosions,
hits, gun angles, arena updates, chat, client events, the camera - is read by
`stream`, found by shape (the engine numbers it differently with patches).

Deaths come from the results (who, by whom, why); their time from the
arena's kill message (1.x), else the health change that ended the vehicle,
else the battle's start plus the victim's `lifeTime` (whole seconds). The
place is where the victim was last seen by then, when that was within five
seconds (else, on newer clients, the place the results give, without a
height). The battle's start is when the arena says the battle period began,
else the first moment any vehicle moves. A recording that stopped before the
end (the player left the battle) has no results, and so no deaths from them.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from . import bigworld as bw
from . import kept
from . import sidecar as sc
from . import stream as st
from .table import slug

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
        "extra": ["event", "vehicle", "type", "own", "battleTime", "other", "reason", "map", "value", "health",
                  "text", "turretYaw", "gunStep", "shot", "hitComponent", "hitCode", "hitU", "hitV", "hitW",
                  "hitExitU", "hitExitV", "hitExitW", "hitDirX", "hitDirY", "hitDirZ"],
    },
}

#: Every column of the table, in order, with its kind: f (float), i (small int), s (text).
COLUMNS = {
    "match": "s", "map": "s", "time": "d", "battleTime": "f", "event": "s",
    "player": "s", "team": "s", "vehicle": "s", "type": "s", "own": "i",
    "x": "f", "y": "f", "z": "f", "dirX": "f", "dirY": "f", "dirZ": "f",
    "other": "s", "reason": "s", "entity": "l",
    "value": "f", "health": "f", "text": "s", "turretYaw": "f", "gunStep": "i", "shot": "l",
    "hitComponent": "i", "hitCode": "i", "hitU": "f", "hitV": "f", "hitW": "f",
    "hitExitU": "f", "hitExitV": "f", "hitExitW": "f", "hitDirX": "f", "hitDirY": "f", "hitDirZ": "f",
}  # fmt: skip

#: A position's pitch and roll as the packet has them, radians: pitch positive nose down, roll as sent. Checked
#: against the ground (see the README): the pitch is minus the slope the vehicle climbs; two vehicles at one spot
#: with one heading have the same roll, with opposite headings opposite rolls.
COLUMNS.update(pitch="f", roll="f")
HINTS["columns"]["extra"] += ["pitch", "roll"]

#: The game's attack reasons (the `reason` of a health change and of a death), as far as they are known for
#: certain; other numbers are written as they are.
ATTACK_REASONS = {0: "shot", 1: "fire", 2: "ramming", 3: "world_collision", 4: "death_zone", 5: "drowning"}

#: The battle's periods, as arena updates number them.
PERIODS = {0: "idle", 1: "waiting", 2: "prebattle", 3: "battle", 4: "afterbattle"}


@dataclass
class Match:
    name: str
    map: str
    rows: dict[str, list] = field(default_factory=lambda: {c: [] for c in COLUMNS})
    summary: dict[str, Any] = field(default_factory=dict)
    #: The sidecar `<match>.messages.parquet`: everything not held whole by the table and the summary (Arrow).
    messages: Any = None

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
    results, end_roster, frags = _results(rep.blocks)
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
    moved = bw.battle_start(tracks)
    dec = st.decode(rep.stream, idx, set(roster))
    arena = _arena(dec, roster)
    # The battle's start: when the arena says the battle period began, else the first movement.
    start = arena["battleStart"] if arena["battleStart"] is not None else moved
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

    def label(vid: int | None) -> str | None:
        return who(vid)["player"] if vid and vid in roster else None

    def where(vid: int | None, t: float) -> tuple[float, float, float] | None:
        i = _fresh(tracks.get(vid), t) if vid is not None else None
        if i is None:
            return None
        tr = tracks[vid]
        return float(tr.x[i]), float(tr.y[i]), float(tr.z[i])

    def add(event: str, t: float, vid: int | None, pos: tuple[float, float, float] | None, **kw: Any) -> None:
        if pos is None:
            return
        w = who(vid) if vid is not None else {"player": "", "team": "", "vehicle": "", "type": "shell", "own": 0}
        m.add(match=match_id, map=map_id, time=t, battleTime=_bt(t, start), event=event, x=pos[0], y=pos[1],
              z=pos[2], **{**w, **kw})

    # Deaths: the arena's kill message (1.x) to a tenth of a second; else the health change that ended the
    # vehicle; else the results' lifeTime, good to a second.
    zero: dict[int, st.Health] = {}
    for h in dec.health:
        if h.new <= 0 and h.victim not in zero:
            zero[h.victim] = h
    deaths: dict[int, float] = {}
    death_source: dict[int, str] = {}
    for vid, r in vres.items():
        if r.get("deathReason", -1) in (-1, None) or vid not in roster:
            continue
        life = r.get("lifeTime")
        if vid in arena["killed"]:
            deaths[vid], death_source[vid] = arena["killed"][vid][0], "arena"
        elif vid in zero:
            deaths[vid], death_source[vid] = zero[vid].time, "health"
        elif start is not None and isinstance(life, (int, float)):
            deaths[vid], death_source[vid] = start + float(life) + 0.5, "lifeTime"
    kills: list[dict[str, Any]] = []
    for vid, r in vres.items():
        if r.get("deathReason", -1) in (-1, None) or vid not in roster:
            continue
        t = deaths.get(vid)
        killer = r.get("killerID") or 0
        kill: dict[str, Any] = {
            "time": round(t, 2) if t is not None else None,
            "timeFrom": death_source.get(vid),
            "victim": who(vid)["player"],
            "killer": who(int(killer))["player"] if killer else None,
            "reason": r.get("deathReason"),
            "reasonName": ATTACK_REASONS.get(r.get("deathReason")),
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

    # Positions, until a vehicle's death, with the turret's yaw and the gun's elevation step.
    in_table: set[int] = set()  # the position packets that are rows (by offset), for the completeness count
    for vid, t in sorted(tracks.items()):
        w = who(vid)
        end = deaths.get(vid, math.inf)
        keep = t.time <= end
        times = t.time[keep]
        turret = np.full(len(times), np.nan)
        step = np.full(len(times), np.nan)
        if vid in dec.guns:
            gt, gc = dec.guns[vid]
            j = np.searchsorted(gt, times, side="right") - 1
            codes = gc[np.clip(j, 0, None)]
            turret = np.where(j >= 0, ((codes >> 6) & 1023) * 2 * np.pi / 1024 - np.pi, np.nan)
            step = np.where(j >= 0, codes & 63, np.nan)
        pitch, roll = t.pitch[keep], t.roll[keep]
        in_table.update(t.offset[keep].tolist())
        for k, (tt, x, y, z, yaw) in enumerate(zip(times, t.x[keep], t.y[keep], t.z[keep], t.yaw[keep])):
            m.add(match=match_id, map=map_id, time=float(tt), battleTime=_bt(tt, start), event="position",
                  x=x, y=y, z=z, dirX=math.sin(yaw), dirY=0.0, dirZ=math.cos(yaw), turretYaw=turret[k],
                  gunStep=step[k], pitch=pitch[k], roll=roll[k], **w)

    # Each death twice, as the 3DHeat CS2 tables have it: "death" where the victim fell, "kill" where the killer stood.
    for vid, r in vres.items():
        t = deaths.get(vid)
        if t is None:
            continue
        killer = int(r.get("killerID") or 0)
        victim_w, killer_w = who(vid), who(killer) if killer in roster else None
        reason = r.get("deathReason")
        vt = tracks.get(vid)
        i = _fresh(vt, t)
        if i is not None:
            m.add(match=match_id, map=map_id, time=t, battleTime=_bt(t, start), event="death",
                  x=vt.x[i], y=vt.y[i], z=vt.z[i], other=killer_w["player"] if killer_w else None,
                  reason=str(reason), text=ATTACK_REASONS.get(reason), **victim_w)
        kt = tracks.get(killer) if killer_w else None
        k = _fresh(kt, t)
        if killer_w and k is not None and killer != vid:
            m.add(match=match_id, map=map_id, time=t, battleTime=_bt(t, start), event="kill",
                  x=kt.x[k], y=kt.y[k], z=kt.z[k], other=victim_w["player"], reason=str(reason),
                  text=ATTACK_REASONS.get(reason), **killer_w)

    # Health changes: "hurt" where the victim was, "damage" where the attacker was.
    for h in dec.health:
        dmg = h.old - max(h.new, 0)
        about = dict(value=dmg, health=h.new, reason=str(h.reason), text=ATTACK_REASONS.get(h.reason))
        add("hurt", h.time, h.victim, where(h.victim, h.time), other=label(h.attacker), **about)
        if h.attacker and h.attacker != h.victim:
            add("damage", h.time, h.attacker, where(h.attacker, h.time), other=label(h.victim), **about)

    # Shells striking a vehicle, those that did no damage too: at the victim, the attacker as `other`.
    changes = {(round(h.time, 1), h.victim): h.old - max(h.new, 0) for h in dec.health}
    for x in dec.hits:
        if x.damage is not None:
            dmg = x.damage
        else:
            dmg = changes.get((round(x.time, 1), x.victim), 0) if x.factor else 0
        # One row a point struck: the part's collision component, a code, where the shell went in and where
        # its path ended, as fractions of the component's box (`stream.hit_point`); the damage on the first.
        points = [p for p in (st.hit_point(r) for r in x.raw) if p is not None] or [None]
        # The victim's turret then (a turret or gun component's box turns with it), and the way the shell came
        # in the hull's frame (x forward, y up, z right), from the attacker's place: the hull's yaw turns it.
        turret, came = None, {}
        if x.victim in dec.guns:
            gt, gc = dec.guns[x.victim]
            j = int(np.searchsorted(gt, x.time, side="right")) - 1
            turret = st.gun_yaw(int(gc[j])) if j >= 0 else None
        vi = _fresh(tracks.get(x.victim), x.time)
        ap = where(x.attacker, x.time)
        if vi is not None and ap is not None:
            vt = tracks[x.victim]
            dx, dy, dz = float(vt.x[vi]) - ap[0], float(vt.y[vi]) - ap[1], float(vt.z[vi]) - ap[2]
            n = math.sqrt(dx * dx + dy * dy + dz * dz)
            if n > 0:
                yaw = float(vt.yaw[vi])
                came = dict(hitDirX=(dx * math.sin(yaw) + dz * math.cos(yaw)) / n, hitDirY=dy / n,
                            hitDirZ=(dx * math.cos(yaw) - dz * math.sin(yaw)) / n)
        for k, p in enumerate(points):
            at = {} if p is None else dict(hitComponent=p["component"], hitCode=p["code"], hitU=p["entry"][0],
                                           hitV=p["entry"][1], hitW=p["entry"][2], hitExitU=p["exit"][0],
                                           hitExitV=p["exit"][1], hitExitW=p["exit"][2])
            add("struck", x.time, x.victim, where(x.victim, x.time), other=label(x.attacker),
                value=dmg if k == 0 else None, text=f"effects {x.effects}, point {k + 1} of {x.points}",
                turretYaw=turret, **at, **came)

    # Shots, tracers and explosions. A shot's direction is its tracer's, else the hull's and turret's.
    by_shooter: dict[int, list[st.Tracer]] = {}
    for tr in dec.tracers:
        if tr.shooter is not None:
            by_shooter.setdefault(tr.shooter, []).append(tr)
    shooter_of = {tr.shot: tr.shooter for tr in dec.tracers if tr.shooter is not None}
    for t_shot, vid, burst in dec.shots:
        pos = where(vid, t_shot)
        matched = [tr for tr in by_shooter.get(vid, []) if abs(tr.time - t_shot) <= 0.15]
        d = None
        if matched:
            v = np.array(matched[0].velocity)
            if np.linalg.norm(v) > 0:
                d = v / np.linalg.norm(v)
        elif pos is not None and vid in dec.guns:
            hull = tracks[vid]
            i = hull.at(t_shot)
            gt, gc = dec.guns[vid]
            j = int(np.searchsorted(gt, t_shot, side="right")) - 1
            if i is not None and j >= 0:
                a = float(hull.yaw[i]) + st.gun_yaw(int(gc[j]))
                d = np.array([math.sin(a), 0.0, math.cos(a)])
        dirs = dict(dirX=d[0], dirY=d[1], dirZ=d[2]) if d is not None else {}
        add("shot", t_shot, vid, pos, value=burst, shot=matched[0].shot if matched else None, **dirs)
    for tr in dec.tracers:
        v = np.array(tr.velocity)
        speed = float(np.linalg.norm(v))
        dirs = dict(dirX=v[0] / speed, dirY=v[1] / speed, dirZ=v[2] / speed) if speed > 0 else {}
        add("tracer", tr.time, tr.shooter if tr.shooter in roster else None, tr.start, value=speed, shot=tr.shot,
            text="shooter inferred" if tr.inferred else None, **dirs)
    for im in dec.impacts:
        shooter = shooter_of.get(im.shot)
        add("impact", im.time, shooter if shooter in roster else None, im.point, shot=im.shot)

    # Chat, battle chat commands, and what the recording player did with the camera.
    by_name = {str(v.get("name")): vid for vid, v in roster.items()}
    for t, sender, said in dec.chat:
        vid = by_name.get(sender.split(" (")[0].strip())
        add("chat", t, vid, where(vid, t), text=said)
    commands = []
    own_vid = next((vid for vid, v in roster.items() if me and v.get("name") == me), None)
    for t, nm, value in dec.client:
        v = bw.plain(value)
        if nm.startswith("bw_chat2") and isinstance(v, list) and len(v) >= 3:
            args = v[2] if isinstance(v[2], dict) else {}
            if "class" in args:  # the game's FixedDict, pickled with its contents as the argument
                args = (args.get("args") or [{}])[0] or args.get("state") or {}
            args = args if isinstance(args, dict) else {}
            sender = args.get("int64Arg1") if args.get("int64Arg1") in roster else None
            target = args.get("int32Arg1") if args.get("int32Arg1") in roster else None
            point = None
            raw = args.get("strArg2")
            if isinstance(raw, str) and len(raw) == 24:
                try:
                    point = bw.vec3(bytes.fromhex(raw), 0)
                except ValueError:
                    point = None
            commands.append({"time": round(t, 2), "action": v[0], "sender": label(sender), "target": label(target),
                             "point": list(point) if point else None, "args": args})
            text = args.get("strArg1") if isinstance(args.get("strArg1"), str) and args.get("strArg1").isprintable() else None
            add("command", t, sender, point or where(sender, t), value=v[0], other=label(target), text=text)
        elif nm == "applyZoom" and own_vid is not None:
            add("zoom", t, own_vid, where(own_vid, t), value=v if isinstance(v, (int, float)) else None)
        elif nm in ("showAutoAimMarker", "hideAutoAimMarker") and own_vid is not None:
            target = v if isinstance(v, int) else None
            add("lock" if nm.startswith("show") else "unlock", t, own_vid, where(own_vid, t), other=label(target))
    camera = []
    for t, mode in dec.camera:
        if re.fullmatch(r"[\d.]+", mode):
            continue  # the client's version, written once at the start
        camera.append({"time": round(t, 2), "mode": mode})
        if own_vid is not None:
            add("camera", t, own_vid, where(own_vid, t), text=mode)

    seen_damage: dict[int, int] = {}
    seen_received: dict[int, int] = {}
    for h in dec.health:
        dmg = h.old - max(h.new, 0)
        seen_received[h.victim] = seen_received.get(h.victim, 0) + dmg
        if h.attacker:
            seen_damage[h.attacker] = seen_damage.get(h.attacker, 0) + dmg
    seen_shots = Counter(vid for _, vid, _b in dec.shots)
    accounts = results.get("players") or {}
    players = []
    for vid, v in sorted(roster.items(), key=lambda kv: (str(kv[1].get("team")), str(kv[1].get("name")))):
        r = vres.get(vid, {})
        t = tracks.get(vid)
        account = r.get("accountDBID")
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
            # What the recording client saw of this vehicle: its own team always, enemies while in range.
            "seen": {"shots": seen_shots.get(vid, 0), "damageDealt": seen_damage.get(vid, 0),
                     "damageReceived": seen_received.get(vid, 0)},
            "header": v,
            "results": r or None,
            "account": accounts.get(str(account)) if account is not None else None,
        })  # fmt: skip
    m.summary = {
        "format": "heat3d-wot-match",
        "version": 2,
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
        "region": head.get("regionCode"),
        "hasMods": head.get("hasMods"),
        "duration": common.get("duration"),
        "winnerTeam": common.get("winnerTeam"),
        "finishReason": common.get("finishReason"),
        "complete": bool(results),
        "truncated": rep.truncated,
        "battleStart": round(start, 2) if start is not None else None,
        "battleStartFrom": "arena" if arena["battleStart"] is not None else "movement",
        "firstMovement": round(moved, 2) if moved is not None else None,
        "recordingSeconds": round(float(idx["time"].max()), 2) if len(idx) else 0.0,
        "positionPacket": kind,
        "decoded": dec.found,
        "hz": bw.rate(tracks),
        "positions": int(sum(1 for e in m.rows["event"] if e == "position")),
        "events": dict(sorted(Counter(e for e in m.rows["event"] if e != "position").items())),
        "units": "metres; x east, y up, z north",
        "players": players,
        "kills": kills,
        "periods": arena["periods"],
        "basePoints": arena["basePoints"],
        "chat": [{"time": round(t, 2), "sender": who_, "text": said} for t, who_, said in dec.chat],
        "commands": commands,
        "camera": camera,
        "clientEvents": [{"time": round(t, 2), "name": nm, "value": bw.plain(v)} for t, nm, v in dec.client
                         if not nm.startswith("bw_chat2")],
        "arenaUpdates": [{"time": round(t, 2), "type": k, "value": bw.plain(v)} for t, k, v in dec.arena],
        # Everything else the file says, as it says it.
        "serverSettings": head.get("serverSettings"),
        "results": {k: v for k, v in results.items() if k != "vehicles"} or None,
        "resultVehicles": end_roster or None,
        "frags": frags or None,
    }  # fmt: skip
    # Everything else, whole, in the sidecar; what became of each kind of item in `selfCheck.completeness`.
    led, entities, entity_check = kept.ledger(rep, idx, dec, set(roster), kind, in_table)
    for i in range(len(rep.raw_blocks)):
        led.block(i, False, "header" if i == 0 else "results" if i == 1 else "")
    version = sc.version(led)
    m.summary["streamVersion"] = version
    m.summary["entities"] = entities
    m.messages, completeness = led.build(f"{slug(match_id)}.{sc.WHAT}.parquet")
    m.summary.setdefault("selfCheck", {}).update(
        completeness=completeness, entities=entity_check,
        streamVersionAgrees=None if version is None else version == _version(head) or version.startswith(_version(head)))
    return m


def _arena(dec: st.Decoded, roster: dict[int, dict]) -> dict[str, Any]:
    """
    The arena updates, told apart by their shape: the battle's periods (period, its end on the server's
    clock, its length, extra), base capture points (team, base, points, time left, invaders, capture
    stopped), and - in 1.x - kills (victim, killer, equipment, reason).
    """
    out: dict[str, Any] = {"periods": [], "basePoints": [], "killed": {}, "battleStart": None}
    by_type: dict[int, list] = {}
    for t, k, v in dec.arena:
        by_type.setdefault(k, []).append((t, v))

    def ints(v: Any, n: int) -> bool:
        return isinstance(v, tuple) and len(v) == n and all(isinstance(x, int) for x in v)

    def period(v: Any) -> bool:
        return (isinstance(v, tuple) and len(v) == 4 and isinstance(v[0], int) and 0 <= v[0] <= 4
                and isinstance(v[1], (int, float)) and isinstance(v[2], (int, float)))  # fmt: skip

    for items in by_type.values():
        values = [v for _, v in items]
        if all(period(v) for v in values):
            for t, v in items:
                out["periods"].append({"time": round(t, 2), "period": v[0], "name": PERIODS.get(v[0]),
                                       "endTime": v[1], "length": v[2], "info": bw.plain(v[3])})
                if v[0] == 3 and out["battleStart"] is None and t > 0:
                    out["battleStart"] = float(t)
        elif all(ints(v, 6) and v[0] in (1, 2) for v in values):
            for t, v in items:
                out["basePoints"].append({"time": round(t, 2), "team": v[0], "base": v[1], "points": v[2],
                                          "timeLeft": v[3], "invaders": v[4], "stopped": bool(v[5])})
        elif all((ints(v, 4) or ints(v, 5)) and v[0] in roster and (v[1] in roster or v[1] == 0) for v in values):
            for t, v in items:
                out["killed"].setdefault(v[0], (float(t), v[1], v[3]))
    return out


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
