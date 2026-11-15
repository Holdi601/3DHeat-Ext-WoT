---
title: "Potpunost"
nav_order: 8
lang: "bs"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Potpunost {#completeness}

Ništa iz replaya se ne baca. Ono što konverter pročita ide u
tabelu i dokument meča; svaka druga stavka čuva se cijela u sidecar datoteci
`<match>.messages.parquet`; a `selfCheck.completeness` dokumenta meča
broji šta se desilo sa svakom vrstom stavke. To je pravilo koje dijele svi
3DHeat konverteri:
[Konverteri čuvaju sve](https://holdi601.github.io/3DHeat/converters.html).

![Samoprovjera sintetičkog replaya: svaka stavka viđena, pročitana, sačuvana ili izgubljena](../assets/img/completeness.svg)

## Broj {#the-count}

Za svaku vrstu stavke, `selfCheck.completeness.types` daje:

| Broj | Znači |
|---|---|
| `seen` | koliko ih replay sadrži |
| `decoded` | pročitano cijelo |
| `partial` | pročitano djelimično i sačuvano cijelo u sidecar datoteci |
| `raw` | samo sačuvano cijelo u sidecar datoteci, nije pročitano |
| `lost` | izgubljeno: uvijek `0` |

Vrste su vlastite vrste replaya: `block 0` (zaglavlje), `block 1` (rezultati),
`container sizes` i `deflate tail` (vlastiti bajtovi kontejnera),
`packet <type>`, a za pozive na entitetima `method <entity type>.<number>`
i `property <entity type>.<number>`. Tipovi entiteta su brojevi koje daju
paketi stvaranja; `selfCheck.entities.roles` kaže koji je avatar
igrača koji snima, a koji su vozila. Vrsta za koju niko nije znao
pojavi se sa svojim brojem.

## Sidecar {#the-sidecar}

| Kolona | Šta |
|---|---|
| `time` | sat replaya, kao u tabeli |
| `type`, `name` | vrsta stavke; kako je konverter naziva, gdje je čita |
| `entity` | vozilo ili avatar kojem pripada, kao `entity` tabele |
| `decoded` | šta je od nje pročitano, kao JSON |
| `payload`, `text` | njeni bajtovi, cijeli; JSON blokovi, cijeli |
| `entityType`, `packet`, `method` | brojevi |

Redovi su sortirani po paketu, metodi, entitetu i vremenu.

## Šta se čita i kako je provjereno {#what-is-read-and-how-it-was-checked}

- **Pitch i roll** svake pozicije: pitch je minus nagib vlastite
  putanje tenka dok vozi naprijed; dva tenka na istom mjestu s istim
  headingom imaju isti roll, a sa suprotnim headingom suprotne rollove.
- **Entiteti** (`entities`): kada je svaki ušao u vidokrug klijenta i izašao.
  Nijedan tenk nema poziciju između izlaska i povratka.
- **Verzija u toku** (`streamVersion`): ista kao ona iz zaglavlja.
- **Nišanjenje igrača koji snima** (paket 38): smjer, u `decoded` sidecar datoteke
  (`forward`); pri hicima igrača razlikuje se za djelić stepena
  od onoga kuda je granata letjela.

Sve ostalo pročitano (zdravlje, pogoci, hici, trasirke, eksplozije, uglovi topa,
ažuriranja arene, čet, načini kamere, događaji klijenta, pozicije) je `partial`:
u tabeli ili dokumentu meča, i sačuvano cijelo u sidecar datoteci.

**Sačuvano ali nepročitano** (`raw`), najveće vrste: ažuriranja pozicija koja nisu u
tabeli (avatarova, poslije smrti tenka, entiteti koji nisu na spisku),
paketi 26, 28, 29, 31, 36, 50, 54 i 57, neka česta svojstva vozila i avatara,
svaka metoda i svojstvo bez čitača (među njima oštećenje modula, posada
i potrošni materijal), te svojstva stvaranja entiteta.

## Nije dostupno {#not-available}

- Ono što server nikad nije poslao klijentu koji snima: nišanjenje, kamera
  i unosi drugih igrača, neprijatelji dok su neotkriveni. Replay je ono što je
  rečeno jednom klijentu.
- Imena tipova entiteta, metoda i svojstava: nalaze se u definicijskim
  datotekama igre, a ne u replayu. Brojevi se čuvaju.
- Elevacija topa u stepenima i sve ostalo što traži vlastite podatke tenkova
  iz datoteka igre.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
