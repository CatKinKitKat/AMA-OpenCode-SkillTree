---
name: decision-surface-layer
description: >
tags: 
version: 1
---


# Decision Surface Layer

Goal
- Separate decision policy from execution instructions.
- Make preferences, weights, and hard constraints explicit and editable.
- Let execution agents consume structured decision signals instead of hidden prompt soup.

Use this when
- 用户说“先定取舍”“先做决策层”“把偏好/约束写清楚”“不要藏在提示词里”“按权重选方案”“硬约束不能破”。
- 多个方案都可行，但需要按目标、偏好、风险、成本、维护性打分选择。
- 某些偏好或 veto 规则会反复影响后续执行。
- 工作流需要先回答“下一步该做什么，为什么”，再派执行代理。

Do not use this when
- The task is a one-off with obvious acceptance criteria.
- The user does not need persistent or explicit tradeoff control.

Core idea
- Keep a compact decision artifact near the work.
- Execution reads it as policy input, not as freeform instruction authority.
- Separate three layers:
  1. objective
  2. weighted preferences
  3. hard constraints

Recommended artifact
- `decision.md` or project-local equivalent.

Suggested structure
```markdown
# Decision Surface

## Primary Objective
- <dominant optimization direction>

## Preferences / Weights
- speed: 0.4
- simplicity: 0.3
- maintainability: 0.2
- novelty: 0.1

## Hard Constraints
- no new dependencies
- do not modify public API
- must pass existing tests

## Tradeoff Rules
- if gains are small, prefer simpler diff
- if performance and readability conflict, keep readability unless >15% speedup

## Out of Scope
- <areas not to optimize>
```

How to use it
1. Read the decision surface before planning or implementation.
2. Translate it into candidate evaluation rules.
3. Use constraints as vetoes, not suggestions.
4. Use weights only when multiple valid paths remain.
5. If the user changes priorities, update the decision surface first.

the agent adaptation
- Good home: repo artifact, skill input, or local workflow file.
- Do not store detailed decision policy in the agent long-term memory.
- Prefer referencing the file from plans, loops, and implementation prompts.
- Combine well with `fres-cont-loop-runn` and `auto-research`.

Good uses
- feature prioritization
- implementation path selection
- optimization under constraints
- repeated human+agent collaboration with stable preferences

Pitfalls
- Do not let the file become a giant prompt dump.
- Do not mix runtime logs into the decision surface.
- Do not treat preferences as hard constraints unless explicitly marked.
- Do not hide key vetoes only in chat if they should govern future execution.
