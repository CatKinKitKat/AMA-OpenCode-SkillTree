---
name: opencode
description: Delegate coding tasks to OpenCode CLI agent for feature implementation, refactoring, PR review, and long-running autonomous sessions. Requires the opencode CLI installed and authenticated.
tags:
  - coding
  - agent
  - opencode
version: 1
---

Goal
- Use OpenCode CLI as a coding subagent for implementation, refactor, review, and longer autonomous coding sessions.

Use when
- User explicitly wants OpenCode.
- Need an alternate coding agent from Codex/the coding agent.
- Long-running coding loops fit OpenCode CLI.

Prerequisites
- `opencode` CLI installed and authenticated.
- Prefer running inside a git repo.

Core workflow
1. Inspect repo state and scope.
2. Run OpenCode with a self-contained prompt.
3. Review produced diffs.
4. Run local verification.

Pitfalls
- Do not clobber unrelated changes.
- Pass exact files, failures, and constraints. The agent has no hidden context.
