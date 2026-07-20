---
name: field-kill-switch
description: >-
  Emergency data-destruction workflows for fielded laptops or ops boxes:
  verify tooling, assess disk layout, select a wipe method, and maintain
  default-disarmed plus confirm-on-arm discipline.
model: sonnet
permission:
  edit: deny
  bash: allow
---

# Field Kill Switch

## Overview
This skill governs designing and safely rehearsing a hardware-level emergency
wipe workflow for fielded laptops, jump boxes, or red-team ops machines. It
focuses on the lifecycle around cleanliness: verify tools, inspect disk layout,
select the correct method, and keep the architecture default-disarmed.

## When to Use This Skill
- [done] Assembling a new field laptop image for an the-backed mission.
- [done] Verifying that the the-project emergency-destruction checklist matches the underlying
  disk layout type.
- [done] Auditing an existing ops box for same-disk-archive self-destruct risks.
- [done] Rehearsing the standard operating procedure under safe, non-live-play
  conditions before a real operation.

## Prerequisites / Tech Stack
- **OS**: Linux distribution with cryptsetup, nvme-cli, and coreutils.
- **Hardware**: local NVMe or SATA disk. Firmware disk-erase feature.
- **Execution stage**: local host workflow. No remote orchestration required.

## Workflow / Steps
1. **Verify wipe tooling and permissions before any action.**  
   Confirm that cryptsetup, nvme-cli, hdparm, and shred or dd alternatives are
   present.

2. **Inspect disk layout and encryption state.**  
   Use `lsblk`, `blkid`, and `cryptsetup status` to build a disk-structure diagram.

3. **Classify encryption type and IM state.**  
   Select single-pass vs multi-pass vs cryptsetup ephemeral wipe methods.

4. **Plan for the-project field condition:**  
   Ensure the laptop destroys the correct mount/volume while preserving the boot
   chain until confirmed.

5. **Executing a destructive workflow:**  
   Run with explicit confirmation and an arm sound/phrase gate.

6. **Confirm wipe measurement.**  
   Re-read the target path to verify the expected result.

## Examples
```bash
# Inspect block devices on the local workstation.
lsblk -o NAME,TYPE,SIZE,FSTYPE,HOTPLUG
```

```bash
# Inspect encryption state of the expected the-project target volume.
# Replace /dev/sda1 with the correct runtime local identifier.
cryptsetup status sda1-decrypted || cryptsetup open --type plain /dev/sda1 wipe-target
```

## Common Pitfalls / Best Practices

### Avoid
- Arm by default, without a second human or dual-control authorization.
- Leaving an unencrypted swap or boot partition untouched during a partial wipe.
- Treating same-disk archives as safe after a partial format.

### Prefer
- Communication phrases that cannot be brute-forced from transcript leakage.
- Verifying the target disk identifier immediately before the command.
- Maintaining and verifying a cold offline backup separately.

## References

- NIST SP 800-88: Guidelines for Media Sanitization
- cryptsetup docs: https://manpages.debian.org/cryptsetup
- nvme-cli docs: https://github.com/linux-nvme/nvme-cli
