---
title: The match document
nav_order: 6
---

# The match document

`<match>.match.json` holds everything the replay says that is not a row of
the table. The viewer's Match tab reads it. (The code calls it the summary.)

![The start of a synthetic match document, and its keys](assets/img/match-document.svg)

## The battle

| Key | What |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; the battle's id; the map's id and its display name |
| `clientVersion`, `streamVersion` | the game version from the header, and as the packet stream says it |
| `recorded` | when the replay was recorded, as the game writes it |
| `player`, `vehicle` | the recording player and their tank |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | the header's battle type number, game mode, server, region, and whether mods were installed |
| `duration` | the battle's length in seconds, from the results |
| `winnerTeam`, `finishReason` | the winning team and the game's number for how the battle ended, from the results |
| `complete`, `truncated` | the results are in the replay; the recording stopped early |
| `battleStart`, `battleStartFrom`, `firstMovement` | the battle's start in seconds of the recording; `arena` (the arena said so) or `movement` (the first moment any tank moved); that first movement |
| `recordingSeconds` | the recording's length in seconds |
| `positionPacket`, `hz`, `positions` | the packet number the positions came in, samples a second, position rows |
| `events` | the number of table rows of each event |
| `units` | `metres; x east, y up, z north` |
| `decoded` | the method and packet numbers found for each kind of message |

## Players and events

| Key | What |
|---|---|
| `players` | one entry a tank: name, team, tank, clan, samples, kills, damage dealt, survived, life time; `seen` (the shots and damage the recording client saw); the header's and the results' whole entry, and the account's |
| `kills` | every death: time (seconds), where the time came from (`arena`, `health` or `lifeTime`), victim, killer, reason number and name |
| `periods` | the battle's periods (waiting, prebattle, battle, afterbattle) with the server's end times |
| `basePoints` | base capture progress per team and base |
| `chat`, `commands` | chat lines; battle chat commands with all their arguments |
| `camera`, `clientEvents` | the recording player's camera modes; what the client recorded about itself (zoom, auto-aim, target changes, vehicle state) |
| `arenaUpdates` | every arena update, decoded, as the game sent it |

## Results and checks

| Key | What |
|---|---|
| `serverSettings` | the server's settings from the header |
| `results`, `resultVehicles`, `frags` | the results screen: common, personal (with per-target details), players, accounts; every tank's results line; kills per player |
| `entities` | every entity the stream creates: its type number and role, when it came into the client's view and when it left |
| `selfCheck` | the completeness count ([Completeness](completeness.md)) and the checks of the entities and the version |

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
