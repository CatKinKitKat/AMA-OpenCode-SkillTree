---
name: coding-agent-delegation
description: Use when delegating implementation, refactoring, PR review, or long-running coding work to external coding-agent CLIs such as the coding agent, Codex, OpenCode, or a Kanban-isolated agent lane.
version: 1.0.0
author: the agent
license: MIT
---


# Coding Agent Delegation

Class-level guide for using external autonomous coding agents from the agent while the agent keeps ownership of scope, verification, and final claims.

## Core rule
External agents are implementation lanes, not authorities. Give them bounded prompts, collect concrete artifacts, then verify with the agent tools before telling the user work is complete.

## Agent choices

### the coding agent
Use when the user explicitly requests the coding agent, when Anthropic's coding agent is already installed/authenticated, or when a task benefits from a strong autonomous repo-editing loop.

Pattern:
1. Create a self-contained prompt with goal, files, constraints, and verification command.
2. Run via terminal in PTY/background when interactive or long-running.
3. Require a final summary with changed paths, commands run, and blockers.
4. Verify diffs and tests yourself.

### Codex
Use when the user asks for Codex/OpenAI coding agent work, when you want an independent implementation lane, or when a Kanban worker needs a lightweight CLI implementer.

Pattern mirrors the coding agent: bounded prompt, isolated cwd/worktree when possible, final artifact handle, then independent verification.

### OpenCode
Use when the user explicitly wants OpenCode or wants an alternate coding agent for implementation/refactor/review. Treat it as a peer lane: never assume its self-report is true without reading files and running verification.

### Kanban Codex lane
Use when a the agent Kanban worker wants Codex as a narrowly scoped implementation lane while the agent keeps task lifecycle, reconciliation, testing, and handoff. The lane prompt should preserve Kanban ownership boundaries: Codex implements. the agent reconciles, tests, and updates state.

Template: `templates/kanban-codex-lane-prompt.md`.

## Prompt contract
Every delegated coding prompt should include:
- repository path and branch/worktree context
- exact objective and non-goals
- allowed files or directories
- expected verification command(s)
- output format: changed files, commands run, failures/blockers, handoff notes

## Verification checklist
- Inspect `git diff` and touched files.
- Run the smallest meaningful test/build/lint command.
- If the agent claims an external side effect, verify the URL/ID/status yourself.
- If verification fails, either fix directly or send a precise follow-up prompt with the failing output.

## Common pitfalls
- Do not let an external agent choose broad architecture without user-approved scope.
- Do not run long bounded jobs without `notify_on_complete=true`.
- Do not archive the external agent's failure as success. Report blockers directly.
- Do not mix multiple agent lanes in the same dirty worktree unless changes are trivially separable.
