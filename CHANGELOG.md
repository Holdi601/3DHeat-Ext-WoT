# Changelog

## 0.3.0

- Its own icon: the 3DHeat cube with a text badge for its game (letters in 3DHeat's colours), as the
  program, window, taskbar and docs icon.
- A new window: the 3DHeat look in dark and light (follows the system, switchable), the logo and
  icon, sharp at any display scaling. Four steps: find the game (each requirement with its fix),
  choose (maps ticked when there is something to do, filters, search; jobs with their fields
  inline), work (progress, time left, cancel), done (open in 3DHeat, open the output folder, and
  for a failure what went wrong and what to do, copy details, report a problem).
- No console window on Windows: the program is a window program. From a terminal it still prints
  as before; `heat3d-wot-cli.cmd` beside it waits for it in a terminal and passes its exit code.
- The update offer in the same look: Update now / Later / Skip this version, and "Update
  automatically" from the dialog.
- CI draws every page and dialog of the window (on Linux under a virtual display) and checks the
  Windows build is a window program.
- `heat3d-wot convert <replay>... -o <out> [--progress-json]` and `heat3d-wot info <replay> --json` (what the
  replay says about its match, read from its header without converting it), the same verbs in every
  3DHeat replay reader; the old command lines work as before.

## 0.2.0

- A standalone program for Windows, Linux (also Steam Deck) and macOS (no Python needed), built by CI with a `SHA256SUMS` file.
  Without arguments it opens a window: what is found and what is missing, and the conversions as buttons.
- `status --json` and `--check --json` for the 3DHeat app's Extractors panel; a replay reader has no maps, so
  `extract` has nothing to do.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).
- The install is found in Steam libraries on Windows, Linux (native, flatpak, Steam Deck) and macOS, in
  the launcher's `Games` folders, and in `~/Games` and Wine/Lutris prefixes on Linux.

## 0.1.0

- `--version` prints the command's name with the version
  (`heat3d-wot-replay 0.1.0`), as the other 3DHeat converters do.
- Documentation: a page for beginners, a key table for the match document,
  generated reference pages, no real map names or replay figures.

- Every vehicle's position, heading, pitch, roll and turret over time; every
  death and kill where it happened.
- Health changes, hits with where the shell struck, shots, tracers,
  explosions, chat, battle chat commands, camera, the results screen.
- Nothing lost: the sidecar keeps every item not read whole, and the
  self-check counts each kind.
- Installs with one pip line from the release zip, no Git needed; a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## Docs

Where each feature is documented:

| Feature | Page |
|---|---|
| installing, updates | [Installing](docs/installing.md), [Before you start](docs/before-you-start.md) |
| converting, options, messages, exit status | [Converting replays](docs/converting.md), [Command reference](docs/cli-reference.md) |
| positions, heading, pitch, roll, turret | [The table](docs/table.md) |
| deaths, kills, health, hits, shots, tracers, explosions | [The table](docs/table.md) (events) |
| chat, commands, camera, periods, base capture, results | [The match document](docs/match-document.md) |
| every column and its type | [Column list](docs/columns.md) |
| the format, and how the reading was checked | [How it reads a replay](docs/how-it-reads.md) |
| sidecar, self-check | [Completeness](docs/completeness.md) |
| what it reads, licence | [Terms and licence](docs/terms.md) |
| releasing | [Maintaining](docs/maintaining.md) |
