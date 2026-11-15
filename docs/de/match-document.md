---
title: Das Match-Dokument
nav_order: 6
lang: "de"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Das Match-Dokument {#the-match-document}

`<match>.match.json` enthält alles, was das Replay sagt und das keine Zeile der
Tabelle ist. Der Reiter Match des Viewers liest es. (Der Code nennt es die Zusammenfassung.)

![Der Anfang eines synthetischen Match-Dokuments und seine Schlüssel](../assets/img/match-document.svg)

## Das Gefecht {#the-battle}

| Schlüssel | Was |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; die Kennung des Gefechts; die Kennung der Karte und ihr Anzeigename |
| `clientVersion`, `streamVersion` | die Spielversion aus dem Kopf und so, wie der Paketstrom sie angibt |
| `recorded` | wann das Replay aufgenommen wurde, so wie das Spiel es schreibt |
| `player`, `vehicle` | der aufnehmende Spieler und sein Panzer |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | die Gefechtsart-Nummer aus dem Kopf, der Spielmodus, der Server, die Region und ob Mods installiert waren |
| `duration` | die Länge des Gefechts in Sekunden, aus den Ergebnissen |
| `winnerTeam`, `finishReason` | das Siegerteam und die Nummer des Spiels dafür, wie das Gefecht endete, aus den Ergebnissen |
| `complete`, `truncated` | die Ergebnisse stehen im Replay; die Aufnahme stoppte früh |
| `battleStart`, `battleStartFrom`, `firstMovement` | der Beginn des Gefechts in Sekunden der Aufnahme; `arena` (die Arena sagte es) oder `movement` (der erste Moment, in dem sich ein Panzer bewegte); diese erste Bewegung |
| `recordingSeconds` | die Länge der Aufnahme in Sekunden |
| `positionPacket`, `hz`, `positions` | die Paketnummer, in der die Positionen kamen, Messwerte pro Sekunde, Zeilen der Positionen |
| `events` | die Anzahl der Zeilen der Tabelle für jedes Ereignis |
| `units` | `metres; x east, y up, z north` (Meter; x Osten, y oben, z Norden) |
| `decoded` | die Methoden- und Paketnummern, die für jede Art von Nachricht gefunden wurden |

## Spieler und Ereignisse {#players-and-events}

| Schlüssel | Was |
|---|---|
| `players` | ein Eintrag je Panzer: Name, Team, Panzer, Clan, Messwerte, Abschüsse, verursachter Schaden, überlebt, Lebensdauer; `seen` (die Schüsse und der Schaden, die der aufnehmende Client sah); der ganze Eintrag aus Kopf und Ergebnissen und der des Kontos |
| `kills` | jeder Tod: Zeit (Sekunden), woher die Zeit stammt (`arena`, `health` oder `lifeTime`), Opfer, Killer, Nummer und Name des Grundes |
| `periods` | die Phasen des Gefechts (Warten, Vorgefecht, Gefecht, Nachgefecht) mit den Endzeiten des Servers |
| `basePoints` | Fortschritt der Basiseroberung je Team und Basis |
| `chat`, `commands` | Chatzeilen; Gefechts-Chatbefehle mit allen ihren Argumenten |
| `camera`, `clientEvents` | die Kameramodi des aufnehmenden Spielers; was der Client über sich selbst aufgenommen hat (Zoom, Zielhilfe, Zielwechsel, Fahrzeugzustand) |
| `arenaUpdates` | jede Arena-Aktualisierung, dekodiert, so wie das Spiel sie gesendet hat |

## Ergebnisse und Prüfungen {#results-and-checks}

| Schlüssel | Was |
|---|---|
| `serverSettings` | die Einstellungen des Servers aus dem Kopf |
| `results`, `resultVehicles`, `frags` | der Ergebnisbildschirm: allgemein, persönlich (mit den Einzelheiten je Ziel), Spieler, Konten; die Ergebniszeile jedes Panzers; Abschüsse je Spieler |
| `entities` | jede Entität, die der Strom erzeugt: ihre Typnummer und Rolle, wann sie in die Sicht des Clients kam und wann sie sie verließ |
| `selfCheck` | die Zählung der Vollständigkeit ([Vollständigkeit](completeness.md)) und die Prüfungen der Entitäten und der Version |

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
