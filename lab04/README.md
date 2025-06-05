# Lab04: Złożony interfejs użytkownika z wykorzystaniem GPIO

Polecenie do zadania: [tutaj](https://github.com/adamgracikowski/LINSW/blob/main/lab04/polecenie.pdf)
Sprawozdanie z wykonania zadania: [tutaj](https://github.com/adamgracikowski/LINSW/blob/main/lab04/overleaf/main.pdf)

## Opis aplikacji

System składa się z dwóch modułów:

- Webowego interfejsu planisty,
- Hardware’owego modułu pracownika linii produkcyjnej.

Wprzyjętym modelu każde zamówienie tworzone przez planistę składa się z nazwy oraz okre
ślonej liczby sztuk trzech rodzajów elementów (produktów):

- Kategorii A,
- Kategorii B,
- Kategorii C.

### Webowy interfejs planisty

- Dostępny tylko po zalogowaniu.
- Pozwala wyświetlić listy zamówień z podziałem na ich aktualny stan:
  - W oczekiwaniu na realizację (`pending`),
  - W trakcie realizacji (`in_progress`),
  - Ukończone (`completed`).
- Umożliwia dodawanie nowych zamówień, które są dodawane do kolejki zamówień oczekujących.
- Wyświetla postęp realizacji aktualnie montowanego zamówienia.
- Pozwala zresetować linię produkcyjną w przypadku zgłoszenia awarii przez pracownika realizującego zamówienie.
- Po zresetowaniu linii produkcyjnej wznawiane jest zamówienie realizowane przed występnieniem awarii.

### Moduł pracownika linii produkcyjnej

- Po uruchomieniu łączy się z serwerem i pobiera z kolejki nowe zamówienie.
- W trakcie realizacji zamówienia świeci się zielona dioda.
- Pracownik ma dostęp do następujących przycisków:
  - Zmontowano element kategorii `A`,
  - Zmontowano element kategorii `B`,
  - Zmontowano element kategorii `C`,
  - Awaria na linii produkcyjnej.
- Wciśnięcie przycisku o zmontowaniu elementu powoduję aktualizację progresu zamówienia w interfejsie webowym planisty.
- Po zrealizowaniu zamówienia z kolejki pobierane jest następne zamówienie.
- W przypadku braku dostępnych zamówień świeci się żółta dioda.
- Po wciśnięciu przycisku awarii zapala się czerwona dioda, odświeża się interfejs webowy oraz jest wysyłane powiadomienie mailowe do planisty, z informacją o wystąpieniu awarii.
