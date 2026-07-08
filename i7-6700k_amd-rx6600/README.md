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
- [Screen Composition](#activate-screen-composition)

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

## Set screen order

Open arandr and see exact ports' names (i.e. HDMI-1 and DP-2).
Then create the Xserver configuration file:

sudo nano /etc/X11/xorg.conf.d/10-monitor.conf

And write this inside

Section "Monitor"
    Identifier  "HDMI-1"
    Option      "Primary" "true"
EndSection

Section "Monitor"
    Identifier  "DP-2"
    Option      "RightOf" "HDMI-1"
EndSection


## Set custom dual wallpaper

Disable EndeavorOS default wallpaper: run 

nano i3 ~/.config/i3/config

Replace this line (or a similar one)

exec --no-startup-id sleep 1 && feh --bg-fill /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png

With this line
exec_always --no-startup-id feh --bg-scale --no-xinerama <path/to/image.jpg>

## Install and configure Flameshot

Edit the i3 config file:

```bash
nano ~/.config/i3/config
```

And replace the bindings associated with print key with this:

bindsym Print exec --no-startup-id flameshot gui

If the screenshot fails due to Xserver, and to avoid the screen selection window, create the config file and its relative directory.
mkdir ~/.config/flameshot

Then create the config file:
nano ~/.config/flameshot/flameshot.ini

And write this inside

[General]
useX11LegacyScreenshot=true
captureActiveMonitor=true

Or use the flameshot config utility selecting the same options.
```bash
flameshot config
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

---

## Activate Screen Composition

Install picom to use fade-in and fade-out animations as well as transparency for terminal windows.
```bash
yay -S picom
```
Open the alacritty configuratio file:
```bash
nano ~/.config/alacritty/alacritty.toml
```
And add the following line;
```toml
[window]
opacity = 0.85
```
Then open i3 config file
```bash
nano ~/.config/i3/config
```
And add the following line to start picom at startup
```text
exec_always --no-startup-id picom -b
```
Then customize picom parameters for the desired appearance. 
Create the default folder for picom config and copy the default config file inside it.
```bash
mkdir -p ~/.config/picom
cp /etc/xdg/picom.conf ~/.config/picom/picom.conf
```
Edit the config file to match the desired appearance (i.e. set delta for different fade speed).
```bash
nano ~/.config/picom/picom.conf
```
