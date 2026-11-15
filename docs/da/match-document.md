---
title: Kampdokumentet
nav_order: 6
lang: da
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Kampdokumentet {#the-match-document}

`<match>.match.json` indeholder alt det, replayet siger, som ikke er en række i tabellen. Viewerens
Kamp-fane læser den. (Koden kalder den resuméet.)

![Starten af et syntetisk kampdokument, og dets nøgler](../assets/img/match-document.svg)

## Slaget {#the-battle}

| Nøgle | Hvad |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; kampens id; kortets id og dets visningsnavn |
| `clientVersion`, `streamVersion` | spilversionen fra headeren, og som pakkestrømmen siger den |
| `recorded` | hvornår replayet blev optaget, som spillet skriver det |
| `player`, `vehicle` | den optagende spiller og dennes tank |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | headerens kamptypenummer, spiltilstand, server, region, og om mods var installeret |
| `duration` | kampens længde i sekunder, fra resultaterne |
| `winnerTeam`, `finishReason` | det vindende hold og spillets nummer for, hvordan kampen endte, fra resultaterne |
| `complete`, `truncated` | resultaterne er i replayet; optagelsen stoppede tidligt |
| `battleStart`, `battleStartFrom`, `firstMovement` | kampens start i sekunder af optagelsen; `arena` (arenaen sagde det) eller `movement` (det første øjeblik, en tank bevægede sig); det første bevægelsestidspunkt |
| `recordingSeconds` | optagelsens længde i sekunder |
| `positionPacket`, `hz`, `positions` | pakkenummeret positionerne kom i, samples i sekundet, positionsrækker |
| `events` | antallet af tabelrækker for hver begivenhed |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metode- og pakkenumrene, der er fundet for hver slags meddelelse |

## Spillere og begivenheder {#players-and-events}

| Nøgle | Hvad |
|---|---|
| `players` | én post pr. tank: navn, hold, tank, klan, samples, drab, forvoldt skade, overlevet, levetid; `seen` (skuddene og skaden den optagende klient så); headerens og resultaternes hele post, og kontoens |
| `kills` | hvert dødsfald: tidspunkt (sekunder), hvor tidspunktet kom fra (`arena`, `health` eller `lifeTime`), offer, dræber, årsagsnummer og -navn |
| `periods` | kampens perioder (venten, forkamp, kamp, efterkamp) med serverens sluttidspunkter |
| `basePoints` | basens erobringsfremskridt pr. hold og base |
| `chat`, `commands` | chatlinjer; kampchatkommandoer med alle deres argumenter |
| `camera`, `clientEvents` | den optagende spillers kameratilstande; det klienten optog om sig selv (zoom, automatisk sigte, målskift, køretøjets tilstand) |
| `arenaUpdates` | hver arenaopdatering, afkodet, som spillet sendte den |

## Resultater og kontroller {#results-and-checks}

| Nøgle | Hvad |
|---|---|
| `serverSettings` | serverens indstillinger fra headeren |
| `results`, `resultVehicles`, `frags` | resultatskærmen: fælles, personlig (med detaljer pr. mål), spillere, konti; hvert køretøjs resultatlinje; drab pr. spiller |
| `entities` | hver entitet strømmen opretter: dens typenummer og rolle, hvornår den kom ind i klientens udsyn, og hvornår den forlod det |
| `selfCheck` | fuldstændighedstællingen ([Fuldstændighed](completeness.md)) og kontrollerne af entiteterne og versionen |

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
