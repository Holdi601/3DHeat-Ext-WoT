---
title: Conas a léann sé athsheinm
nav_order: 7
lang: "ga"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Conas a léann sé athsheinm {#how-it-reads-a-replay}

Is ceanntásc de bhloic JSON agus sruth paicéad an chluiche athsheinm (nótaí formáide i [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- An chéad bhloc, go soiléir: an léarscáil, leagan an chliaint, an t-imreoir taifeadta, socruithe an fhreastalaí agus an rolla (`vehicles`: ainm, foireann, tanc, eochraithe ag id na feithicle).
- An dara ceann, nuair a mhair an taifeadadh go dtí an deireadh: scáileán na dtorthaí - líne gach feithicle (lámhaigh, buillí, treáiteacha, damáiste a rinneadh, a fuarthas, a blocáladh agus a chuidíodh, aimsiú, xp, creidmheasanna, éachtaí...), sonraí an imreora taifeadta in aghaidh na sprice, na cuntais, fad an chluiche, buaiteoir agus cúis chríochnaithe; i roinnt módanna an t-aon rolla iomlán (ní liostaíonn ceanntásc na liostaí sin ach an fhoireann féin).
- An sruth paicéad, comhbhrúite le zlib agus criptithe le Blowfish le heochair a iompraíonn an cluiche, a bhfuil foilsithe ag uirlisí an phobail a léann na comhaid seo ó 2013.

Is iad **suíomhanna** nuashonruithe suímh an einsin: id feithicle, a suíomh agus a threo, aimsithe de réir a gcruth seachas a n-uimhir phaicéid, mar sin ní fholmhaíonn paiste a athuimhríonn iad an tábla. Is iad an méid a dúradh leis an gcliant taifeadta: a fhoireann féin ar fud an chatha, namhaid ach amháin nuair a aimsíodh é (nó laistigh de raon an chliaint). Níl aon sraitheanna ag feithicil nár aimsíodh riamh. Stopann sraitheanna feithicle ag a bás.

**An chuid eile den sruth** - sláinte, lámhaigh, lorgairí, pléascanna, buillí, uillinneacha gunna, nuashonruithe airéine - is glaonna modha agus athruithe airíonna na bhfeithiclí agus avatar an chliaint iad, uimhrithe ag comhaid sainmhínithe an chluiche, a athraíonn le paistí (uimhríonn 1.12 agus 2.4 iad ar bhealach difriúil). Aimsítear gach ceann de réir chruth a argóintí agus conas a cheanglaíonn siad - féach [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - agus tá na huimhreacha a fuarthas i `decoded` na cáipéise cluiche. Is paicéid dá gcuid féin iad comhrá, mód an cheamara agus imeachtaí féin an chliaint. Is pickles Python iad nuashonruithe airéine agus imeachtaí cliaint; léann léitheoir iad a iompaíonn gach aicme a ainmníonn siad ina n-ionadaí támh agus nach rithfidh aon rud.

Tá an méid a dúradh leis an gcliant iomlán dá fhoireann féin agus páirteach do naimhde: tá a gcuid lámhaigh, buillí agus athruithe sláinte ann fad a bhí siad i raon.

**Tús an chatha** is é nuair a deir an nuashonrú airéine gur thosaigh tréimhse an chatha; in athsheinm gan é, an chéad nóiméad inar ghluais feithicil ar bith.

**Básanna:** is é an t-am teachtaireacht maraithe na hairéine (1.x), nó an t-athrú sláinte a chuir deireadh leis an bhfeithicil, nó tús an chatha móide `lifeTime` an íobartaigh ó na torthaí (soicindí iomlána). Is é an áit an áit inar chonacthas an t-íobartach go deireanach, nuair a bhí sin laistigh de chúig soicind óna bhás; nó, ar chliaint 2.x, an áit a thugann na torthaí (x agus z, gan airde), sa cháipéis chluiche amháin. Níl aon bhásanna ag taifeadadh a stop roimh an deireadh.

**Gan léamh:**

- Aimsiú agus an mionléarscáil: níl siad sa sruth mar imeachtaí dá gcuid féin.
- Ardú an ghunna i gcéimeanna: tá céim idir teorainneacha an ghunna sa sruth, agus tá na teorainneacha i gcomhaid feithiclí an chluiche.
- Damáiste modúil, gortuithe criú, earraí inchaite agus lón catha: níorbh fhéidir na glaonna a iompraíonn iad a idirdhealú de réir cruth amháin thar 1.12 agus 2.4.
- Paicéid chruthaithe eintiteas thar an eintiteas agus a chineál: coinníonn siad gach airí d'fheithicil ag teacht isteach i radharc an chliaint ag an am céanna, in ord nach dtugann ach comhaid shainmhínithe (coinnithe iomlán sa chomhad cliatháin).
- Imbhuailtí statacha (crainn, tithe), aim féin an imreora taifeadta agus paicéid fhisice.
- Uimhreacha orduithe comhrá catha mar ainmneacha: is é an cluiche a uimhríonn agus athraíonn sé; coinníonn an cháipéis chluiche argóintí gach ordaithe, eatarthu a eochair nuair atá ceann aige (`ATTACK_ENEMY`, ...).
- Cúiseanna ionsaithe os cionn 5: scríofa mar uimhreacha amháin.

## Conas a seiceáladh an léamh {#how-the-reading-was-checked}

Seiceáladh an léamh ar athsheinmeanna poiblí de chliaint 1.12 agus 2.4, gach luach i gcoinne ruda a thugann an athsheinm an dara huair:

- **Suíomhanna:** tá rian ag gach tanc a chonacthas riamh ag deich sampla sa soicind; fanann luasanna laistigh den méid is féidir le tanc; aontaíonn an treo le treo an taistil go dtí thart ar 0.02 rad; nuair a thugann na torthaí áit báis, tá an áit a léadh anseo laistigh de chúpla méadar de.
- **An t-imreoir taifeadta:** is ionann na lámhaigh agus an damáiste a rinneadh a léadh agus luachanna na dtorthaí, ar gach athsheinm a seiceáladh.
- **Sláinte:** is ionann sláinte dheireanach gach tanc a léadh agus ceann na dtorthaí; ní bhíonn an damáiste a fuarthas a léadh níos mó ná ceann na dtorthaí. Ar 2.4 ní sheoltar an buille marfach go minic chuig tanc lasmuigh de radharc an chliaint.
- **Buillí:** is ionann damáiste buille agus an t-athrú sláinte ag an nóiméad sin do bheagnach gach buille.
- **Tuirlingt:** ag lámhaigh, díríonn treo an choirp móide yaw na tuirlinge ar an áit ar eitil an lorgaire, laistigh de thart ar 0.01 rad (airmheán).
- **Básanna agus tús an chatha:** laistigh de thart ar shoicind den méid a deir na torthaí agus an airéine.

Tógann na tástálacha athsheinmeanna sa leagan amach céanna, mar sin ní choinnítear aon athsheinm fíor sa stóras seo.

**Gan seiceáil:** cliaint roimh 1.12, athsheinmeanna consóil agus Blitz (cluichí difriúla), Mir Tankov Lesta (`.mtreplay`), agus módanna seachas cathanna randamacha agus cineál catha 20.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
