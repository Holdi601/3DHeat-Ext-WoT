---
title: Konwertowanie replayów
nav_order: 4
lang: "pl"
source: converting.md
source_hash: "489c52c182ae"
nav_exclude: true
search_exclude: true
---
# Konwertowanie replayów {#converting-replays}

## Krok po kroku {#step-by-step}

1. **Włącz nagrywanie** w grze: Ustawienia > Ogólne > Nagrywaj bitwy.
   Od tej chwili gra zapisuje każdą bitwę w folderze `replays` Twojej instalacji
   World of Tanks, na przykład
   `C:\Games\World_of_Tanks_EU\replays`.
2. **Otwórz terminal** w folderze, do którego mogą trafić wyniki
   ([Zanim zaczniesz](before-you-start.md)).
3. **Uruchom konwerter** na plikach replayów albo na folderach, które je zawierają:

   ```bash
   heat3d-wot-replay "C:\Games\World_of_Tanks_EU\replays" -o out
   heat3d-wot-replay a.wotreplay b.wotreplay -o out
   ```

   Folder `out` powstaje w folderze, w którym jest terminal.
4. **Przeczytaj, co pisze.** Powinieneś zobaczyć jedną linię na replay, kończącą się
   tabelą, którą zapisał.
5. **Otwórz wynik** w przeglądarce 3DHeat: `out/<map>/<match>.parquet`
   na karcie Mapa cieplna, `<match>.match.json` na karcie Mecz. Albo odczytaj je
   dowolnym czytnikiem Parquet lub JSON.

![Przebieg na syntetycznym replayu: konwertowanie, ponowne uruchomienie, uszkodzony plik, pusty folder](../assets/img/convert.svg)

Obrazek to przebieg na replayu, który testy budują w kodzie (bez prawdziwego replaya):

- replay przekonwertowany: `<file>: <n> positions of <n> vehicles at <rate> Hz, <n> deaths, <map> (<client version>) -> <table>`;
- uruchomione ponownie, mecz już zapisany zostaje pominięty: `<file>: already written, <table>`;
- plik, który nie jest replayem: `<file>: not converted: <why>` (w wyjściu błędów;
  status wyjścia 1, pozostałe replaye są nadal konwertowane);
- nie znaleziono replaya: `no .wotreplay files in <folders>` (status wyjścia 2).

## Opcje {#options}

| Opcja | Domyślnie | Działanie |
|---|---|---|
| `replays` (jeden lub więcej) | - | pliki `.wotreplay` albo foldery, w których się ich szuka (także podfoldery) |
| `-o`, `--out` | wymagana | folder, do którego zapisywać: w środku folder na każdą mapę |
| `--force` | wyłączona | przekonwertuj ponownie to, co już jest zapisane |
| `--version` | - | wypisz `heat3d-wot-replay <version>` i zakończ |
| `-h`, `--help` | - | wypisz opcje i zakończ |

Opcje tak, jak wypisuje je program: [Opis poleceń](../cli-reference.md).

## Co jest zapisywane {#what-is-written}

Tylko pliki luźne: ten konwerter nie zapisuje pliku `.3dheat` (przeglądarka
może spakować je w jeden: [Jeden plik na mecz](https://holdi601.github.io/3DHeat/container.html)).
Na każdy replay, w `out/<map>/`:

| Plik | Co to jest |
|---|---|
| `<match>.parquet` | tabela: pozycja każdego czołgu w czasie i każde zdarzenie, w którym się wydarzyło ([Tabela](table.md)) |
| `<match>.match.json` | dokument meczu: mapa, wersja klienta, gracze, zabójstwa, wyniki i cała reszta ([Dokument meczu](match-document.md)) |
| `<match>.messages.parquet` | plik towarzyszący: każdy element replaya, którego dwa powyższe pliki nie przechowują w całości ([Kompletność](completeness.md)) |

`<match>` to własny identyfikator bitwy albo nazwa pliku, gdy nagrywanie
zatrzymało się przed wynikami.

## Status wyjścia {#exit-status}

`0`, gdy każdy replay został przekonwertowany lub pominięty; `1`, gdy któryś się nie
udał (pozostałe są nadal konwertowane); `2`, gdy nie znaleziono żadnego pliku replaya.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
