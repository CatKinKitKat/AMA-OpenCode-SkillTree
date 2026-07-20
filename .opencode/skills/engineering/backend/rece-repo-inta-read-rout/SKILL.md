---
name: rece-repo-inta-read-rout
description: >
tags: 
version: 1
---


Goal
- Turn a batch of newly cloned local repos into one of three outcomes per repo:
  1. install and verify
  2. study and extract principles
  3. absorb reusable patterns into the agent/project docs
- Prefer README-grounded decisions over guessing from repo name.

Use this when
- User says repos were already cloned locally.
- User wants triage by recency/creation time.
- User explicitly says to decide via README whether to learn, install, or "absorb".

Do not use this when
- The user names one exact repo and wants implementation inside it.
- The task is a formal security review of a foreign repo. Route security review first.

Workflow
1. Route first.
   - Read `.agent/routing/skill-router.md`.
   - If operating under `~`, also read `.agent/routing/project-router.md`.
   - Check nearest `AGENTS.md` / `AGENTS.md` for any repo you actually enter.

2. Find candidate repos by local filesystem birth time.
   - Under `~`, list directories containing `.git`.
   - Sort by `st_birthtime` on macOS. Fall back to `st_ctime` if birth time missing.
   - Start from newest first.
   - Do not assume the most recent repos are the only relevant ones. Inspect several.

3. Read the real docs before deciding.
   - For each candidate repo, locate `README*` first.
   - Also locate `AGENTS.md`, `AGENTS.md`, `docs/*`, or packaged skill files if present.
   - Base the decision on documented install path, purpose, constraints, and reusable ideas.

4. Classify each repo.
   - Install: if the repo is an executable tool/library likely useful now and install steps are clear.
   - Learn: if it is mainly a reference architecture, workflow pattern, or research scaffold.
   - Absorb: if specific ideas should be transferred into the agent docs, routing, memory model, provenance rules, or skills.
   - A repo may be both Learn + Absorb, or Install + Absorb.

5. Install pragmatically, not mechanically.
   - Verify runtime prerequisites from live system, not memory.
   - Example checks: `python3 --version`, `uv --version`, `node --version`, `npm --version`.
   - For Node repos, also check whether multiple major versions are installed (`brew list --versions node node@20 node@22 || true` on macOS is often enough).
   - If native Node addons fail during install under a bleeding-edge Node (common with `tree-sitter`), retry with the repo's documented floor or an LTS major that matches the toolchain. On macOS/Homebrew, prefer a scoped PATH such as `export PATH=/opt/homebrew/opt/node@20/bin:$PATH` instead of mutating the global default.
   - If `pnpm` is missing but `npm` exists, a low-privilege fallback is `npm_config_prefix=$HOME/.npm-global npm install -g pnpm@<version>`. Then prepend `$HOME/.npm-global/bin` to PATH for the task.
   - If project requires newer Python than system default, use `uv python list` and a repo-local venv with the matching interpreter.
   - Do not assume `pip install -e .` is sufficient. Compare with README extras such as `.[mcp]`.
   - After install, run a minimal verification command from the README or package entrypoint.

6. Expect doc/runtime mismatch.
   - If install succeeds but runtime fails on a missing dependency, inspect the traceback.
   - Reconcile with README/dependency metadata.
   - Common pattern: plain editable install omits optional extras needed by runtime. Install the missing package or the documented extra, then rerun verification.
   - Another common pattern: README says the app is local-first, but code review reveals optional network telemetry, hosted LLM calls, packaged build paths that fail on native `.node` modules, or startup validators that still require remote auth/control-plane URLs. Inspect telemetry/service code, `.env.example`, startup validators, and distributable build scripts before calling the repo production-ready.
   - Another common pattern: mock/test mode still pulls remote tokenizer/model assets on first use. Search embedding/tokenizer/bootstrap code before claiming a repo is fully offline-verifiable.
   - Record the mismatch in the final notes.

7. For skill-packaged repos, verify the skill surface.
   - Search for local `SKILL.md`, `.agents/skills/`, `skills/README.md`, or equivalent.
   - If README advertises `npx skills add ...`, verify locally first when possible.
   - If remote listing via `npx skills add ... --list` times out, do not block the whole task. Use local repo evidence if available and note the timeout explicitly.
   - For skill-OS / agent-runtime repos (e.g. Vibe-Skills/VCO), inspect host-root writes (`~/.codex`, `~/.the agent`, `.vibeskills`), promotion/freeze/destructive gates, replay ledgers, proof bundles, and workspace-memory planes before any install. Default to Learn + Absorb, then encode the useful governance as the agent skill/routing/test artifacts rather than installing a second runtime authority.

8. Extract principles, not stacks.
   - Write down reusable patterns in neutral form, e.g.:
     - loop until done
     - disk as state, git as memory
     - provenance sidecar for research outputs
     - fresh vs persistent memory modes for iterative skill evolution
     - typed file handles for large-context workflows
   - Avoid cargo-culting repo-specific framework choices unless the user asks.

9. Persist the intake summary in project docs, not long-term memory.
   - Write a timestamped note into a local knowledge repo such as `~/context-hub/`.
   - Include: repo path, disposition (install/learn/absorb), commands run, failures, fixes, and extracted principles.
   - Keep long-term memory for user preferences only, not per-repo details.

10. Final report format.
   - One short line per repo: installed / learned / absorbed.
   - Mention exact verified path or command only when useful.
   - Mention blockers crisply.

Heuristics
- Install tools that add concrete leverage now.
- Learn from orchestration, memory, provenance, and agent architecture repos even if not installed.
- Absorb only the ideas that change the agent behavior boundaries or reduce future steering.

Pitfalls
- Do not decide from repo names alone.
- Do not skip README just because a repo looks familiar.
- Do not trust system Python version. Check live.
- Do not stop at first install failure. Pivot to uv/local venv/system-level path as needed.
- Do not save repo-specific outcomes into durable memory.
- Do not hide timeouts or verification gaps.

Example outcome types
- `token-savior` style repo: install + verify + note optional runtime deps.
- orchestration repo: learn + absorb workflow principles.
- packaged skill repo: verify local skill files. Remote install check optional if flaky.
