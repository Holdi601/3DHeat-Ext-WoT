---
title: An cháipéis chluiche
nav_order: 6
lang: ga
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# An cháipéis chluiche {#the-match-document}

Coinníonn `<match>.match.json` gach rud a deir an athsheinm nach sraith den tábla é. Léann cluaisín Cluiche na faire é. (Glaonn an cód an achoimre air.)

![Tús cáipéise cluiche sintéisigh, agus a heochracha](../assets/img/match-document.svg)

## An cath {#the-battle}

| Eochair | Cad é |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; id an chatha; id na léarscáile agus a hainm taispeána |
| `clientVersion`, `streamVersion` | leagan an chluiche ón gceanntásc, agus mar a deir an sruth paicéad é |
| `recorded` | cathain a taifeadadh an athsheinm, mar a scríobhann an cluiche é |
| `player`, `vehicle` | an t-imreoir taifeadta agus a thanc |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | uimhir chineál catha an cheanntáisc, mód cluiche, freastalaí, réigiún, agus ar suiteáladh módanna |
| `duration` | fad an chatha i soicindí, ó na torthaí |
| `winnerTeam`, `finishReason` | an fhoireann bhuaiteach agus uimhir an chluiche don chaoi ar chríochnaigh an cath, ó na torthaí |
| `complete`, `truncated` | tá na torthaí san athsheinm; stop an taifeadadh go luath |
| `battleStart`, `battleStartFrom`, `firstMovement` | tús an chatha i soicindí den taifeadadh; `arena` (dúirt an cluiche é) nó `movement` (an chéad nóiméad inar ghluais tanc ar bith); an chéad ghluaiseacht sin |
| `recordingSeconds` | fad an taifeadta i soicindí |
| `positionPacket`, `hz`, `positions` | uimhir an phaicéid inar tháinig na suíomhanna, samplaí sa soicind, sraitheanna suímh |
| `events` | líon sraitheanna an tábla de gach imeacht |
| `units` | `metres; x east, y up, z north` |
| `decoded` | an modh agus uimhreacha paicéad a fuarthas do gach cineál teachtaireachta |

## Imreoirí agus imeachtaí {#players-and-events}

| Eochair | Cad é |
|---|---|
| `players` | iontráil amháin do gach tanc: ainm, foireann, tanc, clan, samplaí, maruithe, damáiste a rinneadh, slán, am saoil; `seen` (na lámhaigh agus an damáiste a chonaic an cliant taifeadta); iontráil iomlán an cheanntáisc agus na dtorthaí, agus an chuntais |
| `kills` | gach bás: am (soicindí), cá as a tháinig an t-am (`arena`, `health` nó `lifeTime`), íobartach, marfóir, uimhir agus ainm na cúise |
| `periods` | tréimhsí an chatha (ag fanacht, réamhchath, cath, iarchath) le hamanna deiridh an fhreastalaí |
| `basePoints` | dul chun cinn gabhála bunáite in aghaidh na foirne agus na bunáite |
| `chat`, `commands` | línte comhrá; orduithe comhrá catha lena n-argóintí ar fad |
| `camera`, `clientEvents` | módanna ceamara an imreora taifeadta; an méid a thaifead an cliant fúithi féin (formhéadú, uath-aim, athruithe sprice, stát feithicle) |
| `arenaUpdates` | gach nuashonrú airéine, díchódaithe, mar a sheol an cluiche é |

## Torthaí agus seiceálacha {#results-and-checks}

| Eochair | Cad é |
|---|---|
| `serverSettings` | socruithe an fhreastalaí ón gceanntásc |
| `results`, `resultVehicles`, `frags` | scáileán na dtorthaí: coitianta, pearsanta (le sonraí in aghaidh na sprice), imreoirí, cuntais; líne torthaí gach tanc; maruithe in aghaidh an imreora |
| `entities` | gach eintiteas a chruthaíonn an sruth: a uimhir chineáil agus a ról, cathain a tháinig isteach i radharc an chliaint agus cathain a d'fhág |
| `selfCheck` | comhaireamh na hiomláine ([Iomláine](completeness.md)) agus seiceálacha na n-eintiteas agus an leagain |

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
