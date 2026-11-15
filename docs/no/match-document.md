---
title: "Kampdokumentet"
nav_order: 6
lang: "no"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Kampdokumentet {#the-match-document}

`<kamp>.match.json` holder alt replayen sier som ikke er en rad i tabellen. Visningsprogrammets
fane Kamp leser den. (Koden kaller den oppsummeringen.)

![Starten på et syntetisk kampdokument, og dets nøkler](../assets/img/match-document.svg)

## Slaget {#the-battle}

| Nøkkel | Hva |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; slagets ID; kartets ID og dets visningsnavn |
| `clientVersion`, `streamVersion` | spillversjonen fra headeren, og slik pakkestrømmen sier den |
| `recorded` | når replayen ble tatt opp, slik spillet skriver det |
| `player`, `vehicle` | opptakspilotens spiller og hans stridsvogn |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | headerens slagtypenummer, spillmodus, server, region, og om modifikasjoner var installert |
| `duration` | slagets lengde i sekunder, fra resultatene |
| `winnerTeam`, `finishReason` | det vinnende laget og spillets nummer for hvordan slaget endte, fra resultatene |
| `complete`, `truncated` | resultatene er i replayen; opptaket stoppet tidlig |
| `battleStart`, `battleStartFrom`, `firstMovement` | slagets start i sekunder av opptaket; `arena` (arenaen sa det) eller `movement` (det første øyeblikket en stridsvogn beveget seg); den første bevegelsen |
| `recordingSeconds` | opptakets lengde i sekunder |
| `positionPacket`, `hz`, `positions` | pakkenummeret posisjonene kom i, samples i sekundet, posisjonsrader |
| `events` | antallet tabellrader for hver hendelse |
| `units` | `metres; x east, y up, z north` (meter; x øst, y opp, z nord) |
| `decoded` | metode- og pakkenumrene som ble funnet for hver type melding |

## Spillere og hendelser {#players-and-events}

| Nøkkel | Hva |
|---|---|
| `players` | én post per stridsvogn: navn, lag, stridsvogn, klan, samples, drap, gjort skade, overlevde, levetid; `seen` (skuddene og skaden opptaksklienten så); hele post fra headeren og resultatene, og kontoens |
| `kills` | hvert dødsfall: tid (sekunder), hvor tiden kom fra (`arena`, `health` eller `lifeTime`), offer, dreper, årsaksnummer og navn |
| `periods` | slagets perioder (venting, forslag, slag, etter slaget) med serverens sluttider |
| `basePoints` | fremdrift i basebeslag per lag og base |
| `chat`, `commands` | chat-linjer; kommandoer i slagchatten med alle deres argumenter |
| `camera`, `clientEvents` | opptakspilotens kameramodi; det klienten tok opp om seg selv (zoom, sikteassistanse, målbytter, kjøretøystatus) |
| `arenaUpdates` | hver arenaoppdatering, dekodet, slik spillet sendte den |

## Resultater og kontroller {#results-and-checks}

| Nøkkel | Hva |
|---|---|
| `serverSettings` | serverens innstillinger fra headeren |
| `results`, `resultVehicles`, `frags` | resultatskjermen: felles, personlig (med detaljer per mål), spillere, kontoer; hver stridsvogns resultatlinje; drap per spiller |
| `entities` | hver entitet strømmen oppretter: dens typenummer og rolle, når den kom inn i klientens syn og når den forlot det |
| `selfCheck` | fullstendighetstellingen ([Fullstendighet](completeness.md)) og kontrollene av entitetene og versjonen |

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
