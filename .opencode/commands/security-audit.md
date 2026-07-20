---
description: Audit the current codebase for security vulnerabilities across 11 domains (secrets, database, auth, payments, mobile, AI/LLM, deployment, data access, API, CI/CD).
agent: build
model: sonnet
---
# the agent Security Audit

Run a security audit of the repository across 11 domains using the `security-audit-agent` agent and the `pentest/security-audit` skill references.

## Usage

```
/security-audit
/security-audit <path-or-domain>
```

## Parameters

- **path-or-domain** (optional): limit the audit to a subdirectory or a single domain (for example: `api`, `auth`, `payments`). When omitted, audit the whole repository.

## Workflow

1. Load the `security-audit-agent` agent.
2. Detect the tech stack (Supabase, Firebase, Stripe, Next.js, React Native, AI APIs, CI/CD).
3. Audit only the domains that apply to the detected stack. Skip the rest.
4. For each applicable domain, load its reference file from `pentest/security-audit/references/`.
5. Report findings ordered by severity: Critical, High, Medium, Low.
6. For each finding, give file path, vulnerability name, concrete attacker impact, and a before/after fix.
7. End with a prioritized summary table. Flag any Critical issue at the top.

## Core Principle

Never trust the client. Validate every price, user ID, role, subscription status, and rate limit counter server-side.

## References

- Agent: `.opencode/agents/security/security-audit-auditor.md`
- Skill: `.opencode/skills/pentest/security-audit/SKILL.md`
- Domain references: `.opencode/skills/pentest/security-audit/references/`
