# Desktop PC Linux Setup Guide

Install and customize Endeavour OS on Desktop PC (i7-6700K, AMD RX 6600, 16GB RAM).

## Table of Contents

- [Install yay](#install-yay)
- [Install VeraCrypt](#install-veracrypt)
- [Remove Battery Indicator](#remove-battery-indicator)
- [Install Zen Kernel](#install-zen-kernel)
- [Install ZRAM Swap](#install-zram-swap)
- [Disable Bluetooth](#disable-bluetooth)
- [Customize GRUB](#customize-grub)
- [Remove Screen/App Association from i3](#remove-screenapp-association-from-i3)
- [Install Sensors](#install-sensors)
- [Install Text Editors](#install-text-editors)

---

## Install yay

Install it once as a prerequisite for all subsequent `yay -S` commands in this guide.
This command only works in Endeavor OS, as it ships with some extra repos that provide yay.

```bash
sudo pacman -S yay
```

---

## Install VeraCrypt

```bash
yay -S veracrypt
```

---

## Remove Battery Indicator

Open the i3blocks config and comment out the battery section:

```bash
nano ~/.config/i3/i3blocks.conf
```

---

## Install Zen Kernel

```bash
yay -S linux-zen linux-zen-headers
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## Install ZRAM Swap

```bash
yay -S zram-generator
```

For configuration, see the [Install ZRAM section in the XPS 9560 guide](../xps9560/README.md#install-zram).

---

## Disable Bluetooth

```bash
sudo systemctl disable bluetooth.service
```

---

## Customize GRUB

```bash
yay -S grub-customizer
```

---

## Remove Screen/App Association from i3

Open the i3blocks config and comment out the Firefox/terminal/Thunar mappings to virtual desktops:

```bash
nano ~/.config/i3/i3blocks.conf
```

---

## Install Sensors

```bash
yay -S lm_sensors
```

---

## Install Text Editors

```bash
yay -S neovim
yay -S vscodium-bin
yay -S lite-xl
```