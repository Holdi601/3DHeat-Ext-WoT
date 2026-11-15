---
title: "Si e lexon një riluajtje"
nav_order: 7
lang: sq
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Si e lexon një riluajtje {#how-it-reads-a-replay}

Një riluajtje është një header me blloqe JSON dhe rrjedha e paketave të lojës (shënime
për formatin te [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Blloku i parë, i hapur: harta, versioni i klientit, lojtari që regjistron,
  cilësimet e serverit dhe lista e lojtarëve (`vehicles`: emri, skuadra, tanku,
  sipas ID-së së mjetit).
- Blloku i dytë, kur regjistrimi zgjati deri në fund: ekrani i rezultateve -
  rreshti i çdo mjeti (të shtëna, goditje, depërtime, dëm i shkaktuar, i marrë,
  i bllokuar dhe i ndihmuar, zbulim, xp, kredite, arritje...), detajet për objektiv
  të lojtarit që regjistron, llogaritë, kohëzgjatja e ndeshjes,
  fituesi dhe arsyeja e mbarimit; në disa mënyra e vetmja listë e plotë lojtarësh (header-i
  i atyre liston vetëm skuadrën e vet).
- Rrjedha e paketave, e kompresuar me zlib dhe e shifruar me Blowfish me një çelës që
  e mban loja, të cilin mjetet e komunitetit që i lexojnë këto skedarë e kanë publikuar
  që nga 2013.

**Pozicionet** janë përditësimet e pozicionit të motorit: ID e një mjeti, pozicioni i tij
dhe heading i tij, të gjetura sipas formës së tyre dhe jo numrit të paketës, kështu që një
patch që i rinumëron nuk e boshatis tabelën. Ato janë ajo që iu tha klientit që regjistron:
skuadrën e vet gjatë gjithë kohës, një armik vetëm kur u zbulua (ose në rrezen e klientit). Një mjet që
nuk u zbulua kurrë nuk ka rreshta. Rreshtat e një mjeti ndalen në vdekjen e tij.

**Pjesa tjetër e rrjedhës** - shëndeti, të shtënat, gjurmët e plumbave, shpërthimet, goditjet, këndet e topit,
përditësimet e arenës - janë thirrje metodash dhe ndryshime vetish të mjeteve
dhe të avatarit të klientit, të numëruara nga skedarët e përkufizimit të lojës, që
ndryshojnë me patch-et (1.12 dhe 2.4 i numërojnë ndryshe). Secila gjendet nga
forma e argumenteve të saj dhe si lidhen ato bashkë - shih
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - dhe numrat e gjetur
janë te `decoded` i dokumentit të ndeshjes. Biseda, mënyra e kamerës dhe ngjarjet e vetë klientit
janë paketa më vete. Përditësimet e arenës dhe ngjarjet e klientit janë Python
pickle; lexohen nga një lexues që çdo klasë që emërtojnë e kthen në një zëvendësues
të pavlefshëm dhe nuk ekzekuton asgjë.

Ajo që iu tha klientit është e plotë për skuadrën e vet dhe e pjesshme për
armiqtë: të shtënat, goditjet dhe ndryshimet e shëndetit të tyre janë aty ndërsa ishin
në rreze.

**Fillimi i betejës** është kur përditësimi i arenës thotë se filloi periudha e betejës;
në një riluajtje pa të, çasti i parë kur lëviz ndonjë mjet.

**Vdekjet:** koha është mesazhi i vrasjes së arenës (1.x), përndryshe ndryshimi i shëndetit
që e mbaroi mjetin, përndryshe fillimi i betejës plus `lifeTime` i viktimës
nga rezultatet (sekonda të plota). Vendi është ku u pa viktima së fundmi,
kur kjo ishte brenda pesë sekondash nga vdekja; përndryshe, në klientët 2.x, vendi
që japin rezultatet (x dhe z, pa lartësi), vetëm në dokumentin e ndeshjes. Një regjistrim
që u ndal para fundit nuk ka vdekje.

**Të palexuara:**

- Zbulimi dhe minihartë: nuk janë në rrjedhë si ngjarje më vete.
- Ngritja e topit në gradë: rrjedha ka një hap midis kufijve të topit,
  dhe kufijtë janë në skedarët e mjeteve të lojës.
- Dëmtimi i moduleve, lëndimet e ekuipazhit, konsumueshmet dhe municioni: thirrjet që
  i mbartin nuk u dallonin dot vetëm nga forma midis 1.12 dhe 2.4.
- Paketat e krijimit të entiteteve përtej entitetit dhe llojit të tij: mbajnë çdo
  veti të një mjeti që hyn në pamjen e klientit njëherësh, në një radhë që e japin vetëm
  skedarët e përkufizimit (ruhen të plota te skedari anësor).
- Përplasjet statike (pemë, shtëpi), synimi i vetë lojtarit që regjistron dhe paketat e
  fizikës.
- Numrat e komandave të bisedës së betejës si emra: numërimi është i lojës dhe
  ndryshon; dokumenti i ndeshjes mban argumentet e çdo komande, mes tyre çelësin e saj
  kur ka (`ATTACK_ENEMY`, ...).
- Arsyet e sulmit mbi 5: shkruhen vetëm si numra.

## Si u kontrollua leximi {#how-the-reading-was-checked}

Leximi u kontrollua në riluajtje publike të klientëve 1.12 dhe 2.4, çdo
vlerë ndaj diçkaje që riluajtja e jep për herë të dytë:

- **Pozicionet:** çdo tank i parë ndonjëherë ka një gjurmë me dhjetë mostra në sekondë;
  shpejtësitë mbeten brenda asaj që mund të bëjë një tank; heading përputhet me
  drejtimin e udhëtimit brenda rreth 0.02 rad; aty ku rezultatet japin vendin e një vdekjeje,
  vendi i lexuar këtu është brenda disa metrash prej tij.
- **Lojtari që regjistron:** të shtënat dhe dëmi i shkaktuar i lexuar janë të barabartë me
  vlerat e rezultateve, në çdo riluajtje të kontrolluar.
- **Shëndeti:** shëndeti i fundit i lexuar i çdo tanku është i barabartë me atë të rezultateve; dëmi
  i marrë i lexuar nuk është kurrë më shumë se ai i rezultateve. Në 2.4 goditja vrasëse mbi
  një tank jashtë pamjes së klientit shpesh nuk dërgohet.
- **Goditjet:** dëmi i një goditjeje është i barabartë me ndryshimin e shëndetit në atë çast
  për pothuajse çdo goditje.
- **Kupola:** në një të shtënë, heading i trupit plus yaw i kupolës tregon
  ku fluturoi gjurma e plumbit, brenda rreth 0.01 rad (mediana).
- **Vdekjet dhe fillimi i betejës:** brenda rreth një sekonde nga ajo që thonë
  rezultatet dhe arena.

Testet i ndërtojnë riluajtjet me të njëjtën strukturë, kështu që asnjë riluajtje e vërtetë nuk
mbahet në këtë depo.

**Të pakontrolluara:** klientët para 1.12, riluajtjet e konsolës dhe Blitz (lojëra
të ndryshme), Mir Tankov i Lesta (`.mtreplay`), dhe mënyra të ndryshme nga betejat e rastësishme
dhe lloji i betejës 20.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
