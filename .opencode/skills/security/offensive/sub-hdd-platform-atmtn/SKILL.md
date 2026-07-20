---
name: sub-hdd-platform-atmtn
description: >
tags: 
version: 1
---


# sub.hdd.sb platform automation

## Goal
- Provide one discoverable umbrella for the whole `sub.hdd.sb` puzzle automation class.
- Cover platform/API reverse engineering, hub-entry/iframe runtime behavior, and recurrent userscript solver maintenance.
- Keep game-specific or session-specific detail in support files under `references/`, `templates/`, or `scripts/` instead of fragmenting into many narrow skills.

## Use when
- The user mentions `sub.hdd.sb`, 号多多, puzzle games, Tampermonkey solvers, puzzle15, memory flip cards, 2048, sudoku, or tile-style puzzle automation.
- You need to debug or improve a local userscript file such as `puzzle15-solver.user.js`, `memory-solver.user.js`, `puzzle2048-solver.user.js`, `sudoku-solver.user.js`, or `tile-solver.user.js`.
- You need to inspect the platform’s API contract, difficulty enums, active-session behavior, or iframe/hub-entry page model.

## Class-level workflow
1. Read the local userscript first, not a repo copy.
2. Identify whether the problem is:
   - platform/API understanding
   - hub-entry / iframe UI runtime
   - solver state correctness
   - heuristic/optimization quality
   - proof/debug instrumentation
3. Apply the smallest code-level fix first.
4. Run `node --check` on each edited userscript.
5. Only after deterministic bugs are fixed should you tune heuristics.

## Core platform model
- `sub.hdd.sb` is a shared puzzle platform with multiple games behind a common shell.
- The site frequently uses `custom/hub-entry` plus a same-origin embedded iframe for the actual game page.
- These games are server-authoritative. Local solver logic plans moves, but the backend decides the true resulting state.
- Therefore API semantics and session sync matter more than DOM-only assumptions.

## Problem classes

### 1. Platform/API reverse engineering
Use this class when you need:
- endpoint discovery
- auth model understanding
- difficulty enum validation
- per-game request/response semantics
- reward / session / anti-cheat behavior

### 2. Hub-entry / iframe runtime bugs
Use this class when you see:
- duplicate panels
- missing panels after navigation
- close buttons that do not stick
- start/difficulty controls that only click shell UI and not the real game surface
- stale panel bindings or stale intervals across page transitions

### 3. Solver-state correctness bugs
Use this class when you see:
- repeated illegal moves
- loops on the same card/index
- already revealed / already matched errors
- replaying consumed puzzle states
- invalid-sequence or local preview/API semantic drift

### 4. Heuristic / optimization work
Use this class when correctness is already stable and the remaining problem is:
- poor win rate
- slow convergence
- weak 4x4/5x5 puzzle performance
- 2048 oscillation or corner-loss behavior

## Global rules
- Prefer API truth over inferred DOM truth.
- Treat iframe and page-kind transitions as first-class runtime concerns.
- Separate deterministic correctness fixes from heuristic tuning.
- Keep script-specific incident detail in `references/` rather than cloning a new skill.

## Important recurrent lessons
- `hub-entry` and embedded pages often need page polling plus explicit panel restoration.
- Existing panels should usually be re-shown and rebound, not rebuilt from scratch.
- Server difficulty enums differ by game. Do not reuse one game’s labels for another.
- Puzzle15 direction semantics often differ between local blank-motion solvers and API tile-slide commands.
- Memory-card solvers need three separate state buckets: known, revealed, matched.
- 2048 small-board reliability usually depends more on stability-aware scoring than raw greedy merges.

## What belongs in support files
- Full per-game API maps
- exact patch recipes for known regressions
- puzzle15 optimization notes
- memory-resume/debugging notes
- other narrow reproductions or game-specific troubleshooting detail

## Verification
- `node --check <userscript>` for every changed script
- confirm no duplicated panel/UI regressions on hub-entry
- verify session-adoption logic against a real active session where relevant
- verify API/local direction semantics before declaring puzzle15 fixed

## See references
- `references/platform-reverse-and-api.md`
- `references/userscript-hotfixes.md`
- `references/puzzle15-optimization.md`
- `references/memory-solver-debugging.md`
