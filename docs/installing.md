---
title: Installing
nav_order: 2
---

# Installing

Needs Python 3.10 or later; numpy and pyarrow are installed with it.

## Step by step

1. Get the code: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git` (or download a release zip from
   [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases) and unpack it).
2. Install it into your Python: in that folder, `pip install -e .`. This
   puts the `heat3d-wot-replay` command on your path.
3. Check it: `heat3d-wot-replay --version` prints the version (the `VERSION` file), and
   `heat3d-wot-replay --help` the options:

![heat3d-wot-replay --help](assets/img/help.svg)

Without installing, `python -m heat3d_ext_wot ...` in the repository folder does the
same.

The 3DHeat Watcher runs this command on new replays when it is installed, and
works without it.

## Updates

Every start first checks the project's GitHub releases (one request at most
every few hours, cached; it never stops a conversion, offline or not). When a
newer release is out, the command asks before installing it: a `git clone` is
updated with `git pull --ff-only` (refused while you have local changes), a
downloaded copy from the release's source archive. `HEAT3D_NO_UPDATE=1`
switches the check and the update off. Code: `heat3d_update`
(`startup("heat3d_ext_wot")`).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
