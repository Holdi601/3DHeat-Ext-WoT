---
title: Converting replays
nav_order: 3
---

# Converting replays

## Step by step

1. Switch replay recording on in the game (below).
2. Run the converter on replay files, or on folders that hold them:

   ```bash
   heat3d-wot-replay "<World of Tanks>/replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

3. Read what it says: one line per replay, with the positions, vehicles and
   events found and the file written, or why it failed.
4. Open the table and the match document in the 3DHeat viewer (Heatmap tab,
   Match tab), or read them with any Parquet / JSON reader.

![A run on a synthetic replay: converting, running again, an empty folder](assets/img/convert.svg)

The picture is a run on a replay built in code by the tests (no real replay):
the second run skips the match already written; a folder without replays
exits 2.

## Where the game saves replays

Replays are where the game saves them when battle recording is on
(Settings > General > Record battles): `<World of Tanks>/replays/`.

## Options

| Option | Default | Does |
|---|---|---|
| `replays` (one or more) | - | `.wotreplay` files, or folders searched for them |
| `-o`, `--out` | required | the folder to write into: a folder per map inside |
| `--force` | off | convert again what is already written |
| `--version` | - | print the version and exit |
| `-h`, `--help` | - | print the options and exit |

## What is written

Per replay, into a folder per map:

| File | What |
|---|---|
| `<match>.parquet` | the table: every vehicle's position over time and every event where it happened ([The table](table.md)) |
| `<match>.match.json` | the match document: the map, the client version, who recorded it, every player's line and everything else the file holds ([The match document](match-document.md)) |
| `<match>.messages.parquet` | the sidecar: every item of the replay the two files above do not hold whole, kept whole ([Completeness](completeness.md)) |

`<match>` is the battle's own id, or the file's name when none is found.

## Exit status

`0` when every replay was converted, `1` when any failed (the rest are still
converted), `2` when none was found.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
