# Lab04

Pobranie środowiska:

```bash
mkdir -p /malina/gracikowskia/ccache-br \
  && cd /malina/gracikowskia \
  && wget https://buildroot.org/downloads/buildroot-2024.11.2.tar.xz \
  && tar -xJf buildroot-2024.11.2.tar.xz \
  && cd buildroot-2024.11.2
```

Wstępna konfiguracja Buildroot-a:

```bash
make raspberrypi4_64_defconfig \
  && make nconfig
```

Uruchomienie Minicom:

```bash
minicom -D /dev/ttyUSB0

mount /dev/mmcblk0p1 /mnt \
  && cd /mnt/user \
  && ls -la
```
