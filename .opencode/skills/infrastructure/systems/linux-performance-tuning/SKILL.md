---
name: linux-performance-tuning
description: Tune Linux CPU, memory, disk, and network performance using sysctl, systemd resource controls, tuned profiles, and cgroups. Use when a host is under load, when I/O wait is high, or when normalizing performance across developer machines and CI.
---
# Linux Performance Tuning

Tune CPU, memory, disk, and network performance.

## When to Use

- [done] A host is under load (high CPU, memory, I/O, or network usage)
- [done] I/O wait > 20% sustained
- [done] Normalizing performance across dev machines and CI runners
- [done] Containers / cgroups not respecting resource limits

## Quick triage

| Symptom | Command | Likely cause |
|---------|---------|--------------|
| High CPU with low load avg | `pidstat 1` | single-threaded heavy process |
| High IOwait | `iostat -xz 1` | disk saturation, RAID rebuild |
| Memory pressure | `free -h`, `vmstat 1` | OOM killer activity, no swap |
| Network drops | `ss -s`, `netstat -s` | socket buffer exhaustion, connection backlog |

## sysctl tuning

```bash
# Network
sysctl -w net.core.somaxconn=4096
sysctl -w net.ipv4.tcp_syncookies=1
sysctl -w net.ipv4.tcp_fin_timeout=15

# Memory
sysctl -w vm.swappiness=10
sysctl -w vm.vfs_cache_pressure=50

# Disk
sysctl -w vm.dirty_ratio=10
sysctl -w vm.dirty_background_ratio=5
```

## systemd resource controls

```ini
# /etc/systemd/system/<service>.d/resources.conf
[Service]
CPUWeight=50
MemoryMax=2G
IOWeight=50
```

## Apply

Persist in `/etc/sysctl.d/99-tuning.conf` and reload:
```bash
sysctl --system
```

Do not tune without baseline measurement first.
