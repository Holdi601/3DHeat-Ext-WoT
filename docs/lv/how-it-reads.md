---
title: Kā tas nolasa atkārtojumu
nav_order: 7
lang: lv
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kā tas nolasa atkārtojumu {#how-it-reads-a-replay}

Atkārtojums ir galvene ar JSON blokiem un spēles paketes straume (formāta piezīmes failā [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Pirmais bloks, atklātā tekstā: karte, klienta versija, ierakstošais spēlētājs, servera iestatījumi un sastāvs (`vehicles`: nosaukums, komanda, tanks, atslēgts pēc transportlīdzekļa ID).
- Otrais, kad ieraksts ilga līdz beigām: rezultātu ekrāns — katra transportlīdzekļa rinda (šāvieni, trāpījumi, caurdurumi, nodarītie, saņemtie, bloķētie un palīdzētie bojājumi, izlūkošana, xp, krediti, sasniegumi...), ierakstošā spēlētāja detaļas pa mērķiem, konti, mača ilgums, uzvarētājs un beigu iemesls; dažos režīmos vienīgais pilnais sastāvs (šo sarakstu galvenes uzskaita tikai savu komandu).
- Paketes straume, saspiesta ar zlib un šifrēta ar Blowfish, ar atslēgu, ko spēle satur un ko kopienas rīki, kas lasa šos failus, ir publicējuši kopš 2013. gada.

**Pozīcijas** ir dzinēja pozīciju atjauninājumi: transportlīdzekļa ID, tā pozīcija un tā virziens, atrasti pēc to formas, nevis to paketes numura, tāpēc ielāps, kas pārnumurē tos, neiztukšo tabulu. Tās ir tas, ko ierakstošais klients tika pateicis: tā paša komanda visu laiku, ienaidnieks tikai kamēr tas ir pamanīts (vai klienta diapazonā). Transportlīdzeklis, kas nekad nav pamanīts, nav rindu. Transportlīdzekļa rindas beidzas ar tā nāvi.

**Pārējā straume** — veselība, šāvieni, trasieri, sprādzieni, trāpījumi, lielgabalu leņķi, arēnas atjauninājumi — ir transportlīdzekļu un klienta avatāra metožu izsaukumi un īpašību izmaiņas, numurētas ar spēles definīciju failiem, kas mainās līdz ar ielāpiem (1.12 un 2.4 tās numurē citādi). Katra tiek atrasta pēc tās argumentu formas un tā, kā tie saistās — skat. [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) — un atrastie numuri ir mača dokumenta `decoded`. Tērzēšana, kameras režīms un klienta paša notikumi ir savas paketes. Arēnas atjauninājumi un klienta notikumi ir Python pickles; tos nolasa lasītājs, kas katru klasi, ko tie nosauc, pārvērš par inertu aizstājēju un neizpilda neko.

Ko klients tika pateicis, ir pilnīgi savai komandai un daļēji ienaidniekiem: viņu šāvieni, trāpījumi un veselības izmaiņas ir tur, kamēr tie bija diapazonā.

**Kaujas sākums** ir brīdis, kad arēnas atjauninājums saka, ka kaujas periods sākās; atkārtojumā bez tā — pirmais brīdis, kad jebkurš transportlīdzeklis kustas.

**Nāves:** laiks ir arēnas nogalināšanas ziņojums (1.x), citādi veselības izmaiņa, kas beidza transportlīdzekli, citādi kaujas sākums plus upura `lifeTime` no rezultātiem (veselas sekundes). Vieta ir tur, kur upuris pēdējo reizi tika redzēts, ja tas bija piecu sekunžu robežās no tā nāves; citādi 2.x klientos vieta, ko dod rezultāti (x un z, bez augstuma), tikai mača dokumentā. Ierakstam, kas apstājās pirms beigām, nāvju nav.

**Nav nolasīts:**

- Atklāšana un minimaps: straumē nav kā atsevišķi notikumi.
- Lielgabala leņķis grādos: straumē ir solis starp lielgabala robežām, un robežas ir spēles transportlīdzekļu failos.
- Moduļu bojājumi, apkalpes ievainojumi, patēriņa priekšmeti un munīcija: izsaukumus, kas tos nes, nevarēja atšķirt pēc formas vien 1.12 un 2.4 starp.
- Entītiju izveides paketes pāri entītijai un tipam: tās satur katru transportlīdzekļa īpašību, kad tas ieiet klienta redzeslokā, vienlaicīgi, secībā, ko dod tikai definīciju faili (paturētas pilnībā papildfailā).
- Statiskās sadursmes (koki, mājas), ieraksta spēlētāja paša mērķēšana un fizikas paketes.
- Kaujas tērzēšanas komandu numuri kā nosaukumi: numerācija ir spēles un mainās; mača dokuments satur katras komandas argumentus, tostarp tās atslēgu, kur tādu ir (`ATTACK_ENEMY`, ...).
- Uzbrukuma iemesli virs 5: rakstīti tikai kā numuri.

## Kā lasīšana pārbaudīta {#how-the-reading-was-checked}

Lasīšana pārbaudīta uz publiskiem 1.12 un 2.4 klientu atkārtojumiem; katra vērtība salīdzināta ar kaut ko, ko atkārtojums dod otrreiz:

- **Pozīcijas:** katram tankam, kāds jebkad redzēts, ir celiņš ar desmit paraugiem sekundē; ātrumi paliek tajā, ko tanks spēj; virziens atbilst kustības virzienam ar nobīdi apmēram 0,02 rad; kur rezultāti dod nāves vietu, šeit nolasītā vieta ir dažu metru robežās no tās.
- **Ierakstošais spēlētājs:** šāvieni un nodarītie bojājumi, kas nolasīti, ir vienādi ar rezultātu vērtībām katrā pārbaudītajā atkārtojumā.
- **Veselība:** katra tanka pēdējā nolasītā veselība ir vienāda ar rezultātu; saņemto bojājumu nolasījums nekad nav lielāks par rezultātu. 2.4 versijā nāvējošais sitiens tankam ārpus klienta redzes bieži netiek nosūtīts.
- **Trāpījumi:** trāpījuma bojājums ir vienāds ar veselības izmaiņu tajā brīdī gandrīz katram trāpījumam.
- **Tornis:** šāviena brīdī korpusa virziens plus torņa yaw norāda, kurp lidoja trasieris, aptuveni 0,01 rad robežās (mediāna).
- **Nāves un kaujas sākums:** apmēram sekundes robežās no tā, ko saka rezultāti un arēna.

Testi veido atkārtojumus tādā pašā izkārtojumā, tāpēc šajā repozitorijā nav neviena īsta atkārtojuma.

**Nav pārbaudīts:** klienti pirms 1.12, konsoles un Blitz atkārtojumi (citas spēles), Lesta Mir Tankov (`.mtreplay`), un režīmi, kas nav nejauša kauja un kaujas tips 20.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
