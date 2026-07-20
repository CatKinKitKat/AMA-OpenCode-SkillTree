# TrendExpansion Regime Discrimination Factor Map

Date: 2026-06-02
Scope: regime-discrimination research reserve for TrendExpansion posterior calibration.
Status: research/calibration map only. Not a trading task, profitability task, promotion packet, or current execution queue.

## Regime-Only Task Boundary

This document is for the separate `辨别因子` / posterior-calibration task. It
must not be used to take over, delay, or redefine a profitability-factor
objective. A profitability task may cite this file only to explain a missing
TrendExpansion posterior proof or a research followup. It must not launch or
commit regime-only sidecar work from this file unless the user explicitly asks
for discrimination-factor work in the current turn.

Regime-discrimination work does not require a profitable strategy, broker/paper
execution, downstream practical closure, `promotion_allowed=true`, or
`trade_usable=true`. Those fields may appear in sidecar outputs only to prove
the packet stayed inspection-only and did not cross into trading admission.

Completion evidence for this separate research reserve is regime evidence:

- the target regimes, TrendExpansion subclasses, and counterexamples are
  explicit.
- `truth.jsonl` rows can carry `label_id`, `subclass_labels`,
  `counterexample_labels`, and `posterior_status`.
- the sidecar pipeline preserves those labels in its report.
- conformal/calibration output honestly reports singleton rate, wide sets,
  class-conditional coverage, and abstain reasons.

## Discrimination Posterior Contract

Use this section only when the active task explicitly asks for a
TrendExpansion regime discriminator or TrendExpansion posterior calibration. It
is not the practical gate for a generic `盈利因子` / clean-AQ profit
survivor.

For that discrimination task, closed-bar evidence should estimate whether the
next state is `TrendExpansion`. Every other regime is training, diagnostic,
abstain, or negative evidence. The high-confidence posterior target remains:

```text
P(TrendExpansion) >= 0.95
```

This is a calibrated root-posterior floor after shifted MTF context,
counterexamples, and abstain labels are resolved. It is not an ADX, Aroon,
KAMA, CHOP, or hand-built score threshold. Sub-0.95 rows may be useful as
`train_only_sub95`, `abstain_or_negative_evidence`, or source-intake rows, but
must not open entry search, downstream practical admission, paper/live
collection, `promotion_allowed`, `trade_usable`, or `update_goal`.

Timeframe scope is part of the label contract. A higher-timeframe
`RangeConsolidation` label, for example on `1h/4h`, is not an automatic veto
against lower-timeframe `TrendExpansion` or clean-AQ profitability work. Treat
the HTF range as a parent liquidity/oscillation container: it may contain many
profitable `1m/3m/5m/15m` trend legs. If an exact lower-timeframe lane proves
positive economics after verified instrument cost, no-lookahead, source
provenance, and execution-safe evidence, the HTF range readback remains
context/risk-sizing evidence, not a blocker for the LTF profitability lane.

For a profitability-factor task, judge the profit factor through the clean-AQ
verified-cost-positive tuple or a stricter lifecycle packet. Do not use a
missing posterior95 packet as a reason to hijack the task into regime-only work.

## Regimes To Distinguish

Use these labels as the discrimination target set for new factor packets. The
first five match current MECE recovery labels. The remaining subclasses are
TrendExpansion-oriented child labels for calibration and attribution.

| Label | Regime-only policy | What it means | Evidence we want |
|---|---|---|---|
| `TrendExpansion` | Positive root class after posterior calibration | The next segment should expand directionally, not merely continue a noisy bar | closed-bar state change, directional efficiency, displacement, MTF agreement |
| `TrendExpansion/OnsetFromCompression` | Candidate subclass | Compression or chop releases into directional range expansion | CHOP high-to-falling, VHF rising, BOCPD reset, Donchian/Keltner acceptance, ATR/range expansion |
| `TrendExpansion/PersistentContinuation` | Candidate subclass | Already directional state persists as a regime | KAMA/ER slope, ADX/DMI, Aroon, Vortex/VI, SuperTrend/ATR, KST/Coppock, HTF slope agreement |
| `TrendExpansion/PullbackRejoin` | Candidate subclass | Trend-root pullback rejoins after closed-bar structure evidence | MSS/CISD, displacement, OTE or range-edge reacceptance, direction-quality recovery |
| `TrendExpansion/VolatilityBulgeResolution` | Candidate subclass | Volatility bulge resolves in the trend direction instead of reversing | Mass Index/Keltner pressure plus directional confirmation, not Mass Index alone |
| `Compression` | Negative/abstain | Tight range, no accepted release yet | narrow range, high or non-falling CHOP, low VHF, low realized range, no accepted breakout |
| `RangeConsolidation` | Negative/abstain on the scoped timeframe. HTF range is context, not an automatic LTF veto | Sideways/chop state where expansion evidence is absent on the labeled timeframe. A larger range may still contain lower-timeframe trend legs | low directional efficiency, mean-reverting closes, MMI/noise indicators, failed range acceptance, range-edge acceptance/rejection context |
| `Manipulation` | Negative/abstain unless it becomes directional reacceptance | Stop run, sweep, or false breakout that closes back inside | extreme pierce and rejection, wick/failure labels, failed breakout antiproof |
| `Reversion` | Negative/abstain | Move snaps back toward mean instead of continuing | close against prior direction toward lookback mean, exhaustion/tail labels, divergence |
| `Stress` / `CrashRecovery` | Negative/abstain by default | Jump/liquidity state can look like expansion but lacks stable continuation | jump/stress score, spread/liquidity warning, event-window context, high posterior entropy |
| `Transition` / `Unknown` | Always abstain | Model disagreement or insufficient evidence | HMM/jump disagreement, high entropy, weak support, missing completed-bar availability |
| `Artifact/Lookahead` | Reject | Source or data path uses future information or malformed market data | signal timestamp after entry, synthetic/incomplete HTF bars, fill-missing artifacts, source archive pollution |

## Candidate Evidence Families

These are candidate factors for the posterior, not standalone entry gates. Each
must record `availability_time`, timeframe, shifted MTF source, direction,
session scope, data/provenance status, and whether it raises or lowers the
TrendExpansion posterior.

| Family | Positive TrendExpansion use | Counterexample / antiproof use | Current repo evidence |
|---|---|---|---|
| Compression-release state change | BOCPD reset, CHOP falling from high, VHF rising, Donchian/Keltner breakout acceptance | high CHOP without release, breakout failure, split/year instability | `trendexpansion-bocpd-dynmom-vhfchop-failclosed-20260531.md`, `trendexpansion-bocpd-30m-density-lift-candidates-20260601.md` |
| Directional efficiency and adaptive slope | KAMA/ER slope, L1 trend-filter slope, linear-regression slope large enough to clear verified friction | tiny slope below cost floor, mixed direction, HTF disagreement | `trendexpansion-chop-kama-mass-15m-cost-positive-20260602.md`, `2026-05-30-paper-strategy-reserve.md` |
| Public trend-strength indicators | ADX/DMI, Aroon, Vortex/VI, Chande-Kroll, SuperTrend/ATR, PSAR, KST/Coppock as posterior features | standalone public trend strength that churns after cost or fails splits | 6E DMI/ADX, 6E Aroon/CCI, 6E Vortex/VI, ES SuperTrend/ADX, NQ KST/Coppock lessons in `SKILL.md` |
| Market-structure confirmation | MSS/CISD, displacement, range-edge rejection or breakout acceptance, HTF range-edge context | sweep-and-reject, wick failure, pullback that never reaccelerates | strict OTE/MSS/CISD NQ/YM/ES/6E lessons in `SKILL.md` |
| Volatility-bulge resolution | Mass Index or Keltner pressure only after direction quality confirms expansion | Mass/Keltner as reversal or no-candidate evidence. Pressure without direction | NQ Mass Index/Keltner negative lesson in `SKILL.md`. CHOP/KAMA/Mass positive 15m candidate reference |
| Session and opening impulse | Initial balance extension, opening drive, Daily Donchian, time-of-day continuation when signal is available before entry | opening-drive lookahead, TOD slot overfit, no accepted paper/live feedback | OpeningDrive causal repair and DailyDonchian lessons in `SKILL.md` |
| Noise and serial-dependence filters | Bartels/MMI/Hurst/visibility graph as parent-signal quality filters or antichop features | standalone serial-randomness admission that creates high-turnover low-edge churn | `tomac-bartels-serial-randomness-3m-churn-negative-20260602.md`, MMI lesson in `SKILL.md` |
| Cross-market confirmation | transfer entropy, risk-on/off, relative trend agreement as sidecars after parent trend evidence | cross-asset rotation that is gross/cost negative or leaks future data | `tomac-crossasset-risk-rotation-negative-20260529.md`, `2026-05-30-crossasset-carry-risk-reserve.md` |

## Counterexample Bank

Use these as negative labels or calibration rows before adding a new hard veto.
They should reduce posterior or force abstain. They should not become silent
extra entry gates unless the operator explicitly approves that gate.

| Antiproof label | Disproves | Evidence hook |
|---|---|---|
| `false_breakout_rejection` | breakout/expansion proxy that pierces and closes back inside | MECE `Manipulation`, failed expansion/fade packets |
| `compression_no_release` | high CHOP or narrow range treated as trend | CHOP high but not falling, low VHF, zero-trade strict resonance |
| `slope_bps_lt_cost_floor` | tiny trend slope counted as MTF agreement | skill rule for friction-aware MTF resonance |
| `public_trend_strength_churn` | ADX/Aroon/Vortex/SuperTrend/KST as standalone entry | 6E DMI/ADX, 6E Aroon/CCI, 6E Vortex/VI, ES SuperTrend/ADX, NQ KST/Coppock negatives |
| `ote_pullback_sparse_or_negative` | "trend confirmed means every pullback is entry" | strict OTE/MSS/CISD YM/ES/6E failures and sparse NQ repairs |
| `volatility_bulge_no_direction` | Mass Index/Keltner pressure as entry by itself | NQ Mass Index/Keltner no-candidate cell |
| `serial_randomness_churn` | randomness/serial-dependence filter as standalone admission | Bartels NQ 3m 14,983-trade cost failure |
| `lookahead_source_exact_positive` | positive source result where signal is unavailable at entry | OpeningDrive entered before opening-range direction was known |
| `split_year_instability` | aggregate cost-positive row without robust chronology | initial BOCPD 30m lead before density-lift repair |
| `direction_side_asymmetry` | bidirectional factor where only one side carries edge | CHOP/KAMA/Mass 15m long-positive, short-negative readback |
| `execution_materialization_absent` | historical exact-AQ survivor treated as practical | posterior95 / BOCPD downstream packets with `no_trade`, ranker not used, accepted feedback rows `0` |
| `artifact_or_fill_missing` | data-plane issue mistaken for regime failure | fill-missing warnings, incomplete HTF aliases, polluted source archives |

## 2026-06-03 Intrabar Source-Series Blocker

Run root:
`/tmp/ict-engine-trendexpansion-intrabar-source-diagnosis-20260603T224905`

Scope: diagnose why the intrabar acceptance report failed source alignment
against the same NQ 15m sidecar used by the regime-only packet.

Finding:

- The 15m sidecar/feather source is the adjusted/continuous
  `NQ_USD-15m-futures.feather` under
  `/tmp/ict-engine-trendexpansion-posterior-tailor-20260602T134939+0800`.
- The available 1m input was the raw local Databento-style per-contract CSV
  `~/Downloads/Tomac/nq future 2021-2025/...ohlcv-1m.csv`.
- All `117914` sidecar bars had at least 12 aggregated 1m rows, so this was not
  a missing-row problem.
- Alignment still failed: median close abs diff `637.75`, p95 `2894.25`, and
  `113402` rows above one-tick tolerance.
- The signed raw-minus-sidecar close offset grew across futures rolls:
  `2021` median `3.0`, `2022` `48.75`, `2023` `637.75`, `2024` `1599.0`,
  `2025` `2627.5`.
- Tail sample `2025-12-31T21:45:00Z`: sidecar close `22306.50`, raw 1m
  aggregated close `25434.75`, diff `3128.25`, modal symbol `NQH6`.

Typed blocker:

```text
source_series_incompatibility_blocks_intrabar_alignment
intrabar_alignment_gate_failed
intrabar_source_series_incompatibility
promotion_allowed=false
trade_usable=false
update_goal=false
```

Interpretation: a highest-volume duplicate-contract policy cannot recover the
adjusted continuous 1m path from unadjusted per-contract rows. Intrabar
completion evidence now requires either a source-equivalent adjusted 1m feed for
the same continuous NQ series, or explicit roll/backadjustment metadata that can
transform raw 1m before aggregation. Do not rerun this intrabar acceptance path
unchanged with the same raw 1m CSV.

## 2026-06-03 Intrabar Clean-1m Retest

Run root:
`/tmp/ict-engine-trendexpansion-intrabar-clean1m-acceptance-20260603T232406+0800`

Scope: resolve the source-series blocker above by using a source-equivalent
adjusted continuous NQ 1m feed generated by the clean-AQ pipeline.

Finding:

- The clean source packet
  `/tmp/ict-engine-trendexpansion-retest-hold-quality-15m-clean-aq-20260601T130955+0800/clean/NQ/clean_quality.json`
  reports `NQ_USD-1m.feather` and `NQ_USD-15m.feather` from the same raw CSV
  with `roll_adjustment_method=boundary_prev_close_minus_new_open`,
  `future_lookahead=false`, `session_scope=ETH/full_retained_session`, and
  `eth_full_retained_coverage_status=verified_retained_rows_outside_rth`.
- The clean `NQ_USD-15m.feather` matches the current sidecar CSV on all
  `117914` overlapping bars with `0.0` max OHLCV diff, proving this clean 1m
  feed is source-equivalent for the sidecar window.
- The adjusted 1m feed was converted only for the existing intrabar measurement
  script (`ts_event=date`, constant `symbol=NQ_ADJUSTED_CONTINUOUS`). Conversion
  readback:
  `/tmp/ict-engine-trendexpansion-intrabar-clean1m-acceptance-20260603T232406+0800/input_conversion_readback.json`.
- Rerun report:
  `/tmp/ict-engine-trendexpansion-intrabar-clean1m-acceptance-20260603T232406+0800/out/intrabar_acceptance_report.json`.
  Alignment now passes: `rows_with_ge12_1m_rows=117914`,
  `rows_missing_or_incomplete_1m=0`, `close_diff_abs_p95=0.0`,
  `high_diff_abs_p95=0.0`, `low_diff_abs_p95=0.0`, and
  `close_diff_gt_0p26_count=0`.
- The intrabar feature scan still found no completion candidate:
  `terminal_decision=intrabar_acceptance_no_completion_candidate`,
  `candidate_with_latest_count=0`, `candidate_without_latest_count=0`, and
  `test_oracle_p95_min12_count=0`.
- Completion audit:
  `/tmp/ict-engine-trendexpansion-intrabar-clean1m-acceptance-20260603T232406+0800/out/completion_audit_with_clean1m_intrabar.json`
  remains fail-closed with `completion_proven=false`.

Interpretation: the earlier raw per-contract 1m source was incompatible, but
the source-equivalent adjusted 1m feed exists and removes the intrabar alignment
blocker. The current honest blocker is no longer "missing adjusted 1m". It is
that intrabar acceptance/failure features did not produce a precision95
completion candidate. Keep `promotion_allowed=false`, `trade_usable=false`, and
`update_goal=false`. Do not rerun the same clean adjusted 1m intrabar scan
unchanged unless the label/feature family changes materially.

## 2026-06-03 MTF + Leader/Follower + Structure Combined Tail5000 Slice

Run root:
`/tmp/ict-engine-trendexpansion-mtf-structure-combined-tail5000-20260603T234221+0800`

Scope: combine the source-authority-clean MTF + leader/follower ablation with
the authorized event lifecycle structure fields, without reintroducing
session/DST or flow/depth source claims.

Evidence:

- Combination report:
  `/tmp/ict-engine-trendexpansion-mtf-structure-combined-tail5000-20260603T234221+0800/prep/mtf_structure_combined_auxiliary_report.json`.
- Rule scan:
  `/tmp/ict-engine-trendexpansion-mtf-structure-combined-tail5000-20260603T234221+0800/checks/rule_tailor_scan.json`.
- Completion audit:
  `/tmp/ict-engine-trendexpansion-mtf-structure-combined-tail5000-20260603T234221+0800/checks/completion_audit.json`.

Combination contract:

- It left-joined authorized event lifecycle structure fields into the MTF +
  leader/follower-only tail5000 auxiliary rows using canonical UTC timestamps.
- It did not forward-fill missing structure rows: 4325 event rows matched and
  675 MTF rows retained no event structure fields.
- It deliberately did not declare session/DST or flow/depth authority.

Source authority result:

- Verified semantic families:
  `auxiliary_mtf_completed_bars`,
  `auxiliary_cross_market_leader_follower`, and
  `auxiliary_structure_lifecycle`.
- No semantic missing/unverified families.
- Counts: `htf_completed_bar_proof_true_count=5000`,
  `leader_follower_available_true_count=4971`,
  `structural_confirmation_available_true_count=4196`, and
  `structure_signal_true_count=4196`.

Completion result:

- `completion_proven=false`, `completion_verdict=not_complete`.
- Latest decision remains `unknown_abstain`.
- `target_regime_posterior=0.65`,
  `target_regime_status=supplementary_sub95`.
- At threshold `0.95`, calibration precision is `0.333333` on `18` selected
  and test precision is `0.391304` on `23` selected.
- Expert training best target precision is `0.272727` with support `94`.
- Rule scan reports `terminal_decision=no_precision95_candidate`,
  `candidate_count=0`, and `completion_candidate_count=0`.

Interpretation: verified MTF completed bars, cross-market leader/follower, and
structure lifecycle authority are not sufficient. This repaired the source
authority loophole but not the discriminator. The bottleneck is discriminative
precision and sparse positive supervision, not missing source authority. Do not
rerun this exact combined tail5000 packet unchanged. All practical flags remain
false.

## Posterior Feature Packet Shape

New packets should emit a small structured readback before any downstream use:

```text
regime_root=TrendExpansion
positive_root_regime=TrendExpansion
other_regimes_policy=diagnostic_reference_only_abstain_or_negative_evidence
posterior_floor=0.95
posterior_status=train_only_sub95|eligible_posterior95|abstain_or_negative_evidence
feature_family=<one of the families above>
positive_evidence=[...]
counterexample_labels=[...]
availability_guard=closed_bar_next_bar_or_later
mtf_guard=completed_bars_shifted_no_fill_missing
session_scope=ETH/full_retained_session|RTH_comparison|session_scope_unverified
promotion_allowed=false_or_not_applicable
trade_usable=false_or_not_applicable
update_goal=false
```

If the row becomes `eligible_posterior95`, that only means the regime posterior
is strong enough for a downstream consumer to inspect. It is not trade readiness
and does not evaluate profitability.

## Timeframe Training Matrix

Each requested timeframe is a separate regime-root factor. Train and label them
independently before any resonance claim:

| timeframe | role | current honest status |
|---|---|---|
| `1m` | fastest onset / high-capacity root | not trained for CHOP/KAMA/Mass. Must prove completed-bar feature availability and cost survival |
| `3m` | microstructure bridge | not trained. Use only if retained real `3m` data exists or exact AQ prepares it without synthetic leakage |
| `5m` | fast onset sibling | not trained for this branch. Useful next AQ slice after 15m posterior labels are shaped |
| `15m` | current evidence root | CHOP/KAMA/Mass Quality and QualityLongOnly are verified-cost-positive training candidates |
| `30m` | slower onset / BOCPD sibling | BOCPD/VHF/CHOP has separate cost-positive leads. Do not merge with 15m evidence |
| `1h` | context or standalone slow factor | not trained for this branch. Completed-bucket MTF integrity must be proven first |
| `4h` | resonance/context | likely sparse as a standalone entry lane. May support posterior context only after shift/no-fill proof |

Multi-timeframe resonance may be used to update the posterior only when every
input is a completed bar available before the executable entry bar. A positive
`15m` branch plus a weak `1h`/`4h` context is not broad timeframe coverage.

## Research Queue, Not Profitability Queue

The ideas below are discrimination research reserve only. They are not the next
steps for a profitability-factor objective, not claim work to steal from another
lane, and not completion evidence for `trade_usable=true`.

1. Calibrate the CHOP/KAMA/Mass 15m Quality branch as long-only first. The short
   side is already negative evidence.
2. Turn BOCPD/VHF/CHOP 30m density-lift into a posterior95 calibration packet
   rather than another threshold relaxation.
3. Test L1 trend-filter slope stability and visibility-graph trend persistence
   as parent-signal filters, not standalone entries.
4. Use ADX/DMI, Aroon, Vortex, SuperTrend, and KST/Coppock only as posterior
   features until a same-root run proves they survive verified cost and splits.
5. Add Bartels/MMI/noise filters primarily as antichop or abstain evidence. Standalone noise-filter admissions have already shown churn risk.
6. Keep OpeningDrive/TOD/session features causal: signal availability must
   precede entry, with earliest fill on the next bar or later.

## External Source References

- TradingView Choppiness Index: https://www.tradingview.com/support/solutions/43000501980-choppiness-index-chop/
- TradingView KAMA: https://www.tradingview.com/support/solutions/43000773012-kaufman-s-adaptive-moving-average-kama/
- StockCharts Mass Index: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/mass-index
- Freqtrade lookahead analysis: https://www.freqtrade.io/en/stable/lookahead-analysis/
- Adams and MacKay BOCPD: https://arxiv.org/abs/0710.3742
