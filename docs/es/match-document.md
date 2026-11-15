---
title: El documento de la partida
nav_order: 6
lang: es
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# El documento de la partida {#the-match-document}

`<partida>.match.json` contiene todo lo que dice la repetición y que no es una fila de la
tabla. La pestaña Partida del visor lo lee. (El código lo llama el resumen.)

![El inicio de un documento de la partida sintético, y sus claves](../assets/img/match-document.svg)

## La batalla {#the-battle}

| Clave | Qué es |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; el id de la batalla; el id del mapa y su nombre para mostrar |
| `clientVersion`, `streamVersion` | la versión del juego según la cabecera, y tal como la indica el flujo de paquetes |
| `recorded` | cuándo se grabó la repetición, tal como lo escribe el juego |
| `player`, `vehicle` | el jugador que graba y su tanque |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | el número de tipo de batalla de la cabecera, modo de juego, servidor, región, y si había mods instalados |
| `duration` | la duración de la batalla en segundos, según los resultados |
| `winnerTeam`, `finishReason` | el equipo ganador y el número del juego para cómo terminó la batalla, según los resultados |
| `complete`, `truncated` | los resultados están en la repetición; la grabación se detuvo antes |
| `battleStart`, `battleStartFrom`, `firstMovement` | el inicio de la batalla en segundos de la grabación; `arena` (lo indicó la arena) o `movement` (el primer instante en que se movió cualquier tanque); ese primer movimiento |
| `recordingSeconds` | la duración de la grabación en segundos |
| `positionPacket`, `hz`, `positions` | el número de paquete por el que llegaron las posiciones, muestras por segundo, filas de posición |
| `events` | el número de filas de la tabla de cada evento |
| `units` | `metres; x east, y up, z north` |
| `decoded` | el método y los números de paquete encontrados para cada tipo de mensaje |

## Jugadores y eventos {#players-and-events}

| Clave | Qué es |
|---|---|
| `players` | una entrada por tanque: nombre, equipo, tanque, clan, muestras, bajas, daño causado, sobrevivió, tiempo de vida; `seen` (los disparos y el daño que vio el cliente que graba); la entrada completa de la cabecera y de los resultados, y la de la cuenta |
| `kills` | cada muerte: hora (segundos), de dónde salió la hora (`arena`, `health` o `lifeTime`), víctima, asesino, número y nombre del motivo |
| `periods` | los periodos de la batalla (espera, previa, batalla, posterior) con las horas de fin del servidor |
| `basePoints` | progreso de captura de la base por equipo y base |
| `chat`, `commands` | líneas de chat; comandos del chat de batalla con todos sus argumentos |
| `camera`, `clientEvents` | los modos de cámara del jugador que graba; lo que el cliente registró de sí mismo (zoom, apuntado automático, cambios de objetivo, estado del vehículo) |
| `arenaUpdates` | cada actualización de la arena, decodificada, tal como la envió el juego |

## Resultados y comprobaciones {#results-and-checks}

| Clave | Qué es |
|---|---|
| `serverSettings` | los ajustes del servidor de la cabecera |
| `results`, `resultVehicles`, `frags` | la pantalla de resultados: común, personal (con los detalles por objetivo), jugadores, cuentas; la línea de resultados de cada tanque; bajas por jugador |
| `entities` | cada entidad que crea el flujo: su número de tipo y su papel, cuándo entró en la vista del cliente y cuándo salió |
| `selfCheck` | el recuento de completitud ([Completitud](completeness.md)) y las comprobaciones de las entidades y de la versión |

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
