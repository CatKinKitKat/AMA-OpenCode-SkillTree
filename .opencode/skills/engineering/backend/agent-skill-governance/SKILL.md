---
name: agent-skill-gov
description: >
tags: 
version: 1
---


Goal
- Keep the agent skills reliable, cheap, and worth invoking.
- Borrow OpenSpace's lifecycle idea without importing its whole platform.

Core policy
Classify each actively used skill into 3 buckets:
1. Bad
   - Symptoms: repeated failure, stale commands, missing prerequisites, user correction, tool misuse, or harmful token waste.
   - Action: patch immediately or stop using until fixed.
2. Middling
   - Symptoms: works sometimes, but outputs are noisy, too long, brittle, or missing key checks.
   - Action: improve incrementally after real use.
3. Good
   - Symptoms: triggers correctly, reduces work, survives repeated use, and produces clean results.
   - Action: freeze behavior except for compatibility fixes.

Signals to track
- Trigger quality: did the skill activate when it should?
- Execution quality: did it reduce steps or token use?
- Reliability: did commands actually work in this environment?
- Correction rate: did the user or tool output expose gaps?
- Drift: did upstream docs/tools/API change?

Repair loop for bad skills
1. Reproduce the failure.
2. Identify the exact stale or missing instruction.
3. Patch the skill immediately.
4. Re-run the smallest verification that proves the fix.
5. Keep the patch small unless the structure is fundamentally wrong.

Improvement loop for middling skills
1. Keep using the skill.
2. After each substantial use, ask:
   - what step was missing?
   - what warning should have been earlier?
   - what can become a reusable check/template/script?
3. Patch only the parts that improved real execution.
4. Avoid expanding prose unless it changes behavior.

Freeze rule for good skills
- Do not rewrite a good skill just to make it prettier.
- Only touch it for:
  - broken commands
  - changed upstream interfaces
  - proven missing constraints

When to create a new skill
- Workflow repeated successfully more than once.
- 5+ tool calls with non-trivial judgment.
- Clear trigger conditions exist.
- It would save future user steering.

When not to create one
- One-off work.
- Pure reference dumping.
- Environment too unstable to encode safely.

Minimal review cadence
- On every significant skill use: micro-review.
- On every failure caused by stale instructions: immediate patch.
- On repeated success across sessions: consider freezing and avoiding churn.

Output pattern
- Skill status: bad / middling / good.
- Reason in 1-3 concrete points.
- Action: patch / keep improving / freeze.


Security interaction
- Before adopting or patching any externally sourced skill or workflow, run `agent-runtime-sec-review` or apply its equivalent review logic first.
