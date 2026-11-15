---
title: Documentul meciului
nav_order: 6
lang: ro
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
`<match>.match.json` ține tot ce spune replay-ul și care nu este un rând al tabelului. Fila Meci a
vizualizatorului îl citește. (Codul îl numește rezumat.)

![Începutul unui document de meci sintetic și cheile sale](../assets/img/match-document.svg)

## Bătălia

| Cheie | Ce este |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; id-ul bătăliei; id-ul hărții și numele său afișat |
| `clientVersion`, `streamVersion` | versiunea jocului din antet, și cum o spune fluxul de pachete |
| `recorded` | când a fost înregistrat replay-ul, așa cum îl scrie jocul |
| `player`, `vehicle` | jucătorul care înregistrează și tancul său |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | numărul tipului de bătălie din antet, modul de joc, serverul, regiunea și dacă erau instalate modificări |
| `duration` | lungimea bătăliei în secunde, din rezultate |
| `winnerTeam`, `finishReason` | echipa câștigătoare și numărul jocului pentru cum s-a încheiat bătălia, din rezultate |
| `complete`, `truncated` | rezultatele sunt în replay; înregistrarea s-a oprit devreme |
| `battleStart`, `battleStartFrom`, `firstMovement` | începutul bătăliei în secunde ale înregistrării; `arena` (arena a spus-o) sau `movement` (primul moment în care s-a mișcat vreun tanc); acea primă mișcare |
| `recordingSeconds` | lungimea înregistrării în secunde |
| `positionPacket`, `hz`, `positions` | numărul pachetului în care au venit pozițiile, eșantioane pe secundă, rândurile de poziție |
| `events` | numărul de rânduri din tabel pentru fiecare eveniment |
| `units` | `metres; x east, y up, z north` (metri; x est, y sus, z nord) |
| `decoded` | numărul metodei și al pachetelor găsite pentru fiecare fel de mesaj |

## Jucători și evenimente

| Cheie | Ce este |
|---|---|
| `players` | o intrare pe tanc: nume, echipă, tanc, clan, eșantioane, ucideri, daune date, supraviețuit, durata vieții; `seen` (loviturile și daunele pe care le-a văzut clientul care înregistrează); toată intrarea din antet și din rezultate, și contul |
| `kills` | fiecare moarte: ora (secunde), de unde a venit ora (`arena`, `health` sau `lifeTime`), victima, ucigașul, numărul și numele motivului |
| `periods` | perioadele bătăliei (așteptare, pregătire, bătălie, după bătălie) cu orele de sfârșit ale serverului |
| `basePoints` | progresul capturării bazei pe echipă și bază |
| `chat`, `commands` | liniile de chat; comenzile de chat din bătălie cu toate argumentele lor |
| `camera`, `clientEvents` | modurile camerei jucătorului care înregistrează; ce a înregistrat clientul despre sine (zoom, ținta automată, schimbările de țintă, starea vehiculului) |
| `arenaUpdates` | fiecare actualizare a arenei, decodată, așa cum a trimis-o jocul |

## Rezultate și verificări

| Cheie | Ce este |
|---|---|
| `serverSettings` | setările serverului din antet |
| `results`, `resultVehicles`, `frags` | ecranul rezultatelor: comun, personal (cu detaliile pe țintă), jucători, conturi; rândul rezultatelor fiecărui tanc; uciderile pe jucător |
| `entities` | fiecare entitate pe care o creează fluxul: numărul tipului său și rolul, când a intrat în vederea clientului și când a ieșit |
| `selfCheck` | numărătoarea de completitudine ([Completitudinea](completeness.md)) și verificările entităților și ale versiunii |

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
