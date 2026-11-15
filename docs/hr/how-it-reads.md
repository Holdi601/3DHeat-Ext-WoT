---
title: Kako se snimka čita
nav_order: 7
lang: "hr"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kako pretvarač čita snimku {#how-it-reads-a-replay}

Snimka je zaglavlje od JSON blokova i tok paketa igre (bilješke o formatu u
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Prvi blok, otvoreno: karta, verzija klijenta, igrač koji snima, postavke poslužitelja i popis
  (`vehicles`: ime, tim, tenk, ključ je id vozila).
- Drugi, kad je snimanje trajalo do kraja: ekran rezultata - redak svakog vozila (hici, pogoci,
  probijanja, nanesena, primljena, blokirana i asistirana šteta, otkrivanje, iskustvo, krediti,
  postignuća...), osobne pojedinosti igrača koji snima po meti, računi, trajanje bitke, pobjednik i razlog
  završetka; u nekim načinima jedini potpuni popis (zaglavlje tih popisa navodi samo vlastiti tim).
- Tok paketa, zlib-komprimiran i Blowfish-šifriran ključem koji nosi igra, koji zajednički alati za
  čitanje ovih datoteka objavljuju od 2013.

**Položaji** su ažuriranja položaja iz motora: id vozila, njegov položaj i smjer, nađeni prema obliku, a ne
prema broju paketa, pa zakrpa koja ih prenumerira ne isprazni tablicu. Oni su ono što je klijent koji snima
dobio: vlastiti tim cijelo vrijeme, a neprijatelj samo dok je uočen (ili u dometu klijenta). Vozilo koje nikad
nije uočeno nema redaka. Redci vozila prestaju njegovom smrću.

**Ostatak toka** - zdravlje, hici, tragovi, eksplozije, pogoci, kutovi topa, ažuriranja arene - su pozivi metoda i
promjene svojstava vozila i avatara igrača, numerirani definicijskim datotekama igre, koje se mijenjaju s
zakrpama (1.12 i 2.4 ih numeriraju različito). Svaki se nalazi prema obliku svojih argumenata i tome kako se
drže zajedno - vidi [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) -
a nađeni brojevi su u `decoded` dokumenta meča. Razgovor, način kamere i vlastiti događaji klijenta su zasebni
paketi. Ažuriranja arene i događaji klijenta su Python pickle; čita ih čitač koji svaku klasu koju imenuju pretvara
u neaktivnu zamjenu i ništa ne izvršava.

Ono što je klijentu rečeno potpuno je za vlastiti tim, a djelomično za neprijatelje: njihovi hici, pogoci i promjene
zdravlja tu su dok su bili u dometu.

**Početak bitke** je trenutak kad ažuriranje arene kaže da je razdoblje bitke počelo; u snimci bez njega, prvi
trenutak kad se bilo koje vozilo pomakne.

**Smrti:** vrijeme je poruka ubojstva arene (1.x), inače promjena zdravlja koja je završila vozilo, inače početak
bitke plus `lifeTime` žrtve iz rezultata (cijele sekunde). Mjesto je gdje je žrtva zadnji put viđena, kad je to bilo
unutar pet sekundi od njezine smrti; inače, na klijentima 2.x, mjesto koje daju rezultati (x i z, bez visine), samo u
dokumentu meča. Snimka koja je stala prije kraja nema smrti.

**Nije čitano:**

- Uočavanje i mini-karta: nisu u toku kao vlastiti događaji.
- Kut elevacije topa u stupnjevima: tok ima korak između granica topa, a granice su u vozilnim datotekama igre.
- Oštećenja modula, ozljede posade, potrošni predmeti i streljivo: pozivi koji ih nose nisu se mogli razlikovati
  samo po obliku kroz 1.12 i 2.4.
- Paketi stvaranja entiteta izvan entiteta i njegova tipa: nose svako svojstvo vozila koje ulazi u pogled klijenta
  odjednom, u redoslijedu koji daju samo definicijske datoteke (sačuvani cijeli u pomoćnoj datoteci).
- Statični sudari (drveće, kuće), vlastito ciljanje igrača koji snima i paketi fizike.
- Brojevi naredbi bitke u razgovoru kao nazivi: numeriranje je igrino i mijenja se; dokument meča čuva argumente
  svake naredbe, među njima njezin ključ gdje ga ima (`ATTACK_ENEMY`, ...).
- Razlozi napada iznad 5: zapisani samo kao brojevi.

## Kako je čitanje provjereno {#how-the-reading-was-checked}

Čitanje je provjereno na javnim snimkama klijenata 1.12 i 2.4, svaka vrijednost prema nečemu što snimka
daje drugi put:

- **Položaji:** svaki tenk ikad viđen ima putanju s deset uzoraka u sekundi; brzine ostaju unutar onoga što
  tenk može; smjer se slaže sa smjerom kretanja unutar oko 0,02 rad; gdje rezultati daju mjesto smrti, ovdje
  pročitano mjesto je unutar nekoliko metara od njega.
- **Igrač koji snima:** hici i nanesena šteta pročitani su jednaki vrijednostima iz rezultata, na svakoj
  provjerenoj snimci.
- **Zdravlje:** zadnje pročitano zdravlje svakog tenka jednako je onom iz rezultata; pročitana primljena
  šteta nikad nije veća od one iz rezultata. Na 2.4 zadnji udarac tenku izvan pogleda klijenta često nije
  poslan.
- **Pogoci:** šteta pogotka jednaka je promjeni zdravlja u tom trenutku za gotovo svaki pogodak.
- **Toranj:** pri hicu, smjer trupa plus zakret tornja pokazuje kamo je trag letio, unutar oko 0,01 rad (medijan).
- **Smrti i početak bitke:** unutar otprilike jedne sekunde od onoga što kažu rezultati i arena.

Testovi grade snimke istim rasporedom, pa ni jedna prava snimka nije sačuvana u ovom repozitoriju.

**Nije provjereno:** klijenti prije 1.12, konzolne i Blitz snimke (druge igre), Lestin Mir Tankov (`.mtreplay`),
i načini osim slučajnih bitaka i vrste bitke 20.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
