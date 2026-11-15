---
title: "Dokument zápasu"
nav_order: 6
lang: "cs"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokument zápasu {#the-match-document}

`<match>.match.json` drží vše, co replay říká a co není řádkem tabulky. Čte ho záložka Zápas prohlížeče.
(Kód to nazývá souhrn.)

![Začátek syntetického dokumentu zápasu a jeho klíče](../assets/img/match-document.svg)

## Bitva {#the-battle}

| Klíč | Co |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; id bitvy; id mapy a její zobrazovaný název |
| `clientVersion`, `streamVersion` | verze hry z hlavičky a tak, jak ji říká proud paketů |
| `recorded` | kdy byl replay nahrán, tak jak to zapisuje hra |
| `player`, `vehicle` | hráč, který nahrával, a jeho tank |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | číslo typu bitvy z hlavičky, herní režim, server, region, a zda byly nainstalovány mody |
| `duration` | délka bitvy v sekundách, z výsledků |
| `winnerTeam`, `finishReason` | vítězný tým a číslo hry pro to, jak bitva skončila, z výsledků |
| `complete`, `truncated` | výsledky jsou v replayi; nahrávání skončilo předčasně |
| `battleStart`, `battleStartFrom`, `firstMovement` | začátek bitvy v sekundách nahrávky; `arena` (aréna to řekla) nebo `movement` (první okamžik, kdy se nějaký tank pohnul); ten první pohyb |
| `recordingSeconds` | délka nahrávky v sekundách |
| `positionPacket`, `hz`, `positions` | číslo paketu, ve kterém přišly pozice, vzorky za vteřinu, řádky pozic |
| `events` | počet řádků tabulky každé události |
| `units` | `metres; x east, y up, z north` |
| `decoded` | čísla metod a paketů nalezená pro každý druh zprávy |

## Hráči a události {#players-and-events}

| Klíč | Co |
|---|---|
| `players` | jeden záznam na tank: jméno, tým, tank, klan, vzorky, zabití, způsobené poškození, přežití, délka života; `seen` (výstřely a poškození, která viděl nahrávající klient); celý záznam z hlavičky a z výsledků, a účet |
| `kills` | každá smrt: čas (sekundy), odkud čas pochází (`arena`, `health` nebo `lifeTime`), oběť, zabiják, číslo a název důvodu |
| `periods` | periody bitvy (čekání, příprava, bitva, po bitvě) s časy konce podle serveru |
| `basePoints` | postup dobývání základny podle týmu a základny |
| `chat`, `commands` | řádky chatu; příkazy bitevního chatu se všemi jejich argumenty |
| `camera`, `clientEvents` | režimy kamery hráče, který nahrával; co klient nahrál sám o sobě (přiblížení, automatické míření, změny cíle, stav vozidla) |
| `arenaUpdates` | každá aktualizace arény, dekódovaná, tak, jak ji hra poslala |

## Výsledky a kontroly {#results-and-checks}

| Klíč | Co |
|---|---|
| `serverSettings` | nastavení serveru z hlavičky |
| `results`, `resultVehicles`, `frags` | obrazovka výsledků: společné, osobní (s podrobnostmi u každého cíle), hráči, účty; řádek výsledků každého tanku; zabití na hráče |
| `entities` | každá entita, kterou proud vytvoří: číslo typu a role, kdy vstoupila do zorného pole klienta a kdy z něj odešla |
| `selfCheck` | počet úplnosti ([Úplnost](completeness.md)) a kontroly entit a verze |

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
