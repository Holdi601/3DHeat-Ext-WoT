---
title: Kaip įrankis skaito įrašą
nav_order: 7
lang: lt
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kaip įrankis skaito įrašą {#how-it-reads-a-replay}

Įrašas yra JSON blokų antraštė ir žaidimo paketų srautas (formato pastabos
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Pirmas blokas, be šifravimo: žemėlapis, kliento versija, įrašantis žaidėjas, serverio nustatymai ir sąrašas
  (`vehicles`: vardas, komanda, technika, raktas - technikos id).
- Antras, kai įrašas tęsėsi iki pabaigos: rezultatų ekranas - kiekvienos technikos eilutė (šūviai, pataikymai,
  prasiskverbimai, padaryta žala, gauta, užblokuota ir padėta žala, žvalgyba, patirtis, kreditai, apdovanojimai...),
  įrašančio žaidėjo informacija apie kiekvieną taikinį, paskyros, mūšio trukmė, laimėtojas ir pabaigos priežastis;
  kai kuriuose režimuose vienintelis pilnas sąrašas (tų sąrašų antraštė nurodo tik savo komandą).
- Paketų srautas, suspaustas zlib ir užšifruotas Blowfish raktu, kurį turi žaidimas; bendruomenės įrankiai, skaitantys
  šiuos failus, jį paskelbė nuo 2013 m.

**Pozicijos** yra variklio pozicijų atnaujinimai: technikos id, jos pozicija ir kryptis, surasti pagal jų formą, o ne
pagal paketo numerį, todėl pataisa, kuri perrikiuoja numerius, nesuteikia tuščios lentelės. Jos yra tai, ką įrašantis
klientas buvo pasakytas: jo paties komanda visą laiką, priešas tik tada, kai jis pastebėtas (arba kliento
nuotolyje). Technika, kurios niekada nepastebėta, eilučių neturi. Technikos eilutės baigiasi jai žuvus.

**Likusi srauto dalis** - sveikata, šūviai, trasuojantys sviediniai, sprogimai, pataikymai, patrankų kampai, arenos
atnaujinimai - yra technikų ir kliento avataro metodų iškvietimai bei savybių pakeitimai, sunumeruoti pagal žaidimo
apibrėžimų failus, kurie keičiasi su pataisomis (1.12 ir 2.4 juos numeruoja skirtingai). Kiekvienas randamas pagal
savo argumentų formą ir tai, kaip jie susiję - žr.
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - o rasti
numeriai yra rungtynių dokumento `decoded` skiltyje. Pokalbis, kameros režimas ir kliento paties įvykiai yra atskiri
paketai. Arenos atnaujinimai ir kliento įvykiai yra Python pickle formatu; juos skaito skaitytuvas, kuris kiekvieną
klasę, kurią jie įvardija, paverčia inertišku pakaitalu ir nieko nevykdo.

Tai, ką klientui buvo pasakyta, yra pilna jo komandai ir dalinė priešams: jų šūviai, pataikymai ir sveikatos pokyčiai
yra įrašyti, kol jie buvo nuotolyje.

**Mūšio pradžia** yra tada, kai arenos atnaujinimas sako, kad mūšio periodas prasidėjo; įraše be jo - pirmą akimirką,
kai kuri nors technika pajuda.

**Žūtys:** laikas yra arenos nužudymo pranešimas (1.x), kitu atveju sveikatos pokytis, kuris užbaigė techniką, kitu
atveju mūšio pradžia plius aukos `lifeTime` iš rezultatų (sveiki sekundės). Vieta yra ten, kur auka paskutinį kartą
matyta, jei tai buvo per penkias sekundes nuo jos žūties; kitu atveju 2.x klientuose - vieta, kurią nurodo rezultatai
(x ir z, be aukščio), tik rungtynių dokumente. Įrašas, kuris sustojo prieš pabaigą, žūčių neturi.

**Neskaitoma:**

- Žvalgyba ir mini žemėlapis: srautas jų kaip savo įvykių neturi.
- Patrankos pakėlimas laipsniais: srautas turi žingsnį tarp patrankos ribų, o ribos yra žaidimo technikos failuose.
- Modulių žala, įgulos sužalojimai, sunaudojamos priemonės ir šaudmenys: iškvietimų, kurie juos neša, negalima atskirti
  vien pagal formą tarp 1.12 ir 2.4.
- Esybės sukūrimo paketai, išskyrus esybę ir jos tipą: jie laiko kiekvieną technikos savybę, kai ji vienu metu įeina į
  kliento matymo lauką, tokia tvarka, kurią duoda tik apibrėžimų failai (pilnai išsaugoti papildomame faile).
- Statiniai susidūrimai (medžiai, namai), įrašančio žaidėjo paties taikymas ir fizikos paketai.
- Mūšio pokalbio komandų numeriai kaip vardai: numeravimas yra žaidimo ir keičiasi; rungtynių dokumente
  išsaugomi kiekvienos komandos argumentai, tarp jų jos raktas, kai jis yra (`ATTACK_ENEMY`, ...).
- Atakos priežastys virš 5: rašomos tik kaip skaičiai.

## Kaip patikrintas skaitymas {#how-the-reading-was-checked}

Skaitymas patikrintas viešuose 1.12 ir 2.4 klientų įrašuose, kiekviena reikšmė - su kitu kartu įraše pateikta
verte:

- **Pozicijos:** kiekvienas kada nors matytas tankas turi trajektoriją dešimt pavyzdžių per sekundę; greičiai lieka
  tame, ką tankas gali; kryptis sutampa su judėjimo kryptimi maždaug 0,02 rad tikslumu; kur rezultatai nurodo žūties
  vietą, čia perskaityta vieta yra per kelis metrus nuo jos.
- **Įrašantis žaidėjas:** šūvių ir padarytos žalos reikšmės lygios rezultatų reikšmėms kiekviename patikrintame įraše.
- **Sveikata:** paskutinė kiekvieno tanko perskaityta sveikata lygi rezultatų; gauta žala niekada neviršija rezultatų.
  2.4 versijoje mirtinas smūgis technikai, esančiai už kliento matymo lauko, dažnai neatsiunčiamas.
- **Pataikymai:** pataikymo žala beveik kiekvienam pataikymui lygi sveikatos pokyčiui tą akimirką.
- **Bokštelis:** šūvio metu korpuso kryptis pliusas bokštelio posūkis rodo, kur skrido trasuojantis sviedinys, maždaug
  0,01 rad tikslumu (mediana).
- **Žūtys ir mūšio pradžia:** maždaug per sekundę nuo to, ką sako rezultatai ir arena.

Testai sukuria įrašus tokiu pačiu išdėstymu, todėl šioje saugykloje joks tikras įrašas nelaikomas.

**Nepatikrinta:** kliento versijos prieš 1.12, konsolių ir Blitz įrašai (kiti žaidimai), Lesta Mir Tankov
(`.mtreplay`), ir režimai, kitokie nei atsitiktiniai mūšiai bei mūšio tipas 20.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
