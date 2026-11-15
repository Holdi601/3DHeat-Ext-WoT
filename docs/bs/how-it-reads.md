---
title: "Kako čita replay"
nav_order: 7
lang: bs
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kako čita replay {#how-it-reads-a-replay}

Replay je zaglavlje JSON blokova i tok paketa igre (bilješke o formatu
u [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Prvi blok, otvoreno: mapa, verzija klijenta, igrač koji snima,
  postavke servera i spisak (`vehicles`: ime, tim, tenk,
  s ključem po id-u vozila).
- Drugi, kada je snimanje trajalo do kraja: ekran rezultata -
  red svakog vozila (hici, pogoci, probijanja, nanesena, primljena,
  blokirana i asistirana šteta, otkrivanje, xp, krediti, dostignuća...),
  lični detalji po meti igrača koji snima, računi, trajanje meča,
  pobjednik i razlog završetka; u nekim načinima jedini potpuni spisak (zaglavlje
  navodi samo vlastiti tim).
- Tok paketa, zlib-komprimiran i Blowfish-šifriran ključem koji
  igra nosi, a koji su zajednički alati što čitaju ove datoteke objavili
  od 2013.

**Pozicije** su ažuriranja pozicija engine-a: id vozila, njegova pozicija
i njegov heading, pronađeni po svom obliku, a ne po broju paketa, pa ih
patch koji renumeriše ne ispraznuje tabelu. To je ono što je rečeno klijentu
koji snima: njegov vlastiti tim cijelo vrijeme, neprijatelj samo dok je
otkriven (ili u dometu klijenta). Vozilo koje nikad nije otkriveno nema redova. Redovi
vozila staju s njegovom smrću.

**Ostatak toka** - zdravlje, hici, trasirke, eksplozije, pogoci, uglovi
topa, ažuriranja arene - su pozivi metoda i promjene svojstava vozila
i klijentovog avatara, numerirani definicijskim datotekama igre, koje se
mijenjaju s patchevima (1.12 i 2.4 ih numerišu različito). Svaki se nalazi
po obliku svojih argumenata i načinu na koji se uklapaju - vidi
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - a pronađeni brojevi
su u `decoded` dokumenta meča. Čet, način kamere i vlastiti događaji klijenta
su paketi za sebe. Ažuriranja arene i događaji klijenta su Python
pickleovi; čita ih čitač koji svaku klasu koju imenuju pretvara u
inertnu zamjenu i ne pokreće ništa.

Ono što je rečeno klijentu potpuno je za njegov vlastiti tim, a djelimično za
neprijatelje: njihovi hici, pogoci i promjene zdravlja tu su dok su bili u
dometu.

**Početak bitke** je kad ažuriranje arene kaže da je period bitke počeo;
u replayu bez njega, prvi trenutak kad se ijedno vozilo pomjeri.

**Smrti:** vrijeme je poruka arene o ubistvu (1.x), inače promjena zdravlja
koja je završila vozilo, inače početak bitke plus `lifeTime` žrtve
iz rezultata (cijele sekunde). Mjesto je ono gdje je žrtva zadnji put viđena,
kad je to bilo unutar pet sekundi od njene smrti; inače, na klijentima 2.x,
mjesto koje daju rezultati (x i z, bez visine), samo u dokumentu meča. Snimak
koji je stao prije kraja nema smrti.

**Ne čita se:**

- Otkrivanje i minimapa: nisu u toku kao vlastiti događaji.
- Elevacija topa u stepenima: tok ima korak između granica topa,
  a granice su u datotekama vozila igre.
- Oštećenje modula, povrede posade, potrošni materijal i municija: pozive
  koji ih nose nije bilo moguće razlikovati samo po obliku kroz 1.12 i 2.4.
- Paketi stvaranja entiteta izvan entiteta i njegovog tipa: drže svako
  svojstvo vozila koje ulazi u vidokrug klijenta odjednom, redoslijedom koji daju
  samo definicijske datoteke (čuvaju se cijeli u sidecar datoteci).
- Statične kolizije (drveće, kuće), vlastito nišanjenje igrača koji snima i
  paketi fizike.
- Brojevi naredbi četa bitke kao imena: numeracija je igre i
  mijenja se; dokument meča čuva argumente svake naredbe, među njima njen ključ
  gdje ga ima (`ATTACK_ENEMY`, ...).
- Razlozi napada iznad 5: pišu se samo kao brojevi.

## Kako je čitanje provjereno {#how-the-reading-was-checked}

Čitanje je provjereno na javnim replayevima klijenata 1.12 i 2.4, svaka
vrijednost prema nečemu što replay daje drugi put:

- **Pozicije:** svaki ikad viđeni tenk ima stazu od deset uzoraka u sekundi;
  brzine ostaju unutar onoga što tenk može; heading se slaže sa
  smjerom kretanja do oko 0,02 rad; gdje rezultati daju mjesto smrti,
  ovdje pročitano mjesto je unutar nekoliko metara od njega.
- **Igrač koji snima:** pročitani hici i nanesena šteta jednaki su
  vrijednostima iz rezultata, na svakom provjerenom replayu.
- **Zdravlje:** zadnje pročitano zdravlje svakog tenka jednako je onom iz rezultata; pročitana primljena
  šteta nikad nije veća od one iz rezultata. Na 2.4 smrtonosni udarac po
  tenku izvan vidokruga klijenta često se ne šalje.
- **Pogoci:** šteta pogotka jednaka je promjeni zdravlja u tom trenutku za
  gotovo svaki pogodak.
- **Kupola:** pri hicu, heading trupa plus yaw kupole pokazuje
  kamo je trasirka letjela, unutar oko 0,01 rad (medijan).
- **Smrti i početak bitke:** unutar oko sekunde od onoga što
  rezultati i arena kažu.

Testovi grade replayeve u istom rasporedu, pa se nijedan pravi replay ne čuva u
ovom repozitoriju.

**Nije provjereno:** klijenti prije 1.12, konzolni i Blitz replayevi (druge
igre), Lestin Mir Tankov (`.mtreplay`) i načini osim nasumičnih bitaka
i tipa bitke 20.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
