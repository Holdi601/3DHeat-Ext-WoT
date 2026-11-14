---
title: How it reads a replay
nav_order: 6
---

# How it reads a replay

A replay is a header of JSON blocks and the game's packet stream (format notes
in [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

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
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - and the numbers found
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

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
