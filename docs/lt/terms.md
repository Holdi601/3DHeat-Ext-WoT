---
title: Sąlygos ir licencija
nav_order: 9
lang: "lt"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Sąlygos ir licencija {#terms-and-licence}

## Wargaming sąlygos {#wargamings-terms}

Perskaityta 2026-11-07, Wargaming EULA 14 versija (galioja nuo 2024 m. balandžio 10 d., nurodyta kaip dabartinė):

- 5.3 (b): jei raštu neleista, negalite "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): draudžiama "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

World of Tanks draudžiamų modifikacijų sąrašas susijęs su pačiu mūšiu: modifikacijos, kurios
"reveal the position of enemies in a way not included in the client", taikymo robotai,
perkrovimo laikmačiai ir panašiai. Nei EULA, nei tas sąrašas nemini įrašų.

Ką daro šis konverteris: jis skaito failą, kurį žaidimas įrašė po mūšio, žaidimo ribų išorėje.
Jis nieko nekeičia žaidime, su jokiu serveriu nesikalba ir mūšio metu nieko nerodo. Tiesa, jis iššifruoja srautą
žaidimo raktu, ir 5.3 (b) bei 12.1 (p) galima aiškinti taip, kad tai patenka. Naudoti jį yra vartotojo sprendimas;
todėl jis yra atskiras paketas.

## Licencija ir šaltiniai {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Reikia numpy (BSD-3-Clause) ir pyarrow
(Apache-2.0). Parašyta šiam projektui: čia esantis Blowfish šifras yra jo paties, o jo lentelės apskaičiuotos iš
skaitmenų, kuriuos šifras apibrėžia pagal skaičių pi. Faktai apie formatą (konteinerį, šifrą, pozicijos paketą) įrankiai,
skaitantys įrašus, žino bendrai - evido/wotreplay-parser (BSD-3-Clause) juos aprašo; joks kodas iš jo ar iš kito
projekto nepaimtas.

`bigworld.py` ir `table.py` yra tie patys failai, kaip ir World of Warships konverteryje
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); keiskite abu kartu.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
