---
name: github-issues-kanban
description: Organize GitHub Issues as a Kanban board: column labels, milestone grouping, automation with GitHub Projects, and maintaining a clean backlog. Use when the project uses Issues + Projects instead of a dedicated PM tool, or when onboarding new contributors to the issue workflow.
---
# GitHub Issues Kanban

Organize GitHub Issues as a Kanban board via labels and Projects automation.

## When to Use

- [done] Setting up a Kanban-style workflow without buying a dedicated PM tool
- [done] Labeling issues for status columns (TODO, IN PROGRESS, DONE)
- [done] Defining milestone grouping and priority ranking
- [done] Onboarding contributors to the issue workflow

## Labels convention

| Label | Meaning | Color |
|-------|---------|-------|
| `area:backend` | scope | auto |
| `area:frontend` | scope | auto |
| `area:devops` | scope | auto |
| `status:todo` | backlog | #0E8A16 |
| `status:in-progress` | active | #FBCA04 |
| `status:review` | PR/approval | #D93F0B |
| `status:done` | shipped | #0075CA |
| `p:0/p:1/p:2` | priority | critical/high/med |
| `good first issue` | new contributor | #7057FF |
| `help wanted` | community | #008672 |
| `wontfix` | closed without action | #FFFFFF |

## PR -> issue linking

```yaml
# .github/pull_request_template.md
Closes #<issue-number>
```

## Milestones

- Group issues by sprint / release window
- Use GitHub Projects (beta) for automated status tracking:
  - When PR is merged -> issue moves to `status:done`
  - When PR is labeled `status:review` -> issue moves to `status:review`

## Onboarding

New contributors:
1. Read CONTRIBUTING.md for issue labels
2. Assign yourself an issue via `/assign @me`
3. Comment on the issue: working on it, estimated completion, blockers

## Output

- Issue labeled with `area:*` and `status:todo`
- Pull request references issue with `Closes #NN`
- Kanban board visible at GitHub Projects URL
