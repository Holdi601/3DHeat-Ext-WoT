---
title: "Hvernig upptaka er lesin"
nav_order: 7
lang: is
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Hvernig upptaka er lesin {#how-it-reads-a-replay}

Upptaka er haus úr JSON-blokkum og pakkastraumur leiksins (sniðathugasemdir
í [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Fyrsta blokkin, ódulkóðuð: kortið, útgáfa biðlarans, upptökumaðurinn,
  stillingar þjónsins og listinn yfir þátttakendur (`vehicles`: nafn, lið, skriðdreki,
  lykluð með auðkenni farartækisins).
- Önnur, þegar upptakan entist til loka: niðurstöðuskjárinn -
  lína hvers farartækis (skot, högg, gegnumskot, skaði veittur, tekinn,
  hindraður og aðstoðaður, kortlagning (spotting), xp, credits, afrek...),
  smáatriði upptökumannsins á skotmark, reikningarnir, lengd leiksins,
  sigurvegari og ástæða loka; í sumum hömum eini fullkomni listinn yfir þátttakendur (haus
  þeirra telur aðeins eigið lið).
- Pakkastraumurinn, zlib-þjappaður og Blowfish-dulkóðaður með lykli sem
  leikurinn ber með sér, og samfélagsverkfærin sem lesa þessar skrár hafa birt
  síðan 2013.

**Stöður** eru stöðuuppfærslur vélarinnar: auðkenni farartækis, staða þess
og stefna, fundnar eftir lögun þeirra frekar en pakkanúmeri, svo uppfærsla sem
endurnúmerar þær tæmir ekki töfluna. Þær eru það sem upptökubiðlaranum var sagt:
eigið lið allan tímann, óvinur aðeins meðan hann var sénn (eða innan sviðs biðlarans). Farartæki sem
aldrei var sénn hefur engar raðir. Raðir farartækis stöðvast við dauða þess.

**Restin af straumnum** - heilsa, skot, ljósrákir (tracers), sprengingar, högg, byssuhorn,
uppfærslur vallar - eru aðferðakall og eiginleikabreytingar farartækjanna
og avatars biðlarans, númeruð af skilgreiningarskrám leiksins, sem
breytast með uppfærslum (1.12 og 2.4 númera þær ólíkt). Hvert er fundið eftir
lögun röksemda sinna og hvernig þær hanga saman - sjá
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - og númerin sem fundust
eru í `decoded` í leikjaskjalinu. Spjall, myndavélarhamurinn og eigin
atburðir biðlarans eru pakkar út af fyrir sig. Uppfærslur vallar og atburðir biðlarans eru Python
pickles; þau eru lesin af lesara sem breytir hverjum flokki sem þau nefna í
óvirkan staðgengil og keyrir ekkert.

Það sem biðlaranum var sagt er fullkomið fyrir eigið lið og hlutfallslegt fyrir
óvini: skot þeirra, högg og heilsubreytingar eru til staðar meðan þeir voru innan
sviðs.

**Upphaf bardagans** er þegar uppfærsla vallar segir að bardagatímabilið hafi hafist;
í upptöku án hennar, fyrsta stund sem nokkurt farartæki hreyfist.

**Dauðsföll:** tíminn er dráps-skilaboð vallarins (1.x), annars heilsubreytingin
sem endaði farartækið, annars upphaf bardagans plús `lifeTime` fórnarlambsins
úr niðurstöðunum (heilar sekúndur). Staðurinn er þar sem fórnarlambið sást síðast,
þegar það var innan fimm sekúndna frá dauða þess; annars, á 2.x biðlurum,
staðurinn sem niðurstöðurnar gefa (x og z, engin hæð), aðeins í leikjaskjalinu. Upptaka
sem stöðvaðist fyrir lokin hefur engin dauðsföll.

**Ekki lesið:**

- Kortlagning (spotting) og smákortið: ekki í straumnum sem eigin atburðir.
- Hæð byssunnar í gráðum: straumurinn hefur skref milli marka byssunnar,
  og mörkin eru í farartækisskrám leiksins.
- Skemmdir á einingum, áhafnarmeiðsli, birgðir og skotfæri: köllin sem
  bera þau var ekki hægt að greina í sundur eftir lögun einni saman milli 1.12 og 2.4.
- Einingarsköpunarpakkar umfram eininguna og tegund hennar: þeir geyma hvern
  eiginleika farartækis sem kemur inn í sjónsvið biðlarans í einu, í röð sem aðeins
  skilgreiningarskrárnar gefa (varðveitt í heild í hliðarskránni).
- Kyrrstæðir árekstrar (tré, hús), eigin miðunar- og eðlisfræðipakkar
  upptökumannsins.
- Skipanir bardagaspjalls sem nöfn: númerunin er leiksins og
  breytist; leikjaskjalið geymir röksemdir hverrar skipunar, þar á meðal lykil hennar
  þar sem hún hefur einn (`ATTACK_ENEMY`, ...).
- Árásarástæður yfir 5: skrifaðar sem tölur eingöngu.

## Hvernig lesturinn var athugaður {#how-the-reading-was-checked}

Lesturinn var athugaður á opinberum upptökum biðlara 1.12 og 2.4, hvert
gildi gegn einhverju sem upptakan gefur í annað sinn:

- **Stöður:** hver skriðdreki sem sást hefur feril á tíu sýnum á sekúndu;
  hraði helst innan þess sem skriðdreki getur; stefnan stemmir við
  stefnu ferðar innan um 0,02 rad; þar sem niðurstöðurnar gefa stað dauða
  er staðurinn sem er lesinn hér innan fárra metra frá honum.
- **Upptökumaðurinn:** skotin og skaðinn veittur sem eru lesin eru jöfn
  gildum niðurstaðnanna, á hverri upptöku sem var athuguð.
- **Heilsa:** síðasta heilsa hvers skriðdreka sem er lesin er jöfn niðurstöðunum; skaðinn
  tekinn sem er lesinn er aldrei meiri en niðurstaðnanna. Á 2.4 er banahöggið á
  skriðdreka utan sjónsviðs biðlarans oft ekki sent.
- **Högg:** skaði höggs er jafn heilsubreytingunni á þeirri stundu fyrir
  nær hvert högg.
- **Turn:** við skot bendir stefna skrokksins plús snúningur turnsins
  þangað sem ljósrákin flaug, innan um 0,01 rad (miðgildi).
- **Dauðsföll og upphaf bardagans:** innan um einnar sekúndu frá því sem
  niðurstöðurnar og völlurinn segja.

Prófanirnar smíða upptökur í sama útliti, svo engin raunveruleg upptaka er geymd í
þessari geymslu.

**Ekki athugað:** biðlarar fyrir 1.12, upptökur leikjatölva og Blitz (aðrir
leikir), Mir Tankov frá Lesta (`.mtreplay`), og hamir aðrir en random battles
og bardagategund 20.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
