---
title: Begriffe und Lizenz
nav_order: 9
lang: de
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Begriffe und Lizenz {#terms-and-licence}

## Die Bedingungen von Wargaming {#wargamings-terms}

Gelesen am 2026-11-07, Wargaming-EULA Version 14 (gültig ab 10. April 2024, als aktuell
aufgeführt). Die Zitate sind der englische Originaltext der EULA und bleiben englisch:

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

Die Liste verbotener Mods von World of Tanks betrifft das Gefecht selbst: Mods, die
"reveal the position of enemies in a way not included in the client" zeigen, Zielbots,
Nachladeanzeigen und Ähnliches. Weder die EULA noch diese Liste erwähnt Replays.

Was dieser Umwandler tut: Er liest eine Datei, die das Spiel nach dem Gefecht geschrieben
hat, außerhalb des Spiels. Er verändert nichts am Spiel, spricht mit keinem Server und
zeigt während eines Gefechts nichts an. Er entschlüsselt den Strom mit dem Schlüssel des
Spiels, was sich so lesen lässt, dass 5.3 (b) und 12.1 (p) es abdecken. Ihn zu benutzen ist
die Entscheidung des Nutzers; deshalb ist er ein eigenes Paket.

## Lizenz und Quellen {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Braucht numpy (BSD-3-Clause) und pyarrow
(Apache-2.0). Für dieses Projekt geschrieben: Die Blowfish-Chiffre hier ist eigene
Arbeit, deren Tabellen aus den Ziffern von Pi berechnet werden, so wie die Chiffre es
vorschreibt. Fakten über das Format (der Container, die Chiffre, das Paket der Position)
sind unter Replay-Werkzeugen allgemein bekannt - evido/wotreplay-parser (BSD-3-Clause)
dokumentiert sie; es wurde kein Code daraus oder aus einem anderen Projekt übernommen.

`bigworld.py` und `table.py` sind dieselben Dateien wie im Umwandler für World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); beide immer zusammen ändern.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
