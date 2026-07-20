---
name: math-frml-agen-patt
description: >
tags: 
version: 1
---


Goal
- Reuse the transferable orchestration ideas from math-formalization agents without inheriting their whole runtime or trusting their bootstrap blindly.

Use this when
- A user shares a theorem-proving / Lean / formalization agent repo and wants the useful parts integrated.
- You need a structured way to plan proofs, decompose subgoals, or store reusable formal results.
- You want the agent to reason about math workflows with explicit reusable artifacts.

Do not use this when
- The task is merely to install or run a third-party math agent. Do security review first.
- The task is ordinary coding/debugging with no formalization workflow.

Core patterns to adopt
1. Tree of Subgoals
   - For hard proofs, decompose into explicit subgoals.
   - Prefer independent subgoals that can be checked separately.
   - Treat subgoal proof status as first-class state.
2. Guide of Plans
   - Generate multiple proof plans or attack strategies before committing.
   - Keep the planner distinct from the prover/executor.
3. Theorem Library
   - Reusable proved statements should be stored in a durable, queryable artifact.
   - Prefer canonical naming and append-only or auditable updates.
4. Axiom Library
   - Temporary assumptions must be explicit, named, and reviewable.
   - Never let assumptions hide inside free-form chat.
5. Tools / Skills / Plugins split
   - Skills encode method.
   - Tools perform deterministic checks/search/stats.
   - Plugins/integrations add optional surface area. Do not bloat the core.
6. Structured feedback loop
   - Compiler/LSP/checker diagnostics should feed repair loops in structured form, not only raw stderr.

the agent adaptation
- Do not install the external runtime unless the user asked for it.
- Absorb workflow ideas into skills and repo artifacts first.
- For theorem-style tasks:
  1. write the target statement
  2. list candidate plans
  3. decompose subgoals
  4. mark assumptions explicitly
  5. run deterministic checks
  6. store proved reusable lemmas/results in a durable artifact if the project has a formal store

Recommended artifacts
- `DEBUG.md` or `PROOF.md` for evidence trail
- `docs/proof-plans/` for larger proof strategies
- project-local theorem/axiom stores when the repo already has them

Adoption filter
- Keep:
  - subgoal trees
  - reusable theorem/axiom stores
  - multi-plan search
  - structured tool/skill split
- Reject or weaken:
  - bootstrap installers as authority
  - hidden assumptions inside prompts
  - unconditional dependence on one vendor CLI/backend

Output pattern
- State what was absorbed: planning, subgoaling, theorem store, axiom discipline, or tool split.
- Name any explicit artifact or skill updated.

Pitfalls
- Do not treat assumptions as proved facts.
- Do not mix planner output and proof output without marking status.
- Do not let theorem libraries become unreviewed dump files.
- Do not force installation when workflow absorption is enough.
