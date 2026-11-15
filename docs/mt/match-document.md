---
title: "Id-dokument tal-partita"
nav_order: 6
lang: mt
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Id-dokument tal-partita {#the-match-document}

`<match>.match.json` iżomm dak kollu li r-ripetizzjoni tgħid li mhuwiex ringiela
tat-tabella. It-tab Partita tal-viewer taqrah. (Il-kodiċi jsejjaħlu s-sommarju.)

![Il-bidu ta' dokument tal-partita sintetiku, u ċ-ċwievet tiegħu](../assets/img/match-document.svg)

## Il-battalja {#the-battle}

| Ċavetta | X'inhi |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; l-id tal-battalja; l-id tal-mappa u l-isem tagħha li jidher |
| `clientVersion`, `streamVersion` | il-verżjoni tal-logħba mill-header, u kif tgħidha l-fluss tal-pakketti |
| `recorded` | meta ġiet irreġistrata r-ripetizzjoni, kif jikteb il-logħba |
| `player`, `vehicle` | il-plejer li rreġistra u t-tank tiegħu |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | in-numru tat-tip ta' battalja tal-header, il-modalità tal-logħba, is-server, ir-reġjun, u jekk kienux installati mods |
| `duration` | it-tul tal-battalja f'sekondi, mir-riżultati |
| `winnerTeam`, `finishReason` | it-tim rebbieħ u n-numru tal-logħba għal kif spiċċat il-battalja, mir-riżultati |
| `complete`, `truncated` | ir-riżultati huma fir-ripetizzjoni; ir-reġistrazzjoni waqfet kmieni |
| `battleStart`, `battleStartFrom`, `firstMovement` | il-bidu tal-battalja f'sekondi tar-reġistrazzjoni; `arena` (l-arena qalet hekk) jew `movement` (l-ewwel mument li xi tank iċċaqlaq); dak l-ewwel moviment |
| `recordingSeconds` | it-tul tar-reġistrazzjoni f'sekondi |
| `positionPacket`, `hz`, `positions` | in-numru tal-pakkett li fih waslu l-pożizzjonijiet, kampjuni fit-tieni, ringieli ta' pożizzjoni |
| `events` | in-numru ta' ringieli tat-tabella għal kull avveniment |
| `units` | `metres; x east, y up, z north` |
| `decoded` | il-metodu u n-numri tal-pakketti misjuba għal kull tip ta' messaġġ |

## Plejers u avvenimenti {#players-and-events}

| Ċavetta | X'inhi |
|---|---|
| `players` | daħla għal kull tank: isem, tim, tank, clan, kampjuni, qtil, ħsara magħmula, baqa' ħaj, żmien ta' ħajja; `seen` (is-sparaturi u l-ħsara li ra l-klijent li rreġistra); id-daħla sħiħa tal-header u tar-riżultati, u tal-kont |
| `kills` | kull mewt: ħin (sekondi), minn fejn ġie l-ħin (`arena`, `health` jew `lifeTime`), vittma, qattiel, numru u isem tar-raġuni |
| `periods` | il-perjodi tal-battalja (stennija, prebattle, battle, afterbattle) bil-ħinijiet tat-tmiem tas-server |
| `basePoints` | il-progress tal-qbid tal-bażi għal kull tim u bażi |
| `chat`, `commands` | linji taċ-chat; kmandi taċ-chat tal-battalja bl-argumenti kollha tagħhom |
| `camera`, `clientEvents` | il-modalitajiet tal-kamera tal-plejer li rreġistra; dak li l-klijent irreġistra dwaru nnifsu (zoom, awto-aim, bidliet tal-mira, stat tal-vettura) |
| `arenaUpdates` | kull aġġornament tal-arena, deċifrat, kif bagħtu l-logħba |

## Riżultati u kontrolli {#results-and-checks}

| Ċavetta | X'inhi |
|---|---|
| `serverSettings` | is-settings tas-server mill-header |
| `results`, `resultVehicles`, `frags` | l-iskrin tar-riżultati: komuni, personali (b'dettalji għal kull mira), plejers, kontijiet; il-linja tar-riżultati ta' kull tank; qtil għal kull plejer |
| `entities` | kull entità li l-fluss joħloq: in-numru tat-tip u r-rwol, meta daħlet fil-vista tal-klijent u meta ħarġet |
| `selfCheck` | l-għadd tal-kompletezza ([Kompletezza](completeness.md)) u l-kontrolli tal-entitajiet u tal-verżjoni |

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
