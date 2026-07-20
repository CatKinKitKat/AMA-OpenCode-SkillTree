# Market regime / regime detection research pack

Use when the user asks for papers, factors, or open-source tooling to identify market regimes.

## Tooling lesson from session

- arXiv API can return `429` quickly on repeated broad finance/regime queries. Back off or switch sources.
- Semantic Scholar unauthenticated search also hit `429`. Use sparingly for citation counts and abstracts.
- Crossref worked well for DOI/citation metadata on known or broad paper queries.
- GitHub API produced intermittent SSL EOF from this environment. `api.gread.dev/repo?name=owner/repo` was more reliable for known repos and README inspection.
- For repo discovery, DuckDuckGo HTML search found niche GitHub repos when GitHub API search was flaky.

## High-value papers found

- Hamilton (1989), `A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle`, DOI `10.2307/1912559`, ~6333 Crossref refs. Core Markov-switching foundation.
- Ang & Bekaert (2002), `International Asset Allocation With Regime Shifts`, DOI `10.1093/rfs/15.4.1137`, ~1324 refs. Regime shifts applied to asset allocation.
- Truong, Oudre, Vayatis (2020), `Selective review of offline change point detection methods`, DOI `10.1016/j.sigpro.2019.107299`, ~1022 refs. Foundation for `ruptures` and change-point segmentation.
- Yuan & Mitra, `Market Regime Identification Using Hidden Markov Models`, DOI `10.2139/ssrn.3406068`. Direct HMM market-regime paper.
- Guidolin & Timmermann (2005), `Asset Allocation under Multivariate Regime Switching`, DOI `10.20955/wp.2005.002`. Multi-asset regime-switching allocation.
- Chen & Tsang (2018), `Regime Change Detection Using Directional Change Indicators in the Foreign Exchange Market to Chart Brexit`, DOI `10.1109/tetci.2017.2775235`. Directional-change event indicators for regime changes.
- Mueller-Glissmann & Ferrario (2024), `Dynamic Asset Allocation Using Machine Learning: Seeing the Forest for the Trees`, DOI `10.3905/jpm.2024.1.582`. Random-forest macro regime probabilities for asset-allocation overlays.

## Open-source repos to inspect first

- `hmmlearn/hmmlearn`: Python HMM library, scikit-learn style, `pip install hmmlearn`. Good for GaussianHMM regime probabilities.
- `deepcharles/ruptures`: offline change-point detection, `pip install ruptures`. Good for structural-break confirmation.
- `jmschrei/pomegranate`: probabilistic models / HMMs with PyTorch backend. Heavier but more flexible.
- `taylorjmellon/market-regime-detection`: small end-to-end SPY pipeline using KMeans + HMM + backtest. Use as scaffold, not trusted dependency.
- `unit8co/darts`: time-series forecasting/anomaly detection. Useful if regime break is framed as anomaly/forecast residual.
- `hudson-and-thames/mlfinlab`: finance ML toolkit ideas. Public repo may not contain full usable core.

## Recommended feature/output schema

Input features:
- `ret_1d`, `ret_5d`
- `vol_20d`, `vol_ratio = vol_20d / vol_120d`
- `trend_20d = close / ma20 - 1`, `trend_60d = close / ma60 - 1`
- `drawdown_20d`
- cross-asset features such as `corr_spy_tlt_60d`, credit spread, yield curve, commodity/gold momentum
- paper-backed evidence layers for implementation audits:
  - HMM/HHMM: state probability, entropy, transition matrix, duration survival, label-switching relabel rule
  - change-point/quickest detection: structural-break score, days/bars since break, transition hazard
  - directional change: DC event frequency, overshoot ratio, event-time volatility, trend persistence
  - realized covariance: correlation-matrix distance, correlation dispersion, stress/risk-off confirmation
  - volatility/vol-of-vol: HV, IV, IV/HV, IV rank, VIX/VIX3M/VVIX-style context

Outputs:
- `regime_id`, `regime_label`
- `p_bull`, `p_bear`, `p_high_vol`
- `regime_entropy = -sum(p * log(p))`
- `regime_persistence = transition[prev, curr]`
- `last_change_point_idx`, `days_since_change_point`
- `segment_vol`, `segment_ret`, `segment_slope`
- `risk_gate`
- `evidence_columns_present` / `evidence_columns_missing` when auditing a trading engine

## Implementation caveats

- Avoid full-sample fit before backtest. Use walk-forward fitting.
- HMM labels can swap between fits. Relabel states by realized mean return / volatility.
- Offline change-point detection has lookahead if used naively. Live use needs rolling windows and delayed confirmation.
- Regime is usually better as a gating/risk overlay than as direct alpha.