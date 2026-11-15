---
title: "Úplnost"
nav_order: 8
lang: "cs"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Úplnost {#completeness}

Nic z replaye se nezahazuje. Co převodník čte, jde do tabulky a dokumentu zápasu; každá další položka se drží celá
v doplňku `<match>.messages.parquet`; a `selfCheck.completeness` dokumentu zápasu počítá, co se stalo s každým
druhem položky. Toto je pravidlo, které sdílejí všechny převodníky 3DHeat:
[Převodníky zachovávají vše](https://holdi601.github.io/3DHeat/converters.html).

![Vlastní kontrola syntetického replaye: každá položka viděna, přečtena, ponechána nebo ztracena](../assets/img/completeness.svg)

## Počet {#the-count}

Pro každý druh položky dává `selfCheck.completeness.types`:

| Počet | Znamená |
|---|---|
| `seen` | kolik jich replay obsahuje |
| `decoded` | přečteno celé |
| `partial` | přečteno zčásti a drženo celé v doplňku |
| `raw` | drženo celé jen v doplňku, nepřečteno |
| `lost` | ztraceno: vždy `0` |

Druhy jsou vlastní druhy replaye: `block 0` (hlavička), `block 1` (výsledky), `container sizes` a `deflate tail`
(vlastní bajty kontejneru), `packet <type>`, a u volání nad entitami `method <entity type>.<number>`
a `property <entity type>.<number>`. Typy entit jsou čísla, která dávají vytvářecí pakety;
`selfCheck.entities.roles` říká, který je avatar hráče, který nahrával, a které jsou vozidla. Druh, o kterém
nikdo nevěděl, se objeví se svým počtem.

## Doplněk {#the-sidecar}

| Sloupec | Co |
|---|---|
| `time` | hodiny replaye, jako v tabulce |
| `type`, `name` | druh položky; jak ji převodník nazývá, kde ji čte |
| `entity` | vozidlo nebo avatar, ke kterému patří, jako `entity` v tabulce |
| `decoded` | co se z ní přečetlo, jako JSON |
| `payload`, `text` | její bajty, celé; bloky JSON, celé |
| `entityType`, `packet`, `method` | čísla |

Řádky jsou seřazeny podle paketu, metody, entity a času.

## Co se čte a jak bylo ověřeno {#what-is-read-and-how-it-was-checked}

- **Sklon a náklon** každé pozice: sklon je minus svah vlastní dráhy tanku, když jede vpřed; dva tanky na jednom
  místě se stejným kurzem mají stejný náklon, s opačnými kurzy opačné náklony.
- **Entity** (`entities`): kdy se každá dostala do zorného pole klienta a kdy z něj odešla.
  Žádný tank nemá pozici mezi odchodem a návratem.
- **Verze ve streamu** (`streamVersion`): stejná jako v hlavičce.
- **Míření hráče, který nahrával** (paket 38): směr, v `decoded` doplňku (`forward`); u výstřelů hráče je to zlomek
  stupně od místa, kam střela letěla.

Vše ostatní, co se čte (zdraví, zásahy, výstřely, stopy, výbuchy, úhly děla, aktualizace arény, chat, režimy
kamery, události klienta, pozice), je `partial`: v tabulce nebo v dokumentu zápasu a drženo celé v doplňku.

**Drženo, ale nečteno** (`raw`), největší druhy: aktualizace pozic, které nejsou v tabulce (avatara po smrti tanku,
entity mimo soupisku), pakety 26, 28, 29, 31, 36, 50, 54 a 57, některé časté vlastnosti vozidel a avatarů,
každá metoda a vlastnost bez čtečky (mezi nimi poškození modulů, posádka a spotřební materiál), a vlastnosti
vytvoření entit.

## Není k dispozici {#not-available}

- Co server nikdy neposlal hráči, který nahrával: míření, kamera a vstupy ostatních hráčů, nepřátelé, dokud nejsou
  spatřeni. Replay je to, co jeden klient dostal.
- Názvy typů entit, metod a vlastností: jsou v definičních souborech hry, ne v replayi. Čísla se drží.
- Sklon děla ve stupních a cokoli jiného, co potřebuje vlastní data tanků ze souborů hry.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
