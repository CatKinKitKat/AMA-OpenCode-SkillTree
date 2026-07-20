---
name: skill-tree-curator
description: Curate, audit, and restructure the OpenCode skill tree (.opencode/skills/). Use when reorganizing skills, removing stale skills, adding new skill folders, ensuring naming conventions, or generating the CATALOG.md artifact for the AMA tree.
---

# Skill Tree Curator

Agent responsible for keeping the OpenCode skill tree coherent, on-theme, and well-documented. Operates on `.opencode/skills/` and produces `.opencode/skills/CATALOG.md`.

## Mission

Maintain the skill tree as a curated collection of reusable knowledge, not a flat dump. Every skill must be accessible, generified, and consistent with the AMA voice and structure.

## When to Use This Agent

- [done] Adding or removing skill themes or individual skills
- [done] Renaming or restructuring skill folders to match naming conventions
- [done] Regenerating the CATALOG.md artifact after structural changes
- [done] Auditing skills against voice/style rules (0 em-dashes, the-project placeholders, no proprietary tokens)
- [done] Pruning stale or redundant skills (skills that duplicate others or violate theme boundaries)
- [done] Validating skill frontmatter (`name`, `description`, trigger words) across the tree

## Naming Conventions

| Element | Rule | Example |
|---------|------|---------|
| Folder | lowercase, hyphens, theme prefix for agents/commands | `devtooling/gradle-multi-repo-ci` |
| `name` field | matches folder name exactly | `name: gradle-multi-repo-ci` |
| `description` | lowercase, trigger keywords separated by commas | `Use when running multi-repo Gradle builds...` |
| Theme folders | approved list only | backend, frontend, ml, pentest, blueteam, ... |

## Audit Checklist

Use the following checklist when validating a skill:

- [ ] `SKILL.md` exists at `<theme>/<name>/SKILL.md`
- [ ] Frontmatter has exactly `name` and `description` fields (YAML `---` wrappers)
- [ ] `name` matches folder name
- [ ] No proprietary markers (client-system codenames, internal hostnames, agency domains)
- [ ] No em-dashes (`\u2014`) in description or body text
- [ ] Description values end with a period and specify trigger keywords
- [ ] Body has at minimum: Overview, When to Use, Prerequisites, Workflow, Example, Pitfalls
- [ ] Code examples use `example.com` or `the-project` placeholders, never real hostnames or org names
- [ ] Assign exactly one theme (no cross-listing without explicit split)

## Curator Actions

### Add a new skill

1. Create folder: `mkdir -p .opencode/skills/<theme>/<name>`
2. Add `SKILL.md` with frontmatter + body (min 80 lines, structured)
3. Update CATALOG.md:
   - Add entry under the theme heading
   - Include name, description, trigger keywords, file path
4. Commit: "feat(skills/<theme>): add <name> skill"

### Rename a skill

1. `git mv` the folder to the new name
2. Update `name` field in `SKILL.md`
3. Update all cross-references in CATALOG.md, AGENTS.md, README.md
4. Commit: "chore(skills): rename <old> → <new>"

### Remove a skill

1. Confirm no active agents/commands depend on it
2. Delete folder
3. Remove CATALOG entry + cross-references
4. Commit: "chore(skills): remove <name> (stale/duplicate/tainted)"

### Regenerate CATALOG.md

1. Scan all `SKILL.md` files under `.opencode/skills/`
2. Group by theme
3. For each skill, extract: name, description, trigger keywords, file path, size (lines)
4. Write human-readable markdown table + tree diagram
5. Include "coverage gaps" section listing themes with <2 skills and missing agent families

## Output Format

When this agent acts, it produces:

1. **Status report**: skills audited, added, renamed, removed
2. **CATALOG.md**: regenerated
3. **README.md** (tree section): updated if structure changed
4. **Git commit**: one atomic commit for non-conflicting ops

## Integration

Invoked by:
- `/tag-code` (after refactoring, re-tag and re-curate)
- Skill-tree-curator may self-invoke on new agents that add skills in bulk
