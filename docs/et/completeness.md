---
title: Täielikkus
nav_order: 8
lang: et
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Täielikkus {#completeness}

Kordusest ei visata midagi ära. See, mida konverter loeb, läheb tabelisse ja mängu dokumenti; kõik muu hoitakse
tervena lisafailis `<match>.messages.parquet`, ja mängu dokumendi `selfCheck.completeness` loeb, mis sai igast
liigist. See on reegel, mida jagavad kõik 3DHeati konverterid:
[Konverterid hoiavad kõike](https://holdi601.github.io/3DHeat/converters.html).

![Synteetilise kordase enesekontroll: iga üksus nähtud, loetud, alles hoitud või kadunud](../assets/img/completeness.svg)

## Loendus {#the-count}

Iga liigi kohta annab `selfCheck.completeness.types`:

| Loend | Tähendab |
|---|---|
| `seen` | mitu seda kordus sisaldab |
| `decoded` | loetud tervena |
| `partial` | loetud osaliselt ja hoitud lisafailis tervena |
| `raw` | ainult lisafailis tervena hoitud, mitte loetud |
| `lost` | kadunud: alati `0` |

Liigid on kordusest endast: `block 0` (päis), `block 1` (tulemused), `container sizes` ja `deflate tail`
(konteineri enda baidid), `packet <type>`, ning olemite kutsete puhul `method <entity type>.<number>` ja
`property <entity type>.<number>`. Olemi tüübid on numbrid, mille loovad paketid annavad;
`selfCheck.entities.roles` ütleb, milline on salvestajamängija avatar ja milline sõidukid. Liik, mida keegi ei
tundnud, ilmub oma loendusega.

## Lisafail {#the-sidecar}

| Veerg | Mis see on |
|---|---|
| `time` | korduse kell, nagu tabelis |
| `type`, `name` | üksuse liik; mida konverter selle nimetab, kus ta seda loeb |
| `entity` | sõiduk või avatar, kuhu see kuulub, nagu tabeli `entity` |
| `decoded` | mis sellest loeti, JSON-ina |
| `payload`, `text` | tema baidid tervena; JSON-plokid tervena |
| `entityType`, `packet`, `method` | numbrid |

Read on sorteeritud paketi, meetodi, olemi ja aja järgi.

## Mida loetakse ja kuidas kontrolliti {#what-is-read-and-how-it-was-checked}

- **Tõus ja rull** igal asukohal: tõus on miinus tanki enda sõidutee kalle, kui ta sõidab edasi; kaks tanki samas
  kohas ühe suunaga on sama rulliga, vastupidise suunaga vastupidise rulliga.
- **Olemid** (`entities`): millal kumbki tuli kliendi vaatevälja ja lahkus sealt. Ühelgi tankil ei ole asukohta
  lahkumise ja tagasituleku vahel.
- **Voo versioon** (`streamVersion`): sama, mis päises.
- **Salvestajamängija siht** (pakett 38): suund, lisafaili `decoded`-is (`forward`); mängija laskudel on see
  kraadi murdosa täpsusega sealt, kust mürsk lendas.

Kõik muu loetu (tervis, tabamused, lasud, jäljed, plahvatused, püssi nurgad, areeni uuendused, vestlus, kaamera
režiimid, kliendi sündmused, asukohad) on `partial`: tabelis või mängu dokumendis ning lisafailis tervena.

**Hoitud, aga mitte loetud** (`raw`), suurimad liigid: asukohauuendused, mida tabelis ei ole (avatari oma, pärast
tanki surma, olemid, mida nimekirjas ei ole), paketid 26, 28, 29, 31, 36, 50, 54 ja 57, mõned sagedased sõiduki ja
avatari omadused, iga meetod ja omadus ilma lugejata (mooduli kahjustus, meeskond ja kulumaterjalid nende hulgas)
ning olemite loomise omadused.

## Pole saadaval {#not-available}

- Mida server ei saatnud kunagi salvestavale kliendile: teiste mängijate siht, kaamera ja sisendid, vaenlased,
  kui neid pole avastatud. Kordus on see, mida üks klient sai teada.
- Olemi tüüpide, meetodite ja omaduste nimed: need on mängu definitsioonifailides, mitte kordusses. Numbrid on alles.
- Püssi tõus kraadides ja kõik muu, mis vajab tankide enda andmeid mängu failidest.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
