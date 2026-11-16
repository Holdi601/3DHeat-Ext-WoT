---
title: Begriffe und Lizenz
nav_order: 9
lang: "de"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Begriffe und Lizenz {#terms-and-licence}

## Was er liest {#what-it-reads}

Der Umwandler liest Replay-Dateien, die das Spiel auf deinem eigenen Computer
geschrieben hat, nach dem Gefecht und außerhalb des Spiels. Er verändert
nichts am Spiel, spricht mit keinem Server und zeigt während eines Gefechts
nichts an. Nichts aus dem Spiel wird mit ihm ausgeliefert oder weitergegeben:
keine Spieldaten, kein Spielcode, keine DLLs. Was er schreibt, bleibt auf
deinem Computer.

3DHeat ist nicht mit Wargaming verbunden und wird nicht von Wargaming
unterstützt. World of Tanks und zugehörige Namen und Marken gehören ihren
Inhabern.

Rechteinhaber: Ein Issue unter
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> genügt - wir antworten
schnell und entfernen auf Anfrage alles.

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
