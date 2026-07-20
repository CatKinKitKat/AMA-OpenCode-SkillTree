# Cross-agent output style normalization

Use when the user corrects global response format/style and expects the agent, Codex, The agent, and OpenClaw prompts to stay aligned.

## Trigger

User says they do not want a forced structure such as bracketed audit fields:

```text
[TARGET PARAMETER/ASSET]
[CURRENT CONTEXT]
[HYPOTHESIS]
[ACTIONABLE TELEMETRY / CODE]
[PARITY AUDIT]
[STATE TRANSITION]
```

## Durable rule

Do not encode rigid bracketed response templates in global `AGENTS.md` / `AGENTS.md` / workspace prompt files unless the user explicitly asks for that protocol.

Prefer:

```text
Output preference
Use concise natural replies. Do not force bracketed audit fields unless the user explicitly asks for that structured format.
```

## Files to check on this host

- the agent/project: `~/.agent/agent-runtime/AGENTS.md`
- Codex: `~/.codex/AGENTS.md`
- The agent: `~/.opencode/AGENTS.md`
- OpenClaw: `~/.openclaw/workspace/AGENTS.md`

## Verification pattern

Search those files for:

```text
Mandatory Output Protocol
TARGET PARAMETER/ASSET
CURRENT CONTEXT
ACTIONABLE TELEMETRY
```

Expected result: no active global prompt file contains the forced bracketed protocol. Historical cron/session output can contain old replies. Do not edit history just to remove old rendered messages.
