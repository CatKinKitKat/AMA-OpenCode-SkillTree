---
description: Browse, search, and manage the AMA skill catalog (1898 skills across 6 divisions, 15 areas).
agent: build
model: sonnet
---
# Curate Skills

Browse and manage the AMA skill tree. Use the `skill-curator` agent to search the catalog, recommend skills for a task, validate frontmatter, and regenerate indexes.

## Usage

```
/curate-skills
/curate-skills <area>
/curate-skills search <keyword>
```

## Parameters

- **area** (optional): list skills under one division/area (for example: `engineering/backend`, `security/offensive`, `operations/product`).
- **search <keyword>** (optional): find skills whose name or description matches the keyword.

## Divisions and Areas

| Division | Area | Focus |
|----------|------|-------|
| `engineering` | `engineering/backend` | Java, Spring, Go, Python, databases, APIs, finance |
| `engineering` | `engineering/frontend` | React, TypeScript, Material-UI, OpenLayers |
| `engineering` | `data-ai` | ML, PyTorch, evaluation, audiocraft |
| `engineering` | `engineering/devtooling` | CI/CD, agents, testing, Docker, Git, MCP |
| `security` | `offensive` | Pentest, red team, AD attacks, network recon |
| `security` | `compliance` | SOC2, ISO27001, GDPR, FDA, quality |
| `security` | `defensive` | ZTNA, kill-switch, field operations |
| `infrastructure` | `systems` | Linux, macOS, terminal, packages |
| `infrastructure` | `cloud` | AWS, Azure architecture |
| `governance` | `methodology` | Planning, debugging, code review, verification |
| `governance` | `requirements` | Specification, clarification, validation |
| `operations` | `operations/github` | GitHub automation, kanban, CI workflows |
| `operations` | `product` | Product management, marketing, career, business |
| `research` | `intelligence` | Deep research, OSINT, competitive analysis |
| `research` | `media` | Creative visual, content, STE100 writing |

## References

- Agent: `.opencode/agents/operations/skill-curator.md`
- Catalog: `.opencode/skills/CATALOG.md`
