---
title: Completesa
nav_order: 8
lang: ca
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Completesa {#completeness}

Res d'una repetició no es descarta. Allò que llegeix el convertidor va a la taula i al document de partida;
cada altre element es guarda sencer a l'annex `<partida>.messages.parquet`; i `selfCheck.completeness` del
document de partida compta què n'ha estat de cada tipus d'element. Aquesta és la regla que comparteixen tots
els convertidors de 3DHeat:
[Els convertidors ho guarden tot](https://holdi601.github.io/3DHeat/converters.html).

![L'autocomprovació d'una repetició sintètica: cada element vist, llegit, guardat o perdut](../assets/img/completeness.svg)

## El recompte {#the-count}

Per a cada tipus d'element, `selfCheck.completeness.types` dona:

| Recompte | Vol dir |
|---|---|
| `seen` | quants n'hi ha a la repetició |
| `decoded` | llegits sencers |
| `partial` | llegits en part, i guardats sencers a l'annex |
| `raw` | només guardats sencers a l'annex, no llegits |
| `lost` | perduts: sempre `0` |

Els tipus són els de la mateixa repetició: `block 0` (la capçalera), `block 1` (els resultats), `container
sizes` i `deflate tail` (els bytes propis del contenidor), `packet <tipus>`, i, per a les crides a entitats,
`method <tipus d'entitat>.<número>` i `property <tipus d'entitat>.<número>`. Els tipus d'entitat són els
números que donen els paquets de creació; `selfCheck.entities.roles` indica quin és l'avatar del jugador que
grava i quins són els vehicles. Un tipus que ningú no coneixia apareix amb el seu recompte.

## L'annex {#the-sidecar}

| Columna | Què és |
|---|---|
| `time` | el rellotge de la repetició, com a la taula |
| `type`, `name` | el tipus d'element; com li diu el convertidor, on el llegeix |
| `entity` | el vehicle o avatar al qual pertany, com el `entity` de la taula |
| `decoded` | el que se n'ha llegit, com a JSON |
| `payload`, `text` | els seus bytes, sencers; els blocs JSON, sencers |
| `entityType`, `packet`, `method` | els números |

Les files s'ordenen per paquet, mètode, entitat i temps.

## Què es llegeix, i com es va comprovar {#what-is-read-and-how-it-was-checked}

- **Inclinació i roll** de cada posició: la inclinació és el pendent negatiu del propi camí del tanc mentre
  avança; dos tancs al mateix lloc amb un mateix heading tenen el mateix roll, amb headings oposats, rolls
  oposats.
- **Entitats** (`entities`): quan cada una va entrar a la vista del client i quan en va sortir. Cap tanc no
  té una posició entre que surt i torna.
- **La versió al flux** (`streamVersion`): la mateixa que la de la capçalera.
- **La mira del jugador que grava** (paquet 38): una direcció, al `decoded` de l'annex (`forward`); als trets
  del jugador és una fracció de grau d'on va volar l'obús.

Tota la resta que es llegeix (salut, impactes, trets, traçadors, explosions, angles de canó, actualitzacions
de l'arena, xat, modes de càmera, esdeveniments del client, posicions) és `partial`: a la taula o al document
de partida, i guardat sencer a l'annex.

**Guardat però no llegit** (`raw`), els tipus més grans: actualitzacions de posició que no són a la taula
(la de l'avatar, després de la mort d'un tanc, entitats fora de la llista), els paquets 26, 28, 29, 31, 36, 50,
54 i 57, algunes propietats freqüents de vehicles i avatars, cada mètode i propietat sense lector (el dany de
mòduls, la tripulació i els consumibles entre ells), i les propietats de les creacions d'entitats.

## No disponible {#not-available}

- Allò que el servidor mai no va enviar al client que grava: la mira, la càmera i les entrades dels altres
  jugadors, els enemics mentre no són detectats. Una repetició és el que se li va dir a un client.
- Els noms dels tipus d'entitat, mètodes i propietats: són als fitxers de definició del joc, no a la
  repetició. Els números es guarden.
- L'elevació del canó en graus i qualsevol altra cosa que necessiti les dades pròpies dels tancs dels fitxers
  del joc.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
