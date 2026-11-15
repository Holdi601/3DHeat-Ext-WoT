---
title: Miten replay luetaan
nav_order: 7
lang: fi
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Miten replay luetaan {#how-it-reads-a-replay}

Replay on JSON-lohkojen otsikko ja pelin paketti­virta (formaattihuomiot:
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Ensimmäinen lohko selkokielisenä: kartta, asiakasversio, tallentava pelaaja, palvelimen asetukset ja
  luettelo (`vehicles`: nimi, joukkue, panssarivaunu, avaimena ajoneuvon tunnus).
- Toinen, kun tallennus kesti loppuun asti: tulosnäkymä, eli jokaisen ajoneuvon rivi (laukaukset, osumat,
  läpäisyt, aiheutettu, vastaanotettu, estetty ja avustettu vahinko, tähystys, kokemus, hopea, saavutukset ...),
  tallentavan pelaajan yksityiskohdat kohteittain, tilit, ottelun kesto, voittaja ja lopetussyy; joissain
  tiloissa ainoa täydellinen luettelo (niiden luettelojen otsikko luettelee vain oman joukkueen).
- Paketti­virta, zlib-pakattuna ja Blowfish-salattuna pelin mukana tulevalla avaimella, jonka replayt lukevat
  yhteisön työkalut ovat julkaisseet vuodesta 2013.

**Sijainnit** ovat moottorin sijaintipäivityksiä: ajoneuvon tunnus, sen sijainti ja sen suunta, tunnistettuna
muodostaan eikä paketin numerostaan, joten paikka, joka numeroi ne uudelleen, ei tyhjennä taulukkoa. Ne ovat sitä,
mitä tallentava asiakas sai tietää: oman joukkueensa koko taistelun ajan, vihollisen vain silloin kun se oli
havaittu (tai asiakkaan etäisyydellä). Ajoneuvo, jota ei koskaan havaittu, ei saa rivejä. Ajoneuvon rivit päättyvät
sen kuolemaan.

**Virran loput** (terveys, laukaukset, luotisuorat, räjähdykset, osumat, tykin kulmat, areenan päivitykset) ovat
ajoneuvojen ja asiakkaan avatarin metodikutsuja ja ominaisuuksien muutoksia, numeroituina pelin määritystiedostojen
mukaan; ne muuttuvat päivitysten mukana (1.12 ja 2.4 numeroivat ne eri tavoin). Jokainen löydetään argumenttiensa
muodon ja niiden keskinäisen yhteyden perusteella; katso
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py), ja löydetyt
numerot ovat ottelun asiakirjan `decoded`-kohdassa. Chat, kameratila ja asiakkaan omat tapahtumat ovat omia
pakettejaan. Areenan päivitykset ja asiakkaan tapahtumat ovat Python-pickle-tiedostoja; ne luetaan lukijalla, joka
muuttaa jokaisen niiden nimeämän luokan toimettomaksi korvikkeeksi eikä aja mitään.

Mitä asiakas sai tietää, on täydellistä oman joukkueensa osalta ja osittaista vihollisten osalta: niiden laukaukset,
osumat ja terveyden muutokset ovat mukana, kun ne olivat kantaman sisällä.

**Taistelun alku** on hetki, jolloin areenan päivitys kertoo taistelujakson alkaneen; replayssa ilman sitä se on
ensimmäinen hetki, jolloin mikään ajoneuvo liikkuu.

**Kuolemat:** aika on areenan tappoviesti (1.x), muuten terveyden muutos, joka lopetti ajoneuvon, muuten taistelun
alku plus uhrin `lifeTime` tuloksista (kokonaisina sekunteina). Paikka on se, missä uhri nähtiin viimeksi, kun se oli
viisi sekuntia tai vähemmän ennen kuolemaa; muuten 2.x-asiakkailla paikka, jonka tulokset antavat (x ja z, ei
korkeutta), vain ottelun asiakirjassa. Tallennus, joka päättyi ennen loppua, ei sisällä kuolemia.

**Ei luettu:**

- Havaitseminen ja minikartta: eivät ole virrassa omina tapahtumina.
- Tykin kohoaminen asteina: virrassa on askel tykin rajojen välillä, ja rajat ovat pelin ajoneuvotiedostoissa.
- Moduulivauriot, miehistövammat, kulutustavarat ja ammukset: kutsut, jotka ne kantavat, eivät erottuneet
  toisistaan pelkällä muodolla 1.12:n ja 2.4:n välillä.
- Kokonaisuuden luontipaketit ajoneuvon ja sen tyypin lisäksi: ne sisältävät kaikki ajoneuvon ominaisuudet, kun
  se tulee asiakkaan näkyviin kerralla, järjestyksessä, jonka vain määritystiedostot antavat (säilytetty kokonaisena
  sivutiedostossa).
- Staattiset törmäykset (puut, talot), tallentavan pelaajan oma tähtäys ja fysiikkapaketit.
- Taistelun chat-komentojen numerot nimineen: numerointi on pelin ja se muuttuu; ottelun asiakirja säilyttää
  jokaisen komennon argumentit, mukana avaimen, jos sillä on sellainen (`ATTACK_ENEMY`, ...).
- Hyökkäyssyyt yli 5: kirjoitettu vain numeroina.

## Miten lukeminen tarkistettiin {#how-the-reading-was-checked}

Lukeminen tarkistettiin julkisilla replayilla asiakasversioista 1.12 ja 2.4, jokainen arvo vertaamalla johonkin,
minkä replay antaa toisen kerran:

- **Sijainnit:** jokaisella koskaan nähdyllä tankilla on rata kymmenellä näytteellä sekunnissa; nopeudet pysyvät
  siinä, mihin tankki pystyy; suunta vastaa liikkeen suuntaa noin 0,02 radiaania; missä tulokset antavat kuoleman
  paikan, tässä luettu paikka on muutaman metrin sisällä siitä.
- **Tallentava pelaaja:** laukausten ja aiheutetun vahingon arvot ovat yhtä suuret kuin tulosten, jokaisella
  tarkistetulla replayllä.
- **Terveys:** jokaisen tankin viimeinen luettu terveys on sama kuin tuloksissa; vastaanotettu vahinko luettuna ei
  ole koskaan suurempi kuin tuloksissa. Asiakkaan näkymän ulkopuolella olevan tankin tappoisku jää usein
  lähettämättä versiossa 2.4.
- **Osumat:** osuman vahinko on yhtä suuri kuin terveyden muutos sillä hetkellä lähes jokaisella osumalla.
- **Torni:** laukauksella rungon suunta plus tornin kääntö osoittaa sinne, minne luotisuora lensi, noin 0,01
  radiaanin tarkkuudella (mediaani).
- **Kuolemat ja taistelun alku:** noin sekunnin tarkkuudella siitä, mitä tulokset ja areena sanovat.

Testit rakentavat replayt samaan asetteluun, joten tässä tietovarastossa ei ole yhtään oikeaa replayta.

**Ei tarkistettu:** asiakasversiot ennen 1.12, konsoli- ja Blitz-replayt (eri pelejä), Lestan Mir Tankov
(`.mtreplay`) ja muut tilat kuin satunnaistaistelut ja taistelutyyppi 20.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
