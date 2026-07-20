---
name: github-org-bootstrap
description: Bootstrap a new GitHub organization: teams, repos, branch protection, CODEOWNERS, security policies, and CI templates. Use when spinning up a new org, project, or monorepo with security-first defaults.
---
# GitHub Org Bootstrap

Bootstrap a new GitHub organization with security-first defaults, CODEOWNERS, teams, and CI templates.

## When to Use

- [done] Spinning up a new GitHub organization for a team or company
- [done] Creating a new monorepo with CODEOWNERS, branch protection, required status checks
- [done] Setting up security policies (Dependabot, secret scanning, CodeQL)
- [done] Creating team-based access control (Engineering, Security, Docs)
- [done] Standardizing pull request templates and contributing guides

## Workflow

### 1. Organization setup

- Create org on github.com
- Configure org-level MFA enforcement
- Set org-level `SECURITY.md` template

### 2. Repo template

```bash
# First repo in the org (template)
gh repo create <org>/<template-repo> --public --template=the-project/templates
```

### 3. Branch protection (main)

```yaml
required_status_checks:
  strict: true
  contexts: ["ci/build", "ci/test", "ci/lint", "sec/codeql"]
required_linear_history: true
required_signatures: true
enforce_admins: true
```

### 4. CODEOWNERS

```text
# Default: org leads
*       @org/leads

# Per-team ownership
/frontend/ @org/frontend
/backend/  @org/backend
/devops/   @org/platform
```

### 5. Security policies

- Enable Dependabot alerts (org-level default)
- Enable secret scanning
- Enable CodeQL (GitHub Advanced Security or free for public repos)
- Enable dependabot for actions, npm, pip

### 6. CONTRIBUTING.md

Standardize:
- PR size limits (small < 400 LOC preferred)
- Conventional commits (`feat(area):`, `fix(area):`, `docs(area):`)
- CI must pass before merge (`ci/build`, `ci/test`, `ci/lint`, `sec/codeql` green)
- CODEOWNERS approval requirement

## Output

- Org with public repos, branch protection on main
- `CONTRIBUTING.md`, `CODEOWNERS`, `.github/pull_request_template.md`, `SECURITY.md`
- Dependabot config in `.github/dependabot.yml`
- GitHub Actions workflow: `ci.yml`
