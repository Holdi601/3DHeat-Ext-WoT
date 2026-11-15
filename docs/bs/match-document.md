---
title: "Dokument meča"
nav_order: 6
lang: bs
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokument meča {#the-match-document}

`<match>.match.json` sadrži sve što replay kaže a nije red
tabele. Kartica Meč preglednika ga čita. (Kod ga naziva sažetkom.)

![Početak sintetičkog dokumenta meča i njegovi ključevi](../assets/img/match-document.svg)

## Bitka {#the-battle}

| Ključ | Šta |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; id bitke; id mape i njeno prikazano ime |
| `clientVersion`, `streamVersion` | verzija igre iz zaglavlja, i kako je kaže tok paketa |
| `recorded` | kada je replay snimljen, kako ga igra piše |
| `player`, `vehicle` | igrač koji snima i njegov tenk |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | broj tipa bitke iz zaglavlja, način igre, server, regija i jesu li instalirani modovi |
| `duration` | trajanje bitke u sekundama, iz rezultata |
| `winnerTeam`, `finishReason` | pobjednički tim i broj igre za to kako se bitka završila, iz rezultata |
| `complete`, `truncated` | rezultati su u replayu; snimanje je stalo prije vremena |
| `battleStart`, `battleStartFrom`, `firstMovement` | početak bitke u sekundama snimka; `arena` (arena je to rekla) ili `movement` (prvi trenutak kad se ijedan tenk pomjerio); to prvo kretanje |
| `recordingSeconds` | trajanje snimka u sekundama |
| `positionPacket`, `hz`, `positions` | broj paketa u kojem su došle pozicije, uzoraka u sekundi, redovi pozicija |
| `events` | broj redova tabele za svaki događaj |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metoda i brojevi paketa pronađeni za svaku vrstu poruke |

## Igrači i događaji {#players-and-events}

| Ključ | Šta |
|---|---|
| `players` | jedna stavka po tenku: ime, tim, tenk, klan, uzorci, ubistva, nanesena šteta, preživio, vrijeme života; `seen` (hici i šteta koje je klijent koji snima vidio); cijela stavka iz zaglavlja i iz rezultata, i računa |
| `kills` | svaka smrt: vrijeme (sekunde), odakle je vrijeme došlo (`arena`, `health` ili `lifeTime`), žrtva, ubica, broj i ime razloga |
| `periods` | periodi bitke (čekanje, prije bitke, bitka, poslije bitke) s krajnjim vremenima servera |
| `basePoints` | napredak zauzimanja baze po timu i bazi |
| `chat`, `commands` | redovi četa; naredbe četa bitke sa svim njihovim argumentima |
| `camera`, `clientEvents` | načini kamere igrača koji snima; šta je klijent zabilježio o sebi (zum, automatsko ciljanje, promjene mete, stanje vozila) |
| `arenaUpdates` | svako ažuriranje arene, dekodirano, kako ga je igra poslala |

## Rezultati i provjere {#results-and-checks}

| Ključ | Šta |
|---|---|
| `serverSettings` | postavke servera iz zaglavlja |
| `results`, `resultVehicles`, `frags` | ekran rezultata: opće, lične (s detaljima po meti), igrači, računi; red rezultata svakog tenka; ubistva po igraču |
| `entities` | svaki entitet koji tok stvara: njegov broj tipa i uloga, kada je ušao u vidokrug klijenta i kada ga je napustio |
| `selfCheck` | broj potpunosti ([Potpunost](completeness.md)) i provjere entiteta i verzije |

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
