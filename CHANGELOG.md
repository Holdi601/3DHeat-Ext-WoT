# Changelog

## Unreleased

- `--version` prints the command's name with the version
  (`heat3d-wot-replay 0.1.0`), as the other 3DHeat converters do.
- Documentation: a page for beginners, a key table for the match document,
  generated reference pages, no real map names or replay figures.

## 0.1.0

- Every vehicle's position, heading, pitch, roll and turret over time; every
  death and kill where it happened.
- Health changes, hits with where the shell struck, shots, tracers,
  explosions, chat, battle chat commands, camera, the results screen.
- Nothing lost: the sidecar keeps every item not read whole, and the
  self-check counts each kind.

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
| Wargaming's terms, licence | [Terms and licence](docs/terms.md) |
| releasing | [Maintaining](docs/maintaining.md) |
