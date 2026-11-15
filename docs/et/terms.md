---
title: Tingimused ja litsents
nav_order: 9
lang: et
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Tingimused ja litsents {#terms-and-licence}

## Wargamingi tingimused {#wargamings-terms}

Loetud 2026-11-07, Wargamingi EULA versioon 14 (jõustus 10. aprillil 2024, on praegu kehtiv):

- 5.3 (b): kui ei ole kirjalikult volitatud, ei tohi sa "... decompile, disassemble, reverse engineer or otherwise make
  unauthorized use of the Content".
- 12.1 (k): keelatud on "Creating, using, making available, or distributing any unauthorized software or tools,
  including hacks, cheats, exploits, scripts, bots, trainers, automation programs, or other software that interacts
  with a Product in any way and for any purpose, including intercepts, emulates, or redirects any communication
  between such software and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user experience ("mods") unless expressly
  permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures implemented by Wargaming".

World of Tanksi keelatud modide nimekiri puudutab lahingut ennast: modid, mis "reveal the position of enemies in a
way not included in the client", sihtimisrobotid, laadimistaimerid ja muu selline. Ei EULA ega see nimekiri ei
maini kordusi.

Mida see konverter teeb: ta loeb faili, mille mäng kirjutas, pärast lahingut, väljaspool mängu. Ta ei muuda mängus
midagi, ei räägi ühegi serveriga ega näita midagi lahingu ajal. Ta dešifreerib voo mängu võtmega, ja 5.3 (b) ning
12.1 (p) võib lugeda nii, et need katavad seda. Selle kasutamine on kasutaja otsus; sellepärast on see eraldi pakett.

## Litsents ja allikad {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Vajab numpy'd (BSD-3-Clause) ja
pyarrow'd (Apache-2.0). Kirjutatud selle projekti jaoks: siinne Blowfishi šiffer on oma, tabelid on arvutatud
numbritest pi, nii nagu šiffer seda määratleb. Formaadi faktid (konteiner, šiffer, asukohapakett) on
replay-tööriistade seas tavateadmised - evido/wotreplay-parser (BSD-3-Clause) dokumenteerib neid; kellegi teise
koodi siit ei ole võetud ega ühestki teisest projektist.

`bigworld.py` ja `table.py` on samad failid, mis World of Warshipsi konverteris
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); muuda neid mõlemat koos.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
