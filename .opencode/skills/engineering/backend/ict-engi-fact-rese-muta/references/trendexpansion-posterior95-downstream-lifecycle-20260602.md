# TrendExpansion Posterior95 Downstream Lifecycle, 2026-06-02

Use this note when continuing the NQ 15m TrendExpansion-only posterior95 state
shift branch. It records the downstream/paper/lifecycle work that was actually
advanced, so future agents should not restart from "missing downstream" or
pretend the practical gate is complete.

Boundary: this is a branch-specific lifecycle record for an explicitly
posterior-gated strategy. It is not a generic `盈利因子` gate and must not be
used to require `P(TrendExpansion) >= 0.95`, same-root execution
materialization, or accepted paper/live feedback for a separate clean-AQ
verified-cost-positive profit survivor unless the current task explicitly asks
for this posterior95 branch or a stricter lifecycle packet.

## Branch Contract

- Factor id:
  `tomac_nq_15m_trend_expansion_only_regime_transition_posterior95_state_shift_exact_aq_v1`
- Branch path:
  `RegimeTransition -> TrendExpansionOnly -> CompressionBreakoutStateShift -> Posterior95AdmissionFilter -> tomac_nq_15m_trend_expansion_only_regime_transition_posterior95_state_shift_exact_aq_v1`
- Entry regime: `TrendExpansion` only.
- Posterior floor: `P(TrendExpansion) >= 0.95`.
- Other regimes: `reference_veto_only_no_entry`.
- Session scope: `ETH/full_retained_session`.
- RTH filter: `false`.
- For this explicit posterior95 lifecycle branch, practical flags remain false
  until same-root execution materialization and accepted paper/live/broker
  feedback exist.

## Source Exact-AQ Evidence

- Source run root:
  `/tmp/ict-engine-trendexpansion-posterior95-state-shift-aq-20260602T095144+0800`
- Validated metrics:
  `/tmp/ict-engine-trendexpansion-posterior95-state-shift-aq-20260602T095144+0800/checks/terminal_metrics.validated.json`
- Trade export:
  `/tmp/ict-engine-trendexpansion-posterior95-state-shift-aq-20260602T095144+0800/checks/aq_trades_TomacNq15mTrendExpansionOnlyRegimeTransitionPosterior95StateShiftExactAqV1.json`

Result:

- Exact-AQ exit: `0`.
- Trades: `624`.
- Instrument-cost total profit pct: `+15.591456`.
- Instrument-cost profit factor: `1.244445`.
- Split instrument-cost positive all thirds: `true`.
- Positive years: `4/5`. `2025` was slightly negative.
- No-lookahead contract: closed-bar evidence, next-bar shifted entry.

## Downstream Lifecycle Run

- Run root:
  `/tmp/ict-engine-trendexpansion-posterior95-downstream-lifecycle-20260602T123700+0800`
- Workdoc:
  `/tmp/ict-engine-trendexpansion-posterior95-downstream-lifecycle-20260602T123700+0800/workdoc.md`
- Terminal metrics:
  `/tmp/ict-engine-trendexpansion-posterior95-downstream-lifecycle-20260602T123700+0800/checks/terminal_metrics.json`
- Terminal summary:
  `/tmp/ict-engine-trendexpansion-posterior95-downstream-lifecycle-20260602T123700+0800/summaries/terminal_summary.json`
- Claim:
  `/tmp/ict-engine-agent-claims/board-b-factor-refinement/20260602T123700+0800-codex-trendexpansion-posterior95-downstream-lifecycle.claim`

All lifecycle and readback stages exited `0`:

- `01_auto_quant_results_import`
- `02_auto_quant_prior_init`
- `03_auto_quant_ingest_diagnostic_trades`
- `04_analyze`
- `05_workflow_status`
- `06_pre_bayes_status`
- `07_policy_training_status`
- `08_export_structural_path_ranking_target`
- `09_apply_structural_path_scores`
- `10_register_path_ranker_artifact`
- `11_enable_structural_path_ranking_runtime`
- `12_workflow_status_after_ranker`
- `13_policy_training_status_after_ranker`
- `14_ibkr_paper_connect_preflight`
- `15_ibkr_execution_readback`

Lifecycle readback:

- Diagnostic feedback source:
  `exact_aq_diagnostic_feedback_not_broker_fill`.
- Diagnostic feedback trades applied: `624`.
- Invalid trades: `0`.
- Feedback observation validation: `624/30`, ready.
- Structural path ranking target: `mature_rows=4`,
  `history_mature_rows=1253`, `raw_scored_mature_rows=1253/30`,
  `production_validation_rows=1252/30`.
- Ranker runtime: enabled, ready, `candidate_set_only`,
  `source_kind=candidate_set`, `active_match_count=3`.
- Factor lifecycle: `learning_admitted_count=4`, `paper_ready_count=4`,
  `deploy_ready_count=0`, `live_ready_count=0`,
  `live_trade_usable_count=0`.

## Execution And Paper Readback

Workflow after ranker exposed the structural candidate with:

- `path_ranker_raw_score=0.95`.
- `path_ranker_runtime_source=candidate_set`.
- `path_ranker_execution_gate_status=pass`.
- `candidate_status=no_trade`.
- `actionable=false`.
- `execution_readiness=0.18126263912576335`.

Execution-tree trace:

- Branch: `block_crowded`.
- Gate status: `blocked`.
- Bias: `skip`.
- `path_ranker_score_visible_to_execution_tree=false`.
- `path_ranker_score_used_by_execution_tree=false`.

IBKR paper side:

- Paper connect preflight exit: `0`.
- Connected account: `DUN189136`, paper account, port `4002`.
- Decision: `paper_order_not_submitted`.
- No `--execute-paper-roundtrip`. No order was placed.
- Read-only `reqExecutions` readback exit: `0`.
- Readback file:
  `/tmp/ict-engine-trendexpansion-posterior95-downstream-lifecycle-20260602T123700+0800/checks/ibkr_execution_readback_nq.json`
- `execution_rows_total=0`.
- Accepted feedback rows: `0`.
- Accepted feedback requirement:
  paired executions with `broker_fill_evidence=true` and
  `commission_report_present=true`.

## Verdict

This branch has progressed beyond "missing downstream/lifecycle":

- Auto-Quant import/prior-init ran.
- Diagnostic exact-AQ trade feedback was ingested.
- Analyze, Pre-Bayes, workflow, policy-training, path-ranker export/apply,
  trainer registration, and runtime enablement ran.
- Paper account connectivity and read-only execution readback ran.

It is still not production practical:

- `same_tree_practical_closure=null`.
- `promotion_allowed=false`.
- `trade_usable=false`.
- `update_goal=false`.
- The execution candidate is still `no_trade`.
- The execution tree blocks the rooted branch and does not consume the ranker
  score.
- There is no accepted broker/paper execution feedback.

Continue from the execution materialization and accepted-feedback blocker. Do
not rerun the same source exact-AQ or repeat the same lifecycle chain unless the
current artifacts are missing or corrupted.
