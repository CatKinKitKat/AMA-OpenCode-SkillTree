# AGENTS.md: AMA (Amaro's Master Archive)

Guidance for the AI coding agent (OpenCode) when working in this repository.
Read it, follow it, don't make a mess.

AMA is a **public, AGPL-3.0 FOSS** shared tree of reusable agent
definitions, skills, slash-commands, and documentation templates. Built to
be community-owned, vendor- and client-neutral. No proprietary code, no
client names, no internal hostnames. I take the engineering seriously,
myself? Less so.

## What lives here

This repo is a **configuration + knowledge tree**, not an application. No
server to boot, no build to run. Just files the agent reads:

- `.opencode/agents/`: specialized subagents (engineering/backend, engineering/frontend,
  offensive security, defensive security, tests, product) as markdown files with OpenCode frontmatter.
- `.opencode/skills/`: reusable `SKILL.md` definitions (by division/area).
- `.opencode/commands/`: slash commands (e.g. `complete-development`,
  `generate-docs`, `security-audit`, `triage-incident`).
- `.opencode/docs/`: generic templates and guides for requirements,
  architecture, projects, and rules. The `docs/requirements/*` folders are
  **example/template** material showing the requirement workflow. They hold
  no real client data (every identifier was generified). Treat them like a
  cookbook, not a live ticket queue.
- `.opencode/opencode.json`: project config (permissions for optional MCP
  servers like Excalidraw).
- `.opencode/hooks/`: hook documentation (hooks live in `opencode.json`).

## How the agent tree is meant to be used

1. **Discover by convention.** OpenCode auto-discovers agents, skills, and
   commands from `.opencode/`. No hardcoded paths, no ritual.
2. **Reference skills, don't reinvent.** Task matches a stack or workflow?
   Load the `SKILL.md`, don't start from a blank page.
3. **Requirement workflow (optional).** `docs/requirements/` + the
   `complete-development` command show a full clarify → specify →
   architect → implement → test → secure → tag loop. The `RQ-*` folders
   are worked examples, not live tickets.
4. **Keep it generic.** Any example, hostname, person, org, or product
   name in this repo MUST be a placeholder (`example.com`, `the-project`,
   `the-backend`, etc.). See a real identifier? Generify it. That's the
   whole deal, don't screw it up.

## Conventions

- Agent/skill/command names are `lowercase-with-hyphens`. Boring on
  purpose.
- Subagents declare `mode: subagent` and an explicit `permission` block
  (read-only reviewers vs. write+exec implementers).
- Docs under `docs/` are written to be reusable across arbitrary projects. Don't hardcode one specific tech estate.
- Skills are organized by division > area (engineering/backend, security/offensive, etc.). See CATALOG.md.
- Temporary files made while working get deleted before you finish. The
  repository stays clean, or we're both in trouble.

## Contributing

This is a shared FOSS tree: PRs that add agents/skills/commands or
improve docs are welcome. Keep everything client-neutral and openly
licensable. Rough edges are intentional, polish is optional.
