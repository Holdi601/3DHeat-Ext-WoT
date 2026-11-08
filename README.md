# World of Tanks replays

World of Tanks replays (`.wotreplay`) into heatmap tables and match
summaries for the 3DHeat viewer - or anything that reads Parquet and JSON.
Every vehicle's position and turret over time; every kill, health change,
shot, tracer, explosion and shell strike where it happened; the chat, battle
chat commands, the battle's periods and base capture; the results screen.

This converter is kept outside the 3DHeat Watcher on purpose: the replays are
enciphered, and Wargaming's terms (below) are broad. If the converter ever has
to go, nothing else goes with it. The Watcher runs it as a command when it is
installed, and works without it.

```bash
pip install -e .                                  # installs the heat3d-wot-replay command
heat3d-wot-replay <replays or folders> -o out     # or: python -m heat3d_ext_wot ...
```

Per replay, into a folder per map (`out/01_karelia/...`):

- `<match>.parquet` - every vehicle's position and turret about ten times a
  second, and every event below where it happened.
- `<match>.match.json` - the map, the client version, who recorded it, the
  result, every player's line, and everything else the file holds (below).
- `<match>.messages.parquet` - the sidecar: every item of the replay the two
  files above do not hold whole, kept whole (see [Completeness](#completeness)).

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
| `event` | what the row is (below) |
| `player`, `team`, `own` | the player's name; team `1` or `2`; `1` on the recording player's rows |
| `vehicle`, `type` | the tank as the game names it (`ussr:R144_K_91`); `tank`, or `shell` for a tracer or explosion whose shooter is not known (no player) |
| `x`, `y`, `z` | metres: x east, y up, z north (the game's own world, left-handed) |
| `dirX`, `dirY`, `dirZ` | where the hull points, a unit vector in the same frame (`dirY` 0: heading only); on a shot or tracer where the shell flew |
| `turretYaw` | the turret's angle from the hull's heading, radians, positive to the right |
| `gunStep` | the gun's elevation as a step 0-63 between the gun's own limits (the limits are the tank's data, not the replay's) |
| `other`, `reason` | the other vehicle of an event (killer, victim, attacker, target); the game's attack reason number |
| `value`, `health` | the event's number (damage, burst, shell speed, zoom, command); health after a change |
| `text` | the reason's name, a chat line, a camera mode, a command's key |
| `shot` | the shell's id: a shot, its tracer and its explosion share it |
| `entity` | the vehicle's id in the replay |
| `pitch`, `roll` | on a position, the hull's pitch (radians, positive nose down) and roll, as the game sends them |

| `event` | On the row of | What |
|---|---|---|
| `position` | every vehicle | about ten times a second, while the client knew where it was |
| `death`, `kill` | the victim, the killer | each death twice: where the victim fell, and where the killer stood |
| `hurt`, `damage` | the victim, the attacker | a health change: `value` the damage, `health` what is left, `reason`/`text` why (`shot`, `fire`, `ramming`, ...) |
| `struck` | the victim | a shell that struck it, those that bounced or did not penetrate too: one row a point struck, `value` the damage it did (on the first); `hitComponent` the collision component, `hitU/V/W` where the shell went in and `hitExitU/V/W` where its path ended as fractions of that component's box (u right, v up, w forward; checked against the attacker's bearing), `hitDirX/Y/Z` the way it came in the hull's frame, `turretYaw` the victim's turret then, `hitCode` a byte sent with the point (not known: it does not follow the damage) |
| `shot` | the shooter | `value` the burst; the direction its tracer flew, else the hull's plus the turret's |
| `tracer` | the shooter | where a shell was first seen and the way it flew; `value` its speed in the game's units |
| `impact` | the shooter | where a shell exploded |
| `chat` | the sender | `text` the line |
| `command` | the sender | a battle chat command (attack, help, a point on the map), at its point when it has one; `value` the command's number, `other` the vehicle it names |
| `camera`, `zoom`, `lock`, `unlock` | the recording player | the camera mode (`sniper`, `arcade`, ...), the zoom, auto-aim on and off a target |

The Parquet footer carries the `heat3d` hints: Y up, Z flipped (so the map is
not mirrored), unit scale 1, a vehicle seven metres across, `player` as the
person, `team` as the group, `match` as the session.

## The summary

Besides the match's own lines: `players` (each with the header's and the
results' whole entry, the account's, and `seen` - the shots and damage the
recording client saw), `kills` (with where the time came from: `arena`,
`health` or `lifeTime`), `periods` (waiting, prebattle, battle, afterbattle,
with the server's end times), `basePoints` (capture progress per team and
base), `chat`, `commands` (with all their arguments), `camera`,
`clientEvents` (what the client recorded about itself: zoom, auto-aim, target
changes, tutorial markers, vehicle state flags), `arenaUpdates` (every arena
update decoded, as the game sent it), `serverSettings`, `results` (common,
personal with its per-target details, players, avatars), `resultVehicles`,
`frags`, and `decoded`: the method and packet numbers found for each kind.
Also `entities` (every entity the stream creates: its type number and role,
when it came into the client's view and when it left), `streamVersion` (the
version as the stream says it) and `selfCheck` (the completeness count, and
the checks of the entities and the version).

## What it reads, and how

A replay is a header of JSON blocks and the game's packet stream (format notes
in [`heat3d_ext_wot/bigworld.py`](heat3d_ext_wot/bigworld.py)):

- The first block, in the clear: the map, the client version, the recording
  player, the server's settings and the roster (`vehicles`: name, team, tank,
  keyed by the vehicle's id).
- The second, when the recording lasted to the end: the results screen -
  every vehicle's line (shots, hits, piercings, damage dealt, received,
  blocked and assisted, spotting, xp, credits, achievements...), the
  recording player's per-target details, the accounts, the match's duration,
  winner and finish reason; in some modes the only full roster (the header of
  those lists just the own team).
- The packet stream, zlib-compressed and Blowfish-enciphered with a key the
  game carries, which the community tools that read these files have published
  since 2013.

**Positions** are the engine's position updates: a vehicle's id, its position
and its heading, found by their shape rather than their packet number, so a
patch that renumbers them does not empty the table. They are what the
recording client was told: its own team throughout, an enemy only while
spotted (or in the client's range). A vehicle never spotted has no rows. Rows
of a vehicle stop at its death.

**The rest of the stream** - health, shots, tracers, explosions, hits, gun
angles, arena updates - is method calls and property changes of the vehicles
and of the client's avatar, numbered by the game's definition files, which
change with patches (1.12 and 2.4 number them differently). Each is found by
the shape of its arguments and how they hang together - see
[`heat3d_ext_wot/stream.py`](heat3d_ext_wot/stream.py) - and the numbers found
are in the summary's `decoded`. Chat, the camera mode and the client's own
events are packets of their own. Arena updates and client events are Python
pickles; they are read by a reader that turns every class they name into an
inert stand-in and runs nothing.

What the client was told is complete for its own team and partial for
enemies: their shots, hits and health changes are there while they were in
range.

**The battle's start** is when the arena update says the battle period began;
in a replay without it, the first moment any vehicle moves.

**Deaths:** the time is the arena's kill message (1.x), else the health change
that ended the vehicle, else the battle's start plus the victim's `lifeTime`
from the results (whole seconds). The place is where the victim was last seen,
when that was within five seconds of its death; else, on 2.x clients, the
place the results give (x and z, no height), in the summary only. A recording
that stopped before the end has no deaths.

**Not read:**

- Spotting and the minimap: not in the stream as events of their own.
- The gun's elevation in degrees: the stream has a step between the gun's
  limits, and the limits are in the game's vehicle files.
- Module damage, crew injuries, consumables and ammunition: the calls that
  carry them could not be told apart by shape alone across 1.12 and 2.4.
- Entity creation packets beyond the entity and its type: they hold every
  property of a vehicle entering the client's view at once, in an order only
  the definition files give (kept whole in the sidecar).
- Static collisions (trees, houses), the recording player's own aiming and
  physics packets.
- Battle chat command numbers as names: the numbering is the game's and
  changes; the summary keeps each command's arguments, among them its key
  where it has one (`ATTACK_ENEMY`, ...).
- Attack reasons above 5: written as numbers only.

## Verified

On public replays, at 2026-11-07:

| Client | Map | Vehicles | Positions | Rate | Deaths (placed) |
|---|---|---|---|---|---|
| 1.12.0 (April 2021) | Karelia | 30 of 30 seen | 47,586 | 10 Hz | 22 (22) |
| 2.4.1 (November 2026) | Westfeld | 28 of 30 seen | 45,424 | 10 Hz | 23 (20 with height, 3 from the results) |
| 2.4.1 | Great Wall | 29 of 30 seen | 50,806 | 10 Hz | 25 (21; 4 never seen near their death) |
| 2.4.1, battle type 20 | Pilsen | 14 of 14 | 15,717 | 10 Hz | 10 (all) |

Checks on the positions: the coordinates span about 1 km (the maps are 1 km
across); speeds have a median of 22 km/h and a 99th percentile of 66 km/h; the
heading agrees with the direction of travel to 0.02 rad; where the 2.4.1
results give a death's place (9 deaths on Great Wall), the place read here is
a median of 1.1 m from it, at most 4.5 m.

Checks on the rest, in the order Karelia, Great Wall, Westfeld, Pilsen:

- **The recording player**, whose events the client always has: the shots
  read equal the results' `shots` (10, 21, 18, 2), the damage dealt read
  equals the results' `damageDealt` (1,033 to 3,397), on every replay.
- **Health:** each vehicle's last health read equals the results' `health`
  (24/24, 26/28, 23/23, 14/14 vehicles); the damage received read is never
  more than the results' and equal for 23/24, 16/28, 21/23, 14/14 - on 2.4.1
  the killing blow to a vehicle out of the client's view is often not sent.
- **Hits:** on 1.12 a hit's damage factor is non-zero exactly when the
  vehicle's health changed at that moment (143 of 143); on 2.4.1 a hit's
  damage equals the health change at that moment (142 of 143, 103 of 106,
  74 of 75).
- **Turret:** at a shot, the hull's heading plus the turret's yaw is a median
  0.004-0.007 rad from the direction its tracer flew (167, 209, 193, 104
  shots).
- **Deaths** read from the arena or the health are 0 to 1.04 s after the
  battle's start plus the results' whole-second `lifeTime` (median 0.4-0.7 s).
- **Battle start:** the arena's battle period begins 0.6 s before the first
  vehicle moves, on every replay.

The tests build replays to the same layout, so no real replay is kept in this
repository.

**Not checked:** clients before 1.12, console and Blitz replays (different
games), Lesta's Mir Tankov (`.mtreplay`), and modes other than random battles
and battle type 20.

## Completeness

The converter follows the rule all 3DHeat converters share,
[Converters keep everything](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md):
what it reads goes into the table and the summary; every other item of the
replay is kept whole in the sidecar `<match>.messages.parquet`; and the
summary's `selfCheck.completeness` counts, for each kind of item, how many the
replay holds (`seen`), how many were read whole (`decoded`), read in part and
kept whole (`partial`), only kept (`raw`), and lost (`lost`, 0).

The kinds are the replay's own: `block 0` (the header), `block 1` (the
results), `container sizes` and `deflate tail` (the container's own bytes),
`packet <type>`, and for entity calls `method <entity type>.<number>` and
`property <entity type>.<number>`. Entity types are the numbers the creating
packets give; the summary's `selfCheck.entities.roles` says which is the
recording player's avatar and which the vehicles (2 and 6 on every replay
read). They are counted as the converter meets them in the stream, so a kind
nobody knew of shows up with its count.

The sidecar's columns: `time` (the replay's clock, as the table's),
`type`, `name` (what the converter calls it, where it reads it), `entity` (the
vehicle or avatar it belongs to, as the table's `entity`), `decoded` (what was
read of it, JSON), `payload` (its bytes, whole: a packet's payload as the
stream has it), `text` (the JSON blocks, whole), `entityType`, `packet` and
`method` (the numbers). Rows are sorted by packet, method, entity and time.
Everything a later reader needs is in it, or in the summary's `entities`.

**Read** (new in this pass, each checked against something independent):

- **Pitch and roll** of every position (`pitch`, `roll`). Pitch: on Karelia,
  Great Wall, Westfeld and Pilsen it is minus the slope of the vehicle's own
  path while it drives forward (correlation -0.96, -0.96, -0.98, -0.84;
  median difference 0.003-0.008 rad). Roll: two vehicles at the same spot
  (within 0.5 m) with the same heading have the same roll (correlation 0.98,
  0.99, 0.98 on Karelia, Westfeld, Great Wall), with opposite headings
  opposite rolls (-0.98, -0.997, -0.98).
- **Entities** (summary `entities`): the creating packets (0 and 5) give the
  entity and its type, the rest of them is kept; the leaving packet (4: the
  entity alone) is read whole. Check: no vehicle has a position update
  between leaving and coming back (0 on all four; 192, 180, 141 and 190
  entities, 199, 141, 105 and 280 leaves).
- **The version in the stream** (packet 24, `streamVersion`): the same as the
  header's on all four.
- **The recording player's aim** (packet 38, 40 bytes, about 10 a second): a
  rotation (x, y, z, w) whose +z is where the player aims; the sidecar's
  `decoded` has that direction (`forward`). Check: at the player's shots it
  is a median 0.14 and 0.14 degrees (26 and 19 shots, 2.4.1) and 0.56 (11
  shots, 1.12) from the direction the shell flew; 6 degrees on the replay with
  2 shots.

Everything read before this pass (health, hits, shots, tracers, explosions,
gun angles, arena updates, chat, camera modes, client events) is `partial`:
read into the table and the summary as above, and kept whole in the sidecar
with what was read in `decoded`. So are the positions: the table has place,
heading, pitch and roll, the sidecar the whole update.

**Kept raw** (in the sidecar, not read), the biggest kinds:

- `packet 10`, the position updates not in the table: the avatar's (it rides
  the vehicle: the second id is the vehicle's), positions after a vehicle's
  death, entities not in the roster; and in every update three floats
  (BigWorld calls them the position's error; not checked) and a flag byte (1
  but for 20-28 updates a replay; not known).
- `packet 26` and `packet 31`, about 10 a second, as many of each: 26 is
  52 bytes (1.12) or 60 (2.4.1) of floats beginning with a point in the
  world, 31 four bytes; not known. `packet 28`, `29` (a float
  each), `57` (2.x, 72 bytes), `54` (2.x, empty): not known.
- The vehicles' frequent 2-byte property (`property 6.11` in 1.12, `6.15` in
  2.4.1) and 1-byte property `6.1`, the avatar's 8-byte property (`2.17`,
  2.19 in 2.4.1): not known.
- `packet 36`: an entity, a byte, a length and that many bytes (likely a
  change inside a property; not read). Every method and property without a
  reader (module damage, crew, consumables and the like among them), the
  entity creations' properties, `packet 50` and the rest.

Per replay (the four of [Verified](#verified)):

| Replay | Seen | Decoded | Partial | Raw | Lost | Sidecar | Replay |
|---|---|---|---|---|---|---|---|
| Karelia 1.12 | 112,582 | 200 | 77,685 | 34,697 | 0 | 1.11 MB | 1.48 MB |
| Great Wall 2.4.1 | 157,992 | 281 | 86,633 | 71,078 | 0 | 1.75 MB | 2.41 MB |
| Westfeld 2.4.1 | 117,360 | 106 | 74,557 | 42,697 | 0 | 1.14 MB | 1.65 MB |
| Pilsen 2.4.1 | 46,880 | 142 | 26,918 | 19,820 | 0 | 0.47 MB | 0.70 MB |

**Not available:**

- What the server never sent the recording client: other players' aim,
  camera and inputs, enemies while unspotted. A replay is what one client
  was told.
- The names of entity types, methods and properties: they are in the game's
  definition files, not in the replay. The numbers are kept; the converter
  names what it finds by content.
- The gun's elevation in degrees and anything else that needs the tanks'
  own data (the game's vehicle files, not the replay).

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
