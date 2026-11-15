---
title: "Vollstännegkeet"
nav_order: 8
lang: lb
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Vollstännegkeet {#completeness}

Näischt an engem Replay gëtt ewechgeheit. Wat de Konverter liest, kënnt an d'
Tabell an d'Match-Dokument; all anert Stéck gëtt ganz an der Niewendatei
`<match>.messages.parquet` behalen; an dem Match-Dokument säin
`selfCheck.completeness` zielt, wat aus all Aart Stéck ginn ass. Dat ass
d'Regel, déi all 3DHeat-Konverter deelen:
[Konverteren behalen alles](https://holdi601.github.io/3DHeat/converters.html).

![D'Selbstkontroll vun engem synthetesche Replay: all Stéck gesinn, gelies, behalen oder verluer](../assets/img/completeness.svg)

## D'Zielung {#the-count}

Fir all Aart Stéck gëtt `selfCheck.completeness.types`:

| Zuel | Bedeit |
|---|---|
| `seen` | wéi vill de Replay hält |
| `decoded` | ganz gelies |
| `partial` | zum Deel gelies, a ganz an der Niewendatei behalen |
| `raw` | nëmmen ganz an der Niewendatei behalen, net gelies |
| `lost` | verluer: émmer `0` |

D'Aarte sinn déi vum Replay selwer: `block 0` (den Header), `block 1` (d'
Resultater), `container sizes` an `deflate tail` (d'eege Bytes vum Container),
`packet <type>`, a fir Opruffer op Entitéite `method <entity type>.<number>`
an `property <entity type>.<number>`. Entitéitstypen sinn d'Nummeren, déi d'
Erstellungspakete ginn; `selfCheck.entities.roles` seet, wéi ee dem
opuelende Spiller säin Avatar ass a wéi eng d'Gefierer. Eng Aart, déi keen kannt huet,
erschéngt mat hirer Zuel.

## D'Niewendatei {#the-sidecar}

| Kolonn | Wat |
|---|---|
| `time` | d'Auer vum Replay, wéi an der Tabell |
| `type`, `name` | d'Aart vum Stéck; wéi de Konverter et nennt, wou en et liest |
| `entity` | d'Gefier oder den Avatar, zu deem et gehéiert, wéi d'`entity` vun der Tabell |
| `decoded` | wat dovunner gelies gouf, als JSON |
| `payload`, `text` | seng Bytes, ganz; d'JSON-Blöck, ganz |
| `entityType`, `packet`, `method` | d'Nummeren |

D'Zeile sinn no Paket, Method, Entitéit an Zäit sortéiert.

## Wat gelies gëtt, a wéi et gepréift gouf {#what-is-read-and-how-it-was-checked}

- **Pitch a Roll** vun all Positioun: d'Pitch ass minus dem Hang vum eegene Wee vum
  Panzer, während en no vir fiert; zwee Panzer op engem Punkt mat engem Heading
  hunn dee selwechte Roll, bei entgéintgesate Headings entgéintgesate Roll.
- **Entitéiten** (`entities`): wéini all an de Bléck vum Client koum a fortgaang ass.
  Kee Panzer huet eng Positioun tëscht dem Fortgoen an dem Zréckkommen.
- **D'Versioun am Stroum** (`streamVersion`): déiselwecht wéi déi vum Header.
- **D'Ziel vum opuelende Spiller** (Paket 38): eng Richtung, am `decoded` vun der
  Niewendatei (`forward`); bei de Schëss vum Spiller ass et e Bruchdeel vun engem Grad
  vun deem, wou d'Granat geflunn ass.

Alles anescht, wat gelies gëtt (Liewen, Treffer, Schëss, Leuchtspuren, Explosiounen, Kanounwénkel,
Arena-Updates, Chat, Kameramoduse, Client-Evenementer, Positiounen), ass `partial`:
an der Tabell oder dem Match-Dokument, a ganz an der Niewendatei behalen.

**Behalen, awer net gelies** (`raw`), déi gréissten Aarten: Positiouns-Updates, déi net an
der Tabell sinn (dee vum Avatar, no engem Panzerdoud, Entitéiten, déi net an der Roster sinn),
d'Pakete 26, 28, 29, 31, 36, 50, 54 an 57, e puer heefeg Propriétéite vu Gefierer an Avatar,
all Method a Propriétéit ouni Reader (ënnert anerem Modulschued, Crew
a Verbrauchsgidder), an d'Propriétéite vun Entitéit-Erstellungen.

## Net verfügbar {#not-available}

- Wat de Server dem opuelende Client ni geschéckt huet: d'Ziel, d'Kamera an d'Inputs vun
  anere Spiller, Feinde, wann net entdeckt. E Replay ass dat, wat een Client
  gesot krut.
- D'Nimm vun Entitéitstypen, Methoden a Propriétéiten: si sinn an den
  Definitiounsdateie vum Spill, net am Replay. D'Nummere ginn behalen.
- D'Elevatioun vun der Kanoun a Grad an alles anescht, wat d'eege Daten vun de Panzer
  aus den Dateie vum Spill brauch.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
