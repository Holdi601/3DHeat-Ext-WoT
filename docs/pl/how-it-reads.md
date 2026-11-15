---
title: Jak czytany jest replay
nav_order: 7
lang: pl
source: how-it-reads.md
source_hash: "cded05962390"
nav_exclude: true
search_exclude: true
---
# Jak czytany jest replay {#how-it-reads-a-replay}

Replay to nagłówek z bloków JSON i strumień pakietów gry (uwagi o formacie w
[`heat3d_ext_wot/bigworld.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/bigworld.py)):

- Pierwszy blok, jawnie: mapa, wersja klienta, nagrywający gracz, ustawienia serwera
  i lista graczy (`vehicles`: nazwa, drużyna, czołg, kluczowane identyfikatorem pojazdu).
- Drugi, gdy nagrywanie trwało do końca: ekran wyników – wiersz każdego pojazdu
  (strzały, trafienia, przebicia, zadane, otrzymane, zablokowane i wsparte obrażenia, wykrycia, doświadczenie, kredyty, osiągnięcia...),
  szczegóły nagrywającego gracza wobec każdego celu, konta, czas trwania meczu,
  zwycięzca i powód zakończenia; w niektórych trybach jedyna pełna lista graczy (nagłówek
  tych list zawiera tylko własną drużynę).
- Strumień pakietów, skompresowany zlib i zaszyfrowany Blowfishem kluczem, który dołącza gra,
  a który narzędzia społeczności czytające te pliki publikują od 2013 roku.

**Pozycje** to aktualizacje pozycji silnika: identyfikator pojazdu, jego pozycja
i kurs, rozpoznawane po kształcie, a nie po numerze pakietu, więc poprawka, która
przenumeruje pakiety, nie opróżni tabeli. To, co dostał nagrywający klient: własna drużyna przez cały czas,
wróg tylko, gdy został wypatrzony (albo w zasięgu klienta). Pojazd, który nigdy nie został
wypatrzony, nie ma wierszy. Wiersze pojazdu kończą się na jego śmierci.

**Reszta strumienia** – zdrowie, strzały, smugi, wybuchy, trafienia, kąty
działa, aktualizacje areny – to wywołania metod i zmiany właściwości pojazdów
oraz awatara klienta, ponumerowane przez pliki definicji gry, które zmieniają się wraz z łatami (1.12 i 2.4 numerują je inaczej). Każde jest znajdowane
po kształcie argumentów i tym, jak się trzymają razem – zob.
[`heat3d_ext_wot/stream.py`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/heat3d_ext_wot/stream.py) – a znalezione
liczby są w `decoded` dokumentu meczu. Czat, tryb kamery i własne zdarzenia klienta to osobne
pakiety. Aktualizacje areny i zdarzenia klienta są pickle w Pythonie; czyta je czytnik, który zamienia
każdą nazwaną klasę w bezwładny zastępnik i nic nie uruchamia.

To, co dostał klient, jest kompletne dla własnej drużyny, a częściowe dla
wrogów: ich strzały, trafienia i zmiany zdrowia są tam, gdy byli w zasięgu.

**Początek bitwy** to moment, w którym aktualizacja areny mówi, że okres bitwy się zaczął;
w replayu bez niej – pierwsza chwila, w której jakikolwiek pojazd się rusza.

**Zgony:** czas to komunikat areny o zabójstwie (1.x), w przeciwnym razie zmiana zdrowia, która
zakończyła pojazd, w przeciwnym razie początek bitwy plus `lifeTime` ofiary
z wyników (w pełnych sekundach). Miejsce to miejsce, w którym ofiarę widziano ostatnio,
gdy było to w ciągu pięciu sekund od jej śmierci; w przeciwnym razie, u klientów 2.x,
miejsce podane w wynikach (x i z, bez wysokości), tylko w dokumencie meczu. Nagranie,
które zatrzymało się przed końcem, nie ma zgonów.

**Nieodczytane:**

- Wykrywanie i minimapa: nie ma ich w strumieniu jako osobnych zdarzeń.
- Podniesienie działa w stopniach: strumień ma krok między ograniczeniami działa,
  a ograniczenia są w plikach pojazdów gry.
- Uszkodzenia modułów, obrażenia załogi, wyposażenie i amunicja: wywołania, które je
  niosą, nie dały się odróżnić po samym kształcie w 1.12 i 2.4.
- Pakiety tworzenia obiektów poza obiektem i jego typem: niosą każdą właściwość pojazdu
  wjeżdżającego naraz do widoku klienta, w kolejności znanej tylko z plików definicji (zachowane w całości w pliku towarzyszącym).
- Statyczne kolizje (drzewa, domy), własne celowanie nagrywającego gracza i pakiety fizyki.
- Numery komend czatu bitewnego jako nazwy: numeracja jest grze własna i się zmienia; dokument meczu
  zachowuje argumenty każdej komendy, w tym jej klucz, jeśli go ma (`ATTACK_ENEMY`, ...).
- Powody ataku powyżej 5: zapisane tylko jako liczby.

## Jak sprawdzono odczyt {#how-the-reading-was-checked}

Odczyt sprawdzono na publicznych replayach klientów 1.12 i 2.4, każdą
wartość względem czegoś, co replay podaje drugi raz:

- **Pozycje:** każdy czołg, jaki kiedykolwiek widziano, ma tor z dziesięcioma próbkami na sekundę; prędkości mieszczą się w tym,
  co czołg potrafi; kurs zgadza się z kierunkiem ruchu w granicach około 0,02 rad; tam, gdzie wyniki podają miejsce zgonu,
  miejsce odczytane tutaj jest w granicach kilku metrów od niego.
- **Nagrywający gracz:** strzały i zadane obrażenia odczytane są równe wartościom
  z wyników, na każdym sprawdzonym replayu.
- **Zdrowie:** ostatni odczyt zdrowia każdego czołgu równa się wynikom; odczytane
  otrzymane obrażenia nigdy nie są większe niż w wynikach. W wersji 2.4 cios śmiertelny
  czołgu spoza widoku klienta często nie jest wysyłany.
- **Trafienia:** obrażenia trafienia równają się zmianie zdrowia w tym momencie przy
  niemal każdym trafieniu.
- **Wieża:** przy strzale kurs kadłuba plus obrót wieży wskazują tam, gdzie
  przeleciała smuga, w granicach około 0,01 rad (mediana).
- **Zgony i początek bitwy:** w granicach około sekundy od tego, co mówią wyniki i arena.

Testy budują replaye w tym samym układzie, więc żaden prawdziwy replay nie jest
przechowywany w tym repozytorium.

**Nie sprawdzono:** klientów przed 1.12, replayów konsolowych i Blitz (inne
gry), Mir Tankov Lesty (`.mtreplay`) oraz tryby inne niż bitwy losowe i typ bitwy 20.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
