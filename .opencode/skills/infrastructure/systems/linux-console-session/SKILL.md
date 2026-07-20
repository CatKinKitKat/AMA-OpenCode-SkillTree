---
name: linux-console-session
description: Recover broken tmux / screen sessions after SSH disconnects, detach stuck sessions, and keep long-running processes alive. Use when a background build, stream, or remote shell dies after a network disconnect.
---
# Linux Console Session

Recover and manage tmux / screen sessions after SSH disconnects.

## When to Use

- [done] Network disconnect killed an SSH session with a running build or stream
- [done] A teammate shares a tmux/screen session for pair programming
- [done] A background process needs to outlive SSH detach

## tmux

```bash
tmux ls                                      # list sessions
tmux attach -t <name>                        # attach
tmux attach -d -t <name>                     # force-detach and attach
tmux kill-session -t <name>                  # kill
```

## screen

```bash
screen -ls
screen -r <pid>
screen -D -r <pid>      # force detach first
```

## nohup / disown

```bash
nohup ./long-job.sh > out.log 2>&1 &
disown %1                     # detach from shell
```

## Best practices

- Prefer tmux over screen for multi-pane support
- Use `tmux -CC` for terminal-plus-GUI
- Link `tmux.conf` from dotfiles repo for consistency

## Systemd long-running jobs

```bash
systemd-run --unit=my-build --scope ./build.sh
journalctl -u my-build -f
systemctl status my-build
```

## nohup alternatives

| Tool | Feature |
|------|---------|
| tmux | Resumable, multi-pane, clipboard |
| screen | Legacy, universally installed |
| nohup + disown | Simple, single process |
| systemd-run | Service unit, journal logging, automatic restart |

Prefer tmux for dev workflows. Systemd-run for production services.
