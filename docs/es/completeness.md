---
title: Completitud
nav_order: 8
lang: es
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Completitud {#completeness}

Nada de una repetición se descarta. Lo que lee el convertidor va a la tabla y al documento de la partida; cada otro elemento se guarda completo en el archivo auxiliar `<partida>.messages.parquet`; y el `selfCheck.completeness` del documento de la partida cuenta qué pasó con cada tipo de elemento. Es la regla que comparten todos los convertidores de 3DHeat:
[Los convertidores lo conservan todo](https://holdi601.github.io/3DHeat/converters.html).

![La autocomprobación de una repetición sintética: cada elemento visto, leído, conservado o perdido](../assets/img/completeness.svg)

## El recuento {#the-count}

Para cada tipo de elemento, `selfCheck.completeness.types` da:

| Recuento | Significa |
|---|---|
| `seen` | cuántos contiene la repetición |
| `decoded` | leídos completos |
| `partial` | leídos en parte, y guardados completos en el archivo auxiliar |
| `raw` | solo guardados completos en el archivo auxiliar, sin leer |
| `lost` | perdidos: siempre `0` |

Los tipos son los propios de la repetición: `block 0` (la cabecera), `block 1` (los
resultados), `container sizes` y `deflate tail` (los bytes propios del contenedor),
`packet <tipo>`, y para las llamadas a entidades `method <tipo de entidad>.<número>`
y `property <tipo de entidad>.<número>`. Los tipos de entidad son los números que dan
los paquetes de creación; `selfCheck.entities.roles` indica cuál es el avatar del
jugador que graba y cuáles los vehículos. Un tipo que nadie conocía aparece con su recuento.

## El archivo auxiliar {#the-sidecar}

| Columna | Qué es |
|---|---|
| `time` | el reloj de la repetición, como en la tabla |
| `type`, `name` | el tipo de elemento; cómo lo llama el convertidor, y dónde lo lee |
| `entity` | el vehículo o avatar al que pertenece, como `entity` de la tabla |
| `decoded` | lo que se leyó de él, como JSON |
| `payload`, `text` | sus bytes, completos; los bloques JSON, completos |
| `entityType`, `packet`, `method` | los números |

Las filas se ordenan por paquete, método, entidad y tiempo.

## Qué se lee, y cómo se comprobó {#what-is-read-and-how-it-was-checked}

- **Cabeceo y balanceo** de cada posición: el cabeceo es menos la pendiente de la trayectoria
  propia del tanque mientras avanza; dos tanques en un mismo punto con un mismo rumbo tienen
  el mismo balanceo, y con rumbos opuestos, balanceos opuestos.
- **Entidades** (`entities`): cuándo entró cada una en la vista del cliente y cuándo salió.
  Ningún tanque tiene posición entre su salida y su regreso.
- **La versión del flujo** (`streamVersion`): la misma que la de la cabecera.
- **La mira del jugador que graba** (paquete 38): una dirección, en el `decoded` del
  auxiliar (`forward`); en los disparos del jugador está a una fracción de grado de
  hacia dónde voló el proyectil.

Todo lo demás que se lee (vida, impactos, disparos, trazadores, explosiones, ángulos del cañón,
actualizaciones de la arena, chat, modos de cámara, eventos del cliente, posiciones) es `partial`:
va a la tabla o al documento de la partida, y se guarda completo en el auxiliar.

**Guardado pero no leído** (`raw`), los tipos más grandes: actualizaciones de posición que no están en
la tabla (las del avatar, tras la muerte de un tanque, entidades que no están en la lista),
los paquetes 26, 28, 29, 31, 36, 50, 54 y 57, algunas propiedades frecuentes de vehículos y avatares,
cada método y propiedad sin lector (daños a módulos, tripulación y consumibles entre ellos),
y las propiedades de las creaciones de entidades.

## No disponible {#not-available}

- Lo que el servidor nunca envió al cliente que grababa: la mira, la cámara y las entradas de
  otros jugadores, los enemigos mientras no fueron detectados. Una repetición es lo que le
  dijeron a un cliente.
- Los nombres de los tipos de entidad, métodos y propiedades: están en los archivos de definición
  del juego, no en la repetición. Los números se conservan.
- La elevación del cañón en grados y cualquier otra cosa que necesite los datos propios de los
  tanques de los archivos del juego.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
