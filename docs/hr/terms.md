---
title: Pojmovi i licenca
nav_order: 9
lang: "hr"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Pojmovi i licenca {#terms-and-licence}

## Wargamingovi uvjeti {#wargamings-terms}

Pročitano 2026-11-07, Wargaming EULA verzija 14 (na snazi od 10. travnja 2024., navedena kao
aktualna):

- 5.3 (b): osim ako nije odobreno u pisanom obliku, ne smiješ "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): zabranjeno je "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

Popis zabranjenih modova World of Tanksa odnosi se na samu bitku: modovi koji
"reveal the position of enemies in a way not included in the client", ciljački botovi,
tajmeri punjenja i slično. Ni EULA ni taj popis ne spominju snimke.

Što ovaj pretvarač radi: čita datoteku koju je igra zapisala, nakon bitke, izvan igre. Ne mijenja
ništa u igri, ne razgovara ni s jednim poslužiteljem i ništa ne prikazuje tijekom bitke. Tok dešifrira
igrinim ključem, a 5.3 (b) i 12.1 (p) se mogu tumačiti da to obuhvaćaju. Korištenje je odluka korisnika;
zato je to zaseban paket.

## Licenca i izvori {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Treba numpy (BSD-3-Clause) i pyarrow
(Apache-2.0). Napisano za ovaj projekt: Blowfish šifra ovdje je vlastita, s tablicama izračunatim iz znamenki broja pi
kako ih šifra definira. Činjenice o formatu (kontejner, šifra, paket položaja) su opće poznate među alatima za
snimke - evido/wotreplay-parser (BSD-3-Clause) ih dokumentira; nijedan kod nije uzet iz njega ni iz nekog drugog projekta.

`bigworld.py` i `table.py` su iste datoteke kao u pretvaraču za World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); mijenjaj ih oba zajedno.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
