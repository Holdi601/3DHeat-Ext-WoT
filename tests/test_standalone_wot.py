"""The standalone spec on a synthetic install (tiny fake files, no game data)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from heat3d_ext_wot import standalone_spec
from heat3d_ext_wot.app import entry, paths, update
from heat3d_ext_wot.app import spec as app_spec


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")
    update.AUTO_THIS_RUN = False


def install(root: Path) -> Path:
    game = root / "steamapps" / "common" / "World of Tanks"
    (game / "replays").mkdir(parents=True)
    (game / "version.xml").write_text("<version.xml>\n  <version> v.1.0.0.0 #1 </version>\n</version.xml>\n")
    (game / "replays" / "20260101_0000_country-tank_01_map.wotreplay").write_bytes(b"x")
    return game


def test_find_in_steam_and_given(tmp_path, monkeypatch):
    steam = tmp_path / "Steam"
    game = install(steam)
    monkeypatch.setattr(paths, "steam_roots", lambda: [steam])
    g = standalone_spec.SPEC.games[0]
    assert g.find(None) == game
    assert g.find(str(game)) == game
    assert g.find(str(tmp_path / "nothing")) is None
    assert g.build(game) == "v.1.0.0.0 #1"


def test_task(tmp_path):
    game = install(tmp_path / "elsewhere")
    app_spec.save_settings("heat3d-wot", {"games": {"wot": str(game)}})
    levels = tmp_path / "levels"
    task = standalone_spec.SPEC.tasks[0]
    src, out = task.inputs
    assert src.default(levels) == str(game / "replays")
    assert out.default(levels) == str(paths.data_dir() / "matches" / "wot")
    argv = task.argv({"src": src.default(levels), "out": "o"}, levels)
    assert argv == ["heat3d-wot-replay", str(game / "replays"), "-o", "o"] and argv[0] in standalone_spec.SPEC.tools


def test_no_maps_nothing_to_extract(tmp_path, capsys):
    game = install(tmp_path / "elsewhere")
    app_spec.save_settings("heat3d-wot", {"games": {"wot": str(game)}})
    assert entry.main(standalone_spec.SPEC, ["status", "--json"]) == 0
    g = json.loads(capsys.readouterr().out)["games"][0]
    assert g["found"] and g["maps"] == []
    assert entry.main(standalone_spec.SPEC, ["extract", "--new", "--progress-json"]) == 0
    assert json.loads(capsys.readouterr().out.splitlines()[-1]) == {"event": "done", "ok": 0, "failed": 0}
