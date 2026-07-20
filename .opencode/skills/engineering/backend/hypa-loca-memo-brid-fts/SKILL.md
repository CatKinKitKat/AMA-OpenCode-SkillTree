---
name: hypa-loca-memo-brid-fts
description: >
tags: 
version: 1
---


Goal
- Stand up a minimal reusable local bridge from agent workflows into Hypatia.
- Detect and fix the common failure mode where writes succeed but `search` returns nothing.

When to use
- You have Hypatia source locally and want practical reuse, not just repo study.
- You want a safe sidecar memory layer before integrating into a main agent system.
- `knowledge-create` or direct writes succeed, but `search` returns `No results found.`

Recommended approach
1. Build Hypatia first.
   - Repo example: `~/Downloads/repo-intake/hypatia`
   - Run: `cargo build --release`
2. Create a thin wrapper script instead of editing the main agent first.
   - Good first commands:
     - `add-note`
     - `search`
     - `get-note`
   - Call the Hypatia binary via subprocess, parse stdout JSON where applicable, and emit stable JSON for the caller.
3. Verify the whole path end to end.
   - Create a note.
   - Read it back with `knowledge-get`.
   - Search for words from name, data, and tags.
4. If read works but search fails, inspect SQLite directly before guessing.
   - Check `~/.hypatia/default/index.sqlite`.
   - Compare counts in `docs_meta` vs `docs_fts`.
   - Inspect recent rows in both tables.
5. If `docs_meta` has rows and `docs_fts` exists but MATCH finds nothing, patch Hypatia schema init to rebuild the FTS index.
6. Rebuild Hypatia and rerun the end-to-end verification.

Bridge template
- Implement a small Python wrapper with:
  - configurable binary path via `HYPATIA_BIN`
  - configurable default shelf via `AGENT_HYPATIA_SHELF`
  - commands for `add-note`, `search`, `get-note`
- Prefer a sidecar workspace such as:
  - `~/Downloads/agent-hacks/agent-hypatia-bridge/`

Key debugging pattern
1. Write test note:
   - `hypatia knowledge-create "the agent bridge test" --data "Hypatia bridge working" --tags agent,memory,bridge --shelf default`
2. Confirm retrieval works:
   - `hypatia knowledge-get "the agent bridge test" --shelf default`
3. If search fails:
   - `hypatia search bridge --limit 10 --shelf default`
   - Inspect SQLite table contents directly.
4. Use Python `sqlite3` for direct inspection when needed:
   - count `docs_meta`
   - count `docs_fts`
   - inspect `key`, `fts_key`, `fts_data`, `fts_tags`
   - run `MATCH` queries directly

Actual fix
- File: `src/storage/sqlite_store.rs`
- In `SqliteStore::init_schema()`, after recreating the triggers, run:

```rust
self.conn
    .execute_batch("INSERT INTO docs_fts(docs_fts) VALUES('rebuild');")
    .map_err(StorageError::from)?;
```

Why this matters
- Hypatia recreates the FTS virtual table in schema init.
- Recreating the FTS table alone does not repopulate it from `docs_meta`.
- Result: writes may exist in `docs_meta`, but `docs_fts MATCH ...` returns no rows.
- The `rebuild` command repopulates the FTS index from the content table.

Verification checklist
- `cargo build --release` succeeds.
- `knowledge-create` succeeds.
- `knowledge-get` returns the inserted object.
- `search` finds terms from title/data/tags.
- Direct SQLite MATCH query also returns rows.

Pitfalls
- Do not assume write failure just because search is empty.
- Do not trust only the CLI search path. Inspect the SQLite backing store directly.
- Do not integrate deeply into the agent first. Prove the sidecar bridge works end to end.
- If a repo claims FTS works, still verify after schema migrations or virtual table recreation.
