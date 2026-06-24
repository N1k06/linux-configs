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
- [Setup Alacritty with Iosevka Fonts](#setup-alacritty-with-iosevka-fonts)
- [Set background](#set-the-double-monitor-background)

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

Open the i3blocks config and comment out the Firefox/Terminal/Thunar mappings to virtual desktops:

```bash
nano ~/.config/i3/config
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

---

## Setup Alacritty with Iosevka Fonts

Install packages:
```bash
yay -S ttf-iosevka-nerd
yay -S alacritty
```

Edit the default Terminal Emulator in the i3 configuration file (search for terminal and replace xfce4-terminal)

```bash
nano ~/.config/i3/config
```

Create che configuration directory for alacritty:

```bash
mkdir -p ~/.config/alacritty
```

Edit the default font:
```bash
nano ~/.config/alacritty/alacritty.toml
```
Paste font setup inside:
```toml
[font]
size = 12.0

[font.normal]
family = "Iosevka Nerd Font"
style = "Regular"

[font.bold]
family = "Iosevka Nerd Font"
style = "Bold"

[font.italic]
family = "Iosevka Nerd Font"
style = "Italic"

[font.bold_italic]
family = "Iosevka Nerd Font"
style = "Bold Italic"
```

---

## Set the double monitor background

Open the i3 config file:
```bash
nano ~/.config/i3/config
```
Tell i3 to load the picture on both screens at startup with feh by adding this line at the end:
```bash
exec_always --no-startup-id feh --bg-scale --no-xinerama /path/to/picture.jpg
```
