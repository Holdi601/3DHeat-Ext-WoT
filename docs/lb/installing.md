---
title: "Installéieren"
nav_order: 3
lang: "lb"
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Installéieren {#installing}

Nei op der Kommandozeil? Liest fir d'éischt [Ier Dir ufänkt](before-you-start.md).
Brauch Python 3.10 oder méi nei; numpy a pyarrow ginn domat installéiert.

## Schrëtt fir Schrëtt {#step-by-step}

1. Hollt de Code: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   oder luet eng Zip vun [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   erof a packt se aus.
2. Mécht en Terminal an deem Dossier op an tippt `pip install -e .`. Dat setzt de
   Befehl `heat3d-wot-replay` op Äre Wee (PATH).
3. Préift et: `heat3d-wot-replay --version`. Dir sollt
   `heat3d-wot-replay 0.1.0` gesinn. `heat3d-wot-replay --help` list d'Optiounen op:

![heat3d-wot-replay --help](../assets/img/help.svg)

Ouni Installatioun mécht `python -m heat3d_ext_wot ...` am Dossier vum Tool
datselwecht.

Den 3DHeat Watcher léisst dëse Befehl op nei Replays lafen, wann en installéiert ass,
a funktionéiert och ouni en.

## Updates {#updates}

All Start kuckt fir d'éischt an de GitHub-Releases vum Projet no (héchstens eng Ufro
all puer Stonnen; et stoppt ni eng Émwandlung, online oder net). Wann e méi neie
Release do ass, freet de Befehl, ier en en installéiert: e `git clone` gëtt
mat `git pull --ff-only` aktualiséiert (verweigert, wann Dir lokal Ännerunge hutt), eng
erofgeluede Kopie aus dem Archiv vum Release. `HEAT3D_NO_UPDATE=1` schalt d'
Kontroll an d'Update aus.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
