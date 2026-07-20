# CI/CD Pipeline Security Reference

**Author:** azizaeffendi  
**Last Updated:** 2026-06-05  
**Applies To:** GitHub Actions, GitLab CI, supply chain security, Docker builds

---

## Quick Reference

Run these grep commands against your repository to surface CI/CD security issues immediately.

```bash
# Find echoed secrets in workflow files
grep -rn "echo.*\${{.*secrets\." .github/workflows/

# Find unpinned actions (using branch or tag instead of SHA)
grep -rn "uses:.*@main\|uses:.*@master\|uses:.*@latest\|uses:.*@v[0-9]" .github/workflows/

# Find secrets passed as --build-arg (leaks into image layers)
grep -rn "\-\-build-arg.*SECRET\|\-\-build-arg.*KEY\|\-\-build-arg.*TOKEN\|\-\-build-arg.*PASSWORD" .github/workflows/ Dockerfile*

# Find workflows with overly broad permissions
grep -rn "permissions:.*write-all\|contents:.*write" .github/workflows/

# Find missing branch protection indicators
grep -rn "push.*branches.*main\|push.*branches.*master" .github/workflows/ | grep -v "branches-ignore"

# Find hardcoded credentials in workflow env blocks
grep -rn "^\s*[A-Z_]*\(KEY\|TOKEN\|SECRET\|PASSWORD\|PASS\)\s*:\s*[a-zA-Z0-9]" .github/workflows/

# Find environment variables that should be secrets
grep -rn "env:$" -A 20 .github/workflows/ | grep -v "\${{.*secrets\."
```

---

## GitHub Actions Secrets

### Rule: Never Echo Secrets

Secrets that are printed to logs are permanently visible in GitHub's workflow run history. Once logged, they must be rotated: there is no way to redact them retroactively from existing runs.

**Vulnerable Pattern: Echoing Secrets:**

```yaml
# INSECURE: secret printed to logs in plaintext
- name: Deploy
  run: |
    echo "Deploying with key: ${{ secrets.DEPLOY_KEY }}"
    echo "API_KEY=${{ secrets.API_KEY }}" >> config.env
    curl -H "Authorization: ${{ secrets.API_TOKEN }}" https://api.example.com/deploy

# INSECURE: setting env var then echoing the env
- name: Debug config
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}
  run: |
    env | grep MY_SECRET   # prints all env vars including secrets
    printenv               # same problem
```

**Vulnerable Pattern: Passing Secrets to untrusted code:**

```yaml
# INSECURE: pull_request_target + checkout of fork code = secret exposure
on: pull_request_target

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # DANGEROUS: checks out fork code
      - run: npm test                                      # fork's package.json runs with repo secrets
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

**Secure Pattern: Use `${{ secrets.NAME }}` Without Echoing:**

```yaml
# SECURE: secret used directly in the command, never printed
- name: Deploy to production
  run: |
    curl \
      --fail \
      -H "Authorization: Bearer $DEPLOY_TOKEN" \
      -X POST \
      https://api.example.com/deploy
  env:
    DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}  # exposed only to this step's env

# SECURE: write to GITHUB_OUTPUT instead of echoing
- name: Generate token
  id: get_token
  run: |
    TOKEN=$(./scripts/generate-token.sh)
    echo "token=$TOKEN" >> "$GITHUB_OUTPUT"  # safe output mechanism
  env:
    SIGNING_KEY: ${{ secrets.SIGNING_KEY }}

- name: Use token
  run: ./deploy.sh
  env:
    TOKEN: ${{ steps.get_token.outputs.token }}
```

**Secure Pattern: Separate Untrusted PR Checks:**

```yaml
# SECURE: pull_request (not pull_request_target) for untrusted code
on: pull_request  # forks do NOT get access to secrets

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4  # checks out the PR code safely
      - run: npm ci
      - run: npm test
      # No secrets needed — safe to run untrusted code here
```

---

## Pinned Action Versions

### Rule: Pin Actions to Full SHA256 Commit Hash

When you reference an action by a mutable tag (`@v4`, `@main`) or branch, GitHub resolves it at run time. A compromised maintainer account or a malicious tag update can swap in code that exfiltrates your secrets.

**Vulnerable Pattern: Unpinned by Tag or Branch:**

```yaml
# INSECURE: resolved at run time — tag can be moved to malicious commit
steps:
  - uses: actions/checkout@main            # mutable branch
  - uses: actions/setup-node@v4            # mutable tag
  - uses: actions/upload-artifact@latest   # mutable alias
  - uses: third-party/some-action@v2       # especially risky for third-party actions
```

**Secure Pattern: Pinned to Full Commit SHA:**

```yaml
# SECURE: SHA is immutable — the code you reviewed is the code that runs
steps:
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683         # v4.2.2
  - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af       # v4.2.0
  - uses: actions/upload-artifact@4cec3d8aa04e39d1a68397de0c4cd6fb9dce8ec1  # v4.6.1

  # For first-party actions in your own org, tags are acceptable if you control the repo
  - uses: your-org/your-action@v1  # only safe if you own and protect this repo
```

**Automating Pin Updates with Dependabot:**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "chore(actions)"
```

---

## Protected Branches

### Main Branch Protection Rules

Without branch protection, any contributor with write access can push directly to `main`, bypassing code review and CI checks.

**Required GitHub Branch Protection Settings for `main`:**

```
Branch protection rule: main
  [x] Require a pull request before merging
      [x] Require approvals: 1 (2 for critical repositories)
      [x] Dismiss stale pull request approvals when new commits are pushed
      [x] Require review from Code Owners
  [x] Require status checks to pass before merging
      [x] Require branches to be up to date before merging
      Required checks: ci/test, ci/lint, security/scan
  [x] Require conversation resolution before merging
  [x] Require signed commits
  [x] Include administrators  (do not bypass rules for admins)
  [x] Restrict who can push to matching branches
  [ ] Allow force pushes  (DISABLED)
  [ ] Allow deletions     (DISABLED)
```

**Automate with GitHub CLI:**

```bash
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci/test","ci/lint"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

**CODEOWNERS File:**

```
# .github/CODEOWNERS
# These owners must approve PRs that touch these paths

# Global owners
*                    @your-org/engineering-leads

# Security-sensitive paths require security team review
.github/workflows/   @your-org/security-team
infrastructure/      @your-org/security-team @your-org/platform-team
**/auth/**           @your-org/security-team
**/payment/**        @your-org/security-team

# Database migrations need DBA approval
db/migrations/       @your-org/dba-team
```

---

## Supply Chain Security

### SLSA Levels

SLSA (Supply-chain Levels for Software Artifacts) is a framework for measuring and improving build integrity.

| Level | Requirements | Protects Against |
|-------|-------------|-----------------|
| SLSA 1 | Documented build process, provenance generated | Accidental build mistakes |
| SLSA 2 | Hosted build service, signed provenance | Compromised developer machine |
| SLSA 3 | Hardened build service, non-falsifiable provenance | Compromised build service |
| SLSA 4 | Two-person review, hermetic builds | Insider threats, supply chain compromise |

**Generate SLSA Provenance in GitHub Actions:**

```yaml
# Use the official SLSA GitHub generator
jobs:
  build:
    outputs:
      digests: ${{ steps.hash.outputs.digests }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: Build artifact
        run: |
          make build
          sha256sum artifact.tar.gz > checksums.txt

      - name: Generate hashes
        id: hash
        run: |
          echo "digests=$(sha256sum artifact.tar.gz | base64 -w0)" >> "$GITHUB_OUTPUT"

  provenance:
    needs: [build]
    permissions:
      actions: read
      id-token: write
      contents: write
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v2.0.0
    with:
      base64-subjects: "${{ needs.build.outputs.digests }}"
```

### Dependency Review

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review
on: pull_request

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: actions/dependency-review-action@ce3cf9537a52e8119d91fd484ab5e8a0d7877abd  # v4
        with:
          fail-on-severity: moderate
          deny-licenses: GPL-3.0, AGPL-3.0
          comment-summary-in-pr: on-failure
```

### Sigstore: Sign and Verify Artifacts

```bash
# Sign a release artifact with cosign (Sigstore)
cosign sign-blob \
  --output-certificate artifact.tar.gz.crt \
  --output-signature artifact.tar.gz.sig \
  artifact.tar.gz

# Verify before deploying
cosign verify-blob \
  --certificate artifact.tar.gz.crt \
  --signature artifact.tar.gz.sig \
  --certificate-identity "https://github.com/your-org/your-repo/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  artifact.tar.gz
```

---

## Least Privilege Permissions

### GITHUB_TOKEN Scopes

By default, `GITHUB_TOKEN` in GitHub Actions is granted broad write permissions. Following the principle of least privilege, explicitly declare only the permissions each job actually needs.

**Vulnerable Pattern: Default Broad Permissions:**

```yaml
# INSECURE: no permissions block = inherits repo's default (often write-all)
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

**Vulnerable Pattern: Explicit Write-All:**

```yaml
# INSECURE: write-all is almost never necessary
permissions:
  contents: write-all  # grants write to everything
```

**Secure Pattern: Minimal Per-Job Permissions:**

```yaml
# SECURE: set minimal permissions at workflow level, override per job as needed
permissions: {}  # deny all by default at workflow level

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read   # checkout only
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: npm ci && npm test

  publish-docs:
    runs-on: ubuntu-latest
    permissions:
      contents: write   # needs to push to gh-pages
      pages: write
      id-token: write   # needed for OIDC/Pages deployment
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: npm run build-docs
      - uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e  # v4

  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write       # create release
      packages: write       # push to GHCR
      id-token: write       # OIDC token for provenance
      attestations: write   # write attestations
    steps:
      - run: make release
```

**Permission Reference:**

| Permission | Read Use | Write Use |
|-----------|----------|-----------|
| `contents` | Checkout code | Push commits, create releases |
| `packages` | Pull packages | Push to GitHub Packages / GHCR |
| `pull-requests` | Read PR info | Create/update PRs, add labels |
| `issues` | Read issues | Create/update issues |
| `id-token` |: | OIDC token (for cloud auth, Sigstore) |
| `security-events` |: | Upload SARIF results |
| `deployments` | Read deployments | Create deployment status |

---

## Secrets in Docker Builds

### The Problem with `--build-arg`

Docker `--build-arg` values are baked into the image layer metadata. Anyone who can pull the image: including CI caches, registries, and build logs: can extract the secret with `docker history`.

**Vulnerable Pattern: Build Arg Leaks Secret:**

```dockerfile
# INSECURE Dockerfile
ARG NPM_TOKEN
ARG DATABASE_URL

RUN npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN && \
    npm ci

# The token is now in this layer's metadata, visible via docker history
```

```yaml
# INSECURE workflow
- name: Build image
  run: |
    docker build \
      --build-arg NPM_TOKEN=${{ secrets.NPM_TOKEN }} \
      --build-arg DATABASE_URL=${{ secrets.DATABASE_URL }} \
      -t myapp:latest .
```

**Verification: How Attackers Extract Secrets:**

```bash
# Attacker runs this after pulling image
docker history --no-trunc myapp:latest
# Output shows: ARG NPM_TOKEN=npm_abc123secrettoken...
```

**Secure Pattern: Docker BuildKit Secret Mounts:**

```dockerfile
# SECURE Dockerfile — secret is mounted at build time, never stored in layers
# syntax=docker/dockerfile:1.4

# Mount the npm token only for the npm ci command
RUN --mount=type=secret,id=npm_token \
    npm config set //registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token) && \
    npm ci && \
    npm config delete //registry.npmjs.org/:_authToken  # clean up

# Secret is NOT present in the resulting image layer
```

```yaml
# SECURE workflow — use BuildKit secret mounting
- name: Build image
  run: |
    echo "${{ secrets.NPM_TOKEN }}" | docker build \
      --secret id=npm_token \
      --progress=plain \
      -t myapp:latest .
  env:
    DOCKER_BUILDKIT: 1
```

**Alternative: Multi-Stage Build Pattern:**

```dockerfile
# SECURE alternative: use multi-stage builds to discard secret-containing layers
FROM node:20 AS builder
ARG NPM_TOKEN
# Even with build-arg, the final stage doesn't inherit this layer
RUN npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN && \
    npm ci --production
RUN npm config delete //registry.npmjs.org/:_authToken

# Final image copies only built artifacts — no secrets
FROM node:20-alpine AS production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

---

## Pitfalls

### Pitfall 1: `pull_request_target` + Fork Checkout = Secret Exfiltration

`pull_request_target` runs in the context of the base repo (with access to secrets) but if you checkout fork code in that context, the attacker's code runs with your secrets. This is one of the most exploited GitHub Actions vulnerabilities.

```yaml
# VULNERABLE: fork code runs with repo secrets
on: pull_request_target
steps:
  - uses: actions/checkout@v4
    with:
      ref: ${{ github.event.pull_request.head.sha }}  # attacker-controlled code
  - run: npm run build  # attacker's package.json postinstall hook runs here

# SECURE: for PRs from forks, use pull_request (no secrets)
on: pull_request
# If you need secrets for external PRs, use a separate approval-gated workflow
```

### Pitfall 2: Environment Variable Inherits Across Steps

Setting a secret as an env var at the job level exposes it to every subsequent step, including any third-party actions that run shell commands.

```yaml
# VULNERABLE: secret visible to all steps including third-party actions
jobs:
  build:
    env:
      AWS_SECRET_KEY: ${{ secrets.AWS_SECRET_KEY }}  # job-level exposure
    steps:
      - uses: some-third-party/action@v1  # this action can read AWS_SECRET_KEY
      - run: npm test

# SECURE: scope secrets to only the steps that need them
    steps:
      - uses: some-third-party/action@v1  # no access to AWS key
      - run: ./deploy.sh
        env:
          AWS_SECRET_KEY: ${{ secrets.AWS_SECRET_KEY }}  # step-level only
```

### Pitfall 3: Workflow Triggers on Forked PRs See Secrets with `workflow_run`

`workflow_run` events triggered by fork PRs inherit the base repo's secrets, similar to `pull_request_target`. The checkout in the `workflow_run` handler must be handled carefully.

```yaml
# VULNERABLE
on:
  workflow_run:
    workflows: [CI]
    types: [completed]

steps:
  - uses: actions/checkout@v4  # this checks out the triggering commit — could be fork code
  - run: ./deploy-preview.sh
    env:
      DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}  # exposed to fork code if above checkout used

# SECURE: when using workflow_run with fork PRs, only use artifacts, not re-checkout
steps:
  - uses: actions/download-artifact@v4
    with:
      name: build-output
      run-id: ${{ github.event.workflow_run.id }}
      github-token: ${{ secrets.GITHUB_TOKEN }}
  # Now deploy from artifact — no fork code executed
```

### Pitfall 4: Caching Can Persist Secrets Between Runs

The actions/cache action stores content to a cache keyed on a hash. If a build step writes secrets to a cached directory (node_modules postinstall scripts, for example), those secrets persist in cache across workflow runs and can be read by later runs.

```yaml
# RISKY: if any step writes secrets to node_modules, they're cached
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}

# MITIGATION: never write secrets to cacheable directories
# Run npm ci AFTER restoring cache, not before
```

### Pitfall 5: Storing Secrets in GitHub Actions Variables Instead of Secrets

GitHub Actions "Variables" (not "Secrets") are not encrypted: they are visible in plaintext in the UI and in API responses to anyone with read access to the repo.

```
# WRONG PLACE: Actions → Variables → "DATABASE_URL" with full connection string
# Anyone with repo read access sees this value

# RIGHT PLACE: Actions → Secrets → "DATABASE_URL"
# Masked in logs, encrypted at rest, not visible after creation
```

### Pitfall 6: Skipping Dependency Review for Internal PRs

Teams often configure dependency review only for external contributors. Internal team members can inadvertently (or maliciously) introduce vulnerable dependencies.

```yaml
# SECURE: run dependency review on ALL pull requests, regardless of origin
on:
  pull_request:
    branches: [main, staging]  # not gated on fork vs internal
```

### Pitfall 7: Environment Promotion Without Re-Verification

Building an artifact in `staging` and then promoting the same artifact to `production` without re-verifying its signature or provenance means any tampering during the staging phase goes undetected.

```bash
# SECURE: verify provenance at every promotion gate
cosign verify-blob artifact.tar.gz \
  --certificate artifact.tar.gz.crt \
  --signature artifact.tar.gz.sig \
  --certificate-identity "https://github.com/your-org/repo/.github/workflows/build.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
# Only promote if verification passes
```

---

## Verification

Run these commands to verify your CI/CD security controls are working.

```bash
# 1. Verify all actions are pinned (no tags or branches)
grep -rn "uses:" .github/workflows/ | grep -E "@(main|master|latest|v[0-9])" && \
  echo "FAIL: Unpinned actions found" || echo "PASS: All actions appear pinned"

# 2. Check for secret echoing in workflows
grep -rn "echo.*secrets\." .github/workflows/ && \
  echo "FAIL: Secrets may be echoed" || echo "PASS: No secret echoing found"

# 3. Verify permissions blocks exist in all workflow files
for f in .github/workflows/*.yml; do
  if ! grep -q "^permissions:" "$f" && ! grep -q "^    permissions:" "$f"; then
    echo "MISSING permissions block: $f"
  fi
done

# 4. Check for --build-arg with sensitive names
grep -rn "\-\-build-arg" .github/workflows/ Dockerfile* | \
  grep -iE "secret|token|key|password|pass|credential" && \
  echo "FAIL: Secrets passed as --build-arg" || echo "PASS: No build-arg secrets found"

# 5. Verify branch protection is enabled (requires gh CLI)
gh api repos/:owner/:repo/branches/main/protection | \
  jq '{
    require_pr: .required_pull_request_reviews != null,
    status_checks: .required_status_checks != null,
    enforce_admins: .enforce_admins.enabled,
    no_force_push: (.allow_force_pushes.enabled == false)
  }'

# 6. Verify CODEOWNERS file exists
test -f .github/CODEOWNERS && echo "PASS: CODEOWNERS exists" || echo "FAIL: No CODEOWNERS"

# 7. Verify dependabot is configured for actions
test -f .github/dependabot.yml && \
  grep -q "github-actions" .github/dependabot.yml && \
  echo "PASS: Dependabot configured for actions" || \
  echo "FAIL: Dependabot not configured for GitHub Actions"

# 8. Verify Docker builds use BuildKit
grep -rn "DOCKER_BUILDKIT\|buildkit" .github/workflows/ | \
  grep -v "0\|false" | \
  head -5
```
