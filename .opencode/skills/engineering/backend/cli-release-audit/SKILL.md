---
name: cli-release-audit
description: Pre-release audit for CLI tools (especially Rust/Python). Checks build, tests, help quality, output friendliness (agent + human), path leaks, dependency portability, .gitignore hygiene, and missing release artifacts.
version: 1.0.0
metadata: 
tags: [release, audit, cli, rust, qa, pre-release]
related_skills: [dogfood, requesting-code-review]
---


# CLI Release Audit

Systematic pre-release review for CLI projects. Trigger when a user says "about to release", "publish", "pre-release check", or asks to review a CLI project for release readiness.

## Audit phases: execute in order

### Phase 1: Build & test health

1. `cargo check` / equivalent build command: must pass clean
2. Run full test suite (`cargo test`). Any failure is P0.
3. Note warning count: clippy warnings are P2 but worth flagging.

### Phase 2: Dependency portability

1. Check `Cargo.toml` (or equivalent) for `path = "..."` local dependencies: these break on other machines. P0.
2. Check for hardcoded absolute paths in source: `rg "/Users/\|/home/\|C:\\\\Users" src/`
3. Check for hardcoded localhost URLs that aren't configurable defaults.

### Phase 3: CLI help quality

1. Run `--help` for every subcommand.
2. Check: do all arguments have description text? Bare `--symbol <SYMBOL>` with no help doc is P1.
3. Check: is there a `--version` flag? Missing = P2.
4. Check: are default values shown and sensible?

### Phase 4: Trial runs

1. Run with minimal/no data to check error messages: are they clear and actionable?
2. Run with existing state (if any) to see real output.
3. Check: does the tool panic or give a clean error on missing input?

### Phase 5: Output friendliness

**For agents:**
- Is there a compact/machine-readable output mode?
- Is the JSON output flat enough to extract key fields without deep nesting?
- Are there redundant/repeated fields inflating token cost?
- Is there a `--compact` or `--agent` flag? If not, flag as P1-P2.

**For humans:**
- Is there a human-readable summary mode (not just raw JSON)?
- Are key decisions (go/no-go, direction, quality) visible without scrolling?
- Are internal IDs, policy hashes, and debug fields hidden by default?
- Is `decision_hint` or equivalent readable, or is it a packed internal string?

### Phase 6: Information leakage

1. Check output for local absolute paths (user home dirs, download folders).
2. Check for leaked internal state paths in recommended commands.
3. Check for PII or machine-specific info in default output.

### Phase 7: Repository hygiene

1. `.gitignore`: are runtime state dirs, `__pycache__/`, temp files excluded?
2. Are state/experiment directories already tracked? (`git ls-files 'state*'` etc.)
3. Is there a LICENSE file?
4. `Cargo.toml` / `package.json`: are `repository`, `license`, `authors` fields present?
5. Are there `.DS_Store` files tracked?

### Phase 8: Documentation

1. Does README cover: install, first run, common workflows?
2. Is there example data or a `--demo` mode for new users?
3. Are internal dev docs separated from public docs?

## Severity guide

| Level | Meaning | Examples |
|: : : -|: : : : -|: : : : -|
| P0 | Blocks release: other machines can't build/run | Local path deps, test failures |
| P1 | Serious UX/trust issue | No help text, path leaks in output, no human-readable mode |
| P2 | Polish | Missing LICENSE, clippy warnings, no: version, bloated main file |

## Pitfalls learned

- Array-before-object check ordering: if code does `as_object()` then `is_array()`, the array case is unreachable. Check array first.
- `.gitignore` patterns like `/state` don't match `state_foo/`: need `state*/` glob.
- Even after adding `/state*/`, a root-level runtime file like `state_autoresearch_cycle_validation.next-spec.json` will still remain as `D + ??` after `git rm --cached` unless it is separately ignored. For release cleanup, verify both tracked directories and similarly named root files with `git ls-files --stage -- <path>` plus `git status --ignored --untracked-files=all`.
- If a runtime artifact lives at repo root (for example `state_autoresearch_cycle_validation.next-spec.json`), `state*/` still will not match it. Add an explicit root ignore like `/state_autoresearch_cycle_validation.next-spec.json`, then `git rm --cached -- <file>`. Expect a staged `D` until commit. In `git status --ignored` the working-copy replacement should appear as `!!`, which is the correct post-cleanup state.
- If a runtime artifact exists both as a tracked repo-root file and as ignored state directories, `git rm --cached` may leave the expected mixed state (`D tracked_file` plus `?? tracked_file`). In that case add an explicit root ignore entry (for example `/state_autoresearch_cycle_validation.next-spec.json`), verify with `git check-ignore -v --no-index`, and treat the final clean state as: normal `git status` shows only the staged deletion while `git status --ignored` shows `!! tracked_file`.
- `serde_json::to_string_pretty` for all output means no compact mode exists by default.
- Recommended-next-command fields that embed absolute data paths from the developer's machine are a common leak vector.
- If you add `--output-format` / `--compact` / `--agent` / `--human`, verify the flags are actually wired through every output path: not just the default branch. In `workflow-status`-style commands this includes: full snapshot output, filtered views (`--actionable-only`, `--conflicts-only`, `--latest-promotable`, hard-block filters), and named phase surfaces.
- Apply path redaction mechanically at the final JSON/value-print boundary so filters and phase outputs cannot bypass it. A small helper like `print_redacted_json()` plus recursive JSON string redaction works well.
- When extending a command input struct with a new field (for example `output_format`), remember to patch all test initializers and helper constructors. Otherwise `cargo check --tests` will fail even when normal `cargo check` passes.
- Large JSON outputs with `latest_*` and `recent_*` sections often duplicate the same record 3-5x, inflating agent token cost dramatically.
- When adding new CLI flags or command-input struct fields in a Rust monolith, run both `cargo check` and `cargo check --tests` before claiming success. Test-only manual initializers often still use the old struct shape.
- If you add `--output-format` / `--compact` / `--agent` / `--human`, wire the output switch for every major branch: full output, phase/filter output, and human view. It is easy to patch only the default path and leave filtered/phase paths leaking old full JSON or local paths.
- For path redaction, do not only redact the top-level full snapshot. Redact filtered lists, phase surfaces, and humanized next-command strings too, or release output will still leak local machine paths.
- Be careful with bulk find/replace when retrofitting test call sites after signature changes. In large `main.rs` files, broad replacements can accidentally modify unrelated helper/test functions with similar trailing arguments.
- When adding CLI output-format flags in a large Rust CLI, propagate the change through all 4 layers in one pass: clap args, command-input structs, emit/print helpers, and test initializers/manual literals. `cargo check` may pass while `cargo check --tests` still fails on stale test struct literals.
- For path-leak cleanup in Rust JSON surfaces, serialize to `serde_json::Value` and recursively redact string leaves before printing. This is safer than trying to sanitize only a few top-level fields because embedded commands and summary arrays often contain duplicated path strings.
- When you claim path redaction is fixed, add explicit regression tests for the helper itself, not only CLI snapshots. Cover multiple local prefixes (at least `/Users/`, `/home/`, `/tmp/`, `/var/`, `/private/`, and macOS external volumes like `/Volumes/`), common delimiters (`space`, `,`, `;`, `|`, `)`, `]`), and nested JSON recursion via the value-walking redaction helper.
- If `workflow-status --human` still prints JSON, the flag is only surface-deep. Emit a true terminal summary (for example 3-5 text lines such as summary/block/latest/next) while keeping the richer JSON builder behind the scenes for tests and phase-specific surfaces.
- `decision_hint` strings that look like internal machine enums (`observe_only_not_comparable_to_last_analyze:...`, `market_view_is_comparable_but_factor_backlog_requires_...`) should be humanized before release. Good release copy preserves the branch meaning but reads like an action statement: observe-only due to non-comparable data, wait due to uncertainty, tune factor X first, or stable/no immediate action required.
- When adding compact/agent output for `analyze`, do not only trim arrays. Add a few high-signal top-level fields (`direction`, `entry_state`, `pre_bayes_gate`, `next_command`) so agents can route quickly without parsing the large nested report.
- For human analyze output, prepend a one-line trading-desk summary plus next-command line before the longer prose sections. This gives both fast human triage and backward-compatible detail.
- Avoid broad `replace_all` edits on test call sites when multiple helper functions share a similar trailing argument list. Search exact function names first and patch each family deliberately, or you can accidentally add arguments to unrelated helpers and create misleading compile errors.
- Cargo may rewrite HTTPS GitHub URLs to SSH via user git config. Validate git dependencies with `CARGO_NET_GIT_FETCH_WITH_CLI=true cargo check` before blaming `Cargo.toml`.
- When adding CLI output-format flags to a Rust/Clap command, wire the enum through command args, match arms, command input structs, emit functions, and all test initializers in one pass. Otherwise tests compile will fail even if `cargo check` passes.
- In large Rust entry files, avoid broad read/write rewrites during release cleanup. Use narrow patches and run `cargo check --tests` after signature/struct changes to catch test-only drift.
- A `--human` surface is not done just because a helper returns a human-oriented JSON object. Verify the CLI actually prints plain-text summary lines for human mode, not pretty JSON containing those fields.
- When the worktree is dirty and the user wants a release-hygiene-only commit, stage only the hygiene files and use a plain `git commit -m ...`. Avoid path-limited commit invocations that mention an ignored runtime artifact path after `git rm --cached`. The deletion is already staged, and adding the ignored path back into the commit command can fail or confuse the scope.
- When auditing clap help quality, do not trust a naive parser that assumes option descriptions always wrap onto the next indented line. Clap often renders short help on the same line as the flag. Cross-check both the actual `--help` output and the source `#[arg(help = ...)]` attributes before claiming parameters are undocumented.
- For repo-level signoff, prefer a mechanical audit script that enumerates subcommands from live root help, runs `<cmd> --help` for each command, parses the `Options:` block, and accepts both same-line and wrapped descriptions. Save both a machine report (`docs/audits/help-audit.json`) and a short human summary (`docs/audits/help-audit.md`) so release review is reproducible and does not depend on chat history.
- For `workflow-status`-style compact surfaces, prefer a small stable schema (`artifact_id`, `artifact_kind`, `decision_hint`, `generated_at`, disagreement `id/severity/summary`) rather than copying full artifact structs. Large release cleanups often guess nonexistent fields and break compilation because artifact/status structs drift over time.

- A `--human` mode that still prints pretty JSON is not actually human-readable release output. For audit purposes, only count it as fixed when the command emits a concise textual summary a person can scan without parsing JSON keys.
- Reconcile README/release-note claims with actual code state before sign-off. Public docs that still warn about hard-coded paths or unfinished portability work can undermine a release even after the code path was repaired.
- When migrating legacy experiment scripts into `scripts/archive/` and adding public wrappers, treat it as one atomic release surface: archive renames + new wrappers + README/docs updates must land together. If only the deletions land, the repo becomes harder to use. If only wrappers/docs land, references may point to files not yet tracked.
- For `workflow-status`-style human output, separate three concepts explicitly: focus reason, execution gate reason, and next-step text. If execution is waiting on user input rather than a hard runtime block, prefer a label like `action_blocked` / `user_input_required` over plain `blocked` so the CLI does not imply the analysis engine itself failed.
- Human `Latest:` lines should use a short derived summary (`direction=... entry=... gate=... quality=...`) while agent/json surfaces may keep the full underlying phase summary. This prevents release UIs from duplicating long `decision_hint` strings and repeated MTF details.
- Path-redaction release fixes should be accompanied by boundary tests, not only spot checks. At minimum cover all supported local prefixes (for example `/Users/`, `/home/`, `/tmp/`, `/var/`, `/private/`, `/Volumes/`) plus nested JSON recursion via the final print/redaction helper.
- In `workflow-status`-style release surfaces, do not overload `blocking_reason` with general focus rationale. Keep 3 concepts separate: focus reason (why this phase is current), hard/user-input gate reason (why execution is blocked), and next-command rationale. If no hard block is active, prefer `blocking_status=unblocked` and `blocking_reason=none` even when `focus_reason` is long and diagnostic.
- For `workflow-status --human`, if execution is blocked waiting on user input rather than a true hard runtime block, use a label like `action_blocked` / `user_input_required` instead of plain `blocked`. This avoids falsely implying the engine itself failed.
- Human `Latest:` lines should use a short derived summary (`direction=... entry=... gate=... quality=...`) instead of dumping the full persisted `phase_summary` / `decision_hint` string. Keep the full version in JSON for debugging, but print only the compact derived form in the terminal-facing human surface.
- In `workflow-status`-style release surfaces, do not overload `blocking_reason` with general focus rationale. Keep 3 concepts separate: focus reason (why this phase is current), hard/user-input gate reason (why execution is blocked), and next-command rationale. If no hard block is active, prefer `blocking_status=unblocked` and `blocking_reason=none` even when focus_reason is long and diagnostic.
- For `workflow-status --human`, if execution is blocked waiting on user input rather than a true hard runtime block, use a label like `action_blocked` / `user_input_required` instead of plain `blocked`. This avoids falsely implying the analysis engine itself failed.
- Human `Latest:` lines should use a short derived summary (`direction=... entry=... gate=... quality=...`) instead of dumping the full persisted `phase_summary` / `decision_hint` string. Keep the full version in JSON for debugging, but print only the compact derived form in the terminal-facing human surface.
- For agent-facing analyze surfaces, avoid making consumers parse a semi-structured `next_command` or raw packed `decision_hint` string when the CLI already knows the gate semantics. Keep backward-compatible raw fields (for example `decision_hint_raw` / `next_command`), but add normalized fields such as `decision_summary` plus a structured `next_step` object (`action_type`, `user_input_required`, `blocked_reason`, `prompt`, `deferred_command`). This matters especially for `ask-user: ... | blocked until ... | then ...` style commands.
- When you add structured agent fields, update README/docs to tell agent consumers which fields are canonical (`decision_summary`, `next_step`) and which are compatibility/debug only (`decision_hint_raw`, display `next_command`). Then verify with a real `--agent` run, not just unit tests.
- If you later add a matching agent surface on another command (for example `workflow-status --agent` after `analyze --agent`), keep the schema aligned instead of inventing a second near-duplicate contract. Reuse the same `next_step` shape so orchestrators do not need command-specific routing code.
- When adding new release-facing subcommands, regenerate the mechanical help-audit artifacts (`docs/audits/help-audit.json` and `.md`) in the same task. Otherwise the repo-level audit docs drift immediately even if live clap help is correct.
- Lightweight release-closure commands are worth adding before a full analytics refactor. A compact `research-verdict` (baseline, bottleneck, next experiment, contamination flag) and an `evidence-quality-breakdown` command can close major release gaps without first solving every architecture issue.
- If the primary repo cannot be pushed because GitHub rejects oversized historical artifacts, the safest release path may be a separate private release-mirror repo instead of rewriting source-repo history right before release. Export the current tree with `git archive`, initialize a clean repo in a temp dir, push that clean history to a private mirror (for example `<name>-release`), tag there, and create the GitHub Release from the mirror repo. Record this routing decision in repo docs/runbooks so future releases follow the same path intentionally.
- A clean worktree and correct `.gitignore` do NOT guarantee GitHub release readiness. Pushes can still fail on historical oversized blobs (`GH001`, >100 MB) even after runtime artifacts are removed from the current tree. Before promising "ready to release", run a remote-facing preflight or at least be prepared to diagnose `pre-receive hook declined` as a history problem, not a current diff problem.
- Git push logs can misleadingly include lines like `To github.com:owner/repo.git` even when the push ultimately fails. For release signoff, trust the final exit code / `remote rejected` lines or verify with `git ls-remote` and `gh release view`, not mid-stream watch-pattern matches.
- If release publication is blocked by historical oversized runtime artifacts (for example `state*` learning-state JSON files), the only durable fix is history cleanup (`git filter-repo` / BFG) plus force-push. Creating a private GitHub Release still requires the branch/tag push to succeed first.
