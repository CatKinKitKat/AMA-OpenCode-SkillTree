# Scope audit notes: vercel-open-source CSV review

Date: 2026-05-11

## Workflow that worked
1. Parse the CSV first.
2. Filter to `asset_type == SOURCE_CODE`.
3. Pick one Tier 1 repo first. Do not spray across all repos.
4. Use `/repo` to map the tree, then `/grep` for high-risk sinks:
   - `execSync`
   - `execFileSync`
   - `spawn(`
   - `shell: true`
   - `eval(` / `new Function`
   - `dangerouslySetInnerHTML`
   - `readFileSync` / `writeFileSync`
5. Read exact files only after a hit.
6. Prove one narrow sink-to-source chain before broadening.

## Confirmed findings from this session
- `vercel/next.js`:
  - `packages/next-codemod/bin/upgrade.ts`
  - `@next/codemod upgrade [revision]`
  - source: CLI `revision`
  - sink: `execSync(\`npm --silent view \"next@${resolvedRevision}\" --json --field version\`)`
  - issue: shell command substitution survives inside double quotes
- `sveltejs/svelte`:
  - `playgrounds/sandbox/scripts/download.js`
  - source: URL path segments
  - sink: `execSync(\`git clone --depth 1 ${repo_url} \"${target_dir}\"\`)`
- `vercel/ai`:
  - `packages/codemod/src/lib/transform.ts`
  - source: CLI `codemod`, `source`, `--jscodeshift`
  - sink: `execSync(command)` after string concatenation

## Rejection criteria for future sweeps
Treat as lower priority if the sink is:
- test fixture only
- docs example only
- internal benchmark script with no user-controlled path into the shell
- build/release helper with strictly bounded inputs and no external input path

## URL / shell note
For `execSync`-style sinks, double quotes are not enough. Shell substitutions like `$(...)` and backticks still execute.

## Output habit
For bounty-scope work, save a short findings note in a reference file and then use that note to draft the final report.