---
title: Kako bere posnetek
nav_order: 7
lang: sl
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kako bere posnetek {#how-it-reads-a-replay}

Posnetek je glava iz blokov JSON in paketni tok igre (opombe o formatu v
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Prvi blok, v čistem besedilu: zemljevid, različica odjemalca, igralec, ki je snemal, nastavitve strežnika in
  seznam (`vehicles`: ime, ekipa, tank, po id-ju vozila).
- Drugi, kadar je snemanje trajalo do konca: zaslon rezultatov – vrstica vsakega vozila (streli, zadetki,
  prebitja, nanesena, prejeta, blokirana in pomagana škoda, odkrivanje, izkušnje, krediti, dosežki ...),
  podrobnosti igralca, ki je snemal, za vsako tarčo, računi, trajanje bitke, zmagovalec in razlog konca; v
  nekaterih načinih edini popoln seznam (glava teh seznamov navaja samo lastno ekipo).
- Paketni tok, stisnjen z zlib in šifriran z Blowfish s ključem, ki ga nosi igra, ki so ga skupnostna orodja za
  branje teh datotek objavila od leta 2013.

**Položaji** so posodobitve položajev motorja: id vozila, njegov položaj in njegova smer, najdeni po obliki, ne po
številki paketa, zato popravek, ki jih prešteje na novo, ne izprazni tabele. So tisto, kar je bilo povedano
odjemalcu, ki je snemal: njegova ekipa ves čas, sovražnik samo med opazovanjem (ali v dosegu odjemalca). Vozilo,
ki ga nikoli niso opazili, nima vrstic. Vrstice vozila se ustavijo ob njegovi smrti.

**Ostali tok** – zdravje, streli, sledi, eksplozije, zadetki, koti topa, posodobitve arene – so klici metod in
spremembe lastnosti vozil ter avatarja odjemalca, oštevilčeni z datotekami definicij igre, ki se spreminjajo s
popravki (1.12 in 2.4 ju številčita drugače). Vsak je najden po obliki svojih argumentov in po tem, kako se
držijo skupaj – glejte [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) –
najdene številke pa so v `decoded` dokumenta tekme. Klepet, način kamere in lastni dogodki odjemalca so svoji
paketi. Posodobitve arene in dogodki odjemalca so pickle Pythona; prebere jih bralnik, ki vsak razred, ki ga
imenujejo, spremeni v nemo nadomestilo in ne izvede ničesar.

Kar je bilo povedano odjemalcu, je popolno za njegovo ekipo in delno za sovražnike: njihovi streli, zadetki in
spremembe zdravja so tam, dokler so bili v dosegu.

**Začetek bitke** je trenutek, ko posodobitev arene pove, da se je obdobje bitke začelo; v posnetku brez nje pa
prvi trenutek, ko se katerokoli vozilo premakne.

**Smrti:** čas je sporočilo arene o ubijanju (1.x), sicer sprememba zdravja, ki je vozilo končala, sicer začetek
bitke plus `lifeTime` žrtve iz rezultatov (cela sekunda). Mesto je, kjer je bila žrtev nazadnje videna, kadar je to
bilo v petih sekundah pred njeno smrtjo; sicer, pri odjemalcih 2.x, mesto, ki ga navajajo rezultati (x in z, brez
višine), samo v dokumentu tekme. Posnetek, ki se je ustavil pred koncem, nima smrti.

**Ni prebrano:**

- Opazovanje in mini zemljevid: v toku kot lastni dogodki niso prisotni.
- Kot topa v stopinjah: tok ima korak med mejama topa, meji pa sta v datotekah vozil igre.
- Poškodbe modulov, poškodbe posadke, potrošni material in strelivo: klici, ki jih nosijo, po obliki sami ne
  morejo biti ločeni med 1.12 in 2.4.
- Paketi ustvarjanja entitet preko entitete in njenega tipa: nosijo vsako lastnost vozila, ki hkrati vstopa v pogled
  odjemalca, v vrstnem redu, ki ga dajo samo datoteke definicij (ohranjeno celo v spremljevalni datoteki).
- Statični trki (drevesa, hiše), lastno ciljanje igralca, ki je snemal, in paketi fizike.
- Številke ukazov klepeta bojnega kot imena: številčenje je igrino in se spreminja; dokument tekme hrani argumente
  vsakega ukaza, med njimi njegov ključ, kjer ga ima (`ATTACK_ENEMY`, ...).
- Razlogi napada nad 5: zapisani samo kot številke.

## Kako je bilo branje preverjeno {#how-the-reading-was-checked}

Branje je bilo preverjeno na javnih posnetkih odjemalcev 1.12 in 2.4, vsaka vrednost z nečim, kar posnetek poda
drugič:

- **Položaji:** vsak tank, ki so ga kdaj videli, ima pot na desetih vzorcih na sekundo; hitrosti ostanejo v tem,
  kar tank zmore; smer se ujema s smerjo leta na približno 0,02 rad; kjer rezultati navajajo mesto smrti, je tukaj
  prebrano mesto znotraj nekaj metrov od njega.
- **Igralec, ki je snemal:** streli in nanesena škoda sta prebrana enaka vrednostim iz rezultatov, na vsakem
  preverjenem posnetku.
- **Zdravje:** zadnje prebrano zdravje vsakega tanka je enako tistemu iz rezultatov; prebrana prejeta škoda ni
  nikoli večja od tiste iz rezultatov. Pri 2.4 smrtonosni udarec tanku zunaj pogleda odjemalca pogosto ni poslan.
- **Zadetki:** škoda zadetka je za skoraj vsak zadetek enaka spremembi zdravja v tistem trenutku.
- **Stolp:** ob strelu smer trupa plus vodoravni kot stolpa kaže, kamor je letela sled, znotraj približno 0,01 rad
  (mediana).
- **Smrti in začetek bitke:** znotraj približno sekunde od tega, kar pravita rezultati in arena.

Testi sestavijo posnetke po isti postavitvi, zato v tem repozitoriju ni nobenega pravega posnetka.

**Ni preverjeno:** odjemalci pred 1.12, posnetki za konzole in Blitz (druge igre), Lestin Mir Tankov
(`.mtreplay`) ter načini, razen naključnih bitk in tipa bitke 20.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
