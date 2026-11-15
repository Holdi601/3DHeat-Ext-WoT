---
title: "Dokument zápasu"
nav_order: 6
lang: "sk"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokument zápasu {#the-match-document}

`<match>.match.json` drží všetko, čo replay hovorí a nie je riadkom tabuľky. Karta Zápas v prehliadači ho číta.
(Kód ho volá súhrn.)

![Začiatok syntetického dokumentu zápasu a jeho kľúče](../assets/img/match-document.svg)

## Bitka {#the-battle}

| Kľúč | Čo |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; id bitky; id mapy a jej zobrazovaný názov |
| `clientVersion`, `streamVersion` | verzia hry z hlavičky a tak, ako ju hovorí tok paketov |
| `recorded` | kedy bol replay nahraný, tak, ako ho hra zapisuje |
| `player`, `vehicle` | hráč, ktorý replay nahral, a jeho tank |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | číslo typu bitky z hlavičky, herný režim, server, región a či boli nainštalované modifikácie |
| `duration` | dĺžka bitky v sekundách, z výsledkov |
| `winnerTeam`, `finishReason` | víťazný tím a číslo hry pre to, ako sa bitka skončila, z výsledkov |
| `complete`, `truncated` | výsledky sú v replayi; nahrávanie sa skončilo predčasne |
| `battleStart`, `battleStartFrom`, `firstMovement` | začiatok bitky v sekundách nahrávania; `arena` (arena to povedala) alebo `movement` (prvý okamih, keď sa niektorý tank pohol); tento prvý pohyb |
| `recordingSeconds` | dĺžka nahrávania v sekundách |
| `positionPacket`, `hz`, `positions` | číslo paketu, v ktorom prišli polohy, vzorky za sekundu, riadky polôh |
| `events` | počet riadkov tabuľky každej udalosti |
| `units` | `metres; x east, y up, z north` (metre; x na východ, y nahor, z na sever) |
| `decoded` | metóda a čísla paketov nájdené pre každý druh správy |

## Hráči a udalosti {#players-and-events}

| Kľúč | Čo |
|---|---|
| `players` | jeden záznam na tank: meno, tím, tank, klan, vzorky, zabitia, spôsobené poškodenie, prežitie, dĺžka života; `seen` (výstrely a poškodenia, ktoré videl klient, ktorý replay nahral); celý záznam z hlavičky a z výsledkov, a účet |
| `kills` | každá smrť: čas (sekundy), odkiaľ čas pochádza (`arena`, `health` alebo `lifeTime`), obeť, vrah, číslo a názov dôvodu |
| `periods` | periódy bitky (čakanie, prebitka, bitka, po bitke) s časmi konca od servera |
| `basePoints` | postup dobývania základne na tím a základňu |
| `chat`, `commands` | riadky chatu; príkazy bojového chatu so všetkými ich argumentmi |
| `camera`, `clientEvents` | režimy kamery hráča, ktorý replay nahral; čo klient zaznamenal o sebe (priblíženie, automatické mierenie, zmeny cieľa, stav vozidla) |
| `arenaUpdates` | každá aktualizácia arény, dekódovaná, tak, ako ju hra poslala |

## Výsledky a kontroly {#results-and-checks}

| Kľúč | Čo |
|---|---|
| `serverSettings` | nastavenia servera z hlavičky |
| `results`, `resultVehicles`, `frags` | obrazovka výsledkov: spoločné, osobné (s podrobnosťami na cieľ), hráči, účty; riadok výsledkov každého tanku; zabitia na hráča |
| `entities` | každá entita, ktorú tok vytvorí: jej číslo typu a úloha, kedy sa dostala do pohľadu klienta a kedy z neho odišla |
| `selfCheck` | počet úplnosti ([Úplnosť](completeness.md)) a kontroly entít a verzie |

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
