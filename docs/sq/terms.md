---
title: "Kushtet dhe licenca"
nav_order: 9
lang: "sq"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Kushtet dhe licenca {#terms-and-licence}

## Kushtet e Wargaming {#wargamings-terms}

Lexuar më 2026-11-07, Wargaming EULA versioni 14 (në fuqi nga 10 prilli 2024, listuar
si aktuale):

- 5.3 (b): unless authorised in writing, you must not "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): prohibited is "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

Lista e mod-eve të ndaluara e World of Tanks ka të bëjë me vetë betejën: mod-e që
"reveal the position of enemies in a way not included in the client",
bot-e synimi, kohëmatës rimbushjeje e të ngjashme. As EULA, as ajo listë nuk i
përmend riluajtjet.

Çfarë bën ky konvertues: lexon një skedar që e shkroi loja, pas betejës,
jashtë lojës. Nuk ndryshon asgjë në lojë, nuk komunikon me asnjë server dhe
nuk shfaq asgjë gjatë një beteje. Ai e deshifron rrjedhën me çelësin e lojës,
gjë që 5.3 (b) dhe 12.1 (p) mund të lexohen si e mbulojnë. Përdorimi i tij është
vendim i përdoruesit; prandaj është paketë e veçantë.

## Licenca dhe burimet {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Ka nevojë për numpy (BSD-3-Clause) dhe pyarrow
(Apache-2.0). Shkruar për këtë projekt: shifra Blowfish këtu është e vetja,
me tabelat e llogaritura nga shifrat e pi-t siç i përcakton shifra.
Faktet për formatin (kontejneri, shifra, paketa e pozicionit) janë
njohuri e përbashkët mes mjeteve të riluajtjeve - evido/wotreplay-parser (BSD-3-Clause)
i dokumenton; nuk u mor kod prej tij ose nga ndonjë projekt tjetër.

`bigworld.py` dhe `table.py` janë të njëjtët skedarë si te konvertuesi i World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); ndryshoji të dy bashkë.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
