---
title: "Plotësia"
nav_order: 8
lang: sq
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Plotësia {#completeness}

Asgjë në një riluajtje nuk hidhet tutje. Çfarë lexon konvertuesi shkon në
tabelë dhe në dokumentin e ndeshjes; çdo element tjetër ruhet i plotë në skedarin anësor
`<match>.messages.parquet`; dhe `selfCheck.completeness` i dokumentit të ndeshjes
numëron çfarë u bë me çdo lloj elementi. Ky është rregulli që ndajnë të gjithë
konvertuesit e 3DHeat:
[Konvertuesit ruajnë gjithçka](https://holdi601.github.io/3DHeat/converters.html).

![Vetëkontrolli i një riluajtjeje sintetike: çdo element i parë, i lexuar, i ruajtur ose i humbur](../assets/img/completeness.svg)

## Numërimi {#the-count}

Për çdo lloj elementi, `selfCheck.completeness.types` jep:

| Numri | Do të thotë |
|---|---|
| `seen` | sa mban riluajtja |
| `decoded` | lexuar i plotë |
| `partial` | lexuar pjesërisht, dhe ruajtur i plotë në skedarin anësor |
| `raw` | vetëm ruajtur i plotë në skedarin anësor, jo i lexuar |
| `lost` | humbur: gjithmonë `0` |

Llojet janë të vetë riluajtjes: `block 0` (header-i), `block 1` (rezultatet),
`container sizes` dhe `deflate tail` (bajtët e vetë kontejnerit),
`packet <type>`, dhe për thirrjet mbi entitete `method <entity type>.<number>`
dhe `property <entity type>.<number>`. Llojet e entiteteve janë numrat që japin
paketat e krijimit; `selfCheck.entities.roles` thotë cili është avatari i
lojtarit që regjistron dhe cilat janë mjetet. Një lloj që askush nuk e njihte
shfaqet me numrin e vet.

## Skedari anësor {#the-sidecar}

| Kolona | Çfarë |
|---|---|
| `time` | ora e riluajtjes, si në tabelë |
| `type`, `name` | lloji i elementit; si e quan konvertuesi, aty ku e lexon |
| `entity` | mjeti ose avatari të cilit i përket, si `entity` i tabelës |
| `decoded` | çfarë u lexua prej tij, si JSON |
| `payload`, `text` | bajtët e tij, të plotë; blloqet JSON, të plota |
| `entityType`, `packet`, `method` | numrat |

Rreshtat renditen sipas paketës, metodës, entitetit dhe kohës.

## Çfarë lexohet, dhe si u kontrollua {#what-is-read-and-how-it-was-checked}

- **Pitch dhe roll** i çdo pozicioni: pitch është minus pjerrësia e shtegut të
  vetë tankut ndërsa vozit përpara; dy tanke në një vend me një heading kanë
  të njëjtin roll, me heading të kundërt roll të kundërt.
- **Entitetet** (`entities`): kur hyri secili në pamjen e klientit dhe kur doli.
  Asnjë tank nuk ka pozicion midis daljes dhe kthimit.
- **Versioni në rrjedhë** (`streamVersion`): i njëjti me atë të header-it.
- **Synimi i lojtarit që regjistron** (paketa 38): një drejtim, te `decoded`
  (`forward`) i skedarit anësor; te të shtënat e lojtarit është një pjesë e gradës
  larg nga ku fluturoi predha.

Çdo gjë tjetër e lexuar (shëndeti, goditjet, të shtënat, gjurmët e plumbave, shpërthimet, këndet e topit,
përditësimet e arenës, biseda, mënyrat e kamerës, ngjarjet e klientit, pozicionet) është `partial`:
në tabelë ose në dokumentin e ndeshjes, dhe e ruajtur e plotë në skedarin anësor.

**Të ruajtura por të palexuara** (`raw`), llojet më të mëdha: përditësimet e pozicionit që nuk janë në
tabelë (ato të avatarit, pas vdekjes së një tanku, entitetet jashtë listës),
paketat 26, 28, 29, 31, 36, 50, 54 dhe 57, disa veti të shpeshta mjetesh dhe avatari,
çdo metodë dhe veti pa lexues (mes tyre dëmtimi i moduleve, ekuipazhi
dhe konsumueshmet), dhe vetitë e krijimeve të entiteteve.

## Të padisponueshme {#not-available}

- Çfarë serveri nuk i dërgoi kurrë klientit që regjistron: synimi, kamera
  dhe hyrjet e lojtarëve të tjerë, armiqtë ndërsa nuk ishin të zbuluar. Një riluajtje është çfarë
  iu tha një klienti.
- Emrat e llojeve të entiteteve, metodave dhe vetive: janë në skedarët e
  përkufizimit të lojës, jo në riluajtje. Numrat ruhen.
- Ngritja e topit në gradë dhe çdo gjë tjetër që kërkon të dhënat e vetë tankeve
  nga skedarët e lojës.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
