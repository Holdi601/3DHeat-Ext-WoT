---
title: "Hoe het een replay leest"
nav_order: 7
lang: "nl"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Hoe het een replay leest {#how-it-reads-a-replay}

Een replay is een kop van JSON-blokken en de pakketstroom van het spel (notities over het formaat staan in
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Het eerste blok, ongeversleuteld: de kaart, de clientversie, de opnemende speler, de instellingen van de
  server en de lijst van deelnemers (`vehicles`: naam, team, tank, gesorteerd op het id van het voertuig).
- Het tweede, wanneer de opname tot het einde duurde: het resultatenscherm - de resultaatregel van elk
  voertuig (schoten, treffers, doordringingen, toegebrachte, ontvangen, geblokkeerde en geassisteerde schade,
  spotten, xp, credits, prestaties...), de details per doel van de opnemende speler, de accounts, de duur van
  de wedstrijd, de winnaar en de reden van afloop; in sommige modi de enige volledige lijst van deelnemers (de kop van
  die lijsten bevat alleen het eigen team).
- De pakketstroom, met zlib gecomprimeerd en met Blowfish versleuteld met een sleutel die het spel meedraagt,
  die de communitytools die deze bestanden lezen sinds 2013 hebben gepubliceerd.

**Posities** zijn de positie-updates van de engine: het id van een voertuig, zijn positie en zijn heading,
gevonden aan hun vorm en niet aan hun pakketnummer, zodat een patch die ze hernummert de tabel niet leegmaakt.
Het zijn de gegevens die de opnemende client kreeg: het eigen team de hele tijd, een vijand alleen zolang
hij gespot was (of in het bereik van de client). Een voertuig dat nooit gespot werd, heeft geen rijen. Rijen
van een voertuig stoppen bij zijn dood.

**De rest van de stroom** - gezondheid, schoten, tracers, explosies, treffers, kanonshoeken, arena-updates -
zijn aanroepen van methoden en wijzigingen van eigenschappen van de voertuigen en van de avatar van de client,
genummerd volgens de definitiebestanden van het spel, die met patches veranderen (1.12 en 2.4 nummeren ze
verschillend). Elk wordt gevonden aan de vorm van zijn argumenten en hoe die samenhangen - zie
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - en de gevonden
nummers staan in `decoded` van het wedstrijddocument. Chat, de cameramodus en de eigen gebeurtenissen van de
client zijn eigen pakketten. Arena-updates en clientgebeurtenissen zijn Python-pickles; ze worden gelezen door een
lezer die elke klasse die ze noemen omzet in een inert naamloos stand-in en niets uitvoert.

Wat de client te horen kreeg, is volledig voor het eigen team en gedeeltelijk voor vijanden: hun schoten, treffers en
gezondheidswijzigingen staan erin zolang ze binnen bereik waren.

**Het begin van het gevecht** is het moment waarop de arena-update zegt dat de gevechtsperiode begon; in een
replay zonder die update is het het eerste moment dat een voertuig beweegt.

**Doden:** de tijd is het killbericht van de arena (1.x), anders de gezondheidswijziging die het voertuig beëindigde,
anders het begin van het gevecht plus de `lifeTime` van het slachtoffer uit de resultaten (hele seconden). De plaats is
waar het slachtoffer het laatst gezien werd, als dat binnen vijf seconden voor zijn dood was; anders, bij 2.x-clients,
de plaats die de resultaten geven (x en z, zonder hoogte), alleen in het wedstrijddocument. Een opname die vóór het
einde stopte, heeft geen doden.

**Niet gelezen:**

- Spotten en de minimap: niet in de stroom als eigen gebeurtenissen.
- De hoogte van het kanon in graden: de stroom heeft een stap tussen de grenzen van het kanon, en die grenzen staan in de
  voertuigbestanden van het spel.
- Schade aan modules, bemanningsverwondingen, verbruiksgoederen en munitie: de aanroepen die ze dragen konden over 1.12 en 2.4
  heen niet alleen aan hun vorm onderscheiden worden.
- Pakketten van entiteitscreatie buiten de entiteit en zijn type: ze bevatten elke eigenschap van een voertuig dat in het
  zicht van de client komt, in één keer, in een volgorde die alleen de definitiebestanden geven (volledig bewaard in de sidecar).
- Statische botsingen (bomen, huizen), het eigen richten en de fysicapakketten van de opnemende speler.
- Nummers van commando's uit de gevechtschat als namen: de nummering is van het spel en verandert; het wedstrijddocument bewaart
  de argumenten van elk commando, daaronder de sleutel waar het er een heeft (`ATTACK_ENEMY`, ...).
- Aanvalsredenen boven 5: alleen als nummer geschreven.

## Hoe de lezing gecontroleerd is {#how-the-reading-was-checked}

De lezing is gecontroleerd op openbare replays van clients 1.12 en 2.4, elke waarde tegen iets dat de replay
een tweede keer geeft:

- **Posities:** elke tank die ooit gezien werd, heeft een spoor met tien samples per seconde; snelheden blijven binnen wat een
  tank kan; de heading komt overeen met de richting van de beweging tot ongeveer 0,02 rad; waar de resultaten de plaats van een
  dood geven, ligt de hier gelezen plaats binnen enkele meters ervan.
- **De opnemende speler:** de schoten en de toegebrachte schade die gelezen zijn, zijn gelijk aan de waarden van de resultaten,
  bij elke gecontroleerde replay.
- **Gezondheid:** de laatst gelezen gezondheid van elke tank is gelijk aan die van de resultaten; de gelezen ontvangen schade
  is nooit meer dan die van de resultaten. Op 2.4 wordt de dodelijke klap op een tank buiten het zicht van de client vaak niet gestuurd.
- **Treffers:** de schade van een treffer is bij bijna elke treffer gelijk aan de gezondheidswijziging op dat moment.
- **Toren:** bij een schot wijst de heading van de romp plus de gier van de toren waarheen de tracer vloog, binnen ongeveer 0,01 rad (mediaan).
- **Doden en het begin van het gevecht:** binnen ongeveer een seconde van wat de resultaten en de arena zeggen.

De tests bouwen replays in dezelfde indeling, dus er wordt geen echte replay in deze repository bewaard.

**Niet gecontroleerd:** clients vóór 1.12, replays van console en Blitz (andere spellen), Mir Tankov van Lesta
(`.mtreplay`), en modi anders dan willekeurige gevechten en gevechtstype 20.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
