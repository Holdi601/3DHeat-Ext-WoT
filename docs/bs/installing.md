---
title: "Instalacija"
nav_order: 3
lang: "bs"
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Instalacija {#installing}

Niste navikli na komandnu liniju? Prvo pročitajte [Prije nego počnete](before-you-start.md).
Potreban je Python 3.10 ili noviji; numpy i pyarrow se instaliraju uz njega.

## Korak po korak {#step-by-step}

1. Nabavite kod: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   ili preuzmite zip sa [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   i raspakirajte ga.
2. Otvorite terminal u tom folderu i upišite `pip install -e .`. Time se naredba
   `heat3d-wot-replay` stavlja na vašu putanju.
3. Provjerite: `heat3d-wot-replay --version`. Trebali biste vidjeti
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` ispisuje opcije:

![heat3d-wot-replay --help](../assets/img/help.svg)

Bez instalacije, `python -m heat3d_ext_wot ...` u folderu alata radi
isto.

3DHeat Watcher pokreće ovu naredbu nad novim replayevima kada je instaliran,
i radi i bez nje.

## Ažuriranja {#updates}

Svako pokretanje prvo provjerava GitHub izdanja projekta (najviše jedan zahtjev
svakih nekoliko sati; nikad ne zaustavlja pretvaranje, bilo da ste online ili ne). Kada izađe novije
izdanje, naredba pita prije instalacije: `git clone` se
ažurira sa `git pull --ff-only` (odbija se dok imate lokalne izmjene), a
preuzeta kopija iz arhive izdanja. `HEAT3D_NO_UPDATE=1` isključuje
provjeru i ažuriranje.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
