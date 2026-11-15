---
title: Pretvorba posnetkov
nav_order: 4
lang: sl
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Pretvorba posnetkov {#converting-replays}

## Korak za korakom {#step-by-step}

1. **Vklopite snemanje v igri:** Nastavitve > Splošno > Snemaj bitke. Od takrat naprej igra shrani
   vsako bitko v mapo `replays` vaše namestitve World of Tanks, na primer
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Odprite ukazno vrstico** v mapi, kamor smejo iti rezultati ([Preden začnete](before-you-start.md)).
3. **Zaženite pretvornik** na datotekah posnetkov ali na mapah, ki jih vsebujejo:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   `out` se ustvari v mapi, v kateri je vaša ukazna vrstica.
4. **Preberite, kaj piše.** Videti bi morali eno vrstico za vsak posnetek, ki se konča s tabelo, ki jo
   je zapisal.
5. **Odprite rezultat** v 3DHeat pregledovalniku: `out/<map>/<match>.parquet` na zavihku Toplotni
   zemljevid, `<match>.match.json` na zavihku Tekma. Lahko ju preberete tudi s katerimkoli bralnikom
   Parquet ali JSON.

![Zagon na sintetičnem posnetku: pretvorba, ponovni zagon, pokvarjena datoteka, prazna mapa](../assets/img/convert.svg)

Slika prikazuje zagon na posnetku, ki ga teste sestavijo v kodi (brez pravega posnetka):

- posnetek pretvorjen: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- zagnan znova, že zapisana tekma se preskoči: `<file>: already written, <table>`;
- datoteka, ki ni posnetek: `<file>: not converted: <why>` (na izhodu za napake; končno stanje 1, ostali posnetki se vseeno pretvorijo);
- posnetka ni bilo najdenega: `no .wotreplay files in <folders>` (končno stanje 2).

## Možnosti {#options}

| Možnost | Privzeto | Kaj počne |
|---|---|---|
| `replays` (ena ali več) | - | datoteke `.wotreplay` ali mape, v katerih se iščejo (tudi podmape) |
| `-o`, `--out` | obvezno | mapa, v katero se piše: mapa za vsak zemljevid znotraj |
| `--force` | izklopljeno | ponovno pretvori, kar je že zapisano |
| `--version` | - | izpiše `heat3d-wot-replay <version>` in se ustavi |
| `-h`, `--help` | - | izpiše možnosti in se ustavi |

Možnosti, kot jih izpiše program: [Referenca ukazov](../cli-reference.md).

## Kaj se zapiše {#what-is-written}

Samo ločene datoteke: ta pretvornik ne zapiše datoteke `.3dheat` (pregledovalnik jih lahko zapakira v
eno: [Ena datoteka za tekmo](https://holdi601.github.io/3DHeat/container.html)). Za vsak posnetek v
`out/<map>/`:

| Datoteka | Kaj |
|---|---|
| `<match>.parquet` | tabela: položaj vsakega tanka skozi čas in vsak dogodek, kjer se je zgodil ([Tabela](table.md)) |
| `<match>.match.json` | dokument tekme: zemljevid, različica odjemalca, igralci, ubijanja, rezultati in vse ostalo ([Dokument tekme](match-document.md)) |
| `<match>.messages.parquet` | spremljevalna datoteka: vsak del posnetka, ki ga zgornji dve datoteki ne hranita celega ([Popolnost](completeness.md)) |

`<match>` je lastni identifikator bitke oziroma ime datoteke, kadar se je snemanje ustavilo, preden so
bili rezultati.

## Končno stanje {#exit-status}

`0`, kadar je bil vsak posnetek pretvorjen ali preskočen, `1`, kadar je kateri spodletel (ostali se
vseeno pretvorijo), `2`, kadar ni bila najdena nobena datoteka posnetka.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
