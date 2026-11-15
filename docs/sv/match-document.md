---
title: "Matchdokumentet"
nav_order: 6
lang: sv
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Matchdokumentet {#the-match-document}

`<match>.match.json` håller allt repriset säger som inte är en rad i tabellen. Visarens
Match-flik läser det. (Koden kallar det sammanfattningen.)

![Början av ett syntetiskt matchdokument, och dess nycklar](../assets/img/match-document.svg)

## Striden {#the-battle}

| Nyckel | Vad |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; stridens id; kartans id och dess visningsnamn |
| `clientVersion`, `streamVersion` | spelversionen ur headern, och så som paketströmmen anger den |
| `recorded` | när repriset spelades in, så som spelet skriver det |
| `player`, `vehicle` | den inspelande spelaren och dess stridsvagn |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | headerns stridstypsnummer, spelläge, server, region, och om moddar var installerade |
| `duration` | stridens längd i sekunder, från resultaten |
| `winnerTeam`, `finishReason` | det vinnande laget och spelets nummer för hur striden slutade, från resultaten |
| `complete`, `truncated` | resultaten finns i repriset; inspelningen stoppade tidigt |
| `battleStart`, `battleStartFrom`, `firstMovement` | stridens start i sekunder av inspelningen; `arena` (arenan sa det) eller `movement` (det första ögonblick någon stridsvagn rörde sig); den första rörelsen |
| `recordingSeconds` | inspelningens längd i sekunder |
| `positionPacket`, `hz`, `positions` | paketnumret positionerna kom i, mätpunkter per sekund, positionsrader |
| `events` | antalet tabellrader för varje händelse |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metod- och paketnumren som hittats för varje slag av meddelande |

## Spelare och händelser {#players-and-events}

| Nyckel | Vad |
|---|---|
| `players` | en post per stridsvagn: namn, lag, stridsvagn, klan, mätpunkter, dödsfall, given skada, överlevde, livstid; `seen` (skotten och skadan som den inspelande klienten såg); hela posten från headern och resultaten, och kontots |
| `kills` | varje dödsfall: tid (sekunder), varifrån tiden kom (`arena`, `health` eller `lifeTime`), offer, dödare, orsaksnummer och namn |
| `periods` | stridens perioder (väntan, förstrid, strid, efterstrid) med serverns sluttider |
| `basePoints` | baserobbningens framsteg per lag och bas |
| `chat`, `commands` | chattrader; stridschattens kommandon med alla sina argument |
| `camera`, `clientEvents` | den inspelande spelarens kamerelägen; vad klienten spelade in om sig själv (zoom, sikthjälp, målbyten, fordonsstatus) |
| `arenaUpdates` | varje arenauppdatering, avkodad, så som spelet skickade den |

## Resultat och kontroller {#results-and-checks}

| Nyckel | Vad |
|---|---|
| `serverSettings` | serverns inställningar ur headern |
| `results`, `resultVehicles`, `frags` | resultatskärmen: gemensamt, personligt (med detaljer per mål), spelare, konton; varje stridsvagns resultatrad; dödsfall per spelare |
| `entities` | varje entitet strömmen skapar: dess typnummer och roll, när den kom in i klientens syn och när den lämnade den |
| `selfCheck` | fullständighetsräkningen ([Fullständighet](completeness.md)) och kontrollerna av entiteterna och versionen |

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
