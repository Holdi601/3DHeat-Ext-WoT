---
title: "Ako sa replay číta"
nav_order: 7
lang: sk
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Ako sa replay číta {#how-it-reads-a-replay}

Replay je hlavička z blokov JSON a tok paketov hry (poznámky k formátu
v [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Prvý blok, čitateľný bez šifry: mapa, verzia klienta, hráč, ktorý replay nahral, nastavenia servera a súpiska
  (`vehicles`: meno, tím, tank, kľúčované id vozidla).
- Druhý, keď nahrávanie trvalo do konca: obrazovka výsledkov – riadok každého vozidla (výstrely, zásahy, preniknutia,
  spôsobené poškodenie, prijaté, zablokované a asistované poškodenie, odhalenie, skúsenosti, kredity, úspechy ...),
  podrobnosti hráča, ktorý replay nahral, na každý cieľ, účty, dĺžka zápasu, víťaz a dôvod ukončenia; v niektorých
  režimoch jediná úplná súpiska (hlavička týchto zoznamov uvádza len vlastný tím).
- Tok paketov, komprimovaný zlibom a šifrovaný Blowfishom s kľúčom, ktorý hra nesie; komunitné nástroje, ktoré tieto
  súbory čítajú, ho zverejňujú od roku 2013.

**Polohy** sú aktualizácie polohy z enginu: id vozidla, jeho poloha a smer, nájdené podľa ich tvaru a nie čísla paketu,
takže oprava, ktorá ich prečísluje, nevyprázdni tabuľku. Sú to to, čo sa klientovi, ktorý nahrával, povedalo: jeho
vlastný tím po celý čas, nepriateľ len kým je spozorovaný (alebo v dosahu klienta). Vozidlo, ktoré nikdy nebolo
spozorované, nemá riadky. Riadky vozidla sa končia jeho smrťou.

**Zvyšok toku** – zdravie, výstrely, stopy, výbuchy, zásahy, uhly zbraní, aktualizácie arény – sú volania metód a zmeny
vlastností vozidiel a avatara klienta, číslované definičnými súbormi hry, ktoré sa menia s patchmi (1.12 a 2.4 ich
číslujú inak). Každé sa nájde podľa tvaru jeho argumentov a toho, ako spolu súvisia – pozri
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) – a nájdené
čísla sú v `decoded` dokumentu zápasu. Chat, režim kamery a vlastné udalosti klienta sú vlastné pakety. Aktualizácie
arény a vlastné udalosti klienta sú pickle súbory Pythonu; číta ich čítačka, ktorá každú triedu, ktorú menujú, zmení
na neaktívnu náhradu a nič nespúšťa.

To, čo bolo klientovi povedané, je úplné pre jeho vlastný tím a čiastočné pre nepriateľov: ich výstrely, zásahy
a zmeny zdravia sú tam, kým boli v dosahu.

**Začiatok bitky** je okamih, keď aktualizácia arény hovorí, že sa začala perióda bitky; v replayi bez nej je to prvý
okamih, keď sa niektoré vozidlo pohne.

**Smrti:** čas je správa o zabití z arény (1.x), inak zmena zdravia, ktorá vozidlo ukončila, inak začiatok bitky plus
`lifeTime` obete z výsledkov (celé sekundy). Miesto je tam, kde bola obeť naposledy videná, keď to bolo do päť sekúnd
od jej smrti; inak, pri klientoch 2.x, miesto, ktoré dávajú výsledky (x a z, bez výšky), len v dokumente zápasu. Nahrávanie,
ktoré sa zastavilo pred koncom, nemá smrti.

**Nečítané:**

- Spozorovanie a minimapa: v toku nie sú ako vlastné udalosti.
- Uhol dela v stupňoch: tok má krok medzi hranicami dela a hranice sú v súboroch vozidiel hry.
- Poškodenie modulov, zranenia posádky, spotrebný materiál a muníciu: volania, ktoré ich nesú, sa tvarom samotným nedali
  rozlíšiť naprieč 1.12 a 2.4.
- Pakety vytvorenia entít nad rámec entity a jej typu: držia každú vlastnosť vozidla, ktoré vstupuje do pohľadu klienta,
  naraz, v poradí, ktoré dávajú len definičné súbory (uchované celé v sprievodnom súbore).
- Statické kolízie (stromy, domy), vlastné mierenie hráča, ktorý replay nahral, a jeho fyzikálne pakety.
- Čísla príkazov bojového chatu ako názvy: číslovanie je hry a mení sa; dokument zápasu si nesie argumenty každého
  príkazu, medzi nimi jeho kľúč, ak ho má (`ATTACK_ENEMY`, ...).
- Dôvody útoku nad 5: zapísané len ako čísla.

## Ako sa čítanie overilo {#how-the-reading-was-checked}

Čítanie sa overilo na verejných replayoch klientov 1.12 a 2.4, každá hodnota oproti niečomu, čo replay dáva druhýkrát:

- **Polohy:** každý tank, ktorý sa kedy videl, má stopu s desiatimi vzorkami za sekundu; rýchlosti zostávajú v tom, čo tank
  dokáže; smer sa zhoduje so smerom letu do asi 0,02 rad; keď výsledky dávajú miesto smrti, miesto prečítané tu je
  do niekoľkých metrov od neho.
- **Hráč, ktorý replay nahral:** výstrely a spôsobené poškodenie sa čítajú rovnaké ako hodnoty výsledkov, na každom
  overenom replayi.
- **Zdravie:** posledné prečítané zdravie každého tanku sa rovná výsledkom; prijaté poškodenie nikdy nie je viac než vo
  výsledkoch. Pri 2.4 smrteľný zásah tanku mimo dohľadu klienta sa často neposiela.
- **Zásahy:** poškodenie zásahu sa takmer pri každom zásahu rovná zmene zdravia v tom okamihu.
- **Veža:** pri výstrele smer trupu plus uhol veže ukazuje tam, kam letela stopa, do asi 0,01 rad (medián).
- **Smrti a začiatok bitky:** do asi jednej sekundy od toho, čo hovoria výsledky a aréna.

Testy skladajú replaye do rovnakého rozloženia, takže v tomto repozitári nie je uložený žiadny skutočný replay.

**Neoverené:** klienty pred 1.12, replaye z konzol a z Blitz (iné hry), Mir Tankov od Lesty (`.mtreplay`) a režimy
iné než náhodné bitky a typ bitky 20.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
