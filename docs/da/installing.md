---
title: Installation
nav_order: 3
lang: "da"
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Installation {#installing}

Ny til kommandolinjen? Læs [Før du går i gang](before-you-start.md) først.
Kræver Python 3.10 eller nyere; numpy og pyarrow installeres sammen med det.

## Trin for trin {#step-by-step}

1. Hent koden: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   eller download en zip fra [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   og pak den ud.
2. Åbn en terminal i den mappe og skriv `pip install -e .`. Det gør kommandoen
   `heat3d-wot-replay` tilgængelig på din sti.
3. Tjek det: `heat3d-wot-replay --version`. Du bør se
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` viser valgmulighederne:

![heat3d-wot-replay --help](../assets/img/help.svg)

Uden installation gør `python -m heat3d_ext_wot ...` i værktøjets mappe det samme.

3DHeat Watcher kører denne kommando på nye replays, når den er installeret, og
fungerer uden den.

## Opdateringer {#updates}

Hver start tjekker først projektets GitHub-releases (højst én forespørgsel hver
få timer; det stopper aldrig en konvertering, hverken online eller offline). Når
en nyere release er udgivet, spørger kommandoen, før den installerer den: en
`git clone` opdateres med `git pull --ff-only` (afvist, mens du har lokale
ændringer), en downloadet kopi fra releasens arkiv. `HEAT3D_NO_UPDATE=1` slår
tjekket og opdateringen fra.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
