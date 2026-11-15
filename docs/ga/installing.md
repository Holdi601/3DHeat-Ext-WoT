---
title: Suiteáil
nav_order: 3
lang: "ga"
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Suiteáil {#installing}

Nua leis an líne ordaithe? Léigh [Sula dtosaíonn tú](before-you-start.md) ar dtús. Teastaíonn Python 3.10 nó níos déanaí; suiteáiltear numpy agus pyarrow leis.

## Céim ar chéim {#step-by-step}

1. Faigh an cód: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`, nó íoslódáil zip ó [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases) agus díphacáil é.
2. Oscail teirminéal sa fhillteán sin agus clóscríobh `pip install -e .`. Cuireann sé seo an t-ordú `heat3d-wot-replay` ar do chonair.
3. Seiceáil é: `heat3d-wot-replay --version`. Ba cheart duit `heat3d-wot-replay 0.1.0` a fheiceáil. Liostaíonn `heat3d-wot-replay --help` na roghanna:

![heat3d-wot-replay --help](../assets/img/help.svg)

Gan suiteáil, déanann `python -m heat3d_ext_wot ...` i bhfillteán na huirlise an rud céanna.

Ritheann 3DHeat Watcher an t-ordú seo ar athsheinmeanna nua nuair atá sé suiteáilte, agus oibríonn sé gan é.

## Nuashonruithe {#updates}

Seiceálann gach tús ar dtús eisiúintí GitHub an tionscadail (ceann amháin ar a mhéad gach cúpla uair an chloig; ní stopann sé tiontú choíche, ar líne nó as líne). Nuair a bhíonn eisiúint níos nuaí amuigh, fiafraíonn an t-ordú sula suiteálann sé í: nuashonraítear `git clone` le `git pull --ff-only` (diúltaítear dó cé go bhfuil athruithe áitiúla agat), cóip íoslódáilte ó chartlann na heisiúna. Cuireann `HEAT3D_NO_UPDATE=1` an seiceáil agus an nuashonrú as.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
