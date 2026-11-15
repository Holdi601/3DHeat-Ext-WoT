---
title: "Il documento della partita"
nav_order: 6
lang: "it"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Il documento della partita {#the-match-document}

`<match>.match.json` contiene tutto ciò che il replay dice e che non è una riga della tabella. La scheda Partita del visualizzatore lo legge. (Nel codice si chiama riepilogo.)

![L'inizio di un documento di partita sintetico, e le sue chiavi](../assets/img/match-document.svg)

## La battaglia {#the-battle}

| Chiave | Cosa |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; l'id della battaglia; l'id della mappa e il suo nome visualizzato |
| `clientVersion`, `streamVersion` | la versione del gioco dall'intestazione, e come la dice il flusso di pacchetti |
| `recorded` | quando è stato registrato il replay, come lo scrive il gioco |
| `player`, `vehicle` | il giocatore che registra e il suo carro |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | il numero del tipo di battaglia dell'intestazione, la modalità di gioco, il server, la regione, e se erano installate modifiche |
| `duration` | la durata della battaglia in secondi, dai risultati |
| `winnerTeam`, `finishReason` | la squadra vincitrice e il numero del gioco per come è finita la battaglia, dai risultati |
| `complete`, `truncated` | i risultati sono nel replay; la registrazione si è fermata prima |
| `battleStart`, `battleStartFrom`, `firstMovement` | l'inizio della battaglia in secondi della registrazione; `arena` (lo ha detto l'arena) o `movement` (il primo istante in cui un carro si è mosso); quel primo movimento |
| `recordingSeconds` | la durata della registrazione in secondi |
| `positionPacket`, `hz`, `positions` | il numero di pacchetto da cui arrivano le posizioni, campioni al secondo, righe di posizione |
| `events` | il numero di righe della tabella per ogni evento |
| `units` | `metres; x east, y up, z north` (metri; x est, y su, z nord) |
| `decoded` | i numeri di metodo e di pacchetto trovati per ogni tipo di messaggio |

## Giocatori ed eventi {#players-and-events}

| Chiave | Cosa |
|---|---|
| `players` | una voce per carro: nome, squadra, carro, clan, campioni, uccisioni, danno inflitto, sopravvissuto, durata della vita; `seen` (i colpi e il danno che ha visto il client che registrava); la voce intera dell'intestazione e dei risultati, e quella dell'account |
| `kills` | ogni morte: ora (secondi), da dove viene l'ora (`arena`, `health` o `lifeTime`), vittima, assassino, numero e nome del motivo |
| `periods` | i periodi della battaglia (attesa, pre-battaglia, battaglia, post-battaglia) con gli orari di fine del server |
| `basePoints` | avanzamento della cattura delle basi per squadra e per base |
| `chat`, `commands` | righe di chat; comandi della chat di battaglia con tutti i loro argomenti |
| `camera`, `clientEvents` | le modalità di telecamera del giocatore che registra; ciò che il client ha registrato su se stesso (zoom, mira automatica, cambi di bersaglio, stato del veicolo) |
| `arenaUpdates` | ogni aggiornamento dell'arena, decodificato, come lo ha inviato il gioco |

## Risultati e verifiche {#results-and-checks}

| Chiave | Cosa |
|---|---|
| `serverSettings` | le impostazioni del server dall'intestazione |
| `results`, `resultVehicles`, `frags` | la schermata dei risultati: comuni, personali (con i dettagli per bersaglio), giocatori, account; la riga dei risultati di ogni carro; uccisioni per giocatore |
| `entities` | ogni entità creata dal flusso: il suo numero di tipo e ruolo, quando è entrata nella vista del client e quando è uscita |
| `selfCheck` | il conteggio di completezza ([Completezza](completeness.md)) e le verifiche delle entità e della versione |

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
