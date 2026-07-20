---
name: agent-harness-evltn
description: Evaluate external agent learning and memory harnesses from code before installing; verify host coupling, enforcement reality, forgetting semantics, and safe adopt-vs-adapt recommendation.
tags: 
when_to_use: 
version: 1
---


Goal
- Produce a grounded judgment from code, not README vibes.
- Decide among: install directly, clone for study, or selectively absorb ideas.

Steps
1. Read the upstream README first.
   - Capture stated claims: learning loop, forgetting, self-protection, install target, dependencies, evaluation guarantees.
   - Note explicit numbers and defaults.

2. Clone or inspect the repo code before recommending installation.
   - Read installer/setup entrypoint first.
   - Read `.env.example`, startup validators, and packaged-config writers early when present.
   - Verify host coupling:
     - Which product it edits (`~/.opencode/settings.json`, shell rc, cron, etc.)
     - Whether it is actually agent-agnostic or tied to one host.
     - Whether README "local-first" claims still hide hosted auth, control-plane, or remote bootstrap dependencies.

3. Inspect the core enforcement files, not just docs.
   - Read at least:
     - install/setup script
     - self-protection hook / guard
     - lesson distillation / memory write path
     - forgetting / pruning implementation
   - Check whether “immutable” means OS-level immutability or merely path blocking inside hooks.
   - Check whether “learning is code-enforced” only covers capture, while lesson content still depends on an LLM.

4. Compare README claims against code.
   - Flag drift explicitly when found.
   - Common checks:
     - README says stale after 37 days but code default is 30
     - README says agent-agnostic but installer edits only the coding agent config
     - README claims weekly lint / active forgetting but prune is only partial marking or depends on external scheduling

5. Judge adoption in four buckets.
   - Host compatibility: safe to install in current environment?
   - Safety model: what is actually protected?
   - Memory quality: does it dedup, decay, validate, and recover from bad lessons?
   - Integration risk: will it conflict with existing memory/skill systems?

6. Recommend one of three outcomes.
   - Install directly: only if host coupling matches current stack and side effects are acceptable.
   - Clone for study only: if promising but too coupled or unverified.
   - Selectively absorb: adopt the mechanisms, not the whole product.

Output pattern
- Verdict: learn / clone / install / selectively absorb.
- Strengths: 3-6 concrete points.
- Hard limits: 3-6 concrete points, each tied to code.
- Why not install: mention exact side effects.
- What to absorb: list mechanisms worth porting.
- What not to absorb: list repo-specific or overclaimed parts.

High-value findings to look for
- Installer writes into host-specific config files.
- “Immutable” protection is only implemented as a write-path denylist.
- Distillation still relies on an LLM CLI, so correctness is not independently guaranteed.
- Forgetting exists, but only as stale tagging / heuristic pruning, not robust verification.
- README-to-code drift is itself a trust signal.

Pitfalls
- Do not judge from README alone.
- Do not recommend direct install before reading installer side effects.
- Do not treat “hook-based” as equivalent to “can’t be bypassed” without checking actual enforcement scope.
- Do not ignore conflict risk with existing memory/skill systems.

Minimal command pattern
- Fetch README.
- Clone repo to a temp path.
- Read install/setup script.
- Read protection hook.
- Read distillation path.
- Read forgetting/pruning implementation.
- Then decide install vs adapt.
