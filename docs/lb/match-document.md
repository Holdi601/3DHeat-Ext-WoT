---
title: "D'Match-Dokument"
nav_order: 6
lang: lb
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# D'Match-Dokument {#the-match-document}

`<match>.match.json` enthält alles, wat de Replay seet an net eng Zeil vun der
Tabell ass. Dem Viewer säi Match-Tab liest et. (De Code nennt et d'Zesummefaassung.)

![Den Ufank vun engem synthetesche Match-Dokument, a seng Schlësselen](../assets/img/match-document.svg)

## D'Gefecht {#the-battle}

| Schlëssel | Wat |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; d'ID vum Gefecht; d'ID vun der Kaart a säin Uweisungsnumm |
| `clientVersion`, `streamVersion` | d'Spillversioun aus dem Header, an dat, wat de Paketstroum seet |
| `recorded` | wéini de Replay opgeholl gouf, wéi d'Spill et schreift |
| `player`, `vehicle` | den opuelende Spiller a säi Panzer |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | d'Gefechtstypnummer aus dem Header, de Spillmodus, de Server, d'Regioun, an ob Mods installéiert waren |
| `duration` | d'Längt vum Gefecht a Sekonnen, aus de Resultater |
| `winnerTeam`, `finishReason` | d'Gewënnerteam an dem Spill seng Nummer dofir, wéi d'Gefecht opgehalen huet, aus de Resultater |
| `complete`, `truncated` | d'Resultater sinn am Replay; d'Opnam huet fréi opgehalen |
| `battleStart`, `battleStartFrom`, `firstMovement` | den Ufank vum Gefecht a Sekonne vun der Opnam; `arena` (d'Arena huet et gesot) oder `movement` (dee Moment, wou e Panzer fir d'éischt beweegt gouf); déi éischt Beweegung |
| `recordingSeconds` | d'Längt vun der Opnam a Sekonnen |
| `positionPacket`, `hz`, `positions` | d'Paketnummer, an där d'Positioune koumen, Echantillonen d'Sekonn, Positiounszeilen |
| `events` | d'Zuel vun den Tabellzeile vun all Evenement |
| `units` | `metres; x east, y up, z north` |
| `decoded` | d'Method an d'Paketnummere, déi fir all Aart Message fonnt goufen |

## Spiller an Evenementer {#players-and-events}

| Schlëssel | Wat |
|---|---|
| `players` | een Androung pro Panzer: Numm, Team, Panzer, Clan, Echantillonen, Kills, ausgedeelte Schued, iwwerlieft, Liewenszäit; `seen` (d'Schëss a de Schued, déi den opuelende Client gesinn huet); dem Header seng a dem Resultater seng ganz Androung, an déi vum Kont |
| `kills` | all Doud: Zäit (Sekonnen), vu wou d'Zäit koum (`arena`, `health` oder `lifeTime`), Affer, Killer, Grondnummer an -numm |
| `periods` | d'Perioden vum Gefecht (waiting, prebattle, battle, afterbattle) mat den Enn-Zäite vum Server |
| `basePoints` | Fortschrëtt vun der Basiseroberung pro Team a Basis |
| `chat`, `commands` | Chat-Zeilen; Kommandoe vum Gefechtschat mat all hire Argumenter |
| `camera`, `clientEvents` | d'Kameramoduse vum opuelende Spiller; wat de Client iwwer sech selwer opgeholl huet (Zoom, Auto-Zil, Zilännerungen, Gefierzoustand) |
| `arenaUpdates` | all Arena-Update, decodéiert, wéi d'Spill en geschéckt huet |

## Resultater a Kontrollen {#results-and-checks}

| Schlëssel | Wat |
|---|---|
| `serverSettings` | d'Astellunge vum Server aus dem Header |
| `results`, `resultVehicles`, `frags` | de Resultater-Ecran: allgemeng, perséinlech (mat Detailer pro Zil), Spiller, Konten; d'Resultaterzeil vun all Panzer; Kills pro Spiller |
| `entities` | all Entitéit, déi de Stroum erstellt: hir Typnummer a Roll, wéini se an de Bléck vum Client koum a wéini se fortgaang ass |
| `selfCheck` | d'Vollstännegkeetszielung ([Vollstännegkeet](completeness.md)) an d'Kontrolle vun den Entitéiten an der Versioun |

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
