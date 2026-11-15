---
title: Dokument meczu
nav_order: 6
lang: pl
source: match-document.md
source_hash: "177568e76e30"
nav_exclude: true
search_exclude: true
---
# Dokument meczu {#the-match-document}

`<match>.match.json` zawiera wszystko, co replay mówi, a co nie jest wierszem
tabeli. Karta Mecz w przeglądarce czyta właśnie ten plik. (W kodzie nazywa się go podsumowaniem.)

![Początek syntetycznego dokumentu meczu i jego klucze](../assets/img/match-document.svg)

## Bitwa {#the-battle}

| Klucz | Co to jest |
|---|---|
| `format`, `version` | `heat3d-wot-match`, `2` |
| `game`, `match`, `map`, `mapName` | `World of Tanks`; identyfikator bitwy; identyfikator mapy i jej nazwa wyświetlana |
| `clientVersion`, `streamVersion` | wersja gry z nagłówka i taka, jaką podaje strumień pakietów |
| `recorded` | kiedy replay został nagrany, tak jak zapisuje to gra |
| `player`, `vehicle` | nagrywający gracz i jego czołg |
| `battleType`, `gameplay`, `server`, `region`, `hasMods` | numer typu bitwy z nagłówka, tryb gry, serwer, region i to, czy zainstalowano mody |
| `duration` | długość bitwy w sekundach, z wyników |
| `winnerTeam`, `finishReason` | drużyna zwycięska i numer gry dla sposobu zakończenia bitwy, z wyników |
| `complete`, `truncated` | wyniki są w replayu; nagrywanie zatrzymało się wcześniej |
| `battleStart`, `battleStartFrom`, `firstMovement` | początek bitwy w sekundach nagrania; `arena` (tak mówi arena) lub `movement` (pierwsza chwila, w której ruszył jakikolwiek czołg); ten pierwszy ruch |
| `recordingSeconds` | długość nagrania w sekundach |
| `positionPacket`, `hz`, `positions` | numer pakietu, w którym przyszły pozycje, próbki na sekundę, wiersze pozycji |
| `events` | liczba wierszy tabeli każdego zdarzenia |
| `units` | `metres; x east, y up, z north` (metry; x na wschód, y w górę, z na północ) |
| `decoded` | numery metod i pakietów znalezione dla każdego rodzaju komunikatu |

## Gracze i zdarzenia {#players-and-events}

| Klucz | Co to jest |
|---|---|
| `players` | jeden wpis na czołg: nazwa, drużyna, czołg, klan, próbki, zabójstwa, zadane obrażenia, przeżycie, czas życia; `seen` (strzały i obrażenia, które widział nagrywający klient); pełny wpis z nagłówka i z wyników oraz konto |
| `kills` | każdy zgon: czas (sekundy), skąd pochodzi czas (`arena`, `health` lub `lifeTime`), ofiara, zabójca, numer i nazwa powodu |
| `periods` | okresy bitwy (oczekiwanie, przed bitwą, bitwa, po bitwie) z czasami końca podanymi przez serwer |
| `basePoints` | postęp przechwytywania bazy na drużynę i bazę |
| `chat`, `commands` | linie czatu; komendy czatu bitewnego ze wszystkimi argumentami |
| `camera`, `clientEvents` | tryby kamery nagrywającego gracza; to, co klient nagrał o sobie (zoom, automatyczne celowanie, zmiany celu, stan pojazdu) |
| `arenaUpdates` | każda aktualizacja areny, odczytana, tak jak wysłała ją gra |

## Wyniki i sprawdzenia {#results-and-checks}

| Klucz | Co to jest |
|---|---|
| `serverSettings` | ustawienia serwera z nagłówka |
| `results`, `resultVehicles`, `frags` | ekran wyników: wspólne, osobiste (ze szczegółami wobec celów), gracze, konta; wiersz wyników każdego czołgu; zabójstwa na gracza |
| `entities` | każdy obiekt, który tworzy strumień: jego numer typu i rola, kiedy wszedł do widoku klienta i kiedy z niego wyszedł |
| `selfCheck` | licznik kompletności ([Kompletność](completeness.md)) oraz sprawdzenia obiektów i wersji |

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
