---
title: "Heilleiki"
nav_order: 8
lang: is
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Heilleiki {#completeness}

Ekkert í upptöku er hent. Það sem breytirinn les fer í töfluna og
leikjaskjalið; hvert annað atriði er varðveitt í heild í hliðarskránni
`<match>.messages.parquet`; og `selfCheck.completeness` í leikjaskjalinu
telur hvað varð um hverja tegund atriða. Þetta er reglan sem allir 3DHeat
breytar deila:
[Breytar varðveita allt](https://holdi601.github.io/3DHeat/converters.html).

![Sjálfsathugun tilbúinnar upptöku: hvert atriði séð, lesið, varðveitt eða tapað](../assets/img/completeness.svg)

## Talningin {#the-count}

Fyrir hverja tegund atriða gefur `selfCheck.completeness.types`:

| Talning | Þýðir |
|---|---|
| `seen` | hversu mörg upptakan geymir |
| `decoded` | lesið í heild |
| `partial` | lesið að hluta, og varðveitt í heild í hliðarskránni |
| `raw` | aðeins varðveitt í heild í hliðarskránni, ekki lesið |
| `lost` | tapað: alltaf `0` |

Tegundirnar eru upptökunnar sjálfrar: `block 0` (hausinn), `block 1`
(niðurstöðurnar), `container sizes` og `deflate tail` (eigin bæti gámsins),
`packet <type>`, og fyrir köll á einingar `method <entity type>.<number>`
og `property <entity type>.<number>`. Einingartegundir eru tölurnar sem
pakkarnir sem búa þær til gefa; `selfCheck.entities.roles` segir hver er
avatar upptökumannsins og hverjar eru farartækin. Tegund sem enginn þekkti
birtist með talningu sinni.

## Hliðarskráin {#the-sidecar}

| Dálkur | Hvað |
|---|---|
| `time` | klukka upptökunnar, eins og í töflunni |
| `type`, `name` | tegund atriðisins; hvað breytirinn kallar það, þar sem hann les það |
| `entity` | farartækið eða avatarinn sem það tilheyrir, eins og `entity` í töflunni |
| `decoded` | það sem var lesið úr því, sem JSON |
| `payload`, `text` | bæti þess, í heild; JSON-blokkirnar, í heild |
| `entityType`, `packet`, `method` | tölurnar |

Raðir eru raðaðar eftir pakka, aðferð, einingu og tíma.

## Hvað er lesið, og hvernig það var athugað {#what-is-read-and-how-it-was-checked}

- **Pitch og roll** hverrar stöðu: pitch er mínus halli eigin ferils
  skriðdrekans meðan hann ekur áfram; tveir skriðdrekar á einum stað með sömu
  stefnu hafa sama roll, með gagnstæðar stefnur gagnstæðan roll.
- **Einingar** (`entities`): hvenær hver kom inn í sjónsvið biðlarans og fór úr því.
  Enginn skriðdreki hefur stöðu milli þess að fara og koma aftur.
- **Útgáfan í straumnum** (`streamVersion`): sú sama og í hausnum.
- **Miðun upptökumannsins** (pakki 38): stefna, í `decoded` hliðarskrárinnar
  (`forward`); við skot spilarans er hún brot úr gráðu frá því
  hvert skelin flaug.

Allt annað sem er lesið (heilsa, högg, skot, ljósrákir (tracers), sprengingar, byssuhorn,
uppfærslur vallar, spjall, myndavélarhamir, biðlaraatburðir, stöður) er `partial`:
í töflunni eða leikjaskjalinu, og varðveitt í heild í hliðarskránni.

**Varðveitt en ekki lesið** (`raw`), stærstu tegundirnar: stöðuuppfærslur sem eru ekki í
töflunni (avatarsins, eftir dauða skriðdreka, einingar sem eru ekki á listanum),
pakkar 26, 28, 29, 31, 36, 50, 54 og 57, nokkrir tíðir eiginleikar farartækja og avatara, hver aðferð og eiginleiki
án lesara (meðal annars skemmdir á einingum, áhöfn og
birgðir), og eiginleikar einingarsköpunar.

## Ekki tiltækt {#not-available}

- Það sem þjónninn sendi aldrei upptökubiðlaranum: miðun, myndavél og
  inntak annarra spilara, óvinir meðan þeir eru ósénir. Upptaka er það sem einum biðlara
  var sagt.
- Nöfn einingartegunda, aðferða og eiginleika: þau eru í
  skilgreiningarskrám leiksins, ekki í upptökunni. Tölurnar eru varðveittar.
- Hæð byssunnar í gráðum og allt annað sem þarf eigin gögn skriðdrekanna
  úr skrám leiksins.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
