---
title: Pilnība
nav_order: 8
lang: "lv"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Pilnība {#completeness}

Neviens atkārtojuma saturs netiek izmests. Ko konvertētājs nolasa, nonāk tabulā un mača dokumentā; katrs cits vienums tiek paturēts pilnībā papildfailā `<match>.messages.parquet`; un mača dokumenta `selfCheck.completeness` skaita, kas notika ar katru vienuma veidu. Tas ir noteikums, ko ievēro visi 3DHeat konvertētāji: [Konvertētāji saglabā visu](https://holdi601.github.io/3DHeat/converters.html).

![Pašpārbaude sintētiskam atkārtojumam: katrs redzētais vienums, nolasīts, paturēts vai zaudēts](../assets/img/completeness.svg)

## Skaits {#the-count}

Katram vienuma veidam `selfCheck.completeness.types` dod:

| Skaits | Nozīmē |
|---|---|
| `seen` | cik to atkārtojumā ir |
| `decoded` | nolasīti pilnībā |
| `partial` | nolasīti daļēji un paturēti pilnībā papildfailā |
| `raw` | tikai paturēti pilnībā papildfailā, nav nolasīti |
| `lost` | zaudēti: vienmēr `0` |

Veidi ir paša atkārtojuma: `block 0` (galvene), `block 1` (rezultāti), `container sizes` un `deflate tail` (konteinera paša baiti), `packet <type>`, un izsaukumiem uz entītijām `method <entity type>.<number>` un `property <entity type>.<number>`. Entītiju tipi ir numuri, ko dod radošās paketes; `selfCheck.entities.roles` saka, kurš ir ieraksta spēlētāja avatārs un kurš — transportlīdzekļi. Veids, par kuru neviens nezināja, parādās ar savu skaitu.

## Papildfails {#the-sidecar}

| Kolonna | Ko tā nozīmē |
|---|---|
| `time` | atkārtojuma pulkstenis, kā tabulā |
| `type`, `name` | vienuma veids; ko konvertētājs to sauc un kur to nolasa |
| `entity` | transportlīdzeklis vai avatārs, kam tas pieder, kā tabulas `entity` |
| `decoded` | kas no tā nolasīts, kā JSON |
| `payload`, `text` | tā baiti, pilnībā; JSON bloki, pilnībā |
| `entityType`, `packet`, `method` | numuri |

Rindas tiek sakārtotas pēc paketes, metodes, entītijas un laika.

## Ko lasa un kā tas pārbaudīts {#what-is-read-and-how-it-was-checked}

- **Pitch un roll** katrai pozīcijai: pitch ir mīnus tanka pašas ceļa slīpums, kamēr tas brauc uz priekšu; divi tanki vienā vietā ar vienu virzienu ir ar vienādu roll, ar pretējiem virzieniem — pretēju roll.
- **Entītijas** (`entities`): kad katra ienāca klienta redzeslokā un aizgāja no tā. Neviens tanks nav pozīcijā starp aiziešanu un atgriešanos.
- **Versija straumē** (`streamVersion`): tā pati kā galvenē.
- **Ieraksta spēlētāja mērķis** (paketes 38): virziens, papildfailā `decoded` (`forward`); spēlētāja šāvienos tas ir daļa no grāda attālumā līdz vietai, kur šāviņš aizlidoja.

Viss pārējais, kas nolasīts (veselība, trāpījumi, šāvieni, trasieri, sprādzieni, lielgabala leņķi, arēnas atjauninājumi, tērzēšana, kameras režīmi, klienta notikumi, pozīcijas), ir `partial`: tabulā vai mača dokumentā, un paturēts pilnībā papildfailā.

**Paturēts, bet nav nolasīts** (`raw`), lielākie veidi: pozīciju atjauninājumi, kas nav tabulā (avatāra, pēc tanka nāves, entītijas, kas nav sarakstā), paketes 26, 28, 29, 31, 36, 50, 54 un 57, daži bieži transportlīdzekļu un avatāru lauki, katra metode un īpašība bez lasītāja (starp tām moduļu bojājumi, apkalpe un patēriņa priekšmeti), un entītiju izveides īpašības.

## Nav pieejams {#not-available}

- Tas, ko serveris nekad nenosūtīja ierakstošajam klientam: citu spēlētāju tēmēšana, kamera un ievades, ienaidnieki, kamēr tie nav pamanīti. Atkārtojums ir tas, ko viens klients tika pateicis.
- Entītiju tipu, metožu un īpašību nosaukumi: tie ir spēles definīciju failos, ne atkārtojumā. Numuri ir paturēti.
- Lielgabala pacēlums grādos un viss cits, kam vajadzīgi tanku paši dati no spēles failiem.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
