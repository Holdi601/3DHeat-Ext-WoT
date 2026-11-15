---
title: Asennus
nav_order: 3
lang: fi
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Asennus {#installing}

Uusi komentoriviltä? Lue ensin [Ennen aloittamista](before-you-start.md). Tarvitaan Python 3.10
tai uudempi; numpy ja pyarrow asennetaan sen mukana.

## Vaihe vaiheelta {#step-by-step}

1. Hae koodi: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`, tai lataa zip-tiedosto
   [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)-sivulta ja pura se.
2. Avaa pääte kyseisessä kansiossa ja kirjoita `pip install -e .`. Tämä asettaa komennon
   `heat3d-wot-replay` polulle.
3. Tarkista: `heat3d-wot-replay --version`. Sinun pitäisi nähdä `heat3d-wot-replay 0.1.0`.
   `heat3d-wot-replay --help` luettelee valinnat:

![heat3d-wot-replay --help](../assets/img/help.svg)

Ilman asennusta `python -m heat3d_ext_wot ...` työkalun kansiossa tekee saman.

3DHeat Watcher ajaa tätä komentoa uusille replayille, kun se on asennettu, ja toimii ilman sitä.

## Päivitykset {#updates}

Jokainen käynnistys tarkistaa ensin projektin GitHub-julkaisut (enintään yksi pyyntö muutaman tunnin
välein; se ei koskaan pysäytä muunnosta, verkossa tai ilman verkkoa). Kun uudempi julkaisu on
ilmestynyt, komento kysyy ennen sen asentamista: `git clone` -kopio päivitetään komennolla
`git pull --ff-only` (hylätään, jos sinulla on paikallisia muutoksia), ladattu kopio julkaisun
arkistosta. `HEAT3D_NO_UPDATE=1` kytkee tarkistuksen ja päivityksen pois.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
