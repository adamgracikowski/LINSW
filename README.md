# 🐧 Linux w Systemach Wbudowanych

Repozytorium zawiera projekty zrealizowane w ramach przedmiotu obieralnego _Linux w Systemach Wbudowanych_, w roku akademickim 2024-2025.

## Zawartość repozytorium

- Laboratoria:
  - lab01: [Wprowadzenie do środowiska Buildroot](https://github.com/adamgracikowski/LINSW/tree/main/lab01)
  - lab02: [Implementacja własnego pakietu w środowisku Buildroot](https://github.com/adamgracikowski/LINSW/tree/main/lab02)
  - lab03: [Zapoznanie z bootloader'em U-Boot, implementacja serwera WWW na Raspberry Pi](https://github.com/adamgracikowski/LINSW/tree/main/lab03)
  - lab04: [Złożony interfejs użytkownika z wykorzystaniem GPIO](https://github.com/adamgracikowski/LINSW/tree/main/lab04)
  - lab05: [Przenoszenie istniejącej aplikacji na środowisko OpenWrt](https://github.com/adamgracikowski/LINSW/tree/main/lab05)

Foldery dla poszczególnych zadań zawierają podfoldery:

- `/solution` zawierający pliki konfiguracyjne środowiska Buildroot oraz nakładki na wygenerowane obrazy systemu z kodem źródłowym oraz skryptami uruchamiającymi.
- `/overleaf` zawierający sprawozdanie (w formacie `.pdf` oraz źródłowym `.tex`) z wykonania zadania wraz z opisem dokonanych modyfikacji

## Polecenia przydatne w trakcie pracy w laboratorium

> Pobranie i rozpakowanie środowiska Buildroot:

```bash
mkdir -p /malina/gracikowskia/ccache-br \
  && cd /malina/gracikowskia \
  && wget https://buildroot.org/downloads/buildroot-2024.11.2.tar.xz \
  && tar -xJf buildroot-2024.11.2.tar.xz \
  && cd buildroot-2024.11.2
```

> Wstępna konfiguracja dla Raspberry Pi:

```bash
make raspberrypi4_64_defconfig \
  && make nconfig
```

> Serwowanie plików z lokalnego folderu:

```bash
ip a
ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1  # pobranie tylko adresu

cd /malina/gracikowskia/buildroot-2024.11.2/output/images \
  && ls -la \
  && python3 -m http.server
```

> Połączenie z płytką Raspberry Pi:

```bash
minicom -D /dev/ttyUSB0

mount /dev/mmcblk0p1 /mnt \
  && cd /mnt/user \
  && ls -la  # oryginalny plik Image powinien być widoczny
```

> Nadpisanie obrazu systemu:

```bash
rm Image \
  && wget <ip-address>:8000/Image \
  && ls -la \
  && reboot
```
