---
title: Kuidas tööriist kordust loeb
nav_order: 7
lang: et
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Kuidas tööriist kordust loeb {#how-it-reads-a-replay}

Kordus on JSON-plokkide päis ja mängu paketivoog (formaadi märkused leheküljel
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Esimene plokk, lahtiselt: kaart, kliendi versioon, salvestajamängija, serveri seaded ja nimekiri
  (`vehicles`: nimi, meeskond, tank, võti on sõiduki ID).
- Teine, kui salvestus kestis lõpuni: tulemuste ekraan - iga sõiduki rida (lasud, tabamused, läbitungid, tekitatud,
  saadud, blokeeritud ja abistatud kahju, märkamine, xp, krediidid, saavutused...), salvestajamängija detailid
  iga sihtmärgi kohta, kontod, lahingu kestus, võitja ja lõpetamise põhjus; mõnes režiimis ainus täielik nimekiri
  (nende nimekirjade päis loetleb ainult oma meeskonna).
- Paketivoog, zlib-pakitud ja Blowfishiga šifreeritud mängu kaasasoleva võtmega, mille on avaldanud kogukonna
  tööriistad, mis neid faile loevad, alates 2013. aastast.

**Asukohad** on mootori asukohauuendused: sõiduki ID, tema asukoht ja suund, leitud nende kuju järgi, mitte paketi
numbri järgi, nii et paranduse, mis need ümber nummerdab, ei tühjenda tabelit. Need on see, mida salvestav klient
sai teada: oma meeskond kogu aeg, vaenlane ainult siis, kui teda nähti (või kliendi ulatuses). Sõiduk, keda
kunagi ei nähtud, ei anna ridu. Sõiduki read lõpevad tema surmaga.

**Ülejäänud voog** - tervis, lasud, tracerid, plahvatused, tabamused, püssi nurgad, areeni uuendused - on sõidukite
ja kliendi avatari meetodikutsed ja omaduste muutused, mis on nummerdatud mängu definitsioonifailide järgi ja mis
muutuvad koos paikadega (1.12 ja 2.4 nummerdavad need erinevalt). Iga üks leitakse oma argumentide kuju järgi ja
selle järgi, kuidas need omavahel sobivad - vt
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - ning
leitud numbrid on mängu dokumendi `decoded`-is. Vestlus, kaamera režiim ja kliendi enda sündmused on omaette
paketid. Areeni uuendused ja kliendi sündmused on Pythoni pickle'd; neid loeb lugeja, mis muudab iga klassi, mida
nad nimetavad, inertseks asendajaks, ega käivita midagi.

Mida klient teada sai, on täielik oma meeskonna jaoks ja osaline vaenlaste jaoks: nende lasud, tabamused ja
tervise muutused on seal, kuni nad olid ulatuses.

**Lahingu algus** on hetk, kui areeni uuendus ütleb, et lahingu periood algas; kordusel, kus seda ei ole, on see
esimene hetk, kui mõni sõiduk liigub.

**Surmad:** aeg on areeni tapmissõnum (1.x), muidu tervise muutus, mis lõpetas sõiduki, muidu lahingu algus pluss
ohvri `lifeTime` tulemustest (täissekundites). Koht on see, kus ohvrit viimati nähti, kui see oli surma eel viie
sekundi piires; muidu 2.x klientidel koht, mille annavad tulemused (x ja z, kõrgust ei ole), ainult mängu
dokumendis. Salvestus, mis katkes enne lõppu, ei sisalda surmi.

**Ei loeta:**

- Märkamine ja minikaart: need ei ole voos eraldi sündmustena.
- Püssi tõus kraadides: voos on samm püssi piiride vahel, ja piirid on mängu sõidukifailides.
- Mooduli kahjustus, meeskonna vigastused, kulumaterjalid ja laskemoon: kutsed, mis neid kannavad, ei olnud 1.12 ja
  2.4 vahel kuju järgi eristatavad.
- Olemi loomise paketid peale olemi ja tema tüübi: need sisaldavad kõiki sõiduki omadusi korraga, kui ta tuleb
  kliendi vaatevälja, järjekorras, mida annavad ainult definitsioonifailid (hoitud lisafailis tervena).
- Staatilised kokkupõrked (puud, majad), salvestajamängija enda sihtimine ja füüsikapaketid.
- Lahingu vestluskäskude numbrid nimedena: numeratsioon on mängu oma ja muutub; mängu dokument hoiab iga käsu
  argumendid, nende hulgas tema võtme, kui sellel on see (`ATTACK_ENEMY`, ...).
- Rünnaku põhjused üle 5: kirjutatud ainult numbritena.

## Kuidas lugemist kontrolliti {#how-the-reading-was-checked}

Lugemist kontrolliti avalikel kordustel klientidest 1.12 ja 2.4, iga väärtust võrreldes sellega, mida kordus annab
teist korda:

- **Asukohad:** iga kunagi nähtud tankil on rada kümne näidisega sekundis; kiirused jäävad sellesse, mida tank
  suudab; suund kokkulangeb sõidusuunaga umbes 0,02 radiaani täpsusega; kus tulemused annavad surma koha, on siin
  loetud koht sellest mõne meetri piires.
- **Salvestajamängija:** lasud ja tekitatud kahju loetud väärtused on võrdsed tulemuste omadega, igal kontrollitud
  kordusel.
- **Tervis:** iga tanki viimane loetud tervis võrdub tulemuste omaga; saadud kahju loetud väärtus ei ole kunagi
  suurem kui tulemuste oma. 2.4-l ei saadeta sageli tanki tapvat lööki, mis on väljaspool kliendi vaatevälja.
- **Tabamused:** tabamuse kahju võrdub peaaegu iga tabamuse korral tervise muutusega sel hetkel.
- **Torn:** lasu hetkel osutab korpuse suund pluss torni pööre sinna, kuhu tracer lendas, umbes 0,01 radiaani
  täpsusega (mediaan).
- **Surmad ja lahingu algus:** umbes sekundi täpsusega sellest, mida tulemused ja areen ütlevad.

Testid koostavad kordused samale paigutusele, nii et ühtegi päris kordust ei hoita selles hoidlas.

**Ei ole kontrollitud:** kliendid enne 1.12, konsooli ja Blitzi kordused (teised mängud), Lesta Mir Tankov
(`.mtreplay`) ja muud režiimid peale juhuslike lahingute ja lahingutüübi 20.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
