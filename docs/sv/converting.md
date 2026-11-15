---
title: "Konvertera repriser"
nav_order: 4
lang: "sv"
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Konvertera repriser {#converting-replays}

## Steg för steg {#step-by-step}

1. **Slå på inspelning i spelet:** Inställningar > Allmänt > Spela in strider.
   Från och med då sparar spelet varje strid i mappen `replays` i din
   World of Tanks-installation, till exempel
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Öppna en terminal** i en mapp dit resultaten får skrivas
   ([Innan du börjar](before-you-start.md)).
3. **Kör konverteraren** på repriserfiler, eller på mappar som innehåller dem:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out` skapas i mappen din terminal står i.
4. **Läs vad den skriver.** Du bör se en rad per repris, som slutar med tabellen
   den skrev.
5. **Öppna resultatet** i 3DHeat-visaren: `out/<map>/<match>.parquet` på
   Värmekarta-fliken, `<match>.match.json` på Match-fliken. Eller läs dem med
   valfri Parquet- eller JSON-läsare.

![En körning på en syntetisk repris: konvertering, ny körning, en trasig fil, en tom mapp](../assets/img/convert.svg)

Bilden är en körning på en repris som testerna bygger i kod (ingen riktig repris):

- en repris konverterad: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- körd igen, hoppas matchen som redan skrivits över: `<file>: already written, <table>`;
- en fil som inte är en repris: `<file>: not converted: <why>` (på felutdata; exitstatus 1,
  de andra repriserna konverteras ändå);
- ingen repris hittad: `no .wotreplay files in <folders>` (exitstatus 2).

## Alternativ {#options}

| Alternativ | Standard | Gör |
|---|---|---|
| `replays` (en eller flera) | - | `.wotreplay`-filer, eller mappar som söks efter sådana (även undermappar) |
| `-o`, `--out` | krävs | mappen att skriva till: en mapp per karta inuti |
| `--force` | av | konvertera det som redan är skrivet igen |
| `--version` | - | skriv `heat3d-wot-replay <version>` och stanna |
| `-h`, `--help` | - | skriv alternativen och stanna |

Alternativen så som programmet skriver dem: [Kommandoreferens](../cli-reference.md).

## Vad som skrivs {#what-is-written}

Bara lösa filer: den här konverteraren skriver ingen `.3dheat`-fil (visaren kan
packa dem till en: [En fil per match](https://holdi601.github.io/3DHeat/container.html)).
Per repris, i `out/<map>/`:

| Fil | Vad |
|---|---|
| `<match>.parquet` | tabellen: varje stridsvagns position över tid och varje händelse där den skedde ([Tabellen](table.md)) |
| `<match>.match.json` | matchdokumentet: karta, klientversion, spelare, dödsfall, resultat och allt annat ([Matchdokumentet](match-document.md)) |
| `<match>.messages.parquet` | sidofilen: varje del av repriset som de två filerna ovan inte håller helt ([Fullständighet](completeness.md)) |

`<match>` är stridens eget id, eller filens namn när inspelningen stoppade före
resultaten.

## Exitstatus {#exit-status}

`0` när varje repris konverterades eller hoppades över, `1` när någon misslyckades (de
övriga konverteras ändå), `2` när ingen repris-fil hittades.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
