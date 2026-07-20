---
name: mmpl-exte-memo-setu
description: >
tags: 
version: 1
---


Goal
- Stand up MemPalace as an isolated local external memory layer.
- Avoid polluting the main Python environment.
- Verify with a tiny corpus before wiring MCP.

Why this skill exists
- the agent built-in memory is intentionally small and should only hold compact durable preferences/facts.
- Project-specific workflow state belongs in project docs/skills/session recall, not long-term memory.
- MemPalace is a better fit for searchable verbatim external memory, but setup has practical pitfalls.

Recommended approach
1. Clone into a separate workspace.
2. Create a dedicated venv.
3. Install MemPalace inside that venv.
4. Run a tiny trial corpus first.
5. Only after search works, use the MCP server from the same venv.

Verified paths from a working setup
- Repo: `~/Downloads/external-memory/mempalace`
- Venv: `~/Downloads/external-memory/mempalace-venv`
- Trial notes dir: `~/Downloads/external-memory/mempalace-trial/notes`
- Verification log: `~/Downloads/external-memory/mempalace-verified.txt`

Install
```bash
python3 -m venv ~/Downloads/external-memory/mempalace-venv
~/Downloads/external-memory/mempalace-venv/bin/python -m pip install --upgrade pip setuptools wheel
~/Downloads/external-memory/mempalace-venv/bin/python -m pip install --default-timeout=120 ~/Downloads/external-memory/mempalace
```

Minimal verification flow
```bash
VENV=~/Downloads/external-memory/mempalace-venv/bin
$VENV/mempalace init --yes ~/Downloads/external-memory/mempalace-trial/notes
$VENV/mempalace mine ~/Downloads/external-memory/mempalace-trial/notes
$VENV/mempalace search "PostgreSQL auth concurrent writes"
$VENV/mempalace status
```

Expected verification outcome
- `mine` should file drawers successfully.
- `search` should return the expected matching note first.
- `status` should show non-zero drawers.

MCP hookup
```bash
~/Downloads/external-memory/mempalace-venv/bin/python -m mempalace.mcp_server
```

Common pitfalls
- Do not install into the main environment if you care about dependency stability.
  - In one real setup, non-isolated install upgraded `protobuf` and conflicted with `streamlit`.
- `mempalace init` is interactive by default.
  - Use `--yes` for non-interactive automation.
- First `mine` may appear stalled because Chroma downloads the local ONNX embedding model.
  - Wait for `~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz` to finish.
  - This can be slow and dominate setup time.
- Telemetry warnings like `capture() takes 1 positional argument but 3 were given` may appear.
  - Treat as noisy but non-blocking if indexing/search still work.
- Default palace path used by CLI is typically `~/.mempalace/palace`.

Decision rule
- Use the agent built-in memory for compact long-term preferences.
- Use project docs/skills/session_search for project workflow guidance.
- Use MemPalace for large searchable verbatim external memory.
