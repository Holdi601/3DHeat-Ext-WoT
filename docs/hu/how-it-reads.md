---
title: "Hogyan olvassa a visszajátszást"
nav_order: 7
lang: hu
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Hogyan olvassa a visszajátszást {#how-it-reads-a-replay}

A visszajátszás JSON-blokkok fejlécéből és a játék csomagfolyamából áll (a formátum
megjegyzései itt: [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Az első blokk, titkosítatlanul: a térkép, a kliens verziója, a felvevő játékos, a szerver
  beállításai és a névsor (`vehicles`: név, csapat, tank, a jármű azonosítója szerint kulcsolva).
- A második, ha a felvétel a végéig tartott: az eredménytábla – minden jármű sora (lövések,
  találatok, áthatolások, okozott, kapott, blokkolt és asszisztált sebzés, felderítés, tapasztalat,
  kredit, kitüntetések...), a felvevő játékos célonkénti részletei, a fiókok, a meccs hossza,
  győztese és befejezési oka; egyes módokban az egyetlen teljes névsor (ezeknek a listáknak a
  fejléce csak a saját csapatot sorolja fel).
- A csomagfolyam, zlib-tömörítve és a játék által hordozott kulccsal Blowfish-titkosítva, amelyet
  a közösség eszközei 2013 óta közzétettek ezeket a fájlokat olvasva.

**A pozíciók** a motor helyzetfrissítései: egy jármű azonosítója, a helyzete és az iránya, alakjuk
alapján megtalálva, nem a csomagszámuk szerint, így egy javítás, amely átszámozza őket, nem üríti ki
a táblázatot. Azt mutatják, amit a felvevő kliens megkapott: a saját csapatát végig, egy ellenséget
csak amíg felderítették (vagy a kliens hatótávolságában volt). Egy soha nem felderített járműnek nincs
sora. Egy jármű sorai a haláláig tartanak.

**A folyam többi része** – életerő, lövések, nyomjelzők, robbanások, találatok, ágyúszögek, aréna-frissítések –
a járművek és a kliens avatarjának metódushívásai és tulajdonságváltozásai, amelyeket a játék
definíciós fájljai számoznak, és amelyek a javításokkal változnak (az 1.12 és a 2.4 másként számozza
őket). Mindegyiket az argumentumai alakja és egymáshoz való viszonya alapján találjuk meg – lásd
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) –,
a megtalált számok pedig a meccsdokumentum `decoded` mezőjében vannak. A chat, a kameramód és a kliens
saját eseményei saját csomagok. Az aréna-frissítések és a kliens-események Python-pickle-ök; ezeket
olyan olvasó dolgozza fel, amely minden általuk megnevezett osztályt tehetetlen helyettesítővé alakít,
és semmit nem futtat.

Amit a kliens megkapott, az a saját csapatára teljes, az ellenségekre részleges: a lövéseik, találataik
és életerő-változásaik ott vannak, amíg hatótávolságban voltak.

**A csata kezdete** az a pillanat, amikor az aréna-frissítés szerint a csataidőszak elkezdődött; ha nincs
ilyen a visszajátszásban, az az első pillanat, amikor bármelyik jármű mozog.

**Halálok:** az idő az aréna ölés-üzenete (1.x), különben az az életerő-változás, amely a járművet
megölte, különben a csata kezdete plusz az áldozat `lifeTime` értéke az eredményekből (egész másodpercekben).
A hely ott van, ahol az áldozatot utoljára látták, ha ez a haláltól öt másodpercen belül volt; különben
2.x kliensnél az eredmények által adott hely (x és z, magasság nélkül), csak a meccsdokumentumban. Egy
a vége előtt megállt felvétel halálokokat nem tartalmaz.

**Nincs olvasva:**

- A felderítés és a kistérkép: a folyamban nincsenek saját eseményként.
- Az ágyú emelkedése fokban: a folyamban van egy lépcső az ágyú határai között, a határok pedig a játék
  járműfájljaiban vannak.
- Modulsérülés, személyzeti sérülések, fogyóeszközök és lőszer: az őket hordozó hívásokat alakjuk alapján
  nem lehetett megkülönböztetni az 1.12 és a 2.4 között.
- Az entitás-létrehozási csomagok az entitáson és a típusán túl: egyszerre tartalmazzák egy jármű minden
  tulajdonságát, amint belép a kliens látóterébe, olyan sorrendben, amelyet csak a definíciós fájlok adnak
  (egészben megtartva a kísérőfájlban).
- Statikus ütközések (fák, házak), a felvevő játékos saját célzása és fizikai csomagjai.
- A csatachat-parancsok számai nevekként: a számozás a játéké, és változik; a meccsdokumentum minden parancs
  argumentumait megtartja, köztük a kulcsát, ahol van (`ATTACK_ENEMY`, ...).
- Az 5-nél nagyobb támadási okok: csak számokként írva.

## Hogyan ellenőriztük az olvasást {#how-the-reading-was-checked}

Az olvasást az 1.12-es és a 2.4-es kliens nyilvános visszajátszásain ellenőriztük, minden értéket
összevetve valamivel, amit a visszajátszás másodszor is megad:

- **Pozíciók:** minden eddig látott tanknak tizedmásodpercenként mintákból álló pályája van; a sebességek
  azon belül maradnak, amit egy tank tud; az irány a haladási iránnyal 0,02 radiánon belül egyezik;
  ahol az eredmények megadják egy halál helyét, az itt olvasott hely néhány méteren belül van tőle.
- **A felvevő játékos:** a lövések és az okozott sebzés az eredmények értékeivel egyenlők, minden
  ellenőrzött visszajátszáson.
- **Életerő:** minden tank utolsó olvasott életereje egyenlő az eredményekével; a kapott sebzés olvasott
  értéke sosem nagyobb az eredményekénél. 2.4-en a kliens látóterén kívüli tank halálos találatát gyakran
  nem küldik el.
- **Találatok:** egy találat sebzése szinte minden találatnál egyenlő az adott pillanatbeli életerő-változással.
- **Torony:** egy lövésnél a törzs iránya plusz a torony elfordulása oda mutat, ahová a nyomjelző repült,
  körülbelül 0,01 radiánon belül (medián).
- **Halálok és a csata kezdete:** az eredmények és az aréna adatától körülbelül egy másodpercen belül.

A tesztek ugyanezzel az elrendezéssel építik fel a visszajátszásokat, így valódi visszajátszás nincs
megtartva ebben a tárolóban.

**Nincs ellenőrizve:** az 1.12 előtti kliensek, a konzolos és a Blitz visszajátszások (más játékok),
a Lesta Mir Tankov (`.mtreplay`), és a véletlen csatákon és a 20-as csatatípuson kívüli módok.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
