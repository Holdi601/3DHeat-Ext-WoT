"""
What of a World of Tanks replay is read, and what is kept whole: the marks
on every item for `sidecar.Ledger`, so that the sidecar
`<match>.messages.parquet` holds everything the table and the match document
do not, and the match document says how much of each kind there was.

Items read in part (`partial`) carry what was read as JSON in the sidecar's
`decoded`; the layouts are the ones `stream` finds (see there):

| Item | `decoded` |
|---|---|
| position (in the table) | none: x, y, z, yaw, pitch, roll are the table's row |
| health (vehicle method) | new, old, attacker, reason, rest (hex) |
| health (vehicle property) | health |
| gun angles (vehicle property) | code, yawStep (turret yaw: yawStep * 2 pi / 1024 - pi), gunStep |
| shot (vehicle method) | burst, rest |
| hit (vehicle method) | attacker, points (each as `stream.hit_point`), effects, factor, damage, tail (hex) |
| tracer (avatar method) | shot, shooter, start, velocity |
| explosion (avatar method) | shot, point |
| arena update (avatar method) | type, value (the pickle as JSON) |
| chat, camera, client event (packets) | line / mode / name and value |
| entity created (packets 0, 5) | entity, entityType |
| aim (packet of 40 bytes) | forward: +z turned by the rotation in its first four floats (x, y, z, w), where the recording player aims |
"""

from __future__ import annotations

import html
import re
import struct
from typing import Any

import numpy as np

from . import bigworld as bw
from . import sidecar as sc
from . import stream as st

_TAGS = re.compile(r"<[^>]*>")


def _calls(calls: list[bw.Call], kind: int, method: int, roster: set[int], on_roster: bool) -> list[bw.Call]:
    return [c for c in calls if c.type == kind and c.method == method and (c.entity in roster) == on_roster]


def ledger(rep: bw.Replay, idx: np.ndarray, dec: st.Decoded, roster: set[int], position: int | None,
           in_table: set[int]) -> tuple[sc.Ledger, list[dict[str, Any]], dict[str, Any]]:
    """
    The marks for a replay read by `replay.read`: `position` the position
    packet type, `in_table` the offsets of the position packets that are rows
    of the table. Returns the ledger, the entities (for the match document)
    and their check.
    """
    led = sc.Ledger(rep, idx)
    stream = rep.stream
    first = idx[(idx["type"] == 0) & (idx["size"] >= 4)]
    player = struct.unpack_from("<I", stream, int(first[0]["at"]))[0] if len(first) else None
    # Roles of the entity types: the avatar is what packet 0 creates; vehicles are the roster's.
    roles: dict[int, str] = {}
    if player is not None and player in led.types:
        roles[led.types[player]] = "avatar"
    vt = [led.types[v] for v in roster if v in led.types]
    if vt:
        roles[max(set(vt), key=vt.count)] = "vehicle"
    ents, check = sc.entities(led, position, roles)
    check["roles"] = {str(k): v for k, v in sorted(roles.items())}

    if position is not None:
        led.names[f"packet {position}"] = "position"
        for at in in_table:
            led.partial(int(at), None, "position")
    kinds = [k for k in bw.call_types(stream, idx) if k in (st.PROPERTY, st.METHOD)]
    calls = bw.calls(stream, kinds, idx) if kinds else []
    found = dec.found

    def mark(cs: list[bw.Call], name: str, read) -> None:
        for c in cs:
            try:
                value = read(c.args)
            except (struct.error, IndexError, ValueError):
                value = None
            led.partial(c.at, value, name)

    if "health" in found:
        mark(_calls(calls, st.METHOD, found["health"], roster, True), "health",
             lambda a: dict(zip(("new", "old", "attacker", "reason"), struct.unpack_from("<hhIB", a)), rest=a[9:]))
    if "healthProperty" in found:
        mark(_calls(calls, st.PROPERTY, found["healthProperty"], roster, True), "health",
             lambda a: {"health": struct.unpack_from("<h", a)[0]})
    if "gunAngles" in found:
        mark(_calls(calls, st.PROPERTY, found["gunAngles"], roster, True), "gun angles",
             lambda a: {"code": (c := struct.unpack_from("<H", a)[0]), "yawStep": c >> 6, "gunStep": c & 63})
    if "shot" in found:
        mark(_calls(calls, st.METHOD, found["shot"], roster, True), "shot", lambda a: {"burst": a[0], "rest": a[1:]})
    if "hit" in found:
        size = found["hit"]["point"]

        def hit(a: bytes) -> dict[str, Any]:
            n = a[4]
            at = 5 + n * size
            tail = a[at:]
            return {"attacker": struct.unpack_from("<I", a)[0],
                    "points": [st.hit_point(a[5 + i * size : 5 + (i + 1) * size]) for i in range(n)],
                    "effects": tail[0] if tail else None,
                    "factor": tail[1] if len(tail) > 1 and len(tail) < 6 else None,
                    "damage": struct.unpack_from("<I", tail, 2)[0] if len(tail) >= 6 else None, "tail": tail}

        mark(_calls(calls, st.METHOD, found["hit"]["method"], roster, True), "hit", hit)
    if "impact" in found:
        mark(_calls(calls, st.METHOD, found["impact"], roster, False), "explosion",
             lambda a: {"shot": struct.unpack_from("<I", a)[0], "point": struct.unpack_from("<3f", a, 4)})
    for f in found.get("tracer", []):
        def tracer(a: bytes, f=f) -> dict[str, Any]:
            return {"shot": struct.unpack_from("<I", a, f["shot"])[0],
                    "shooter": struct.unpack_from("<I", a, f["shooter"])[0] if f["shooter"] is not None else None,
                    "start": struct.unpack_from("<3f", a, f["start"]),
                    "velocity": struct.unpack_from("<3f", a, f["start"] + 12)}

        mark(_calls(calls, st.METHOD, f["method"], roster, False), "tracer", tracer)
    if "arena" in found:
        def arena(a: bytes) -> dict[str, Any]:
            raw, _ = bw.bw_string(a, 1)
            return {"type": a[0], "value": bw.plain(bw.unpickle(raw))}

        mark(_calls(calls, st.METHOD, found["arena"], roster, False), "arena update", _safe(arena))
    _packets(led, idx, stream, found)
    _aim(led, idx, stream)
    return led, ents, check


def _aim(led: sc.Ledger, idx: np.ndarray, stream: bytes) -> None:
    """
    The recording player's aim, ten times a second: a packet of 40 bytes
    that begins with a rotation (x, y, z, w, of length 1) turning +z (the
    world's north) to where the player aims. Found as the packet type of that
    size whose first four floats have length 1. Checked: at the recording
    player's shots, its +z is a median 0.14-0.56 degrees from the way the
    shell flew (the 1.12 and 2.4.1 replays). The six floats after it are kept,
    not read.
    """
    best, best_n = None, 0
    for kind in np.unique(idx["type"][idx["size"] == 40]):
        rows = idx[(idx["type"] == kind) & (idx["size"] == 40)]
        if len(rows) < 20 or len(rows) < 0.99 * int((idx["type"] == kind).sum()):
            continue
        q = np.array([struct.unpack_from("<4f", stream, int(r["at"])) for r in rows[:: max(1, len(rows) // 200)]])
        if np.mean(np.abs(np.linalg.norm(q, axis=1) - 1) < 1e-3) >= 0.95 and len(rows) > best_n:
            best, best_n = int(kind), len(rows)
    if best is None:
        return
    led.names[f"packet {best}"] = "aim"
    for r in idx[(idx["type"] == best) & (idx["size"] == 40)]:
        x, y, z, w = struct.unpack_from("<4f", stream, int(r["at"]))
        # +z turned by the rotation: the third column of its matrix.
        fwd = (2 * (x * z + w * y), 2 * (y * z - w * x), 1 - 2 * (x * x + y * y))
        led.partial(int(r["at"]), {"forward": [round(v, 5) for v in fwd]}, "aim")


def _safe(read):
    """`read`, with anything it cannot read (a pickle that does not load) as None rather than an error."""
    def inner(a: bytes):
        try:
            return read(a)
        except Exception:  # noqa: BLE001 - what is not read stays raw, whole
            return None

    return inner


def _texts(idx: np.ndarray, stream: bytes) -> list[int]:
    """
    The packet types `stream` takes for the camera mode: a length and as many printable bytes, 40 at most. More
    than one fits (the camera mode, the version, a 32-digit hex string): `found` names only the last.
    """
    out = []
    for kind in np.unique(idx["type"]):
        rows = idx[idx["type"] == kind]
        if int(kind) in (st.PROPERTY, st.METHOD) or not len(rows) or any(int(r["size"]) > 40 for r in rows):
            continue
        ok = True
        for r in rows:
            p = stream[int(r["at"]) : int(r["at"]) + int(r["size"])]
            ok = ok and len(p) >= 5 and struct.unpack_from("<I", p)[0] == len(p) - 4 and all(32 <= b < 127 for b in p[4:])
        if ok:
            out.append(int(kind))
    return out


def _packets(led: sc.Ledger, idx: np.ndarray, stream: bytes, found: dict[str, Any]) -> None:
    """Chat, camera modes (and other short texts in the same layout) and client events: read in part."""
    keys = [(found[k], k, n) for k, n in (("chat", "chat"), ("client", "client event")) if k in found]
    for kind in _texts(idx, stream):
        texts = {stream[int(r["at"]) + 4 : int(r["at"]) + int(r["size"])] for r in idx[idx["type"] == kind]}
        # The camera's modes are words (`arcade`, `sniper`, ...), and more than one; other texts are kept unnamed.
        keys.append((kind, "camera", "camera" if all(t.isalpha() for t in texts) else ""))
    for kind, key, name in keys:
        if name:
            led.names[f"packet {kind}"] = name
        for r in idx[idx["type"] == kind]:
            at, size = int(r["at"]), int(r["size"])
            p = stream[at : at + size]
            try:
                n = struct.unpack_from("<I", p)[0]
                if key == "chat":
                    line = p[4 : 4 + n].decode("utf-8", "replace")
                    value = {"line": html.unescape(_TAGS.sub("", line)).replace("\xa0", " ").strip()}
                elif key == "camera":
                    value = {"mode" if name else "text": p[4 : 4 + n].decode("ascii", "replace")}
                else:
                    m = struct.unpack_from("<I", p, 4 + n)[0]
                    value = {"name": p[4 : 4 + n].decode("ascii", "replace"),
                             "value": _safe(lambda b: bw.plain(bw.unpickle(b)))(p[8 + n : 8 + n + m])}
            except (struct.error, ValueError):
                continue
            led.partial(at, value, name)
