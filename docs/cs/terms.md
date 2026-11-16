---
title: "Podmínky a licence"
nav_order: 9
lang: "cs"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Podmínky a licence {#terms-and-licence}

## Co čte {#what-it-reads}

Převodník čte soubory replayů, které hra zapsala na vašem vlastním počítači,
po bitvě a mimo hru. Nic ve hře nemění, nekomunikuje s žádným serverem a během
bitvy nic nezobrazuje. Nic ze hry se s ním nedodává ani dál nešíří: žádná data
hry, žádný kód hry, žádné knihovny DLL. To, co zapíše, zůstává na vašem
počítači.

3DHeat není přidružen ke společnosti Wargaming ani jí schválen. World of Tanks
a související názvy a ochranné známky patří jejich vlastníkům.

Držitelé práv: založte issue na
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - odpovídáme rychle a na
požádání cokoli odstraníme.

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
