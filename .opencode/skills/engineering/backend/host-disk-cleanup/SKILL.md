---
name: host-disk-cleanup
description: Use when the local machine is out of disk space or the user asks to delete unused, untagged, old, cache, log, snapshot, Codex, or the agent local state without touching important personal files.
version: 1.0.0
author: the agent
license: MIT
metadata: 
tags: [disk, cleanup, macos, cache, logs, codex, agent]
related_skills: [keep-codex-fast, agent-runtime, skill-routing-gov]
---


# Host Disk Cleanup

## Overview

Use this for emergency local disk cleanup on the user's machine. The core rule is: inspect first, reclaim obvious rebuildable or disposable data, preserve continuity, and never delete personal/project artifacts just because they are old.

The concrete macOS pattern learned on this host: a single active Codex log (`~/.codex/log/codex-tui.log`) can grow past 150 GiB while many Codex processes keep it open. The right response is not broad deletion. Preserve a tail, truncate the active log, then verify free space.

## When to Use

Use when the user says any of:
- 本地空间不足
- 磁盘满了
- 空间不够
- 清理空间
- 清理本地垃圾
- 把不用的删掉
- 删一周内不用的
- 删没标签的
- 清理未打标签文件
- Codex 日志太大
- the agent state snapshots 太大
- macOS 缓存太大

Do not use for:
- deciding which personal documents, books, screenshots, or Downloads to delete without a candidate list
- deleting repos, worktrees, session history, memories, skills, plugins, cron jobs, auth, or credentials
- destructive cleanup without a manifest and before/after verification

## Safety Contract

1. Baseline first:
   - `df -h / /System/Volumes/Data 2>/dev/null || df -h /`
   - `du -xhd1 "$HOME" 2>/dev/null | sort -h | tail -30`
2. Treat Finder tags as keep signals. Before deleting user-facing files, check `com.apple.metadata:_kMDItemUserTags`.
3. Default safe deletion scope:
   - rebuildable caches: `~/.cache`, `~/Library/Caches`, package-manager caches
   - temp folders explicitly named temp/tmp
   - old the agent pre-update snapshots or legacy checkpoints beyond retention
   - oversized logs, but truncate with tail preservation rather than blind delete
4. Default protected scope:
   - `~/Downloads`, `~/Documents`, `~/Desktop`, repo roots, credentials, session transcripts, memories, skills, plugins, cron state
5. For active logs opened by a running process, use `lsof` first and preserve a tail before truncation.
6. Write a cleanup manifest under `~/.agent/logs/` with removed paths, byte counts, skipped tagged paths, command outputs, and errors.
7. Verify after cleanup with `df` and targeted `du`.

## Triage Commands

## Session References

- `references/macos-disk-candidates-20260530.md` records observed Codex SQLite log behavior, Chrome model-cache targets, the agent state caveats, and targeted macOS scan commands from a real cleanup run.

## Triage Commands

```bash
# Filesystem pressure
df -h / /System/Volumes/Data 2>/dev/null || df -h /

# Largest top-level roots under home
du -xhd1 "$HOME" 2>/dev/null | sort -h | tail -30

# Common local-state roots
du -xhd1 "$HOME"/.codex "$HOME"/.agent "$HOME"/.cache "$HOME"/Library 2>/dev/null | sort -h | tail -50

# Largest files in a suspect root
python3 - <<'PY'
import os, time, heapq
root=os.path.expanduser('~/.codex/log')
heap=[]
for dp, dns, fns in os.walk(root):
    for fn in fns:
        p=os.path.join(dp,fn)
        try: st=os.stat(p)
        except OSError: continue
        item=(st.st_size,p,st.st_mtime)
        if len(heap)<30: heapq.heappush(heap,item)
        else: heapq.heappushpop(heap,item)
for size,p,mt in sorted(heap, reverse=True):
    print(f'{size/1024/1024/1024:8.2f}G {((time.time()-mt)/86400):6.1f}d {p}')
PY

# Who is writing an oversized log
lsof "$HOME/.codex/log/codex-tui.log" 2>/dev/null | head -20
```

## Safe Active Log Truncation

Use this pattern when a log is huge and active. It keeps the last bytes for evidence and truncates the same inode so open writers continue safely.

```bash
python3 - <<'PY'
from pathlib import Path
import time
path = Path.home()/'.codex/log/codex-tui.log'
keep_bytes = 20 * 1024 * 1024
archive_dir = Path.home()/'.codex/archived_logs'
archive_dir.mkdir(parents=True, exist_ok=True)
stamp = time.strftime('%Y%m%d-%H%M%S')
tail_path = archive_dir / f'{path.name}.{stamp}.tail'
size = path.stat().st_size
with open(path, 'rb') as f:
    f.seek(max(0, size - keep_bytes))
    data = f.read()
with open(tail_path, 'wb') as out:
    out.write(data)
with open(path, 'r+b') as f:
    f.truncate(0)
print(f'truncated={path} old_bytes={size} kept_tail={tail_path} kept_bytes={len(data)}')
PY
```

Also check the agent MCP stderr when the agent logs are large:

```bash
lsof "$HOME/.agent/logs/mcp-stderr.log" 2>/dev/null | head -20
```

Apply the same preserve-tail-and-truncate pattern, with `keep_bytes = 5 * 1024 * 1024` and archive dir `~/.agent/logs/archived`.

## Older-than-7-Days Untagged Cleanup

For this user's phrasing, "一周内不用" means candidates older than 7 days. Do not apply it to all of `$HOME`. Apply only to safe classes unless the user explicitly approves a candidate list for personal files.

Safe classes:
- `~/.cache/*` older than 7 days and untagged
- `~/Library/Caches/*` older than 7 days and untagged
- `~/tmp/*` older than 7 days and untagged
- `~/.agent/state-snapshots/YYYYMMDD-*-pre-update` older than 7 days and untagged
- `~/.agent/checkpoints/legacy-*` older than 7 days and untagged

Do not automatically delete old files under `~/Downloads`. Produce a list first.

Finder tag check:

```python
import os

def has_finder_tags(path: str) -> bool:
    try:
        return bool(os.getxattr(path, 'com.apple.metadata:_kMDItemUserTags'))
    except OSError:
        return False
```

## Package Cache Cleaners

Run after targeted triage, not before the baseline:

```bash
uv cache prune --no-progress
npm cache clean --force
python3 -m pip cache purge
go clean -cache -testcache
brew cleanup --prune=7
```

Ignore unavailable tools. Record output in the manifest.

## Manifest Requirements

Write JSON to:

```text
~/.agent/logs/disk-cleanup-YYYYMMDD-HHMMSS.json
```

Include:
- start and finish timestamp
- before and after `df`
- every removed path and byte count
- every truncated log, old size, tail path, kept bytes
- every skipped path due to Finder tags
- every package-clean command exit code and output tail
- errors such as macOS Trash permission denial

## Verification Checklist

- [ ] `df` shows meaningful reclaimed space.
- [ ] Largest suspected log no longer dominates disk usage.
- [ ] Tail archive exists for truncated logs.
- [ ] Recent the agent state snapshots remain if they are within retention.
- [ ] `Downloads`, repos, documents, skills, memories, sessions, auth, and cron state were not broadly deleted.
- [ ] Manifest path is reported to the user.

## Common Pitfalls

1. Broadly applying "older than 7 days" to the whole home directory. This can delete books, screenshots, datasets, and project artifacts. Restrict to safe classes first.
2. Deleting an open log file instead of truncating it. On Unix, deleting an open file may not reclaim space until the writer exits. Truncate the active inode after preserving a tail.
3. Trusting source paths over live disk usage. Always use `du` and `lsof` on the live machine.
4. Treating all `.agent` state as disposable. Preserve sessions, auth, skills, plugins, cron jobs, and recent snapshots.
5. Failing silently on macOS protected folders such as `.Trash`. Record permission errors. Do not force privileged deletion unless explicitly approved.
