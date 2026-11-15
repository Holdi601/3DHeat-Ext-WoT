---
title: Iomláine
nav_order: 8
lang: ga
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Iomláine {#completeness}

Ní chaitear aon rud in athsheinm uait. Téann an méid a léann an tiontaire isteach sa tábla agus sa cháipéis chluiche; coinnítear gach mír eile iomlán sa chomhad cliatháin `<match>.messages.parquet`; agus comhairíonn `selfCheck.completeness` na cáipéise cluiche cad a tharla do gach cineál míre. Is é seo an riail a roinneann gach tiontaire 3DHeat: [Coimeádann tiontairí gach rud](https://holdi601.github.io/3DHeat/converters.html).

![Féinseiceáil athsheinm sintéisigh: gach mír a chonacthas, a léadh, a coinníodh nó a cailleadh](../assets/img/completeness.svg)

## An comhaireamh {#the-count}

Do gach cineál míre, tugann `selfCheck.completeness.types`:

| Comhaireamh | Ciallaíonn sé |
|---|---|
| `seen` | cé mhéad atá san athsheinm |
| `decoded` | léite iomlán |
| `partial` | léite i bpáirt, agus coinnithe iomlán sa chomhad cliatháin |
| `raw` | coinnithe iomlán sa chomhad cliatháin amháin, gan léamh |
| `lost` | caillte: i gcónaí `0` |

Is iad cineálacha na hathsheinme féin iad na cineálacha: `block 0` (an ceanntásc), `block 1` (na torthaí), `container sizes` agus `deflate tail` (beartanna féin an choimeádáin), `packet <type>`, agus do ghlaonna ar eintitis `method <entity type>.<number>` agus `property <entity type>.<number>`. Is iad na huimhreacha a thugann na paicéid chruthaithe cineálacha eintitis; deir `selfCheck.entities.roles` cé acu avatar an imreora taifeadta agus cé acu na feithiclí. Taispeánann cineál nach raibh a fhios ag aon duine faoi lena chomhaireamh.

## An comhad cliatháin {#the-sidecar}

| Colún | Cad é |
|---|---|
| `time` | clog na hathsheinme, mar atá sa tábla |
| `type`, `name` | an cineál míre; an t-ainm a thugann an tiontaire air, nuair a léann sé é |
| `entity` | an fheithicil nó an avatar dá mbaineann sé, mar `entity` an tábla |
| `decoded` | an méid a léadh de, mar JSON |
| `payload`, `text` | a bheartanna, iomlán; na bloic JSON, iomlán |
| `entityType`, `packet`, `method` | na huimhreacha |

Sórtáiltear sraitheanna de réir paicéid, modha, eintitis agus ama.

## Cad a léitear, agus conas a seiceáladh é {#what-is-read-and-how-it-was-checked}

- **Pitch agus roll** gach suímh: is é an pitch lúide fána chosán féin an tanc fad a thiomáineann sé ar aghaidh; tá an roll céanna ag dhá thanc ag áit amháin le heading amháin, rolls urchomhaireacha le headings urchomhaireacha.
- **Eintitis** (`entities`): cathain a tháinig gach ceann isteach i radharc an chliaint agus cathain a d'fhág. Níl aon suíomh ag tanc ar bith idir imeacht agus teacht ar ais.
- **An leagan sa sruth** (`streamVersion`): mar an gcéanna le leagan an cheanntáisc.
- **Aim an imreora taifeadta** (paicéad 38): treo, i `decoded` an chomhaid chliatháin (`forward`); ag lámhaigh an imreora is codán céime é ón áit ar eitil an sliogán.

Tá gach rud eile a léadh (sláinte, buillí, lámhaigh, lorgairí, pléascanna, uillinneacha gunna, nuashonruithe airéine, comhrá, módanna ceamara, imeachtaí cliaint, suíomhanna) `partial`: sa tábla nó sa cháipéis chluiche, agus coinnithe iomlán sa chomhad cliatháin.

**Coinnithe ach gan léamh** (`raw`), na cineálacha is mó: nuashonruithe suímh nach bhfuil sa tábla (an avatar, tar éis bháis tanc, eintitis nach bhfuil sa rolla), paicéid 26, 28, 29, 31, 36, 50, 54 agus 57, roinnt airíonna minice feithicle agus avatar, gach modh agus airí gan léitheoir (damáiste modúil, criú agus earraí inchaite ina measc), agus airíonna cruthaithe eintiteas.

## Gan a bheith ar fáil {#not-available}

- An méid nár sheol an freastalaí chuig an gcliant taifeadta riamh: aim, ceamara agus ionchuir imreoirí eile, naimhde nuair nár aimsíodh iad. Is é athsheinm an méid a dúradh le cliant amháin.
- Ainmneacha cineálacha eintitis, modhanna agus airíonna: tá siad i gcomhaid shainmhínithe an chluiche, ní san athsheinm. Coinnítear na huimhreacha.
- Ardú an ghunna i gcéimeanna agus aon rud eile a theastaíonn sonraí féin na dtancanna ó chomhaid an chluiche.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
