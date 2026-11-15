---
title: "Jak se replay čte"
nav_order: 7
lang: "cs"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Jak se replay čte {#how-it-reads-a-replay}

Replay je hlavička z bloků JSON a proud paketů hry (poznámky k formátu v
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- První blok, čitelný přímo: mapa, verze klienta, hráč, který nahrával, nastavení serveru a soupiska
  (`vehicles`: jméno, tým, tank, klíčované id vozidla).
- Druhý, když nahrávka trvala až do konce: obrazovka výsledků - řádek každého vozidla (výstřely, zásahy,
  průrazy, způsobené, přijaté, zablokované a asistované poškození, spotting, zkušenost, kredity, úspěchy...),
  podrobnosti hráče, který nahrával, u každého cíle, účty, délka zápasu, vítěz a důvod konce; v některých
  režimech jediná úplná soupiska (v záhlaví těchto seznamů jen vlastní tým).
- Proud paketů, komprimovaný zlibem a šifrovaný Blowfishem klíčem, který hra nese; komunitní nástroje, které tyto
  soubory čtou, ho zveřejnily od roku 2013.

**Pozice** jsou aktualizace pozic enginu: id vozidla, jeho pozice a kurz, nalezené podle tvaru, ne podle čísla
paketu, takže záplata, která je přečísluje, nevyprázdní tabulku. Jsou to to, co bylo řečeno nahrávajícímu klientovi:
jeho vlastní tým po celou dobu, nepřítel jen dokud byl spotted (nebo v dosahu klienta). Vozidlo, které nikdy nebylo
spotted, nemá žádné řádky. Řádky vozidla končí jeho smrtí.

**Zbytek proudu** - zdraví, výstřely, stopy, výbuchy, zásahy, úhly děla, aktualizace arény - jsou volání metod
a změny vlastností vozidel a avatara klienta, očíslované definičními soubory hry, které se mění se záplatami
(1.12 a 2.4 je číslují jinak). Každé se najde podle tvaru svých argumentů a toho, jak spolu souvisejí - viz
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - a
nalezená čísla jsou v `decoded` dokumentu zápasu. Chat, režim kamery a vlastní události klienta jsou samostatné
pakety. Aktualizace arény a události klienta jsou pickle soubory Pythonu; čte je čtečka, která každou třídu, kterou
pojmenují, promění v neškodnou náhražku a nic nespouští.

Co bylo řečeno klientovi, je úplné pro jeho vlastní tým a částečné pro nepřátele: jejich výstřely, zásahy a změny
zdraví tam jsou, dokud byli v dosahu.

**Začátek bitvy** je okamžik, kdy aktualizace arény říká, že bitevní perioda začala; v replayi bez ní je to první
okamžik, kdy se nějaké vozidlo pohne.

**Smrti:** čas je zpráva o zabití z arény (1.x), jinak změna zdraví, která vozidlo ukončila, jinak začátek bitvy
plus `lifeTime` oběti z výsledků (celé vteřiny). Místo je to, kde byla oběť naposledy spatřena, když to bylo do
pěti sekund od její smrti; jinak u klientů 2.x místo, které dávají výsledky (x a z, bez výšky), jen v dokumentu
zápasu. Nahrávka, která skončila před koncem, nemá žádné smrti.

**Nečteno:**

- Spotting a minimapa: v proudu nejsou jako vlastní události.
- Sklon děla ve stupních: proud má krok mezi mezemi děla a meze jsou v definičních souborech vozidel hry.
- Poškození modulů, zranění posádky, spotřební materiál a munice: volání, která je nesou, se podle tvaru samotného
  nedají rozlišit napříč 1.12 a 2.4.
- Pakety vytvoření entit nad entitu a její typ: drží každou vlastnost vozidla, které vstoupí do zorného pole
  klienta, najednou, v pořadí, které dávají jen definiční soubory (drženo celé v doplňku).
- Statické kolize (stromy, domy), vlastní míření hráče, který nahrával, a pakety fyziky.
- Čísla příkazů bitevního chatu jako názvy: číslování je hry a mění se; dokument zápasu drží argumenty každého příkazu,
  mezi nimi jeho klíč, je-li nějaký (`ATTACK_ENEMY`, ...).
- Důvody útoku nad 5: zapsané jen jako čísla.

## Jak bylo čtení ověřeno {#how-the-reading-was-checked}

Čtení bylo ověřeno na veřejných replayích klientů 1.12 a 2.4, každá hodnota proti něčemu, co replay dává podruhé:

- **Pozice:** každý tank, který byl kdy spatřen, má trať s deseti vzorky za vteřinu; rychlosti zůstávají v tom, co tank
  umí; kurz souhlasí se směrem jízdy do asi 0,02 rad; kde výsledky dávají místo smrti, místo přečtené zde je do
  několika metrů od něj.
- **Hráč, který nahrával:** výstřely a způsobené poškození se čtou stejně jako hodnoty z výsledků, u každého
  kontrolovaného replaye.
- **Zdraví:** poslední přečtené zdraví každého tanku se rovná výsledkům; přijaté poškození přečtené nikdy není vyšší
  než ve výsledcích. U 2.4 rána, která zabila tank mimo zorné pole klienta, často není poslána.
- **Zásahy:** poškození zásahu se u téměř každého zásahu rovná změně zdraví v tu chvíli.
- **Věž:** při výstřelu kurz trupu plus natočení věže ukazuje tam, kam letěla stopa, do asi 0,01 rad (medián).
- **Smrti a začátek bitvy:** do asi jedné vteřiny od toho, co říkají výsledky a aréna.

Testy staví replaye ve stejném rozložení, takže v tomto repozitáři není uložen žádný skutečný replay.

**Neověřeno:** klienti před 1.12, konzolové a Blitz replaye (jiné hry), Mir Tankov od Lesty (`.mtreplay`), a režimy
jiné než náhodné bitvy a typ bitvy 20.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
