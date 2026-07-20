# Source-code repo triage for bounty scopes

Use this when the scope artifact lists public source repositories instead of, or in addition to, a live URL.

## Procedure

1. Resolve the exact repository from the scope item.
2. Read repo-local instructions first:
   - `AGENTS.md`
   - `AGENTS.md`
   - any nearer project instructions if present
3. Inspect the repo structure and search for high-risk sinks:
   - command execution (`exec`, `spawn`, `system`, shell strings)
   - file read/write/delete and path joins
   - network fetches / SSRF / redirect handling
   - host/origin / CSRF / authz comparison logic
   - template rendering / `innerHTML` / HTML sinks
   - deserialization / eval / code generation
   - sandbox / temp-file / cross-process brokers
4. Read the exact function around each hit before deciding it matters.
5. Prefer one narrow exploit path with concrete evidence over many weak leads.
6. Ignore test-only code, fixtures, docs comments, and dead paths unless runtime evidence shows they execute.

## Evidence standard

A valid finding should include:
- repository and file path
- function or symbol name
- source-to-sink path
- why the trust boundary is violated
- any relevant guard that fails or can be bypassed

## Session notes

This session found useful repo-audit patterns in Vercel OSS scopes:
- scope CSVs can be used to resolve exact in-scope repos before any code search
- `gread` works well for fast repo search/read on public GitHub repos
- `AGENTS.md` at repo root should be read before deeper inspection
- search results must be narrowed to the live code path. Test files and compiled bundles are usually noise
- suspicious patterns that deserved follow-up included `execSync`, temp files in `/tmp`, host/origin comparisons, and direct filesystem reads in server paths
