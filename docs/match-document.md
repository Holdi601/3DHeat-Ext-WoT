---
title: The match document
nav_order: 5
---

# The match document

`<match>.match.json` holds everything the replay says that is not a row of
the table. The viewer's Match tab reads it.

![The start of a synthetic match document, and its keys](assets/img/match-document.svg)

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

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
