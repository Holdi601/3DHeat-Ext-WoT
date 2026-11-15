---
title: "Het wedstrijddocument"
nav_order: 6
lang: "nl"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Het wedstrijddocument {#the-match-document}

`<match>.match.json` bevat alles wat de replay zegt dat geen rij van de tabel is. Het tabblad Match van de viewer leest het. (De code noemt het de samenvatting.)

![Het begin van een synthetisch wedstrijddocument, en zijn sleutels](../assets/img/match-document.svg)

## Het gevecht {#the-battle}

| Sleutel | Wat |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; het id van het gevecht; het id van de kaart en haar weergavenaam |
| `clientVersion`, `streamVersion` | de versie van het spel uit de kop, en zoals de pakketstroom die noemt |
| `recorded` | wanneer de replay is opgenomen, zoals het spel het schrijft |
| `player`, `vehicle` | de opnemende speler en zijn tank |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | het gevechtstypenummer uit de kop, de spelmodus, de server, de regio, en of er mods geïnstalleerd waren |
| `duration` | de lengte van het gevecht in seconden, uit de resultaten |
| `winnerTeam`, `finishReason` | het winnende team en het nummer van het spel voor hoe het gevecht eindigde, uit de resultaten |
| `complete`, `truncated` | de resultaten staan in de replay; de opname stopte vroeg |
| `battleStart`, `battleStartFrom`, `firstMovement` | het begin van het gevecht in seconden van de opname; `arena` (de arena zei het) of `movement` (het eerste moment dat een tank bewoog); dat eerste bewegen |
| `recordingSeconds` | de lengte van de opname in seconden |
| `positionPacket`, `hz`, `positions` | het pakketnummer waarin de posities kwamen, samples per seconde, positierijen |
| `events` | het aantal tabelrijen van elke gebeurtenis |
| `units` | `metres; x east, y up, z north` (meters; x oost, y omhoog, z noord) |
| `decoded` | de methode- en pakketnummers die gevonden zijn voor elke soort bericht |

## Spelers en gebeurtenissen {#players-and-events}

| Sleutel | Wat |
|---|---|
| `players` | één item per tank: naam, team, tank, clan, samples, kills, toegebrachte schade, overleefd, levensduur; `seen` (de schoten en schade die de opnemende client zag); het volledige item van de kop en van de resultaten, en dat van het account |
| `kills` | elke dood: tijd (seconden), waar de tijd vandaan kwam (`arena`, `health` of `lifeTime`), slachtoffer, killer, redennummer en -naam |
| `periods` | de periodes van het gevecht (wachten, voorbereiding, gevecht, na het gevecht) met de eindtijden van de server |
| `basePoints` | de voortgang van het veroveren van de basis per team en per basis |
| `chat`, `commands` | chatregels; commando's uit de gevechtschat met al hun argumenten |
| `camera`, `clientEvents` | de cameramodi van de opnemende speler; wat de client over zichzelf opnam (zoom, automatisch richten, wijzigingen van doel, toestand van het voertuig) |
| `arenaUpdates` | elke arena-update, gedecodeerd, zoals het spel hem stuurde |

## Resultaten en controles {#results-and-checks}

| Sleutel | Wat |
|---|---|
| `serverSettings` | de instellingen van de server uit de kop |
| `results`, `resultVehicles`, `frags` | het resultatenscherm: algemeen, persoonlijk (met details per doel), spelers, accounts; de resultaatregel van elke tank; kills per speler |
| `entities` | elke entiteit die de stroom aanmaakt: zijn typenummer en rol, wanneer hij in het zicht van de client kwam en wanneer hij weg was |
| `selfCheck` | de telling van volledigheid ([Volledigheid](completeness.md)) en de controles van de entiteiten en de versie |

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
