---
name: gradle-multi-repo-ci
description: Configure GitHub Actions for multi-repo Gradle builds: build cache, dependency graph, cross-project publishing, and release automation. Use when setting up or optimizing CI for Gradle multi-module or multi-repo projects.
---
# Gradle Multi-Repo CI

Configure GitHub Actions for multi-repo Gradle builds with build cache, dependency graph, and release automation.

## When to Use

- [done] Setting up CI for a new Gradle multi-module repo
- [done] Configuring cross-repo dependency graph caching (composite builds)
- [done] Optimizing slow CI (dependency cache miss, network-bound tasks)
- [done] Release automation: Maven Central, npm, Container, Changelog

## Tech Stack

- GitHub Actions (composite actions, reusable workflows)
- Gradle 7+ (toolchains, configuration cache, build cache)
- Gradle Build Cache (local + remote, HTTP backend)
- semver-release / changelog generation
- Maven Central (GPG signing, Nexus staging)
- Container registry (GHCR, Docker Hub)

## Workflow

### Build cache

```yaml
- uses: gradle/actions/setup-gradle@v4
  with:
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}
```

Cache key: hash of gradle/wrapper/gradle-wrapper.properties (Gradle version) + settings.gradle + build.gradle.

### Parallel jobs

```yaml
jobs:
  lint:  ./gradlew detekt ktlintCheck
  test:  ./gradlew test
  build: ./gradlew assemble
  needs: [lint, test]
```

### Publish (main only)

```yaml
if: github.ref == 'refs/heads/main'
steps:
  - run: ./gradlew publish       -PsigningKey=${{ secrets.SIGNING_KEY }}       -PsigningPassword=${{ secrets.SIGNING_PASSWORD }}
```

## Pitfalls

- Do not publish on PR triggers (use `push` + `if:` guard)
- Pin actions by SHA digest when possible
- Use Gradle Toolchains (JDK version per project, not per CI image)
- Set job timeout to avoid zombie runners

## Output

```
.github/workflows/ci.yml (or ci-<project>.yml per repo)
```

Reference `ci-cd-pipeline-agent` for pipeline orchestration across multiple repos.
