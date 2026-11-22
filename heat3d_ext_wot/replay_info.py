"""
What a World of Tanks replay says about its battle, from the JSON blocks at
the head of the file only: the packet stream is neither deciphered nor read.

The first block (written when the battle began) gives the map, the client
version, the recording player, the date and the roster; the second (only when
the recording lasted to the end) gives the results: the battle's length, the
winning team and each vehicle's kills and damage.
"""

from __future__ import annotations

import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import bigworld as bw
from .replay import _results, _vehicle_results, _version

#: More blocks than a replay has, and a larger block than one holds: a file past these is not a replay.
MAX_BLOCKS = 16
MAX_BLOCK_BYTES = 64 << 20


def _head_bytes(path: Path) -> bytes:
    """The magic, the block count and the JSON blocks, read without the stream after them."""
    with open(path, "rb") as f:
        out = bytearray(f.read(8))
        if len(out) < 8:
            raise ValueError("not a World of Tanks replay: the file is too short")
        magic, count = struct.unpack("<II", out)
        if magic != bw.MAGIC or not 0 < count < MAX_BLOCKS:
            raise ValueError("not a World of Tanks replay")
        for _ in range(count):
            size = f.read(4)
            if len(size) < 4:
                raise ValueError("not a World of Tanks replay: the file ends inside its header")
            (n,) = struct.unpack("<I", size)
            if n > MAX_BLOCK_BYTES:
                raise ValueError("not a World of Tanks replay: a header block is too large")
            block = f.read(n)
            if len(block) < n:
                raise ValueError("not a World of Tanks replay: the file ends inside its header")
            out += size + block
        # `read_raw_blocks` wants at least 12 bytes; the stream's two sizes follow the blocks anyway.
        out += f.read(8)
    return bytes(out)


def _date(head: dict, common: dict) -> str | None:
    """The battle's start: the arena's creation time (a Unix time, so UTC), else the recording's local clock."""
    created = common.get("arenaCreateTime")
    if isinstance(created, (int, float)) and created > 0:
        return datetime.fromtimestamp(created, tz=timezone.utc).isoformat()
    text = head.get("dateTime")
    if isinstance(text, str):
        try:
            return datetime.strptime(text.strip(), "%d.%m.%Y %H:%M:%S").isoformat()
        except ValueError:
            return None
    return None


def _int(v: Any) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def info(path: Path) -> dict:
    """The battle a World of Tanks replay holds: map, mode, date, length, players, teams, outcome, version."""
    try:
        blocks, _raw, _at = bw.read_raw_blocks(_head_bytes(Path(path)))
    except ValueError as e:
        msg = str(e)
        raise ValueError(msg if msg.startswith("not a World of Tanks") else f"not a World of Tanks replay: {msg}") from e
    head = blocks[0] if blocks and isinstance(blocks[0], dict) else None
    if not head or "mapName" not in head:
        raise ValueError("not a World of Tanks replay: no battle header")
    roster = head.get("vehicles")
    # World of Warships writes the same container, its roster a list and its maps under spaces/.
    if isinstance(roster, list) or str(head.get("mapName")).startswith("spaces/"):
        raise ValueError("not a World of Tanks replay: a World of Warships one")
    results, end_roster, _frags = _results(blocks)
    common = results.get("common") or {}
    vres = _vehicle_results(results)
    me = str(head.get("playerName") or "")

    # The header's roster, then the results' for vehicles it leaves out (as the converter does).
    vehicles: dict[int, dict] = {}
    for source in (roster if isinstance(roster, dict) else {}, end_roster):
        for vid, v in source.items():
            if isinstance(v, dict) and _int(vid) is not None:
                vehicles.setdefault(int(vid), v)
    players = []
    for vid, v in sorted(vehicles.items(), key=lambda kv: (str(kv[1].get("team")), str(kv[1].get("name")))):
        r = vres.get(vid, {})
        players.append({
            "name": v.get("name") or v.get("fakeName"),
            "team": _int(v.get("team")),
            "vehicle": v.get("vehicleType") or None,
            "clan": v.get("clanAbbrev") or None,
            "own": bool(me and v.get("name") == me),
            "kills": r.get("kills"),
            "damage": r.get("damageDealt"),
            "survived": None if not r else r.get("deathReason", -1) == -1,
        })  # fmt: skip
    teams = [{"id": t} for t in sorted({p["team"] for p in players if p["team"] is not None})]

    outcome = None
    winner = _int(common.get("winnerTeam"))
    if winner is not None:
        mine = next((p["team"] for p in players if p["own"]), None)
        if winner == 0:
            result = "draw"
        elif mine is not None:
            result = "win" if mine == winner else "loss"
        else:
            result = None
        outcome = {"winner": winner or None, "result": result}

    duration = common.get("duration")
    gameplay = head.get("gameplayID")
    return {
        "map": str(head.get("mapName")),
        "map_title": head.get("mapDisplayName") or None,
        "mode": str(gameplay) if gameplay else None,
        "battle_type": _int(head.get("battleType")),
        "match": str(results.get("arenaUniqueID") or "") or None,
        "date": _date(head, common),
        "duration_s": float(duration) if isinstance(duration, (int, float)) else None,
        "players": players,
        "teams": teams,
        "outcome": outcome,
        "game_version": _version(head) or None,
        "player": me or None,
        "complete": bool(results),
    }
