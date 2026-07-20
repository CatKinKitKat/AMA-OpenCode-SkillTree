# Clean-AQ Profitability Practical Admission Boundary

Date: 2026-06-02
Scope: `route_line=profitability_factor` only.
Status: profit-route admission contract. Not a regime-discrimination work queue.

## Boundary

Use this note when the current task asks for `盈利因子`, `实战因子`,
`trade_usable=true`, clean-AQ practical admission, objective closure, or commit
prep for a profit factor.

A clean-AQ verified-cost-positive profit survivor is judged by trading economics
and execution-safe proof:

- learning admission is present.
- `evidence_count >= 12`.
- leakage and no-lookahead checks pass.
- market-data provenance is verified.
- branch and factor identity are preserved.
- exact instrument-cost model is verified.
- net result stays positive after that verified cost.
- when `survives_instrument_cost` is present it is authoritative and must be
  typed boolean `true`. Explicit `false`, string `"false"`, or any non-true
  value vetoes the cost survivor even if the after-cost net field is positive. Positive after-cost net can infer survival only for legacy rows where the
  explicit survivor marker is absent.
- command exits zero with no timeout.
- source archive validation passes.
- `promotion_allowed=true` and `trade_usable=true` come from the clean-AQ
  practical admission owner, not from a raw counter or regime sidecar.

Missing posterior/truth-label artifacts are not profit-route blockers. Record
missing `posterior95`, truth labels, subclasses, counterexample labels, or
`P(TrendExpansion) >= 0.95` as
`discrimination_followup_not_profit_blocker`, then continue the profitability
task.

Do not launch, patch, or commit regime-only sidecar work from a profitability
task unless the user explicitly asks for `辨别因子`, posterior calibration,
truth labels, subclasses, counterexamples, conformal calibration, or
`P(TrendExpansion) >= 0.95` in the current turn.

## Advisory Readiness

This project is an advisory CLI. For policy-training readback,
`paper_ready_count` and `live_ready_count` share the same advisory basis. A good
factor with verified evidence can be practical without accepted broker/paper
fills, Pre-Bayes/BBN/execution-tree placement, same-tree closure, or same-root
feedback loops. Those artifacts are robustness and breadth evidence, not the
generic clean-AQ profit-survivor gate.

Accepted paper/live/broker execution feedback and same-tree practical closure are
stronger lifecycle evidence. They may upgrade confidence when present, but their
absence does not veto a clean-AQ verified-cost-positive profit survivor.

## Contractized Library Closure

Clean-AQ practical admission proves the factor earned practical profitability
status. It does not by itself make the factor naturally recallable by the
system. Once a profitability lane proves `promotion_allowed=true` and
`trade_usable=true`, close the lane by converting the survivor into a
contractized `factor_library/profitability/<factor_id>/factor.json` record.

A contractized profitability factor must retain the redacted evidence ref and
must carry all four machine-readable consumer contracts:

- `strategy_recipe`: setup context, entry model, exit model, invalidations,
  evidence refs, and `runtime_actionability`.
- `activation_contract`: market/timeframe/session scope, closed-bar-only
  requirements, current activation gates, and suppression conditions.
- `bbn_hooks`: `target_node=trade_outcome`, `target_states=["win","scratch","loss"]`,
  prior evidence refs, posterior-query conditioning fields, and update
  observations.
- `tree_hooks`: safe `execution_tree_consumers`, pre-branch checks, action
  sequence, entry context, exit context, and evidence refs.

Do not copy raw `/tmp` Auto-Quant output, candles, broker fills, account fields,
or maintainer-local paths into the repo. The record is a lightweight executable
contract plus redacted proof summary, not a raw experiment archive and not a
direct order-placement instruction.

Before treating the current factor-training lane as finished, run and record:

```bash
python3 support/scripts/research/factor_library_audit.py --compact
python3 support/scripts/research/factor_library_profitability_bundle.py \
  --output-json /tmp/factor_library_profitability_consumer_bundle.json \
  --compact
python3 support/scripts/research/factor_library_runtime_boundary_audit.py --compact
```

Also inspect the exported profitability bundle and prove the target factor is
present with `strategy_recipe`, `activation_contract`, `bbn_hooks`, and
`tree_hooks`. The audit must show zero schema, route-boundary, evidence,
privacy, and lightweight violations. The bundle must show
`runtime_actionability=requires_current_activation_and_runtime_gates`.

This contractized library state is a valid local end state for a profitability
training lane after the coherent factor-library slice is committed. Remote push
or remote readback is required only when the user asks to push, when release or
remote sync is in scope, or when a release-readiness audit requires it.

After a contractized factor closes, do one of two things explicitly:

- `Decision: stop_after_contractized_factor`
- `Decision: loop_new_factor`

If looping, terminalize or close the old claim first, preserve the old `/tmp`
run root as external evidence, rerun the current claim/process collision audit,
and start a fresh claim, run root, and factor id. Do not keep mutating the same
closed factor or reuse its scratch state as the next lane's authority.

## Full Refining Process

Relaxed practical admission is not the whole profitability-factor refining
process. A factor can be advisory practical while the full process is still
open. The full process must keep these followups visible until typed evidence
closes them:

- `paper_feedback_pending`
- `live_feedback_pending`
- `broker_feedback_pending`
- `slippage_expansion_unverified`
- `cross_market_revalidation_missing`
- `cross_contract_revalidation_missing`
- `drift_monitoring_missing`

Code/readbacks should expose `full_process_evidence`,
`full_process_complete=false`, and the corresponding `full_process_followups`
rather than hiding the missing work in prose. These followups are not generic
relaxed-admission vetoes. They are objective-closure blockers when the task asks
whether the complete profitability-factor refining process is done. In
`objective_closure_snapshot.py`, a validated practical proof with unresolved
followups must report
`profitability_full_process_incomplete` while preserving the practical proof's
`promotion_allowed`, `trade_usable`, and `update_goal` flags. The followups also
become terminal defects when the followup evidence proves a concrete failure,
such as non-positive net after expanded slippage, invalid broker/paper/live
feedback, cross-market or cross-contract failure, or drifted live behavior.

Audit/readback consumers must not trust an explicit `full_process_followups`
list as a complete list unless the corresponding proof fields are present.
Normalize the readback by adding every required followup whose proof field is
absent, not `true`, or lacks the corresponding positive `*_evidence` detail
field. A non-empty detail object or string that declares `failed`, `blocked`,
`pending`, `missing`, `invalid`, `timeout`, `todo`, or an equivalent non-proof
status is not positive proof. The same applies when the negative diagnosis lives
outside a `status` field, for example `reason=missing data`,
`verification_basis=not_rate_verified`, `HTTP 403/404`, non-positive
revalidation reasons, or a non-empty `violations` array. Preserve those details
for diagnosis, but keep the followup open. Otherwise an older packet can hide
missing slippage expansion or drift monitoring merely by setting a naked
boolean, attaching a failed placeholder, or omitting those strings.

## Code Owners

- Profit admission policy: `src/application/factor_lifecycle/profitability_admission.rs`
- Policy-training readback counts: `src/application/entry_models/training_export.rs`
- Workflow-status lifecycle readback: `src/application/orchestration/workflow_status.rs`
- Clean-AQ packet audit/readback: `support/scripts/factor_claim_terminalization_audit.py`
- Objective closure audit: `support/scripts/objective_closure_snapshot.py`
- Factor-library audit: `support/scripts/research/factor_library_audit.py`
- Profitability consumer bundle export:
  `support/scripts/research/factor_library_profitability_bundle.py`
- Runtime/library boundary audit:
  `support/scripts/research/factor_library_runtime_boundary_audit.py`

Regime-discrimination references may be cited only as separate-route followup
context. They are not the source of truth for this profit-route admission
policy and are not the next action for a profitability-factor objective.
