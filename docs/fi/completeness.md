---
title: Täydellisyys
nav_order: 8
lang: fi
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Täydellisyys {#completeness}

Replayssa ei heitetä mitään pois. Se, minkä muunnin lukee, menee taulukkoon ja ottelun asiakirjaan; jokainen
muu kohta säilytetään kokonaisena sivutiedostossa `<match>.messages.parquet`; ja ottelun asiakirjan
`selfCheck.completeness` laskee, mitä kullekin kohtatyypille tapahtui. Tämä on sääntö, jonka kaikki 3DHeat-muuntimet
jakavat: [Muuntimet säilyttävät kaiken](https://holdi601.github.io/3DHeat/converters.html).

![Synteettisen replayn itsetarkistus: jokainen kohta nähty, luettu, säilytetty tai menetetty](../assets/img/completeness.svg)

## Laskuri {#the-count}

Jokaiselle kohtatyypille `selfCheck.completeness.types` antaa:

| Laskuri | Tarkoittaa |
|---|---|
| `seen` | kuinka monta replay sisältää |
| `decoded` | luettu kokonaisena |
| `partial` | luettu osittain, ja säilytetty kokonaisena sivutiedostossa |
| `raw` | vain säilytetty kokonaisena sivutiedostossa, ei luettu |
| `lost` | menetetty: aina `0` |

Tyypit ovat replayn omia: `block 0` (otsikko), `block 1` (tulokset), `container sizes` ja `deflate tail`
(säiliön omat tavut), `packet <type>`, ja kokonaisuuksiin kohdistuville kutsuille `method <entity type>.<number>`
ja `property <entity type>.<number>`. Kokonaisuustyypit ovat numeroita, jotka luovat paketit antavat;
`selfCheck.entities.roles` kertoo, mikä on tallentavan pelaajan avatar ja mitkä ajoneuvot. Tyyppi, josta kukaan ei
tiennyt, näkyy laskurinsa kanssa.

## Sivutiedosto {#the-sidecar}

| Sarake | Mitä se on |
|---|---|
| `time` | replayn kello, kuten taulukossa |
| `type`, `name` | kohdetyyppi; sen nimi muuntimessa, siellä missä se luetaan |
| `entity` | ajoneuvo tai avatar, johon se kuuluu, kuten taulukon `entity` |
| `decoded` | siitä luettu, JSON-muodossa |
| `payload`, `text` | sen tavut kokonaisina; JSON-lohkot kokonaisina |
| `entityType`, `packet`, `method` | numerot |

Rivit on lajiteltu paketin, metodin, kokonaisuuden ja ajan mukaan.

## Mitä luetaan, ja miten se tarkistettiin {#what-is-read-and-how-it-was-checked}

- **Kallistus ja roll** jokaisesta sijainnista: kallistus on miinus tankin oman reitin kaltevuus, kun se ajaa
  eteenpäin; kaksi tankkia samassa paikassa samalla suunnalla saa saman rollin, vastakkaisilla suunnilla
  vastakkaiset rollit.
- **Kokonaisuudet** (`entities`): milloin kukin tuli asiakkaan näkyviin ja poistui sieltä. Yksikään tankki ei
  ole sijainnissa poistumisen ja paluun välillä.
- **Version virrassa** (`streamVersion`): sama kuin otsikon.
- **Tallentavan pelaajan tähtäys** (paketti 38): suunta, sivutiedoston `decoded`-kentässä (`forward`); pelaajan
  laukauksilla se on murto-asteen tarkkuudella siitä, mihin kuori lensi.

Kaikki muu luettu (terveys, osumat, laukaukset, luotisuorat, räjähdykset, tykin kulmat, areenan päivitykset,
chat, kameratilat, asiakkaan tapahtumat, sijainnit) on `partial`: taulukossa tai ottelun asiakirjassa, ja
säilytettynä kokonaisena sivutiedostossa.

**Säilytetty mutta ei luettu** (`raw`), suurimmat tyypit: sijaintipäivitykset, joita ei ole taulukossa (avatarin,
tankin kuoleman jälkeen, kokonaisuudet, jotka eivät ole luettelossa), paketit 26, 28, 29, 31, 36, 50, 54 ja 57,
joitakin usein toistuvia ajoneuvo- ja avatar-ominaisuuksia, jokainen metodi ja ominaisuus, jolla ei ole lukijaa
(moduulivauriot, miehistö ja kulutustavarat niiden joukossa), sekä kokonaisuuksien luomisen ominaisuudet.

## Ei saatavilla {#not-available}

- Mitä palvelin ei koskaan lähettänyt tallentavalle asiakkaalle: muiden pelaajien tähtäys, kamera ja
  syötteet, viholliset, kun niitä ei ole nähty. Replay on se, mitä yksi asiakas sai tietää.
- Kokonaisuustyyppien, metodien ja ominaisuuksien nimet: ne ovat pelin määritystiedostoissa, eivät replayssa.
  Numerot säilytetään.
- Tykin kohoaminen asteina ja kaikki muu, mikä vaatii tankkien omat tiedot pelin tiedostoista.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
