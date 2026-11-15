---
title: "Услови и лиценца"
nav_order: 9
lang: mk
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Услови и лиценца {#terms-and-licence}

## Условите на Wargaming {#wargamings-terms}

Прочитано на 2026-11-07, Wargaming EULA верзија 14 (во сила од 10 April 2024, наведена како актуелна):

- 5.3 (b): освен ако не е овластено писмено, не смеете да „... decompile, disassemble, reverse engineer or otherwise make unauthorized use of the Content“.
- 12.1 (k): забрането е „Creating, using, making available, or distributing any unauthorized software or tools, including hacks, cheats, exploits, scripts, bots, trainers, automation programs, or other software that interacts with a Product in any way and for any purpose, including intercepts, emulates, or redirects any communication between such software and Wargaming.“
- 12.1 (l): „... any software designed to modify a Product and change the user experience ("mods") unless expressly permitted by Wargaming“.
- 12.1 (p): „Circumventing or bypassing enforcement and security measures implemented by Wargaming“.

Листата на забранети модови на World of Tanks е за самата битка: модови што „reveal the position of enemies in a way not included in the client“, aim ботови, тајмери за презареддување и слично. Ниту EULA ниту таа листа ги спомнува снимките.

Што прави овој конвертор: чита датотека што ја напишала играта, по битката, надвор од играта. Не менува ништо во играта, не разговара со ниту еден сервер и не прикажува ништо за време на битка. Го дешифрира текот со клучот на играта, што 5.3 (b) и 12.1 (p) може да се прочитаат дека го опфаќаат. Користењето е одлука на корисникот; затоа е одделен пакет.

## Лиценца и извори {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Бара numpy (BSD-3-Clause) и pyarrow (Apache-2.0). Напишано за овој проект: шифрата Blowfish тука е сопствена, со табели пресметани од цифрите на пи како што ги дефинира шифрата. Фактите за форматот (контејнерот, шифрата, пакетот со позиции) се општо знаење меѓу алатките за снимки - evido/wotreplay-parser (BSD-3-Clause) ги документира; ниту еден код не е земен од него или од кој и да е друг проект.

`bigworld.py` и `table.py` се истите датотеки како во конверторот за World of Warships ([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); менувајте ги заедно.

---

Дел од [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
