---
title: Comment le replay est lu
nav_order: 7
lang: "fr"
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Comment le replay est lu {#how-it-reads-a-replay}

Un replay est un en-tête de blocs JSON et le flux de paquets du jeu (notes sur le format dans
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)) :

- Le premier bloc, en clair : la carte, la version du client, le joueur qui enregistre, les réglages du
  serveur et la liste des joueurs (`vehicles` : nom, équipe, char, classés par l'identifiant du véhicule).
- Le second, lorsque l'enregistrement a duré jusqu'à la fin : l'écran des résultats - la ligne de chaque
  véhicule (tirs, impacts, pénétrations, dégâts infligés, reçus, bloqués et assistés, repérage, expérience,
  crédits, succès...), le détail du joueur qui enregistre par cible, les comptes, la durée du match, le
  vainqueur et la raison de la fin ; dans certains modes, la seule liste complète des joueurs (l'en-tête
  de ces listes ne donne que sa propre équipe).
- Le flux de paquets, compressé en zlib et chiffré en Blowfish avec une clé que le jeu contient, et que les
  outils communautaires qui lisent ces fichiers ont publiée depuis 2013.

**Les positions** sont les mises à jour de position du moteur : l'identifiant d'un véhicule, sa position et
son cap, trouvés par leur forme plutôt que par leur numéro de paquet, de sorte qu'un patch qui les renumérote
ne vide pas la table. Ce sont celles que le client qui enregistre a reçues : celles de sa propre équipe
pendant toute la bataille, celles d'un ennemi seulement lorsqu'il est repéré (ou dans la portée du client). Un
véhicule jamais repéré n'a aucune ligne. Les lignes d'un véhicule s'arrêtent à sa mort.

**Le reste du flux** - points de vie, tirs, traceurs, explosions, impacts, angles de canon, mises à jour de
l'arène - sont des appels de méthodes et des changements de propriétés des véhicules et de l'avatar du client,
numérotés par les fichiers de définition du jeu, qui changent avec les patchs (les versions 1.12 et 2.4 ne les numérotent
pas de la même façon). Chacun est trouvé par la forme de ses arguments et par la façon dont ils s'enchaînent -
voir [`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) -
et les numéros trouvés figurent dans le `decoded` du document de partie. Le chat, le mode de caméra et les
événements propres au client sont des paquets à part. Les mises à jour de l'arène et les événements du client
sont des pickles Python ; ils sont lus par un lecteur qui transforme chaque classe qu'ils nomment en une
coquille inerte et n'exécute rien.

Ce que le client a reçu est complet pour sa propre équipe, et partiel pour les ennemis : leurs tirs, impacts
et changements de points de vie y sont lorsqu'ils étaient à portée.

**Le début de la bataille** correspond au moment où la mise à jour de l'arène indique que la phase de bataille
a commencé ; dans un replay qui n'en a pas, c'est le premier instant où un véhicule bouge.

**Les morts :** l'heure est le message de destruction de l'arène (1.x), sinon le changement de points de vie
qui a mis fin au véhicule, sinon le début de la bataille plus le `lifeTime` de la victime tiré des résultats
(en secondes entières). Le lieu est l'endroit où la victime a été vue en dernier, lorsque c'était moins de cinq
secondes avant sa mort ; sinon, sur les clients 2.x, le lieu que donnent les résultats (x et z, sans hauteur),
dans le document de partie seulement. Un enregistrement arrêté avant la fin n'a aucune mort.

**Non lu :**

- Le repérage et la minicarte : ils ne sont pas dans le flux sous forme d'événements propres.
- L'élévation du canon en degrés : le flux contient un pas entre les limites du canon, et ces limites figurent
  dans les fichiers de véhicule du jeu.
- Les dégâts de modules, les blessures d'équipage, les consommables et les munitions : les appels qui les portent
  ne pouvaient pas être distingués par leur seule forme entre 1.12 et 2.4.
- Les paquets de création d'entités au-delà de l'entité et de son type : ils contiennent toutes les propriétés
  d'un véhicule qui entre dans la vue du client d'un coup, dans un ordre que seuls les fichiers de définition
  donnent (conservés en entier dans le fichier annexe).
- Les collisions statiques (arbres, maisons), la visée propre du joueur qui enregistre et ses paquets de physique.
- Les numéros des commandes de chat de bataille convertis en noms : la numérotation est celle du jeu et elle change ; le
  document de partie conserve les arguments de chaque commande, dont sa clé lorsqu'elle en a une (`ATTACK_ENEMY`, ...).
- Les raisons d'attaque supérieures à 5 : écrites seulement en nombres.

## Comment la lecture a été vérifiée {#how-the-reading-was-checked}

La lecture a été vérifiée sur des replays publics des clients 1.12 et 2.4, chaque valeur par rapport à quelque
chose que le replay donne une seconde fois :

- **Positions :** chaque char jamais vu a une trajectoire à dix échantillons par seconde ; les vitesses restent
  dans ce qu'un char peut faire ; le cap concorde avec la direction de déplacement à environ 0,02 rad près ; là où
  les résultats donnent le lieu d'une mort, le lieu lu ici est à quelques mètres près.
- **Le joueur qui enregistre :** les tirs et les dégâts infligés lus sont égaux aux valeurs des résultats, sur
  chaque replay vérifié.
- **Points de vie :** la dernière valeur lue pour chaque char est égale à celle des résultats ; les dégâts reçus
  lus ne dépassent jamais ceux des résultats. Sur 2.4, le coup fatal porté à un char hors de la vue du client
  n'est souvent pas envoyé.
- **Impacts :** les dégâts d'un impact sont égaux au changement de points de vie à cet instant, pour presque
  chaque impact.
- **Tourelle :** à un tir, le cap de la coque plus le lacet de la tourelle pointe là où le traceur a volé, à
  environ 0,01 rad près (médiane).
- **Morts et début de la bataille :** à environ une seconde près de ce que disent les résultats et l'arène.

Les tests construisent des replays selon la même disposition, de sorte qu'aucun vrai replay n'est conservé
dans ce dépôt.

**Non vérifié :** les clients antérieurs à 1.12, les replays console et Blitz (d'autres jeux), le Mir Tankov de
Lesta (`.mtreplay`), et les modes autres que les batailles aléatoires et le type de bataille 20.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
