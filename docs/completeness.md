---
title: Completeness
nav_order: 7
---

# Completeness

![The self-check of a synthetic replay: every item seen, read, kept or lost](assets/img/completeness.svg)

The converter follows the rule all 3DHeat converters share,
[Converters keep everything](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md):
what it reads goes into the table and the summary; every other item of the
replay is kept whole in the sidecar `<match>.messages.parquet`; and the
summary's `selfCheck.completeness` counts, for each kind of item, how many the
replay holds (`seen`), how many were read whole (`decoded`), read in part and
kept whole (`partial`), only kept (`raw`), and lost (`lost`, 0).

The kinds are the replay's own: `block 0` (the header), `block 1` (the
results), `container sizes` and `deflate tail` (the container's own bytes),
`packet <type>`, and for entity calls `method <entity type>.<number>` and
`property <entity type>.<number>`. Entity types are the numbers the creating
packets give; the summary's `selfCheck.entities.roles` says which is the
recording player's avatar and which the vehicles (2 and 6 on every replay
read). They are counted as the converter meets them in the stream, so a kind
nobody knew of shows up with its count.

The sidecar's columns: `time` (the replay's clock, as the table's),
`type`, `name` (what the converter calls it, where it reads it), `entity` (the
vehicle or avatar it belongs to, as the table's `entity`), `decoded` (what was
read of it, JSON), `payload` (its bytes, whole: a packet's payload as the
stream has it), `text` (the JSON blocks, whole), `entityType`, `packet` and
`method` (the numbers). Rows are sorted by packet, method, entity and time.
Everything a later reader needs is in it, or in the summary's `entities`.

**Read** (new in this pass, each checked against something independent):

- **Pitch and roll** of every position (`pitch`, `roll`). Pitch: on Karelia,
  Great Wall, Westfeld and Pilsen it is minus the slope of the vehicle's own
  path while it drives forward (correlation -0.96, -0.96, -0.98, -0.84;
  median difference 0.003-0.008 rad). Roll: two vehicles at the same spot
  (within 0.5 m) with the same heading have the same roll (correlation 0.98,
  0.99, 0.98 on Karelia, Westfeld, Great Wall), with opposite headings
  opposite rolls (-0.98, -0.997, -0.98).
- **Entities** (summary `entities`): the creating packets (0 and 5) give the
  entity and its type, the rest of them is kept; the leaving packet (4: the
  entity alone) is read whole. Check: no vehicle has a position update
  between leaving and coming back (0 on all four; 192, 180, 141 and 190
  entities, 199, 141, 105 and 280 leaves).
- **The version in the stream** (packet 24, `streamVersion`): the same as the
  header's on all four.
- **The recording player's aim** (packet 38, 40 bytes, about 10 a second): a
  rotation (x, y, z, w) whose +z is where the player aims; the sidecar's
  `decoded` has that direction (`forward`). Check: at the player's shots it
  is a median 0.14 and 0.14 degrees (26 and 19 shots, 2.4.1) and 0.56 (11
  shots, 1.12) from the direction the shell flew; 6 degrees on the replay with
  2 shots.

Everything read before this pass (health, hits, shots, tracers, explosions,
gun angles, arena updates, chat, camera modes, client events) is `partial`:
read into the table and the summary as above, and kept whole in the sidecar
with what was read in `decoded`. So are the positions: the table has place,
heading, pitch and roll, the sidecar the whole update.

**Kept raw** (in the sidecar, not read), the biggest kinds:

- `packet 10`, the position updates not in the table: the avatar's (it rides
  the vehicle: the second id is the vehicle's), positions after a vehicle's
  death, entities not in the roster; and in every update three floats
  (BigWorld calls them the position's error; not checked) and a flag byte (1
  but for 20-28 updates a replay; not known).
- `packet 26` and `packet 31`, about 10 a second, as many of each: 26 is
  52 bytes (1.12) or 60 (2.4.1) of floats beginning with a point in the
  world, 31 four bytes; not known. `packet 28`, `29` (a float
  each), `57` (2.x, 72 bytes), `54` (2.x, empty): not known.
- The vehicles' frequent 2-byte property (`property 6.11` in 1.12, `6.15` in
  2.4.1) and 1-byte property `6.1`, the avatar's 8-byte property (`2.17`,
  2.19 in 2.4.1): not known.
- `packet 36`: an entity, a byte, a length and that many bytes (likely a
  change inside a property; not read). Every method and property without a
  reader (module damage, crew, consumables and the like among them), the
  entity creations' properties, `packet 50` and the rest.

Per replay (the four of [Verified](how-it-reads.md#verified)):

| Replay | Seen | Decoded | Partial | Raw | Lost | Sidecar | Replay |
|---|---|---|---|---|---|---|---|
| Karelia 1.12 | 112,582 | 200 | 77,685 | 34,697 | 0 | 1.11 MB | 1.48 MB |
| Great Wall 2.4.1 | 157,992 | 281 | 86,633 | 71,078 | 0 | 1.75 MB | 2.41 MB |
| Westfeld 2.4.1 | 117,360 | 106 | 74,557 | 42,697 | 0 | 1.14 MB | 1.65 MB |
| Pilsen 2.4.1 | 46,880 | 142 | 26,918 | 19,820 | 0 | 0.47 MB | 0.70 MB |

**Not available:**

- What the server never sent the recording client: other players' aim,
  camera and inputs, enemies while unspotted. A replay is what one client
  was told.
- The names of entity types, methods and properties: they are in the game's
  definition files, not in the replay. The numbers are kept; the converter
  names what it finds by content.
- The gun's elevation in degrees and anything else that needs the tanks'
  own data (the game's vehicle files, not the replay).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
