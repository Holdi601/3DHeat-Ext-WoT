---
title: "Instalace"
nav_order: 3
lang: cs
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Instalace {#installing}

Nikdy jste nepracovali s příkazovým řádkem? Nejdříve si přečtěte [Než začnete](before-you-start.md).
Potřebuje Python 3.10 nebo novější; numpy a pyarrow se nainstalují spolu s ním.

## Krok za krokem {#step-by-step}

1. Získejte kód: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   nebo stáhněte zip z [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   a rozbalte ho.
2. Otevřete terminál v té složce a napište `pip install -e .`. Tím se příkaz
   `heat3d-wot-replay` dostane na vaši cestu (PATH).
3. Ověřte to: `heat3d-wot-replay --version`. Měli byste vidět
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` vypíše volby:

![heat3d-wot-replay --help](../assets/img/help.svg)

Bez instalace dělá totéž `python -m heat3d_ext_wot ...` ve složce nástroje.

Watcher 3DHeat spouští tento příkaz nad novými replayi, když je nainstalovaný,
a funguje i bez něj.

## Aktualizace {#updates}

Každé spuštění nejdřív zkontroluje GitHub vydání projektu (nejvýš jeden dotaz každých pár hodin; převod nikdy
nezastaví, ať je online, nebo ne). Když je vydána novější verze, příkaz se před instalací zeptá: `git clone` se
aktualizuje příkazem `git pull --ff-only` (odmítne se, pokud máte lokální změny), stažená kopie z archivu vydání.
`HEAT3D_NO_UPDATE=1` kontrolu i aktualizaci vypne.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
