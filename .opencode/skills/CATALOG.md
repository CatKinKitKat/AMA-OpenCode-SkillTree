# AMA Skills Catalog

> Generic OpenCode skills for the AMA (OpenCode Skill & Agent Tree).
> Organized by corporate divisional structure: division > area > skill.
> All proprietary codenames have been generified.

## Divisions and Areas

| Division | Area | Skills |
|----------|------|--------|
| `engineering` | `backend` | 310 |
| `engineering` | `data-ai` | 20 |
| `engineering` | `devtooling` | 600 |
| `engineering` | `frontend` | 4 |
| `governance` | `methodology` | 32 |
| `governance` | `requirements` | 6 |
| `infrastructure` | `cloud` | 2 |
| `infrastructure` | `systems` | 11 |
| `operations` | `github` | 9 |
| `operations` | `product` | 15 |
| `research` | `intelligence` | 73 |
| `research` | `media` | 14 |
| `security` | `compliance` | 27 |
| `security` | `defensive` | 3 |
| `security` | `offensive` | 773 |

## Tree

```
engineering/
  backend/               310 skills: Java, Spring, Go, Python, databases, APIs, finance
  data-ai/                20 skills: ML, PyTorch, evaluation, audiocraft
  devtooling/            600 skills: CI/CD, agents, testing, Docker, Git, MCP, standards
  frontend/                4 skills: React, TypeScript, UI frameworks

governance/
  methodology/            32 skills: planning, debugging, code review, verification
  requirements/            6 skills: specification, clarification, validation

infrastructure/
  cloud/                   2 skills: AWS, Azure architecture
  systems/                11 skills: Linux, macOS, terminal, packages

operations/
  github/                  9 skills: repo management, kanban, issues, CI workflows
  product/                15 skills: product management, marketing, career, business

research/
  intelligence/           73 skills: deep research, OSINT, competitive analysis
  media/                  14 skills: creative visual, content, STE100 writing

security/
  compliance/             27 skills: SOC2, ISO27001, GDPR, FDA, regulatory, quality, license audit
  defensive/               3 skills: ZTNA, kill-switch, field operations
  offensive/             773 skills: pentest, red team, AD attacks, network recon
```

## Agents (34)

| Division/Area | Agents |
|---------------|--------|
| engineering/backend | backend-architect, backend-developer, backend-code-reviewer, api-specialist |
| engineering/devtooling | ci-cd-pipeline-agent |
| engineering/devtooling/tests | flow-test-logger, flow-test, robot-tester, unit-test-generator, req-checker, test-plan |
| engineering/frontend | frontend-architect, frontend-code-reviewer, frontend-engineer, ui-ux-designer |
| governance/methodology | product-owner, skill-tree-curator, code-tagger |
| infrastructure/systems | sysadmin-operator |
| operations | skill-curator |
| security/compliance | security-audit-agent |
| security/defensive | blueteam-operator, blueteam-auditor, security-architect, auth-security-specialist, cloud-security-reviewer, code-security-auditor, static-analysis-enforcer, runtime-security-tester, dependency-vuln-scanner, secrets-auditor, supply-chain-guardian |
| security/offensive | pentest-operator, pentest-reporter |

## Commands (6)

| Command | Function |
|---------|----------|
| `/complete-development <req-id>` | Full loop: clarify, specify, architect, implement, test, security, tag |
| `/curate-skills [theme]` | Browse and manage the skill catalog |
| `/generate-docs` | Auto-generate `docs/` structure from repo analysis |
| `/security-audit [path-or-domain]` | Audit the codebase across 11 security domains |
| `/init-skill <theme> <name>` | Scaffold a new OpenCode skill from AMA template |
| `/triage-incident` | Emergency incident triage: classify, assign owner, produce ticket |

## Hooks (2)

| Hook | Trigger | Function |
|------|---------|----------|
| `format-skills.sh` | pre-commit | Lint SKILL.md frontmatter and section ordering |
| `cleanup-nul-files.ps1` | Windows cleanup | Remove DOS `nul` files |

## Stats

- Skills: 1899
- Agents: 34
- Commands: 6
- Hooks: 2
- Divisions: 6
- Areas: 15

## Provenance

Skills were sourced from public datasets and community repositories,
then rewritten with ASD-STE100 Issue 9 (Simplified Technical English),
flavored variant. All proprietary codenames were generified. Duplicate
skills across themes were merged. Organized into a corporate divisional
structure (engineering, security, infrastructure, governance, research,
operations). Sources: open-licensed public community skill collections and
contributor submissions. The STE100 standard and checker live at
`research/media/ste100/`.

## Compliance

Licensed under **AGPL-3.0-or-later**. See `COMPLIANCE.md` and the
`security/compliance/license-compliance-audit` skill for enforcement policy.
