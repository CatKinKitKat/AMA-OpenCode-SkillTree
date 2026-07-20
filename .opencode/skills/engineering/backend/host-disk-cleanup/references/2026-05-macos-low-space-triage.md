# macOS low-space triage notes (2026-05 session)

Context: user reported disk full on macOS. Data volume was effectively full. Safe cleanup reclaimed only a few GiB, so the remaining value came from identifying large candidate roots without deleting personal files.

Useful pattern:

1. Baseline `df` first, but expect available space to fluctuate while the system is under pressure.
2. If `du -xhd1 "$HOME"` times out, do not broaden or stall. Narrow immediately to known high-value roots:
   - `~/.codex`
   - `~/.agent`
   - `~/Library`
   - `~/Downloads`
   - `~/Library/Application Support`
   - `~/Library/Android`
   - `~/Library/Logs`
3. Search deleted-open files with `lsof +L1`. If none, proceed to live logs and cache roots.
4. For oversized logs, preserve a tail and truncate the active inode. In this session:
   - `~/Library/Logs/cliproxyapi-v7.stdout.log` was ~2.0G.
   - `~/.agent/logs/mcp-stderr.log` was ~132M.
5. Safe cleanup that did not touch personal files:
   - truncate oversized logs with tail archives
   - clear `~/.cache` and `~/Library/Caches`
   - run package cache cleaners if present: `uv cache prune`, `npm cache clean --force`, `python3 -m pip cache purge`, `go clean -cache -testcache`, `brew cleanup --prune=7`
6. After safe cleanup, report remaining large candidates rather than deleting them:
   - `~/Downloads/Tomac` (~9G)
   - `~/Downloads/repo-intake` (~4G)
   - `~/.codex/sessions` (~14G)
   - `~/.agent/state-snapshots` (~6.6G, but recent snapshots should be preserved unless user approves)
   - `~/Library/Application Support/Google` (~6.7G)
   - `~/Library/Android/sdk` (~5.3G)

Output style that worked: concise outcome -> current free space -> what was touched -> what was not touched -> largest remaining candidates -> one explicit next deletion candidate requiring user confirmation.
