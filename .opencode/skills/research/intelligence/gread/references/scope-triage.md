# Scope triage for bounty-scope repo reviews

Use when the user supplies a scope/export CSV and asks to find source-code issues.

## Workflow
1. Parse the CSV first.
2. Filter to `asset_type == SOURCE_CODE`.
3. Rank repos by scope priority / bounty relevance.
4. Pick one repo first. Do not spray across the whole list.
5. Use `gread` endpoints in this order:
   - `/repo?name=owner/repo` to map the tree.
   - `/grep` for scope keywords: `scope`, `token`, `auth`, `path`, `exec`, `eval`, `readFile`, `dangerouslySetInnerHTML`.
   - `/read` for the exact files that match.
6. Prove one narrow end-to-end flow before expanding.

## Evidence rules
- Prefer live code paths over comments or tests.
- Treat generated docs, fixtures, and examples as lower priority than active command paths.
- If one file shows a real sink, capture the exact call chain and stop long enough to summarize the impact before broadening.

## Common sink patterns
- shell command construction via `exec`, `execSync`, `spawn` with `shell: true`
- path joins / resolves fed by untrusted input
- file reads from CLI flags without allowlist checks
- HTML sinks in frontend code (`dangerouslySetInnerHTML`, `innerHTML`)
- token / scope confusion in CLI auth flows