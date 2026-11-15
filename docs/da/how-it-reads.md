---
title: Sådan læses et replay
nav_order: 7
lang: da
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Sådan læses et replay {#how-it-reads-a-replay}

Et replay er en header af JSON-blokke og spillets pakkestrøm (formatnoter i
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Den første blok, i klartekst: kortet, klientversionen, den optagende spiller, serverens indstillinger og
  rosteren (`vehicles`: navn, hold, tank, nøglet efter køretøjets id).
- Den anden, når optagelsen varede til enden: resultatskærmen - hvert køretøjs linje (skud, træf,
  gennemslag, forvoldt, modtaget, blokeret og assisteret skade, spotting, xp, kreditter, præstationer ...),
  den optagende spillers detaljer pr. mål, kontoerne, kampens varighed, vinder og afslutningsårsag; i nogle
  tilstande den eneste fulde rosterliste (headeren på disse lister angiver kun det egne hold).
- Pakkestrømmen, zlib-komprimeret og Blowfish-krypteret med en nøgle, spillet bærer, og som fællesskabets
  værktøjer, der læser disse filer, har offentliggjort siden 2013.

**Positioner** er motorens positionsopdateringer: et køretøjs id, dets position og dets heading, fundet ud
fra deres form og ikke fra deres pakkenummer, så en patch, der nummererer dem om, ikke tømmer tabellen. De er
det, den optagende klient fik at vide: dets eget hold hele tiden, en fjende kun, mens den er spottet (eller
inden for klientens rækkevidde). Et køretøj, der aldrig er spottet, har ingen rækker. Et køretøjs rækker
holder op ved dets død.

**Resten af strømmen** - liv, skud, sporstof, eksplosioner, træf, kanonvinkler, arenaopdateringer - er
metodekald og egenskabsændringer på køretøjerne og på klientens avatar, nummereret efter spillets
definitionsfiler, som ændrer sig med patches (1.12 og 2.4 nummererer dem forskelligt). Hvert findes ud fra
formen af dets argumenter og hvordan de hænger sammen - se
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) -
og de fundne tal står i kampdokumentets `decoded`. Chat, kameratilstanden og klientens egne hændelser er
pakker for sig selv. Arenaopdateringer og klienthændelser er Python-pickles; de læses af en læser, der gør
hver klasse, de navngiver, til en inert stand-in og ikke kører noget.

Det, klienten fik at vide, er fuldstændigt for sit eget hold og delvist for fjender: deres skud, træf og
livsændringer er der, mens de var inden for rækkevidde.

**Kampens start** er det tidspunkt, arenaopdateringen siger, at kampperioden begyndte; i et replay uden den
er det første øjeblik, et køretøj bevæger sig.

**Dødsfald:** tidspunktet er arenaens drabsmeddelelse (1.x), ellers den livsændring, der afsluttede køretøjet,
ellers kampens start plus offerets `lifeTime` fra resultaterne (hele sekunder). Stedet er, hvor offeret sidst
blev set, når det var inden for fem sekunder af dets død; ellers, på 2.x-klienter, stedet resultaterne giver
(x og z, ingen højde), kun i kampdokumentet. En optagelse, der stoppede før slutningen, har ingen dødsfald.

**Ikke læst:**

- Spotting og minikortet: ikke i strømmen som hændelser for sig selv.
- Kanonens hævning i grader: strømmen har et trin mellem kanonens grænser, og grænserne står i spillets
  køretøjsfiler.
- Modulskade, mandskabsskader, forbrugsvarer og ammunition: kaldene, der bærer dem, kunne ikke skelnes fra
  hinanden alene på formen på tværs af 1.12 og 2.4.
- Entitetsoprettelsespakker ud over entiteten og dens type: de rummer hver egenskab ved et køretøj, der kommer
  ind i klientens udsyn på én gang, i en rækkefølge kun definitionsfilerne giver (gemt helt i sidecaren).
- Statiske kollisioner (træer, huse), den optagende spillers egen sigte- og fysikpakker.
- Kampchatkommandoernes numre som navne: nummereringen er spillets og ændrer sig; kampdokumentet beholder
  hver kommandos argumenter, blandt dem dens nøgle, hvor den har en (`ATTACK_ENEMY`, ...).
- Angrebsårsager over 5: skrevet kun som tal.

## Sådan blev læsningen kontrolleret {#how-the-reading-was-checked}

Læsningen blev kontrolleret på offentlige replays af klienterne 1.12 og 2.4, hver værdi mod noget, replayet
giver en anden gang:

- **Positioner:** hver tank, der nogensinde er set, har et spor med ti samples i sekundet; hastighederne holder
  sig inden for, hvad en tank kan; headingen stemmer med færdens retning inden for ca. 0,02 rad; hvor
  resultaterne giver et dødsfalds sted, ligger det sted, der læses her, inden for få meter af det.
- **Den optagende spiller:** skuddene og den forvoldte skade læst er lig resultaternes værdier, på hvert
  kontrolleret replay.
- **Liv:** hver tanks sidst læste livsværdi er lig resultaternes; den læste modtagne skade er aldrig mere end
  resultaternes. På 2.4 sendes det dødelige slag mod en tank uden for klientens udsyn ofte ikke.
- **Træf:** et træfs skade er lig livsændringen på det tidspunkt for næsten hvert træf.
- **Kanon og tårn:** ved et skud peger hovedets heading plus tårnets drejning dertil, hvor sporstoffet fløj,
  inden for ca. 0,01 rad (median).
- **Dødsfald og kampens start:** inden for ca. et sekund af, hvad resultaterne og arenaen siger.

Testene bygger replays efter det samme layout, så intet rigtigt replay gemmes i dette repository.

**Ikke kontrolleret:** klienter før 1.12, konsol- og Blitz-replays (andre spil), Lestas Mir Tankov
(`.mtreplay`), og andre tilstande end tilfældige kampe og kamptype 20.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
