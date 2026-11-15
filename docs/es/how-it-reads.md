---
title: Cómo lee una repetición
nav_order: 7
lang: es
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Cómo lee una repetición {#how-it-reads-a-replay}

Una repetición es una cabecera de bloques JSON y el flujo de paquetes del juego (notas sobre el formato
en [`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- El primer bloque, en claro: el mapa, la versión del cliente, el jugador que graba, los ajustes del
  servidor y la lista de jugadores (`vehicles`: nombre, equipo, tanque, con clave en el id del vehículo).
- El segundo, cuando la grabación llegó hasta el final: la pantalla de resultados -
  la línea de cada vehículo (disparos, impactos, perforaciones, daño causado, recibido,
  bloqueado y asistido, detección, experiencia, créditos, logros...), los detalles por objetivo
  del jugador que graba, las cuentas, la duración de la partida, el ganador y el motivo del final; en algunos modos,
  la única lista completa de jugadores (la cabecera de esas listas solo trae el propio equipo).
- El flujo de paquetes, comprimido con zlib y cifrado con Blowfish con una clave que trae el
  juego, que las herramientas de la comunidad que leen estos archivos han publicado desde 2013.

**Las posiciones** son las actualizaciones de posición del motor: el id de un vehículo, su posición
y su rumbo, encontrados por su forma y no por su número de paquete, así que un parche que los renumere
no vacía la tabla. Son lo que se le dijo al cliente que grababa: su propio equipo todo el tiempo, un enemigo solo
mientras estuvo detectado (o en el alcance del cliente). Un vehículo que nunca fue detectado no tiene filas.
Las filas de un vehículo terminan con su muerte.

**El resto del flujo** - vida, disparos, trazadores, explosiones, impactos, ángulos del cañón,
actualizaciones de la arena - son llamadas a métodos y cambios de propiedades de los vehículos
y del avatar del cliente, numerados por los archivos de definición del juego, que cambian con los
parches (1.12 y 2.4 los numeran de forma distinta). Cada uno se encuentra por la forma de sus
argumentos y por cómo encajan entre sí - véase
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) - y
los números encontrados están en el `decoded` del documento de la partida. El chat, el modo de
cámara y los eventos propios del cliente son paquetes propios. Las actualizaciones de la arena y los eventos del cliente son
pickles de Python; los lee un lector que convierte cada clase que nombran en un sustituto inerte
y no ejecuta nada.

Lo que se le dijo al cliente está completo para su propio equipo y parcial para
los enemigos: sus disparos, impactos y cambios de vida están mientras estuvieron al alcance.

**El inicio de la batalla** es cuando la actualización de la arena dice que empezó el periodo de batalla;
en una repetición sin ella, el primer instante en que se mueve cualquier vehículo.

**Muertes:** la hora es el mensaje de baja de la arena (1.x), si no el cambio de vida que terminó
con el vehículo, si no el inicio de la batalla más el `lifeTime` de la víctima según los resultados
(segundos enteros). El lugar es donde se vio por última vez a la víctima,
cuando eso fue a menos de cinco segundos de su muerte; si no, en clientes 2.x, el
lugar que dan los resultados (x y z, sin altura), solo en el documento de la partida. Una grabación
que se detuvo antes del final no tiene muertes.

**No se lee:**

- La detección y el minimapa: no están en el flujo como eventos propios.
- La elevación del cañón en grados: el flujo tiene un paso entre los límites del cañón, y los límites
  están en los archivos de vehículo del juego.
- Daños a módulos, heridas de la tripulación, consumibles y munición: las llamadas que los llevan
  no se pueden distinguir solo por la forma entre 1.12 y 2.4.
- Los paquetes de creación de entidades más allá de la entidad y su tipo: contienen cada propiedad de un
  vehículo que entra en la vista del cliente de golpe, en un orden que solo dan los archivos de definición
  (guardados completos en el auxiliar).
- Colisiones estáticas (árboles, casas), y los paquetes de apuntado y físicas del propio jugador que graba.
- Los números de los comandos de chat de batalla como nombres: la numeración es del juego y
  cambia; el documento de la partida guarda los argumentos de cada comando, entre ellos su clave
  cuando la tiene (`ATTACK_ENEMY`, ...).
- Motivos de ataque por encima de 5: se escriben solo como números.

## Cómo se comprobó la lectura {#how-the-reading-was-checked}

La lectura se comprobó con repeticiones públicas de los clientes 1.12 y 2.4, cada
valor frente a algo que la repetición da por una segunda vía:

- **Posiciones:** cada tanque visto tiene una trayectoria a diez muestras por segundo;
  las velocidades se mantienen dentro de lo que puede hacer un tanque; el rumbo coincide con la
  dirección de avance a unos 0,02 rad; donde los resultados dan el lugar de una muerte, el lugar leído
  aquí está a pocos metros de él.
- **El jugador que graba:** los disparos y el daño causado leídos son iguales a los valores de
  los resultados, en cada repetición comprobada.
- **Vida:** la última vida leída de cada tanque es igual a la de los resultados; el daño
  recibido leído nunca es mayor que el de los resultados. En 2.4 a menudo no se envía el golpe
  final a un tanque fuera de la vista del cliente.
- **Impactos:** el daño de un impacto es igual al cambio de vida en ese momento en casi
  todos los impactos.
- **Torreta:** en un disparo, el rumbo del casco más el giro de la torreta apunta
  hacia donde voló el trazador, a unos 0,01 rad (mediana).
- **Muertes y el inicio de la batalla:** a menos de un segundo de lo que dicen los resultados y la arena.

Los tests construyen repeticiones con la misma disposición, así que en este repositorio no se guarda
ninguna repetición real.

**No comprobado:** clientes anteriores a 1.12, repeticiones de consola y de Blitz (juegos
distintos), Mir Tankov de Lesta (`.mtreplay`), y modos distintos de las batallas aleatorias y del
tipo de batalla 20.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
