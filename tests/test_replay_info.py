"""The header-only reader on a replay built here: made-up battle, no real game data."""

from __future__ import annotations

import pytest

from heat3d_ext_wot import bigworld as bw
from heat3d_ext_wot.replay import KEY
from heat3d_ext_wot.replay_info import info

HEADER = {
    "mapName": "99_testmap",
    "mapDisplayName": "Test Map",
    "clientVersionFromExe": "2, 4, 1, 0",
    "playerName": "alpha",
    "playerVehicle": "ussr-R1_Test",
    "dateTime": "07.11.2026 12:00:00",
    "battleType": 1,
    "gameplayID": "ctf",
    "vehicles": {
        "11": {"name": "alpha", "team": 1, "vehicleType": "ussr:R1_Test", "clanAbbrev": "TST"},
        "12": {"name": "bravo", "team": 1, "vehicleType": "germany:G1_Test", "clanAbbrev": ""},
        "13": {"name": "charlie", "team": 2, "vehicleType": "usa:A1_Test"},
    },
}

RESULTS = [
    {
        "arenaUniqueID": 123456789,
        "common": {"duration": 321, "winnerTeam": 1, "arenaCreateTime": 1794052800},
        "vehicles": {
            "11": [{"deathReason": -1, "kills": 1, "damageDealt": 900}],
            "13": [{"deathReason": 0, "kills": 0, "damageDealt": 0}],
        },
    },
    {},
    {},
]


def write(tmp_path, blocks):
    p = tmp_path / "test.wotreplay"
    p.write_bytes(bw.encipher(blocks, bw.packet(1, 0.0, b"x"), KEY))
    return p


def test_a_whole_battle(tmp_path):
    i = info(write(tmp_path, [HEADER, RESULTS]))
    assert i["map"] == "99_testmap"
    assert i["map_title"] == "Test Map"
    assert i["mode"] == "ctf"
    assert i["date"] == "2026-11-07T12:00:00+00:00"
    assert i["duration_s"] == 321.0
    assert i["game_version"] == "2.4.1.0"
    assert i["match"] == "123456789"
    assert i["teams"] == [{"id": 1}, {"id": 2}]
    assert i["outcome"] == {"winner": 1, "result": "win"}
    by_name = {p["name"]: p for p in i["players"]}
    assert set(by_name) == {"alpha", "bravo", "charlie"}
    assert by_name["alpha"] == {"name": "alpha", "team": 1, "vehicle": "ussr:R1_Test", "clan": "TST", "own": True,
                                "kills": 1, "damage": 900, "survived": True}
    assert by_name["bravo"]["clan"] is None and by_name["bravo"]["survived"] is None
    assert by_name["charlie"]["team"] == 2 and by_name["charlie"]["survived"] is False


def test_a_recording_cut_off_before_the_results(tmp_path):
    i = info(write(tmp_path, [HEADER]))
    assert i["date"] == "2026-11-07T12:00:00"  # the recording's local clock: no zone
    assert i["duration_s"] is None and i["outcome"] is None and i["match"] is None
    assert len(i["players"]) == 3


def test_a_draw(tmp_path):
    results = [{**RESULTS[0], "common": {"duration": 900, "winnerTeam": 0}}, {}, {}]
    assert info(write(tmp_path, [HEADER, results]))["outcome"] == {"winner": None, "result": "draw"}


def test_garbage_is_not_a_replay(tmp_path):
    p = tmp_path / "junk.wotreplay"
    p.write_bytes(b"this is not a replay at all, just some text" * 10)
    with pytest.raises(ValueError, match="not a World of Tanks replay"):
        info(p)
    p.write_bytes(b"")
    with pytest.raises(ValueError):
        info(p)


def test_a_warships_replay_is_refused(tmp_path):
    ships = {"mapName": "spaces/00_test", "vehicles": [{"name": "delta", "shipId": 1}]}
    with pytest.raises(ValueError, match="World of Warships"):
        info(write(tmp_path, [ships]))
