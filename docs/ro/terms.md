---
title: Termeni și licență
nav_order: 9
lang: "ro"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Termeni și licență {#terms-and-licence}

## Ce citește {#what-it-reads}

Convertorul citește fișierele de reluare pe care jocul le-a scris pe propriul
tău calculator, după bătălie și în afara jocului. Nu schimbă nimic în joc, nu
comunică cu niciun server și nu afișează nimic în timpul unei bătălii. Nimic
din joc nu este livrat sau redistribuit împreună cu el: nicio resursă a
jocului, niciun cod al jocului, niciun DLL. Ce scrie rămâne pe calculatorul
tău.

3DHeat nu este afiliat cu Wargaming și nici aprobat de Wargaming. World of
Tanks și numele și mărcile comerciale asociate aparțin proprietarilor lor.

Deținători de drepturi: deschideți un issue la
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - răspundem repede și
eliminăm orice la cerere.

## Licență și surse {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Are nevoie de numpy (BSD-3-Clause) și pyarrow
(Apache-2.0). Scris pentru acest proiect: cifrul Blowfish de aici este propriul său,
cu tabelele sale calculate din cifrele lui pi, așa cum le definește cifrul.
Faptele despre format (containerul, cifrul, pachetul de poziție) sunt cunoscute în comun de instrumentele pentru replay -
evido/wotreplay-parser (BSD-3-Clause) le documentează; niciun cod nu a fost luat de la el sau de la vreun alt proiect.

`bigworld.py` și `table.py` sunt aceleași fișiere ca în convertorul pentru World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); schimbați-le pe amândouă împreună.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
