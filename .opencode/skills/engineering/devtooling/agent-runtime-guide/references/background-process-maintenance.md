# Background process maintenance in the agent sessions

Session pattern: a Python background job was started with `terminal(..., background=true)`. `process poll` showed the bash wrapper alive but no output. The real Python child was sleeping and stdout visibility was poor.

Useful checks:

```bash
ps -p <wrapper-pid> -o pid,ppid,stat,etime,command
pgrep -P <wrapper-pid> -a || true
ps -axo pid,ppid,stat,etime,command | grep '<script-name>' | grep -v grep
lsof -Pan -p <child-pid> -iTCP
sample <child-pid> 3 1 | sed -n '1,80p'   # macOS: confirms sleep vs network hang vs CPU loop
```

Observed interpretation:
- wrapper process may be `/bin/bash -lic set +m; python3 ...`
- child Python process holds the actual state
- `status=running` plus no TCP sockets and `sample` showing `time_sleep/__select` means the script is idle/sleeping, not hung
- empty `process log` can happen even when the child is healthy

Hardening pattern for long-running helper scripts:
- run with `python3 -u` for unbuffered stdout
- add explicit file logging under `~/.agent/logs/<job>.log`
- write a line before every long sleep, every request, and every state transition
- after restart, verify both process status and log file creation

Example log helper:

```python
LOG_PATH = "~/.agent/logs/job.log"

def log(*parts):
    line = " ".join(str(part) for part in (time.strftime("%Y-%m-%d %H:%M:%S"), *parts))
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
```

Safe maintenance loop:
1. Poll the the agent process session.
2. Identify wrapper and child PIDs.
3. Inspect child with `ps`, `lsof`, and `sample`.
4. If observability is missing, kill old process, patch logging, syntax-check, restart with `python3 -u`.
5. Verify log file contains an immediate startup line.
