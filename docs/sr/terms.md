---
title: Услови и лиценца
nav_order: 9
lang: "sr"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Услови и лиценца {#terms-and-licence}

## Wargaming-ови услови {#wargamings-terms}

Прочитано 2026-11-07, Wargaming EULA верзија 14 (на снази од 10. априла 2024,
наведена као актуелна):

- 5.3 (b): unless authorised in writing, you must not "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): prohibited is "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

Листа забрањених модова World of Tanks-а тиче се саме битке: модови који
"reveal the position of enemies in a way not included in the client", нишанске ботове, тајмере за поновно пуњење и слично. Ни EULA ни та листа не помињу реплеје.

Шта овај конвертор ради: чита датотеку коју је игра записала, после битке,
ван игре. Ништа не мења у игри, не разговара ни са једним сервером, и ништа
не приказује током битке. Он ипак дешифрује низ игриним кључем, што се 5.3 (b)
и 12.1 (p) могу читати да покривају. Коришћење је одлука корисника; зато је
посебан пакет.

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
