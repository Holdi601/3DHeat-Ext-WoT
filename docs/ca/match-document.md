---
title: El document de partida
nav_order: 6
lang: ca
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# El document de partida {#the-match-document}

`<partida>.match.json` guarda tot el que diu la repetició que no és una fila de la taula. La pestanya Partida
del visualitzador el llegeix. (El codi l'anomena el resum.)

![L'inici d'un document de partida sintètic, i les seves claus](../assets/img/match-document.svg)

## La batalla {#the-battle}

| Clau | Què és |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; l'identificador de la batalla; l'identificador del mapa i el seu nom per mostrar |
| `clientVersion`, `streamVersion` | la versió del joc de la capçalera, i tal com l'indica el flux de paquets |
| `recorded` | quan es va gravar la repetició, tal com ho escriu el joc |
| `player`, `vehicle` | el jugador que grava i el seu tanc |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | el número de tipus de batalla de la capçalera, el mode de joc, el servidor, la regió, i si hi havia mods instal·lats |
| `duration` | la durada de la batalla en segons, dels resultats |
| `winnerTeam`, `finishReason` | l'equip guanyador i el número del joc per com va acabar la batalla, dels resultats |
| `complete`, `truncated` | els resultats són a la repetició; la gravació es va aturar abans |
| `battleStart`, `battleStartFrom`, `firstMovement` | l'inici de la batalla en segons de la gravació; `arena` (l'arena ho va dir) o `movement` (el primer moment en què es va moure un tanc); aquell primer moviment |
| `recordingSeconds` | la durada de la gravació en segons |
| `positionPacket`, `hz`, `positions` | el número de paquet en què van arribar les posicions, mostres per segon, files de posició |
| `events` | el nombre de files de la taula de cada esdeveniment |
| `units` | `metres; x est, y amunt, z nord` |
| `decoded` | el mètode i els números de paquet trobats per a cada tipus de missatge |

## Jugadors i esdeveniments {#players-and-events}

| Clau | Què és |
|---|---|
| `players` | una entrada per tanc: nom, equip, tanc, clan, mostres, morts, dany fet, supervivència, temps de vida; `seen` (els trets i el dany que va veure el client que gravava); l'entrada completa de la capçalera i dels resultats, i la del compte |
| `kills` | cada mort: hora (segons), d'on ve l'hora (`arena`, `health` o `lifeTime`), víctima, assassí, número i nom de la raó |
| `periods` | els períodes de la batalla (espera, prebatalla, batalla, després de la batalla) amb les hores de final del servidor |
| `basePoints` | el progrés de captura de bases per equip i base |
| `chat`, `commands` | les línies de xat; les ordres de xat de batalla amb tots els seus arguments |
| `camera`, `clientEvents` | els modes de càmera del jugador que grava; el que el client va gravar de si mateix (zoom, punteria automàtica, canvis d'objectiu, estat del vehicle) |
| `arenaUpdates` | cada actualització de l'arena, desxifrada, tal com la va enviar el joc |

## Resultats i comprovacions {#results-and-checks}

| Clau | Què és |
|---|---|
| `serverSettings` | la configuració del servidor de la capçalera |
| `results`, `resultVehicles`, `frags` | la pantalla de resultats: comú, personal (amb els detalls per objectiu), jugadors, comptes; la línia de resultats de cada tanc; morts per jugador |
| `entities` | cada entitat que crea el flux: el seu número de tipus i el seu rol, quan va entrar a la vista del client i quan en va sortir |
| `selfCheck` | el recompte de completesa ([Completesa](completeness.md)) i les comprovacions de les entitats i de la versió |

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
