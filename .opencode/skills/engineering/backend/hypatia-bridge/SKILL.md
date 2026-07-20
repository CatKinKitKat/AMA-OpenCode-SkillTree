---
name: hypatia-bridge
description: >
tags: 
version: 1
---


# Hypatia Bridge

## Purpose

Use local Hypatia as a sidecar memory layer for the agent.

## When to use

- Need durable local notes beyond built-in memory limits
- Need searchable external memory
- Need subject/predicate/object graph facts
- Need a local fallback when hosted memory is not enough

## Assets

Workspace:
- `~/Downloads/agent-hacks/agent-hypatia-bridge/`

Primary CLI:
- `python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py`

Default Hypatia binary:
- `~/Downloads/repo-intake/hypatia/target/release/hypatia`

## Linked reference

- `references/usage.md`

## Commands

### Add note
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py add-note "Name" "Body" --tags a,b
```

### Search
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py search "query"
```

### Get note
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py get-note "Name"
```

### Add statement
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py add-statement the agent uses Hypatia --data "external memory backend"
```

### Query triple
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py query-triple the agent uses Hypatia
```

### Raw JSE query
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_hypatia.py query '["$knowledge", ["$search", "persona"]]'
```

### Selective the agent sync
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_memory_sync.py add-memory user persona "Default terse Wenyan mode"
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_memory_sync.py add-fact the agent uses Hypatia --data "external memory backend"
```

### Semi-auto wrapper
```bash
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py memory user persona "Default terse Wenyan mode"
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py fact the agent uses Hypatia --data "external memory backend"
python3 ~/Downloads/agent-hacks/agent-hypatia-bridge/agent_auto_sync.py memory memory long_term_rule "Prefer direct execution" --sync no
```

## Environment

- `HYPATIA_BIN`
- `AGENT_HYPATIA_SHELF`

## Pitfalls

- If search returns empty after writes, verify Hypatia binary is rebuilt with FTS rebuild fix in `src/storage/sqlite_store.rs`.
- Keep built-in the agent memory for compact user prefs. Use Hypatia for larger external recall.
