---
title: "Voorwaarden en licentie"
nav_order: 9
lang: "nl"
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Voorwaarden en licentie {#terms-and-licence}

## De voorwaarden van Wargaming {#wargamings-terms}

Gelezen op 2026-11-07, Wargaming EULA versie 14 (van kracht vanaf 10 april 2024, vermeld
als actueel):

- 5.3 (b): tenzij schriftelijk toegestaan, mag je niet "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): verboden is "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

De lijst van verboden mods van World of Tanks gaat over het gevecht zelf: mods die
"reveal the position of enemies in a way not included in the client", aimbots, herlaadtimers en
dergelijke. Noch de EULA noch die lijst noemt replays.

Wat deze converter doet: hij leest een bestand dat het spel schreef, na het gevecht, buiten het spel. Hij
verandert niets aan het spel, praat met geen enkele server, en toont niets tijdens een gevecht. Hij ontcijfert
de stroom wel met de sleutel van het spel, wat volgens 5.3 (b) en 12.1 (p) gelezen kan worden als
gedekt. Het gebruik ervan is de beslissing van de gebruiker; daarom is het een apart pakket.

## Licentie en bronnen {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Heeft numpy (BSD-3-Clause) en pyarrow
(Apache-2.0) nodig. Voor dit project geschreven: de Blowfish-cijfer hier is zelf gemaakt, met tabellen die
berekend zijn uit de cijfers van pi zoals het cijfer ze voorschrijft.
Feiten over het formaat (de container, het cijfer, het positiepakket) zijn algemeen bekend onder replaytools -
evido/wotreplay-parser (BSD-3-Clause) beschrijft ze; er is geen code van die of van enig ander project overgenomen.

`bigworld.py` en `table.py` zijn dezelfde bestanden als in de converter voor World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); wijzig ze altijd samen.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
