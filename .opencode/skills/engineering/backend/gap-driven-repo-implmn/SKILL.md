---
name: gap-driven-repo-implmn
description: Identify project gaps, search GitHub for reference implementations, translate/adapt to target language, integrate with tests
---


# Gap-Driven Repo Implementation

Use when: project has conceptual gaps, need to find and adapt existing implementations rather than write from scratch.

## Workflow

1. **Gap Analysis**
   - Review available project docs
   - Map existing capabilities vs. stated goals
   - List missing modules with one-line descriptions

2. **GitHub Search** (parallel queries)
   - Use curl to GitHub API: `https://api.github.com/search/repositories?q=...&sort=stars&order=desc&per_page=5`
   - Save JSON to temp files, parse with Python
   - Search strategies:
     - Exact concept terms: `"hidden semi markov regime python"`
     - Broader combo: `"hmm regime detection python finance"`
     - Related methods: `"wasserstein clustering python"`, `"particle filter regime"`
   - Check repo structure via API
   - Download key files via raw.githubusercontent.com

3. **Repo Evaluation Criteria**
   - Stars (4+ for academic, 10+ for production)
   - Has README + working code + ideally paper/PDF
   - Code quality: type hints, docstrings, tests
   - License compatibility (Apache 2.0 / MIT preferred)
   - Can core logic be isolated from framework deps?

4. **Translation to Target Language**
   - Extract pure algorithmic core
   - Strip framework deps, reimplement minimal equivalents
   - Map source language patterns to target idioms
   - For Rust: use enums/structs properly, avoid dynamic typing

5. **Integration**
   - Create module directory with types.rs, engine.rs, mod.rs
   - Write tests for each public function
   - Register in lib.rs
   - Document formulas in module docstrings

6. **Test-Driven Fixes**
   - Run tests after each module
   - Fix compilation errors before moving on
   - If assertion too strict, relax to essential properties

## Pitfalls

- Don't clone large repos: use raw.githubusercontent.com for individual files
- GitHub API may return 0 results with overly specific queries: try broader terms
- Python code often has implicit deps: identify and reimplement from scratch
- Strict mathematical properties may not hold in approximations

## Heuristic-Algorithm Adaptation Notes

When the target is an existing solver/bot and the user asks to improve success rate from external links:

1. Inspect the current local evaluator/search first.
   - Identify whether failure is coming from shallow search, weak heuristic weights, bad move ordering, or target-specific runtime issues.
   - Do not blindly port an entire upstream project if only the scoring core is weak.

2. Prefer extracting the decisive core, not the packaging.
   - Read raw source or rendered code snippets from linked repos/pages.
   - Ignore upstream UI, worker, build, or platform glue unless the target actually needs it.
   - For browser userscripts, a pure-JS heuristic/search upgrade is often the fastest reliable landing zone. WASM/worker ports are optional later.

3. For 2048-style solvers, the highest-value borrowed ideas are usually evaluation terms, not just deeper search.
   - snake-path / gradient weighting
   - empty-cell reward
   - monotonicity
   - smoothness
   - merge potential
   - corner / edge anchoring for the max tile
   - memoized search state
   - deterministic move ordering (often favoring left/up before right/down)
   - bounded chance-node sampling to keep runtime tractable

4. Integrate surgically.
   - Replace or patch only the local solver module.
   - Preserve the surrounding API/UI surface unless the references prove the interface itself is the bottleneck.
   - After integration, verify that old symbols/call sites still line up.

## Example

ict-engine: Found gaps in regime duration, multi-scale resonance, liquidity.
Searched GitHub, found wess_hmm (Wasserstein+HMM) and MSM_python.
Ported to Rust: 12 files, 285 tests passing, 3 new modules.
Output: GAP_REMEDIATION_PLAN.md with formulas and integration plan.
