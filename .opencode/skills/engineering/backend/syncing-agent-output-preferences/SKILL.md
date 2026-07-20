---
name: syncing-agent-output-preferences
description: Use when a user rejects an agent output format, system prompt rule, memory habit, or host-agent instruction and wants the agent, Codex, the coding agent, and OpenClaw behavior made consistent.
version: 1.0.0
---


# Syncing Agent Output Preferences

## Overview

When the user rejects an output contract, fix the durable instruction surfaces, not just the current reply. Check the agent memory plus host-agent docs for Codex, the coding agent, and OpenClaw.

## When to Use

Use when the user says:
- "不要这种格式", "别再用 []", "修系统提示词和记忆"
- Codex/The agent/OpenClaw/the agent output differs
- a style preference should persist across agent hosts

Do not use for one-off formatting requests unless the user asks to remember or unify it.

## Workflow

1. Load `autonomous-ai-agents/agent-runtime` before the agent config/prompt work.
2. If routing/skills are involved, load `software-development/skill-routing-gov`.
3. Find active prompt surfaces first:
   - the agent repo/current project: nearest `AGENTS.md` / `AGENTS.md`
   - Codex: `~/.codex/AGENTS.md`
   - the coding agent: `~/.opencode/AGENTS.md`
   - OpenClaw: `~/.openclaw/workspace/AGENTS.md`
4. Search only targeted config/workspace roots first. Avoid broad home-directory scans unless needed.
5. Remove or rewrite the offending rule in every active surface where it exists.
6. Save a compact user memory only if the preference is durable.
7. Verify by re-reading the edited section and searching the active host roots for the rejected phrase.
8. Report which hosts were changed or already clean.

## Known Host Files

- the agent current project: `AGENTS.md` in the active repo or project.
- Codex global: `~/.codex/AGENTS.md`.
- the coding agent global: `~/.opencode/AGENTS.md`.
- OpenClaw workspace: `~/.openclaw/workspace/AGENTS.md`.

## References

- `references/bracketed-audit-output-cleanup.md` records the concrete cleanup pattern for rejected bracketed audit fields across the agent, Codex, the coding agent, and OpenClaw.

## Verification Commands

```bash
rg -n "Mandatory Output Protocol|TARGET PARAMETER/ASSET|CURRENT CONTEXT|ACTIONABLE TELEMETRY" \
  ~/.codex ~/.the agent ~/.openclaw/workspace ~/.agent/agent-runtime -g '*.md'
```

Expected result after removing the bracketed audit format: no matches in active host prompt files.

## Pitfalls

- Do not treat the agent memory as the only source. Host agents read their own prompt docs.
- Do not claim Codex/The agent/OpenClaw are fixed without checking their actual files.
- Do not scan all of `~/Library` for prompt text. MacOS protected paths create noise and timeouts.
- Do not add a new rigid output schema while removing another one.
