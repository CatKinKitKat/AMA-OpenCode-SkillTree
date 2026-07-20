---
name: linux-color-management
description: Install and verify ICC display profiles, calibrate monitors, and set up color-managed environments for web (sRGB) and creative work (Display P3 / Adobe RGB). Use when colors are wrong on a monitor, after a hardware change, or when shipping creative work.
---
# Linux Color Management

Install ICC profiles and verify display color accuracy.

## When to Use

- [done] Colors are visibly wrong on a monitor
- [done] After a hardware change (new monitor, GPU)
- [done] Shipping creative work (photo/video) to clients
- [done] Setting up a color-managed workspace (sRGB or Display P3)

## Workflow

### Profile

```bash
# GNOME Color (default)
colormgr get-devices
colormgr get-profile <device-id>
colormgr add-profile <device-id> <.icc file>

# Verify
colormgr get-profile <device-id>
```

### Monitor profile

- Use hardware calibrator (X-Rite i1Display, Datacolor SpyderX)
- Export ICC profile to `~/.local/share/icc/`
- Assign via GNOME color picker

### sRGB targets

Default target for web UIs and most code:
- Monitor: sRGB native
- OS: sRGB ICC profile assigned
- Browser: `color-srgb` CSS (default)

### Display P3 targets

For wide-gamut displays / creative work:
- Monitor: Display P3 capable (DCI-P3)
- OS: Display P3 ICC assigned
- Browser: `color-gamut:p3` media query, CSS `color(display-p3 ...)` syntax

## Verify

Reference color-scheme websites:
- https://www.photoshop.com/en/colorchecker
- https://projects.lukehaas.me/checkerboard

## Output

- Profile assigned: device ID + ICC path
- Verification: color-scheme output (e.g. "PASS: no banding, neutral grays")
