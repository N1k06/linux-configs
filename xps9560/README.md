# XPS 9560 Linux Optimization Guide

Install and customize Endeavor OS on Dell XPS 15 (9560).

## Table of Contents

- [Remove TPM Slowdown on Boot](#remove-tpm-slowdown-on-boot)
- [Install yay](#install-yay)
- [Disable NVIDIA Discrete GPU](#disable-nvidia-discrete-gpu)
- [Install ZRAM](#install-zram)
- [Install Zen Kernel](#install-zen-kernel)
- [Disable Bluetooth](#disable-bluetooth)
- [Customize GRUB (Background)](#customize-grub-background)
- [Install Powertop & auto-cpufreq](#install-powertop--auto-cpufreq)

---

## Remove TPM Slowdown on Boot

Disable TPM in the XPS 9560 BIOS under the **Security** tab.

---

## Install yay

Install it once as a prerequisite for all subsequent `yay -S` commands in this guide.
This command only works in Endeavor OS, as it ships with some extra repos that provide yay.

```bash
sudo pacman -S yay
```

---

## Disable NVIDIA Discrete GPU

> **Note:** Repeat this step after any fresh kernel installation.

```bash
yay -S envycontrol
sudo envycontrol -s integrated
```

---

## Install ZRAM

```bash
yay -S zram-generator
```

Create `/etc/sysctl.d/99-zram.conf`:

```ini
vm.swappiness = 100
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
vm.page-cluster = 0
```

Create `/etc/systemd/zram-generator.conf`:

```ini
[zram0]
zram-size = ram
compression-algorithm = zstd
```

Apply and start:

```bash
sudo systemctl daemon-reload
sudo systemctl start systemd-zram-setup@zram0.service
```

Verify:

```bash
zramctl
swapon --show
```

---

## Install Zen Kernel

```bash
sudo pacman -S linux-zen linux-zen-headers
sudo envycontrol -s integrated   # repeat — see Disable NVIDIA section
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## Disable Bluetooth

```bash
sudo systemctl disable bluetooth.service
```

---

## Customize GRUB (Background)

```bash
yay -S grub-customizer
```

---

## Install Powertop & auto-cpufreq

```bash
yay -S powertop
sudo powertop --calibrate
```

Test:

```bash
sudo powertop
```

```bash
yay -S auto-cpufreq
sudo auto-cpufreq --install
sudo systemctl enable --now auto-cpufreq
```

Test:

```bash
auto-cpufreq --stats
```