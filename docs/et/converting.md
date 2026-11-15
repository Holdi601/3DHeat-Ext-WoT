---
title: Kordustete konverteerimine
nav_order: 4
lang: "et"
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Kordustete konverteerimine {#converting-replays}

## Samm-sammult {#step-by-step}

1. **Lülita salvestamine mängus sisse:** Settings > General > Record battles (Seaded > Üldine > Salvesta lahingud).
   Sellest hetkest salvestab mäng iga lahingu World of Tanksi installatsiooni kausta `replays`, näiteks
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Ava terminal** kaustas, kuhu tulemusi tohib kirjutada ([Enne alustamist](before-you-start.md)).
3. **Käivita konverter** kordusfailidel või kaustadel, kus need on:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out` luuakse terminali kaustas.
4. **Loe, mida see ütleb.** Peaksid nägema ühte rida iga kordus kohta, mis lõpeb tabeliga, mille see kirjutas.
5. **Ava tulemus** 3DHeat vaaturis: `out/<map>/<match>.parquet` vahekaardil **Soojuskaart**,
   `<match>.match.json` vahekaardil **Matš**. Või loe neid mis tahes Parquet- või JSON-lugejaga.

![Käivitus sünteetilise kordusega: konverteerimine, uuesti käivitamine, katkine fail, tühi kaust](../assets/img/convert.svg)

Pilt on käivitus kordusel, mille testid koostavad koodis (päris kordust ei ole):

- kordus konverteeritud: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- uuesti käivitatud, juba kirjutatud lahing jäetakse vahele: `<file>: already written, <table>`;
- fail, mis ei ole kordus: `<file>: not converted: <why>` (veateates; väljumisolek 1, ülejäänud kordused
  konverteeritakse siiski);
- kordust ei leitud: `no .wotreplay files in <folders>` (väljumisolek 2).

## Valikud {#options}

| Valik | Vaikimisi | Mida teeb |
|---|---|---|
| `replays` (üks või mitu) | - | `.wotreplay` failid või kaustad, mida neid otsitakse (ka alamkaustad) |
| `-o`, `--out` | nõutav | kaust, kuhu kirjutada: kaust iga kaardi kohta sees |
| `--force` | väljas | konverteeri uuesti see, mis on juba kirjutatud |
| `--version` | - | prindi `heat3d-wot-replay <version>` ja lõpeta |
| `-h`, `--help` | - | prindi valikud ja lõpeta |

Valikud nii, nagu programm need prindib: [Käskude viide](../cli-reference.md).

## Mis kirjutatakse {#what-is-written}

Ainult lahtised failid: see konverter ei kirjuta `.3dheat` faili (vaaturi saab need pakkida ühte:
[Üks fail mängu kohta](https://holdi601.github.io/3DHeat/container.html)). Iga kordus kohta kausta `out/<map>/`:

| Fail | Mis see on |
|---|---|
| `<match>.parquet` | tabel: iga tanki asukoht ajas ja iga sündmus seal, kus see juhtus ([Tabel](table.md)) |
| `<match>.match.json` | mängu dokument: kaart, kliendi versioon, mängijad, tapmised, tulemused ja kõik muu ([Mängu dokument](match-document.md)) |
| `<match>.messages.parquet` | lisafail: iga korduse üksus, mida kaks ülaltoodud faili ei hoia tervena ([Täielikkus](completeness.md)) |

`<match>` on lahingu enda ID või faili nimi, kui salvestus katkes enne tulemusi.

## Väljumisolek {#exit-status}

`0`, kui iga kordus konverteeriti või jäeti vahele, `1`, kui mõni ebaõnnestus (ülejäänud konverteeritakse siiski),
`2`, kui kordusfaili ei leitud.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
