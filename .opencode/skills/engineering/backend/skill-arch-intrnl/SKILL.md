---
name: skill-arch-intrnl
description: >
tags: 
version: 1
---


Goal
- Internalize the useful parts of skill-based architecture without cargo-culting its repo.
- Keep user-facing responses short while making agent-facing docs easier to trigger, route, and maintain.

Use this when
- AGENTS.md or a skill file is getting too large.
- Rules are duplicated across entry files.
- A project has recurring costly mistakes not surfacing during execution.
- A repo needs clearer routing from task -> reads -> workflow.

Do not use this when
- The project is tiny and a single short SKILL.md is enough.
- There are no duplicated rules and no repeated gotchas.

Core pattern
1. Keep entry files thin.
   - AGENTS.md, AGENTS.md, CODEX.md should contain only the minimum hard rules plus a compact routing table.
2. Separate concerns.
   - `rules/` = stable constraints.
   - `workflows/` = procedures.
   - `references/` = background, architecture, pitfall indexes.
3. Make descriptions triggerable.
   - Skill `description` should contain explicit activation phrases and conditions, not passive summaries.
4. Surface costly gotchas.
   - If a pitfall is expensive and recurrent, do not leave it only in `references/`. Add it to workflow checks or concise rules.
5. Run a task-closure scan for non-trivial work.
   - Ask: new pattern? new pitfall? missing rule? stale rule?
6. Record sparingly.
   - Only formalize lessons that meet at least 2 of 3:
     - repeatable
     - costly
     - not obvious from code

Recommended structure
- `skills/<name>/SKILL.md`
- `skills/<name>/rules/`
- `skills/<name>/workflows/`
- `skills/<name>/references/`
- optional templates/scripts only when they remove repeated setup cost

Practical migration steps
1. Audit current agent-facing docs.
2. Identify duplicate rules and repeated failure points.
3. Move durable constraints into `rules/`.
4. Move step-by-step procedures into `workflows/`.
5. Keep only routing and priority in the top-level SKILL.md or AGENTS.md.
6. Verify trigger descriptions are explicit.
7. Add one concise gotcha surface in the workflow path for common costly errors.

Output pattern
- State whether to keep single-file docs or split.
- If splitting, name the exact files to create.
- List 2-5 high-value gotchas to surface.
- Give one routing table if entry files are being rewritten.

Pitfalls
- Do not split purely because of line count.
- Do not copy full external templates unless they save real effort.
- Do not bury important lessons in references only.
- Do not leave vague skill descriptions that never trigger.
