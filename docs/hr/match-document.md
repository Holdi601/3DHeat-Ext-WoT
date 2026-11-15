---
title: Dokument meča
nav_order: 6
lang: "hr"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokument meča {#the-match-document}

`<match>.match.json` drži sve što snimka kaže, a što nije redak tablice. Kartica Meč
preglednika ga čita. (Kod ga zove sažetak.)

![Početak sintetičkog dokumenta meča, i njegovi ključevi](../assets/img/match-document.svg)

## Bitka {#the-battle}

| Ključ | Što |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; id bitke; id karte i njezin prikazni naziv |
| `clientVersion`, `streamVersion` | verzija igre iz zaglavlja, i kako ju kaže tok paketa |
| `recorded` | kad je snimka zabilježena, kako je igra zapisuje |
| `player`, `vehicle` | igrač koji snima i njegov tenk |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | broj vrste bitke iz zaglavlja, način igre, poslužitelj, regija, i jesu li modovi bili instalirani |
| `duration` | trajanje bitke u sekundama, iz rezultata |
| `winnerTeam`, `finishReason` | pobjednički tim i igrin broj za to kako je bitka završila, iz rezultata |
| `complete`, `truncated` | rezultati su u snimci; snimanje je stalo rano |
| `battleStart`, `battleStartFrom`, `firstMovement` | početak bitke u sekundama snimanja; `arena` (arena je to rekla) ili `movement` (prvi trenutak kad se bilo koji tenk pomaknuo); taj prvi pomak |
| `recordingSeconds` | trajanje snimanja u sekundama |
| `positionPacket`, `hz`, `positions` | broj paketa u kojem su došli položaji, uzoraka u sekundi, redci položaja |
| `events` | broj redaka tablice za svaki događaj |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metode i brojevi paketa nađeni za svaku vrstu poruke |

## Igrači i događaji {#players-and-events}

| Ključ | Što |
|---|---|
| `players` | jedan unos po tenku: ime, tim, tenk, klan, uzorci, ubojstva, nanesena šteta, preživljeno, vrijeme života; `seen` (hici i šteta koje je klijent koji snima vidio); cijeli unos iz zaglavlja i rezultata, i račun |
| `kills` | svaka smrt: vrijeme (sekunde), odakle je vrijeme došlo (`arena`, `health` ili `lifeTime`), žrtva, ubojica, broj i naziv razloga |
| `periods` | razdoblja bitke (čekanje, prebitka, bitka, nakon bitke) sa završnim vremenima poslužitelja |
| `basePoints` | napredak zauzimanja baze po timu i bazi |
| `chat`, `commands` | redovi razgovora; naredbe bitke u razgovoru sa svim njihovim argumentima |
| `camera`, `clientEvents` | načini kamere igrača koji snima; što je klijent zabilježio o sebi (zum, automatsko ciljanje, promjene cilja, stanje vozila) |
| `arenaUpdates` | svako ažuriranje arene, dekodirano, kako ga je igra poslala |

## Rezultati i provjere {#results-and-checks}

| Ključ | Što |
|---|---|
| `serverSettings` | postavke poslužitelja iz zaglavlja |
| `results`, `resultVehicles`, `frags` | ekran rezultata: zajedničko, osobno (s pojedinostima po meti), igrači, računi; redak rezultata svakog tenka; ubojstva po igraču |
| `entities` | svaki entitet koji tok stvara: njegov broj vrste i uloga, kad je ušao u pogled klijenta i kad je izašao |
| `selfCheck` | brojanje potpunosti ([Potpunost](completeness.md)) i provjere entiteta i verzije |

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
