---
title: Инсталација
nav_order: 3
lang: sr
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Инсталација {#installing}

Први пут у командној линији? Прво прочитајте [Пре почетка](before-you-start.md).
Потребан је Python 3.10 или новији; numpy и pyarrow се инсталирају са њим.

## Корак по корак {#step-by-step}

1. Преузмите код: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   или преузмите зип са [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   и распакујте га.
2. Отворите терминал у тој фасцикли и укуцајте `pip install -e .`. Ово ставља
   команду `heat3d-wot-replay` на вашу путању.
3. Проверите: `heat3d-wot-replay --version`. Требало би да видите
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` исписује опције:

![heat3d-wot-replay --help](../assets/img/help.svg)

Без инсталирања, `python -m heat3d_ext_wot ...` у фасцикли алатке ради
исто.

3DHeat Watcher покреће ову команду над новим реплејима кад је инсталиран, а
ради и без ње.

## Ажурирања {#updates}

Сваки старт прво проверава GitHub издања пројекта (највише једном у
неколико сати; никад не зауставља претварање, на мрежи или ван ње). Кад је
нова верзија изашла, команда пита пре инсталације: `git clone` се ажурира
помоћу `git pull --ff-only` (одбија се док имате локалне измене), а преузета
копија из архиве издања. `HEAT3D_NO_UPDATE=1` искључује проверу и ажурирање.

---

Део [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
