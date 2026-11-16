---
title: "Uvjeti i licenca"
nav_order: 9
lang: "bs"
source: terms.md
source_hash: "52f99a5bfca6"
nav_exclude: true
search_exclude: true
---
# Uvjeti i licenca {#terms-and-licence}

## Šta čita {#what-it-reads}

Konverter čita fajlove replayeva koje je igra zapisala na vašem vlastitom
računaru, nakon bitke i izvan igre. Ne mijenja ništa u igri, ne komunicira ni
sa jednim serverom i ne prikazuje ništa tokom bitke. Ništa iz igre se ne
isporučuje niti dalje distribuira s njim: nema resursa igre, koda igre ni
DLL-ova. Ono što zapiše ostaje na vašem računaru.

3DHeat nije povezan s Wargamingom niti ga Wargaming podržava. World of Tanks i
povezani nazivi i zaštitni znakovi pripadaju svojim vlasnicima.

Nosioci prava: otvorite issue na
<https://github.com/Holdi601/3DHeat-Ext-WoT/issues> - brzo odgovaramo i na
zahtjev uklanjamo bilo šta.

## Licenca i izvori {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Potrebni su numpy (BSD-3-Clause) i pyarrow
(Apache-2.0). Napisano za ovaj projekat: Blowfish šifra ovdje je vlastita,
s tabelama izračunatim iz cifara broja pi kako ih šifra definira.
Činjenice o formatu (kontejner, šifra, paket pozicija) su
opće znanje među alatima za replayeve - evido/wotreplay-parser (BSD-3-Clause)
ih dokumentira; nikakav kod nije preuzet iz njega niti iz bilo kojeg drugog projekta.

`bigworld.py` i `table.py` su iste datoteke kao u World of Warships
konverteru ([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs)); mijenjajte oba zajedno.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
