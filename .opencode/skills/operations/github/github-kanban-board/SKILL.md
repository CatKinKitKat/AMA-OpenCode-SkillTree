---
name: github-kanban-board
description: Maintain a GitHub Projects (beta) Kanban board for a team or OSS repo. Use when managing backlog, sprint rotation, or release planning via GitHub Projects instead of an external tool.
---
# GitHub Projects Kanban Board

Maintain a GitHub Projects Kanban board for sprint or release planning.

## When to Use

- [done] Setting up a project board for a team or OSS repo
- [done] Managing sprint rotation (backlog -> todo -> doing -> review -> done)
- [done] Release planning (group issues by milestone)
- [done] Tracking team capacity and blockers

## Columns (default)

| Column | Rules | Owner |
|--------|-------|-------|
| Backlog | status:todo, no assignee | PM |
| Ready | status:todo + assignee | - |
| In Progress | status:in-progress | Engineer |
| Review | status:review | Reviewer |
| Done | status:done | PM to verify |

## Views

- Board view: Kanban (default for stakeholders)
- Table view: for bulk triage and sorting
- Roadmap view: for release milestones (quarterly)

## Automation

GitHub Projects automation (Workflows tab):
- When item added to Backlog -> set status:todo label
- When PR links to issue -> move to Review
- When PR is merged -> move to Done
- When issue closed without PR -> add label `wontfix`

## Output

- Project board URL: `https://github.com/users/<org>/projects/<id>`
- Issues linked via `Closes #NN`
- Milestones linked to quarter columns

## Card metadata

Required per card:
- linked issue (url)
- assignee
- milestone
- estimate (optional)

## Field configuration

| Field | Type | Use |
|-------|------|-----|
| status | Single select | To Do / In Progress / Review / Done |
| area | Single select | Backend / Frontend / Devops / Docs |
| estimate | Number | Story points |
| sprint | Text | Quarter or sprint ID |

## Reporting

Weekly export: `gh project field-list <project-id> --format json` -> `projects/report.md`
