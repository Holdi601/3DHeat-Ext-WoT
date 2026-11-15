---
title: O documento da partida
nav_order: 6
lang: "pt"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# O documento da partida {#the-match-document}

`<match>.match.json` guarda tudo o que o replay diz e que não é uma linha da tabela. A aba Partida
do visualizador lê esse arquivo. (O código o chama de resumo.)

![O início de um documento da partida sintético, e as suas chaves](../assets/img/match-document.svg)

## A batalha {#the-battle}

| Chave | O que é |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; o id da batalha; o id do mapa e o seu nome de exibição |
| `clientVersion`, `streamVersion` | a versão do jogo no cabeçalho, e como o fluxo de pacotes a informa |
| `recorded` | quando o replay foi gravado, como o jogo o escreve |
| `player`, `vehicle` | o jogador que grava e o seu tanque |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | o número do tipo de batalha do cabeçalho, o modo de jogo, o servidor, a região, e se havia mods instalados |
| `duration` | a duração da batalha em segundos, dos resultados |
| `winnerTeam`, `finishReason` | a equipe vencedora e o número do jogo para o modo como a batalha terminou, dos resultados |
| `complete`, `truncated` | os resultados estão no replay; a gravação parou cedo |
| `battleStart`, `battleStartFrom`, `firstMovement` | o início da batalha em segundos da gravação; `arena` (a arena informou) ou `movement` (o primeiro momento em que qualquer tanque se moveu); esse primeiro movimento |
| `recordingSeconds` | a duração da gravação em segundos |
| `positionPacket`, `hz`, `positions` | o número do pacote em que chegaram as posições, amostras por segundo, linhas de posição |
| `events` | o número de linhas da tabela de cada evento |
| `units` | `metres; x east, y up, z north` (metros; x para leste, y para cima, z para norte) |
| `decoded` | o método e os números de pacote encontrados para cada tipo de mensagem |

## Jogadores e eventos {#players-and-events}

| Chave | O que é |
|---|---|
| `players` | uma entrada por tanque: nome, equipe, tanque, clã, amostras, abates, dano causado, sobreviveu, tempo de vida; `seen` (os tiros e o dano que o cliente que grava viu); a entrada completa do cabeçalho e dos resultados, e a da conta |
| `kills` | cada morte: tempo (segundos), de onde veio o tempo (`arena`, `health` ou `lifeTime`), vítima, abatedor, número e nome do motivo |
| `periods` | os períodos da batalha (espera, pré-batalha, batalha, pós-batalha) com os horários de fim do servidor |
| `basePoints` | progresso de captura de bases por equipe e por base |
| `chat`, `commands` | linhas de chat; comandos do chat de batalha com todos os seus argumentos |
| `camera`, `clientEvents` | os modos de câmera do jogador que grava; o que o cliente registrou sobre si mesmo (zoom, mira automática, mudanças de alvo, estado do veículo) |
| `arenaUpdates` | cada atualização da arena, decodificada, como o jogo a enviou |

## Resultados e verificações {#results-and-checks}

| Chave | O que é |
|---|---|
| `serverSettings` | as configurações do servidor, do cabeçalho |
| `results`, `resultVehicles`, `frags` | a tela de resultados: comum, pessoal (com os detalhes por alvo), jogadores, contas; a linha de resultados de cada tanque; abates por jogador |
| `entities` | cada entidade que o fluxo cria: seu número de tipo e papel, quando entrou na visão do cliente e quando saiu |
| `selfCheck` | a contagem de completude ([Completude](completeness.md)) e as verificações das entidades e da versão |

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
