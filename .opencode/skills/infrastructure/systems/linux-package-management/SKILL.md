---
name: linux-package-management
description: Manage packages across Debian/Ubuntu, RHEL/Fedora, Arch, and Alpine: audit, install, remove, upgrade, and identify orphaned packages. Use when provisioning a new host, cleaning up disks, or auditing installed packages for security compliance.
---
# Linux Package Management

Manage packages across Debian/Ubuntu, RHEL/Fedora, Arch, Alpine.

## When to Use

- [done] Provisioning a new host
- [done] Cleaning up old kernels / orphaned packages (disk pressure)
- [done] Auditing installed packages for compliance (all are from trusted repos?)
- [done] Rolling back a broken upgrade

## Workflow

### Debian/Ubuntu

```bash
apt update && apt upgrade -y
apt autoremove --purge -y
apt list --upgradable
dpkg -l | grep -E "^rc" | awk '{print $2}'   # leftover configs
```

### RHEL/Fedora

```bash
dnf upgrade --refresh
dnf autoremove -y
dnf repoquery --extras                       # orphaned
rpm -qa | grep -i kernel                     # old kernels
```

### Arch

```bash
pacman -Syu
pacman -Rns $(pacman -Qdtq)                  # orphans
```

### Alpine

```bash
apk update && apk upgrade
apk audit                                  # inconsistencies
apk info -r                                # required-by check
```

## Audit

Validate every installed package comes from a signed repo / vendor. Flag: locally-installed .deb / .rpm not from a repo (hard to patch).

## Output

- List of installed packages + versions (artifact)
- List of orphaned packages + candidates for removal
- Local-only packages (audit)
