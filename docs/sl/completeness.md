---
title: Popolnost
nav_order: 8
lang: "sl"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Popolnost {#completeness}

Nič v posnetku se ne zavrže. Kar pretvornik prebere, gre v tabelo in dokument tekme; vsak drug del
se ohrani celo v spremljevalni datoteki `<match>.messages.parquet`; `selfCheck.completeness` v dokumentu
tekme šteje, kaj se je zgodilo z vsako vrsto dela. To je pravilo, ki ga delijo vsi pretvorniki 3DHeat:
[Pretvorniki ohranijo vse](https://holdi601.github.io/3DHeat/converters.html).

![Samopreverjanje sintetičnega posnetka: vsak del viden, prebran, ohranjen ali izgubljen](../assets/img/completeness.svg)

## Števila {#the-count}

Za vsako vrsto dela `selfCheck.completeness.types` navaja:

| Število | Pomeni |
|---|---|
| `seen` | koliko jih posnetek vsebuje |
| `decoded` | prebrano celo |
| `partial` | prebrano delno in ohranjeno celo v spremljevalni datoteki |
| `raw` | samo ohranjeno celo v spremljevalni datoteki, ni prebrano |
| `lost` | izgubljeno: vedno `0` |

Vrste so posnetkove lastne: `block 0` (glava), `block 1` (rezultati), `container sizes` in `deflate tail`
(lastni bajti vsebnika), `packet <type>`, za klice na entitetah pa `method <entity type>.<number>` in
`property <entity type>.<number>`. Tipi entitet so številke, ki jih dajo paketi ustvarjanja;
`selfCheck.entities.roles` pove, kateri je avatar igralca, ki je snemal, in kateri so vozila. Vrsta, ki je ni nihče poznal, se pokaže s svojim številom.

## Spremljevalna datoteka {#the-sidecar}

| Stolpec | Kaj |
|---|---|
| `time` | ura posnetka, kot v tabeli |
| `type`, `name` | vrsta dela; kako ga pretvornik imenuje, kjer ga bere |
| `entity` | vozilo ali avatar, kateremu pripada, kot `entity` v tabeli |
| `decoded` | kar je bilo prebrano iz njega, kot JSON |
| `payload`, `text` | njegovi bajti, celi; bloki JSON, celi |
| `entityType`, `packet`, `method` | številke |

Vrstice so razvrščene po paketu, metodi, entiteti in času.

## Kaj se bere in kako je bilo preverjeno {#what-is-read-and-how-it-was-checked}

- **Naklon in zvitek** vsake pozicije: naklon je minus naklon lastne poti tanka, medtem ko vozi naprej; dva
  tanka na istem mestu z eno smerjo imata isti zvitek, z nasprotnima smerema pa nasprotna zvitka.
- **Entitete** (`entities`): kdaj je vsaka prišla v pogled odjemalca in kdaj ga je zapustila. Noben tank
  nima položaja med odhodom in vrnitvijo.
- **Različica v toku** (`streamVersion`): enaka kot v glavi.
- **Cilj igralca, ki je snemal** (paket 38): smer, v spremljevalni datoteki v `decoded` (`forward`); pri
  strelih igralca je delček stopinje od tistega, kamor je letel izstrelek.

Vse drugo, kar je prebrano (zdravje, zadetki, streli, sledi, eksplozije, koti topa, posodobitve arene,
klepet, načini kamere, dogodki odjemalca, položaji), je `partial`: v tabeli ali dokumentu tekme in celo v
spremljevalni datoteki.

**Ohranjeno, a ni prebrano** (`raw`), največje vrste: posodobitve položajev, ki niso v tabeli (avatarjeve,
po smrti tanka, entitete, ki niso v seznamu), paketi 26, 28, 29, 31, 36, 50, 54 in 57, nekatere pogoste
lastnosti vozil in avatarjev, vsaka metoda in lastnost brez bralnika (med njimi poškodbe modulov, posadka
in potrošni material), ter lastnosti ustvarjanja entitet.

## Ni na voljo {#not-available}

- Kar strežnik nikoli ni poslal odjemalcu, ki je snemal: cilji drugih igralcev, kamera in vnosi, sovražniki,
  dokler niso opaženi. Posnetek je tisto, kar je bil povedan en odjemalec.
- Imena tipov entitet, metod in lastnosti: so v datotekah definicij igre, ne v posnetku. Števila se hranijo.
- Kot topa v stopinjah in vse drugo, kar potrebuje podatke tankov iz datotek igre.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
