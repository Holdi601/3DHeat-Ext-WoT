---
title: "Fullständighet"
nav_order: 8
lang: sv
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Fullständighet {#completeness}

Ingenting i en repris kastas bort. Det konverteraren läser går in i tabellen och
matchdokumentet; varje annat objekt behålls helt i sidofilen
`<match>.messages.parquet`; och matchdokumentets `selfCheck.completeness` räknar vad
som blev av varje slag av objekt. Det här är regeln alla 3DHeat-konverterare delar:
[Konverterare behåller allt](https://holdi601.github.io/3DHeat/converters.html).

![Självkontrollen för en syntetisk repris: varje objekt sett, läst, behållet eller förlorat](../assets/img/completeness.svg)

## Räkningen {#the-count}

För varje slag av objekt ger `selfCheck.completeness.types`:

| Räkning | Betyder |
|---|---|
| `seen` | hur många repriset innehåller |
| `decoded` | lästa helt |
| `partial` | lästa delvis, och behållna helt i sidofilen |
| `raw` | bara behållna helt i sidofilen, inte lästa |
| `lost` | förlorade: alltid `0` |

Slagen är repriset egna: `block 0` (headern), `block 1` (resultaten), `container sizes` och
`deflate tail` (containerns egna byte), `packet <type>`, och för anrop på entiteter
`method <entity type>.<number>` och `property <entity type>.<number>`. Entitetstyper är de
nummer som skapandepaketen anger; `selfCheck.entities.roles` säger vilken som är den
inspelande spelarens avatar och vilka som är fordonen. Ett slag som ingen kände till
syns med sin räkning.

## Sidofilen {#the-sidecar}

| Kolumn | Vad |
|---|---|
| `time` | repriets klocka, som i tabellen |
| `type`, `name` | slaget av objekt; vad konverteraren kallar det, där den läser det |
| `entity` | fordonet eller avataren det hör till, som tabellens `entity` |
| `decoded` | vad som lästes av det, som JSON |
| `payload`, `text` | dess byte, helt; JSON-blocken, helt |
| `entityType`, `packet`, `method` | talen |

Rader sorteras efter paket, metod, entitet och tid.

## Vad som lästes, och hur det kontrollerades {#what-is-read-and-how-it-was-checked}

- **Stigning och rulle** för varje position: stigningen är minus lutningen på stridsvagnens
  egen väg medan den kör framåt; två stridsvagnar på samma plats med en kurs har samma rulle,
  med motsatta kurser motsatta rullar.
- **Entiteter** (`entities`): när var och en kom in i klientens syn och lämnade den.
  Ingen stridsvagn har en position mellan att lämna och komma tillbaka.
- **Versionen i strömmen** (`streamVersion`): samma som headerns.
- **Den inspelande spelarens sikte** (paket 38): en riktning, i sidofilens `decoded`
  (`forward`); vid spelarens skott är den en bråkdel av en grad från vart granaten flög.

Allt annat som lästs (hälsa, träffar, skott, spårämnen, explosioner, kanonvinklar,
arenauppdateringar, chatt, kameralägen, klienthändelser, positioner) är `partial`: i tabellen
eller matchdokumentet, och behållet helt i sidofilen.

**Behållet men inte läst** (`raw`), de största slagen: positionsuppdateringar som inte finns i
tabellen (avatarens, efter en stridsvagns död, entiteter som inte finns i listan), paketen 26, 28,
29, 31, 36, 50, 54 och 57, några vanliga fordons- och avataregenskaper, varje metod och egenskap
utan läsare (modulskada, besättning och förbrukningsartiklar bland dem), och egenskaperna hos
entitetsskapanden.

## Inte tillgängligt {#not-available}

- Det som servern aldrig skickade till den inspelande klienten: andra spelares sikte, kamera och
  indata, fiender när de inte är upptäckta. En repris är vad en klient fick veta.
- Namnen på entitetstyper, metoder och egenskaper: de finns i spelets definitionsfiler, inte i
  repriset. Talen behålls.
- Kanonens höjd i grader och allt annat som kräver stridsvagnarnas egna data ur spelets filer.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
