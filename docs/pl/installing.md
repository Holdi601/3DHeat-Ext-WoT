---
title: Instalacja
nav_order: 3
lang: pl
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Instalacja {#installing}

Nowy w wierszu poleceń? Najpierw przeczytaj [Zanim zaczniesz](before-you-start.md).
Potrzebny jest Python 3.10 lub nowszy; numpy i pyarrow instalują się razem z nim.

## Krok po kroku {#step-by-step}

1. Pobierz kod: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   albo pobierz archiwum zip z [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   i rozpakuj je.
2. Otwórz terminal w tym folderze i wpisz `pip install -e .`. To umieszcza
   polecenie `heat3d-wot-replay` na Twojej ścieżce (PATH).
3. Sprawdź: `heat3d-wot-replay --version`. Powinieneś zobaczyć
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` wypisuje opcje:

![heat3d-wot-replay --help](../assets/img/help.svg)

Bez instalowania to samo daje `python -m heat3d_ext_wot ...` w folderze narzędzia.

Watcher 3DHeat uruchamia to polecenie na nowych replayach, gdy jest zainstalowany,
i działa bez niego.

## Aktualizacje {#updates}

Każde uruchomienie najpierw sprawdza wydania projektu na GitHubie (najwyżej jedno
zapytanie co kilka godzin; nigdy nie przerywa konwersji, online czy offline). Gdy wychodzi
nowsze wydanie, polecenie pyta, zanim je zainstaluje: `git clone` jest
aktualizowany przez `git pull --ff-only` (odmawia, gdy masz lokalne zmiany), a
pobrana kopia z archiwum wydania. `HEAT3D_NO_UPDATE=1` wyłącza
sprawdzanie i aktualizację.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
