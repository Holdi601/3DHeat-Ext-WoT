---
title: Com llegeix una repetició
nav_order: 7
lang: ca
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Com llegeix una repetició {#how-it-reads-a-replay}

Una repetició és una capçalera de blocs JSON i el flux de paquets del joc (notes del format a
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- El primer bloc, sense xifrar: el mapa, la versió del client, el jugador que grava, la configuració del
  servidor i la llista de vehicles (`vehicles`: nom, equip, tanc, indexada per l'identificador del vehicle).
- El segon, quan la gravació va durar fins al final: la pantalla de resultats; la línia de cada vehicle
  (trets, impactes, perforacions, dany fet, rebut, bloquejat i assistit, detecció, experiència, crèdits,
  assoliments...), els detalls per objectiu del jugador que grava, els comptes, la durada de la partida, el
  guanyador i el motiu de final; en alguns modes, l'única llista completa de vehicles (la capçalera d'aquestes
  llistes només té el propi equip).
- El flux de paquets, comprimit amb zlib i xifrat amb Blowfish amb una clau que porta el joc, que les eines de
  la comunitat que llegeixen aquests fitxers han publicat des del 2013.

**Les posicions** són les actualitzacions de posició del motor: l'identificador d'un vehicle, la seva posició
i el seu heading, trobades per la seva forma més que pel seu número de paquet, de manera que un pedaç que els
renumeri no buida la taula. Són el que se li va dir al client que gravava: el seu propi equip durant tota la
partida, i un enemic només mentre és detectat (o dins l'abast del client). Un vehicle mai detectat no té
files. Les files d'un vehicle s'aturen a la seva mort.

**La resta del flux** (salut, trets, traçadors, explosions, impactes, angles de canó, actualitzacions de
l'arena) són crides a mètodes i canvis de propietats dels vehicles i de l'avatar del client, numerats pels
fitxers de definició del joc, que canvien amb els pedaços (1.12 i 2.4 els numeren de manera diferent). Cada
una es troba per la forma dels seus arguments i com s'enganxen entre ells (vegeu
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py)), i
els números trobats són al `decoded` del document de partida. El xat, el mode de càmera i els esdeveniments
propis del client són paquets propis. Les actualitzacions de l'arena i els esdeveniments del client són
`pickle` de Python; els llegeix un lector que converteix cada classe que nomenen en un substitut inert i no
n'executa res.

El que se li va dir al client és complet per al seu propi equip i parcial per als enemics: els seus trets,
impactes i canvis de salut hi són mentre eren a l'abast.

**L'inici de la batalla** és quan l'actualització de l'arena diu que el període de batalla va començar; en una
repetició sense ella, el primer moment en què es mou un vehicle.

**Les morts:** l'hora és el missatge de mort de l'arena (1.x), si no el canvi de salut que va acabar el vehicle,
si no l'inici de la batalla més el `lifeTime` de la víctima als resultats (segons sencers). El lloc és on la
víctima es va veure per última vegada, quan era dins de cinc segons de la seva mort; si no, en clients 2.x, el
lloc que donen els resultats (x i z, sense alçada), només al document de partida. Una gravació que es va aturar
abans del final no té morts.

**No llegit:**

- La detecció i el minimapa: no són al flux com a esdeveniments propis.
- L'elevació del canó en graus: el flux té un pas entre els límits del canó, i els límits són als fitxers de
  vehicle del joc.
- El dany de mòduls, les ferides de la tripulació, els consumibles i la munició: les crides que els porten no
  es podien distingir només per la forma entre 1.12 i 2.4.
- Els paquets de creació d'entitats més enllà de l'entitat i el seu tipus: porten totes les propietats d'un
  vehicle que entra a la vista del client d'una vegada, en un ordre que només donen els fitxers de definició
  (guardats sencers a l'annex).
- Les col·lisions estàtiques (arbres, cases), la mira pròpia del jugador que grava i els paquets de física.
- Els números de les ordres de xat de batalla com a noms: la numeració és la del joc i canvia; el document de
  partida guarda els arguments de cada ordre, entre ells la seva clau quan en té una (`ATTACK_ENEMY`, ...).
- Les raons d'atac per sobre de 5: escrites només com a números.

## Com es va comprovar la lectura {#how-the-reading-was-checked}

La lectura es va comprovar amb repeticions públiques dels clients 1.12 i 2.4, cada valor amb una altra cosa
que la repetició dona una segona vegada:

- **Posicions:** cada tanc vist mai té una trajectòria a deu mostres per segon; les velocitats es mantenen
  dins del que pot fer un tanc; el heading coincideix amb la direcció del moviment a uns 0,02 rad; quan els
  resultats donen el lloc d'una mort, el lloc llegit aquí és a pocs metres.
- **El jugador que grava:** els trets i el dany fet llegits són iguals als valors dels resultats, a cada
  repetició comprovada.
- **Salut:** l'últim valor de salut llegit de cada tanc és igual al dels resultats; el dany rebut llegit no és
  mai més gran que el dels resultats. En la 2.4 sovint no s'envia el cop mortal a un tanc fora de la vista del
  client.
- **Impactes:** el dany d'un impacte és igual al canvi de salut en aquell moment a gairebé cada impacte.
- **Torreta:** en un tret, el heading del casc més el guinyol de la torreta apunta on va volar el traçador, dins
  d'uns 0,01 rad (mediana).
- **Morts i inici de la batalla:** dins d'un segon aproximadament del que diuen els resultats i l'arena.

Els tests construeixen repeticions amb la mateixa disposició, de manera que cap repetició real no es guarda en
aquest repositori.

**No comprovat:** clients anteriors a 1.12, repeticions de consola i de Blitz (jocs diferents), el Mir Tankov de
Lesta (`.mtreplay`), i els modes diferents de les batalles aleatòries i del tipus de batalla 20.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
