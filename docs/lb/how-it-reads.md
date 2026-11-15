---
title: "Wéi e Replay gelies gëtt"
nav_order: 7
lang: "lb"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Wéi e Replay gelies gëtt {#how-it-reads-a-replay}

E Replay ass en Header aus JSON-Blöck an dem Paketstroum vum Spill (Formatnotizen
an [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Den éischte Block, am Kloren: d'Kaart, d'Clientversioun, den opuelende
  Spiller, d'Astellunge vum Server an d'Roster (`vehicles`: Numm, Team, Panzer,
  mat der ID vum Gefier als Schlëssel).
- Deen zweeten, wann d'Opnam bis zum Enn gedauert huet: de Resultater-Ecran -
  d'Zeil vun all Gefier (Schëss, Treffer, Duerchschléi, ausgedeelte, kritten,
  geblockten an assistéierte Schued, Spotting, xp, Credits, Auszeechnungen...), d'
  Detailer pro Zil vum opuelende Spiller, d'Konten, d'Längt vum Match,
  de Gewënner an de Grond vum Enn; a verschiddene Modi déi eenzeg komplett Roster (den Header
  vun deene lëscht nëmmen dat eegent Team).
- De Paketstroum, mat zlib komprimiert a mat Blowfish chiffréiert, mat engem Schlëssel, deen d'
  Spill mat sech dréit, dee Communautéitstools, déi dës Dateien liesen, zënter 2013
  verëffentlecht hunn.

**Positioune** sinn d'Positiouns-Updates vun der Engine: d'ID vun engem Gefier, seng Positioun
a säin Heading, erkannt un hirer Form amplaz un hirer Paketnummer, sou datt e Patch, deen se
nei nummeréiert, d'Tabell net eidel mécht. Si sinn dat, wat dem opuelende Client gesot gouf: säin
eegent Team duerchgängeg, e Feind nëmmen, wann en entdeckt war (oder an der Reechwäit vum Client). E Gefier, dat ni
entdeckt gouf, huet keng Zeilen. D'Zeile vun engem Gefier héieren bei sengem Doud op.

**De Rescht vum Stroum** - Liewen, Schëss, Leuchtspuren, Explosiounen, Treffer, Kanounwénkel,
Arena-Updates - sinn Methodenopruff a Propriétéitsännerunge vun de Gefierer
an vum Avatar vum Client, nummeréiert duerch d'Definitiounsdateie vum Spill, déi
sech mat Patche änneren (1.12 an 2.4 nummeréieren se anescht). All gëtt un der
Form vu sengen Argumenter erkannt, a wéi si zesummehänken - kuck
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - an déi fonnte Nummere
stinn am `decoded` vum Match-Dokument. Chat, de Kameramodus an dem Client seng eege
Evenementer si Pakete fir sech. Arena-Updates a Client-Evenementer sinn Python-
Pickles; si ginn vun engem Reader gelies, deen all Klass, déi si nennen, an en
inerte Stellvertrieder verwandelt a näischt ausféiert.

Wat dem Client gesot gouf, ass komplett fir säin eegent Team a partiell fir
Feinde: hir Schëss, Treffer a Liewensännerunge sinn do, solaang si an der
Reechwäit waren.

**Den Ufank vum Gefecht** ass, wann d'Arena-Update seet, datt d'Gefechtsperiod ugefaang huet;
an engem Replay ouni se dee Moment, wou d'éischt Gefier beweegt gëtt.

**Doudeger:** d'Zäit ass d'Kill-Message vun der Arena (1.x), soss d'Liewensännerung,
déi d'Gefier beendegt huet, soss den Ufank vum Gefecht plus dem Affer säin `lifeTime`
aus de Resultater (ganz Sekonnen). D'Plaz ass, wou d'Affer zuletzt gesi gouf,
wann dat bannent fënnef Sekonne vu sengem Doud war; soss, op 2.x-Clienten, d'
Plaz, déi d'Resultater ginn (x an z, keng Héicht), nëmmen am Match-Dokument. Eng Opnam,
déi virum Enn opgehalen huet, huet keng Doudeger.

**Net gelies:**

- Spotting an d'Minikaart: net als eege Evenementer am Stroum.
- D'Elevatioun vun der Kanoun a Grad: de Stroum huet e Schrëtt tëscht de Limite vun der
  Kanoun, an d'Limite sinn an de Gefierdateie vum Spill.
- Modulschued, Verletzunge vun der Crew, Verbrauchsgidder a Munitioun: d'Opruffer, déi
  se droen, konnten iwwer 1.12 an 2.4 hannen net un der Form eleng ennerscheet ginn.
- Entitéit-Erstellungspakete iwwer d'Entitéit a säin Typ eraus: si halen all
  Propriétéit vun engem Gefier, dat an de Bléck vum Client kënnt, op eemol, an enger Reiefolleg, déi
  nëmmen d'Definitiounsdateie ginn (ganz an der Niewendatei behalen).
- Statesch Kollisiounen (Beem, Haiser), dem opuelende Spiller säin eegent Zielen a
  seng Physikpakete.
- Chat-Kommandonummere als Nimm: d'Nummeréierung ass dem Spill seng a
  ännert sech; d'Match-Dokument hält d'Argumenter vun all Kommando, ënnert hinnen säi Schlëssel,
  wou en een huet (`ATTACK_ENEMY`, ...).
- Ugrëffsgrënn iwwer 5: nëmmen als Zuelen geschriwwen.

## Wéi d'Liese gepréift gouf {#how-the-reading-was-checked}

D'Liese gouf op ëffentleche Replays vun den Clienten 1.12 an 2.4 gepréift, all
Wäert géint eppes, wat de Replay en zweet Kéier gëtt:

- **Positiounen:** all Panzer, dee jee gesi gouf, huet eng Spur mat zéng Echantillonen d'Sekonn;
  Geschwindegkeete bleiwen bannent deem, wat e Panzer kann; d'Heading stëmmt mat der
  Beweegungsrichtung bis op ongeféier 0.02 rad iwwereneen; wou d'Resultater d'Plaz vun engem Doud
  ginn, ass déi hei gelies Plaz bannent e puer Meter dovun.
- **Den opuelende Spiller:** déi gelies Schëss an de gelies ausgedeelte Schued sinn
  gläich wéi d'Wäerter vun de Resultater, op all gepréiften Replay.
- **Liewen:** dat lescht gelies Liewe vun all Panzer ass gläich wéi dat vun de Resultater; de
  gelies kritte Schued ass ni méi wéi dee vun de Resultater. Op 2.4 gëtt den Doudesschlag op e
  Panzer ausserhalb vum Bléck vum Client dacks net geschéckt.
- **Treffer:** de Schued vun engem Treffer ass gläich wéi d'Liewensännerung an deem Moment bei
  bal all Treffer.
- **Turm:** bei engem Schoss weist dem Rumpf säin Heading plus dem Turm säi Yaw dohin, wou
  d'Leuchtspur geflunn ass, bannent ongeféier 0.01 rad (Median).
- **Doudeger an den Ufank vum Gefecht:** bannent ongeféier enger Sekonn vun deem, wat d'
  Resultater an d'Arena soen.

D'Tester bauen Replays an der selwechter Layout, dofir gëtt kee richtege Replay an
dësem Repository behalen.

**Net gepréift:** Clienten virun 1.12, Konsol- a Blitz-Replays (aner
Spiller), Lesta säi Mir Tankov (`.mtreplay`), a Modi aner wéi Zoufallsgefechter
a Gefechtstyp 20.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
