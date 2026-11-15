---
title: Ottelun asiakirja
nav_order: 6
lang: "fi"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Ottelun asiakirja {#the-match-document}

`<match>.match.json` sisältää kaiken, minkä replay kertoo ja joka ei ole taulukon rivi. Katselimen
Ottelu-välilehti lukee sen. (Koodi kutsuu sitä yhteenvedoksi.)

![Synteettisen ottelun asiakirjan alku ja sen avaimet](../assets/img/match-document.svg)

## Taistelu {#the-battle}

| Avain | Mitä se on |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; taistelun tunnus; kartan tunnus ja sen näyttönimi |
| `clientVersion`, `streamVersion` | pelin versio otsikosta, ja sellaisena kuin pakettivirta sen kertoo |
| `recorded` | milloin replay tallennettiin, sellaisena kuin peli sen kirjoittaa |
| `player`, `vehicle` | tallentava pelaaja ja hänen panssarivaununsa |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | otsikon taistelutyypin numero, pelimuoto, palvelin, alue ja se, oliko modeja asennettu |
| `duration` | taistelun pituus sekunteina, tuloksista |
| `winnerTeam`, `finishReason` | voittava joukkue ja pelin numero sille, miten taistelu päättyi, tuloksista |
| `complete`, `truncated` | tulokset ovat replayssa; tallennus pysähtyi aikaisin |
| `battleStart`, `battleStartFrom`, `firstMovement` | taistelun alku sekunteina tallennuksesta; `arena` (areena sanoi niin) tai `movement` (ensimmäinen hetki, jolloin mikään tankki liikkui); tuo ensimmäinen liike |
| `recordingSeconds` | tallennuksen pituus sekunteina |
| `positionPacket`, `hz`, `positions` | paketin numero, jossa sijainnit tulivat, näytettä sekunnissa, sijaintirivit |
| `events` | jokaisen tapahtuman taulukkorivien määrä |
| `units` | `metres; x east, y up, z north` |
| `decoded` | jokaiselle viestityypille löydetyt metodi- ja pakettinumerot |

## Pelaajat ja tapahtumat {#players-and-events}

| Avain | Mitä se on |
|---|---|
| `players` | yksi merkintä tankkia kohden: nimi, joukkue, panssarivaunu, klaani, näytteet, tapot, aiheutettu vahinko, selviytyi, elinaika; `seen` (laukaukset ja vahinko, jotka tallentava asiakas näki); otsikon ja tulosten koko merkintä sekä tili |
| `kills` | jokainen kuolema: aika (sekunteina), mistä aika tuli (`arena`, `health` tai `lifeTime`), uhri, tappaja, syynumero ja nimi |
| `periods` | taistelun jaksot (odotus, ennen taistelua, taistelu, taistelun jälkeen) palvelimen loppuajoilla |
| `basePoints` | tukikohdan valloituksen edistyminen joukkuetta ja tukikohtaa kohden |
| `chat`, `commands` | chat-rivit; taistelun chat-komennot kaikkine argumentteineen |
| `camera`, `clientEvents` | tallentavan pelaajan kameratilat; mitä asiakas tallensi itsestään (zoom, automaattitähtäys, kohteen vaihdot, ajoneuvon tila) |
| `arenaUpdates` | jokainen areenan päivitys, dekoodattuna, sellaisena kuin peli sen lähetti |

## Tulokset ja tarkistukset {#results-and-checks}

| Avain | Mitä se on |
|---|---|
| `serverSettings` | palvelimen asetukset otsikosta |
| `results`, `resultVehicles`, `frags` | tulosnäkymä: yhteiset, henkilökohtaiset (kohdekohtaisine yksityiskohtineen), pelaajat, tilit; jokaisen tankin tulosrivi; tapot pelaajaa kohden |
| `entities` | jokainen pakettivirran luoma kokonaisuus: sen tyyppinumero ja rooli, milloin se tuli asiakkaan näkyviin ja milloin se poistui |
| `selfCheck` | täydellisyyslaskuri ([Täydellisyys](completeness.md)) ja kokonaisuuksien ja version tarkistukset |

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
