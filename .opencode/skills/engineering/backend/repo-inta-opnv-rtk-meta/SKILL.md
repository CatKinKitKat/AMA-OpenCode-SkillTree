---
name: repo-inta-opnv-rtk-meta
description: >-
bgclick reverse-engineering into the agent-native execution: 
version: 1
---


# Repo Intake: OpenEvolve / RTK / Meta-Harness / bgclick

Goal
- Convert four external repos/docs into the agent-native behavior, not cargo-cult installs.
- Prefer selective absorption over adding a second runtime authority.

Use when
- User drops one or more external repos and says to learn, install, absorb, or "吞噬" them.
- Themes include self-iteration, token reduction, harness search, or reverse-engineering workflow.

Decision rules
1. OpenEvolve
   - Learn + absorb, not direct runtime dependency by default.
   - Keep: benchmark-gated branching, baseline-first scoring, traces under repo artifacts, branch/worktree search.
   - Map to the agent via `/background` + cron + repo-local state, not by embedding OpenEvolve itself as a required engine.
2. RTK
   - Install if local Rust toolchain exists and binary verifies.
   - Keep: command-output compression as a distinct surface, with fallbacks when filters fail.
   - the agent-native application: prefer compact outputs for slash/help/status/index surfaces and any generated audit blobs.
3. Meta-Harness
   - Learn + absorb.
   - Keep: treat harness as searchable code around a fixed base model. Separate onboarding/spec from implementation. Log proposer interactions.
   - the agent-native application: optimize routing, memory, context compression, and tool/context presentation as harness layers.
4. bgclick reverse skill
   - Learn + absorb only if the prerequisite stack is absent.
   - Keep: evidence bundle discipline, one-question-per-file, priors-to-verify, shared-context file, empirical reproduction loop.
   - Do not install blindly as a runtime skill if the dependency contract (IDA MCP, macOS reverse stack) is unmet.

the agent-native implementation targets
1. Self-iteration
   - Prefer `/background <self-contained prompt>` for long-running autonomous loops.
   - If repeatable, package as cron prompt + optional skills.
   - Keep state in repo files, not long-term memory.
2. Token thrift
   - Favor compact summaries, indexed metadata, cache-first lookup, and condensed command/report surfaces.
   - Use generated indexes or summaries before raw remote enumeration.
3. Harness search
   - Treat memory, retrieval, routing, compression, and prompt/context construction as harness code.
   - Keep base model fixed unless the user explicitly asks otherwise.
4. Reverse workflow
   - Start with priors, then verify each with runtime evidence.
   - Use research bundle outputs and open-question files for uncertain findings.

Output pattern
- One short verdict per upstream input: install / absorb / learn.
- Then name the the agent artifact added: skill, script, router, command patch, or verified binary.

Pitfalls
- Do not install every promising repo.
- Do not push external doctrine into AGENTS.md.
- Do not turn one-off repo notes into long-term memory.
- Do not claim reverse workflows are ready when key prerequisites are missing.