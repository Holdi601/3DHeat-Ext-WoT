---
title: Cum citește un replay
nav_order: 7
lang: "ro"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Cum citește un replay {#how-it-reads-a-replay}

Un replay este un antet de blocuri JSON și fluxul de pachete al jocului (note de format
în [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Primul bloc, în clar: harta, versiunea clientului, jucătorul care înregistrează, setările serverului și lista
  (`vehicles`: nume, echipă, tanc, cheiat după id-ul vehiculului).
- Al doilea, când înregistrarea a durat până la sfârșit: ecranul rezultatelor -
  rândul fiecărui vehicul (lovituri, pătrunderi, daune date, primite,
  blocate și asistate, observare, xp, credite, realizări...), detaliile jucătorului care înregistrează pe fiecare țintă, conturile, durata meciului,
  câștigătorul și motivul încheierii; în unele moduri singura listă completă (antetul acelor liste
  dă doar echipa proprie).
- Fluxul de pachete, comprimat zlib și criptat Blowfish cu o cheie pe care o poartă jocul, pe care instrumentele comunității care citesc aceste fișiere au publicat-o din 2013.

**Pozițiile** sunt actualizările de poziție ale motorului: id-ul unui vehicul, poziția sa și cursul său, găsite după forma lor și nu după numărul pachetului, deci un patch care le renumerotează nu golește tabelul. Ele sunt ce i s-a spus clientului care înregistrează: echipa sa tot timpul, un inamic doar cât timp este observat (sau în raza clientului). Un vehicul niciodată observat nu are rânduri. Rândurile unui vehicul se opresc la moartea sa.

**Restul fluxului** - viața, loviturile, proiectilele, traseele de trasor, exploziile, lovitările, unghiurile tunului, actualizările arenei - sunt apeluri de metode și schimbări de proprietăți ale vehiculelor și ale avatarului clientului, numerotate după fișierele de definiție ale jocului, care se schimbă odată cu patch-urile (1.12 și 2.4 le numerotează diferit). Fiecare este găsit după forma argumentelor sale și după cum se leagă între ele - vedeți [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - iar numerele găsite sunt în `decoded` din documentul meciului. Chatul, modul camerei și evenimentele proprii ale clientului sunt pachete separate. Actualizările arenei și evenimentele clientului sunt pickle Python; sunt citite de un cititor care transformă fiecare clasă pe care o numesc într-un substitut inert și nu rulează nimic.

Ce i s-a spus clientului este complet pentru echipa sa și parțial pentru inamici: loviturile, lovitările și schimbările de viață ale acestora sunt acolo cât timp au fost în rază.

**Începutul bătăliei** este momentul în care actualizarea arenei spune că perioada bătăliei a început; într-un replay fără ea, primul moment în care se mișcă un vehicul.

**Morțile:** ora este mesajul de ucidere al arenei (1.x), altfel schimbarea de viață care a încheiat vehiculul, altfel începutul bătăliei plus `lifeTime` al victimei din rezultate (secunde întregi). Locul este unde a fost văzută ultima oară victima, când aceasta a fost în cinci secunde de moartea sa; altfel, la clienții 2.x, locul pe care îl dau rezultatele (x și z, fără înălțime), doar în documentul meciului. Un replay care s-a oprit înainte de sfârșit nu are morți.

**Nu se citesc:**

- Observarea și harta minimă: nu sunt în flux ca evenimente proprii.
- Înălțimea în grade a tunului: fluxul are un pas între limitele tunului, iar limitele sunt în fișierele vehiculelor din joc.
- Avarierea modulelor, rănile echipajului, consumabilele și muniția: apelurile care le transportă nu au putut fi deosebite doar după formă între 1.12 și 2.4.
- Pachetele de creare a entităților dincolo de entitate și tipul ei: ele țin fiecare proprietate a unui vehicul care intră deodată în vederea clientului, într-o ordine pe care o dau doar fișierele de definiție (păstrate întregi în fișierul auxiliar).
- Coliziunile statice (copaci, case), țintirea proprie a jucătorului care înregistrează și pachetele de fizică.
- Numerele comenzilor de chat de bătălie ca nume: numerotarea este a jocului și se schimbă; documentul meciului păstrează argumentele fiecărei comenzi, printre ele cheia sa acolo unde o are (`ATTACK_ENEMY`, ...).
- Motivele de atac peste 5: scrise doar ca numere.

## Cum a fost verificată citirea {#how-the-reading-was-checked}

Citirea a fost verificată pe replay-uri publice ale clienților 1.12 și 2.4, fiecare valoare
față de ceva ce replay-ul dă a doua oară:

- **Pozițiile:** fiecare tanc văzut vreodată are un traseu la zece eșantioane pe secundă; vitezele rămân în ce poate face un tanc; cursul concordă cu direcția de deplasare în limita a aproximativ 0,02 rad; acolo unde rezultatele dau locul unei morți, locul citit aici este la câțiva metri de el.
- **Jucătorul care înregistrează:** loviturile și daunele date sunt egale cu valorile din rezultate, pe fiecare replay verificat.
- **Viața:** ultima valoare citită a vieții fiecărui tanc este egală cu cea din rezultate; daunele primite citite nu depășesc niciodată pe cele din rezultate. Pe 2.4, lovitura fatală asupra unui tanc aflat în afara vederii clientului adesea nu este trimisă.
- **Loviturile:** daunea unei lovituri este egală cu schimbarea de viață din acel moment, pentru aproape fiecare lovitură.
- **Turela:** la un foc, cursul caroseriei plus rotirea turelei arată unde a zburat trasorul, în limita a aproximativ 0,01 rad (mediană).
- **Morțile și începutul bătăliei:** în limita a aproximativ o secundă față de ce spun rezultatele și arena.

Testele construiesc replay-uri în același aranjament, deci niciun replay real nu este păstrat în
acest depozit.

**Nu s-a verificat:** clienții dinaintea versiunii 1.12, replay-urile de consolă și Blitz (alte jocuri),
Mir Tankov de la Lesta (`.mtreplay`) și alte moduri decât bătăliile aleatorii și tipul de bătălie 20.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
