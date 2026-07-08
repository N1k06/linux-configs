# Raionbook K4 (AIstone X4KKNAL) Linux Optimization Guide

Install and customize Linux on Raionbook K4 (barebone AIstone X4KKNAL), with AMD Ryzen AI 7 350 CPU, 32 GBs of RAM and 14" LED QHD+ display.

## Table of Contents

- [General Configuration](#general-configuration)
  - [Hibernation](#hibernation)
  - [Fix Keyboard after suspend (generic)](#fix-keyboard-after-suspend-generic)
  - [Disable Bluetooth](#disable-bluetooth)
  - [Install Powertop & CPU Autofreq](#install-powertop--cpu-autofreq)
- [CachyOS (Sway)](#cachyos-sway)
  - [Add screen lock](#add-screen-lock)
  - [Awake Keyboard after lid opened](#awake-keyboard-after-lid-opened)
  - [Customize windows' borders](#customize-windows-borders)
  - [Terminal transparency](#terminal-transparency)
  - [Enable Dark Mode on PCManFM](#enable-dark-mode-on-pcmanfm)
  - [Change background](#change-background)
  - [Enable keyboard shortcuts (volume and screen brightness)](#enable-keyboard-shortcuts-volume-and-screen-brightness)
  - [Add indicators/buttons to bar](#add-indicatorsbuttons-to-bar)
- [EndeavorOS (i3)](#endeavoros-i3)
  - [Set screen DPI](#set-screen-dpi)

---

## General Configuration

### Hibernation

BIOS does not support deep sleep. To ensure safety when in a bag during installation, provide at least 32GB of swap to allow full hibernation.

### Fix Keyboard after suspend (generic)

This solution prevents the laptop from fully entering sleep, so it should be avoided.

```bash
sudo nano /etc/modprobe.d/amd_pmc.conf
```

Add the following line:
```conf
options amd_pmc enable_stb=1
```

Then run:
```bash
sudo mkinitcpio -P
```

### Disable Bluetooth

TODO

### Install Powertop & CPU Autofreq

TODO

---

## CachyOS (Sway)

### Add screen lock

Install `swaylock` and edit the config file.

### Awake Keyboard after lid opened

The keyboard becomes unresponsive after resume from suspend (s2idle). This happens because of a bug that affects other similar laptops as well.

This is a known, fairly widespread issue on multiple AMD Ryzen laptops using s2idle (reported across different OEMs using similar reference designs), tied to firmware/EC timing during resume — not something caused by user configuration. Kernel parameters (`atkbd.reset`, `i8042.nomux`, `i8042.reset`, etc.) did not reliably fix it.

**Root cause** (confirmed via kernel log):
The i8042/atkbd driver fails to reset the internal PS/2 keyboard controller during resume:

```
atkbd serio0: keyboard reset failed on isa0060/serio0
atkbd serio0: Failed to deactivate keyboard on isa0060/serio0
atkbd serio0: Failed to enable keyboard on isa0060/serio0
```

**Fix:**

A systemd hook that force-unbinds the atkbd driver from serio0 shortly after resume, triggering the kernel's automatic serio reconnect/reset logic (a manual re-bind is unnecessary — the kernel re-attaches the driver on its own).

> **Note:** The standard `/etc/systemd/system-sleep/` hook directory did not get invoked automatically on this system for reasons still unclear (script executes fine when run manually, but was never triggered by real suspend cycles). Bypassed this by attaching the script directly via a systemd unit drop-in instead.

**1. Create the folder that contains the script:**

```bash
sudo mkdir /etc/systemd/system-sleep
```

**2. Create the script:**

```bash
sudo nano /etc/systemd/system-sleep/atkbd-fix.sh
```

Write this inside (the logging can be removed if desired):

```bash
#!/bin/bash
case "$1" in
  post)
    logger "atkbd-fix: post-resume hook triggered"
    sleep 1
    if echo "serio0" > /sys/bus/serio/drivers/atkbd/unbind; then
      logger "atkbd-fix: unbind OK"
    else
      logger "atkbd-fix: unbind FAILED"
    fi
    sleep 0.5
    if echo "serio0" > /sys/bus/serio/drivers/atkbd/bind; then
      logger "atkbd-fix: bind OK"
    else
      logger "atkbd-fix: bind FAILED"
    fi
    ;;
esac
```

**3. Give the script execution privileges:**

```bash
sudo chmod 0755 /etc/systemd/system-sleep/atkbd-fix.sh
```

**4. Force it to run via a drop-in on systemd-suspend.service:**

Create the folder containing the service that attaches to systemd-suspend.service:

```bash
sudo mkdir -p /etc/systemd/system/systemd-suspend.service.d
```

Create the configuration file inside:

```bash
sudo nano /etc/systemd/system/systemd-suspend.service.d/atkbd-fix.conf
```

Write this inside:
```ini
[Service]
ExecStopPost=/etc/systemd/system-sleep/atkbd-fix.sh post suspend
```

**5. Reload the systemctl daemon:**

```bash
sudo systemctl daemon-reload
```

> **Note:** This is a workaround, not a root-cause fix — the underlying firmware/EC issue (also reflected in an unrelated ACPI BIOS error, `_SB.ACDC.RTAC AE_NOT_FOUND`, seen on every suspend/resume cycle) remains unresolved upstream.

### Customize windows' borders

Add the following to your sway config file:

```conf
default_border pixel 2
gaps inner 10
gaps outer 5
```

⚠️ **Watch out for upscaling!** Pixels specified here are upscaled 2x.

### Terminal transparency

Edit `foot.ini`:

```ini
[main]
font=monospace:size=7

[colors-dark]
# Set the background (6-digit hex, e.g., 000000 for black or 1e1e1e for dark gray)
background=000000

# Set opacity here (0.0 to 1.0)
alpha=0.85
```

### Enable Dark Mode on PCManFM

Create the config directory and file:

```bash
mkdir -p ~/.config/gtk-3.0
nano ~/.config/gtk-3.0/settings.ini
```

Add the following:

```ini
[Settings]
gtk-theme-name = Adwaita-dark
gtk-application-prefer-dark-theme = true
```

### Change background

Install `swaybg` and change the picture path from the config file:

```bash
yay -S swaybg
```

### Enable keyboard shortcuts (volume and screen brightness)

Audio already works from the sway config default file. For brightness control, install `brightnessctl`:

```bash
yay -S brightnessctl
```

### Add indicators/buttons to bar

TODO
- Battery
- Audio
- Network
- Shutdown

---

## EndeavorOS (i3)
### Set screen DPI

Set screen DPI to 144 by configuring the X server.

**1. Edit .Xresources:**

```bash
nano ~/.Xresources
```

Add these lines:

```
Xft.dpi: 144
Xcursor.size: 32
```

**2. Edit i3 config file:**

```bash
nano ~/.config/i3/config
```

Add this line to auto-merge Xresources on startup:

```bash
exec_always xrdb -merge ~/.Xresources
```

**3. Set scaling for Qt apps:**

Create or edit your xprofile/bashprofile:

```bash
nano ~/.xprofile
```

Or:

```bash
nano ~/.bashprofile
```

Add these lines:

```bash
export QT_AUTO_SCREEN_SCALE_FACTOR=0
export QT_SCALE_FACTOR=1.5
```

### Install AMD Microcode
Prevent system slowdown when using gpu (i.e. decoding videos from youtube)

yay -S amd-ucode
---

### Increase size of context menus

Increase powermenu size by opening its config file:

```bash
nano ~/.config/i3/scripts/powermenu
```
Search "rofi" section and set a bigger font size:
chosen="$(echo -e "$options" | rofi -dmenu -i -p "Power Menu" \
  -font "Noto Sans Regular 16" \
  -theme $ROFI_THEME)"


Increase rofi size by opening its config file:
```bash
nano ~/.config/i3/config
```

Add the font flag to the line launching the menu:

```text
bindsym $mod+d exec --no-startup-id rofi -font "Noto Sans Regular 16" -show drun -theme ~/.config/rofi/launchers/type-1/style-1.rasi
```

---

## Change order of Systemd-boot entries

---

## Install zen kernel

---

## Install and configure screen composition

---