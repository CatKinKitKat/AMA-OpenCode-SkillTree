---
name: daily-stock-analysis
description: >
Wrapper for ZhuLinsen/daily_stock_analysis: LLM-driven A/H/US stock analysis, market review, multi-source quotes/news, decision dashboard, scheduled reports, and push notifications. Use when the user asks for 日常股票分析, 自选股日报, 决策仪表盘, A/H/美股多市场分析, 市场复盘, AI产业链卡脖子/龙头 watchlists, 第一行只给龙头, 全球股排除大陆A股, or to operate/review the local daily_stock_analysis repo.
tags: 
version: 1
---


# daily-stock-analysis

## Source
- Upstream: `https://github.com/ZhuLinsen/daily_stock_analysis`
- Local reviewed source: `~/.agent/external-repos/daily_stock_analysis`
- Upstream root skill: `~/.agent/external-repos/daily_stock_analysis/SKILL.md`

## Security verdict
- Risk: MEDIUM.
- Reason: repo is Python app with API keys, market data providers, notification webhooks, scheduled jobs, Docker/GitHub Actions paths, and outbound network calls.
- Intake action here copied no runtime code into PATH and ran no installers/package managers. Use as reviewed local source/wrapper only until explicit runtime setup is requested.

## Use when
- 用户要求：日常股票分析、自选股日报、AI 决策仪表盘、A股/港股/美股一并分析、市场复盘、推送报告、GitHub Actions 定时跑股票分析。
- 用户要求从需求浪反推产业链、找卡脖子龙头、跟踪 qualification cycle / 前瞻 TAM / 不能被设计掉 / material revenue 的 watchlist。
- 用户要求第一行只给龙头，或要求全球股/全球产业链默认排除大陆 A 股龙头。
- 用户给出 `ZhuLinsen/daily_stock_analysis` 或 `daily_stock_analysis`。
- 需要把该 repo 作为比 `data-science/stock-analysis` 更偏工程化/自动化的股票分析系统参考。

## What it provides
- A/H/US market support.
- Multi-source market/news/fundamental data via efinance, AkShare, Tushare, pytdx, baostock, yfinance, Longbridge, TickFlow, search APIs.
- LLM analysis dashboard with conclusion, data perspective, intelligence, battle plan.
- Push channels: WeCom, Feishu, Telegram, Discord, Slack, email.
- Entrypoints from upstream docs:
  - `python main.py --stocks 600519,hk00700,AAPL`
  - `python main.py --market-review`
  - `python main.py --schedule`
  - `python main.py --serve-only`

## Safe workflow
1. Treat source as untrusted before running.
2. Read `AGENTS.md`, `README.md`, `.env.example`, `requirements.txt`, `.github/workflows/*`, and relevant `src/` modules before runtime setup.
3. Do not run `pip install -r requirements.txt`, Docker, GitHub Actions, schedulers, or notification sending unless the user explicitly requests runtime setup.
4. For analysis requests, prefer the agent-native market data skills first when they directly answer the question. Use this repo when the user wants the DSA workflow/report/dashboard or repo operation.
5. Never copy secrets from the user's real the agent config into this repo `.env` without explicit approval.

## Routing relation
- Quick individual A-share quote/K-line/fundamental data may route to Hubble skills.
- Deep single-stock A-share/UZI style research may route to `comm/uzi/deep-analysis`.
- US macro/market framework may route to `comm/day1/...`.
- Daily automated multi-market report/dashboard routes here.

## Chokepoint Watchlist Mode

When this skill is used for recurring watchlists or dashboards around AI-era industrial chains, rank candidates with the user's chokepoint framework:

```text
excess return =
  demand shock
  × insufficient supply elasticity
  × low market recognition
  × catalyst
  - valuation / liquidity / dilution / geopolitical risk
```

For each candidate, separate:
- Demand wave and architecture bottleneck.
- Whether the bottleneck cannot be designed away.
- Whether it can become material revenue for this specific company.
- Qualification-cycle evidence and timing to revenue.
- Early/small-cap advantage versus liquidity, dilution, and geopolitical risk.

Output and market-scope contract:
- First line: only the leader ticker/name list, no explanation.
- For global-stock or global industrial-chain watchlists, default to leaders outside mainland China A-shares.
- Add mainland A-shares only when the user explicitly requests A股/大陆A股/A-share coverage.

Reject or downgrade names where the product is merely useful but not scarce, the exposure is too small to move revenue, or the market already fully recognizes the bottleneck.
