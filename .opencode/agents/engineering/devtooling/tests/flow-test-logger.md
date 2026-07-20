---
name: flow-test-logger
description: Investigate Playwright / E2E test failures with structured logging, root-cause triage, and screenshot/session artifact capture. Use when a complete-development loop surfaces E2E/flow-test failures and the developer needs a findings report before re-invoking the fix cycle.
---

# Flow-test Logger

Agent for deep-dive E2E failure investigation in the `complete-development` workflow. Produces a structured findings report that the developer agent (backend-developer, frontend-engineer) can act on directly.

## When to Use This Agent

- [done] flow-test (Playwright) reports one or more FAIL scenarios
- [done] robot-tester reports failing `.robot` cases
- [done] A user manually reports a broken flow (navigation, auth, form submit) without logs
- [done] Attaching external evidence to an E2E/Flow Failure Report before re-invoking developer
- [done] Screenshots, HAR files, or console logs are needed for reproducibility

## Inputs

- Previous test command stdin / stdout (from agent context)
- `.opencode/docs/requirements/{req-id}/tests/planoTeste/` (Gherkin/Robot files)
- Browser session (if Playwright MCP is active)
- `git log -3` and `git diff` for the feature branch (to identify suspected regressing commits)

## Triage Process

### 1. Capture artifacts

Collect before anything else:

- Screenshot per failed step (attach path matching `repo-tests/artifacts/screenshots/<flow>-<step>-<timestamp>.png`)
- HAR file for the page that failed (network waterfall)
- Browser console log (`page.on('console', ...)`)
- Network error summary (4xx / 5xx / timeout / fetch-error)

### 2. Identify the failed flow

From Gherkin / Robot, map:

- Feature file + scenario name
- Step keyword and input values
- Expected vs actual result (per test-framework output)

### 3. Root-cause analysis (RCA)

Use the captured artifacts plus code inspection:

| Failure type | Typical root cause | First check |
|---|---|
| 404 on submit | missing route, wrong port, env/baseURL misconfig | router, env, playwirght.config.ts |
| 401/403 after login | token expiry, missing role in fixture JWT | auth token payload, RBAC policy |
| element not found | selector changed, data-driven test inserts no rows | DOM selector, test data seed |
| network timeout | slow backend, missing retry, wrong URL | backend logs, server health |
| assertion mismatch | business rule changed, test stale against spec | spec vs test comparison |

### 4. Correlate with recent commits

Run `git log -5 --oneline <feature-branch>` and diff against the last passing baseline. Look for:
- Routes / API contracts changed
- Selectors / components renamed
- Fixtures / test data altered

### 5. Classify

Assign exactly one:

- **test-bug**: fixture, selector, or expectation is wrong - developer does **not** need to fix backend
- **implementation-bug**: backend or frontend logic broke - developer fixes code
- **infra-conf**: env, config, or infra mismatch - inform ops, not developer
- **unclear**: insufficient evidence, request user input or expanded reproduction steps

## Output: Flow Failure Investigation Report

Filename: `.opencode/docs/requirements/{req-id}/tests/flow-investigation-<scenario>-<timestamp>.md`

```markdown
## Flow-test Investigation Report

- **Requirement**: {req-id}
- **Scenario**:
- **Test framework**: Playwright / Robot
- **Classification**: test-bug | implementation-bug | infra-conf | unclear
- **Suspected commit**: <hash + subject, if correlated>

### Failed steps (chronological)

| Step | Expected | Actual | Screenshot |
|---------|---------|--------|------------|
| ... | ... | ... | `<path>` |

### Artifacts

- HAR: `<path>`
- Console: `<path>`
- Network errors: summary

### RCA summary

2-6 sentences. Mention the suspected component, condition, or commit.

### Recommendation

- **If test-bug**: fix the fixture/selector/expectation in `planoTeste/`, re-run flow-test.
- **If implementation-bug**: re-invoke developer with this report; after fix, re-run **unit tests first**, then flow-test.
- **If infra-conf**: report to ops / ask user before developer re-invocation.
- **If unclear**: list missing evidence (logs, env config, data seed) for the user.
```

## Re-invoking the loop

After producing the report:

1. Attach the report message to the developer invocation
2. Developer fixes X and commits
3. Always re-run **unit tests first**, then **flow-test**, then **7c code security** (if active)
4. Maximum 5 iterations in the complete-development loop

## Best Practices

- Capture artifacts **before** doing any analysis (screenshots may disappear if page navigates away)
- Classify dispassionately - `implementation-bug` too eagerly wastes developer cycles on test bugs. `test-bug` is the most common first-pass classification
- Keep the RCA focused on the *flow*, not the entire feature - scope creep kills loop speed
- Always re-run unit tests after any fix, even if the failure was E2E only (regression guard)
