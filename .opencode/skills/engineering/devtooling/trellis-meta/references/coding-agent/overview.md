# the coding agent Features Overview

These features require **the coding agent** and don't work on Cursor or other platforms.

---

## Why the coding agent Only?

the coding agent provides unique capabilities:

| Feature | the coding agent | Why Required |
|---------|-------------|--------------|
| Hooks | ✅ | Hook system for lifecycle events |
| Task tool | ✅ | Subagent invocation with context |
| `--agent` flag | ✅ | Load agent definitions |
| `--resume` | ✅ | Session persistence |
| CLI scripting | ✅ | Automation with `the agent` command |

---

## Feature Categories

### Hooks System
Automatic context injection and quality enforcement.

| Hook | When | Purpose |
|------|------|---------|
| `SessionStart` | Session begins | Inject workflow context |
| `PreToolUse:Task` | Before subagent | Inject specs via JSONL |
| `SubagentStop:check` | Check agent stops | Ralph Loop enforcement |

→ See [hooks.md](./hooks.md)

### Agent System
Specialized agents for different development phases.

| Agent | Purpose |
|-------|---------|
| `dispatch` | Orchestrate pipeline |
| `implement` | Write code |
| `check` | Review and self-fix |
| `debug` | Fix issues |
| `research` | Find patterns |
| `plan` | Evaluate requirements |

→ See [agents.md](./agents.md)

### Ralph Loop
Quality enforcement for Check Agent.

- Runs verify commands when Check Agent stops
- Blocks completion until all pass
- Max 5 iterations, 30min timeout

→ See [ralph-loop.md](./ralph-loop.md)

### Multi-Session
Parallel isolated sessions using Git worktrees.

- Each session in separate worktree
- Own branch, own The agent process
- Automated PR creation

→ See [multi-session.md](./multi-session.md)

### worktree.yaml
Configuration for Multi-Session and Ralph Loop.

→ See [worktree-config.md](./worktree-config.md)

---

## Documents in This Directory

| Document | Content |
|----------|---------|
| `hooks.md` | Hook system, context injection |
| `agents.md` | Agent types, invocation, context |
| `ralph-loop.md` | Quality enforcement mechanism |
| `multi-session.md` | Parallel worktree sessions |
| `worktree-config.md` | worktree.yaml configuration |
| `scripts.md` | the coding agent only scripts |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      CODING AGENT INTEGRATION                             │
│                                                                          │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐        │
│  │  SessionStart  │    │  PreToolUse    │    │  SubagentStop  │        │
│  │     Hook       │    │     Hook       │    │     Hook       │        │
│  └───────┬────────┘    └───────┬────────┘    └───────┬────────┘        │
│          │                     │                     │                  │
│          ▼                     ▼                     ▼                  │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐        │
│  │ session-start  │    │ inject-context │    │  ralph-loop    │        │
│  │     .py        │    │     .py        │    │     .py        │        │
│  └───────┬────────┘    └───────┬────────┘    └───────┬────────┘        │
│          │                     │                     │                  │
│          ▼                     ▼                     ▼                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     CORE SYSTEMS (File-Based)                    │   │
│  │  Workspace  │  Tasks  │  Specs  │  Commands  │  Scripts          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Checking the coding agent Availability

```bash
# Check if the coding agent is installed
the agent --version

# Verify hooks are configured
cat .opencode/settings.json | grep -A 5 '"hooks"'
```

If hooks aren't present, the coding agent features won't work.
