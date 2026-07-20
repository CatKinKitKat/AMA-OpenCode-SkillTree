---
name: terminal-graphics-setup
description: Fix broken terminal graphics on Linux: Xorg/Wayland session recovery, NVIDIA/AMD/Intel driver issues, font rendering, and monitor EDID problems. Use when the display is corrupted, resolution is wrong, or after a driver update left the desktop unusable.
---
# Terminal Graphics Setup

Fix broken Linux display/graphics sessions.

## When to Use

- [done] Display is corrupted after driver update
- [done] Resolution is wrong or monitor not detected
- [done] NVIDIA/AMD/Intel driver issues (blank screen, tearing, flicker)
- [done] Font rendering suddenly degraded or missing

## Workflow

### Collect evidence

```bash
journalctl /usr/bin/gnome-shell --since "10 minutes ago"
journalctl /usr/bin/Xorg --since "10 minutes ago"
cat ~/.local/share/xorg/Xorg.0.log | grep "(EE)"
xrandr --query
```

### NVIDIA

```bash
nvidia-smi
nvidia-settings
# reinstall if DKMS broke:
sudo dkms autoinstall && sudo modprobe nvidia
```

### AMD / Intel

```bash
sudo dmesg | grep -iE "amdgpu|radeon|i915"
sudo modprobe amdgpu  # or i915
```

## EDID / resolution

```bash
xrandr --newmode "1920x1080_60.00" ...
xrandr --addmode HDMI-1 "1920x1080_60.00"
xrandr --output HDMI-1 --mode "1920x1080_60.00"
```

## Fonts

Use system fonts (Noto Sans, Inter). Verify:
```bash
fc-match sans
fc-match monospace
```

## Output

- Evidence: `graphics-<date>.log`
- Fix applied: config path and value changed
- Rollback command provided
