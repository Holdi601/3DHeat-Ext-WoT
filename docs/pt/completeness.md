---
title: Completude
nav_order: 8
lang: pt
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Completude {#completeness}

Nada de um replay é descartado. O que o conversor lê vai para a tabela e para o documento da
partida; todo outro item é guardado inteiro no arquivo auxiliar `<match>.messages.parquet`; e
`selfCheck.completeness` no documento da partida conta o que aconteceu com cada tipo de item.
Esta é a regra que todos os conversores do 3DHeat seguem:
[Conversores mantêm tudo](https://holdi601.github.io/3DHeat/converters.html).

![A autoverificação de um replay sintético: cada item visto, lido, guardado ou perdido](../assets/img/completeness.svg)

## A contagem {#the-count}

Para cada tipo de item, `selfCheck.completeness.types` dá:

| Contagem | Significa |
|---|---|
| `seen` | quantos o replay contém |
| `decoded` | lidos inteiros |
| `partial` | lidos em parte, e guardados inteiros no arquivo auxiliar |
| `raw` | só guardados inteiros no arquivo auxiliar, não lidos |
| `lost` | perdidos: sempre `0` |

Os tipos são os do próprio replay: `block 0` (o cabeçalho), `block 1` (os resultados),
`container sizes` e `deflate tail` (os próprios bytes do contêiner), `packet <type>`, e, para
chamadas em entidades, `method <entity type>.<number>` e `property <entity type>.<number>`. Os
tipos de entidade são os números que os pacotes de criação dão; `selfCheck.entities.roles`
diz qual é o avatar do jogador que grava e quais são os veículos. Um tipo que ninguém conhecia
aparece com a sua contagem.

## O arquivo auxiliar {#the-sidecar}

| Coluna | O que é |
|---|---|
| `time` | o relógio do replay, como na tabela |
| `type`, `name` | o tipo do item; como o conversor o chama, onde o lê |
| `entity` | o veículo ou avatar a que pertence, como o `entity` da tabela |
| `decoded` | o que foi lido dele, em JSON |
| `payload`, `text` | seus bytes, inteiros; os blocos JSON, inteiros |
| `entityType`, `packet`, `method` | os números |

As linhas são ordenadas por pacote, método, entidade e tempo.

## O que é lido, e como foi conferido {#what-is-read-and-how-it-was-checked}

- **Arfagem e rolamento** de cada posição: a arfagem é o negativo da inclinação da trilha do
  próprio tanque enquanto ele anda para a frente; dois tanques no mesmo ponto com um rumo têm o
  mesmo rolamento, com rumos opostos têm rolamentos opostos.
- **Entidades** (`entities`): quando cada uma entrou na visão do cliente e quando saiu. Nenhum
  tanque tem posição entre sair e voltar.
- **A versão no fluxo** (`streamVersion`): igual à do cabeçalho.
- **A mira do jogador que grava** (pacote 38): uma direção, no `decoded` do arquivo auxiliar
  (`forward`); nos tiros do jogador ela fica a uma fração de grau de onde o projétil voou.

Tudo o mais lido (vida, acertos, tiros, traçantes, explosões, ângulos de canhão, atualizações
da arena, chat, modos de câmera, eventos do cliente, posições) é `partial`: na tabela ou no
documento da partida, e guardado inteiro no arquivo auxiliar.

**Guardado mas não lido** (`raw`), os tipos maiores: atualizações de posição que não estão na
tabela (a do avatar, depois da morte de um tanque, entidades fora da lista), os pacotes 26, 28,
29, 31, 36, 50, 54 e 57, algumas propriedades frequentes de veículos e avatares, cada método e
propriedade sem leitor (dano em módulos, tripulação e consumíveis entre eles), e as propriedades
das criações de entidades.

## Não disponível {#not-available}

- O que o servidor nunca enviou ao cliente que gravou: a mira, a câmera e os comandos de outros
  jogadores, inimigos enquanto não foram vistos. Um replay é o que um cliente foi informado.
- Os nomes dos tipos de entidade, métodos e propriedades: estão nos arquivos de definição do
  jogo, não no replay. Os números são guardados.
- A elevação do canhão em graus e qualquer outra coisa que precise dos dados próprios dos tanques
  nos arquivos do jogo.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
