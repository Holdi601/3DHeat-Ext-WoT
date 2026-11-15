---
title: Dokument tekme
nav_order: 6
lang: sl
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokument tekme {#the-match-document}

`<match>.match.json` hrani vse, kar posnetek pove in ni vrstica tabele. Zavihek Tekma v pregledovalniku ga bere.
(Koda ga imenuje povzetek.)

![Začetek sintetičnega dokumenta tekme in njegovi ključi](../assets/img/match-document.svg)

## Bitka {#the-battle}

| Ključ | Kaj |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; identifikator bitke; identifikator zemljevida in njegovo prikazno ime |
| `clientVersion`, `streamVersion` | različica igre iz glave in kot jo pove paketni tok |
| `recorded` | kdaj je bil posnetek narejen, kot ga zapiše igra |
| `player`, `vehicle` | igralec, ki je snemal, in njegov tank |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | številka tipa bitke iz glave, način igre, strežnik, regija in ali so bile nameščene modifikacije |
| `duration` | dolžina bitke v sekundah, iz rezultatov |
| `winnerTeam`, `finishReason` | zmagovalna ekipa in igrina številka za to, kako se je bitka končala, iz rezultatov |
| `complete`, `truncated` | rezultati so v posnetku; snemanje se je ustavilo zgodaj |
| `battleStart`, `battleStartFrom`, `firstMovement` | začetek bitke v sekundah posnetka; `arena` (arena je to povedala) ali `movement` (prvi trenutek, ko se je kateri koli tank premaknil); ta prvi premik |
| `recordingSeconds` | dolžina posnetka v sekundah |
| `positionPacket`, `hz`, `positions` | številka paketa, v katerem so prišli položaji, vzorci na sekundo, vrstice položajev |
| `events` | število vrstic tabele za vsak dogodek |
| `units` | `metres; x east, y up, z north` |
| `decoded` | številke metod in paketov, najdene za vsako vrsto sporočila |

## Igralci in dogodki {#players-and-events}

| Ključ | Kaj |
|---|---|
| `players` | en vnos za tank: ime, ekipa, tank, klan, vzorci, ubijanja, nanesena škoda, preživel, čas življenja; `seen` (streli in škoda, ki jo je videl odjemalec, ki je snemal); celoten vnos iz glave in rezultatov ter račun |
| `kills` | vsaka smrt: čas (sekunde), od kod je prišel čas (`arena`, `health` ali `lifeTime`), žrtev, ubijalec, številka in ime razloga |
| `periods` | obdobja bitke (čakanje, predbitka, bitka, pobitka) s časi konca strežnika |
| `basePoints` | napredek zajema baze za vsako ekipo in bazo |
| `chat`, `commands` | vrstice klepeta; ukazi klepeta bojnega polja z vsemi argumenti |
| `camera`, `clientEvents` | načini kamere igralca, ki je snemal; kar je odjemalec zabeležil o sebi (zoom, samodejno ciljanje, spremembe cilja, stanje vozila) |
| `arenaUpdates` | vsaka posodobitev arene, dekodirana, kot jo je poslala igra |

## Rezultati in preverjanja {#results-and-checks}

| Ključ | Kaj |
|---|---|
| `serverSettings` | nastavitve strežnika iz glave |
| `results`, `resultVehicles`, `frags` | zaslon rezultatov: skupno, osebno (s podrobnostmi za vsako tarčo), igralci, računi; vrstica rezultatov vsakega tanka; ubijanja na igralca |
| `entities` | vsaka entiteta, ki jo ustvari tok: njena številka tipa in vloga, kdaj je prišla v pogled odjemalca in kdaj ga je zapustila |
| `selfCheck` | število popolnosti ([Popolnost](completeness.md)) in preverjanja entitet ter različice |

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
