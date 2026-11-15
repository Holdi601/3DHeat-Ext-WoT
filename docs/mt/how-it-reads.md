---
title: "Kif taqra ripetizzjoni"
nav_order: 7
lang: mt
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kif taqra ripetizzjoni {#how-it-reads-a-replay}

Ripetizzjoni hija header ta' blokok JSON u l-fluss tal-pakketti tal-logħba (noti
dwar il-format f'[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- L-ewwel blokk, bla ċifrar: il-mappa, il-verżjoni tal-klijent, il-plejer li
  rreġistra, is-settings tas-server u r-roster (`vehicles`: isem, tim, tank,
  bl-id tal-vettura bħala ċavetta).
- It-tieni, meta r-reġistrazzjoni damet sa tmiem il-battalja: l-iskrin tar-riżultati -
  il-linja ta' kull vettura (sparaturi, daqqiet, penetrazzjonijiet, ħsara magħmula,
  riċevuta, imblukkata u megħjuna, spotting, xp, krediti, kisbiet...), id-dettalji
  għal kull mira tal-plejer li rreġistra, il-kontijiet, it-tul tal-partita, ir-rebbieħ
  u r-raġuni tat-tmiem; f'xi modalitajiet l-uniku roster sħiħ (il-header ta' dawk
  jelenka biss it-tim tiegħu).
- Il-fluss tal-pakketti, ikkompressat b'zlib u ċifrat b'Blowfish b'ċavetta li
  tġorr il-logħba, u li l-għodod tal-komunità li jaqraw dawn il-fajls ippubblikaw
  mill-2013.

**Il-pożizzjonijiet** huma l-aġġornamenti tal-pożizzjoni tal-magna: l-id ta' vettura,
il-pożizzjoni tagħha u d-direzzjoni tagħha, misjuba mill-forma tagħhom u mhux min-numru
tal-pakkett, biex patch li jibdel in-numri ma jħallix it-tabella vojta. Huma dak li l-klijent
li rreġistra ntqal: it-tim tiegħu kollu, l-għadu biss waqt li ġie spotted (jew fil-firxa tal-klijent).
Vettura li ma ġietx spotted qatt m'għandha ringieli. Ir-ringieli ta' vettura jieqfu
mal-mewt tagħha.

**Il-bqija tal-fluss** - saħħa, sparaturi, tracers, splużjonijiet, daqqiet, angoli
tal-kanun, aġġornamenti tal-arena - huma sejħiet ta' metodi u bidliet fi proprjetajiet
tal-vetturi u tal-avatar tal-klijent, innumerati mill-fajls tad-definizzjoni tal-logħba,
li jinbidlu mal-patches (1.12 u 2.4 jinnumeraw differenti). Kull wieħed jinstab
mill-forma tal-argumenti tiegħu u kif jingħaqdu flimkien - ara
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - u n-numri misjuba
jinsabu fid-`decoded` tad-dokument tal-partita. Iċ-chat, il-modalità tal-kamera u l-avvenimenti
proprji tal-klijent huma pakketti għalihom. L-aġġornamenti tal-arena u l-avvenimenti tal-klijent
huma Python pickles; jinqraw minn qarrej li jbiddel kull klassi li jsemmu f'sostitut inerti
u ma jħaddem xejn.

Dak li l-klijent ġie mgħarraf huwa komplut għat-tim tiegħu u parzjali għall-għedewwa:
is-sparaturi, id-daqqiet u l-bidliet fis-saħħa tagħhom jinsabu hemm waqt li kienu fil-firxa.

**Il-bidu tal-battalja** huwa meta l-aġġornament tal-arena jgħid li beda l-perjodu
tal-battalja; f'ripetizzjoni mingħajru, l-ewwel mument li xi vettura tiċċaqlaq.

**Imwiet:** il-ħin huwa l-messaġġ tal-qtil tal-arena (1.x), inkella l-bidla fis-saħħa
li temmet il-vettura, inkella l-bidu tal-battalja flimkien mal-`lifeTime` tal-vittma
mir-riżultati (sekondi sħaħ). Il-post huwa fejn il-vittma dehret l-aħħar, meta dan kien
fi żmien ħames sekondi mill-mewt tagħha; inkella, fuq klijenti 2.x, il-post li jagħtu
r-riżultati (x u z, mingħajr għoli), fid-dokument tal-partita biss. Reġistrazzjoni
li waqfet qabel it-tmiem m'għandha l-ebda mewt.

**Mhux moqri:**

- Spotting u l-minimap: mhumiex fil-fluss bħala avvenimenti għalihom.
- L-elevazzjoni tal-kanun f'gradi: il-fluss għandu pass bejn il-limiti tal-kanun,
  u l-limiti jinsabu fil-fajls tal-vetturi tal-logħba.
- Ħsara fil-moduli, korrimenti tal-ekwipaġġ, consumables u munizzjon: is-sejħiet li
  jġorruhom ma setgħux jiġu mifrudin mill-forma biss fuq 1.12 u 2.4.
- Pakketti tal-ħolqien tal-entitajiet lil hinn mill-entità u t-tip tagħha: ikollhom
  kull proprjetà ta' vettura li tidħol fil-vista tal-klijent f'daqqa, f'ordni li
  tagħtiha biss il-fajls tad-definizzjoni (miżmuma sħaħ fis-sidecar).
- Kolliżjonijiet statiċi (siġar, djar), l-aiming u l-pakketti tal-fiżika tal-plejer
  li rreġistra.
- In-numri tal-kmandi taċ-chat tal-battalja bħala ismijiet: in-numerazzjoni hija tal-logħba
  u tinbidel; id-dokument tal-partita jżomm l-argumenti ta' kull kmand, fosthom iċ-ċavetta
  tiegħu meta jkollu (`ATTACK_ENEMY`, ...).
- Raġunijiet tal-attakk 'l fuq minn 5: miktuba bħala numri biss.

## Kif ġie kkontrollat il-qari {#how-the-reading-was-checked}

Il-qari ġie kkontrollat fuq ripetizzjonijiet pubbliċi ta' klijenti 1.12 u 2.4, kull
valur kontra xi ħaġa li r-ripetizzjoni tagħti darba oħra:

- **Pożizzjonijiet:** kull tank li dehret qatt għandu mogħdija b'għaxar kampjuni
  fit-tieni; il-veloċitajiet jibqgħu fi ħdan dak li tank jista' jagħmel; id-direzzjoni
  taqbel mad-direzzjoni tal-vjaġġ sa madwar 0.02 rad; fejn ir-riżultati jagħtu l-post
  ta' mewt, il-post moqri hawn huwa fi ftit metri minnu.
- **Il-plejer li rreġistra:** is-sparaturi u l-ħsara magħmula moqrija huma ugwali
  għall-valuri tar-riżultati, fuq kull ripetizzjoni kkontrollata.
- **Saħħa:** l-aħħar saħħa moqrija ta' kull tank hija ugwali għal dik tar-riżultati;
  il-ħsara riċevuta moqrija qatt ma hija aktar minn dik tar-riżultati. Fuq 2.4 id-daqqa li
  toqtol tank barra mill-vista tal-klijent ħafna drabi ma tinbagħatx.
- **Daqqiet:** il-ħsara ta' daqqa hija ugwali għall-bidla fis-saħħa f'dak il-mument
  għal kważi kull daqqa.
- **Turret:** fi sparatura, id-direzzjoni tal-iskoss flimkien mal-yaw tat-turret tipponta
  lejn fejn tajjar it-tracer, sa madwar 0.01 rad (medjan).
- **Imwiet u l-bidu tal-battalja:** sa madwar sekonda minn dak li jgħidu r-riżultati
  u l-arena.

It-testijiet jibnu ripetizzjonijiet bl-istess layout, għalhekk ebda ripetizzjoni vera
ma tinżamm f'dan ir-repożitorju.

**Mhux ikkontrollat:** klijenti qabel 1.12, ripetizzjonijiet tal-console u ta' Blitz
(logħob differenti), Mir Tankov ta' Lesta (`.mtreplay`), u modalitajiet minbarra
l-battaljiet każwali u t-tip ta' battalja 20.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
