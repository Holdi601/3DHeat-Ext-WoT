---
title: Exhaustivité
nav_order: 8
lang: fr
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Exhaustivité {#completeness}

Rien dans un replay n'est jeté. Ce que le convertisseur lit va dans la table et le document de match ;
chaque autre élément est conservé en entier dans le fichier annexe `<match>.messages.parquet` ; et
`selfCheck.completeness` du document de match compte ce qu'est devenu chaque type d'élément. C'est la
règle que partagent tous les convertisseurs de 3DHeat :
[Les convertisseurs gardent tout](https://holdi601.github.io/3DHeat/converters.html).

![Le contrôle interne d'un replay synthétique : chaque élément vu, lu, conservé ou perdu](../assets/img/completeness.svg)

## Le compte {#the-count}

Pour chaque type d'élément, `selfCheck.completeness.types` donne :

| Compte | Signification |
|---|---|
| `seen` | combien le replay en contient |
| `decoded` | lus en entier |
| `partial` | lus en partie, et conservés en entier dans le fichier annexe |
| `raw` | seulement conservés en entier dans le fichier annexe, non lus |
| `lost` | perdus : toujours `0` |

Les types sont ceux du replay lui-même : `block 0` (l'en-tête), `block 1` (les résultats), `container sizes`
et `deflate tail` (les octets propres du conteneur), `packet <type>`, et pour les appels sur des entités
`method <entity type>.<number>` et `property <entity type>.<number>`. Les types d'entités sont les numéros
donnés par les paquets de création ; `selfCheck.entities.roles` indique lequel est l'avatar du joueur qui
enregistre et lesquels sont les véhicules. Un type que personne ne connaissait apparaît avec son compte.

## Le fichier annexe {#the-sidecar}

| Colonne | Contenu |
|---|---|
| `time` | l'horloge du replay, comme dans la table |
| `type`, `name` | le type de l'élément ; le nom que lui donne le convertisseur, là où il le lit |
| `entity` | le véhicule ou l'avatar auquel il appartient, comme `entity` de la table |
| `decoded` | ce qui en a été lu, en JSON |
| `payload`, `text` | ses octets, en entier ; les blocs JSON, en entier |
| `entityType`, `packet`, `method` | les numéros |

Les lignes sont triées par paquet, méthode, entité et temps.

## Ce qui est lu, et comment cela a été vérifié {#what-is-read-and-how-it-was-checked}

- **Tangage et roulis** de chaque position : le tangage est l'opposé de la pente de la trajectoire du char
  lui-même lorsqu'il avance ; deux chars au même endroit avec le même cap ont le même roulis, avec des caps
  opposés des roulis opposés.
- **Entités** (`entities`) : le moment où chacune est entrée dans la vue du client et en est sortie. Aucun
  char n'a de position entre sa sortie et son retour.
- **La version dans le flux** (`streamVersion`) : la même que celle de l'en-tête.
- **La visée du joueur qui enregistre** (paquet 38) : une direction, dans le `decoded` de l'annexe
  (`forward`) ; lors des tirs du joueur, elle est à une fraction de degré près de la trajectoire de l'obus.

Tout le reste lu (points de vie, impacts, tirs, traceurs, explosions, angles de canon, mises à jour de
l'arène, chat, modes de caméra, événements du client, positions) est `partial` : dans la table ou le
document de match, et conservé en entier dans le fichier annexe.

**Conservé mais non lu** (`raw`), les plus gros types : les mises à jour de position qui ne sont pas dans la
table (celle de l'avatar, après la mort d'un char, les entités absentes de la liste), les paquets 26, 28,
29, 31, 36, 50, 54 et 57, certaines propriétés fréquentes des véhicules et des avatars, chaque méthode et
propriété sans lecteur (dégâts de modules, équipage et consommables parmi elles), et les propriétés des
créations d'entités.

## Non disponible {#not-available}

- Ce que le serveur n'a jamais envoyé au client qui enregistre : la visée, la caméra et les commandes des
  autres joueurs, les ennemis tant qu'ils ne sont pas repérés. Un replay est ce qu'un client a été informé.
- Les noms des types d'entités, des méthodes et des propriétés : ils se trouvent dans les fichiers de
  définition du jeu, non dans le replay. Les numéros sont conservés.
- L'élévation du canon en degrés, et tout ce qui demande les données propres des chars tirées des fichiers
  du jeu.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
