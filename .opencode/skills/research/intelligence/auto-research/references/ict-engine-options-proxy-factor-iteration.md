# ict-engine options-proxy factor iteration notes

Use when iterating practical options-like factors without reliable historical option-chain/OI/Greeks data.

## Durable pattern

When real options data is missing, do not label the factor as true GEX, 0DTE flow, IV skew, or dealer positioning. Use explicit proxy names:
- `vrp_proxy`
- `ivrv_compression_proxy`
- `gamma_pin_proxy`
- `realized_skew_proxy`
- `zeroDTE_flow_proxy`

Practical first pass:
1. Use a dense, already-validated price trigger for entries, e.g. MACD zero-line/signal reclaim.
2. Add option-volatility logic only as a regime gate, not as the sole trigger:
   - realized-vol compression
   - ATR percentile cap
   - realized skew / downside pressure
   - optional VIX/VXN sidecar if available
3. Sweep all practical timeframes above 1m: `5m`, `15m`, `1h`, `4h`, `1d`.
4. Keep only timeframes that clear both density and profitability gates.
5. Send only surviving branches into tree / structural path ranking.

## Gate example from 2026-05-17

Branch:
`TrendExpansion -> OptionsProxyVolCarry -> ivrv_compression_reclaim -> macd_ivrv_proxy_reclaim_v2`

3-month NQ retained data window: `20251001-20251231`.

Results:
- `5m`: signals=242, trades=240, wins=83, losses=157, PF=1.571, Sharpe=2.174, profit=+3.424%, MDD=-0.931%: keep
- `15m`: trades=78, PF=0.945: discard
- `1h`: trades=16, PF=0.899: discard
- `4h`: trades=2, PF=0.000: discard
- `1d`: trades=0: discard

Tree handoff evidence:
- real trade observations ingested: 336
- structural path runtime: `ready=true`, `status=enabled_history_ready`, `active_match_count=1`
- validation: raw_scored_mature=336/30, production_validation=336/30, observation_validation=336/30
- analyze gate: `pass_neutralized`. Promotion may still be false due market policy/liquidity penalty rather than data shortage.

## Pitfalls

- If a strict ICT/liquidity-sweep branch produces zero trades across 3 months, switch trigger family rather than only widening sweep thresholds.
- If option-chain data is missing, do not spend the iteration pretending dealer fields exist. Run proxy factors and record the data limitation plainly.
- If a framework backtest reports zero trades even though standalone signal counts are non-zero, separate signal validation from framework execution: export the signals, run a small deterministic pandas backtest, and ingest real-trade JSONL as a proxy evidence stream. Treat this as a diagnostic/proxy path, not a final production backtest.
- For tree handoff, verification is not just trade count. Confirm policy-training/structural-path status: runtime ready, validation rows above minimum, and active match count.
