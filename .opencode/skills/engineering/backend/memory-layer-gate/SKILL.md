---
name: memory-layer-gate
description: Route newly learned information into the right the agent layer: repo doc, skill, memory, or session_search/L4. Use when deciding where a fact, workflow, correction, or task artifact should live after execution.
tags: 
version: 1
---


Goal
- Decide the correct home for newly learned information.
- Prevent pollution of the agent long-term memory.
- Promote only verified, reusable knowledge.

Use when
- You learned something and need to decide: memory, skill, repo doc, or leave in session history.
- A task produced a new workflow, correction, rule, or project fact.
- You are about to call `memory`, `skill_manage`, or write repo governance docs.
- You are unsure whether something should stay only in `session_search` / transcripts.
- The user asks for post-session memory/skill review, session learning capture, or durable preference extraction.

Post-session review bias
- Be active, not passive: style corrections, frustration, missing workflow steps, and reusable fixes are first-class skill signals.
- Prefer patching a loaded/currently relevant skill before searching for another umbrella.
- Prefer class-level umbrella skills with rich `SKILL.md` and `references/` support files over narrow one-session skills.
- If only protected bundled or hub-installed skills would fit, do not edit them. Report `Nothing to save.`

Do not use when
- The information is obviously ephemeral and can be ignored.
- The task is trivial and produced no durable learning.

Canonical layer map
1. L0: Meta rules / hard constraints
   - Home: `AGENTS.md`, `.agent/routing/*.md`, high-priority governance skills
   - Put here when: the rule changes how the agent should operate broadly or inside a repo.
   - Examples:
     - hard safety boundary
     - mandatory routing order
     - stable repo operating rule

2. L1: Routing hints / insight index
   - Home: `.agent/routing/skill-router.md`, `.agent/routing/project-router.md`, `.agent/routing/skill-index.md`
   - Put here when: a stable trigger, route, or preference order changed.
   - Examples:
     - new skill with clear trigger
     - project-specific preferred workflow
     - new router edge like memory-layer routing

3. L2: Durable compact facts
   - Home: the agent `memory` / user profile
   - Put here when all are true:
     - stable across sessions
     - compact
     - useful without repo context
     - belongs to the user or stable environment, not project state
     - user permission allows it
   - Examples:
     - user prefers concise Chinese
     - stable OS/tooling fact
     - repeated correction to agent behavior
   - Never put here:
     - project progress
     - one-off task result
     - bulky research or docs

4. L3: Reusable workflow / SOP
   - Home: the agent skills, repo-local agent docs for project-local procedure
   - Put here when:
     - workflow succeeded and is reusable
     - trigger is clear
     - steps are non-trivial
     - will reduce future steering
   - Examples:
     - install/debug workflow
     - review/verification pipeline
     - recurring integration recipe

5. L4: Session archive / continuity
   - Home: `session_search`, transcripts, repo plans/logs/evidence
   - Default holding area for most task output.
   - Keep here when:
     - not yet verified
     - maybe useful later but not stable enough
     - task-specific continuity only
   - Examples:
     - debugging trail
     - temporary conclusions
     - partial hypotheses
     - one-session decisions

Decision procedure
1. Ask: is this a hard operating rule?
   - yes -> L0
2. Else: is this a routing/indexing rule?
   - yes -> L1
3. Else: is this a stable compact user/environment fact with permission?
   - yes -> L2
4. Else: is this a reusable verified workflow with trigger?
   - yes -> L3
5. Else -> L4 only

Promotion gate
Promote out of L4 only if at least 3 hold:
- verified by tool output or repo evidence
- reusable beyond current task
- reduces future steering
- has clear trigger or scope
- fits one target layer cleanly

Preferred actions by destination
- L0 -> patch/write repo artifact
- L1 -> patch router/index docs
- L2 -> call `memory` only if user policy allows
- L3 -> `skill_manage(create|patch)` and update router docs in same task
- L4 -> do nothing durable. Rely on `session_search` and transcript history, or write versioned plan/log if repo truth needs evidence

Heuristics
- When torn between L2 and L3, prefer L3 if it is procedure.
- When torn between L3 and L4, prefer L4 unless repeatability is proven.
- When torn between repo doc and the agent memory, prefer repo doc for project truth.
- User-specific preference -> L2 only with permission. Global playbook -> L3/L0, not L2.

Output pattern
- Destination: L0 / L1 / L2 / L3 / L4
- Why: 1-3 concrete reasons
- Action: patch doc / update router / write memory / create skill / leave in session history

Pitfalls
- Do not auto-crystallize every solved task into a skill.
- Do not save temporary task state to the agent memory.
- Do not put project facts into L2.
- Do not update router docs without a stable trigger.
- Do not create a skill before the workflow is actually verified.
- For crypto/decode sessions, do not create a narrow one-off skill from an unsolved trace. If the transform chain ran but final verification failed because parameters are missing, keep the artifact in L4 unless an existing crypto/CTF umbrella already covers it.
- For compact style/persona corrections, update the governing communication/routing skill only when a loaded or existing umbrella clearly owns that class. Otherwise prefer L2 user profile if permission allows, not a new style-only skill.

## Memory vs Tools Boundary (2026-04-24 实测教训)

**"优化记忆"只动 L2（MEMORY.md / user profile），不碰 L3/L4 资产。**

用户说"清理记忆"、"优化记忆"、"记忆太臃肿"时：
- ✓ 改 MEMORY.md（系统记忆）
- ✓ 改 user profile（用户记忆）
- ✗ 删 skills（L3: 工具，不是记忆）
- ✗ 删 cloned repos（外部依赖，不是记忆）
- ✗ 删外部工具目录

skills 和 repos 是工具层（L3），记忆是 L2。两者独立维护，互不侵入。

**L2 压缩格式：架构链**

散装条目 → 树状依赖链，token 省 70%+：

```
元：长忆从严→直做勿问→效驱>轮询→全量不挑。
├─红线：勿删cron/自动化，清前确认存废。
├─重试：始后败不重（断线除外），败即弃。
├─cron链：模型驱→禁脚本→deliver=feishu→冲突必解→sniper参数分离。
├─Hansa链：只收不挪→cron走MCP→状态机(查→sniper→pause→claim→resume)。
└─Quest链：禁Twitter→禁视频→"赚钱"=续做→"不搞了"=弃。
```

规则：
- 顶层 = 元规则（行为原则）
- ├─ = 并列分支
- └─ = 最后分支
- → = 因果/依赖链
- 每条链 ≤ 30 字
