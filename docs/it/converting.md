---
title: "Conversione dei replay"
nav_order: 4
lang: "it"
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Conversione dei replay {#converting-replays}

## Passo dopo passo {#step-by-step}

1. **Attiva la registrazione** nel gioco: Impostazioni > Generale > Registra le battaglie.
   Da quel momento il gioco salva ogni battaglia nella cartella `replays` della tua
   installazione di World of Tanks, per esempio
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Apri un terminale** in una cartella dove possono finire i risultati
   ([Prima di iniziare](before-you-start.md)).
3. **Esegui il convertitore** su file di replay, o su cartelle che li contengono:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out` viene creata nella cartella in cui si trova il terminale.
4. **Leggi cosa dice.** Dovresti vedere una riga per replay, che finisce con la
   tabella che ha scritto.
5. **Apri il risultato** nel visualizzatore 3DHeat: `out/<map>/<match>.parquet`
   nella scheda Mappa di calore, `<match>.match.json` nella scheda Partita. Oppure leggili
   con un qualsiasi lettore di Parquet o JSON.

![Un'esecuzione su un replay sintetico: conversione, nuova esecuzione, un file rotto, una cartella vuota](../assets/img/convert.svg)

L'immagine mostra un'esecuzione su un replay che i test creano nel codice (nessun replay reale):

- un replay convertito: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- eseguito di nuovo, la partita già scritta viene saltata: `<file>: already written, <table>`;
- un file che non è un replay: `<file>: not converted: <why>` (nell'output degli errori; stato di uscita 1, gli altri replay vengono comunque convertiti);
- nessun replay trovato: `no .wotreplay files in <folders>` (stato di uscita 2).

## Opzioni {#options}

| Opzione | Predefinito | Cosa fa |
|---|---|---|
| `replays` (uno o più) | - | file `.wotreplay`, o cartelle in cui cercarli (anche le sottocartelle) |
| `-o`, `--out` | obbligatoria | la cartella in cui scrivere: una cartella per mappa al suo interno |
| `--force` | disattivata | converti di nuovo ciò che è già scritto |
| `--version` | - | stampa `heat3d-wot-replay <versione>` e si ferma |
| `-h`, `--help` | - | stampa le opzioni e si ferma |

Le opzioni come le stampa il programma: [Riferimento dei comandi](../cli-reference.md).

## Cosa viene scritto {#what-is-written}

Solo file separati: questo convertitore non scrive alcun file `.3dheat` (il visualizzatore può
raccoglierli in uno solo: [Un file per partita](https://holdi601.github.io/3DHeat/container.html)).
Per replay, dentro `out/<map>/`:

| File | Cosa |
|---|---|
| `<match>.parquet` | la tabella: la posizione di ogni carro nel tempo e ogni evento in cui è accaduto ([La tabella](table.md)) |
| `<match>.match.json` | il documento della partita: mappa, versione del client, giocatori, uccisioni, risultati e tutto il resto ([Il documento della partita](match-document.md)) |
| `<match>.messages.parquet` | il file accessorio: ogni elemento del replay che i due file sopra non contengono intero ([Completezza](completeness.md)) |

`<match>` è l'id proprio della battaglia, oppure il nome del file quando la registrazione si è fermata prima dei risultati.

## Codice di uscita {#exit-status}

`0` quando ogni replay è stato convertito o saltato, `1` quando uno è fallito (gli
altri vengono comunque convertiti), `2` quando non è stato trovato alcun file di replay.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
