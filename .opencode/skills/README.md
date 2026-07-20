# Skills - Specialized Technical Knowledge

## Description

This folder contains **skills** (specialized technology knowledge). Each skill
is a `SKILL.md` that defines standards, conventions, best practices, and
specific configurations for a technology or framework. Everything here is
generic: no real client, system, or person is named.

## What They Are For

1. **Standardize development** across a technology.
2. **Provide technical context**: versions, libraries, configurations.
3. **Implementation guide**: examples and templates.
4. **Reference for agents**: AI agents consult these automatically.
5. **Onboarding**: learn the conventions for a stack.

## Structure

```
skills/
├── backend/        # langs, frameworks, data, IaC
├── frontend/       # (removed: was tainted with client system names)
├── ml/             # model + ML infra
├── requirement-engineering/  # spec lifecycle
├── github/         # git / gh workflow
├── linux/          # sysadmin / tuning / desktop
├── devtooling/     # build / CI / runtime / env
├── pentest/        # RED team
├── blueteam/      # DEFENSIVE / detection
└── research/       # discovery / analysis
```

## File Format

```yaml
---
name: skill-name
description: Brief description of the skill and when to use it
---
```

Followed by: Technology Stack, Architecture & Patterns, Naming
Conventions, Code Quality Standards, Bootstrap & Setup, Folder
Structure, Configuration, Testing Strategy, Best Practices.

## How to Use Skills

- **Developers:** read the relevant skill before touching a technology.
- **Agents:** consult automatically when the task matches a stack.
- **New skill:** drop a folder under `skills/<theme>/<name>/` with a
  `SKILL.md`.

## Maintenance

- New version -> update the skill.
- New library -> add to the stack.
- Standard change -> update the relevant section.

## Important Notes

- Skills are generic. Any `example.com` / `the-project` / `the-backend`
  token is a placeholder, not a real identifier.
- Keep it client-neutral. Scrub real names before committing.
