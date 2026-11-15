---
title: Vollständigkeit
nav_order: 8
lang: "de"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Vollständigkeit {#completeness}

Nichts aus einem Replay wird weggeworfen. Was der Umwandler liest, geht in die Tabelle
und das Match-Dokument; jeder andere Teil wird vollständig im Sidecar
`<match>.messages.parquet` aufbewahrt; und `selfCheck.completeness` im Match-Dokument
zählt, was aus jeder Art von Teil geworden ist. Das ist die Regel, die alle
3DHeat-Umwandler teilen:
[Umwandler behalten alles](https://holdi601.github.io/3DHeat/converters.html).

![Die Selbstprüfung eines synthetischen Replays: jeder Teil gesehen, gelesen, behalten oder verloren](../assets/img/completeness.svg)

## Die Zählung {#the-count}

Für jede Art von Teil gibt `selfCheck.completeness.types` an:

| Zählung | Bedeutung |
|---|---|
| `seen` | wie viele das Replay enthält |
| `decoded` | ganz gelesen |
| `partial` | teilweise gelesen, und vollständig im Sidecar aufbewahrt |
| `raw` | nur vollständig im Sidecar aufbewahrt, nicht gelesen |
| `lost` | verloren: immer `0` |

Die Arten sind die des Replays selbst: `block 0` (der Kopf), `block 1` (die
Ergebnisse), `container sizes` und `deflate tail` (die eigenen Bytes des Containers),
`packet <type>`, und für Aufrufe an Entitäten `method <entity type>.<number>` und
`property <entity type>.<number>`. Die Entitätstypen sind die Nummern, die die
erzeugenden Pakete angeben; `selfCheck.entities.roles` sagt, welcher der Avatar des
aufnehmenden Spielers ist und welche die Fahrzeuge. Eine Art, die niemand kannte,
erscheint mit ihrer Zählung.

## Der Sidecar {#the-sidecar}

| Spalte | Was |
|---|---|
| `time` | die Uhr des Replays, wie in der Tabelle |
| `type`, `name` | die Art des Teils; wie der Umwandler es nennt, wo er es liest |
| `entity` | das Fahrzeug oder der Avatar, zu dem es gehört, wie das `entity` der Tabelle |
| `decoded` | was davon gelesen wurde, als JSON |
| `payload`, `text` | seine Bytes, vollständig; die JSON-Blöcke, vollständig |
| `entityType`, `packet`, `method` | die Nummern |

Die Zeilen sind nach Paket, Methode, Entität und Zeit sortiert.

## Was gelesen wird, und wie es geprüft wurde {#what-is-read-and-how-it-was-checked}

- **Nicken und Rollen** jeder Position: Das Nicken ist das negative Gefälle des eigenen
  Weges des Panzers, während er vorwärts fährt; zwei Panzer an einer Stelle mit einem Kurs
  haben dieselbe Rolle, bei entgegengesetzten Kursen entgegengesetzte Rollen.
- **Entitäten** (`entities`): wann jede in die Sicht des Clients kam und sie verließ.
  Kein Panzer hat zwischen Verlassen und Wiederkommen eine Position.
- **Die Version im Strom** (`streamVersion`): dieselbe wie im Kopf.
- **Das Zielen des aufnehmenden Spielers** (Paket 38): eine Richtung, im `decoded` des
  Sidecars (`forward`); bei den Schüssen des Spielers liegt sie auf einen Bruchteil eines
  Grades genau dort, wohin die Granate flog.

Alles andere, was gelesen wird (Lebenspunkte, Treffer, Schüsse, Leuchtspur, Explosionen,
Geschützwinkel, Arena-Aktualisierungen, Chat, Kameramodi, Client-Ereignisse, Positionen),
ist `partial`: in der Tabelle oder im Match-Dokument, und vollständig im Sidecar aufbewahrt.

**Aufbewahrt, aber nicht gelesen** (`raw`), die größten Arten: Positionsaktualisierungen,
die nicht in der Tabelle stehen (die des Avatars, nach dem Tod eines Panzers, Entitäten,
die nicht in der Liste stehen), die Pakete 26, 28, 29, 31, 36, 50, 54 und 57, einige häufige
Eigenschaften von Fahrzeugen und Avataren, jede Methode und Eigenschaft ohne Leser (darunter
Modulschaden, Besatzung und Verbrauchsgüter) und die Eigenschaften der Entitätserzeugungen.

## Nicht verfügbar {#not-available}

- Was der Server dem aufnehmenden Client nie gesendet hat: das Zielen, die Kamera und
  Eingaben anderer Spieler, Gegner, solange sie nicht gesichtet sind. Ein Replay ist das,
  was einem Client mitgeteilt wurde.
- Die Namen der Entitätstypen, Methoden und Eigenschaften: Sie stehen in den
  Definitionsdateien des Spiels, nicht im Replay. Die Nummern werden aufbewahrt.
- Der Höhenwinkel des Geschützes in Grad und alles andere, was die eigenen Daten der Panzer
  aus den Dateien des Spiels braucht.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
