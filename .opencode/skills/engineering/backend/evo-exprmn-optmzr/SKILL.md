---
name: evo-exprmn-optmzr
description: Convert evo's experiment-tree optimization model into a the agent-native workflow for benchmark-driven code evolution using git worktrees, scored experiments, gates, traces, and iterative branching.
version: 1
---


Goal
- Let the agent run evo-style optimization without requiring the coding agent plugin surfaces.
- Use repo-local git worktrees as experiment branches.
- Keep only changes that improve a measurable benchmark and pass gates.
- Preserve traces, diffs, and branch history for later inspection.

Use when
- User wants benchmark-driven autonomous improvement.
- A repo has a clear target file/module and a benchmark command that emits a parsable score.
- The task benefits from branching search instead of one linear edit loop.
- You want the agent to explore multiple hypotheses with rollback discipline.

Do not use when
- There is no executable benchmark.
- Success is subjective and cannot be scored.
- The repo is too dirty to establish a clean baseline.

Core model absorbed from evo
- Workspace init with explicit target, benchmark, metric, optional gate.
- Each experiment gets its own git worktree from a parent node.
- Benchmark output is parsed into a numeric score.
- Candidate is kept only if score improves over parent and gates pass.
- Failed branches are discarded. Good branches become new parents.
- Traces, diff, and notes are saved per experiment.
- Prefer shallow tree search over blind repeated edits on one branch.

the agent-native workflow
1. Preconditions
   - Verify repo is git-controlled and clean enough to branch.
   - Verify benchmark command runs from repo root.
   - Verify score extraction rule before any code edits.
   - Verify any required gate commands.

2. Define experiment contract in chat or repo note
   - target path(s)
   - benchmark command
   - metric direction: max or min
   - gate command(s)
   - score parse rule
   - budget: number of branches / rounds

3. Create baseline
   - Run benchmark on current branch.
   - Save score and command output.
   - Treat this as root parent.

4. Branch experiments with worktrees
   - For each hypothesis, create a git worktree on a branch like `evo/<topic>/<n>`.
   - Make one focused change per branch.
   - Run benchmark.
   - Run gates.
   - Save benchmark output, gate output, diff, and short hypothesis note.

5. Keep or discard
   - If score improves and gates pass: keep branch as candidate parent.
   - Else: discard branch or leave as explicit failed trace if user wants auditability.

6. Iterate
   - Spawn more experiments from the best surviving parent.
   - Use traces from failed runs to propose new hypotheses.
   - Stop on budget exhaustion, stall, or user interrupt.

7. Finalize
   - Report best branch, best score delta, and gate status.
   - Present exact diff or commit for human decision.
   - Clean stale worktrees if user scope permits.

Suggested repo artifact layout
- `.agent/evo/<run-id>/baseline.log`
- `.agent/evo/<run-id>/experiments/<exp-id>/benchmark.log`
- `.agent/evo/<run-id>/experiments/<exp-id>/gate.log`
- `.agent/evo/<run-id>/experiments/<exp-id>/diff.patch`
- `.agent/evo/<run-id>/experiments/<exp-id>/notes.md`
- `.agent/evo/<run-id>/summary.md`

Recommended commands
- baseline: use `terminal()` from repo root
- branches/worktrees: `git worktree add ...`
- diff capture: `git diff <parent>...<branch>`
- traces/logs: write to repo-local files, not memory

Score parsing
- Prefer benchmark commands that print one numeric score plainly.
- If output is noisy, extract with a stable regex or small Python parser via `execute_code`.
- Never guess score direction. Make max/min explicit.

Gates
- Gates are pass/fail safety rails separate from benchmark score.
- Typical gates: tests, lint, typecheck, smoke run, invariant checks.
- A higher score that fails a gate is rejected.

Heuristics
- Change one variable per branch when possible.
- Keep hypotheses short and falsifiable.
- Prefer 2-5 high-signal branches over many low-quality ones.
- If benchmark is slow, reduce branch fanout and increase hypothesis quality.
- Use delegate_task only when the user already approved a multi-branch coding run and subtasks are independent.

Pitfalls
- Do not start before baseline is reproducible.
- Do not compare scores across changed benchmark definitions.
- Do not keep ungated wins.
- Do not let multiple branches edit overlapping files without clear isolation.
- Do not store experiment state only in chat. Keep repo-local artifacts.

Output pattern
- baseline score
- best branch
- score delta
- gate result
- kept vs discarded branches
- next best experiment directions
