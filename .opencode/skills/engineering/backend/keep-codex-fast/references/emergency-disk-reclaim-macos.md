# Emergency disk reclaim on macOS

Use this reference when the host is nearly full and Codex/the agent state is a major contributor.

Session-proven pattern:

1. Baseline first:
   - `df -h / /System/Volumes/Data 2>/dev/null || df -h /`
   - `du -xhd1 "$HOME" 2>/dev/null | sort -h | tail -30`
   - `du -xhd1 "$HOME"/.codex "$HOME"/.agent "$HOME"/.cache 2>/dev/null | sort -h | tail -40`
2. If `~/.codex/log/codex-tui.log` is huge and actively open, do not delete the file while writers hold it open. Keep a small tail copy, then truncate in place:
   - archive dir: `~/.codex/archived_logs/`
   - keep tail: 20 MiB is enough for diagnostics in most emergency cleanups
   - truncate with Python `open(path, "r+b").truncate(0)` so disk blocks are released even while the process may reopen/use the same path
3. Check active writers before/after:
   - `pgrep -afil 'codex|Codex' || true`
   - `lsof "$HOME/.codex/log/codex-tui.log" 2>/dev/null | head -20`
4. For the agent state, prefer age-bounded deletion of pre-update snapshots/checkpoints, not broad deletion of sessions/skills/memory:
   - safe candidate class: `~/.agent/state-snapshots/YYYYMMDD-*-pre-update` older than 7 days and without Finder tags
   - safe candidate class: `~/.agent/checkpoints/legacy-*` older than 7 days and without Finder tags
   - keep recent snapshots unless the user explicitly asks for deeper cleanup
5. Respect Finder tags. Before removing user-visible or ambiguous paths, check `com.apple.metadata:_kMDItemUserTags`. Skip tagged items.
6. Avoid personal data by default:
   - do not delete `Downloads`, repos, documents, sessions, memories, skills, plugins, automations, or credential files unless explicitly requested and scoped
   - for `Downloads`, produce a candidate list first unless the user explicitly approves deletion criteria
7. Rebuildable cache cleaners that are usually safe after inspection:
   - `uv cache prune --no-progress`
   - `npm cache clean --force`
   - `python3 -m pip cache purge`
   - `go clean -cache -testcache`
   - `brew cleanup --prune=7`
8. Write a local manifest under `~/.agent/logs/disk-cleanup-YYYYMMDD-HHMMSS.json` with paths, byte counts, reasons, and command output tails.
9. Verify with `df` and targeted `du` after cleanup.

Key pitfall:
- A single active log can dominate disk usage. In one run, `~/.codex/log/codex-tui.log` was 152G while the host had only 138MiB free. Tail-preserving in-place truncation recovered space immediately and safely preserved diagnostic context.