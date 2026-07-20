# Bracketed audit output cleanup pattern

Session signal: user rejected forced bracketed audit fields such as `[TARGET PARAMETER/ASSET]`, `[CURRENT CONTEXT]`, `[HYPOTHESIS]`, `[ACTIONABLE TELEMETRY / CODE]`, `[PARITY AUDIT]`, and `[STATE TRANSITION]`.

Durable lesson:
- Treat style/format rejection as both memory and skill signal.
- Fix active prompt surfaces, not only the current reply.
- Check host-specific instruction files for the agent, Codex, the coding agent, and OpenClaw.
- Prefer concise natural replies unless the user explicitly asks for a rigid schema.

Observed active surfaces:
- the agent current project: `AGENTS.md` in active repo.
- Codex global: `~/.codex/AGENTS.md`.
- the coding agent global: `~/.opencode/AGENTS.md`.
- OpenClaw workspace: `~/.openclaw/workspace/AGENTS.md`.

Verification regex:
```bash
rg -n "Mandatory Output Protocol|TARGET PARAMETER/ASSET|CURRENT CONTEXT|ACTIONABLE TELEMETRY" \
  ~/.codex ~/.the agent ~/.openclaw/workspace ~/.agent/agent-runtime -g '*.md'
```

Expected clean state: no matches in active host prompt files.

Pitfall:
- Do not run broad home-directory scans first. MacOS protected `~/Library` paths create permission noise and timeouts. Start with the known host roots above.
