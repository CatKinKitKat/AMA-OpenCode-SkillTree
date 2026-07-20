---
name: github-trending-spider
description: >
Operate or review the AI Daily Frontier / github-trending-spider project: a Python + Vue app that aggregates GitHub Trending, Hacker News, TLDR AI, V2EX, Linux.do, OpenAI, Anthropic, and InfoQ AI sources into Chinese AI/frontier summaries, JSON snapshots, a FastAPI read API, optional scheduler, optional SMTP email, and a Vue frontend. Use when the user mentions github-trending-spider, AI Daily Frontier, 每日AI前沿, AI 资讯聚合, GitHub Trending 日报, AI 新闻爬虫, or multi-source AI news digest automation.
tags: 
version: 1
---


# GitHub Trending Spider

This is a the agent wrapper for the local external source checkout:

- Source root: `~/.agent/external-repos/github-trending-spider`
- Upstream: `https://github.com/wenbochang888/github-trending-spider`
- Reviewed commit: `22d2605a2ba9d88bfcb59552af677d2e279ded5b`

## Use When

- The user asks about `github-trending-spider`, `AI Daily Frontier`, `每日AI前沿`, `AI资讯聚合`, or `GitHub Trending 日报`.
- The task is to inspect, configure, adapt, or safely run the multi-source AI news spider.
- The user wants a daily AI news digest, Chinese AI summary feed, FastAPI read API, Vue news frontend, Redis-backed snapshot cache, or optional email delivery.

## Safety Boundary

Treat this as an application repo, not a pure markdown skill.

Default safe actions:

- Read source and docs.
- Explain architecture and configuration.
- Patch source after normal repo review.
- Run offline syntax checks such as Python compile checks.

Do not run these unless the user explicitly asks for runtime bring-up and confirms scope:

- `pip install -r requirements.txt`
- `npm install`, `npm run serve`, or frontend build commands
- `python3 main.py`
- `python3 -m uvicorn api:app ...`
- `bash scripts/start_backend.sh`, `bash scripts/start_frontend.sh`, or `bash scripts/start_all.sh`
- SMTP send tests or any action with `SEND_EMAIL_ENABLED=true`
- Scheduled collection with `SPIDER_SCHEDULER_ENABLED=true`

## Runtime Risks

- Reads `GITHUB_TOKEN` for GitHub Models summaries.
- Can read SMTP variables and send email through `SMTP_USER` / `SMTP_PASSWORD`.
- Fetches external sites: GitHub Trending, Hacker News, TLDR AI, V2EX, Linux.do, OpenAI, Anthropic, and InfoQ.
- Writes logs and JSON snapshots. The default log path is `/root/logs/github-python/trending.log`, so local runs should override `LOG_FILE`.
- `scripts/start_backend.sh` installs Python dependencies, sources shell/env files, kills existing `uvicorn api:app` processes, creates `/root/logs/github-python`, and binds the backend to `0.0.0.0` by default.
- API startup can launch an in-process scheduler unless `SPIDER_SCHEDULER_ENABLED=false`.

## Safe Verification

For offline checks, prefer:

```bash
cd ~/.agent/external-repos/github-trending-spider
python3 -m py_compile main.py config.py github_trending.py hacker_news.py tldr_ai.py official_ai_sources.py content_items.py content_store.py redis_client.py scheduler.py source_registry.py api.py access_log.py email_builder.py email_sender.py
```

If checking frontend syntax without installing packages, limit yourself to file inspection unless dependencies already exist.

## Runtime Bring-Up Pattern

Only after explicit approval, use a constrained local run:

```bash
cd ~/.agent/external-repos/github-trending-spider
export LOG_FILE=/tmp/github-trending-spider.log
export OUTPUT_JSON_PATH=/tmp/github-trending-spider-latest.json
export OUTPUT_ARCHIVE_DIR=/tmp/github-trending-spider-output
export SPIDER_SCHEDULER_ENABLED=false
export SPIDER_RUN_ON_STARTUP=false
export SEND_EMAIL_ENABLED=false
python3 -m uvicorn api:app --host 127.0.0.1 --port 8000
```

For one-shot collection, confirm which external sources may be contacted and whether `GITHUB_TOKEN` should be used. Keep `SEND_EMAIL_ENABLED=false` unless email sending is the explicit task.

## Response Rules

- State whether you are doing source review, offline verification, or approved runtime execution.
- Never print token, SMTP password, or email authorization code values.
- If a secret is relevant, report only set/unset and rough length.
- Prefer local `/tmp` log/output paths for ad hoc runs.
- Preserve the repo's module boundaries: source fetching, content normalization, persistence, API, scheduler, email, and frontend are separate.
