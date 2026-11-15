---
title: Converting replays
nav_order: 4
---

# Converting replays

## Step by step

1. **Switch recording on** in the game: Settings > General > Record battles.
   From then on the game saves each battle in the `replays` folder of your
   World of Tanks install, for example
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Open a terminal** in a folder where the results may go
   ([Before you start](before-you-start.md)).
3. **Run the converter** on replay files, or on folders that hold them:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out` is made in the folder your terminal is in.
4. **Read what it says.** You should see one line per replay, ending in the
   table it wrote.
5. **Open the result** in the 3DHeat viewer: `out/<map>/<match>.parquet`
   in the Heatmap tab, `<match>.match.json` in the Match tab. Or read them
   with any Parquet or JSON reader.

![A run on a synthetic replay: converting, running again, a broken file, an empty folder](assets/img/convert.svg)

The picture is a run on a replay the tests build in code (no real replay):

- a replay converted: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- run again, the match already written is skipped: `<file>: already written, <table>`;
- a file that is not a replay: `<file>: not converted: <why>` (on the error
  output; exit status 1, the other replays are still converted);
- no replay found: `no .wotreplay files in <folders>` (exit status 2).

## Options

| Option | Default | Does |
|---|---|---|
| `replays` (one or more) | - | `.wotreplay` files, or folders searched for them (subfolders too) |
| `-o`, `--out` | required | the folder to write into: a folder per map inside |
| `--force` | off | convert again what is already written |
| `--version` | - | print `heat3d-wot-replay <version>` and stop |
| `-h`, `--help` | - | print the options and stop |

The options as the program prints them: [Command reference](cli-reference.md).

## What is written

Loose files only: this converter writes no `.3dheat` file (the viewer can
pack them into one: [One file a match](https://holdi601.github.io/3DHeat/container.html)).
Per replay, into `out/<map>/`:

| File | What |
|---|---|
| `<match>.parquet` | the table: every tank's position over time and every event where it happened ([The table](table.md)) |
| `<match>.match.json` | the match document: map, client version, players, kills, results and everything else ([The match document](match-document.md)) |
| `<match>.messages.parquet` | the sidecar: every item of the replay the two files above do not hold whole ([Completeness](completeness.md)) |

`<match>` is the battle's own id, or the file's name when the recording
stopped before the results.

## Exit status

`0` when every replay was converted or skipped, `1` when any failed (the
rest are still converted), `2` when no replay file was found.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
