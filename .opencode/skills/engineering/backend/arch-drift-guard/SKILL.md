---
name: arch-drift-guard
description: >
Use when a repo is suffering architecture drift, API drift, main-file bloat, boundary erosion, or repeated breakage from cross-layer edits. Enforces artifact-first anti-drift governance: classify drift type, declare allowed change surface, write durable repo artifacts, require mechanical checks, and only then modify code.
tags: 
version: 1
---


# arch-drift-guard

## When to use
Use this skill when any of the following appears:
- giant `main.rs` / god file keeps regrowing
- repeated API drift after partial refactors
- struct initializer drift after adding fields
- cross-layer edits keep breaking compile/tests
- module boundaries are unclear or routinely violated
- agent edits cause repo erosion over time
- user says things like: “漂移”, “越改越乱”, “边界不稳”, “模块化不够”

## Do not use when
- simple isolated bug with clear local fix -> use `systmt-dbggng`
- brand-new system design -> use `ddd-project-grdrls`
- only one extraction move with known order in ict-engine main.rs -> consider `ict-engi-stag-main-extr`

## Core rule
Do not start with code changes.
First classify the drift, define the allowed change surface, and write the governing artifacts.

## Drift classes
Classify the problem before touching code:
1. `file-truncation-drift`
   - file content is cut, reverted, or structurally broken
2. `api-signature-drift`
   - function signatures changed, call sites stale
3. `struct-initializer-drift`
   - new fields added, builders/defaults/tests stale
4. `boundary-erosion`
   - logic leaks across application/domain/reporting/orchestration layers
5. `workflow-surface-drift`
   - output/report/workflow snapshots evolve without synchronized adapters
6. `dependency-drift`
   - imports/dependencies move without declared layering rules

## Mandatory artifact-first flow
Before significant edits, create or update repo artifacts:
- `DEBUG.md` for reproduction and evidence
- `docs/architecture-boundaries.md` for durable module/layer boundaries
- `docs/change-surface.md` for this task's allowed edit surface
- `docs/drift-ledger.md` for repeated erosion patterns and fixes

If the repo already has equivalent artifacts, update them instead of creating duplicates.

## Allowed change surface
Define explicitly:
- files allowed to change
- files forbidden to change
- public interfaces allowed to move
- invariants that must remain stable
- tests/checks that must pass before expanding scope

If a fix requires touching files outside the declared surface, stop and revise the artifact first.

## Required checks
Always prefer mechanical enforcement over prose.
For each drift task, choose at least 2:
- compile/build check
- targeted test
- full test suite if surface is broad
- search for stale symbols/imports/call sites
- graph/dependency inspection
- diff audit on boundary-sensitive files

## Anti-drift implementation order
1. restore file integrity first
2. restore type/build consistency
3. restore adapter/wrapper surfaces
4. restore module boundaries
5. only then add new feature work

## Contract-first growth under external unknowns
Use this pattern when the target depends on real websites, browsers, callbacks, payment flows, or APIs whose runtime truth is not yet verified, and the user asks for “禁污染/禁负债” style progress:
1. Re-open `docs/change-surface.md` for each increment. Make the current task, allowed files, forbidden files, completion criteria, and rollback trigger explicit.
2. Prefer pure contracts first: dataclasses, state machines, repository methods, schema tables, serializer helpers, and tests.
3. Keep unverified URL/DOM/network/API assumptions out of production services. Place them only in `probes/` or `adapters/experimental/` after evidence exists.
4. Do not widen into pipeline, browser workers, or old giant scripts unless the change surface explicitly permits it.
5. Verify with targeted tests plus full suite/compile check when the surface touches models or storage. Remove generated caches before finalizing.


## Architecture guardrails
- One new field -> update struct, default, builders, tests, fixtures in one pass
- One new function signature -> patch all call sites immediately
- New reporting/output surface -> add adapter/helper first, do not inline giant logic into `main.rs`
- Repeated similar output blocks -> extract helper, do not wide-replace text
- If touching a god file, prefer unique helper insertion over direct large rewrites
- For Rust `main.rs` signature migrations, do not run broad textual close-paren replacements (`)?` vs `})?`) across the file. Use unique, per-callsite edits or AST-aware/manual patches. Wide replacements can silently corrupt unrelated `append_*` / `save_*` calls.
- When modularizing a god-file CLI/workflow surface, extract pure value/surface builders first, then command functions later. Command handlers often depend on local loaders, refresh helpers, and private bootstrap glue. Moving them first creates unresolved-boundary churn.
- Before moving a function out of a monolith, list its private dependencies explicitly: data loaders, snapshot refreshers, local helper views, and crate-path assumptions (`crate::...` vs binary-side `ict_engine::...`). If those are not portable yet, narrow the extraction surface.

## Recommended repo artifacts

### docs/architecture-boundaries.md
Include:
- layer list
- ownership of each layer
- forbidden dependency directions
- allowed adapter bridges
- “what does not belong here” examples

### docs/change-surface.md
Include:
- task objective
- drift class
- editable paths
- non-editable paths
- verification commands
- rollback trigger

### docs/drift-ledger.md
Append entries like:
- symptom
- root cause
- repair order that worked
- new permanent guardrail added

## Validation standard
Minimum before claiming done:
- target compile/build passes
- no stale references in touched surfaces
- declared tests pass
- artifacts updated
- diff is scoped to declared surface or the surface artifact was revised

## Escalation rule
If the same area has drifted 3+ times, stop treating it as a one-off bug.
Create or update a durable architecture boundary artifact or a repo-specific skill.

## Good outputs from this skill
- compact drift classification
- repo artifact updates
- small repair sequence
- boundary/ownership clarification
- mechanical checks listed and executed

## Bad outputs
- vague “we should modularize more” with no artifact
- giant refactor started before classifying drift
- code changes without declared change surface
- relying on memory instead of repo truth

## Suggested commands/checks
Use the agent tools first, but typical shell verification may include:
- `cargo fmt --all`
- `cargo check`
- `cargo test`
- targeted test names
- targeted symbol searches for stale paths/signatures

## Relationship to other skills
- use with `systmt-dbggng` when root cause still unknown
- use with `ict-engi-stag-main-extr` for large `main.rs` extraction in ict-engine
- use with `ict-engi-safe-main-outp` when drift is concentrated in output/reporting wiring
- use with `ddd-project-grdrls` if drift reveals missing strategic boundaries
