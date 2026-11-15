---
title: Como ele lê um replay
nav_order: 7
lang: pt
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Como ele lê um replay {#how-it-reads-a-replay}

Um replay é um cabeçalho de blocos JSON e o fluxo de pacotes do jogo (notas sobre o formato em
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- O primeiro bloco, sem cifra: o mapa, a versão do cliente, o jogador que grava, as configurações
  do servidor e a lista de participantes (`vehicles`: nome, equipe, tanque, indexada pelo id do
  veículo).
- O segundo, quando a gravação durou até o fim: a tela de resultados - a linha de cada veículo
  (tiros, acertos, perfurações, dano causado, recebido, bloqueado e assistido, detecção, xp,
  créditos, conquistas...), os detalhes por alvo do jogador que grava, as contas, a duração da
  partida, o vencedor e o motivo do fim; em alguns modos, a única lista completa de participantes
  (o cabeçalho dessas listas traz só a própria equipe).
- O fluxo de pacotes, comprimido com zlib e cifrado com Blowfish, com uma chave que o jogo traz
  consigo, e que as ferramentas da comunidade que leem esses arquivos publicam desde 2013.

**Posições** são as atualizações de posição do motor: o id de um veículo, sua posição e seu
rumo, encontrados pela forma e não pelo número do pacote, então um patch que renumera os pacotes
não esvazia a tabela. São o que o cliente que gravou foi informado: a própria equipe o tempo todo,
e um inimigo só enquanto é detectado (ou dentro do alcance do cliente). Um veículo nunca detectado
não tem linhas. As linhas de um veículo param na sua morte.

**O resto do fluxo** - vida, tiros, traçantes, explosões, acertos, ângulos de canhão, atualizações
da arena - são chamadas de método e mudanças de propriedade dos veículos e do avatar do cliente,
numerados pelos arquivos de definição do jogo, que mudam com os patches (1.12 e 2.4 os numeram de
modo diferente). Cada uma é encontrada pela forma dos seus argumentos e pelo modo como eles se
relacionam - veja [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - e os números
encontrados estão no `decoded` do documento da partida. Chat, o modo de câmera e os eventos
próprios do cliente são pacotes à parte. Atualizações da arena e eventos do cliente são pickles
do Python; são lidos por um leitor que transforma cada classe que eles nomeiam num substituto
inerte e não executa nada.

O que o cliente foi informado é completo para a própria equipe e parcial para os inimigos: seus
tiros, acertos e mudanças de vida estão ali enquanto estavam no alcance.

**O início da batalha** é quando a atualização da arena diz que o período de batalha começou; em
um replay sem ela, é o primeiro momento em que qualquer veículo se move.

**Mortes:** o tempo é a mensagem de abate da arena (1.x), senão a mudança de vida que encerrou o
veículo, senão o início da batalha mais o `lifeTime` da vítima nos resultados (em segundos inteiros).
O lugar é onde a vítima foi vista pela última vez, quando isso ocorreu a menos de cinco segundos da
sua morte; senão, em clientes 2.x, o lugar que os resultados dão (x e z, sem altura), só no
documento da partida. Uma gravação que parou antes do fim não tem mortes.

**Não lido:**

- Detecção e minimapa: não estão no fluxo como eventos próprios.
- A elevação do canhão em graus: o fluxo tem um passo entre os limites do canhão, e os limites
  estão nos arquivos de veículo do jogo.
- Dano em módulos, ferimentos da tripulação, consumíveis e munição: as chamadas que os trazem não
  puderam ser distinguidas só pela forma entre 1.12 e 2.4.
- Pacotes de criação de entidades além da entidade e do seu tipo: eles trazem todas as
  propriedades de um veículo que entra na visão do cliente de uma vez, numa ordem que só os
  arquivos de definição dão (guardados inteiros no arquivo auxiliar).
- Colisões estáticas (árvores, casas), a própria mira do jogador que grava e os pacotes de física.
- Números de comandos do chat de batalha como nomes: a numeração é do jogo e muda; o documento da
  partida guarda os argumentos de cada comando, entre eles a sua chave quando tem uma
  (`ATTACK_ENEMY`, ...).
- Motivos de ataque acima de 5: escritos só como números.

## Como a leitura foi conferida {#how-the-reading-was-checked}

A leitura foi conferida em replays públicos dos clientes 1.12 e 2.4, cada valor contra algo que o
replay dá uma segunda vez:

- **Posições:** cada tanque já visto tem uma trilha a dez amostras por segundo; as velocidades ficam
  dentro do que um tanque consegue; o rumo concorda com a direção do deslocamento em cerca de 0,02
  rad; onde os resultados dão o lugar de uma morte, o lugar lido aqui fica a poucos metros dele.
- **O jogador que grava:** os tiros e o dano causado lidos são iguais aos valores dos resultados, em
  todo replay conferido.
- **Vida:** a última leitura de vida de cada tanque é igual à dos resultados; o dano recebido lido
  nunca é maior que o dos resultados. Na 2.4, o golpe fatal num tanque fora da visão do cliente
  muitas vezes não é enviado.
- **Acertos:** o dano de um acerto é igual à mudança de vida naquele momento, em quase todo acerto.
- **Torre:** num tiro, o rumo do casco mais a rotação da torre aponta para onde o traçante voou, a
  cerca de 0,01 rad (mediana).
- **Mortes e início da batalha:** a cerca de um segundo do que dizem os resultados e a arena.

Os testes criam replays no mesmo layout, então nenhum replay real é guardado neste repositório.

**Não conferido:** clientes anteriores a 1.12, replays de console e Blitz (jogos diferentes), o
Mir Tankov da Lesta (`.mtreplay`), e modos que não sejam batalhas aleatórias e o tipo de batalha 20.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
