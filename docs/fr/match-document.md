---
title: Le document de partie
nav_order: 6
lang: "fr"
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Le document de partie {#the-match-document}

`<match>.match.json` contient tout ce que dit le replay et qui n'est pas une ligne de la table.
L'onglet Match du visualiseur le lit. (Le code l'appelle le résumé.)

![Le début d'un document de partie synthétique, et ses clés](../assets/img/match-document.svg)

## La bataille {#the-battle}

| Clé | Contenu |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks` ; l'identifiant de la bataille ; l'identifiant de la carte et son nom affiché |
| `clientVersion`, `streamVersion` | la version du jeu d'après l'en-tête, et telle que le flux de paquets la donne |
| `recorded` | le moment où le replay a été enregistré, tel que le jeu l'écrit |
| `player`, `vehicle` | le joueur qui enregistre et son char |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | le numéro de type de bataille de l'en-tête, le mode de jeu, le serveur, la région, et si des mods étaient installés |
| `duration` | la durée de la bataille en secondes, d'après les résultats |
| `winnerTeam`, `finishReason` | l'équipe gagnante et le numéro, donné par le jeu, de la façon dont la bataille s'est terminée, d'après les résultats |
| `complete`, `truncated` | les résultats sont dans le replay ; l'enregistrement s'est arrêté tôt |
| `battleStart`, `battleStartFrom`, `firstMovement` | le début de la bataille en secondes de l'enregistrement ; `arena` (l'arène l'a dit) ou `movement` (le premier instant où un char a bougé) ; ce premier mouvement |
| `recordingSeconds` | la durée de l'enregistrement en secondes |
| `positionPacket`, `hz`, `positions` | le numéro de paquet d'où viennent les positions, les échantillons par seconde, les lignes de position |
| `events` | le nombre de lignes de la table pour chaque événement |
| `units` | `metres; x east, y up, z north` |
| `decoded` | les numéros de méthode et de paquet trouvés pour chaque type de message |

## Joueurs et événements {#players-and-events}

| Clé | Contenu |
|---|---|
| `players` | une entrée par char : nom, équipe, char, clan, échantillons, frags, dégâts infligés, survie, durée de vie ; `seen` (les tirs et dégâts que le client qui enregistre a vus) ; l'entrée complète de l'en-tête et des résultats, et celle du compte |
| `kills` | chaque mort : heure (secondes), d'où vient l'heure (`arena`, `health` ou `lifeTime`), victime, tueur, numéro et nom de la raison |
| `periods` | les phases de la bataille (attente, pré-bataille, bataille, après-bataille) avec les heures de fin données par le serveur |
| `basePoints` | la progression de capture des bases par équipe et par base |
| `chat`, `commands` | les lignes de chat ; les commandes du chat de bataille avec tous leurs arguments |
| `camera`, `clientEvents` | les modes de caméra du joueur qui enregistre ; ce que le client a enregistré sur lui-même (zoom, visée automatique, changements de cible, état du véhicule) |
| `arenaUpdates` | chaque mise à jour de l'arène, décodée, telle que le jeu l'a envoyée |

## Résultats et contrôles {#results-and-checks}

| Clé | Contenu |
|---|---|
| `serverSettings` | les réglages du serveur, d'après l'en-tête |
| `results`, `resultVehicles`, `frags` | l'écran des résultats : commun, personnel (avec le détail par cible), joueurs, comptes ; la ligne de résultats de chaque char ; les frags par joueur |
| `entities` | chaque entité que le flux crée : son numéro de type et son rôle, le moment où elle est entrée dans la vue du client et celui où elle en est sortie |
| `selfCheck` | le compte d'exhaustivité ([Exhaustivité](completeness.md)) et les contrôles des entités et de la version |

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
