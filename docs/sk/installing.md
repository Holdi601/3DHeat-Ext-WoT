---
title: "Inštalácia"
nav_order: 3
lang: "sk"
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Inštalácia {#installing}

Ste noví v príkazovom riadku? Najskôr si prečítajte [Než začnete](before-you-start.md).
Potrebujete Python 3.10 alebo novší; numpy a pyarrow sa nainštalujú spolu s ním.

## Krok za krokom {#step-by-step}

1. Získajte kód: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   alebo stiahnite zip z [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   a rozbaľte ho.
2. Otvorte terminál v tomto priečinku a napíšte `pip install -e .`. Tento príkaz
   sprístupní príkaz `heat3d-wot-replay` vo vašej ceste PATH.
3. Skontrolujte to: `heat3d-wot-replay --version`. Mali by ste vidieť
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` vypíše možnosti:

![heat3d-wot-replay --help](../assets/img/help.svg)

Bez inštalácie urobí to isté `python -m heat3d_ext_wot ...` v priečinku nástroja.

Watcher 3DHeat spúšťa tento príkaz na nové replaye, keď je nainštalovaný,
a funguje aj bez neho.

## Aktualizácie {#updates}

Každé spustenie najskôr skontroluje GitHub releases projektu (najviac jedna
požiadavka každých pár hodín; konverziu nikdy nezastaví, či ste online alebo
nie). Keď je vydaná novšia verzia, príkaz sa pred inštaláciou opýta: `git clone`
sa aktualizuje cez `git pull --ff-only` (odmietne sa, ak máte lokálne zmeny),
stiahnutá kópia z archívu vydania. `HEAT3D_NO_UPDATE=1` kontrolu aj aktualizáciu vypne.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
