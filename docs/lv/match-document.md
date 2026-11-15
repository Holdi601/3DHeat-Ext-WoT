---
title: Mača dokuments
nav_order: 6
lang: lv
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Mača dokuments {#the-match-document}

`<match>.match.json` satur visu, ko atkārtojums saka un kas nav tabulas rinda. Skatītāja Mača cilne to nolasa. (Kods to sauc par kopsavilkumu.)

![Sintētiska mača dokumenta sākums un tā atslēgas](../assets/img/match-document.svg)

## Kauja {#the-battle}

| Atslēga | Ko tā nozīmē |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; kaujas ID; kartes ID un tās parādāmais nosaukums |
| `clientVersion`, `streamVersion` | spēles versija no galvenes un kā to saka paketes straume |
| `recorded` | kad atkārtojums ierakstīts, kā to raksta spēle |
| `player`, `vehicle` | ierakstošais spēlētājs un viņa tanks |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | galvenes kaujas tipa numurs, spēles režīms, serveris, reģions un vai bija uzstādītas modifikācijas |
| `duration` | kaujas garums sekundēs, no rezultātiem |
| `winnerTeam`, `finishReason` | uzvarējusī komanda un spēles numurs tam, kā kauja beidzās, no rezultātiem |
| `complete`, `truncated` | rezultāti ir atkārtojumā; ieraksts apstājās agri |
| `battleStart`, `battleStartFrom`, `firstMovement` | kaujas sākums sekundēs no ieraksta; `arena` (arēna to teica) vai `movement` (pirmais brīdis, kad jebkurš tanks kustējās); šī pirmā kustība |
| `recordingSeconds` | ieraksta garums sekundēs |
| `positionPacket`, `hz`, `positions` | paketes numurs, kurā nāca pozīcijas; paraugi sekundē; pozīciju rindas |
| `events` | katra notikuma tabulas rindu skaits |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metodes un paketes numuri, kas atrasti katram ziņojuma veidam |

## Spēlētāji un notikumi {#players-and-events}

| Atslēga | Ko tā nozīmē |
|---|---|
| `players` | viens ieraksts katram tankam: vārds, komanda, tanks, klans, paraugi, nogalinājumi, nodarītie bojājumi, izdzīvoja, dzīves ilgums; `seen` (šāvieni un bojājumi, ko ierakstošais klients redzēja); galvenes un rezultātu pilnais ieraksts, un konta ieraksts |
| `kills` | katra nāve: laiks (sekundes), no kurienes nāca laiks (`arena`, `health` vai `lifeTime`), upuris, slepkava, iemesla numurs un nosaukums |
| `periods` | kaujas periodi (gaidīšana, pirmskaujas, kauja, pēckaujas) ar servera beigu laikiem |
| `basePoints` | bāzes iekarošanas progress katrai komandai un bāzei |
| `chat`, `commands` | tērzēšanas rindas; kaujas tērzēšanas komandas ar visiem to argumentiem |
| `camera`, `clientEvents` | ierakstošā spēlētāja kameras režīmi; ko klients ierakstīja par sevi (tuvināšana, automātiskā mērķēšana, mērķa maiņas, transportlīdzekļa stāvoklis) |
| `arenaUpdates` | katrs arēnas atjauninājums, atšifrēts, kā spēle to nosūtīja |

## Rezultāti un pārbaudes {#results-and-checks}

| Atslēga | Ko tā nozīmē |
|---|---|
| `serverSettings` | servera iestatījumi no galvenes |
| `results`, `resultVehicles`, `frags` | rezultātu ekrāns: kopīgais, personīgais (ar detaļām pa mērķiem), spēlētāji, konti; katra tanka rezultātu rinda; nogalinājumi pa spēlētājiem |
| `entities` | katra entītija, ko straume izveido: tās tipa numurs un loma, kad tā ieiet klienta redzeslokā un kad aizgāja |
| `selfCheck` | pilnības skaits ([Pilnība](completeness.md)) un entītiju, versijas pārbaudes |

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
