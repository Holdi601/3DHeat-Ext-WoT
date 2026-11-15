---
title: So liest es ein Replay
nav_order: 7
lang: "de"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# So liest es ein Replay {#how-it-reads-a-replay}

Ein Replay besteht aus einem Kopf aus JSON-Blöcken und dem Paketstrom des Spiels (Hinweise
zum Format in [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Der erste Block, im Klartext: die Karte, die Client-Version, der aufnehmende Spieler, die
  Einstellungen des Servers und die Aufstellung (`vehicles`: Name, Team, Panzer, mit der ID
  des Fahrzeugs als Schlüssel).
- Der zweite, wenn die Aufnahme bis zum Ende dauerte: der Ergebnisbildschirm - die Zeile jedes
  Fahrzeugs (Schüsse, Treffer, Durchschläge, verursachter, erhaltener, geblockter und
  unterstützter Schaden, Aufklärung, Erfahrung, Credits, Auszeichnungen ...), die Einzelheiten
  des aufnehmenden Spielers je Ziel, die Konten, die Dauer des Matches, Sieger und Grund des
  Endes; in manchen Modi die einzige vollständige Aufstellung (der Kopf dieser Listen nennt
  nur das eigene Team).
- Der Paketstrom, zlib-komprimiert und mit Blowfish verschlüsselt, mit einem Schlüssel, den das
  Spiel mitführt und den die Community-Werkzeuge, die diese Dateien lesen, seit 2013 veröffentlicht haben.

**Positionen** sind die Positionsaktualisierungen der Engine: die ID eines Fahrzeugs, seine Position
und sein Kurs, gefunden an ihrer Form und nicht an ihrer Paketnummer, sodass ein Patch, der sie neu
nummeriert, die Tabelle nicht leert. Sie sind das, was dem aufnehmenden Client mitgeteilt wurde: durchgehend
das eigene Team, ein Gegner nur, während er gesichtet ist (oder in der Reichweite des Clients). Ein
Fahrzeug, das nie gesichtet wurde, hat keine Zeilen. Die Zeilen eines Fahrzeugs enden mit seinem Tod.

**Der Rest des Stroms** - Lebenspunkte, Schüsse, Leuchtspur, Explosionen, Treffer, Geschützwinkel,
Arena-Aktualisierungen - sind Methodenaufrufe und Eigenschaftsänderungen der Fahrzeuge und des
Avatars des Clients, nummeriert nach den Definitionsdateien des Spiels, die sich mit Patches ändern
(1.12 und 2.4 nummerieren sie verschieden). Jeder wird an der Form seiner Argumente gefunden und daran,
wie sie zusammenhängen - siehe [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) -,
und die gefundenen Nummern stehen im `decoded` des Match-Dokuments. Chat, der Kameramodus und die
eigenen Ereignisse des Clients sind Pakete für sich. Arena-Aktualisierungen und Client-Ereignisse sind
Python-Pickles; sie werden von einem Leser gelesen, der jede darin genannte Klasse in einen leblosen
Platzhalter verwandelt und nichts ausführt.

Was dem Client mitgeteilt wurde, ist für das eigene Team vollständig und für Gegner teilweise: Ihre Schüsse,
Treffer und Lebensänderungen stehen drin, solange sie in Reichweite waren.

**Der Beginn des Gefechts** ist der Zeitpunkt, zu dem die Arena-Aktualisierung sagt, dass die
Gefechtsphase begann; in einem Replay ohne sie der erste Moment, in dem sich ein Fahrzeug bewegt.

**Tode:** Die Zeit ist die Abschussmeldung der Arena (1.x), sonst die Lebensänderung, die das Fahrzeug
beendet hat, sonst der Beginn des Gefechts plus die `lifeTime` des Opfers aus den Ergebnissen (ganze
Sekunden). Der Ort ist dort, wo das Opfer zuletzt gesehen wurde, wenn das innerhalb von fünf Sekunden
vor seinem Tod lag; sonst auf Clients von 2.x der Ort, den die Ergebnisse angeben (x und z, ohne Höhe),
nur im Match-Dokument. Eine Aufnahme, die vor dem Ende stoppte, hat keine Tode.

**Nicht gelesen:**

- Aufklärung und Minikarte: nicht als eigene Ereignisse im Strom.
- Der Höhenwinkel des Geschützes in Grad: Der Strom hat einen Schritt zwischen den Grenzen des
  Geschützes, und die Grenzen stehen in den Fahrzeugdateien des Spiels.
- Modulschaden, Besatzungsverletzungen, Verbrauchsgüter und Munition: Die Aufrufe, die sie tragen,
  ließen sich über 1.12 und 2.4 allein an der Form nicht unterscheiden.
- Entitätserzeugungspakete über die Entität und ihren Typ hinaus: Sie enthalten jede Eigenschaft eines
  Fahrzeugs, das gleichzeitig in die Sicht des Clients kommt, in einer Reihenfolge, die nur die
  Definitionsdateien angeben (vollständig im Sidecar aufbewahrt).
- Statische Kollisionen (Bäume, Häuser), das eigene Zielen des aufnehmenden Spielers und seine
  Physikpakete.
- Die Nummern der Chat-Befehle als Namen: Die Nummerierung gehört dem Spiel und ändert sich; das
  Match-Dokument behält die Argumente jedes Befehls, darunter seinen Schlüssel, wo er einen hat
  (`ATTACK_ENEMY`, ...).
- Angriffsgründe über 5: nur als Zahlen geschrieben.

## So wurde das Lesen geprüft {#how-the-reading-was-checked}

Das Lesen wurde an öffentlichen Replays der Clients 1.12 und 2.4 geprüft, jeder Wert gegen etwas,
das das Replay ein zweites Mal angibt:

- **Positionen:** Jeder Panzer, der je gesichtet wurde, hat eine Spur mit zehn Messwerten pro Sekunde;
  die Geschwindigkeiten bleiben in dem, was ein Panzer kann; der Kurs stimmt mit der Fahrtrichtung auf
  etwa 0,02 rad überein; wo die Ergebnisse den Ort eines Todes angeben, liegt der hier gelesene Ort
  innerhalb weniger Meter davon.
- **Der aufnehmende Spieler:** Die Schüsse und der verursachte Schaden stimmen auf jedem geprüften
  Replay mit den Werten der Ergebnisse überein.
- **Lebenspunkte:** Der letzte gelesene Lebenswert jedes Panzers ist gleich dem der Ergebnisse; der
  gelesene erhaltene Schaden ist nie größer als der der Ergebnisse. Auf 2.4 wird der tödliche Treffer
  auf einen Panzer außerhalb der Sicht des Clients oft nicht gesendet.
- **Treffer:** Der Schaden eines Treffers ist bei fast jedem Treffer gleich der Lebensänderung in
  diesem Moment.
- **Turm:** Bei einem Schuss zeigt der Kurs der Wanne plus der Gierwinkel des Turms dorthin, wohin die
  Leuchtspur flog, innerhalb von etwa 0,01 rad (Median).
- **Tode und Beginn des Gefechts:** innerhalb von etwa einer Sekunde dessen, was die Ergebnisse und
  die Arena sagen.

Die Tests bauen Replays in demselben Aufbau, daher liegt in diesem Repository kein echtes Replay.

**Nicht geprüft:** Clients vor 1.12, Replays für Konsole und Blitz (andere Spiele), Mir Tankov von Lesta
(`.mtreplay`) und andere Modi als Zufallsgefechte und Gefechtsart 20.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
