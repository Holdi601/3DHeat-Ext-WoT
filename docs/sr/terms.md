---
title: Услови и лиценца
nav_order: 9
lang: "sr"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Услови и лиценца {#terms-and-licence}

## Шта чита {#what-it-reads}

Конвертор чита датотеке реплеја које је игра записала на вашем сопственом
рачунару, после битке и ван игре. Не мења ништа у игри, не комуницира ни са
једним сервером и не приказује ништа током битке. Ништа из игре се не
испоручује нити даље дистрибуира са њим: нема ресурса игре, кода игре ни DLL
датотека. Оно што запише остаје на вашем рачунару.

3DHeat није повезан са Wargaming-ом нити га Wargaming подржава. World of Tanks
и повезани називи и жигови припадају својим власницима.

Носиоци права: отворите issue на
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - брзо одговарамо и на
захтев уклањамо било шта.

## Лиценца и извори {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Потребни су numpy (BSD-3-Clause) и pyarrow
(Apache-2.0). Написано за овај пројекат: Blowfish шифра овде је њена сопствена,
с табелама израчунатим из цифара броја пи, како шифра то дефинише.
Чињенице о формату (контејнер, шифра, пакет позиције) су опште знање међу
алаткама за реплеје - evido/wotreplay-parser (BSD-3-Clause) их документује;
ниједан код није узет из њега или из било ког другог пројекта.

`bigworld.py` и `table.py` су исте датотеке као у конвертору World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); мењајте обе заједно.

---

Део [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
