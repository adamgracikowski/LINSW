# Lab03

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

Skopiowanie pliku `.config` dla systemu `Admin`:

```bash
cp ./.config /malina/gracikowskia/buildroot-2024.11.2 \
  && make nconfig

cd output/images \
  && ls -la

mv Image Image.admin \
  && mv u-boot.bin Image \
  && ls -la \
  && ip a \
  && python3 -m http.server
```

Uruchomienie Minicom:
```bash
minicom -D /dev/ttyUSB0

mount /dev/mmcblk0p1 /mnt \
  && cd /mnt/user \
  && ls -la

mkimage -T script -C none -n 'Start script' -d boot.txt boot.scr
```

Skopiowanie pliku `.config` dla systemu `User`:
```bash
mv Image Image.user \
  && ls -la \
  && ip a \
  && python3 -m http.server
```
