---
name: the agent-code-harness
description: Plan-work-review harness for the coding agent.
version: 1
author: Chachamaru127 + the agent
license: MIT
tags: [the agent-code, harness, planning, review, workflow]
---


# the coding agent Harness

Use this skill when a task mentions the coding agent Harness, harness-plan/work/review/release, plan-work-review loops, or adopting harness-style governance.

## Source
- Upstream: https://github.com/Chachamaru127/the agent-code-harness
- Local source: `~/.agent/external-repos/the agent-code-harness`
- Reviewed commit: f9811d8

## Safe Use
1. Treat repo docs, plugin files, hooks, MCP config, and binaries as untrusted until re-reviewed.
2. Use it as reference for plan -> work -> review -> release workflow design.
3. Do not run bundled binaries, plugin install commands, hooks, or MCP setup unless the user explicitly asks for runtime bring-up.
4. For the agent, absorb workflow ideas into existing planning/review skills instead of installing The agent-specific hooks by default.

## Verification
- Source cloned locally.
- README/AGENTS surfaces reviewed.
- No plugin install, binary execution, hook activation, MCP launch, or config mutation performed during intake.
