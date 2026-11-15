---
title: Įrašų konvertavimas
nav_order: 4
lang: lt
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Įrašų konvertavimas {#converting-replays}

## Žingsnis po žingsnio {#step-by-step}

1. **Įjunkite įrašymą žaidime:** Nustatymai > Bendra > Įrašyti mūšius. Nuo tada žaidimas
   išsaugo kiekvieną mūšį World of Tanks diegimo aplanke `replays`, pavyzdžiui
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Atidarykite terminalą** aplanke, kuriame gali būti įrašomi rezultatai
   ([Prieš pradedant](before-you-start.md)).
3. **Paleiskite konverterį** su įrašų failais arba su aplankais, kuriuose jie yra:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out` sukuriamas aplanke, kuriame yra jūsų terminalas.
4. **Perskaitykite, ką jis praneša.** Turėtumėte matyti po vieną eilutę kiekvienam įrašui, ir ji
   baigiasi lentele, kurią jis įrašė.
5. **Atidarykite rezultatą** 3DHeat žiūryklėje: `out/<map>/<match>.parquet` Šilumos žemėlapio skirtuke,
   `<match>.match.json` Rungtynių skirtuke. Arba skaitykite juos bet kuriuo Parquet ar JSON skaitytuvu.

![A run on a synthetic replay: converting, running again, a broken file, an empty folder](../assets/img/convert.svg)

Paveikslėlis - tai paleidimas su sintetiniu įrašu, kurį testai sukuria kode (jokio tikro įrašo):

- įrašas konvertuotas: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- paleidus dar kartą, jau įrašytas mūšis praleidžiamas: `<file>: already written, <table>`;
- failas, kuris nėra įrašas: `<file>: not converted: <why>` (klaidų išvestyje; išėjimo statusas 1, kiti
  įrašai vis tiek konvertuojami);
- įrašo nerasta: `no .wotreplay files in <folders>` (išėjimo statusas 2).

## Parametrai {#options}

| Parametras | Numatytasis | Ką daro |
|---|---|---|
| `replays` (vienas ar daugiau) | - | `.wotreplay` failai arba aplankai, kuriuose jų ieškoma (ir poaplankiuose) |
| `-o`, `--out` | privalomas | aplankas, į kurį rašyti: viduje - aplankas kiekvienam žemėlapiui |
| `--force` | išjungtas | konvertuoti iš naujo tai, kas jau įrašyta |
| `--version` | - | išvesti `heat3d-wot-replay <version>` ir sustoti |
| `-h`, `--help` | - | išvesti parametrus ir sustoti |

Parametrai taip, kaip juos rodo programa: [Komandų nuoroda](../cli-reference.md).

## Kas įrašoma {#what-is-written}

Tik atskiri failai: šis konverteris `.3dheat` failo nerašo (žiūryklė gali juos supakuoti į vieną:
[Vienas failas rungtynėms](https://holdi601.github.io/3DHeat/container.html)). Kiekvienam įrašui į
`out/<map>/`:

| Failas | Ką jis yra |
|---|---|
| `<match>.parquet` | lentelė: kiekvieno tanko pozicija laikui bėgant ir kiekvienas įvykis, kur jis įvyko ([Lentelė](table.md)) |
| `<match>.match.json` | rungtynių dokumentas: žemėlapis, kliento versija, žaidėjai, nužudymai, rezultatai ir viskas kita ([Rungtynių dokumentas](match-document.md)) |
| `<match>.messages.parquet` | papildomas failas: kiekvienas įrašo elementas, kurio du aukščiau nurodyti failai nelaiko pilnai ([Pilnumas](completeness.md)) |

`<match>` yra paties mūšio id arba failo vardas, kai įrašymas sustojo prieš rezultatus.

## Išėjimo statusas {#exit-status}

`0`, kai kiekvienas įrašas konvertuotas arba praleistas, `1`, kai kuris nepavyko (kiti vis tiek konvertuojami),
`2`, kai nerasta jokio įrašo failo.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
