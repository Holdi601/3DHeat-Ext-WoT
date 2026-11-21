---
title: Installing
nav_order: 3
---

# Installing

New to the command line? Read [Before you start](before-you-start.md) first.
Needs Python 3.10 or later; numpy and pyarrow are installed with it.

## The standalone program (no Python needed)

Each [release](https://github.com/Holdi601/3DHeat-Ext-WoT/releases/latest) has a ready-to-run program for Windows, Linux (also Steam Deck) and macOS
(`heat3d-wot-<version>-windows-x64.zip`, `...-linux-x64.tar.gz`, `...-macos-arm64.tar.gz`), with a
`SHA256SUMS` file to check the download. Unpack it anywhere and start `heat3d-wot` (on macOS the
first start may need *Open* from the right-click menu, as the program is not notarised).

Started without arguments it opens a window that:

- finds your World of Tanks install (Steam on any system, the launcher's `Games` folders,
  `~/Games` and Wine/Lutris prefixes on Linux), or lets you choose its folder;
- says what is missing (the game, free disk space);
- converts the battles in its `replays` folder, or any folder you pick, into tables and match
  documents (by default into the 3DHeat data folder's `matches/wot`);
- checks for updates and asks before installing one, unless you tick *Update automatically*.

The same program runs every command below: `heat3d-wot heat3d-wot-replay --help`. For scripts:
`heat3d-wot --check --json` says what is found and missing, and `heat3d-wot status --json` what is found
(a replay reader has no maps; `extract` has nothing to do). The 3DHeat app's Extractors panel installs,
updates and starts it for you.

## Step by step

1. Get the code: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   or download a zip from [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   and unpack it.
2. Open a terminal in that folder and type `pip install -e .`. This puts the
   `heat3d-wot-replay` command on your path.
3. Check it: `heat3d-wot-replay --version`. You should see
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` lists the options:

![heat3d-wot-replay --help](assets/img/help.svg)

Without installing, `python -m heat3d_ext_wot ...` in the tool's folder does
the same.

The 3DHeat Watcher runs this command on new replays when it is installed,
and works without it.

## Updates

Every start first checks the project's GitHub releases (at most one request
every few hours; it never stops a conversion, online or not). When a newer
release is out, the command asks before installing it: a `git clone` is
updated with `git pull --ff-only` (refused while you have local changes), a
downloaded copy from the release's archive. `HEAT3D_NO_UPDATE=1` switches the
check and the update off.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
