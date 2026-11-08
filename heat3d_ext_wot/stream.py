"""
Everything in a World of Tanks packet stream besides the positions, found by
shape rather than by number.

The engine numbers an entity's methods and properties by their place in the
game's definition files, which change with patches: 1.12 and 2.4 number the
same calls differently. So each kind is found by what its arguments look like
and how they hang together, and the numbers found are written into the match
summary (`decoded`). What is read:

- **Health** (a vehicle method): new health int16, old health int16, the
  attacker's entity id uint32, the attack reason uint8 (and in 2.x one more
  byte). Found as the method whose calls chain - each call's old health is
  the previous call's new one.
- **Shots** (a vehicle method of 2 or 3 bytes: the burst count first): found
  as the one whose calls coincide with tracers.
- **Tracers and explosions** (methods of the client's own avatar): a shot's id
  then, in a tracer, its start point and velocity; in an explosion, the point.
  Found by the shot ids the two share; the start point by the offset at which
  the velocity points at the explosion. Tracers whose explosion the client
  never saw are found by the same layout and shot ids from the same counter.
  Most carry the shooter's id; those that do not (1.x and 2.x: shells of
  shooters out of sight) get the one vehicle that fired within 0.15 s, if
  only one did.
- **Hits** (a vehicle method): the attacker's id, a count of points struck
  (8 bytes each in 1.x, 16 in 2.x), the effects index, then the damage factor
  (1.x) or the damage itself (2.x) - shells that bounced or did not
  penetrate too.
- **Gun angles** (a vehicle property of 2 bytes, the most frequent one): the
  turret's yaw relative to the hull in the top 10 bits (code 512 straight
  ahead), the gun's elevation in the low 6 bits as a step of the gun's own
  limits (which the replay does not hold).
- **Arena updates** (an avatar method: update type uint8, a pickled payload):
  the battle's periods, base capture points, kills (1.x), frags, players
  ready. Read with a pickle reader that runs nothing (`bigworld.unpickle`).
- **Chat** (a packet of its own: length and the line as the client shows it,
  in HTML).
- **Client events** (a packet of its own: a name and a pickle): battle chat
  commands with their map points, zoom, auto-aim lock.
- **Camera mode** (a packet of its own: length and the mode's name).
"""

from __future__ import annotations

import html
import re
import struct
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from . import bigworld as bw

PROPERTY, METHOD = 7, 8


@dataclass
class Health:
    time: float
    victim: int
    new: int
    old: int
    attacker: int
    reason: int


@dataclass
class Tracer:
    time: float
    shot: int
    shooter: int | None
    start: tuple[float, float, float]
    velocity: tuple[float, float, float]
    #: True when the shooter was worked out (nearest vehicle that fired), not read.
    inferred: bool = False


@dataclass
class Impact:
    time: float
    shot: int
    point: tuple[float, float, float]


@dataclass
class Decoded:
    health: list[Health] = field(default_factory=list)
    shots: list[tuple[float, int, int]] = field(default_factory=list)  # time, vehicle, burst
    tracers: list[Tracer] = field(default_factory=list)
    hits: list["Hit"] = field(default_factory=list)
    impacts: list[Impact] = field(default_factory=list)
    #: entity -> (times, packed gun angles)
    guns: dict[int, tuple[np.ndarray, np.ndarray]] = field(default_factory=dict)
    arena: list[tuple[float, int, Any]] = field(default_factory=list)
    chat: list[tuple[float, str, str]] = field(default_factory=list)  # time, sender, text
    client: list[tuple[float, str, Any]] = field(default_factory=list)
    camera: list[tuple[float, str]] = field(default_factory=list)
    #: What was found where: method and packet numbers, for the summary.
    found: dict[str, Any] = field(default_factory=dict)


def _by_method(calls: list[bw.Call]) -> dict[tuple[int, int], list[bw.Call]]:
    out: dict[tuple[int, int], list[bw.Call]] = defaultdict(list)
    for c in calls:
        out[(c.type, c.method)].append(c)
    return out


# ------------------------------------------------------------------ health


def _health_method(groups: dict, roster: set[int]) -> int | None:
    best, best_n = None, 0
    for (kind, m), cs in groups.items():
        if kind != METHOD or not all(9 <= len(c.args) <= 12 for c in cs) or len(cs) < 2:
            continue
        ok = chained = 0
        last: dict[int, int] = {}
        for c in cs:
            new, old, attacker = struct.unpack_from("<hhI", c.args)
            if new < old and (attacker == 0 or attacker in roster):
                ok += 1
            if last.get(c.entity) == old:
                chained += 1
            last[c.entity] = new
        repeats = len(cs) - len(last)
        if ok >= 0.9 * len(cs) and (repeats == 0 or chained >= 0.8 * repeats) and len(cs) > best_n:
            best, best_n = m, len(cs)
    return best


# --------------------------------------------------------- tracers, impacts


def _impact_candidates(groups: dict) -> dict[int, list[bw.Call]]:
    out = {}
    for (kind, m), cs in groups.items():
        if kind == METHOD and len(cs) >= 3 and all(len(c.args) == 16 for c in cs):
            if sum(bw.vec3(c.args, 4) is not None for c in cs) >= 0.95 * len(cs):
                out[m] = cs
    return out


def _tracers(groups: dict, roster: set[int], dec: Decoded) -> None:
    impacts = _impact_candidates(groups)
    if not impacts:
        return
    ids = {m: {struct.unpack_from("<I", c.args)[0] for c in cs} for m, cs in impacts.items()}
    found: list[tuple[int, int, int]] = []  # method, shot id offset, impact method
    for (kind, m), cs in groups.items():
        if kind != METHOD or m in impacts or len(cs) < 3 or min(len(c.args) for c in cs) < 28:
            continue
        for off in (0, 4):
            for im, s in ids.items():
                hit = sum(struct.unpack_from("<I", c.args, off)[0] in s for c in cs)
                if hit >= 0.3 * len(cs):
                    found.append((m, off, im))
    if not found:
        return
    impact_m = Counter(im for _, _, im in found).most_common(1)[0][0]
    points = {}
    for c in impacts[impact_m]:
        shot = struct.unpack_from("<I", c.args)[0]
        dec.impacts.append(Impact(c.time, shot, bw.vec3(c.args, 4)))
        points.setdefault(shot, bw.vec3(c.args, 4))
    dec.found["impact"] = impact_m
    dec.found["tracer"] = []
    for m, off, im in found:
        if im != impact_m:
            continue
        cs = groups[(METHOD, m)]
        size = min(len(c.args) for c in cs)
        # The start point is where the velocity after it points at the explosion of the same shot.
        best_k, best_score = None, 0.0
        for k in range(off + 4, size - 23):
            score = n = 0
            for c in cs[:400]:
                shot = struct.unpack_from("<I", c.args, off)[0]
                end = points.get(shot)
                start, vel = bw.vec3(c.args, k), struct.unpack_from("<3f", c.args, k + 12)
                if end is None:
                    continue
                n += 1
                if start is None or not all(np.isfinite(vel)):
                    continue
                d = np.array(end) - np.array(start)
                v = np.array(vel)
                if np.linalg.norm(d) > 1 and np.linalg.norm(v) > 1:
                    score += float(d @ v / np.linalg.norm(d) / np.linalg.norm(v)) > 0.9
            if n and score / n > best_score:
                best_k, best_score = k, score / n
        if best_k is None or best_score < 0.6:
            continue
        # The shooter: an entity id of the roster before the shot id, when there is one.
        shooter_at = None
        for o in (0, 4):
            if o != off and o + 4 <= best_k and sum(struct.unpack_from("<I", c.args, o)[0] in roster for c in cs) >= 0.9 * len(cs):
                shooter_at = o
        dec.found["tracer"].append({"method": m, "shot": off, "start": best_k, "shooter": shooter_at})
        _add_tracers(dec, cs, off, best_k, shooter_at)
    if not dec.tracers:
        return
    # Tracers of shells whose explosion the client never saw (2.x: those of unseen shooters) have
    # the same layout after the shot id as a tracer found above, and shot ids from the same counter.
    lay = dec.found["tracer"][0]
    gap = lay["start"] - lay["shot"]
    lo, hi = min(t.shot for t in dec.tracers), max(t.shot for t in dec.tracers)
    lo, hi = lo - (hi - lo) // 10 - 1000, hi + (hi - lo) // 10 + 1000
    known = {f["method"] for f in dec.found["tracer"]}
    for (kind, m), cs in groups.items():
        if kind != METHOD or m in known or m in impacts or len(cs) < 3 or min(len(c.args) for c in cs) < gap + 24:
            continue
        for off in (0, 4):
            ok = sum(lo <= struct.unpack_from("<I", c.args, off)[0] <= hi and bw.vec3(c.args, off + gap) is not None for c in cs)
            if ok >= 0.9 * len(cs):
                dec.found["tracer"].append({"method": m, "shot": off, "start": off + gap, "shooter": None})
                _add_tracers(dec, cs, off, off + gap, None)
                break
    dec.tracers.sort(key=lambda t: t.time)


def _add_tracers(dec: Decoded, cs: list[bw.Call], off: int, start_at: int, shooter_at: int | None) -> None:
    for c in cs:
        shot = struct.unpack_from("<I", c.args, off)[0]
        start = bw.vec3(c.args, start_at)
        vel = struct.unpack_from("<3f", c.args, start_at + 12)
        if start is None or not all(np.isfinite(vel)):
            continue
        shooter = struct.unpack_from("<I", c.args, shooter_at)[0] if shooter_at is not None else None
        dec.tracers.append(Tracer(c.time, shot, shooter, start, tuple(float(v) for v in vel)))


# -------------------------------------------------------------------- hits


@dataclass
class Hit:
    """A shell that struck a vehicle, as the vehicle was told: who fired, how many points it touched."""

    time: float
    victim: int
    attacker: int
    points: int
    effects: int
    #: The damage factor: 0 when the shell did no damage (bounced, or stopped by the armour).
    factor: int
    #: The damage it did (2.x, which says so), else None.
    damage: int | None = None
    #: Each point struck as sent (8 bytes in 1.x, 16 in 2.x) - `hit_point` reads them.
    raw: list[bytes] = field(default_factory=list)


def hit_point(raw: bytes) -> dict[str, Any] | None:
    """
    One struck point: the vehicle part's collision component (its index),
    a code, and where the shell went in and where its path ended, each a
    point of 8 bits an axis inside the component's bounding box (0 its
    least, 255 its most: u across, v up, w along, as the box's own x, y, z).
    1.x sends these 8 bytes alone; 2.x the same 8 after four zero bytes,
    and three more bytes after them (`extra`, not known).
    """
    if len(raw) == 16:
        body, extra = raw[4:12], raw[12:15].hex()
    elif len(raw) == 8:
        body, extra = raw, ""
    else:
        return None
    return {"component": body[0], "code": body[1], "entry": tuple(b / 255 for b in body[2:5]),
            "exit": tuple(b / 255 for b in body[5:8]), "extra": extra}


def _hits(groups: dict, roster: set[int], dec: Decoded, health_m: int | None) -> None:
    """
    The vehicle method an attacker's id begins, then a count of hit points
    of a fixed size each (8 bytes in 1.x, 16 in 2.x), then a fixed tail
    beginning with the effects index and the damage factor.
    """
    for (kind, m), cs in groups.items():
        if kind != METHOD or m == health_m or len(cs) < 3:
            continue
        if sum(len(c.args) >= 7 and struct.unpack_from("<I", c.args)[0] in roster for c in cs) < 0.95 * len(cs):
            continue
        for size in (16, 8):  # the larger first: with one point per call both fit, and 2.x's is 16
            tails = Counter(len(c.args) - 5 - c.args[4] * size for c in cs if len(c.args) >= 7)
            tail, n = tails.most_common(1)[0]
            if tail >= 2 and n >= 0.95 * len(cs) and len({c.args[4] for c in cs}) >= 1 and all(1 <= c.args[4] <= 16 for c in cs):
                dec.found["hit"] = {"method": m, "point": size, "tail": tail}
                for c in cs:
                    at = 5 + c.args[4] * size
                    if len(c.args) != at + tail:
                        continue
                    # 2.x: effects index, a byte, the damage uint32, ...; 1.x: effects index, damage factor.
                    damage = struct.unpack_from("<I", c.args, at + 2)[0] if tail >= 6 else None
                    factor = c.args[at + 1] if tail < 6 else int(bool(damage))
                    raw = [bytes(c.args[5 + i * size: 5 + (i + 1) * size]) for i in range(c.args[4])]
                    dec.hits.append(Hit(c.time, c.entity, struct.unpack_from("<I", c.args)[0], c.args[4], c.args[at],
                                        factor, damage, raw))
                return


def _shot_method(groups: dict, roster: set[int], dec: Decoded, health_m: int | None) -> int | None:
    """The 2-3 byte vehicle method, burst count first, whose calls coincide with tracers most."""
    times = np.array(sorted(t.time for t in dec.tracers))
    best, best_score = None, -1.0
    for (kind, m), cs in groups.items():
        if kind != METHOD or m == health_m or len(cs) < 2:
            continue
        if not all(2 <= len(c.args) <= 3 and 1 <= c.args[0] <= 10 and c.entity in roster for c in cs):
            continue
        if len({len(c.args) for c in cs}) != 1:
            continue
        if len(times):
            near = sum(_near(times, c.time, 0.15) for c in cs) / len(cs)
        else:
            near = 0.0
        if near > best_score:
            best, best_score = m, near
    if best is not None and len(times) and best_score < 0.5:
        return None
    return best


def _near(times: np.ndarray, t: float, tol: float) -> bool:
    i = int(np.searchsorted(times, t))
    return any(0 <= j < len(times) and abs(times[j] - t) <= tol for j in (i - 1, i))


# ----------------------------------------------------------- arena, packets


def _arena(groups: dict, roster: set[int], dec: Decoded) -> None:
    for (kind, m), cs in groups.items():
        if kind != METHOD or len(cs) < 3 or any(c.entity in roster for c in cs):
            continue
        out, ok = [], 0
        for c in cs:
            try:
                raw, end = bw.bw_string(c.args, 1)
                if end != len(c.args) or raw[:1] not in (b"\x80", b"\x78"):
                    continue
                out.append((c.time, c.args[0], bw.unpickle(raw)))
                ok += 1
            except Exception:  # noqa: BLE001 - not this method
                continue
        if ok >= 0.9 * len(cs):
            dec.arena = out
            dec.found["arena"] = m
            return


_TAGS = re.compile(r"<[^>]*>")


def _packets(stream: bytes, idx: np.ndarray, dec: Decoded) -> None:
    """Chat, client events and the camera mode: packets that say their own length and carry text."""
    for kind in np.unique(idx["type"]):
        rows = idx[idx["type"] == kind]
        if kind in (PROPERTY, METHOD) or not len(rows):
            continue
        first = stream[int(rows[0]["at"]) : int(rows[0]["at"]) + int(rows[0]["size"])]
        if len(first) < 5 or struct.unpack_from("<I", first)[0] > len(first) - 4:
            continue
        lead = first[4:16]
        if lead.startswith(b"<font") or lead.startswith(b"<"):
            dec.found["chat"] = int(kind)
            for r in rows:
                p = stream[int(r["at"]) : int(r["at"]) + int(r["size"])]
                text = p[4 : 4 + struct.unpack_from("<I", p)[0]].decode("utf-8", "replace")
                line = html.unescape(_TAGS.sub("", text)).replace("\xa0", " ").strip()
                sender, _, said = line.partition(" : ")
                if not said:
                    sender, _, said = line.partition(": ")
                dec.chat.append((float(r["time"]), sender.strip(), said.strip()))
        elif all(32 <= b < 127 for b in first[4:]) and len(first) <= 40 and struct.unpack_from("<I", first)[0] == len(first) - 4:
            if all(int(r["size"]) <= 40 for r in rows):
                dec.found["camera"] = int(kind)
                for r in rows:
                    p = stream[int(r["at"]) : int(r["at"]) + int(r["size"])]
                    dec.camera.append((float(r["time"]), p[4:].decode("ascii", "replace")))
        else:
            try:
                n = struct.unpack_from("<I", first)[0]
                name = first[4 : 4 + n]
                m = struct.unpack_from("<I", first, 4 + n)[0]
                if not name or not all(32 <= b < 127 for b in name) or 8 + n + m != len(first):
                    continue
            except struct.error:
                continue
            dec.found["client"] = int(kind)
            for r in rows:
                p = stream[int(r["at"]) : int(r["at"]) + int(r["size"])]
                try:
                    n = struct.unpack_from("<I", p)[0]
                    m = struct.unpack_from("<I", p, 4 + n)[0]
                    dec.client.append((float(r["time"]), p[4 : 4 + n].decode("ascii", "replace"), bw.unpickle(p[8 + n : 8 + n + m])))
                except Exception:  # noqa: BLE001 - one unreadable event is skipped
                    continue


# ---------------------------------------------------------------- the lot


def decode(stream: bytes, idx: np.ndarray, roster: set[int]) -> Decoded:
    dec = Decoded()
    kinds = [k for k in bw.call_types(stream, idx) if k in (PROPERTY, METHOD)]
    groups = _by_method(bw.calls(stream, kinds, idx)) if kinds else {}
    vehicle_groups = {k: [c for c in cs if c.entity in roster] for k, cs in groups.items()}
    vehicle_groups = {k: cs for k, cs in vehicle_groups.items() if cs}
    other_groups = {k: [c for c in cs if c.entity not in roster] for k, cs in groups.items()}
    other_groups = {k: cs for k, cs in other_groups.items() if cs}

    hm = _health_method(vehicle_groups, roster)
    if hm is not None:
        dec.found["health"] = hm
        for c in vehicle_groups[(METHOD, hm)]:
            new, old, attacker, reason = struct.unpack_from("<hhIB", c.args)
            dec.health.append(Health(c.time, c.entity, new, old, attacker, reason))

    _tracers(other_groups, roster, dec)
    _hits(vehicle_groups, roster, dec, hm)
    sm = _shot_method(vehicle_groups, roster, dec, hm)
    if sm is not None:
        dec.found["shot"] = sm
        dec.shots = [(c.time, c.entity, c.args[0]) for c in vehicle_groups[(METHOD, sm)]]
    _infer_shooters(dec)

    # Gun angles: the vehicles' most frequent 2-byte property, other than health.
    props = [(len(cs), m) for (k, m), cs in vehicle_groups.items() if k == PROPERTY and all(len(c.args) == 2 for c in cs)]
    health_prop = _health_property(vehicle_groups, dec)
    props = [p for p in props if p[1] != health_prop]
    if props:
        _, gm = max(props)
        dec.found["gunAngles"] = gm
        per: dict[int, list[tuple[float, int]]] = defaultdict(list)
        for c in vehicle_groups[(PROPERTY, gm)]:
            per[c.entity].append((c.time, struct.unpack_from("<H", c.args)[0]))
        dec.guns = {e: (np.array([t for t, _ in v]), np.array([g for _, g in v], dtype=np.int64)) for e, v in per.items()}
    if health_prop is not None:
        dec.found["healthProperty"] = health_prop

    _arena(other_groups, roster, dec)
    _packets(stream, idx, dec)
    return dec


def _health_property(groups: dict, dec: Decoded) -> int | None:
    """The 2-byte vehicle property whose values are the health method's new healths."""
    news = {(round(h.time, 1), h.victim): h.new for h in dec.health}
    if not news:
        return None
    for (k, m), cs in groups.items():
        if k != PROPERTY or not all(len(c.args) == 2 for c in cs):
            continue
        hit = sum(news.get((round(c.time, 1), c.entity)) == struct.unpack_from("<h", c.args)[0] for c in cs)
        if hit >= 0.5 * min(len(cs), len(news)):
            return m
    return None


def _infer_shooters(dec: Decoded) -> None:
    """A tracer without a shooter: the vehicle that fired then (within 0.15 s); several - left open."""
    if not dec.shots:
        return
    shots = sorted(dec.shots)
    times = np.array([s[0] for s in shots])
    for t in dec.tracers:
        if t.shooter is not None:
            continue
        i, j = np.searchsorted(times, t.time - 0.15), np.searchsorted(times, t.time + 0.15, side="right")
        who = {shots[k][1] for k in range(int(i), int(j))}
        if len(who) == 1:
            t.shooter, t.inferred = who.pop(), True


def gun_yaw(code: int) -> float:
    """The turret's yaw relative to the hull, radians, from a packed gun-angles code (+ to the right)."""
    return ((code >> 6) & 1023) * 2 * np.pi / 1024 - np.pi


def gun_pitch_step(code: int) -> int:
    """The gun's elevation as a step 0-63 of the gun's own limits (which are the tank's data, not the replay's)."""
    return code & 63
