# AMA (Amaro's Master Archive) - OpenCode Skill & Agent Tree

> **Public. AGPL-3.0. Client-neutral.** A reusable shared skill tree for OpenCode, covering engineering, security, infrastructure, governance, research, and operations.

## What this is

AMA is a shared skill and agent tree for [OpenCode](https://opencode.ai). It bundles:

- **Skills** (`SKILL.md`): reusable technology knowledge: Java, Spring Boot, OpenAPI, React, TypeScript, Kafka, Linux tuning, penetration testing, model evaluation, Gradle CI, etc.
- **Agents** (`*.md` under `.opencode/agents/`): specialized roles (backend-architect, pentest-operator, blueteam-operator, ci-cd-pipeline-agent, sysadmin-operator, test agents, etc.)
- **Commands** (`*.md` under `.opencode/commands/`): slash-commands you invoke from the OpenCode CLI (`/complete-development`, `/generate-docs`, `/security-audit`, `/triage-incident`, etc.)
- **Hooks** (under `.opencode/hooks/`): shell scripts that gate the workflow (skill lint, cleanup)
- **Documentation** (under `.opencode/docs/`): guides, architecture notes, project templates, example requirements, business-rule catalogs

## Organization principles

1. **Division-first**: every skill lives in a division/area folder (`engineering/engineering/backend/`, `security/offensive/`, etc.)
2. **Generic only**: no client, system, agency, or person identifiers. the-project / example.com placeholders
3. **Structured SKILL.md**: every skill must have `name`, `description`, Overview, When to Use, Tech Stack, Workflow, Examples, Pitfalls, References
4. **Agent-driven workflow**: skills + agents + commands + hooks compose into full deliver loops (e.g. `complete-development`)

## Divisions and areas

| Division | Area | Skills | Focus |
|----------|------|--------|-------|
| `engineering` | `engineering/backend` | 310 | Java, Spring, Go, Python, databases, APIs, finance |
| `engineering` | `engineering/frontend` | 4 | React, TypeScript, Material-UI, OpenLayers |
| `engineering` | `data-ai` | 20 | ML, PyTorch, evaluation, audiocraft |
| `engineering` | `engineering/devtooling` | 600 | CI/CD, agents, testing, Docker, Git, MCP, coding standards |
| `security` | `offensive` | 773 | Pentest, red team, AD attacks, network recon |
| `security` | `compliance` | 26 | SOC2, ISO27001, GDPR, FDA, quality audits |
| `security` | `defensive` | 3 | ZTNA, kill-switch, field operations |
| `infrastructure` | `systems` | 11 | Linux, macOS, terminal, packages |
| `infrastructure` | `cloud` | 2 | AWS, Azure architecture |
| `governance` | `methodology` | 32 | Planning, debugging, code review, verification |
| `governance` | `requirements` | 6 | Specification, clarification, validation |
| `operations` | `operations/github` | 9 | Repo management, kanban, issues, CI workflows |
| `operations` | `product` | 15 | Product management, marketing, career, business |
| `research` | `intelligence` | 73 | Deep research, OSINT, competitive analysis |
| `research` | `media` | 14 | Creative visual, content, STE100 writing |

## Agents

| Division/Area | Agent | Function |
|---------------|-------|----------|
| engineering/backend | backend-architect | Technical architecture for backend services |
| engineering/backend | backend-developer | Implementation |
| engineering/backend | backend-code-reviewer | Code review |
| engineering/backend | api-specialist | API design and contract review |
| engineering/frontend | frontend-architect | Frontend architecture |
| engineering/frontend | frontend-engineer | Implementation |
| engineering/frontend | frontend-code-reviewer | Frontend code review |
| engineering/frontend | ui-ux-designer | Design pass |
| engineering/devtooling | ci-cd-pipeline-agent | CI/CD pipelines |
| engineering/engineering/devtooling/tests | 6 test agents | Full testing loop (unit, E2E, flow, robot, req-check, test-plan) |
| security/offensive | pentest-operator | Lead penetration testing engagements |
| security/offensive | pentest-reporter | Structured pentest reports, CVSS scoring |
| security/defensive | 9 agents | AuthN/AuthZ review, architecture security, cloud security, static analysis, runtime testing, supply-chain, dependency scanning, secrets audit |
| security/compliance | security-audit-agent | Security audit across 11 domains |
| infrastructure/systems | sysadmin-operator | Day-to-day system administration |
| governance/methodology | product-owner | Requirement clarification and specification |
| governance/methodology | code-tagger | Code tagging |
| governance/methodology | skill-tree-curator | Maintain the skill tree (reorganize, audit, regenerate catalog) |
| operations | skill-curator | Browse and manage the skill catalog |
| operations | product agents | Product management, marketing, career |

## Commands

| Command | Function |
|---------|----------|
| `/complete-development <req-id>` | Full loop: clarify → specify → architect → implement → test → security → tag |
| `/curate-skills [theme]` | Browse and manage the skill catalog |
| `/generate-docs` | Auto-generate `docs/` structure from repo analysis |
| `/init-skill <theme> <name>` | Scaffold a new OpenCode skill from AMA template |
| `/security-audit [path-or-domain]` | Audit the codebase across 11 security domains |
| `/triage-incident` | Emergency incident triage: classify severity, assign owner, produce ticket |

## Hooks

| Hook | Trigger | Function |
|------|---------|----------|
| `format-skills.sh` | pre-commit | Lint SKILL.md frontmatter and section ordering |
| `cleanup-nul-files.ps1` | Windows cleanup | Remove DOS `nul` files |

## Flow reference

```text
Clarify → Specify → Architect → Implement → Test (unit+E2E) → Security → Tag
```

Use `/complete-development <req-id>` to run this loop agentically.

## Voice

AMA uses a defined writing style profile (terse, factual, no em-dashes, no semicolons in prose, tables over prose):
- Short, direct, fact-first prose
- No em-dashes in any committed markdown
- No semicolons in prose
- Tables over prose
- Evidence over assertion

## License

[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html) - copyleft, network-use clause included.
