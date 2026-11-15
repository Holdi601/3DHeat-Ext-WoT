---
title: Condicions i llicència
nav_order: 9
lang: "ca"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Condicions i llicència {#terms-and-licence}

## Les condicions de Wargaming {#wargamings-terms}

Llegides el 2026-11-07, EULA de Wargaming versió 14 (en vigor des del 10 d'abril de 2024, indicada com a
vigent):

- 5.3 (b): tret que s'autoritzi per escrit, no pots «... decompile, disassemble, reverse engineer or otherwise
  make unauthorized use of the Content» (descompilar, desmuntar, fer enginyeria inversa o fer d'una altra manera
  un ús no autoritzat del Contingut).
- 12.1 (k): es prohibeix «Creating, using, making available, or distributing any unauthorized software or tools,
  including hacks, cheats, exploits, scripts, bots, trainers, automation programs, or other software that interacts
  with a Product in any way and for any purpose, including intercepts, emulates, or redirects any communication
  between such software and Wargaming» (crear, usar, posar a disposició o distribuir qualsevol programari o eina no
  autoritzats, incloent-hi hacks, trampes, exploits, scripts, bots, entrenadors, programes d'automatització o
  qualsevol altre programari que interactuï d'alguna manera amb un Producte i per a qualsevol finalitat, incloent-hi
  els que interceptin, emulin o redirigeixin qualsevol comunicació entre aquest programari i Wargaming).
- 12.1 (l): «... any software designed to modify a Product and change the user experience ("mods") unless expressly
  permitted by Wargaming» (qualsevol programari dissenyat per modificar un Producte i canviar l'experiència de
  l'usuari («mods») tret que Wargaming ho permeti expressament).
- 12.1 (p): «Circumventing or bypassing enforcement and security measures implemented by Wargaming» (eludir o
  saltar-se les mesures de compliment i de seguretat que aplica Wargaming).

La llista de mods prohibits de World of Tanks tracta de la batalla en si: mods que «reveal the position of enemies
in a way not included in the client» (revelen la posició dels enemics d'una manera que no és al client), bots de
punteria, temporitzadors de recàrrega i similars. Ni l'EULA ni aquella llista no esmenten les repeticions.

El que fa aquest convertidor: llegeix un fitxer que ha escrit el joc, després de la batalla, fora del joc. No canvia
res al joc, no parla amb cap servidor, i no mostra res durant una batalla. Sí que desxifra el flux amb la clau del
joc, cosa que 5.3 (b) i 12.1 (p) es poden llegir com a coberta. Fer-lo servir és decisió de l'usuari; per això és un
paquet a part.

## Llicència i fonts {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Necessita numpy (BSD-3-Clause) i
pyarrow (Apache-2.0). Escrit per a aquest projecte: el xifrat Blowfish d'aquí és propi, amb les seves taules calculades
a partir dels dígits de pi tal com les defineix el xifrat. Els fets del format (el contenidor, el xifrat, el paquet de
posició) són coneguts entre les eines de repeticions: evido/wotreplay-parser (BSD-3-Clause) els documenta; no s'hi ha
pres cap codi ni d'ell ni de cap altre projecte.

`bigworld.py` i `table.py` són els mateixos fitxers que al convertidor de World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); canvia'ls tots dos alhora.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
