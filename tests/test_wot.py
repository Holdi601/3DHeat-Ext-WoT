"""
The World of Tanks reader on replays built here, to the layout real ones have:
no real replay is kept in the repository.
"""

from __future__ import annotations

import json
import math
import struct

import pyarrow.parquet as pq
import pytest

from heat3d_ext_wot import bigworld as bw
from heat3d_ext_wot.cli import main
from heat3d_ext_wot.replay import KEY, read

ME, ALLY, ENEMY, AVATAR = 1001, 1002, 1003, 999

HEADER = {
    "mapName": "99_testmap",
    "mapDisplayName": "Test Map",
    "clientVersionFromExe": "2.4.1.0",
    "playerName": "me",
    "playerVehicle": "ussr-R1_Test",
    "dateTime": "07.11.2026 12:00:00",
    "vehicles": {
        str(ME): {"name": "me", "team": 1, "vehicleType": "ussr:R1_Test"},
        str(ALLY): {"name": "friend", "team": 1, "vehicleType": "germany:G1_Test"},
        str(ENEMY): {"name": "foe", "team": 2, "vehicleType": "usa:A1_Test"},
    },
}

#: The countdown: nothing moves for the first five seconds.
START = 5.0


def results(enemy_life: int = 8) -> list:
    return [
        {
            "arenaUniqueID": 123456789,
            "common": {"duration": 20, "winnerTeam": 1},
            "vehicles": {
                str(ME): [{"lifeTime": 15, "deathReason": -1, "killerID": 0, "kills": 1, "damageDealt": 900}],
                str(ALLY): [{"lifeTime": 15, "deathReason": -1, "killerID": 0, "kills": 0}],
                str(ENEMY): [{"lifeTime": enemy_life, "deathReason": 0, "killerID": ME, "kills": 0}],
            },
        },
        {},
        {},
    ]


def position(entity: int, x: float, y: float, z: float, yaw: float) -> bytes:
    return bw.POSITION.pack(entity, 1, x, y, z, 0, 0, 0, yaw, 0, 0, 0)


def stream(position_type: int = 10) -> bytes:
    out = bytearray()
    out += bw.packet(0x16, 0.0, b"version")  # something that is not a position
    for i in range(201):
        t = i / 10
        moving = max(0.0, t - START)
        out += bw.packet(position_type, t, position(ME, 10.0 * moving, 1.0, 0.0, math.pi / 2))  # east
        out += bw.packet(position_type, t, position(ALLY, -50.0, 1.0, 5.0 * moving, 0.0))  # north
        out += bw.packet(position_type, t, position(ENEMY, 100.0, 2.0, -100.0 + moving, 0.0))
        out += bw.packet(position_type, t, position(AVATAR, 0.0, 0.0, 0.0, 0.0))  # the avatar, never placed
        out += bw.packet(7, t, struct.pack("<III", ME, 3, 2) + b"\x01\x02")
    return bytes(out)


def replay(**kw) -> bytes:
    return bw.encipher([HEADER, results(**kw)], stream(), KEY)


# -------------------------------------------------------------------- cipher


def test_blowfish_matches_the_published_test_vectors():
    for key, plain, cipher in [
        (bytes(8), bytes(8), "4ef997456198dd78"),
        (b"\xff" * 8, b"\xff" * 8, "51866fd5b85ecb8a"),
        (bytes.fromhex("3000000000000000"), bytes.fromhex("1000000000000001"), "7d856f9a613063f2"),
    ]:
        bf = bw.Blowfish(key)
        assert bf.encrypt_block(plain).hex() == cipher
        assert bf.decrypt(bytes.fromhex(cipher)).tobytes() == plain


def test_pi_is_where_blowfish_starts():
    words = bw._pi_words()
    assert words[0] == 0x243F6A88 and words[1] == 0x85A308D3 and words[18] == 0xD1310BA6


def test_a_replay_round_trips():
    data = stream()
    rep = bw.read_replay(bw.encipher([HEADER], data, KEY), KEY)
    assert rep.header["mapName"] == "99_testmap"
    assert rep.stream == data and not rep.truncated


def test_not_a_replay_is_refused():
    with pytest.raises(ValueError):
        read(b"\x00" * 64)


def test_the_wrong_key_is_refused():
    with pytest.raises(ValueError):
        bw.read_replay(bw.encipher([HEADER], stream(), bytes(16)), KEY)


# --------------------------------------------------------------------- match


def test_every_vehicle_is_tracked_at_ten_hz():
    m = read(replay())
    s = m.summary
    assert s["map"] == "99_testmap" and s["mapName"] == "Test Map" and s["clientVersion"] == "2.4.1.0"
    assert s["match"] == "123456789" and s["winnerTeam"] == 1 and s["complete"]
    assert s["hz"] == pytest.approx(10.0)
    assert {p["name"] for p in s["players"]} == {"me", "friend", "foe"}
    # The avatar, never placed, is not a vehicle.
    assert set(m.rows["entity"]) == {ME, ALLY, ENEMY}
    rows = [i for i, p in enumerate(m.rows["player"]) if p == "me" and m.rows["event"][i] == "position"]
    assert len(rows) == 201
    assert all(m.rows["own"][i] == 1 for i in rows)
    assert m.rows["vehicle"][rows[0]] == "ussr:R1_Test" and m.rows["team"][rows[0]] == "1"


def test_battle_start_is_the_first_movement():
    s = read(replay()).summary
    assert s["battleStart"] == pytest.approx(START + 0.1, abs=0.15)


def test_heading_becomes_a_direction():
    m = read(replay())
    i = m.rows["player"].index("me")
    assert m.rows["dirX"][i] == pytest.approx(1.0) and m.rows["dirZ"][i] == pytest.approx(0.0, abs=1e-6)


def test_a_death_is_placed_where_the_victim_was_and_the_kill_where_the_killer_was():
    m = read(replay(enemy_life=8))
    s = m.summary
    (kill,) = s["kills"]
    assert kill["victim"] == "foe" and kill["killer"] == "me"
    death_time = s["battleStart"] + 8 + 0.5
    assert kill["time"] == pytest.approx(death_time, abs=0.01)
    assert kill["z"] == pytest.approx(-100.0 + (death_time + 0.5 - START), abs=0.2)
    d = m.rows["event"].index("death")
    k = m.rows["event"].index("kill")
    assert m.rows["player"][d] == "foe" and m.rows["other"][d] == "me"
    assert m.rows["player"][k] == "me" and m.rows["other"][k] == "foe"
    assert m.rows["x"][k] == pytest.approx(10.0 * (death_time + 0.5 - START), abs=1.5)
    # No positions of a wreck after its death.
    foe_times = [t for t, p, e in zip(m.rows["time"], m.rows["player"], m.rows["event"]) if p == "foe" and e == "position"]
    assert max(foe_times) <= death_time
    assert [p for p in s["players"] if p["name"] == "foe"][0]["survived"] is False


def test_a_replay_without_results_has_positions_and_no_deaths():
    m = read(bw.encipher([HEADER], stream(), KEY), name="unfinished")
    assert m.summary["match"] == "unfinished" and not m.summary["complete"]
    assert m.summary["kills"] == [] and m.summary["positions"] == 3 * 201


def test_a_renumbered_position_packet_is_still_found():
    m = read(bw.encipher([HEADER, results()], stream(position_type=0x31), KEY))
    assert m.summary["positionPacket"] == 0x31 and m.summary["positions"] > 400


# ----------------------------------------------------------------------- CLI


def test_the_command_writes_the_table_and_summary(tmp_path):
    src = tmp_path / "in"
    src.mkdir()
    (src / "battle.wotreplay").write_bytes(replay())
    out = tmp_path / "out"
    assert main([str(src), "-o", str(out)]) == 0
    table = out / "99_testmap" / "123456789.parquet"
    t = pq.read_table(table)
    hints = json.loads(t.schema.metadata[b"heat3d"])
    assert hints["axes"]["flipZ"] is True and hints["columns"]["personId"] == "player"
    assert {"vehicle", "team", "event", "x", "y", "z", "dirX"} <= set(t.column_names)
    doc = json.loads((out / "99_testmap" / "123456789.match.json").read_text(encoding="utf-8"))
    assert doc["format"] == "heat3d-wot-match" and len(doc["kills"]) == 1
    # Already written: skipped, still a success.
    assert main([str(src), "-o", str(out)]) == 0


def test_the_command_says_when_there_is_nothing(tmp_path):
    assert main([str(tmp_path), "-o", str(tmp_path / "out")]) == 2


def test_a_bad_file_fails_without_stopping_the_rest(tmp_path):
    (tmp_path / "a.wotreplay").write_bytes(b"not a replay")
    (tmp_path / "b.wotreplay").write_bytes(replay())
    assert main([str(tmp_path), "-o", str(tmp_path / "out")]) == 1
    assert (tmp_path / "out" / "99_testmap" / "123456789.parquet").exists()


def test_a_vehicle_only_the_results_name_is_still_named():
    # Some modes' headers list only the recording player's team; the results' roster has everyone.
    head = {**HEADER, "vehicles": {k: v for k, v in HEADER["vehicles"].items() if v["team"] == 1}}
    res = results()
    res[1] = {str(ENEMY): {"name": "foe", "team": 2, "vehicleType": "usa:A1_Test"}}
    m = read(bw.encipher([head, res], stream(), KEY))
    assert {p["name"] for p in m.summary["players"]} == {"me", "friend", "foe"}
    assert m.summary["kills"][0]["victim"] == "foe" and "foe" in m.rows["player"]
