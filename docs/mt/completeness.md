---
title: "Kompletezza"
nav_order: 8
lang: "mt"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Kompletezza {#completeness}

Xejn f'ripetizzjoni ma jintrema. Dak li l-konvertitur jaqra jmur fit-tabella u
fid-dokument tal-partita; kull element ieħor jinżamm sħiħ fis-sidecar
`<match>.messages.parquet`; u `selfCheck.completeness` tad-dokument tal-partita
jgħodd x'sar minn kull tip ta' element. Din hija r-regola li jaqsmu l-konvertituri
kollha tad-3DHeat:
[Il-konvertituri jżommu kollox](https://holdi601.github.io/3DHeat/converters.html).

![L-awto-kontroll ta' ripetizzjoni sintetika: kull element li deher, ġie moqri, miżmum jew mitluf](../assets/img/completeness.svg)

## L-għadd {#the-count}

Għal kull tip ta' element, `selfCheck.completeness.types` jagħti:

| Għadd | Tfisser |
|---|---|
| `seen` | kemm fiha r-ripetizzjoni |
| `decoded` | moqri sħiħ |
| `partial` | moqri parzjalment, u miżmum sħiħ fis-sidecar |
| `raw` | miżmum sħiħ biss fis-sidecar, mhux moqri |
| `lost` | mitluf: dejjem `0` |

It-tipi huma dawk tar-ripetizzjoni nnifisha: `block 0` (il-header), `block 1` (ir-riżultati),
`container sizes` u `deflate tail` (il-bytes tal-kontenitur nnifsu), `packet <type>`, u għal
sejħiet fuq entitajiet `method <entity type>.<number>` u `property <entity type>.<number>`.
It-tipi tal-entitajiet huma n-numri li jagħtu l-pakketti tal-ħolqien; `selfCheck.entities.roles`
jgħid liema huwa l-avatar tal-plejer li rreġistra u liema huma l-vetturi. Tip li ħadd ma kien jaf
bih jidher bl-għadd tiegħu.

## Is-sidecar {#the-sidecar}

| Kolonna | X'inhi |
|---|---|
| `time` | l-arloġġ tar-ripetizzjoni, bħal fit-tabella |
| `type`, `name` | it-tip ta' element; kif isejjaħlu l-konvertitur, fejn jaqrah |
| `entity` | il-vettura jew l-avatar li jappartjeni lilu, bħall-`entity` tat-tabella |
| `decoded` | dak li ntqara minnu, bħala JSON |
| `payload`, `text` | il-bytes tiegħu, sħaħ; il-blokok JSON, sħaħ |
| `entityType`, `packet`, `method` | in-numri |

Ir-ringieli huma ordnati skont pakkett, metodu, entità u ħin.

## X'jinqara, u kif ġie kkontrollat {#what-is-read-and-how-it-was-checked}

- **Pitch u roll** ta' kull pożizzjoni: il-pitch huwa l-inklinazzjoni, bis-sinjal
  maqlub, tal-mogħdija tat-tank stess waqt li jsuq 'il quddiem; żewġ tankijiet fl-istess
  post bl-istess direzzjoni għandhom l-istess roll, b'direzzjonijiet opposti rolls opposti.
- **Entitajiet** (`entities`): meta kull waħda daħlet fil-vista tal-klijent u ħarġet.
  Ebda tank m'għandu pożizzjoni bejn meta joħroġ u meta jerġa' jiġi.
- **Il-verżjoni fil-fluss** (`streamVersion`): l-istess bħal dik tal-header.
- **L-aim tal-plejer li rreġistra** (pakkett 38): direzzjoni, fid-`decoded` tas-sidecar
  (`forward`); fis-sparaturi tal-plejer hija frazzjoni ta' grad minn fejn tajjar il-qoxra.

Kull ħaġa oħra moqrija (saħħa, daqqiet, sparaturi, tracers, splużjonijiet, angoli tal-kanun,
aġġornamenti tal-arena, chat, modalitajiet tal-kamera, avvenimenti tal-klijent, pożizzjonijiet)
hija `partial`: fit-tabella jew fid-dokument tal-partita, u miżmuma sħiħa fis-sidecar.

**Miżmum imma mhux moqri** (`raw`), l-akbar tipi: aġġornamenti tal-pożizzjoni li mhumiex
fit-tabella (dawk tal-avatar, wara l-mewt ta' tank, entitajiet li mhumiex fir-roster),
pakketti 26, 28, 29, 31, 36, 50, 54 u 57, xi proprjetajiet frekwenti tal-vetturi u
tal-avatar, kull metodu u proprjetà mingħajr qarrej (fosthom ħsara fil-moduli, ekwipaġġ
u consumables), u l-proprjetajiet tal-ħolqien tal-entitajiet.

## Mhux disponibbli {#not-available}

- Dak li s-server qatt ma bagħat lill-klijent li rreġistra: l-aim, il-kamera u l-inputs
  ta' plejers oħra, l-għedewwa waqt li ma ġewx spotted. Ripetizzjoni hija dak li ntqal
  lil klijent wieħed.
- L-ismijiet tat-tipi tal-entitajiet, tal-metodi u tal-proprjetajiet: jinsabu fil-fajls
  tad-definizzjoni tal-logħba, mhux fir-ripetizzjoni. In-numri jinżammu.
- L-elevazzjoni tal-kanun f'gradi u kull ħaġa oħra li teħtieġ id-dejta tat-tankijiet stess
  mill-fajls tal-logħba.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
