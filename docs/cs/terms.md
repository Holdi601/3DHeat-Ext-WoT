---
title: "Podmínky a licence"
nav_order: 9
lang: cs
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Podmínky a licence {#terms-and-licence}

## Podmínky Wargamingu {#wargamings-terms}

Přečteno 2026-11-07, EULA Wargamingu verze 14 (účinná od 10. dubna 2024, uvedená jako platná):

- 5.3 (b): pokud to nepovolíte písemně, nesmíte "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): zakázáno je "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

Seznam zakázaných modů World of Tanks se týká samotné bitvy: mody, které
"reveal the position of enemies in a way not included in the client", aim
boty, časovače přebíjení a podobně. Ani EULA, ani tento seznam nezmiňuje
replaye.

Co tento převodník dělá: čte soubor, který hra zapsala po bitvě, mimo hru. Nic ve hře nemění, s žádným serverem
nemluví a během bitvy nic neukazuje. Proud dešifruje klíčem hry, o kterém lze podle 5.3 (b) a 12.1 (p) číst, že je
pokrytý. Použití je rozhodnutí uživatele; proto je to samostatný balíček.

## Licence a zdroje {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Potřebuje numpy (BSD-3-Clause) a pyarrow
(Apache-2.0). Napsáno pro tento projekt: šifra Blowfish zde je vlastní,
s tabulkami spočítanými z číslic pí, jak ji šifra definuje.
Fakta o formátu (kontejner, šifra, paket pozic) jsou mezi nástroji pro čtení replayů běžně známá - evido/wotreplay-parser (BSD-3-Clause)
je dokumentuje; žádný kód z něj ani z jiného projektu nebyl převzat.

`bigworld.py` a `table.py` jsou stejné soubory jako v převodníku pro World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); měňte je vždy společně.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
