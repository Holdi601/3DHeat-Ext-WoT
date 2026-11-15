---
title: "Completezza"
nav_order: 8
lang: "it"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Completezza {#completeness}

Nulla di un replay viene buttato via. Ciò che il convertitore legge va nella tabella e nel documento della partita; ogni altro elemento viene conservato intero nel file accessorio
`<match>.messages.parquet`; e il `selfCheck.completeness` del documento della partita conta cosa è diventato ogni tipo di elemento. Questa è la regola che condividono tutti i convertitori 3DHeat:
[I convertitori conservano tutto](https://holdi601.github.io/3DHeat/converters.html).

![L'autocontrollo di un replay sintetico: ogni elemento visto, letto, conservato o perso](../assets/img/completeness.svg)

## Il conteggio {#the-count}

Per ogni tipo di elemento, `selfCheck.completeness.types` dà:

| Conteggio | Significa |
|---|---|
| `seen` | quanti ne contiene il replay |
| `decoded` | letti interi |
| `partial` | letti in parte, e conservati interi nel file accessorio |
| `raw` | solo conservati interi nel file accessorio, non letti |
| `lost` | persi: sempre `0` |

I tipi sono quelli del replay stesso: `block 0` (l'intestazione), `block 1` (i risultati), `container sizes` e `deflate tail` (i byte propri del contenitore),
`packet <type>`, e per le chiamate alle entità `method <entity type>.<number>`
e `property <entity type>.<number>`. I tipi di entità sono i numeri che danno i pacchetti di creazione; `selfCheck.entities.roles` dice quale è l'avatar del giocatore che registra e quali sono i veicoli. Un tipo che nessuno conosceva compare con il suo conteggio.

## Il file accessorio {#the-sidecar}

| Colonna | Cosa |
|---|---|
| `time` | l'orologio del replay, come nella tabella |
| `type`, `name` | il tipo di elemento; come lo chiama il convertitore, dove lo legge |
| `entity` | il veicolo o l'avatar a cui appartiene, come `entity` della tabella |
| `decoded` | ciò che ne è stato letto, come JSON |
| `payload`, `text` | i suoi byte, interi; i blocchi JSON, interi |
| `entityType`, `packet`, `method` | i numeri |

Le righe sono ordinate per pacchetto, metodo, entità e tempo.

## Cosa viene letto, e come è stato verificato {#what-is-read-and-how-it-was-checked}

- **Beccheggio e rollio** di ogni posizione: il beccheggio è meno la pendenza del percorso del carro stesso mentre va avanti; due carri nello stesso punto con lo stesso rilevamento hanno lo stesso rollio, con rilevamenti opposti rollii opposti.
- **Entità** (`entities`): quando ciascuna è entrata nella vista del client e quando è uscita. Nessun carro ha una posizione tra l'uscita e il rientro.
- **La versione nel flusso** (`streamVersion`): uguale a quella dell'intestazione.
- **La mira del giocatore che registra** (pacchetto 38): una direzione, in `decoded` del file accessorio (`forward`); nei colpi del giocatore è a una frazione di grado da dove è volato il proiettile.

Tutto il resto letto (salute, colpi, tiri, traccianti, esplosioni, angoli dei cannoni, aggiornamenti dell'arena, chat, modalità della telecamera, eventi del client, posizioni) è `partial`: nella tabella o nel documento della partita, e conservato intero nel file accessorio.

**Conservato ma non letto** (`raw`), i tipi più grossi: aggiornamenti di posizione non nella tabella (quelli dell'avatar, dopo la morte di un carro, entità non nel roster), i pacchetti 26, 28, 29, 31, 36, 50, 54 e 57, alcune proprietà frequenti di veicoli e avatar, ogni metodo e proprietà senza un lettore (tra cui danni ai moduli, equipaggio e consumabili), e le proprietà delle creazioni di entità.

## Non disponibile {#not-available}

- Ciò che il server non ha mai inviato al client che registrava: la mira, la telecamera e i comandi di altri giocatori, i nemici finché non sono avvistati. Un replay è ciò che è stato detto a un solo client.
- I nomi dei tipi di entità, dei metodi e delle proprietà: stanno nei file di definizione del gioco, non nel replay. I numeri vengono conservati.
- L'elevazione del cannone in gradi e qualsiasi altra cosa che richieda i dati propri dei carri dai file del gioco.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
