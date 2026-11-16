---
title: "Podmienky a licencia"
nav_order: 9
lang: "sk"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Podmienky a licencia {#terms-and-licence}

## Čo číta {#what-it-reads}

Konvertor číta súbory replayov, ktoré hra zapísala na vašom vlastnom počítači,
po bitke a mimo hry. V hre nič nemení, nekomunikuje so žiadnym serverom a
počas bitky nič nezobrazuje. Nič z hry sa s ním nedodáva ani ďalej nešíri:
žiadne dáta hry, žiadny kód hry, žiadne DLL. To, čo zapíše, zostáva na vašom
počítači.

3DHeat nie je pridružený k spoločnosti Wargaming ani ňou schválený. World of
Tanks a súvisiace názvy a ochranné známky patria ich vlastníkom.

Držitelia práv: založte issue na
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - odpovedáme rýchlo a na
požiadanie čokoľvek odstránime.

## Licencia a zdroje {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Potrebuje numpy (BSD-3-Clause) a pyarrow
(Apache-2.0). Napísané pre tento projekt: šifra Blowfish tu je vlastná, jej tabuľky sú vypočítané z číslic čísla pi, ako to šifra definuje.
Fakty o formáte (kontajner, šifra, paket polohy) sú medzi autormi replay nástrojov všeobecne známe – evido/wotreplay-parser (BSD-3-Clause)
ich dokumentuje; žiadny kód sa z neho ani z iného projektu neprebral.

`bigworld.py` a `table.py` sú tie isté súbory ako v konvertore pre World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); meňte ich oba naraz.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
