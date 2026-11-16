---
title: Termos e licença
nav_order: 9
lang: "pt"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Termos e licença {#terms-and-licence}

## O que ele lê {#what-it-reads}

O conversor lê arquivos de replay que o jogo gravou no seu próprio computador,
depois da batalha e fora do jogo. Ele não altera nada no jogo, não fala com
nenhum servidor e não mostra nada durante uma batalha. Nada do jogo é
fornecido nem redistribuído com ele: nenhum recurso do jogo, nenhum código do
jogo, nenhuma DLL. O que ele grava fica no seu computador.

O 3DHeat não é afiliado à Wargaming nem endossado pela Wargaming. World of
Tanks e os nomes e marcas relacionados pertencem aos seus proprietários.

Titulares de direitos: abram uma issue em
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - respondemos rápido e
removemos qualquer coisa a pedido.

## Licença e fontes {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Precisa de numpy
(BSD-3-Clause) e pyarrow (Apache-2.0). Escrito para este projeto: a cifra Blowfish daqui é própria,
com as suas tabelas calculadas a partir dos dígitos de pi, como a cifra define. Fatos sobre o formato
(o contêiner, a cifra, o pacote de posição) são conhecimento comum entre as ferramentas de replay -
evido/wotreplay-parser (BSD-3-Clause) os documenta; nenhum código foi tirado dele nem de nenhum outro
projeto.

`bigworld.py` e `table.py` são os mesmos arquivos do conversor de World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); altere os dois juntos.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
