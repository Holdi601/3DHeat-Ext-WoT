---
title: "Dokumenti i ndeshjes"
nav_order: 6
lang: sq
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokumenti i ndeshjes {#the-match-document}

`<match>.match.json` mban gjithçka që thotë riluajtja dhe që nuk është rresht i
tabelës. Skeda Ndeshja e shikuesit e lexon. (Kodi e quan summary.)

![Fillimi i një dokumenti ndeshjeje sintetik, dhe çelësat e tij](../assets/img/match-document.svg)

## Beteja {#the-battle}

| Çelësi | Çfarë |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; ID e betejës; ID e hartës dhe emri i saj i shfaqur |
| `clientVersion`, `streamVersion` | versioni i lojës nga header-i, dhe siç e thotë rrjedha e paketave |
| `recorded` | kur u regjistrua riluajtja, siç e shkruan loja |
| `player`, `vehicle` | lojtari që regjistron dhe tanku i tij |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | numri i llojit të betejës nga header-i, mënyra e lojës, serveri, rajoni, dhe nëse ishin instaluar mod-e |
| `duration` | gjatësia e betejës në sekonda, nga rezultatet |
| `winnerTeam`, `finishReason` | skuadra fituese dhe numri i lojës për mënyrën si mbaroi beteja, nga rezultatet |
| `complete`, `truncated` | rezultatet janë në riluajtje; regjistrimi u ndal herët |
| `battleStart`, `battleStartFrom`, `firstMovement` | fillimi i betejës në sekonda të regjistrimit; `arena` (arena e tha këtë) ose `movement` (çasti i parë kur lëvizi ndonjë tank); ajo lëvizja e parë |
| `recordingSeconds` | gjatësia e regjistrimit në sekonda |
| `positionPacket`, `hz`, `positions` | numri i paketës në të cilën erdhën pozicionet, mostra në sekondë, rreshta pozicioni |
| `events` | numri i rreshtave të tabelës për çdo ngjarje |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metoda dhe numrat e paketave të gjetura për çdo lloj mesazhi |

## Lojtarët dhe ngjarjet {#players-and-events}

| Çelësi | Çfarë |
|---|---|
| `players` | një hyrje për tank: emri, skuadra, tanku, klani, mostrat, vrasjet, dëmi i shkaktuar, mbijetoi, koha e jetës; `seen` (të shtënat dhe dëmi që pa klienti që regjistron); hyrja e plotë e header-it dhe e rezultateve, dhe ajo e llogarisë |
| `kills` | çdo vdekje: koha (sekonda), nga erdhi koha (`arena`, `health` ose `lifeTime`), viktima, vrasësi, numri dhe emri i arsyes |
| `periods` | periudhat e betejës (waiting, prebattle, battle, afterbattle) me kohët e mbarimit nga serveri |
| `basePoints` | progresi i kapjes së bazës për skuadër dhe bazë |
| `chat`, `commands` | rreshta bisede; komandat e bisedës së betejës me të gjitha argumentet e tyre |
| `camera`, `clientEvents` | mënyrat e kamerës së lojtarit që regjistron; çfarë regjistroi klienti për veten (zmadhimi, synimi automatik, ndryshimet e objektivit, gjendja e mjetit) |
| `arenaUpdates` | çdo përditësim i arenës, i dekoduar, siç e dërgoi loja |

## Rezultatet dhe kontrollet {#results-and-checks}

| Çelësi | Çfarë |
|---|---|
| `serverSettings` | cilësimet e serverit nga header-i |
| `results`, `resultVehicles`, `frags` | ekrani i rezultateve: të përbashkëta, personale (me detaje për objektiv), lojtarët, llogaritë; rreshti i rezultateve i çdo tanku; vrasjet për lojtar |
| `entities` | çdo entitet që krijon rrjedha: numri i llojit dhe roli i tij, kur hyri në pamjen e klientit dhe kur doli |
| `selfCheck` | numërimi i plotësisë ([Plotësia](completeness.md)) dhe kontrollet e entiteteve dhe të versionit |

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
