---
title: "Úplnosť"
nav_order: 8
lang: sk
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Úplnosť {#completeness}

Nič z replaye sa nevyhodí. To, čo konvertor číta, ide do tabuľky a dokumentu zápasu; každá ďalšia položka sa uchová
celá v sprievodnom súbore `<match>.messages.parquet`; a položka `selfCheck.completeness` dokumentu zápasu počíta, čo sa
stalo s každým druhom položky. Toto je pravidlo, ktoré zdieľajú všetky konvertory 3DHeat:
[Konvertory zachovávajú všetko](https://holdi601.github.io/3DHeat/converters.html).

![Samokontrola syntetického replaye: každá položka videná, prečítaná, uchovaná alebo stratená](../assets/img/completeness.svg)

## Počet {#the-count}

Pre každý druh položky dáva `selfCheck.completeness.types`:

| Počet | Znamená |
|---|---|
| `seen` | koľko ich replay obsahuje |
| `decoded` | prečítané celé |
| `partial` | prečítané čiastočne a uchované celé v sprievodnom súbore |
| `raw` | len uchované celé v sprievodnom súbore, nečítané |
| `lost` | stratené: vždy `0` |

Druhy sú replaye vlastné: `block 0` (hlavička), `block 1` (výsledky), `container sizes` a `deflate tail` (vlastné bajty
kontajnera), `packet <type>` a pre volania na entitách `method <entity type>.<number>` a `property <entity type>.<number>`.
Typy entít sú čísla, ktoré dávajú vytvárajúce pakety; `selfCheck.entities.roles` hovorí, ktorý je avatar hráča, ktorý
replay nahral, a ktoré sú vozidlá. Druh, o ktorom nikto nevedel, sa ukáže so svojím počtom.

## Sprievodný súbor {#the-sidecar}

| Stĺpec | Čo |
|---|---|
| `time` | hodiny replaye, ako v tabuľke |
| `type`, `name` | druh položky; ako ju konvertor volá, tam, kde ju číta |
| `entity` | vozidlo alebo avatar, ktorému patrí, ako `entity` v tabuľke |
| `decoded` | čo sa z nej prečítalo, ako JSON |
| `payload`, `text` | jej bajty, celé; bloky JSON, celé |
| `entityType`, `packet`, `method` | čísla |

Riadky sú zoradené podľa paketu, metódy, entity a času.

## Čo sa číta a ako sa to overilo {#what-is-read-and-how-it-was-checked}

- **Sklon a náklon** každej polohy: sklon je mínus sklon vlastnej dráhy tanku, kým jazdí dopredu; dva tanky na jednom
  mieste s jedným smerom majú rovnaký náklon, s opačnými smermi opačné náklony.
- **Entity** (`entities`): kedy sa každá dostala do pohľadu klienta a kedy z neho odišla. Žiadny tank nemá polohu medzi
  odchodom a návratom.
- **Verzia v toku** (`streamVersion`): rovnaká ako v hlavičke.
- **Mierenie hráča, ktorý replay nahral** (paket 38): smer, v sprievodnom súbore v `decoded` (`forward`); pri výstreloch
  hráča je to zlomok stupňa od miesta, kam letela strela.

Všetko ostatné, čo sa číta (zdravie, zásahy, výstrely, stopy, výbuchy, uhly zbraní, aktualizácie arény, chat, režimy
kamery, vlastné udalosti klienta, polohy), je `partial`: v tabuľke alebo v dokumente zápasu a uchované celé v sprievodnom súbore.

**Uchované, ale nečítané** (`raw`), najväčšie druhy: aktualizácie polôh, ktoré nie sú v tabuľke (avatarove, po smrti
tanku, entity, ktoré nie sú v súpiske), pakety 26, 28, 29, 31, 36, 50, 54 a 57, niektoré časté vlastnosti vozidiel
a avatara, každá metóda a vlastnosť bez čítačky (medzi nimi poškodenie modulov, posádka a spotrebný materiál),
a vlastnosti vytvorení entít.

## Nedostupné {#not-available}

- To, čo server nikdy neposlal klientovi, ktorý nahrával: mierenie, kamera a vstupy iných hráčov, nepriatelia, kým neboli
  spozorovaní. Replay je to, čo jednému klientovi bolo povedané.
- Názvy typov entít, metód a vlastností: sú v definičných súboroch hry, nie v replayi. Čísla sa uchovávajú.
- Uhol dela v stupňoch a čokoľvek iné, čo potrebuje vlastné údaje tankov zo súborov hry.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
