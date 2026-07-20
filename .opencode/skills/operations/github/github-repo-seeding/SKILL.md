---
name: github-repo-seeding
description: Clone, scaffold, and initialize GitHub repositories with templates, branch protection, and first commit. Use when starting a new repo, cloning an the-project template repo, or bootstrapping a project in under 60 seconds.
---
# GitHub Repo Seeding

Clone, scaffold, and initialize GitHub repositories with templates and first commit.

## When to Use

- [done] Starting a new repo from an the-project template
- [done] Bootstrapping a new project (monorepo, microservice, library)
- [done] Setting up branch protection on the first commit
- [done] Initializing a new repo with CONTRIBUTING.md, CODEOWNERS, and `.gitignore`

## Workflow

### 1. Create or clone

```bash
gh repo create <org>/<repo-name> --public --template=ACMAME/templates
gh repo clone <org>/<repo-name>
cd <repo-name>
```

### 2. Initialize structure

```bash
mkdir -p src/main/kotlin/com/example/<project>
echo "name: <project>" > settings.gradle.kts
cat << 'GITIGNORE' > .gitignore
.gradle/
build/
out/
.idea/
*.iml
.env
.terraform/
GITIGNORE
```

### 3. First commit

```bash
git add -A
git commit -m "feat: <project> scaffold"
git push -u origin main
```

### 4. Branch protection

```bash
gh api repos/<org>/<repo>/branches/main/protection -X PUT -F required_status_checks=...
```

## Template selection

- `templates/kotlin-spring` : Spring Boot 3 + Kotlin service
- `templates/react-ts` : React + TypeScript + Vite
- `templates/std-lib` : Plain Kotlin library with Gradle
- `templates/python` : Python package with pytest

## Output

- Repo cloned and scaffolded with first commit on main
- Branch protection active
- README populated from template
