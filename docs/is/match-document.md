---
title: "Leikjaskjalið"
nav_order: 6
lang: is
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Leikjaskjalið {#the-match-document}

`<match>.match.json` geymir allt sem upptakan segir og er ekki röð í
töflunni. Flipinn Leikur í skoðaranum les það. (Kóðinn kallar það samantektina.)

![Upphaf tilbúins leikjaskjals og lyklar þess](../assets/img/match-document.svg)

## Bardaginn {#the-battle}

| Lykill | Hvað |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; auðkenni bardagans; auðkenni kortsins og birtingarnafn þess |
| `clientVersion`, `streamVersion` | leikjaútgáfan úr hausnum, og eins og pakkastraumurinn segir hana |
| `recorded` | hvenær upptakan var tekin, eins og leikurinn skrifar það |
| `player`, `vehicle` | upptökumaðurinn og skriðdreki hans |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | bardagategundarnúmer hausins, leikjahamur, þjónn, svæði, og hvort viðbætur (mods) voru uppsettar |
| `duration` | lengd bardagans í sekúndum, úr niðurstöðunum |
| `winnerTeam`, `finishReason` | sigurliðið og númer leiksins fyrir hvernig bardaginn endaði, úr niðurstöðunum |
| `complete`, `truncated` | niðurstöðurnar eru í upptökunni; upptakan stöðvaðist snemma |
| `battleStart`, `battleStartFrom`, `firstMovement` | upphaf bardagans í sekúndum upptökunnar; `arena` (völlurinn sagði það) eða `movement` (fyrsta stund sem einhver skriðdreki hreyfðist); sú fyrsta hreyfing |
| `recordingSeconds` | lengd upptökunnar í sekúndum |
| `positionPacket`, `hz`, `positions` | pakkanúmerið sem stöðurnar komu í, sýni á sekúndu, stöðuraðir |
| `events` | fjöldi taflaraða af hverjum atburði |
| `units` | `metres; x east, y up, z north` |
| `decoded` | aðferðar- og pakkanúmerin sem fundust fyrir hverja tegund skilaboða |

## Spilarar og atburðir {#players-and-events}

| Lykill | Hvað |
|---|---|
| `players` | ein færsla fyrir hvern skriðdreka: nafn, lið, skriðdreki, ætt (clan), sýni, dráp, skaði veittur, lifði af, lífstími; `seen` (skotin og skaðinn sem upptökubiðlarinn sá); öll færsla hausins og niðurstaðnanna, og reikningsins |
| `kills` | hvert dauðsfall: tími (sekúndur), hvaðan tíminn kom (`arena`, `health` eða `lifeTime`), fórnarlamb, drápsmaður, ástæðunúmer og nafn |
| `periods` | tímabil bardagans (bið, fyrir bardaga, bardagi, eftir bardaga) með lokatímum þjónsins |
| `basePoints` | framvinda handtöku bækistöðva á lið og bækistöð |
| `chat`, `commands` | spjalllínur; skipanir bardagaspjalls með öllum röksemdum sínum |
| `camera`, `clientEvents` | myndavélarhamir upptökumannsins; það sem biðlarinn skráði um sjálfan sig (aðdráttur, sjálfvirk miðun, breytingar á skotmarki, ástand farartækis) |
| `arenaUpdates` | hver uppfærsla vallar, afkóðuð, eins og leikurinn sendi hana |

## Niðurstöður og athuganir {#results-and-checks}

| Lykill | Hvað |
|---|---|
| `serverSettings` | stillingar þjónsins úr hausnum |
| `results`, `resultVehicles`, `frags` | niðurstöðuskjárinn: almennt, persónulegt (með smáatriðum á skotmark), spilarar, reikningar; niðurstöðulína hvers skriðdreka; dráp á spilara |
| `entities` | hver eining sem straumurinn býr til: tegundarnúmer hennar og hlutverk, hvenær hún kom inn í sjónsvið biðlarans og hvenær hún fór úr því |
| `selfCheck` | heilleikatalningin ([Heilleiki](completeness.md)) og athuganir á einingum og útgáfunni |

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
