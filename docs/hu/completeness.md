---
title: "Teljesség"
nav_order: 8
lang: "hu"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Teljesség {#completeness}

A visszajátszásból semmi sem vész el. Amit a konvertáló beolvas, az a táblázatba és a
meccsdokumentumba kerül; minden más tételt egészben megtart a `<match>.messages.parquet`
kísérőfájl; a meccsdokumentum `selfCheck.completeness` mezője pedig számolja, mi lett
minden tételfajtával. Ez az a szabály, amelyet minden 3DHeat-konverter közösen követ:
[A konverterek mindent megtartanak](https://holdi601.github.io/3DHeat/converters.html).

![A szintetikus visszajátszás önellenőrzése: minden látott, beolvasott, megtartott vagy elveszett tétel](../assets/img/completeness.svg)

## A számlálás {#the-count}

Tételfajtánként a `selfCheck.completeness.types` a következőket adja:

| Számláló | Jelentése |
|---|---|
| `seen` | hány van a visszajátszásban |
| `decoded` | egészben beolvasva |
| `partial` | részben beolvasva, és egészben megtartva a kísérőfájlban |
| `raw` | csak egészben megtartva a kísérőfájlban, nincs beolvasva |
| `lost` | elveszett: mindig `0` |

A fajták a visszajátszás saját fajtái: `block 0` (a fejléc), `block 1` (az eredmények),
`container sizes` és `deflate tail` (a tároló saját bájtjai), `packet <type>`, és az
entitásokon végzett hívásoknál `method <entity type>.<number>` és `property <entity type>.<number>`.
Az entitástípusok a létrehozó csomagok számai; a `selfCheck.entities.roles` megmondja, melyik
a felvevő játékos avatarja és melyek a járművek. Egy fajta, amelyről senki nem tudott, a
darabszámával együtt jelenik meg.

## A kísérőfájl {#the-sidecar}

| Oszlop | Mi |
|---|---|
| `time` | a visszajátszás órája, mint a táblázatban |
| `type`, `name` | a tétel fajtája; a konverter hogyan nevezi, ahol olvassa |
| `entity` | a jármű vagy avatar, amelyhez tartozik, mint a táblázat `entity` mezője |
| `decoded` | ami beolvasva belőle, JSON-ként |
| `payload`, `text` | a bájtjai egészben; a JSON-blokkok egészben |
| `entityType`, `packet`, `method` | a számok |

A sorok csomag, metódus, entitás és idő szerint vannak rendezve.

## Mi van beolvasva, és hogyan ellenőriztük {#what-is-read-and-how-it-was-checked}

- Minden pozíció **dőlése és billenése**: a dőlés a tank saját útjának lejtésének mínusza, amíg
  előre hajt; két tank ugyanazon a helyen, azonos iránnyal azonos billenésű, ellentétes iránnyal
  ellentétes billenésű.
- **Entitások** (`entities`): mikor kerültek a kliens látóterébe, és mikor távoztak onnan. Egyetlen
  tanknak sincs helye az eltűnése és visszatérése között.
- **A folyam verziója** (`streamVersion`): ugyanaz, mint a fejlécé.
- **A felvevő játékos célzása** (38-as csomag): egy irány, a kísérőfájl `decoded` mezőjében
  (`forward`); a játékos lövéseinél a lövedék repülési irányától egy fok töredékén belül van.

Minden más beolvasott adat (életerő, találatok, lövések, nyomjelzők, robbanások, ágyúszögek,
aréna-frissítések, chat, kameramódok, kliens-események, helyzetek) `partial`: a táblázatban vagy
a meccsdokumentumban van, és egészben megtartva a kísérőfájlban.

**Megtartva, de nincs beolvasva** (`raw`), a legnagyobb fajták: a táblázatban nem szereplő
helyzetfrissítések (az avatarról, egy tank halála után, a névsorban nem szereplő entitások),
a 26, 28, 29, 31, 36, 50, 54 és 57-es csomagok, néhány gyakori jármű- és avatar-tulajdonság,
minden olyan metódus és tulajdonság, amelyhez nincs olvasó (közöttük a modulsérülés, a
személyzet és a fogyóeszközök), és az entitás-létrehozások tulajdonságai.

## Nem elérhető {#not-available}

- Ami a szerver soha nem küldött a felvevő kliensnek: más játékosok célzása, kamerája és
  bemenetei, az ellenségek, amíg nem voltak felfedezve. A visszajátszás azt tartalmazza, amit
  egy kliens megkapott.
- Az entitástípusok, metódusok és tulajdonságok nevei: ezek a játék definíciós fájljaiban vannak,
  nem a visszajátszásban. A számok megmaradnak.
- Az ágyú emelkedése fokban és minden más, ami a tankok saját adataihoz kell a játék fájljaiból.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
