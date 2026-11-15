---
title: "Så läser den en repris"
nav_order: 7
lang: sv
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Så läser den en repris {#how-it-reads-a-replay}

En repris är en header av JSON-block och spelets paketström (formatanteckningar i
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Det första blocket, i klartext: kartan, klientversionen, den inspelande spelaren, serverns
  inställningar och listan över fordon (`vehicles`: namn, lag, stridsvagn, nycklat på fordonets id).
- Det andra, när inspelningen varade till slutet: resultatskärmen - varje fordons rad (skott, träffar,
  genomslag, given och blockerad skada, upptäckt och assists, erfarenhet, krediter, utmärkelser...),
  den inspelande spelarens detaljer per mål, konton, matchens längd, vinnare och slutorsak; i en del
  lägen den enda kompletta listan över fordon (headern för dessa listar bara det egna laget).
- Paketströmmen, zlib-komprimerad och Blowfish-chifferskriven med en nyckel som spelet bär, vilken de
  gemenskapsverktyg som läser dessa filer har publicerat sedan 2013.

**Positioner** är motorns positionsuppdateringar: ett fordons id, dess position och dess kurs, funna
via deras form snarare än deras paketnummer, så en patch som numrerar om dem inte tömmer tabellen. De är
vad den inspelande klienten fick veta: dess eget lag hela tiden, en fiende bara medan den var upptäckt
(eller inom klientens räckvidd). Ett fordon som aldrig upptäcktes har inga rader. Ett fordons rader slutar
vid dess död.

**Resten av strömmen** - hälsa, skott, spårämnen, explosioner, träffar, kanonvinklar, arenauppdateringar -
är metodanrop och egenskapsändringar för fordonen och för klientens avatar, numrerade av spelets
definitionsfiler, som ändras med patcharna (1.12 och 2.4 numrerar dem olika). Varje anrop hittas via
formen på dess argument och hur de hänger ihop - se
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - och de
nummer som hittas står i matchdokumentets `decoded`. Chatt, kameraläget och klientens egna händelser är
egna paket. Arenauppdateringar och klienthändelser är Python-pickles; de läses av en läsare som gör varje
klass de nämner till en inert stand-in och inte kör något.

Det klienten fick veta är komplett för sitt eget lag och delvis för fiender: deras skott, träffar och
hälsoförändringar finns där medan de var inom räckhåll.

**Stridens start** är när arenauppdateringen säger att stridsperioden började; i en repris utan den är det
första ögonblick något fordon rör sig.

**Dödsfall:** tiden är arenans dödsmeddelande (1.x), annars hälsoförändringen som avslutade fordonet,
annars stridens start plus offrets `lifeTime` från resultaten (hela sekunder). Platsen är där offret sist
sågs, när det var inom fem sekunder från dess död; annars, på 2.x-klienter, platsen resultaten anger (x
och z, ingen höjd), bara i matchdokumentet. En inspelning som stoppade före slutet har inga dödsfall.

**Inte läst:**

- Upptäckt och minikartan: inte i strömmen som egna händelser.
- Kanonens höjd i grader: strömmen har ett steg mellan kanonens gränser, och gränserna finns i spelets
  fordonsfiler.
- Modulskada, besättningsskador, förbrukningsartiklar och ammunition: anropen som bär dem kunde inte
  skiljas åt enbart på form över 1.12 och 2.4.
- Entitetsskapande paket utöver entiteten och dess typ: de innehåller varje egenskap hos ett fordon som
  kommer in i klientens syn på en gång, i en ordning bara definitionsfilerna ger (behållna helt i sidofilen).
- Statiska kollisioner (träd, hus), den inspelande spelarens egna siktes- och fysikpaket.
- Chattens kommandonummer som namn: numreringen är spelets och ändras; matchdokumentet behåller varje
  kommandos argument, bland dem dess nyckel där den har en (`ATTACK_ENEMY`, ...).
- Angreppsorsaker över 5: skrivs bara som nummer.

## Så kontrollerades läsningen {#how-the-reading-was-checked}

Läsningen kontrollerades på publika repriser från klienterna 1.12 och 2.4, varje värde mot något som
repriset ger en andra gång:

- **Positioner:** varje stridsvagn som någonsin setts har en bana med tio mätpunkter per sekund;
  hastigheterna håller sig inom vad en stridsvagn kan göra; kursen stämmer med färdriktningen inom
  ungefär 0,02 rad; där resultaten anger ett dödsfalls plats ligger platsen som läses här inom några meter
  från den.
- **Den inspelande spelaren:** skotten och given skada läses lika med resultatens värden, på varje
  kontrollerad repris.
- **Hälsa:** varje stridsvagns sist lästa hälsa är lika med resultatens; given skada som läses är aldrig
  mer än resultatens. På 2.4 skickas ofta dödsslaget mot en stridsvagn utanför klientens syn inte.
- **Träffar:** en träffs skada är lika med hälsoförändringen i det ögonblicket för nästan varje träff.
- **Torn:** vid ett skott pekar skrovets kurs plus tornets gir dit spårämnet flög, inom ungefär 0,01 rad
  (median).
- **Dödsfall och stridens start:** inom ungefär en sekund från vad resultaten och arenan säger.

Testerna bygger repriser i samma layout, så ingen riktig repris sparas i det här arkivet.

**Inte kontrollerat:** klienter före 1.12, konsol- och Blitz-repriser (andra spel), Lesta:s Mir Tankov
(`.mtreplay`), och andra lägen än slumpstrider och stridstyp 20.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
