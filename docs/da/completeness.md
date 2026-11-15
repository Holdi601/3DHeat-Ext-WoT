---
title: Fuldstændighed
nav_order: 8
lang: "da"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Fuldstændighed {#completeness}

Intet i et replay bliver smidt væk. Det konverteren læser, går ind i tabellen og kampdokumentet;
hvert andet element gemmes helt i sidecaren `<match>.messages.parquet`; og kampdokumentets
`selfCheck.completeness` tæller, hvad der blev af hver slags element. Dette er reglen, alle
3DHeat-konvertere deler: [Konvertere bevarer alt](https://holdi601.github.io/3DHeat/converters.html).

![Selvkontrollen af et syntetisk replay: hvert element set, læst, gemt eller tabt](../assets/img/completeness.svg)

## Tællingen {#the-count}

For hver slags element giver `selfCheck.completeness.types`:

| Tælling | Betyder |
|---|---|
| `seen` | hvor mange replayet indeholder |
| `decoded` | læst helt |
| `partial` | læst delvist, og gemt helt i sidecaren |
| `raw` | kun gemt helt i sidecaren, ikke læst |
| `lost` | tabt: altid `0` |

Slagene er replayets egne: `block 0` (headeren), `block 1` (resultaterne), `container sizes` og
`deflate tail` (containerens egne bytes), `packet <type>`, og for kald på entiteter
`method <entity type>.<number>` og `property <entity type>.<number>`. Entitetstyperne er de tal,
oprettelsespakkerne giver; `selfCheck.entities.roles` siger, hvilken der er den optagende spillers avatar,
og hvilke der er køretøjerne. En slags, ingen kendte til, dukker op med sin tælling.

## Sidecaren {#the-sidecar}

| Kolonne | Hvad |
|---|---|
| `time` | replayets ur, som i tabellen |
| `type`, `name` | slags element; hvad konverteren kalder det, hvor den læser det |
| `entity` | køretøjet eller avataren, det hører til, som tabellens `entity` |
| `decoded` | det, der blev læst af det, som JSON |
| `payload`, `text` | dets bytes, helt; JSON-blokkene, helt |
| `entityType`, `packet`, `method` | tallene |

Rækkerne sorteres efter pakke, metode, entitet og tid.

## Hvad der læses, og hvordan det blev kontrolleret {#what-is-read-and-how-it-was-checked}

- **Hældning og rulning** for hver position: hældningen er minus hældningen af tankens egen vej,
  mens den kører frem; to tanke på samme sted med én heading har samme rulning, med modsatte
  headings modsatte rulninger.
- **Entiteter** (`entities`): hvornår hver kom ind i klientens udsyn, og hvornår den forlod det.
  Ingen tank har en position mellem at forlade og komme tilbage.
- **Versionen i strømmen** (`streamVersion`): den samme som headerens.
- **Den optagende spillers sigte** (pakke 38): en retning, i sidecarens `decoded` (`forward`); ved
  spillerens skud ligger den inden for en brøkdel af en grad fra, hvor granaten fløj.

Alt det øvrige, der læses (liv, træf, skud, sporstof, eksplosioner, kanonvinkler, arenaopdateringer,
chat, kameratilstande, klienthændelser, positioner), er `partial`: i tabellen eller kampdokumentet,
og gemt helt i sidecaren.

**Gemt, men ikke læst** (`raw`), de største slags: positionsopdateringer, der ikke er i tabellen
(avatarens, efter et tanks død, entiteter, der ikke står på listen), pakkerne 26, 28, 29, 31, 36, 50, 54
og 57, nogle hyppige køretøjs- og avataregenskaber, hver metode og egenskab uden en læser (blandt andet
modulskade, mandskab og forbrugsvarer), og egenskaberne ved entitetsoprettelser.

## Ikke tilgængeligt {#not-available}

- Det, serveren aldrig sendte til den optagende klient: andre spilleres sigte, kamera og input, fjender,
  mens de ikke er opdaget. Et replay er det, én klient blev fortalt.
- Navnene på entitetstyper, metoder og egenskaber: de står i spillets definitionsfiler, ikke i replayet.
  Tallene gemmes.
- Kanonens hævning i grader og alt andet, der kræver tankenes egne data fra spillets filer.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
