"""
The standalone app's description of this tool (app/spec.py): the World of
Tanks install (Steam on any system, the launcher's Games folders, or the folder
you choose), its `replays` folder, and their conversion as a task. A replay
reader has no maps. `python -m heat3d_ext_wot.standalone_spec` runs the app
from a checkout; the release executables run the same.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import GameSpec, Input, Spec, Task, game_folders

FOLDER_NAMES = ("World_of_Tanks", "World of Tanks", "World_of_Tanks_EU", "World_of_Tanks_NA", "World_of_Tanks_ASIA",
                "World_of_Tanks_CT")


def _is_install(p: Path) -> bool:
    return p.is_dir() and ((p / "version.xml").is_file() or (p / "WorldOfTanks.exe").is_file() or (p / "res").is_dir())


def _candidates() -> list[Path]:
    """Every Steam library (Windows, Linux incl. flatpak and Steam Deck, macOS), the launcher's `<drive>:/Games`
    on Windows, and `~/Games` (also inside Wine/Lutris prefixes) elsewhere."""
    out = [d for name in FOLDER_NAMES for d in paths.steam_game_dirs(name)]
    if sys.platform == "win32":
        out += [Path(f"{drive}:/Games") / name for drive in "CDEFGH" for name in FOLDER_NAMES]
    else:
        games = Path.home() / "Games"
        out += [games / name for name in FOLDER_NAMES]
        try:
            prefixes = [p for p in games.iterdir() if (p / "drive_c").is_dir()] if games.is_dir() else []
        except OSError:
            prefixes = []
        out += [p / "drive_c" / "Games" / name for p in prefixes for name in FOLDER_NAMES]
    return out


def _find(given: str | None) -> Path | None:
    if given:
        return Path(given) if _is_install(Path(given)) else None
    return paths.first(_candidates(), _is_install)


def _build(game: Path) -> str | None:
    try:
        m = re.search(r"<version>\s*([^<]+?)\s*</version>", (game / "version.xml").read_text("utf-8", "replace"))
    except OSError:
        return None
    return m.group(1)[:40] if m else None


def _replays(levels: Path) -> str:
    game = game_folders(SPEC).get("wot")
    return str(game / "replays") if game and (game / "replays").is_dir() else ""


SPEC = Spec(
    id="heat3d-wot",
    name="3DHeat WoT",
    repo="Holdi601/3DHeat-Ext-WoT",
    version=__version__,
    tools={"heat3d-wot-replay": "heat3d_ext_wot.cli:main"},
    default_tool="heat3d-wot-replay",
    description="World of Tanks replays into matches for the 3DHeat viewer",
    module="heat3d_ext_wot.standalone_spec",
    games=[GameSpec(key="wot", label="World of Tanks", find=_find, subdir="wot", build=_build,
                    platforms=("windows-x64", "linux-x64", "macos-arm64"))],
    tasks=[Task(
        "replays", "Convert replays",
        [Input("src", "Folder with .wotreplay replays", "folder", default=_replays),
         Input("out", "Where the matches go", "folder", default=lambda levels: str(paths.data_dir() / "matches" / "wot"))],
        lambda v, levels: ["heat3d-wot-replay", v["src"], "-o", v["out"]],
        help="each battle becomes a table and match document the viewer opens",
    )],
    min_free_gb=1.0,
    notice="Not affiliated with or endorsed by Wargaming.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))
