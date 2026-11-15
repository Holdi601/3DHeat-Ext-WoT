---
title: "Installazione"
nav_order: 3
lang: it
source: installing.md
source_hash: "da6c577ace69"
nav_exclude: true
search_exclude: true
---
# Installazione {#installing}

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).
Serve Python 3.10 o successivo; numpy e pyarrow vengono installati con esso.

## Passo dopo passo {#step-by-step}

1. Scarica il codice: `git clone https://github.com/Holdi601/3DHeat-Ext-WoT.git`,
   oppure scarica uno zip da [Releases](https://github.com/Holdi601/3DHeat-Ext-WoT/releases)
   e decomprimilo.
2. Apri un terminale in quella cartella e scrivi `pip install -e .`. Questo mette il
   comando `heat3d-wot-replay` nel tuo percorso (PATH).
3. Verifica: `heat3d-wot-replay --version`. Dovresti vedere
   `heat3d-wot-replay 0.1.0`. `heat3d-wot-replay --help` elenca le opzioni:

![heat3d-wot-replay --help](../assets/img/help.svg)

Senza installare, `python -m heat3d_ext_wot ...` nella cartella dello strumento fa
la stessa cosa.

Il Watcher di 3DHeat esegue questo comando sui nuovi replay quando è installato,
e funziona senza di esso.

## Aggiornamenti {#updates}

Ogni avvio controlla prima le release GitHub del progetto (al massimo una richiesta
ogni poche ore; non blocca mai una conversione, che sia online o no). Quando è
uscita una release più recente, il comando chiede prima di installarla: un clone `git`
viene aggiornato con `git pull --ff-only` (rifiutato se hai modifiche locali),
una copia scaricata dall'archivio della release. `HEAT3D_NO_UPDATE=1` disattiva
il controllo e l'aggiornamento.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
