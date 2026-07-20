# Market regime / strategy source scan pattern

Use when the user asks for finance/trading papers plus open-source repos, forums, or strategy-script sites around market regimes, factors, options, volatility, or profitable strategy discovery.

## Source mix

1. arXiv first for structured finance papers:
   - `cat:q-fin.ST` for regime/statistical classification
   - `cat:q-fin.PM` for portfolio/factor allocation
   - `cat:q-fin.TR` for trading/options/execution
   - Prefer `AND` terms. Avoid broad `regime OR switching` noise.
2. GitHub next for executable references:
   - Search `market regime detection trading strategy`, `hidden markov model trading strategy python`, `quant factor library alpha factors python`, `volatility risk premium options strategy python`.
   - Treat stars/README as triage only, not return evidence.
3. Web/forum/script sources for folk formulas and implementation variants:
   - TradingView scripts: market regime, volatility, trend filter, Pine Script.
   - NinjaTrader forum/ecosystem: regime switching, relative volume, volatility stops, NQ/ES execution rules.
   - QuantConnect/LEAN: options chains, VRP examples, executable framework references.
   - OptionAlpha, MenthorQ, VolatilityBox, Quantpedia, AQR: VRP/put-writing/volatility education and whitepapers.

## Finance paper query patterns

- `all:market+AND+all:regime+AND+all:classification+AND+cat:q-fin.ST`
- `all:hidden+AND+all:markov+AND+all:trading+AND+cat:q-fin.ST`
- `all:regime+AND+all:switching+AND+all:financial+AND+cat:q-fin.PM`
- `all:volatility+AND+all:risk+AND+all:premium+AND+cat:q-fin.PM`
- `all:factor+AND+all:timing+AND+all:market+AND+cat:q-fin.PM`
- `all:momentum+AND+all:regime+AND+cat:q-fin.PM`
- `all:option+AND+all:volatility+AND+all:strategy+AND+cat:q-fin.TR`
- `all:limit+AND+all:order+AND+all:book+AND+all:regime+AND+cat:q-fin.TR`

## Output shape

Write a user-facing markdown synthesis, not raw search dumps:

- Fast conclusion: no single perfect regime classifier. Recommend ensemble/gating.
- Paper sections:
  - market regime detection
  - factor/strategy papers
  - options/volatility papers
- Open-source repos with one-line use case and trust caveat.
- Forum/script sites with entry URLs and extraction guidance.
- Market-by-market mapping:
  - equities/index futures
  - options/volatility
  - gold/commodities
  - crypto
  - FX if enough evidence
- Implementation priority:
  - P0 immediately testable features/gates
  - P1 ensemble/specialists
  - P2 data-heavy or experimental methods
- Validation standard: Purged CV, embargo, DSR/PBO, turnover, slippage, OOS across regimes, tail-risk stress for short-vol.

## Interpretation rules

- Papers are evidence candidates. Repos/scripts are implementation clues.
- TradingView/NinjaTrader scripts are formula sources only. Do not trust published backtests without independent replication.
- VRP/short-vol strategies require tail-risk gates: VIX/VIX3M, VVIX/VIX, IV-RV, HV percentile, event/calendar, correlation spike.
- Regime classifier output should map to execution roles such as TrendExpansion, RangeConsolidation, ExtremeStress, ReversalBrewing, Unknown.
