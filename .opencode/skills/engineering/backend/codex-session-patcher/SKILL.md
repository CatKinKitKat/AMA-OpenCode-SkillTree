---
name: codex-session-patcher
description: Codex/The agent/OpenCode session patcher review.
version: 1
author: ryfineZ + the agent
license: MIT
tags: [codex, ctf, session, patcher, the agent-code, opencode]
---


# Codex Session Patcher

Use this skill when the user asks about `codex-session-patcher`, Codex/The agent/OpenCode session cleanup, refusal replacement, or CTF profile/workspace prompt injection.

## Source
- Upstream: https://github.com/ryfineZ/codex-session-patcher
- Local source: `~/.agent/external-repos/codex-session-patcher`
- Reviewed commit: 9fbe665

## Safety
This tool can modify AI session stores and inject CTF prompts. Treat runtime use as HIGH-risk relative to local state integrity.

## Safe Use
1. Start with source review and dry-run mode.
2. Require explicit user approval before editing Codex, the coding agent, or OpenCode session/config paths.
3. Back up target session/config files before mutation.
4. Do not install with `pip install -e`, run Web UI, or execute `scripts/install.sh` unless the user explicitly asks for runtime setup.

## Verification
- Source cloned locally.
- README and Python package surfaces reviewed.
- No pip install, Web UI launch, session patch, profile injection, or config mutation performed during intake.
