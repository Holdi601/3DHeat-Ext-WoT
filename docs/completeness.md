---
title: Completeness
nav_order: 8
---

# Completeness

Nothing in a replay is thrown away. What the converter reads goes into the
table and the match document; every other item is kept whole in the sidecar
`<match>.messages.parquet`; and the match document's
`selfCheck.completeness` counts what became of each kind of item. This is
the rule all 3DHeat converters share:
[Converters keep everything](https://holdi601.github.io/3DHeat/converters.html).

![The self-check of a synthetic replay: every item seen, read, kept or lost](assets/img/completeness.svg)

## The count

For each kind of item, `selfCheck.completeness.types` gives:

| Count | Means |
|---|---|
| `seen` | how many the replay holds |
| `decoded` | read whole |
| `partial` | read in part, and kept whole in the sidecar |
| `raw` | only kept whole in the sidecar, not read |
| `lost` | lost: always `0` |

The kinds are the replay's own: `block 0` (the header), `block 1` (the
results), `container sizes` and `deflate tail` (the container's own bytes),
`packet <type>`, and for calls on entities `method <entity type>.<number>`
and `property <entity type>.<number>`. Entity types are the numbers the
creating packets give; `selfCheck.entities.roles` says which is the
recording player's avatar and which the vehicles. A kind nobody knew of
shows up with its count.

## The sidecar

| Column | What |
|---|---|
| `time` | the replay's clock, as in the table |
| `type`, `name` | the kind of item; what the converter calls it, where it reads it |
| `entity` | the vehicle or avatar it belongs to, as the table's `entity` |
| `decoded` | what was read of it, as JSON |
| `payload`, `text` | its bytes, whole; the JSON blocks, whole |
| `entityType`, `packet`, `method` | the numbers |

Rows are sorted by packet, method, entity and time.

## What is read, and how it was checked

- **Pitch and roll** of every position: the pitch is minus the slope of the
  tank's own path while it drives forward; two tanks at one spot with one
  heading have the same roll, with opposite headings opposite rolls.
- **Entities** (`entities`): when each came into the client's view and left.
  No tank has a position between leaving and coming back.
- **The version in the stream** (`streamVersion`): the same as the header's.
- **The recording player's aim** (packet 38): a direction, in the sidecar's
  `decoded` (`forward`); at the player's shots it is a fraction of a degree
  from where the shell flew.

Everything else read (health, hits, shots, tracers, explosions, gun angles,
arena updates, chat, camera modes, client events, positions) is `partial`:
in the table or the match document, and kept whole in the sidecar.

**Kept but not read** (`raw`), the biggest kinds: position updates not in
the table (the avatar's, after a tank's death, entities not in the roster),
packets 26, 28, 29, 31, 36, 50, 54 and 57, some frequent vehicle and avatar
properties, every method and property without a reader (module damage, crew
and consumables among them), and the properties of entity creations.

## Not available

- What the server never sent the recording client: other players' aim,
  camera and inputs, enemies while unspotted. A replay is what one client
  was told.
- The names of entity types, methods and properties: they are in the game's
  definition files, not in the replay. The numbers are kept.
- The gun's elevation in degrees and anything else that needs the tanks' own
  data from the game's files.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
