# Getting Started

This is a generic guide for working inside the AMA tree. It names no
client, system, or person.

## Prereqs

- [OpenCode](https://opencode.ai) installed.
- A terminal and `git`.

## Open the project

```bash
cd AMA-OpenCode-SkillTree
opencode .
```

OpenCode auto-discovers `.opencode/` from the project root.

## Common first tasks

- **Add a skill:** drop a folder under `.opencode/skills/<theme>/<name>/`
  with a `SKILL.md`.
- **Add an agent:** add a markdown file under `.opencode/agents/<area>/`.
- **Run a command:** `/complete-development <req-id>`.
- **Generate docs:** `/generate-docs`.

## Keeping it clean

Before any commit, scrub real identifiers. The `skill-tree-curator`
agent can audit a change for leaks (client names, people, internal
hosts, secrets).
