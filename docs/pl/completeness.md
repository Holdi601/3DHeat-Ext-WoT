---
title: Kompletność
nav_order: 8
lang: pl
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Kompletność {#completeness}

Nic z replaya nie jest wyrzucane. To, co odczytuje konwerter, trafia do
tabeli i dokumentu meczu; każdy inny element jest zachowany w całości w pliku
towarzyszącym `<match>.messages.parquet`; a `selfCheck.completeness` w dokumencie
meczu liczy, co stało się z każdym rodzajem elementu. To zasada, którą dzielą wszystkie konwertery 3DHeat:
[Konwertery zachowują wszystko](https://holdi601.github.io/3DHeat/converters.html).

![Samosprawdzenie syntetycznego replaya: każdy element widziany, odczytany, zachowany lub stracony](../assets/img/completeness.svg)

## Liczniki {#the-count}

Dla każdego rodzaju elementu `selfCheck.completeness.types` podaje:

| Licznik | Znaczy |
|---|---|
| `seen` | ile replay zawiera |
| `decoded` | odczytane w całości |
| `partial` | odczytane częściowo i zachowane w całości w pliku towarzyszącym |
| `raw` | tylko zachowane w całości w pliku towarzyszącym, nieodczytane |
| `lost` | stracone: zawsze `0` |

Rodzaje są własne dla replaya: `block 0` (nagłówek), `block 1` (wyniki),
`container sizes` i `deflate tail` (własne bajty kontenera),
`packet <type>`, a dla wywołań obiektów `method <entity type>.<number>`
i `property <entity type>.<number>`. Typy obiektów to liczby, które podają
pakiety tworzące; `selfCheck.entities.roles` mówi, który to awatar nagrywającego gracza,
a które to pojazdy. Rodzaj, o którym nikt nie wiedział, pojawia się z własnym licznikiem.

## Plik towarzyszący {#the-sidecar}

| Kolumna | Co to jest |
|---|---|
| `time` | zegar replaya, jak w tabeli |
| `type`, `name` | rodzaj elementu; jak nazywa go konwerter, tam gdzie go czyta |
| `entity` | pojazd albo awatar, do którego należy, jak `entity` w tabeli |
| `decoded` | co z niego odczytano, jako JSON |
| `payload`, `text` | jego bajty w całości; bloki JSON w całości |
| `entityType`, `packet`, `method` | liczby |

Wiersze są posortowane wg pakietu, metody, obiektu i czasu.

## Co jest odczytywane i jak to sprawdzono {#what-is-read-and-how-it-was-checked}

- **Pochylenie i przechył** każdej pozycji: pochylenie to minus nachylenie własnej drogi czołgu, gdy jedzie do przodu; dwa czołgi w jednym miejscu z jednym kursem mają ten sam przechył, z przeciwnymi kursami – przeciwne przechyły.
- **Obiekty** (`entities`): kiedy każdy wszedł do widoku klienta i kiedy z niego wyszedł.
  Żaden czołg nie ma pozycji między wyjściem a powrotem.
- **Wersja w strumieniu** (`streamVersion`): taka sama jak w nagłówku.
- **Celowanie nagrywającego gracza** (pakiet 38): kierunek, w `decoded` pliku towarzyszącego
  (`forward`); przy strzałach gracza jest w ułamku stopnia od tego, dokąd leciał pocisk.

Wszystko inne odczytane (zdrowie, trafienia, strzały, smugi, wybuchy, kąty
działa, aktualizacje areny, czat, tryby kamery, zdarzenia klienta, pozycje) jest `partial`:
w tabeli lub dokumencie meczu, a w całości w pliku towarzyszącym.

**Zachowane, ale nieodczytane** (`raw`), największe rodzaje: aktualizacje pozycji, których nie ma w tabeli (awatara po śmierci czołgu,
obiekty spoza listy), pakiety 26, 28, 29, 31, 36, 50, 54 i 57, niektóre częste właściwości pojazdów i awatarów,
każda metoda i właściwość bez czytnika (wśród nich uszkodzenia modułów, załoga i
wyposażenie), oraz właściwości tworzenia obiektów.

## Niedostępne {#not-available}

- To, czego serwer nigdy nie wysłał nagrywającemu klientowi: celowanie innych graczy,
  kamera i sterowanie, wrogowie, dopóki nie zostali wypatrzeni. Replay to to, co jeden klient
  został poinformowany.
- Nazwy typów obiektów, metod i właściwości: są w plikach definicji gry, a nie w replayu.
  Liczby są zachowane.
- Podniesienie działa w stopniach i wszystko inne, co wymaga własnych danych czołgów z plików gry.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
