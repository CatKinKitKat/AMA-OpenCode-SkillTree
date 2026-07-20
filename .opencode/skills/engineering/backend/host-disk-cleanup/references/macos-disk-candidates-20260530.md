# macOS disk cleanup candidates from 2026-05-30 session

Durable lessons from a real host cleanup run.

## Codex local state

Two different Codex storage shapes appeared:

- Old shape: `~/.codex/log/codex-tui.log` can grow to 140-150 GiB. If active, preserve a tail and truncate the same inode.
- New shape: `~/.codex/logs_2.sqlite` can grow large (observed 13 GiB) with `logs_2.sqlite-wal` and many active `codex` processes holding it open. Do not treat this as a text log. Check with:

```bash
lsof "$HOME/.codex/logs_2.sqlite" "$HOME/.codex/logs_2.sqlite-wal" 2>/dev/null || true
sqlite3 "$HOME/.codex/logs_2.sqlite" 'PRAGMA page_count; PRAGMA page_size; PRAGMA wal_checkpoint(PASSIVE); PRAGMA freelist_count;' 2>/dev/null || true
```

If open by Codex, stop/exit Codex first before backup, VACUUM, or deletion. Direct truncation/deletion while active risks corrupting current state.

## the agent local state

- `~/.agent/state-snapshots/*-pre-update` can be multi-GiB. They are disposable only when user approves or they exceed retention. Recent snapshots may still be useful after upgrades.
- `~/.agent/state.db` may be large (observed 3.3 GiB). Do not delete as generic cleanup. Treat as a the agent state compaction task.
- `~/.agent/sessions` is reclaimable but loses cross-session search/history.

## Chrome / Google data

Do not delete `~/Library/Application Support/Google/Chrome/Default` or the whole Chrome profile when trying to free space, because it can contain login state, extensions, IndexedDB, Local Storage, and profile data.

Safer targets seen on this host:

```text
~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel
~/Library/Application Support/Google/Chrome/optimization_guide_model_store
~/Library/Application Support/Google/Chrome/component_crx_cache
~/Library/Application Support/Google/Chrome/extensions_crx_cache
~/Library/Application Support/Google/Chrome/Crashpad/completed
~/Library/Application Support/Google/GoogleUpdater/crx_cache
```

These are rebuildable model/component/update/crash caches.

## Other good candidates

- `~/Library/Android/sdk` if the user no longer needs Android builds/emulators. Otherwise it will need reinstall.
- `~/Library/Containers/com.docker.docker` if Docker Desktop is not in use. This includes Docker VM state.
- `~/Library/Group Containers/6N38VWS5BX.ru.keepcoder.Telegram` for Telegram local media/cache. Media may need redownload.
- `~/Library/Application Support/Steam` if Steam/games are not needed.
- `~/Downloads` project/data folders after explicit user approval.

## Scanning pattern

Full `$HOME` `du` or huge `find` scans can time out on this host. Prefer targeted roots discovered from prior results:

```bash
du -xhd1 "$HOME/Library/Application Support" 2>/dev/null | sort -h | tail -40
du -xhd1 "$HOME/Library/Containers" "$HOME/Library/Group Containers" "$HOME/Library/Logs" 2>/dev/null | sort -h | tail -50
du -xhd1 "$HOME/Downloads" "$HOME/.codex" "$HOME/.agent" 2>/dev/null | sort -h | tail -50
find "$HOME/Library/Application Support" "$HOME/Library/Containers" "$HOME/Library/Group Containers" "$HOME/Downloads" "$HOME/.codex" "$HOME/.agent" -type f -size +500M -print0 2>/dev/null | xargs -0 ls -lh 2>/dev/null | sort -k5 -h | tail -60
```
