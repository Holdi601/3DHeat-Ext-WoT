---
title: "Vilkår og lisens"
nav_order: 9
lang: "no"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Vilkår og lisens {#terms-and-licence}

## Hva den leser {#what-it-reads}

Konverteren leser replayfiler som spillet skrev på din egen datamaskin, etter
kampen og utenfor spillet. Den endrer ingenting i spillet, snakker ikke med
noen server og viser ingenting under en kamp. Ingenting fra spillet følger med
eller videredistribueres: ingen spillressurser, ingen spillkode, ingen DLL-er.
Det den skriver, blir værende på datamaskinen din.

3DHeat er ikke tilknyttet eller godkjent av Wargaming. World of Tanks og
tilhørende navn og varemerker tilhører sine eiere.

Rettighetshavere: opprett en issue på
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - vi svarer raskt og
fjerner hva som helst på forespørsel.

## Lisens og kilder {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Trenger numpy (BSD-3-Clause) og pyarrow
(Apache-2.0). Skrevet for dette prosjektet: Blowfish-chifferet her er sitt eget, med tabellene regnet ut fra sifrene i pi slik
chifferet definerer dem. Fakta om formatet (containeren, chifferet, posisjonspakken) er allment kjent blant replayverktøy -
evido/wotreplay-parser (BSD-3-Clause) dokumenterer dem; ingen kode er tatt fra den eller fra noe annet prosjekt.

`bigworld.py` og `table.py` er de samme filene som i World of Warships-konverteren
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); endre begge sammen.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
