---
title: "Skilmálar og leyfi"
nav_order: 9
lang: is
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Skilmálar og leyfi {#terms-and-licence}

## Skilmálar Wargaming {#wargamings-terms}

Lesið 2026-11-07, Wargaming EULA útgáfa 14 (í gildi frá 10. apríl 2024, skráð
sem núverandi):

- 5.3 (b): nema með skriflegri heimild máttu ekki "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): bannað er "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

Listi World of Tanks yfir bannaðar viðbætur (mods) snýst um bardagann sjálfan: viðbætur sem
"reveal the position of enemies in a way not included in the client", miðunar-
bottar, endurhleðslutímar og þess háttar. Hvorki EULA né sá listi nefnir
upptökur.

Það sem þessi breytir gerir: hann les skrá sem leikurinn skrifaði, eftir bardagann,
utan leiksins. Hann breytir engu í leiknum, talar við engan þjón og
sýnir ekkert meðan á bardaga stendur. Hann afkóðar strauminn með lykli leiksins,
sem hægt er að lesa 5.3 (b) og 12.1 (p) þannig að nái yfir. Notkun hans er ákvörðun
notandans; þess vegna er hann sérstakur pakki.

## Leyfi og heimildir {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Þarf numpy (BSD-3-Clause) og pyarrow
(Apache-2.0). Skrifað fyrir þetta verkefni: Blowfish dulmálið hér er eigið,
með töflur sínar reiknaðar úr tölustöfum pí eins og dulmálið skilgreinir þær.
Staðreyndir um sniðið (gáminn, dulmálið, stöðupakkann) eru almenn vitneskja meðal
upptökuverkfæra - evido/wotreplay-parser (BSD-3-Clause) skjalfestir þær;
enginn kóði var tekinn úr honum né úr nokkru öðru verkefni.

`bigworld.py` og `table.py` eru sömu skrár og í World of Warships
breytinum ([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); breyttu báðum saman.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
