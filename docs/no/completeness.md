---
title: "Fullstendighet"
nav_order: 8
lang: "no"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Fullstendighet {#completeness}

Ingenting i en replay kastes. Det konverteren leser, går inn i tabellen og
kampdokumentet; alt annet beholdes helt i sidefilen
`<kamp>.messages.parquet`; og kampdokumentets
`selfCheck.completeness` teller hva som ble av hver type post. Dette er regelen alle
3DHeat-konvertere deler: [Konvertere beholder alt](https://holdi601.github.io/3DHeat/converters.html).

![Selvkontrollen til en syntetisk replay: hver post sett, lest, beholdt eller tapt](../assets/img/completeness.svg)

## Tellingen {#the-count}

For hver type post gir `selfCheck.completeness.types`:

| Telling | Betyr |
|---|---|
| `seen` | hvor mange replayen holder |
| `decoded` | lest helt |
| `partial` | lest delvis, og beholdt helt i sidefilen |
| `raw` | bare beholdt helt i sidefilen, ikke lest |
| `lost` | tapt: alltid `0` |

Typene er replayens egne: `block 0` (headeren), `block 1` (resultatene), `container sizes` og
`deflate tail` (containerens egne byte), `packet <type>`, og for kall på entiteter
`method <entitetstype>.<nummer>` og `property <entitetstype>.<nummer>`. Entitetstypene er
tallene de opprettende pakkene gir; `selfCheck.entities.roles` sier hvilken som er
opptakspilotens avatar og hvilke som er kjøretøyene. En type ingen kjente til, vises
med sin telling.

## Sidefilen {#the-sidecar}

| Kolonne | Hva |
|---|---|
| `time` | replayens klokke, som i tabellen |
| `type`, `name` | typen post; hva konverteren kaller den, der den leser den |
| `entity` | kjøretøyet eller avataren den hører til, som tabellens `entity` |
| `decoded` | det som ble lest av den, som JSON |
| `payload`, `text` | dens byte, helt; JSON-blokkene, helt |
| `entityType`, `packet`, `method` | tallene |

Rader sorteres etter pakke, metode, entitet og tid.

## Hva som leses, og hvordan det ble kontrollert {#what-is-read-and-how-it-was-checked}

- **Stigning og rull** for hver posisjon: stigningen er minus helningen på stridsvognens eget spor
  mens den kjører forover; to stridsvogner på samme sted med én retning har samme rull, med motsatte
  retninger motsatt rull.
- **Entiteter** (`entities`): når hver kom inn i klientens syn og forlot det. Ingen stridsvogn har
  en posisjon mellom at den forlot synet og at den kom tilbake.
- **Versjonen i strømmen** (`streamVersion`): den samme som headerens.
- **Opptakspilotens sikte** (pakke 38): en retning, i sidefilens `decoded` (`forward`); ved
  spillerens skudd er den en brøkdel av en grad fra der granaten fløy.

Alt annet som leses (helse, treff, skudd, sporstoffer, eksplosjoner, kanonvinkler,
arenaoppdateringer, chat, kameramodi, klienthendelser, posisjoner) er `partial`: i
tabellen eller kampdokumentet, og beholdt helt i sidefilen.

**Beholdt men ikke lest** (`raw`), de største typene: posisjonsoppdateringer som ikke er i
tabellen (avatarens, etter en stridsvogns død, entiteter som ikke er i listen), pakkene 26, 28, 29,
31, 36, 50, 54 og 57, noen hyppige egenskaper for kjøretøy og avatar, hver metode og egenskap
uten leser (blant dem skademodul, mannskap og forbruksvarer), og egenskapene til entitetsopprettelser.

## Ikke tilgjengelig {#not-available}

- Det serveren aldri sendte til opptaksklienten: andre spilleres sikte, kamera og
  inndata, fiender som ikke er sett. En replay er det én klient ble fortalt.
- Navnene på entitetstyper, metoder og egenskaper: de står i spillets definisjonsfiler, ikke i
  replayen. Tallene beholdes.
- Kanonens hevning i grader, og alt annet som krever tankenes egne data fra spillets filer.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
