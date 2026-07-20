# Security code audit with Gread

Use this reference when doing public GitHub source audit for bug bounty scope without accounts.

## Fast workflow

1. Start from the bounty scope artifact and isolate source-code assets first.
2. Use `/repo` for directory map, then `/grep` for security-control nouns:
   - `permission`, `allowed_non_write_users`, `github_token`, `secrets.`, `GITHUB_TOKEN`
   - `allowed-tools`, `mcp-config`, `writeFile`, `child_process`, `exec`, `eval`
   - `path traversal`, `realpath`, `credential.helper`, `show_full_output`
3. Read exact files with `/read`, not broad summaries.
4. Trace one end-to-end path:
   public input -> trigger validation -> permission gate -> prompt construction -> tool allowlist -> privileged token/tool -> write/comment/exfil sink.
5. Separate three result classes:
   - confirmed vuln: reproducible sink impact with exact path and input
   - high-risk design: privileged automation on public input but mitigations still block impact
   - false lead/tool artifact: gread/raw masking, generated docs, or non-runtime examples

## the coding agent Action pattern

For `anthropics/coding-agent-action` style workflows, check:

- `action.yml`: inputs, env passed to runner, post steps, token outputs, `show_full_output`, `display_report`.
- `src/github/validation/permissions.ts`: whether `allowed_non_write_users` or bot allowlists bypass write checks.
- `src/modes/*`: mode detection and whether explicit workflow `prompt` switches to agent mode.
- `src/create-prompt/*` and data formatter/sanitizer: untrusted issue/PR/comment content boundaries.
- `src/mcp/*`: MCP server env tokens, tool exposure, path validation, commit/comment sinks.
- `base-action/src/parse-sdk-options.ts`: allowed/disallowed tools parsing, `mcp-config` merging, env scrub/removal.
- repo workflows using the action: declared `permissions`, `github_token`, `allowed_non_write_users`, `CLAUDE_CODE_SCRIPT_CAPS`, `the agent_args`.

## Pitfalls

- `allowed_non_write_users="*"` is not automatically a reportable bug. It becomes reportable when a public/non-write actor can cause non-intended write, secret exposure, or privilege use beyond the intended limited workflow.
- Tool output may mask tokens or templates (`***`, `${{ ... }}`). Verify suspicious action lines from raw GitHub/release tag before treating them as evidence.
- Docs admitting residual prompt-injection risk are supporting context, not proof. Tie them to a concrete exploitable sink.
- If a source repo delegates crucial behavior to a packaged CLI/binary, mark the source finding as incomplete and inspect the release artifact or package next.
- For GitHub Action source audits, do not stop at symmetric-looking code review. Compare paired operations (`commit_files` vs `delete_files`, create vs cleanup, read vs write) and then prove suspected path issues against the underlying primitive. Example: GitHub file-op wrappers may miss `validatePathWithinRepo` on delete, but local Git tree creation rejects slash-containing `../x` entries. Without API proof this stays a false lead, not a report.
- When raw `action.yml` lines show `***` or malformed `${{ ... }}` around secrets/tokens, treat it as possible masking by the retrieval layer. Re-check via raw GitHub, release tags, or package artifacts before reporting token revocation/output bugs.
