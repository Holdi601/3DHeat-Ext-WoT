---
title: Potpunost
nav_order: 8
lang: hr
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Potpunost {#completeness}

Ništa iz snimke se ne baca. Što pretvarač čita ide u tablicu i dokument meča; svaka druga stavka
čuva se cijela u pomoćnoj datoteci `<match>.messages.parquet`; a `selfCheck.completeness` dokumenta
meča broji što se dogodilo sa svakom vrstom stavke. Ovo je pravilo koje dijele svi pretvarači
3DHeata: [Pretvarači zadržavaju sve](https://holdi601.github.io/3DHeat/converters.html).

![Samoprovjera sintetičke snimke: svaka stavka viđena, pročitana, sačuvana ili izgubljena](../assets/img/completeness.svg)

## Brojanje {#the-count}

Za svaku vrstu stavke, `selfCheck.completeness.types` daje:

| Brojač | Znači |
|---|---|
| `seen` | koliko ih snimka sadrži |
| `decoded` | pročitano cijelo |
| `partial` | pročitano djelomično, i sačuvano cijelo u pomoćnoj datoteci |
| `raw` | samo sačuvano cijelo u pomoćnoj datoteci, nije pročitano |
| `lost` | izgubljeno: uvijek `0` |

Vrste su snimkine vlastite: `block 0` (zaglavlje), `block 1` (rezultati), `container sizes` i
`deflate tail` (vlastiti bajtovi kontejnera), `packet <type>`, a za pozive nad entitetima
`method <entity type>.<number>` i `property <entity type>.<number>`. Vrste entiteta su brojevi koje
daju pakete stvaranja; `selfCheck.entities.roles` kaže koji je avatar igrača koji snima, a koji
vozila. Vrsta koju nitko nije poznavao pojavi se sa svojim brojem.

## Pomoćna datoteka {#the-sidecar}

| Stupac | Što |
|---|---|
| `time` | sat snimke, kao u tablici |
| `type`, `name` | vrsta stavke; što je pretvarač zove, gdje je čita |
| `entity` | vozilo ili avatar kojem pripada, kao `entity` u tablici |
| `decoded` | što se od nje pročitalo, kao JSON |
| `payload`, `text` | njezini bajtovi, cijeli; JSON blokovi, cijeli |
| `entityType`, `packet`, `method` | brojevi |

Reci su poredane po paketu, metodi, entitetu i vremenu.

## Što se čita, i kako je provjereno {#what-is-read-and-how-it-was-checked}

- **Nagib i valjanje** svakog položaja: nagib je minus nagib vlastite putanje tenka dok vozi naprijed;
  dva tenka na jednom mjestu s jednim smjerom imaju isto valjanje, a s suprotnim smjerovima suprotno valjanje.
- **Entiteti** (`entities`): kad je svaki ušao u pogled klijenta i kad je izašao. Nijedan tenk nema
  položaj između odlaska i povratka.
- **Verzija u toku** (`streamVersion`): ista kao u zaglavlju.
- **Nišan igrača koji snima** (paket 38): smjer, u `decoded` pomoćne datoteke (`forward`); pri hicima
  igrača to je djelić stupnja od smjera kojim je granata letjela.

Sve ostalo što je pročitano (zdravlje, pogoci, hici, tragovi, eksplozije, kutovi topa, ažuriranja
arene, razgovor, načini kamere, događaji klijenta, položaji) je `partial`: u tablici ili dokumentu
meča, i cijelo sačuvano u pomoćnoj datoteci.

**Sačuvano, ali nepročitano** (`raw`), najveće vrste: ažuriranja položaja koja nisu u tablici (avatarova,
nakon smrti tenka, entiteti koji nisu u popisu), paketi 26, 28, 29, 31, 36, 50, 54 i 57, neka česta
svojstva vozila i avatara, svaka metoda i svojstvo bez čitača (oštećenja modula, posada i potrošni
predmeti među njima), i svojstva stvaranja entiteta.

## Nije dostupno {#not-available}

- Što poslužitelj nikad nije poslao klijentu koji snima: nišan, kamera i upravljanje drugih igrača,
  neprijatelji dok nisu uočeni. Snimka je ono što je jedan klijent dobio.
- Nazivi vrsta entiteta, metoda i svojstava: oni su u definicijskim datotekama igre, ne u snimci.
  Brojevi su sačuvani.
- Kut elevacije topa u stupnjevima i sve što treba vlastite podatke tenkova iz datoteka igre.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
