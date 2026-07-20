---
name: fres-cont-loop-runn
description: >
tags: 
version: 1
---


# Fresh Context Loop Runner

Goal
- Execute long implementation work as small resumable loops.
- Keep the orchestrator thin. Let each fresh agent do the real work.
- Persist state on disk so context loss is survivable.

Use this when
- 用户要“自主循环推进”“一直做直到完成”“分小步反复推进”“断点续跑”“每轮重新读状态”“像 Ralph 那样跑”。
- 用户明确嫌大上下文臃肿，希望把任务切成小验收单元。
- 任务可拆成小步，且至少有一个可执行验证命令。

Do not use this when
- The task is a simple one-shot edit.
- There is no clear stop condition.
- There is no rollback path.
- The user asked for pure planning only. Route to `plan` or `/plan` instead.

Core pattern
1. State lives on disk.
   - `.agent-loop/tasks.json` or project-native equivalent tracks work items.
   - `.agent-loop/progress.md` records durable learnings and gotchas.
   - `.agent-loop/loop.lock` records active loop identity if a long loop is running.
2. Git is memory.
   - Start from a clean or understood worktree.
   - Commit or snapshot after a verified work item.
   - Do not stack fixes on top of a known-bad attempt.
3. Fresh context is reliability.
   - Each iteration re-reads task state, relevant docs, changed files, and verification output.
   - Do not rely on chat memory for completion state.
4. Backpressure beats prescription.
   - Give agents success criteria and gates, not giant step scripts.
   - Gates: tests, typecheck, lint, build, browser verification, review checklist.
5. Small work items only.
   - Each item should fit in one context window and one verification loop.
   - Split anything that smells like "build the whole dashboard".

Minimal state schema
```json
{
  "objective": "short goal",
  "verify": ["command 1", "command 2"],
  "items": [
    {
      "id": "T1",
      "title": "small deliverable",
      "acceptance": ["observable criterion"],
      "status": "pending|in_progress|done|blocked",
      "notes": "compact handoff note"
    }
  ]
}
```

Loop procedure
1. Inspect repo docs and nearest agent docs.
2. Create or update `.agent-loop/tasks.json` with small items.
3. For each iteration:
   - read `.agent-loop/tasks.json`, `.agent-loop/progress.md`, recent git log, and current diff
   - choose the highest-priority pending or blocked item that is now actionable
   - make the smallest change that satisfies one item
   - run verification commands
   - if pass: mark item done, append progress note, commit/snapshot if appropriate
   - if fail: record blocker and exact failing evidence. Either fix once or mark blocked
4. Stop when all items are done, verification passes, or a real blocker is recorded.

the agent execution options
- For current-session loops, use normal tools and keep state files updated.
- For long-running background loops, route to `/background <self-contained prompt>` when available.
- For independent fresh agents, spawn `agent chat -q '<self-contained iteration prompt>'` or use `delegate_task` for bounded subtasks.
- Use worktrees for parallel loops that edit code.

Self-contained iteration prompt template
```text
Workdir: <repo>
Read first: local agent docs, .agent-loop/tasks.json, .agent-loop/progress.md, git diff, git log -5.
Pick exactly one pending task.
Make the smallest change.
Run: <verify commands>.
Update .agent-loop/tasks.json and .agent-loop/progress.md.
Stop after one task or one blocker. Report changed files and verification result.
```

Verification
- A task is not done until its acceptance criteria and repo checks pass.
- For UI tasks, include browser verification when available.
- If checks are slow, run the narrow check first, then broad check before final.

Pitfalls
- Do not turn the loop runner into a second platform.
- Do not add complex retry policy. Fresh context plus state files handles most recovery.
- Do not let multiple loops edit the same files without worktree or lock discipline.
- Do not update global memory with loop progress. Use repo state files.
- Do not mark done from natural language alone. Require proof bundle or command output.
