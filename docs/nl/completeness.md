---
title: "Volledigheid"
nav_order: 8
lang: nl
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Volledigheid {#completeness}

Niets in een replay wordt weggegooid. Wat de converter leest, gaat in de tabel
en het wedstrijddocument; elk ander onderdeel wordt volledig bewaard in de sidecar
`<match>.messages.parquet`; en `selfCheck.completeness` van het wedstrijddocument telt wat er
van elke soort onderdeel geworden is. Dit is de regel die alle 3DHeat-converters delen:
[Converters bewaren alles](https://holdi601.github.io/3DHeat/converters.html).

![De zelfcontrole van een synthetische replay: elk onderdeel gezien, gelezen, bewaard of verloren](../assets/img/completeness.svg)

## De telling {#the-count}

Voor elke soort onderdeel geeft `selfCheck.completeness.types`:

| Telling | Betekent |
|---|---|
| `seen` | hoeveel de replay er bevat |
| `decoded` | volledig gelezen |
| `partial` | gedeeltelijk gelezen, en volledig bewaard in de sidecar |
| `raw` | alleen volledig bewaard in de sidecar, niet gelezen |
| `lost` | verloren: altijd `0` |

De soorten zijn die van de replay zelf: `block 0` (de kop), `block 1` (de
resultaten), `container sizes` en `deflate tail` (de eigen bytes van de container),
`packet <type>`, en voor aanroepen op entiteiten `method <entiteitstype>.<nummer>`
en `property <entiteitstype>.<nummer>`. Entiteitstypen zijn de nummers die de
aanmakende pakketten geven; `selfCheck.entities.roles` zegt welke de avatar van de
opnemende speler is en welke de voertuigen. Een soort die niemand kende, verschijnt
met zijn telling.

## De sidecar {#the-sidecar}

| Kolom | Wat |
|---|---|
| `time` | de klok van de replay, zoals in de tabel |
| `type`, `name` | de soort onderdeel; hoe de converter het noemt, waar hij het leest |
| `entity` | het voertuig of de avatar waar het bij hoort, als `entity` in de tabel |
| `decoded` | wat ervan gelezen is, als JSON |
| `payload`, `text` | de bytes, volledig; de JSON-blokken, volledig |
| `entityType`, `packet`, `method` | de nummers |

Rijen zijn gesorteerd op pakket, methode, entiteit en tijd.

## Wat er gelezen wordt, en hoe het gecontroleerd is {#what-is-read-and-how-it-was-checked}

- **Helling en rol** van elke positie: de helling is de min van de helling van het eigen pad van de tank
  terwijl hij vooruit rijdt; twee tanks op één plek met één heading hebben dezelfde rol, met tegengestelde
  headings tegengestelde rollen.
- **Entiteiten** (`entities`): wanneer elk in het zicht van de client kwam en wegging. Geen enkele tank
  heeft een positie tussen het weggaan en het terugkomen.
- **De versie in de stroom** (`streamVersion`): gelijk aan die van de kop.
- **Het doel van de opnemende speler** (pakket 38): een richting, in `decoded` van de sidecar
  (`forward`); bij de schoten van de speler ligt die op een fractie van een graad van waar het projectiel vloog.

Al het andere dat gelezen wordt (gezondheid, treffers, schoten, tracers, explosies, kanonshoeken,
arena-updates, chat, cameramodi, clientgebeurtenissen, posities) is `partial`: in de tabel
of het wedstrijddocument, en volledig bewaard in de sidecar.

**Bewaard maar niet gelezen** (`raw`), de grootste soorten: positie-updates die niet in de
tabel staan (die van de avatar, na de dood van een tank, entiteiten die niet in de lijst staan),
pakketten 26, 28, 29, 31, 36, 50, 54 en 57, enkele vaak voorkomende eigenschappen van voertuigen en avatars,
elke methode en eigenschap zonder lezer (schademodules, bemanning en verbruiksgoederen daaronder),
en de eigenschappen van entiteitscreaties.

## Niet beschikbaar {#not-available}

- Wat de server de opnemende client nooit stuurde: de richting, camera en besturing van andere spelers,
  vijanden zolang ze niet gespot waren. Een replay is wat één client te horen kreeg.
- De namen van entiteitstypen, methoden en eigenschappen: die staan in de definitiebestanden van het spel,
  niet in de replay. De nummers worden bewaard.
- De hoogte van het kanon in graden en alles andere dat de eigen gegevens van de tanks uit de
  bestanden van het spel nodig heeft.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
