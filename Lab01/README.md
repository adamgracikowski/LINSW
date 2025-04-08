# Cheat Sheet:

Download Buildroot:

```bash
mkdir -p /malina/gracikowskia/ccache-br \
  && cd /malina/gracikowskia \
  && wget https://buildroot.org/downloads/buildroot-2024.11.2.tar.xz \
  && tar -xJf buildroot-2024.11.2.tar.xz \
  && cd buildroot-2024.11.2
```

Configure for Raspberry Pi 4:

```bash
make raspberrypi4_64_defconfig \
  && make nconfig
```

Start http server:

```bash
ip a
ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1  # to get just the address

cd /malina/gracikowskia/buildroot-2024.11.2/output/images \
  && ls -la \
  && python3 -m http.server
```

Start Minicom:

```bash
minicom -D /dev/ttyUSB0
```

Mount:

```bash
mount /dev/mmcblk0p1 /mnt \
  && cd /mnt/user \
  && ls -la                  # Image file should be listed here
```

Get the `Image`:

```bash
rm Image \
  && wget <ip address>:8000/Image \
  && ls -la \
  && reboot                  # to run the system with uploaded Image
```
