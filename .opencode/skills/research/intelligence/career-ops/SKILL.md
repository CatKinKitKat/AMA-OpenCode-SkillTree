---
name: career-ops
description: Use when operating or reviewing santifer/career-ops, an AI job-search command center for job-offer evaluation, tailored CV/PDF generation, application tracking, portal scanning, batch processing, interview prep, and follow-up workflows.
tags: 
version: 1
---


# Career-Ops the agent Wrapper

Source repo:
- `~/.agent/external-repos/career-ops`
- Upstream: `https://github.com/santifer/career-ops`
- Reviewed commit: `4c415a9128c2ecaf2150e6e484324bc53a524dc6`

Runtime role:
- This the agent skill is a wrapper over the reviewed local source repo.
- The upstream operational skill lives at:
  - `~/.agent/external-repos/career-ops/.agents/skills/career-ops/SKILL.md`
  - mirrored variants also exist under `.opencode/skills/career-ops/` and `.qwen/skills/career-ops/`.

## Load Sequence

When the user asks to use career-ops:
1. Read the repo-local instructions:
   - `AGENTS.md`
   - `AGENTS.md`
   - `.agents/skills/career-ops/SKILL.md`
2. Read the relevant mode file under `modes/`.
3. Respect the data contract:
   - user-specific data belongs in `cv.md`, `config/profile.yml`, `modes/_profile.md`, `article-digest.md`, `portals.yml`, `data/`, `reports/`, `output/`, and `interview-prep/`.
   - do not put user-specific personalization into shared system files such as `modes/_shared.md`.
4. If using the source clone as the working app, confirm before storing personal career data under the the agent external-repo clone. Prefer a user-chosen working copy for ongoing real use.

## Safety Rules

Treat the repo as MEDIUM risk for runtime use:
- It can read `.env` / `GEMINI_API_KEY`.
- It can call Google Gemini, GitHub, and recruiting providers such as Greenhouse, Lever, Ashby, Workable, SmartRecruiters, and Recruitee.
- It can install Node dependencies and Playwright Chromium.
- It can generate PDFs, write reports and trackers, update local git state, and run batch worker flows.

Do not run these unless the user explicitly asks for runtime setup or operation:
- `npm install`
- `npx playwright install chromium`
- `npm run scan`, `node scan.mjs`, or any live portal scan
- `node gemini-eval.mjs` or any LLM/API-backed evaluation
- `node update-system.mjs apply` or `npm run update`
- dashboard, batch, cron, scheduler, browser automation, or application-submission flows

For application assistance:
- Never submit, send, or click final Apply/Submit on behalf of the user.
- Draft, fill, and prepare only. Stop for user review before final submission.
- Strongly discourage low-fit applications unless the user gives a specific override.

## Safe Default Actions

Allowed without extra approval when requested:
- Read and summarize career-ops documentation.
- Inspect local config/templates for setup status.
- Draft a setup plan.
- Generate or edit local draft/profile files after the user provides the needed career data.
- Evaluate safety and side effects of a proposed career-ops command before running it.

## Common Triggers

Use this wrapper for:
- `career-ops`
- job-search pipeline
- job offer evaluation
- CV/PDF tailoring
- ATS resume generation
- application tracker
- recruiting portal scan
- interview prep
- follow-up cadence
- 求职流水线
- 岗位评估
- 简历定制
- 招聘门户扫描
- 申请追踪
