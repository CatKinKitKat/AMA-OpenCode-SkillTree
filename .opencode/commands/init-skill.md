---
description: Initialize a new OpenCode skill with boilerplate, validation, and a themed prompt.
agent: build
model: sonnet
---
# Initialize Skill

Create a new OpenCode skill from template, with validation, autocorrect for the AMA tree, and a division/area-scoped prompt from the CATALOG.

## Usage

```
/init-skill <division> <area> <name>
/init-skill engineering backend vllm
/init-skill security offensive godmode
/init-skill operations product marketing
```

## Parameters

- `division`: one of: `engineering`, `security`, `infrastructure`, `governance`, `operations`, `research`
- `area`: one of the areas under the chosen division
- `name`: lowercase, hyphens, matches folder name (e.g. `spring-boot-kotlin-modulith`, `pentest-egress`)

## Division/Area Map

| Division | Areas |
|----------|-------|
| `engineering` | `engineering/backend`, `engineering/frontend`, `data-ai`, `engineering/devtooling` |
| `security` | `offensive`, `compliance`, `defensive` |
| `infrastructure` | `systems`, `cloud` |
| `governance` | `methodology`, `requirements` |
| `operations` | `operations/github`, `product` |
| `research` | `intelligence`, `media` |

## Workflow

1. Validate division against approved list
2. Validate area against the division's approved areas
3. Validate name (lowercase, hyphens, no spaces, match folder)
4. Check for duplicate: if `.opencode/skills/<division>/<area>/<name>/SKILL.md` already exists, abort with suggestion
5. Create folder structure:

   ```
   .opencode/skills/<division>/<area>/<name>/
   └── SKILL.md
   ```

6. Write SKILL.md with boilerplate:

   ```yaml
   ---
   name: <name>
   description: <one-line summary, trigger-words separated by commas>. Use when ...
   ---
   
   > Transposed from [source name if applicable].
   > Licensed under AGPL-3.0-or-later.
   
   # <Title>
   
   ## Overview
   
   1-3 sentences on what this skill teaches.
   
   ## When to Use This Skill
   
   - [done] concrete trigger 1
   - [done] concrete trigger 2
   - [done] concrete trigger 3
   
   ## Prerequisites / Tech Stack
   
   list tools, languages, versions
   
   ## Workflow / Steps
   
   numbered or bullet steps the agent follows
   
   ## Examples
   
   short code/config snippet
   
   ## Common Pitfalls / Best Practices
   
   what to avoid, what to prefer
   
   ## References
   
   AMA style guide: terse, factual, no em-dashes, tables over prose (see docs/overview.md)
   ```

7. Update `.opencode/skills/CATALOG.md`: add new entry under the division/area heading
8. Update `README.md` skills section if tree diagram is present
9. Commit: `feat(skills/<division>/<area>): add <name> skill`

## Validation Rules

- `name` must match folder exactly (enforced at creation time)
- `description` must be lowercase and end with a period
- Trigger keywords must be concrete (not generic like "when working with code")
- Body must include the 6 required sections (Overview / When to Use / Prerequisites / Workflow / Examples / Pitfalls / References)

## After Creation

Use `/generate-docs` to scaffold documentation at the project root if the skill needs a companion `docs/` reference. Use `skill-curator` agent after adding multiple skills to regenerate the catalog.
