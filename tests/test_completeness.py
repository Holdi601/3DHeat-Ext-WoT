"""
The rule every 3DHeat converter follows (docs/converters.md of 3DHeat): all
the replay holds is decoded, or kept whole in the sidecar
`<match>.messages.parquet`, and the match document counts what became of
each kind of item - nothing lost. On replays built here.
"""

from __future__ import annotations

import json
import math
import struct

import pyarrow.parquet as pq

from heat3d_ext_wot import bigworld as bw
from heat3d_ext_wot.cli import main
from heat3d_ext_wot.replay import KEY, read
from test_stream import GUN, HEALTH, call
from test_stream import stream as full_stream
from test_wot import ALLY, AVATAR, ENEMY, HEADER, ME, results

UNKNOWN_PACKET, UNKNOWN_METHOD, AIM = 77, 61, 38
VEHICLE, AVATAR_TYPE = 6, 2


def stream() -> bytes:
    """The stream of test_stream, with the entities created, the version, and things nobody reads yet."""
    out = bytearray()
    out += bw.packet(0, 0.0, struct.pack("<IH", AVATAR, AVATAR_TYPE) + b"\x00properties")
    for e in (ME, ALLY, ENEMY):
        out += bw.packet(5, 0.0, struct.pack("<IH", e, VEHICLE) + b"\x00" * 20)
    out += bw.packet(24, 0.0, struct.pack("<I", 7) + b"2.4.1.0")
    # The recording player aiming east: a rotation of 90 degrees about +y turns +z (north) to +x.
    for i in range(30):
        out += bw.packet(AIM, i / 10, struct.pack("<4f", 0.0, math.sqrt(0.5), 0.0, math.sqrt(0.5)) + bytes(24))
    out += full_stream()
    out += bw.packet(UNKNOWN_PACKET, 19.0, b"\x01\x02\x03 whatever this is")
    out += call(8, 19.0, ENEMY, UNKNOWN_METHOD, b"\xaa\xbb")
    # A pitched and rolled vehicle, and the enemy leaving the client's view after its last position.
    out += bw.packet(10, 20.05, bw.POSITION.pack(ALLY, 0, -50.0, 1.0, 76.0, 0, 0, 0, 0.0, -0.1, 0.05, 1))
    out += bw.packet(4, 20.1, struct.pack("<I", ENEMY))
    return bytes(out)


def replay() -> bytes:
    return bw.encipher([HEADER, results(enemy_life=8)], stream(), KEY)


def completeness(m):
    return m.summary["selfCheck"]["completeness"]


def test_nothing_is_lost():
    m = read(replay())
    c = completeness(m)
    assert c["lost"] == 0 and all(t["lost"] == 0 for t in c["types"].values())
    assert c["rule"] == "https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md"
    assert c["sidecars"] == ["123456789.messages.parquet"]
    # Seen: every packet of the stream, the two blocks, and the container's own bytes.
    rep = bw.read_replay(replay(), KEY)
    packets = len(bw.index(rep.stream))
    assert c["seen"] == packets + 2 + sum(1 for b in (rep.sizes, rep.leftover, rep.unused) if b)
    assert c["seen"] == c["decoded"] + c["partial"] + c["raw"]
    # Every item not decoded whole is a row of the sidecar.
    assert m.messages.num_rows == c["seen"] - c["decoded"]
    assert m.messages.column_names[:7] == ["time", "type", "name", "entity", "decoded", "payload", "text"]


def test_what_nobody_reads_yet_is_kept_whole():
    m = read(replay())
    rows = m.messages.to_pylist()
    (unknown,) = [r for r in rows if r["type"] == f"packet {UNKNOWN_PACKET}"]
    assert unknown["payload"] == b"\x01\x02\x03 whatever this is" and unknown["time"] == 19.0
    (method,) = [r for r in rows if r["type"] == f"method {VEHICLE}.{UNKNOWN_METHOD}"]
    assert method["entity"] == ENEMY and method["entityType"] == VEHICLE
    assert method["payload"] == struct.pack("<III", ENEMY, UNKNOWN_METHOD, 2) + b"\xaa\xbb"
    assert completeness(m)["types"][f"method {VEHICLE}.{UNKNOWN_METHOD}"]["raw"] == 1
    # The blocks whole, as text.
    (header,) = [r for r in rows if r["type"] == "block 0"]
    assert json.loads(header["text"]) == HEADER


def test_what_is_read_in_part_carries_what_was_read():
    m = read(replay())
    rows = m.messages.to_pylist()
    health = [r for r in rows if r["type"] == f"method {VEHICLE}.{HEALTH}"]
    assert health and all(r["name"] == "health" for r in health)
    first = json.loads(health[0]["decoded"])
    assert (first["new"], first["old"], first["attacker"]) == (1600, 2000, ME)
    gun = [json.loads(r["decoded"]) for r in rows if r["type"] == f"property {VEHICLE}.{GUN}" and r["entity"] == ME]
    assert gun[0] == {"code": (768 << 6) | 9, "yawStep": 768, "gunStep": 9}
    types = completeness(m)["types"]
    assert types[f"method {VEHICLE}.{HEALTH}"]["partial"] == len(health)
    assert types["packet 10"]["name"] == "position" and types["packet 10"]["partial"] > 0


def test_the_aim_is_read_in_part():
    m = read(replay())
    aims = [r for r in m.messages.to_pylist() if r["type"] == f"packet {AIM}"]
    assert len(aims) == 30 and all(r["name"] == "aim" for r in aims)
    fwd = json.loads(aims[0]["decoded"])["forward"]
    assert fwd == [1.0, 0.0, 0.0] and len(aims[0]["payload"]) == 40


def test_entities_come_and_go():
    m = read(replay())
    ents = {e["entity"]: e for e in m.summary["entities"]}
    assert ents[AVATAR]["role"] == "avatar" and ents[ENEMY]["role"] == "vehicle"
    assert ents[ENEMY]["left"] == [20.100000381469727] and ents[ME]["left"] == []
    check = m.summary["selfCheck"]["entities"]
    assert check["positionsWhileGone"] == 0 and check["roles"] == {"2": "avatar", "6": "vehicle"}
    assert completeness(m)["types"]["packet 4"]["decoded"] == 1  # the id alone: read whole


def test_the_version_in_the_stream():
    m = read(replay())
    assert m.summary["streamVersion"] == "2.4.1.0" and m.summary["selfCheck"]["streamVersionAgrees"] is True
    assert completeness(m)["types"]["packet 24"] == {"seen": 1, "decoded": 1, "partial": 0, "raw": 0, "lost": 0,
                                                     "name": "version"}


def test_pitch_and_roll_are_in_the_table():
    m = read(replay())
    i = max(k for k, (e, p) in enumerate(zip(m.rows["event"], m.rows["player"])) if e == "position" and p == "friend")
    assert math.isclose(m.rows["pitch"][i], -0.1, rel_tol=1e-6) and math.isclose(m.rows["roll"][i], 0.05, rel_tol=1e-6)


def test_the_command_writes_the_sidecar(tmp_path):
    (tmp_path / "a.wotreplay").write_bytes(replay())
    out = tmp_path / "out"
    assert main([str(tmp_path), "-o", str(out)]) == 0
    side = pq.read_table(out / "99_testmap" / "123456789.messages.parquet")
    doc = json.loads((out / "99_testmap" / "123456789.match.json").read_text(encoding="utf-8"))
    c = doc["selfCheck"]["completeness"]
    assert c["lost"] == 0 and side.num_rows == c["seen"] - c["decoded"]
    assert "pitch" in pq.read_table(out / "99_testmap" / "123456789.parquet").column_names
