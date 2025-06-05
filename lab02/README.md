# Lab02: Implementacja własnego pakietu w środowisku Buildroot

Polecenie do zadania: [tutaj](https://github.com/adamgracikowski/LINSW/blob/main/lab02/polecenie.pdf)

Sprawozdanie z wykonania zadania: [tutaj](https://github.com/adamgracikowski/LINSW/blob/main/lab02/overleaf/main.pdf)

## Opis funkcjonalności pakietu `Morse`

Aplikacja realizuje prosty symulator alfabetu Morse'a z interfejsem opartym o trzy przyciski i jedną diodę LED.

### Funkcjonalności przycisków

- Przycisk `DOT` - po jego naciśnięciu do sekwencji sygnałów dodawany jest krótki sygnał (kropka),
- Przycisk `DASH` - po jego naciśnięciu do sekwencji sygnałów dodawany jest długi sygnał (pauza, czyli myślnik),
- Przycisk `ACCEPT` - po jego naciśnięciu, użytkownik zatwierdza sekwencję, która następnie zostaje odtworzona przy użyciu diody LED.

Program kończy działanie po wyświetleniu całej wprowadzonej sekwencji sygnałów.

### Działanie wyświetlania

- Po zatwierdzeniu sekwencji, system iteruje po wprowadzonych sygnałach.
- Dla kropki dioda zapala się na krótki czas ($400ms$).
- Dla myślnika dioda zapala się na dłuższy czas ($800ms$).
- Pomiędzy kolejnymi sygnałami następuje krótkie wyłączenie ($200ms$).
