# LINSW

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

Kompilacja aplikacji:
```bash
cd /malina/gracikowskia/buildroot-2024.11.2/packages/morse/src \
  && code .

source /malina/gracikowskia/buildroot-2024.11.2/output/host/environment-setup

rm *.o \
  && rm morse \
  && make
```

Uruchamianie serwera http:
```bash
ip a

python3 -m http.server
```

Minicom:
```bash
minicom -D /dev/ttyUSB0

mount /dev/mmcblk0p1 /mnt \
  && cd /mnt/user \
  && ls -la
```

Pobieranie aplikacji na urządzenie:
```bash
rm morse \
  && wget 192.168.122.1:8000/morse \
  && chmod +x morse \
  && ./morse
```

Konfiguracja domowa:

```bash
mkdir -p /home/adam/linsw/ccache-br \
  && cd /home/adam/linsw \
  && wget https://buildroot.org/downloads/buildroot-2024.11.2.tar.xz \
  && tar -xJf buildroot-2024.11.2.tar.xz \
  && cd buildroot-2024.11.2
```
