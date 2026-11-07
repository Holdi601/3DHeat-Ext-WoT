# World of Tanks replays

World of Tanks replays (`.wotreplay`) into heatmap tables and match
summaries for the 3DHeat viewer - or anything that reads Parquet and JSON.
Every vehicle's position over time, and every kill where it happened.

This converter is kept outside the 3DHeat Watcher on purpose: the replays are
enciphered, and Wargaming's terms (below) are broad. If the converter ever has
to go, nothing else goes with it. The Watcher runs it as a command when it is
installed, and works without it.

```bash
pip install -e .                                  # installs the heat3d-wot-replay command
heat3d-wot-replay <replays or folders> -o out     # or: python -m heat3d_ext_wot ...
```

Per replay, into a folder per map (`out/01_karelia/...`):

- `<match>.parquet` - every vehicle's position about ten times a second, and
  each death twice: where the victim fell, and where the killer stood.
- `<match>.match.json` - the map, the client version, who recorded it, the
  result, and every player's line: team, vehicle, kills, damage, survival.

`<match>` is the battle's own id (`arenaUniqueID`), or the file's name when the
recording stopped before the results came. A match already written is skipped
unless `--force`. Exit status 0 when every replay was converted, 1 when any
failed (the rest are still converted), 2 when none was found.

Replays are where the game saves them when battle recording is on
(Settings > General > Record battles): `<World of Tanks>/replays/`.

## The table

| Column | What |
|---|---|
| `match`, `map` | the battle's id; the map's id (`01_karelia`) |
| `time` | seconds since the recording began (the countdown is in it) |
| `battleTime` | seconds since the battle began; negative during the countdown |
| `event` | `position`, `death` (where the victim was), `kill` (where the killer was) |
| `player`, `team`, `own` | the player's name; team `1` or `2`; `1` on the recording player's rows |
| `vehicle`, `type` | the tank as the game names it (`ussr:R144_K_91`); `tank` for every vehicle |
| `x`, `y`, `z` | metres: x east, y up, z north (the game's own world, left-handed) |
| `dirX`, `dirY`, `dirZ` | where the hull points, a unit vector in the same frame (`dirY` 0: heading only) |
| `other`, `reason` | for a death the killer, for a kill the victim; the game's death reason number |
| `entity` | the vehicle's id in the replay |

The Parquet footer carries the `heat3d` hints: Y up, Z flipped (so the map is
not mirrored), unit scale 1, a vehicle seven metres across, `player` as the
person, `team` as the group, `match` as the session.

## What it reads, and how

A replay is a header of JSON blocks and the game's packet stream (format notes
in [`heat3d_ext_wot/bigworld.py`](heat3d_ext_wot/bigworld.py)):

- The first block, in the clear: the map, the client version, the recording
  player and the roster (`vehicles`: name, team, tank, keyed by the vehicle's
  id).
- The second, when the recording lasted to the end: the results - each
  vehicle's `lifeTime`, killer and death reason, kills and damage; the match's
  duration and winner; and in some modes the only full roster (the header of
  those lists just the own team).
- The packet stream, zlib-compressed and Blowfish-enciphered with a key the
  game carries, which the community tools that read these files have published
  since 2013. Deciphered, it holds the engine's position updates: a vehicle's
  id, its position and its heading. They are found by their shape rather than
  their packet number, so a patch that renumbers them does not empty the table.

**Positions** are what the recording client was told: its own team throughout,
an enemy only while spotted (or while in the client's range). A vehicle never
spotted has no rows. Rows of a vehicle stop at its death.

**Deaths** are from the results, not the stream: the death's time is the
battle's start on the replay's clock plus the victim's `lifeTime` (whole
seconds), so it is good to about a second. The battle's start is the first
moment any vehicle moves - nothing moves in the countdown. On the replays
checked, a victim's last movement fell a median of -0.1 to 0.3 s from the
start plus its `lifeTime` (single deaths scatter more: a tank often stops
before it is killed). The place is where the
victim was last seen, when that was within five seconds of its death; else, on
2.x clients, the place the results give (x and z, no height), in the summary
only. A recording that stopped before the end has positions and no deaths.

**Not read:** shots, hits and damage events, spotting, turret direction,
health, camera, chat. They are in the stream as method calls whose numbering
changes with every patch, and reading them reliably needs the game's own
definition files.

## Verified

On public replays, at 2026-11-07:

| Client | Map | Vehicles | Positions | Rate | Deaths (placed) |
|---|---|---|---|---|---|
| 1.12.0 (April 2021) | Karelia | 30 of 30 seen | 47,675 | 10 Hz | 22 (22) |
| 2.4.1 (November 2026) | Westfeld | 28 of 30 seen | 45,539 | 10 Hz | 23 (20 with height, 3 from the results) |
| 2.4.1 | Great Wall | 29 of 30 seen | 50,889 | 10 Hz | 25 (21; 4 never seen near their death) |
| 2.4.1, battle type 20 | Pilsen | 14 of 14 | 15,768 | 10 Hz | 10 (all) |

Checks on them: the coordinates span about 1 km (the maps are 1 km across);
speeds have a median of 22 km/h and a 99th percentile of 66 km/h; the heading
agrees with the direction of travel to 0.02 rad; where the 2.4.1 results give
a death's place (9 deaths on Great Wall), the place read here is a median of
1.1 m from it, at most 4.5 m. The tests build
replays to the same layout, so no real replay is kept in this repository.

**Not checked:** clients before 1.12, console and Blitz replays (different
games), Lesta's Mir Tankov (`.mtreplay`), and modes other than random battles
and battle type 20.

## Wargaming's terms

Read on 2026-11-07, Wargaming EULA version 14 (effective 10 April 2024, listed
as current):

- 5.3 (b): unless authorised in writing, you must not "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): prohibited is "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

World of Tanks' list of prohibited mods is about the battle itself: mods that
"reveal the position of enemies in a way not included in the client", aim
bots, reload timers and the like. Neither the EULA nor that list mentions
replays.

What this converter does: it reads a file the game wrote, after the battle,
outside the game. It changes nothing in the game, talks to no server, and
shows nothing during a battle. It does decipher the stream with the game's
key, which 5.3 (b) and 12.1 (p) can be read to cover. Using it is the user's
decision; that is why it is a separate package.

## Licence and sources

MIT ([`LICENSE`](LICENSE)). Needs numpy (BSD-3-Clause) and pyarrow
(Apache-2.0). Written for this project: the Blowfish cipher here is its own,
with its tables computed from the digits of pi as the cipher defines them.
Facts about the format (the container, the cipher, the position packet) are
common knowledge among replay tools - evido/wotreplay-parser (BSD-3-Clause)
documents them; no code was taken from it or from any other project.

`bigworld.py` and `table.py` are the same files as in the World of Warships
converter (`../wows-replay`); change both together.
