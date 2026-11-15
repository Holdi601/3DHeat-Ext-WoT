---
title: "A meccsdokumentum"
nav_order: 6
lang: hu
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# A meccsdokumentum {#the-match-document}

A `<match>.match.json` mindent tartalmaz, amit a visszajátszás elmond, és ami nem a táblázat egy
sora. A nézegető Meccs fülje ezt olvassa. (A kód összefoglalónak nevezi.)

![Egy szintetikus meccsdokumentum eleje és kulcsai](../assets/img/match-document.svg)

## A csata {#the-battle}

| Kulcs | Mi |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; a csata azonosítója; a térkép azonosítója és megjelenő neve |
| `clientVersion`, `streamVersion` | a játék verziója a fejlécből, és ahogy a csomagfolyam megadja |
| `recorded` | mikor lett a visszajátszás rögzítve, ahogy a játék írja |
| `player`, `vehicle` | a felvevő játékos és a tankjuk |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | a fejléc csatatípus-száma, játékmód, szerver, régió, és hogy voltak-e telepített modok |
| `duration` | a csata hossza másodpercben, az eredményekből |
| `winnerTeam`, `finishReason` | a győztes csapat, és a játék száma arra, hogyan ért véget a csata, az eredményekből |
| `complete`, `truncated` | az eredmények benne vannak a visszajátszásban; a felvétel korán megállt |
| `battleStart`, `battleStartFrom`, `firstMovement` | a csata kezdete a felvétel másodperceiben; `arena` (az aréna ezt mondta) vagy `movement` (az első pillanat, amikor bármelyik tank mozgott); és ez az első mozgás |
| `recordingSeconds` | a felvétel hossza másodpercben |
| `positionPacket`, `hz`, `positions` | a csomagszám, amelyben a pozíciók érkeztek, minta másodpercenként, pozíciósorok |
| `events` | minden eseményfajta táblázatbeli sorainak száma |
| `units` | `metres; x east, y up, z north` (méterek; x kelet, y fel, z észak) |
| `decoded` | minden üzenetfajtához megtalált metódus- és csomagszámok |

## Játékosok és események {#players-and-events}

| Kulcs | Mi |
|---|---|
| `players` | egy bejegyzés tankonként: név, csapat, tank, klán, minták, ölések, okozott sebzés, túlélte-e, életidő; `seen` (amit a felvevő kliens látott a lövésekből és sebzésekből); a fejléc és az eredmények teljes bejegyzése, és a fiók |
| `kills` | minden halál: idő (másodperc), honnan jött az idő (`arena`, `health` vagy `lifeTime`), áldozat, gyilkos, az ok száma és neve |
| `periods` | a csata szakaszai (várakozás, előkészítés, csata, csata utáni) a szerver befejezési idejeivel |
| `basePoints` | bázis-elfoglalási állás csapatonként és bázisonként |
| `chat`, `commands` | chat-sorok; csatachat-parancsok minden argumentumukkal |
| `camera`, `clientEvents` | a felvevő játékos kameramódjai; amit a kliens saját magáról rögzített (nagyítás, automatikus célzás, célváltások, járműállapot) |
| `arenaUpdates` | minden aréna-frissítés, dekódolva, ahogy a játék küldte |

## Eredmények és ellenőrzések {#results-and-checks}

| Kulcs | Mi |
|---|---|
| `serverSettings` | a szerver beállításai a fejlécből |
| `results`, `resultVehicles`, `frags` | az eredménytábla: közös, személyes (célonkénti részletekkel), játékosok, fiókok; minden tank eredménysora; ölések játékosonként |
| `entities` | minden entitás, amelyet a folyam létrehoz: típusszáma és szerepe, mikor került a kliens látóterébe, és mikor távozott onnan |
| `selfCheck` | a teljességi számlálás ([Teljesség](completeness.md)), és az entitások és a verzió ellenőrzései |

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
