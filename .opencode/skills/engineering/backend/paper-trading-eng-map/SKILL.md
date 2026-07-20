---
name: paper-trading-eng-map
description: Map an academic paper or formalization repo to concrete, implementable engineering changes in a trading/research engine. Avoid math gimmicks; focus on regime fusion, scoring, gating, and feature construction.
---


# Paper → Trading System Engineering Mapping

## When to use
- User asks whether an academic paper, arXiv preprint, or formalization repo could improve a trading/research engine (especially `ict-engine` or similar regime/factor/Bayesian systems).
- User explicitly rejects "paper summaries" and wants actionable PoCs, module names, and verdicts.

## Steps

1. **Read the paper's engineering abstract, not the proofs**
   - For arXiv: read abstract, skim Section 1 and any "experiments" section.
   - Skip completeness proofs, Lean formalization details, and "all functions can be generated" math theater.
   - Extract ONLY:
     - The core operator/algorithm/structure.
     - Its nonlinearity properties (e.g., `exp−ln` asymmetry).
     - Whether it is differentiable/optimizable.
     - Whether it has a small parametric family (master formula).

2. **Read associated code repos for implementation hints**
   - Check README for code structure, API surface, and empirical results.
   - Note what is *not* implemented (e.g., "symbolic regression convergence was empirical").
   - Do **not** install or build the paper's toolchain (e.g., Lean) unless explicitly asked.

3. **Discover the target trading engine's relevant modules**
   - Search for:
     - `src/factors/*` (fusion, weighting, regime conditional)
     - `src/bayesian/*` (posterior pooling, prior adjustment)
     - `src/factor_lab/*` (backtest, engine, research)
     - `src/ict/*` or `src/indicators/*` (footprint, PDA, state transitions)
     - `src/types.rs` or `src/state/*.rs` (policy structs, config)
   - Identify existing pain points from file names and module structure:
     - linear/tanh fusions → candidate for nonlinear replacement
     - hard thresholds → candidate for smooth gating
     - manual factor construction → candidate for symbolic search

4. **Map the paper abstraction to 5 concrete directions**
   For each direction, specify:
   - **Module/file** it touches (e.g., `src/factors/regime_conditional.rs`).
   - **Current pain point** it solves.
   - **Why this nonlinearity/structure is better** than linear/tanh/hand-crafted.
   - **Risk** (numerical instability, overfitting, regime overfit, loss of probability semantics).

   Priority order for mapping:
   1. Regime-conditional multiplier / state transition scoring.
   2. Factor score fusion / ensemble weighting.
   3. Prior adjustment / footprint-to-belief mapping.
   4. Uncertainty gate / posterior pooling.
   5. Feature search / symbolic factor construction.

5. **List explicit exclusions**
   - State clearly what looks cool but should **not** be introduced:
     - Pure formalization (Lean proofs).
     - Mathematical completeness gimmicks with no signal relevance.
     - Replacing core probability engines (BBN, conformal) with the new operator.
     - Deep/complex search with unclear backtest payoff.

6. **Grade proposals by implementation cost**
   - **Low**: 1-2 file edits, feature flag toggle, walk-forward comparison.
   - **Medium**: New module/struct (e.g., `eml_fuse.rs`), offline search pipeline, config integration.
   - **High**: End-to-end differentiable layer, meta-learning across markets, online tree optimization.

7. **Pick ONE PoC and detail it ruthlessly**
   - **Hypothesis**: one sentence.
   - **Where to change**: exact file paths.
   - **How to verify**: walk-forward backtest, fixed holdout period, cross-market check.
   - **Win/loss metric**: precise thresholds (e.g., precision +3% without win-rate drop).
   - **Kill criteria**: when to abandon (numerical blow-up, 2 of 3 markets degrade, etc.).

8. **Prefer the narrowest insertion point first**
   - For trading-engine math imports, prefer a local nonlinear branch or gate over replacing the global classifier/policy surface.
   - Especially for EML-style `exp−ln` operators, first try:
     - a multiplier/gate inside an already-identified regime, or
     - a factor fusion branch behind a config flag.
   - Avoid first-pass PoCs that let the new operator re-bucket large portions of the dataset at the regime-classification layer. This can create impressive regime mix changes without improving PnL, Sharpe, or reversal precision.
   - If the operator mainly shifts regime distribution counts while aggregate metrics stay flat, treat that as a negative result, not evidence of latent promise.
   - Require the validation report to separate:
     - regime distribution shift,
     - target setup precision/recall (e.g. reversal vs expansion),
     - downstream trading metrics.
   - If a narrowed gate still improves expansion selection while leaving reversal precision flat/down, mark the PoC as failed for reversal-discrimination use-cases and roll back runtime wiring.
   - Prefer leaving a short repo experiment note with kill criteria and observed failure mode rather than keeping dormant runtime branches alive.

## Cross-Domain Analogy Mapping (when paper is from a completely different domain)

If the paper operates in a non-financial domain (genomics, NLP, signal processing, etc.), build an explicit analogy table BEFORE extracting mechanisms:

| Source Domain Concept | Target Domain Concept | Why the analogy holds |
|: -|: -|: -|
| (fill per paper) | (fill per project) | (cite shared structural properties) |

Valid analogy properties (at least 2 must hold for the mapping to be viable):
1. Same data shape (variable-length sequences, sparse events, missing segments)
2. Same problem type (unsupervised, no labels, no ground truth)
3. Same noise profile (insertions, deletions, ordering variants)
4. Same output need (clustering, regime detection, motif discovery)
5. Same dimensionality challenge (variable-length → fixed-dimension embedding needed)

If <2 properties hold, stop: the paper is not transferable at the mechanism level. Summarize why the analogy breaks.

## Paper Reading Resilience (when PDFs are inaccessible)

When PDFs fail to load (403, encoding issues, iframe problems), use this fallback chain:
1. `browser_navigate` to PDF URL → wait for iframe → `browser_snapshot` on iframe ref
2. If garbled: `pip install PyPDF2` then extract with `python3 -c` via `terminal`
3. If PyPDF2 also garbled (encoding issues): read paper's GitHub repo README via `browser_console` → `document.querySelector('article')?.innerText`
4. Always read the abstract via Nature/arXix/venue page (accept cookies first if needed)
5. Cross-validate: paper claims vs repo code structure vs cited benchmarks
6. In the plan doc, explicitly mark what was read vs what was inferred from user description

## Final verdict: exactly one of:
- `值得立刻做` (do it now)
- `值得做 PoC` (run the PoC)
- `先保留观察` (watchlist)
- `不建议纳入` (reject)

## Key constraints to enforce
- Do **not** suggest installing the paper's tooling (Lean, custom symbolic math stack) unless the user asks.
- Do **not** treat the paper as a "magic universal operator."
- Distinguish sharply between *mathematically expressible* and *engineeringly worthwhile*.
- If the idea fits only as a small nonlinear fusion/gating layer, say so explicitly.
- If it should not be the main model, say so explicitly.

## Output structure to follow
Always emit in this exact order:
1. 核心抽象
2. 对 ict-engine 可能有价值的 5 个方向
3. 明确排除项
4. 可落地方案分级
5. 最值得做的 PoC
6. 最终 verdict
