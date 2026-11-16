---
title: Termes et licence
nav_order: 9
lang: "fr"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Termes et licence {#terms-and-licence}

## Ce qu'il lit {#what-it-reads}

Le convertisseur lit les fichiers de replay que le jeu a écrits sur votre
propre ordinateur, après la bataille et hors du jeu. Il ne change rien au jeu,
ne parle à aucun serveur et n'affiche rien pendant une bataille. Rien du jeu
n'est fourni ni redistribué avec lui : aucune ressource du jeu, aucun code du
jeu, aucune DLL. Ce qu'il écrit reste sur votre ordinateur.

3DHeat n'est ni affilié à Wargaming ni approuvé par Wargaming. World of Tanks
ainsi que les noms et marques associés appartiennent à leurs propriétaires.

Titulaires de droits : ouvrez une issue sur
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - nous répondons vite et
retirons tout ce qui est demandé.

## Licence et sources {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Nécessite numpy
(BSD-3-Clause) et pyarrow (Apache-2.0). Écrit pour ce projet : le chiffrement Blowfish d'ici est le sien, ses
tables étant calculées à partir des chiffres de pi comme le définit le chiffrement. Les faits sur le format (le
conteneur, le chiffrement, le paquet de position) sont des connaissances communes aux outils de replays ;
evido/wotreplay-parser (BSD-3-Clause) les documente ; aucun code n'a été repris de lui ni d'aucun autre projet.

`bigworld.py` et `table.py` sont les mêmes fichiers que dans le convertisseur de World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)) ; modifiez les deux ensemble.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
