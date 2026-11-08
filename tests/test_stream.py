"""
Everything besides positions, on a replay built here to the 2.x layout: health
changes, shots, tracers and explosions, gun angles, arena updates, chat,
battle chat commands, the camera. The method numbers are made up on purpose -
the reader must find them by shape.
"""

from __future__ import annotations

import math
import pickle
import struct

import pytest

from heat3d_ext_wot import bigworld as bw
from heat3d_ext_wot import stream as st
from heat3d_ext_wot.replay import KEY, read
from test_wot import ALLY, AVATAR, ENEMY, HEADER, ME, START, position, results

HEALTH, SHOT, HITS, TRACER, IMPACT, ARENA, GUN = 41, 3, 17, 52, 29, 77, 22
CHAT, CAMERA, CLIENT = 35, 27, 49


def call(kind: int, t: float, entity: int, method: int, args: bytes) -> bytes:
    return bw.packet(kind, t, struct.pack("<III", entity, method, len(args)) + args)


def arena(t: float, kind: int, value) -> bytes:
    raw = pickle.dumps(value, protocol=2)
    return call(8, t, AVATAR, ARENA, bytes([kind, len(raw)]) + raw)


def text(kind: int, t: float, s: str) -> bytes:
    raw = s.encode("utf-8")
    return bw.packet(kind, t, struct.pack("<I", len(raw)) + raw)


def client(t: float, name: str, value) -> bytes:
    raw = pickle.dumps(value, protocol=3)  # bytes as bytes, as the game's Python 2 writes its strings
    return bw.packet(CLIENT, t, struct.pack("<I", len(name)) + name.encode() + struct.pack("<I", len(raw)) + raw)


def stream() -> bytes:
    out = bytearray()
    out += arena(0.0, 3, (1, 1000.0, 60.0, (1, 1)))
    out += arena(0.0, 3, (2, 1010.0, 5, []))
    out += text(CAMERA, 0.0, "2.4.1.0")
    health = 2000
    shot_id = 7000
    for i in range(201):
        t = round(i / 10, 2)
        moving = max(0.0, t - START)
        out += bw.packet(10, t, position(ME, 10.0 * moving, 1.0, 0.0, math.pi / 2))
        out += bw.packet(10, t, position(ALLY, -50.0, 1.0, 5.0 * moving, 0.0))
        enemy = (100.0, 2.0, -100.0 + moving)
        out += bw.packet(10, t, position(ENEMY, *enemy, 0.0))
        out += bw.packet(10, t, position(AVATAR, 0.0, 0.0, 0.0, 0.0))
        if i == 50:
            out += arena(t, 3, (3, 2000.0, 900, []))  # the battle begins
            out += text(CAMERA, t, "sniper")
        if i % 10 == 0:
            # The turret turned 90 degrees right of the hull (code 768 in the top ten bits), gun at step 9.
            out += call(7, t, ME, GUN, struct.pack("<H", (768 << 6) | 9))
            out += call(7, t, ENEMY, GUN, struct.pack("<H", (512 << 6) | 30))
        if i in (60, 80, 100, 120):
            # I fire: the shot, my tracer, its explosion at the enemy, the enemy's health.
            me_x = 10.0 * moving
            shot_id += 1
            out += call(8, t, ME, SHOT, bytes([1, 0, 0]))
            vel = (enemy[0] - me_x, 0.0, enemy[2])
            out += call(8, t, AVATAR, TRACER, struct.pack("<II4sf3f3f", ME, shot_id, b"\x22\x03\x02\x04", 105.0,
                                                          me_x, 1.0, 0.0, *vel) + bytes(14))
            out += call(8, t + 0.05, AVATAR, IMPACT, struct.pack("<I3f", shot_id, *enemy))
            if i < 120:
                new = health - 400
                out += call(8, t + 0.05, ENEMY, HEALTH, struct.pack("<hhIBb", new, health, ME, 0, -1))
                out += call(8, t + 0.05, ENEMY, HITS, struct.pack("<IB", ME, 1) + POINT
                            + bytes([0x22, 3]) + struct.pack("<I", 400) + bytes(7))
                health = new
            else:
                out += call(8, t + 0.05, ENEMY, HITS, struct.pack("<IB", ME, 1) + bytes(16)
                            + bytes([0x22, 3]) + struct.pack("<I", 0) + bytes(7))  # bounced
        if i == 130:
            out += call(8, t, ENEMY, HEALTH, struct.pack("<hhIBb", 0, health, ME, 1, -1))  # burnt out
        if i == 70:
            out += text(CHAT, t, "<font color='#80D63A'>friend (G1)&nbsp;: </font><font color='#80D63A'>go left</font>")
            fixed = {"int32Arg1": 3, "int64Arg1": ALLY, "floatArg1": 0.0, "strArg1": "",
                     "strArg2": struct.pack("<3f", 20.0, 1.0, 30.0)}
            out += client(t, "bw_chat2.onActionReceived", (28, 0, fixed))
            out += client(t, "applyZoom", 4.0)
    return bytes(out)


def replay() -> bytes:
    return bw.encipher([HEADER, results(enemy_life=8)], stream(), KEY)


def rows(m, event):
    return [{c: v[i] for c, v in m.rows.items()} for i, e in enumerate(m.rows["event"]) if e == event]


def test_the_calls_are_found_by_their_shape():
    rep = bw.read_replay(replay(), KEY)
    dec = st.decode(rep.stream, bw.index(rep.stream), {ME, ALLY, ENEMY})
    assert dec.found["health"] == HEALTH and dec.found["shot"] == SHOT and dec.found["impact"] == IMPACT
    assert dec.found["tracer"][0] == {"method": TRACER, "shot": 4, "start": 16, "shooter": 0}
    assert dec.found["hit"]["method"] == HITS and dec.found["gunAngles"] == GUN and dec.found["arena"] == ARENA
    assert dec.found["chat"] == CHAT and dec.found["camera"] == CAMERA and dec.found["client"] == CLIENT


def test_the_arena_says_when_the_battle_began():
    s = read(replay()).summary
    assert s["battleStart"] == pytest.approx(5.0) and s["battleStartFrom"] == "arena"
    assert [p["name"] for p in s["periods"]] == ["waiting", "prebattle", "battle"]


def test_health_changes_are_hurt_and_damage_rows():
    m = read(replay())
    hurt = rows(m, "hurt")
    assert [r["value"] for r in hurt] == [400, 400, 400, 800]
    assert hurt[-1]["health"] == 0 and hurt[-1]["text"] == "fire" and all(r["other"] == "me" for r in hurt)
    damage = rows(m, "damage")
    assert all(r["player"] == "me" and r["other"] == "foe" for r in damage)
    # The death is where the health ran out (13 s), not at the results' whole second.
    (kill,) = m.summary["kills"]
    assert kill["time"] == pytest.approx(13.0) and kill["timeFrom"] == "health"
    foe = [p for p in m.summary["players"] if p["name"] == "foe"][0]
    assert foe["seen"]["damageReceived"] == 2000


#: A struck point as 2.x sends it: four zero bytes, the component (4), a code (1), the entry (middle across, a
#: third up, the front face) and where the path ended (further in, lower), three more bytes, a zero.
POINT = bytes(4) + bytes([4, 1, 128, 85, 255, 128, 60, 200]) + bytes([0x44, 0xB0, 3, 0])


def test_a_struck_point_is_where_it_went_in_and_ended():
    p = st.hit_point(POINT)
    assert (p["component"], p["code"]) == (4, 1)
    assert p["entry"] == pytest.approx((128 / 255, 85 / 255, 1.0)) and p["exit"] == pytest.approx((128 / 255, 60 / 255, 200 / 255))
    assert st.hit_point(POINT[4:12])["entry"] == p["entry"]  # 1.x: the 8 bytes alone
    struck = [r for r in rows(read(replay()), "struck") if r["value"]]
    assert struck[0]["hitComponent"] == 4 and struck[0]["hitW"] == pytest.approx(1.0)
    # The shells come from "me", west of the enemy: the shot travels east, the enemy facing north - to its right.
    d = (struck[0]["hitDirX"], struck[0]["hitDirY"], struck[0]["hitDirZ"])
    assert math.hypot(*d) == pytest.approx(1.0) and d[2] > 0.5


def test_shots_tracers_impacts_and_strikes():
    m = read(replay())
    shots = rows(m, "shot")
    assert len(shots) == 4 and all(r["player"] == "me" for r in shots)
    assert len(rows(m, "tracer")) == 4 and all(r["player"] == "me" for r in rows(m, "impact"))
    struck = rows(m, "struck")
    assert [r["value"] for r in struck] == [400, 400, 400, 0]
    assert m.summary["players"][[p["name"] for p in m.summary["players"]].index("me")]["seen"]["shots"] == 4


def test_the_turret_yaw_is_relative_to_the_hull():
    m = read(replay())
    pos = [r for r in rows(m, "position") if r["player"] == "me" and r["time"] >= 1.0]
    assert pos[0]["turretYaw"] == pytest.approx(math.pi / 2, abs=0.01) and pos[0]["gunStep"] == 9
    foe = [r for r in rows(m, "position") if r["player"] == "foe" and r["time"] >= 1.0]
    assert foe[0]["turretYaw"] == pytest.approx(0.0, abs=0.01)


def test_chat_commands_and_camera():
    m = read(replay())
    (chat,) = rows(m, "chat")
    assert chat["player"] == "friend" and chat["text"] == "go left"
    (cmd,) = rows(m, "command")
    assert cmd["player"] == "friend" and (cmd["x"], cmd["z"]) == (20.0, 30.0) and cmd["value"] == 28
    assert [r["text"] for r in rows(m, "camera")] == ["sniper"]
    assert [r["value"] for r in rows(m, "zoom")] == [4.0]
    assert m.summary["chat"][0]["text"] == "go left"


def test_unpickling_runs_nothing():
    # A pickle naming a function to call: the reader keeps the name, calls nothing.
    evil = b"cos\nsystem\n(S'echo pwned'\ntR."
    value = bw.unpickle(evil)
    assert isinstance(value, bw.Global) and type(value).__name__ == "system"
    assert bw.plain(value) == {"class": "system", "args": ["echo pwned"]}
