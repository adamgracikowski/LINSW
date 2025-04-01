# LINSW

Pobranie środowiska:
```bash
mkdir -p /malina/gracikowskia/ccache-br \
  && cd /malina/gracikowskia \
  && wget https://buildroot.org/downloads/buildroot-2024.11.2.tar.xz \
  && tar -xJf buildroot-2024.11.2.tar.xz \
  && cd buildroot-2024.11.2
```

Wstępna konfiguracja:
```bash
make raspberrypi4_64_defconfig \
  && make nconfig
```

```bash
mkdir -p package/quiz \
  && cd package/quiz \
  && touch Config.in \
  && touch quiz.mk \
  && nano Config.in
```
