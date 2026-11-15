---
title: Rungtynių dokumentas
nav_order: 6
lang: "lt"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Rungtynių dokumentas {#the-match-document}

`<match>.match.json` laiko viską, ką įrašas sako ir kas nėra lentelės eilutė. Žiūryklės Rungtynių skirtukas
skaito jį. (Kode jis vadinamas santrauka.)

![The start of a synthetic match document, and its keys](../assets/img/match-document.svg)

## Mūšis {#the-battle}

| Raktas | Ką reiškia |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; mūšio id; žemėlapio id ir jo rodomas pavadinimas |
| `clientVersion`, `streamVersion` | žaidimo versija iš antraštės ir kaip ją nurodo paketų srautas |
| `recorded` | kada įrašas buvo įrašytas, kaip jį rašo žaidimas |
| `player`, `vehicle` | įrašantis žaidėjas ir jo tankas |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | antraštės mūšio tipo numeris, žaidimo režimas, serveris, regionas ir ar buvo įdiegtų modifikacijų |
| `duration` | mūšio trukmė sekundėmis, iš rezultatų |
| `winnerTeam`, `finishReason` | laimėjusi komanda ir žaidimo numeris, kaip mūšis baigėsi, iš rezultatų |
| `complete`, `truncated` | rezultatai yra įraše; įrašymas sustojo anksti |
| `battleStart`, `battleStartFrom`, `firstMovement` | mūšio pradžia įrašo sekundėmis; `arena` (taip nurodė arena) arba `movement` (pirmoji akimirka, kai kuris nors tankas pajudėjo); ta pirmoji judėjimo akimirka |
| `recordingSeconds` | įrašo ilgis sekundėmis |
| `positionPacket`, `hz`, `positions` | paketo numeris, kuriame atėjo pozicijos, pavyzdžiai per sekundę, pozicijų eilutės |
| `events` | kiekvieno įvykio lentelės eilučių skaičius |
| `units` | `metres; x east, y up, z north` |
| `decoded` | metodo ir paketo numeriai, rasti kiekvienai pranešimų rūšiai |

## Žaidėjai ir įvykiai {#players-and-events}

| Raktas | Ką reiškia |
|---|---|
| `players` | vienas įrašas tankui: vardas, komanda, tankas, klanas, pavyzdžiai, nužudymai, padaryta žala, išgyventa, gyvavimo trukmė; `seen` (šūviai ir žala, kuriuos matė įrašantis klientas); visas antraštės ir rezultatų įrašas, ir paskyros įrašas |
| `kills` | kiekviena žūtis: laikas (sekundės), iš kur paimtas laikas (`arena`, `health` arba `lifeTime`), auka, žudikas, priežasties numeris ir vardas |
| `periods` | mūšio periodai (laukimas, prieš mūšį, mūšis, po mūšio) su serverio pabaigos laikais |
| `basePoints` | bazių užėmimo eiga kiekvienai komandai ir bazei |
| `chat`, `commands` | pokalbio eilutės; mūšio pokalbio komandos su visais jų argumentais |
| `camera`, `clientEvents` | įrašančio žaidėjo kameros režimai; ką klientas įrašė apie save (priartinimas, automatinis taikymas, taikinio pakeitimai, technikos būsena) |
| `arenaUpdates` | kiekvienas arenos atnaujinimas, iššifruotas, kaip jį siuntė žaidimas |

## Rezultatai ir patikrinimai {#results-and-checks}

| Raktas | Ką reiškia |
|---|---|
| `serverSettings` | serverio nustatymai iš antraštės |
| `results`, `resultVehicles`, `frags` | rezultatų ekranas: bendras, asmeninis (su kiekvieno taikinio detalėmis), žaidėjai, paskyros; kiekvienos technikos rezultatų eilutė; nužudymai pagal žaidėją |
| `entities` | kiekviena esybė, kurią sukuria srautas: jos tipo numeris ir vaidmuo, kada ji pateko į kliento matymo lauką ir kada išėjo |
| `selfCheck` | pilnumo skaičiai ([Pilnumas](completeness.md)) ir esybių bei versijos patikrinimai |

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
