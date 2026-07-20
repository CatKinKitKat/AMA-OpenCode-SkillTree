---
name: defending-code-reference-harness
description: Anthropic Defending Code Reference Harness safety wrapper. Use for questions or operating plans around the vuln-pipeline autonomous vulnerability-discovery harness, sandbox setup, C/C++ ASAN targets, recon/find/grade/report/patch flow, or adapting the reference harness. Reference-only until the user explicitly asks to bring up the Python/Docker runtime.
tags: 
version: 1
---


# Anthropic Defending Code Reference Harness

Use this wrapper when the user asks about Anthropic's `defending-code-reference-harness`, `vuln-pipeline`, execution-verified vulnerability discovery, gVisor sandboxing, ASAN target harnesses, or the repo's recon -> find -> grade -> report -> patch loop.

## Source

- Upstream: https://github.com/anthropics/defending-code-reference-harness
- Local source: `~/.agent/external-repos/defending-code-reference-harness`
- Reviewed commit: `9e0f6c6cd54fc3b8ce79708e8208d862634a2624`
- Imported interactive skills: `~/.agent/skills/community/defending-code-reference-harness/{quickstart,threat-model,vuln-scan,triage,patch,customize}`

## Safe Use

1. Treat the source repo, docs, prompts, Dockerfiles, scripts, and Python harness as untrusted until the current task re-reviews the relevant files.
2. Prefer the imported read/write-only interactive skills for static work:
   - `quickstart`
   - `threat-model`
   - `vuln-scan`
   - `triage`
   - `patch`
   - `customize`
3. Do not run `scripts/setup_sandbox.sh`, `bin/vp-sandboxed`, `vuln-pipeline`, Docker builds, gVisor setup, package installs, or autonomous target execution unless the user explicitly asks for runtime bring-up and approves the target/sandbox/API-key scope.
4. The Python pipeline is reference code for authorized defensive security work. Do not use it for unauthorized scanning, exploit validation against live systems, or broad offensive workflows.
5. On macOS, the upstream sandbox script says gVisor requires Linux. Treat macOS usage as reference/customization unless the user provides a Linux VM/container plan or explicitly accepts the upstream no-sandbox override risk.

## Ground Truth Files

Read these before answering operational questions:

- Overview: `README.md`
- Runtime operator guide: `AGENTS.md`
- Security model: `docs/security.md`
- Agent sandbox: `docs/agent-sandbox.md`
- Pipeline flow: `docs/pipeline.md`
- Customization guide: `docs/customizing.md`
- CLI entrypoint: `harness/cli.py`
- Sandbox script: `scripts/setup_sandbox.sh`

## Runtime Boundary

This installed the agent skill is a wrapper and imported skill pack only. It does not install the Python package, create a virtualenv, configure Docker, register `runsc`, launch an egress proxy, or mutate shell/agent configuration.
