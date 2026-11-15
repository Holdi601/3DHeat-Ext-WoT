---
title: How it reads a replay
nav_order: 7
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
are in the match document's `decoded`. Chat, the camera mode and the client's own
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
place the results give (x and z, no height), in the match document only. A recording
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
  changes; the match document keeps each command's arguments, among them its key
  where it has one (`ATTACK_ENEMY`, ...).
- Attack reasons above 5: written as numbers only.

## How the reading was checked

The reading was checked on public replays of clients 1.12 and 2.4, each
value against something the replay gives a second time:

- **Positions:** every tank ever seen has a track at ten samples a second;
  speeds stay within what a tank can do; the heading agrees with the
  direction of travel to about 0.02 rad; where the results give a death's
  place, the place read here is within a few metres of it.
- **The recording player:** the shots and the damage dealt read equal the
  results' values, on every replay checked.
- **Health:** each tank's last health read equals the results'; the damage
  received read is never more than the results'. On 2.4 the killing blow to
  a tank out of the client's view is often not sent.
- **Hits:** a hit's damage equals the health change at that moment for
  nearly every hit.
- **Turret:** at a shot, the hull's heading plus the turret's yaw points
  where the tracer flew, within about 0.01 rad (median).
- **Deaths and the battle's start:** within about a second of what the
  results and the arena say.

The tests build replays to the same layout, so no real replay is kept in
this repository.

**Not checked:** clients before 1.12, console and Blitz replays (different
games), Lesta's Mir Tankov (`.mtreplay`), and modes other than random battles
and battle type 20.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
