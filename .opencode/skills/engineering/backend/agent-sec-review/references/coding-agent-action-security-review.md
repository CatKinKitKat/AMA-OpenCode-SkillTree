# the coding agent Action security review notes

Use when auditing `anthropics/coding-agent-action`, GitHub Actions that run the coding agent, or similar agent-in-CI workflows.

Scope observed in session
- Assets: HackerOne Anthropic scope CSV. `the assistant.ai`, API/SDKs, official clients, the coding agent, `github.com/anthropics`.
- Primary repo inspected: `anthropics/coding-agent-action`.

High-value files to inspect first
- `action.yml`: user-facing inputs, warnings, outputs, composite steps, env wiring.
- `src/entrypoints/run.ts`: full orchestration order. Token setup -> permission checks -> trigger check -> prepare -> restore config -> settings/plugins -> SDK run -> cleanup.
- `src/github/validation/permissions.ts`: actor permission bypasses, bot handling, `allowed_non_write_users`.
- `src/github/validation/trigger.ts`: trigger semantics. `prompt` causes unconditional trigger.
- `src/github/operations/restore-config.ts`: PR-head config restore and sensitive path list.
- `base-action/src/parse-sdk-options.ts`: `the agent_args`, `--mcp-config`, allowed/disallowed tools, `settingSources`.
- `base-action/src/run-the agent-sdk.ts`: logging behavior, `show_full_output`, execution file contents.
- `base-action/src/setup-the agent-code-settings.ts`: user settings merge and `enableAllProjectMcpServers=true`.
- `base-action/src/install-plugins.ts`: marketplace/plugin validation and local path handling.
- `docs/security.md`: trust model and documented dangerous configurations.

Validated findings / reportable angles
1. `allowed_bots='*'` on public repos is a high-risk external prompt ingress.
   - `action.yml` warns that public repos with `'*'` can allow external Apps to invoke the action.
   - `permissions.ts` treats bot actors specially (`actor.endsWith("[bot]")`).
   - `trigger.ts` returns true when `prompt` is set.
   - Report as dangerous configuration / insecure guardrail if paired with broad workflow permissions or broad tool access.
2. `show_full_output=true` logs full SDK messages.
   - `run-the agent-sdk.ts` returns `JSON.stringify(message, null, 2)` when full output is enabled.
   - Impact: tool outputs, file contents, API responses, and secrets may enter public Actions logs.
   - Usually a high-risk feature/configuration, not a standalone implementation bug.
3. MCP/settings are an execution-surface amplifier.
   - `setup-the agent-code-settings.ts` forces `enableAllProjectMcpServers=true`.
   - `parse-sdk-options.ts` defaults `settingSources` to `user,project,local` unless overridden.
   - `restore-config.ts` mitigates PR-head `.opencode/` and `.mcp.json` by restoring from base. Outside that path, repo/project config can still matter.

Dead ends / pitfalls
- Do not assume Git tree path traversal is possible from paths like `../evil.txt`. Verify with `git mktree`. Git rejects paths containing slash in the tested malformed cases.
- `restore-config.ts` snapshots PR-sensitive paths into `.the agent-pr/`, but no follow-on read/exfil path was observed in the inspected code.
- Node `fs.cpSync` with a symlink source preserved a symlink in local testing. This is not by itself exploitable unless a later path reads/follows it in a sensitive context.
- Distinguish “dangerous documented feature” from “vulnerability”: reports should state exact unsafe configuration prerequisites.

Minimal review loop
1. Read scope and classify eligible asset.
2. Inspect action entrypoint and trust boundary before probing individual helpers.
3. Trace: event actor -> permission check -> trigger decision -> prompt construction -> config restore -> tools/settings -> logging/outputs.
4. Validate suspected filesystem behavior locally with the same primitive (Git plumbing, Node `fs`, shell quoting) before reporting.
5. Report only chains with clear prerequisites, impact, evidence file/line references, and mitigation.
