---
title: Vilkår og licens
nav_order: 9
lang: "da"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Vilkår og licens {#terms-and-licence}

## Wargamings vilkår {#wargamings-terms}

Læst 2026-11-07, Wargaming EULA version 14 (i kraft fra 10. april 2024, angivet som gældende):

- 5.3 (b): medmindre det er godkendt skriftligt, må du ikke "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): forbudt er "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

World of Tanks' liste over forbudte mods handler om selve kampen: mods, der "reveal the position of
enemies in a way not included in the client", sigtebots, genladningstimere og lignende. Hverken EULA'en
eller den liste nævner replays.

Hvad denne konverter gør: den læser en fil, spillet skrev, efter kampen, uden for spillet. Den ændrer
intet i spillet, taler med ingen server og viser intet under en kamp. Den dekrypterer strømmen med spillets
nøgle, hvilket 5.3 (b) og 12.1 (p) kan læses som dækkende. At bruge den er brugerens beslutning; derfor er
den en separat pakke.

## Licens og kilder {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Kræver numpy (BSD-3-Clause) og pyarrow
(Apache-2.0). Skrevet til dette projekt: Blowfish-chifferet her er sit eget, med tabellerne udregnet ud fra cifrene i pi,
som chifferet definerer dem. Fakta om formatet (containeren, chifferet, positionspakken) er almindeligt kendt blandt
replay-værktøjer - evido/wotreplay-parser (BSD-3-Clause) dokumenterer dem; ingen kode er taget fra den eller fra
noget andet projekt.

`bigworld.py` og `table.py` er de samme filer som i World of Warships-konverteren
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); ændr begge sammen.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
