---
title: "Slik leser den en replay"
nav_order: 7
lang: no
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Slik leser den en replay {#how-it-reads-a-replay}

En replay er en header av JSON-blokker og spillets pakkestrøm (formatnotater i
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Den første blokken, i klartekst: kartet, klientversjonen, opptakspilotens spiller, serverens innstillinger og
  listen over deltakere (`vehicles`: navn, lag, tank, nøklet etter kjøretøyets ID).
- Den andre, når opptaket varte til slutten: resultatskjermen - hvert kjøretøys linje
  (skudd, treff, gjennomslag, skade gjort, mottatt, blokkert og assistert, spotting, xp,
  kreditter, prestasjoner ...), opptakspilotens detaljer per mål, kontoene, kampens varighet,
  vinner og årsak til slutten; i noen moduser den eneste fullstendige listen (headeren til
  disse listene viser bare ens eget lag).
- Pakkestrømmen, zlib-komprimert og Blowfish-kryptert med en nøkkel spillet bærer, som
  fellesskapets verktøy som leser disse filene har publisert siden 2013.

**Posisjoner** er motorens posisjonsoppdateringer: et kjøretøys ID, dets posisjon og dets
retning, funnet etter deres form i stedet for pakkenummeret, så en oppdatering som
nummererer dem på nytt ikke tømmer tabellen. De er det opptaksklienten ble fortalt: sitt eget
lag hele tiden, en fiende bare mens den er spottet (eller i klientens rekkevidde). Et kjøretøy
som aldri ble spottet, har ingen rader. Radene til et kjøretøy stopper ved dets død.

**Resten av strømmen** - helse, skudd, sporstoffer, eksplosjoner, treff, kanonvinkler,
arenaoppdateringer - er metodekall og egenskapsendringer på kjøretøyene og på klientens avatar,
nummerert etter spillets definisjonsfiler, som endres med oppdateringer (1.12 og 2.4 nummererer dem
forskjellig). Hver blir funnet etter formen på argumentene og hvordan de henger sammen - se
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - og tallene som
ble funnet, står i kampdokumentets `decoded`. Chat, kameramodus og klientens egne hendelser er
pakker for seg selv. Arenaoppdateringer og klienthendelser er Python-pickles; de leses av en leser som gjør
hver klasse de nevner om til en inert stand-in og kjører ingenting.

Det klienten ble fortalt, er fullstendig for sitt eget lag og delvis for fiender: deres skudd, treff og
helseendringer er der mens de var i rekkevidde.

**Slagets start** er når arenaoppdateringen sier at kampperioden begynte; i en replay uten den, det
første øyeblikket noen kjøretøy beveger seg.

**Dødsfall:** tiden er arenaens drapsmelding (1.x), ellers helseendringen som avsluttet kjøretøyet, ellers
slagets start pluss offerets `lifeTime` fra resultatene (hele sekunder). Stedet er der offeret sist ble sett,
når det var innen fem sekunder før dets død; ellers, på 2.x-klienter, stedet resultatene gir (x og z, ingen
høyde), bare i kampdokumentet. Et opptak som stoppet før slutten, har ingen dødsfall.

**Ikke lest:**

- Spotting og minikartet: ikke i strømmen som hendelser for seg selv.
- Kanonens hevning i grader: strømmen har et steg mellom kanonens grenser, og grensene står i spillets kjøretøyfiler.
- Skademoduler, mannskapsskader, forbruksvarer og ammunisjon: kallene som bærer dem kunne ikke skilles fra
  hverandre bare på form over 1.12 og 2.4.
- Opprettelsespakker for entiteter utover entiteten og dens type: de holder hver egenskap til et kjøretøy som kommer
  inn i klientens syn på én gang, i en rekkefølge bare definisjonsfilene gir (beholdt helt i sidefilen).
- Statiske kollisjoner (trær, hus), opptakspilotens egen sikting og fysikkpakker.
- Kommandonumre for chat i slaget som navn: nummereringen er spillets og endres; kampdokumentet beholder hver kommandos
  argumenter, blant dem nøkkelen der den har en (`ATTACK_ENEMY`, ...).
- Angrepsårsaker over 5: skrevet bare som tall.

## Hvordan lesingen ble kontrollert {#how-the-reading-was-checked}

Lesingen ble kontrollert på offentlige replayer fra klientene 1.12 og 2.4, hver verdi mot noe replayen
gir en annen gang:

- **Posisjoner:** hver tank som noen gang er sett, har et spor med ti samples i sekundet; farter holder seg
  innenfor det en tank kan; retningen stemmer med bevegelsesretningen til ca. 0,02 rad; der resultatene gir et
  dødsfalls sted, ligger stedet lest her innen noen få meter fra det.
- **Opptakspilotens:** skudd og gjort skade leses lik resultatenes verdier, på hver replay som ble kontrollert.
- **Helse:** hver tanks siste leste helse er lik resultatenes; mottatt skade som leses, er aldri mer enn resultatenes.
  På 2.4 sendes ofte det dødelige slaget mot en tank utenfor klientens syn ikke.
- **Treff:** et treffs skade er lik helseendringen i det øyeblikket for nesten hvert treff.
- **Tårn:** ved et skudd peker skrogets retning pluss tårnets gir dit sporstoffet fløy, innen ca. 0,01 rad (median).
- **Dødsfall og slagets start:** innen ca. ett sekund av det resultatene og arenaen sier.

Testene bygger replayer i samme oppsett, så ingen ekte replay ligger i dette depotet.

**Ikke kontrollert:** klienter før 1.12, konsoll- og Blitz-replayer (andre spill), Lestas Mir Tankov
(`.mtreplay`), og moduser utover tilfeldige slag og slagtype 20.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
