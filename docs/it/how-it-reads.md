---
title: "Come legge un replay"
nav_order: 7
lang: it
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Come legge un replay {#how-it-reads-a-replay}

Un replay è un'intestazione di blocchi JSON e il flusso di pacchetti del gioco (note sul formato in
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Il primo blocco, in chiaro: la mappa, la versione del client, il giocatore che registra, le impostazioni del server e il roster (`vehicles`: nome, squadra, carro, indicizzato con l'id del veicolo).
- Il secondo, quando la registrazione è durata fino alla fine: la schermata dei risultati - la riga di ogni veicolo (colpi, colpi a segno, perforazioni, danno inflitto, subito, bloccato e assistito, avvistamento, xp, crediti, risultati...), i dettagli per bersaglio del giocatore che registra, gli account, la durata della partita, il vincitore e il motivo della fine; in alcune modalità l'unico roster completo (l'intestazione di quegli elenchi riporta solo la propria squadra).
- Il flusso di pacchetti, compresso con zlib e cifrato con Blowfish con una chiave che il gioco contiene, che gli strumenti della comunità che leggono questi file hanno pubblicato dal 2013.

Le **posizioni** sono gli aggiornamenti di posizione del motore: l'id di un veicolo, la sua posizione e il suo rilevamento, trovati dalla loro forma anziché dal numero del pacchetto, così una patch che li rinumera non svuota la tabella. Sono ciò che è stato detto al client che registrava: la sua squadra per tutta la battaglia, un nemico solo mentre è avvistato (o nel raggio del client). Un veicolo mai avvistato non ha righe. Le righe di un veicolo si fermano alla sua morte.

**Il resto del flusso** - salute, colpi, traccianti, esplosioni, colpi a segno, angoli dei cannoni, aggiornamenti dell'arena - sono chiamate di metodi e cambi di proprietà dei veicoli e dell'avatar del client, numerati dai file di definizione del gioco, che cambiano con le patch (1.12 e 2.4 li numerano in modo diverso). Ognuno viene trovato dalla forma dei suoi argomenti e da come si legano tra loro - vedi [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - e i numeri trovati sono nel `decoded` del documento della partita. La chat, la modalità della telecamera e gli eventi propri del client sono pacchetti a sé. Gli aggiornamenti dell'arena e gli eventi del client sono pickle di Python; vengono letti da un lettore che trasforma ogni classe che nominano in un segnaposto inerte e non esegue nulla.

Ciò che è stato detto al client è completo per la sua squadra e parziale per i nemici: i loro colpi, colpi a segno e variazioni di salute ci sono mentre erano nel raggio.

**L'inizio della battaglia** è il momento in cui l'aggiornamento dell'arena dice che il periodo di battaglia è iniziato; in un replay senza di esso, il primo istante in cui un veicolo si muove.

**Morti:** l'ora è il messaggio di uccisione dell'arena (1.x), altrimenti la variazione di salute che ha chiuso il veicolo, altrimenti l'inizio della battaglia più la `lifeTime` della vittima dai risultati (secondi interi). Il luogo è dove la vittima è stata vista per l'ultima volta, quando ciò è avvenuto entro cinque secondi dalla sua morte; altrimenti, sui client 2.x, il luogo che danno i risultati (x e z, senza altezza), solo nel documento della partita. Una registrazione interrotta prima della fine non ha morti.

**Non letto:**

- Avvistamento e minimappa: non sono nel flusso come eventi propri.
- L'elevazione del cannone in gradi: il flusso ha un passo tra i limiti del cannone, e i limiti stanno nei file dei veicoli del gioco.
- Danni ai moduli, ferite dell'equipaggio, consumabili e munizioni: le chiamate che li portano non si possono distinguere per forma soltanto tra 1.12 e 2.4.
- Pacchetti di creazione di entità oltre all'entità e al suo tipo: contengono ogni proprietà di un veicolo che entra nella vista del client tutte insieme, in un ordine che solo i file di definizione danno (conservati interi nel file accessorio).
- Collisioni statiche (alberi, case), la mira propria del giocatore che registra e i pacchetti di fisica.
- I numeri dei comandi di chat di battaglia come nomi: la numerazione è quella del gioco e cambia; il documento della partita conserva gli argomenti di ogni comando, tra cui la sua chiave dove ne ha una (`ATTACK_ENEMY`, ...).
- Motivi di attacco oltre il 5: scritti solo come numeri.

## Come è stata verificata la lettura {#how-the-reading-was-checked}

La lettura è stata verificata su replay pubblici dei client 1.12 e 2.4, ogni valore confrontato con qualcosa che il replay dà una seconda volta:

- **Posizioni:** ogni carro mai visto ha una traccia a dieci campioni al secondo; le velocità restano entro ciò che un carro può fare; il rilevamento concorda con la direzione di marcia entro circa 0,02 rad; dove i risultati danno il luogo di una morte, il luogo letto qui è entro pochi metri da esso.
- **Il giocatore che registra:** i colpi e il danno inflitto letti sono uguali ai valori dei risultati, su ogni replay controllato.
- **Salute:** l'ultima lettura della salute di ogni carro è uguale a quella dei risultati; il danno subito letto non è mai superiore a quello dei risultati. Sul 2.4 il colpo mortale a un carro fuori dalla vista del client spesso non viene inviato.
- **Colpi:** il danno di un colpo è uguale alla variazione di salute in quel momento per quasi ogni colpo.
- **Torretta:** a un colpo, il rilevamento dello scafo più l'imbardata della torretta punta dove è volato il traccia-tiro, entro circa 0,01 rad (mediana).
- **Morti e inizio della battaglia:** entro circa un secondo da ciò che dicono i risultati e l'arena.

I test costruiscono i replay con lo stesso layout, quindi nessun replay reale è conservato in questo repository.

**Non verificato:** client precedenti all'1.12, replay di console e Blitz (giochi diversi), Mir Tankov di Lesta (`.mtreplay`), e modalità diverse dalle battaglie casuali e dal tipo di battaglia 20.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
