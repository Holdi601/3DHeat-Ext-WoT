---
title: Pilnumas
nav_order: 8
lang: lt
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Pilnumas {#completeness}

Niekas įraše neišmetama. Tai, ką konverteris perskaito, patenka į lentelę ir rungtynių dokumentą; kiekvienas
kitas elementas išsaugomas pilnai papildomame faile `<match>.messages.parquet`; o rungtynių dokumento
`selfCheck.completeness` suskaičiuoja, kas nutiko kiekvienos rūšies elementui. Tai taisyklė, kurios laikosi visi
3DHeat konverteriai: [Konverteriai išsaugo viską](https://holdi601.github.io/3DHeat/converters.html).

![The self-check of a synthetic replay: every item seen, read, kept or lost](../assets/img/completeness.svg)

## Skaičius {#the-count}

Kiekvienai elementų rūšiai `selfCheck.completeness.types` pateikia:

| Skaičius | Reiškia |
|---|---|
| `seen` | kiek jų yra įraše |
| `decoded` | perskaityta pilnai |
| `partial` | perskaityta iš dalies, o pilnai išsaugota papildomame faile |
| `raw` | tik pilnai išsaugota papildomame faile, neskaityta |
| `lost` | prarasta: visada `0` |

Rūšys yra paties įrašo: `block 0` (antraštė), `block 1` (rezultatai), `container sizes` ir `deflate tail`
(paties konteinerio baitai), `packet <type>`, o esybių iškvietimams - `method <entity type>.<number>` ir
`property <entity type>.<number>`. Esybių tipai yra skaičiai, kuriuos duoda kuriantys paketai;
`selfCheck.entities.roles` nurodo, kuris yra įrašančio žaidėjo avataras ir kurios yra technikos. Rūšis, apie
kurią niekas nežinojo, pasirodo su savo skaičiumi.

## Papildomas failas {#the-sidecar}

| Stulpelis | Ką reiškia |
|---|---|
| `time` | įrašo laikrodis, kaip lentelėje |
| `type`, `name` | elemento rūšis; kaip konverteris jį vadina ir kur jį skaito |
| `entity` | technika ar avataras, kuriam jis priklauso, kaip lentelės `entity` |
| `decoded` | kas buvo perskaityta, JSON formatu |
| `payload`, `text` | jo baitai, pilnai; JSON blokai, pilnai |
| `entityType`, `packet`, `method` | skaičiai |

Eilutės surūšiuotos pagal paketą, metodą, esybę ir laiką.

## Ką skaitome ir kaip tai patikrinta {#what-is-read-and-how-it-was-checked}

- **Kėlimas ir posūkis** kiekvienos pozicijos: kėlimas yra tanko paties kelio nuolydis su priešingu ženklu, kai jis
  važiuoja pirmyn; du tankai vienoje vietoje su viena kryptimi turi tokį patį posūkį, o su priešingomis kryptimis -
  priešingus posūkius.
- **Esybės** (`entities`): kada kiekviena pateko į kliento matymo lauką ir kada iš jo išėjo. Joks tankas nėra
  pozicijoje tarp išėjimo ir grįžimo.
- **Versija srautuose** (`streamVersion`): tokia pati kaip antraštės.
- **Įrašančio žaidėjo taikymas** (paketas 38): kryptis, `decoded` papildomame faile (`forward`); žaidėjo šūviuose
  ji nuo to, kur skrido sviedinys, nukrypsta per dalį laipsnio.

Viskas kita, kas perskaityta (sveikata, pataikymai, šūviai, trasuojantys sviediniai, sprogimai, patrankų kampai,
arenos atnaujinimai, pokalbis, kameros režimai, kliento įvykiai, pozicijos), yra `partial`: lentelėje arba
rungtynių dokumente, ir pilnai išsaugota papildomame faile.

**Išsaugota, bet neskaityta** (`raw`), didžiausios rūšys: pozicijų atnaujinimai, kurių nėra lentelėje (avataro,
po tanko žūties, esybės, kurių nėra sąraše), paketai 26, 28, 29, 31, 36, 50, 54 ir 57, kai kurios dažnai
kintančios technikos ir avataro savybės, kiekvienas metodas ir savybė be skaitytuvo (tarp jų modulių žala, įgula
ir sunaudojamos priemonės), ir esybių sukūrimų savybės.

## Nėra prieinama {#not-available}

- Tai, ko serveris niekada nesiuntė įrašančiam klientui: kitų žaidėjų taikymas, kamera ir įvestys, priešai, kol jie
  nepastebėti. Įrašas - tai tai, ką vienas klientas buvo pasakytas.
- Esybių tipų, metodų ir savybių vardai: jie yra žaidimo apibrėžimų failuose, o ne įraše. Skaičiai išsaugomi.
- Patrankos pakėlimas laipsniais ir viskas kita, kam reikia tankų paties duomenų iš žaidimo failų.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
