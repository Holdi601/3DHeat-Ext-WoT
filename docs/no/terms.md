---
title: "Vilkår og lisens"
nav_order: 9
lang: no
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Vilkår og lisens {#terms-and-licence}

## Wargamings vilkår {#wargamings-terms}

Lest 2026-11-07, Wargaming EULA versjon 14 (gjelder fra 10. april 2024, oppført som gjeldende):

- 5.3 (b): med mindre det er gitt skriftlig tillatelse, må du ikke «... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content».
- 12.1 (k): forbudt er «Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming.»
- 12.1 (l): «... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming».
- 12.1 (p): «Circumventing or bypassing enforcement and security measures
  implemented by Wargaming».

Listen over forbudte mods i World of Tanks handler om selve slaget: mods som
«reveal the position of enemies in a way not included in the client», sikteroboter,
ladetidstimere og lignende. Verken EULA eller den listen nevner replayer.

Hva denne konverteren gjør: den leser en fil spillet skrev, etter slaget, utenfor spillet. Den endrer ingenting
i spillet, snakker med ingen server, og viser ingenting under et slag. Den dekrypterer strømmen med spillets
nøkkel, noe 5.3 (b) og 12.1 (p) kan leses som å dekke. Å bruke den er brukerens egen beslutning; derfor er den en egen pakke.

## Lisens og kilder {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Trenger numpy (BSD-3-Clause) og pyarrow
(Apache-2.0). Skrevet for dette prosjektet: Blowfish-chifferet her er sitt eget, med tabellene regnet ut fra sifrene i pi slik
chifferet definerer dem. Fakta om formatet (containeren, chifferet, posisjonspakken) er allment kjent blant replayverktøy -
evido/wotreplay-parser (BSD-3-Clause) dokumenterer dem; ingen kode er tatt fra den eller fra noe annet prosjekt.

`bigworld.py` og `table.py` er de samme filene som i World of Warships-konverteren
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); endre begge sammen.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
