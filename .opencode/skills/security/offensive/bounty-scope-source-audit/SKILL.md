---
name: bounty-scope-source-audit
description: Use when auditing bounty scope CSVs, public source repos, or no-account bounty surfaces such as exposed RPC/API services; also use for HackerOne-style reports, weakness classification, and PoC zip attachments.
version: 1.1.2
author: the agent
license: MIT
metadata: 
tags: [bounty, source-audit, gread, command-injection, report-template, poc-zip]
---


# Bounty Scope Source Audit

## When to Use

Use for:
- scope CSV / 漏洞赏金 scope / bounty scope
- 按 scope 挖源码漏洞
- GitHub 开源仓库审计
- no-account / 不需要账号的公开 RPC、API、service 暴露验证
- CLI / helper script 命令注入
- HackerOne / Report Intent 表单
- 需要 PoC zip 附件

Do not use for broad live target probing. This skill is source-first. Live checks must be in-scope, low-volume, read-only, and tied to a source/config hypothesis.

## Core Workflow

1. Parse scope CSV first. Filter `asset_type == SOURCE_CODE`.
2. Rank by bounty eligibility first, then bounty tier, then direct project relevance.
3. Split rows into three buckets before reading code:
   - `eligible_for_bounty == true` and `eligible_for_submission == true`
   - `SOURCE_CODE` but not bounty-eligible
   - non-source rows that still name a repo/path and may help orient the tree
4. Pick one repo first. Do not spray all repos.
5. Map repo tree, then grep narrow sinks:
   - `execSync`, `exec(`, `spawn(`, `shell: true`
   - `eval(`, `new Function`
   - `readFileSync`, `writeFileSync`, `path.join`, `path.resolve`
   - `dangerouslySetInnerHTML`, `innerHTML`
   - archive extraction: `tar`, `unzip`, `extract`
   - web/API routes: look for `parseEntity`, `parameters(...)`, `path(...)`, `get`, `post`, and any default `reference.conf` that turns a feature on by default.
6. Prove one narrow end-to-end flow before expanding.
7. Classify only after proof. Prefer `confirmed`, `high-risk design`, or `false lead`.
8. If the target has a standalone launcher, verify the exact run entrypoint and config file instead of assuming `sbt test` is the fastest proof path.
9. If a route wrapper exists, inspect the wrapper config too. Permissive defaults like wildcard CORS often live outside the route file.
10. If no new same-grade finding after one high-risk sweep, stop and formalize report.
11. Before treating a signature / auth check as real, verify the effective runtime knob and shipped defaults. A validator behind a default-off feature flag is not proof of enforcement.
12. If local regression tests need infra tools such as `atlas`, note the environment gap and keep the source conclusion separate from the failed runtime check.

## Session References

- `references/lightspark-withdrawal-validation.md`: withdrawal-validation finding and verification caveat.
- `references/no-account-open-source-bounty-triage.md`: triage pattern for “no account needed” bounty scope work, including source-first findings and no-account service risks.
- `references/privy-no-account-postmessage-triage.md`: Privy/npm package no-account triage: postMessage origin/source validation, popup trust boundaries, and OAuth `redirect_to` candidates.
- `references/moonpay-agent-skill-supply-chain.md`: MoonPay org-level SOURCE_CODE triage with explicit ineligible repo overrides, GitHub org repo enumeration, and `http://... | sh` agent-skill supply-chain finding pattern.
- `references/chainlink-no-account-source-audit.md`: scope CSV triage and code-map notes from the Chainlink session. Useful as a worked example of filtering `SOURCE_CODE` rows, prioritizing bounty-eligible assets, and proving one unauthenticated adapter path.
- `references/plaid-no-account-source-audit.md`: SDK/client source audit pattern where the user wanted ready markdown reports plus executable PoC files and a zip archive.

## No-account bounty triage

When the user asks for bugs that do not need prepared accounts:
- Start from the scope CSV and separate `SOURCE_CODE` targets from live web/mobile targets.
- Prefer public open-source repos and unauthenticated local/service endpoints over member-only flows.
- Do not assume every in-scope row is equally good: rows marked `OTHER` may still name repos, but `asset_type == SOURCE_CODE` is the cleanest first pass.
- After command-injection/eval sweeps, also search for unauthenticated route registration, default CORS, request-body aggregation, compression/decompression, publish/write APIs, and config defaults.
- For SDKs and client libraries, inspect remote script loaders, platform-specific redirect/OAuth bridges, and token-to-handler propagation before hunting broader auth flaws.
- For source-first conclusions, distinguish `confirmed`, `high-risk design`, and `needs runtime proof`. Do not present a config-default concern as a confirmed vuln until local or documented deployment behavior is reproduced.
- For browser popup / `postMessage` flows, treat `event.origin` and `event.source` as mandatory checks. `event.data.type` alone is not enough.
- If the only proven impact is spoofed connection state or forced request failure, score it conservatively as Medium unless token theft or signed transaction execution is shown.
- See `references/privy-cvss-postmessage.md` for the CVSS pattern used in this session.
- See `references/plaid-no-account-triage.md` for the Plaid SDK session pattern: no-account triage, source loader trust boundaries, and why several candidates stop at high-risk design.


## No-account service/RPC exposure triage

Use this when a scope row names a public RPC/API host and the user wants no-account findings:
- First inspect source/config/docs for the intended public-safe surface: default bind address, enabled modules, middleware/interceptors, auth flags, TLS/mTLS, and safe/unsafe namespace lists.
- Confirm live behavior only with low-cost read-only requests. For JSON-RPC, start with `rpc_modules`, `web3_clientVersion`, `net_version`, `eth_chainId`. Then prove one exposed sensitive method with bounded output.
- Safe read-only examples: empty `trace_call`, `debug_getRawHeader latest`, `debug_getRawBlock latest`, `txpool_status`, truncated `txpool_content`.
- Avoid mutating or risky methods such as `admin_addPeer`, `admin_removePeer`, debug verbosity/GC controls, broad historical tracing, fuzzing, or high-rate polling.
- Record negative results too. If `admin_*` is blocked but `trace_*` works, report only the confirmed exposed methods and bound the impact.
- Classify exposed dangerous RPC methods as `Exposed Dangerous Method or Function (CWE-749)`. Use `CWE-200` only when the primary proven impact is sensitive data disclosure rather than dangerous functionality exposure.

## Unauthenticated signer/service triage

Use this for remote signers, callback signers, validators, and cryptographic service sidecars:
- Trace the public server registration, default bind address, proto/interface, middleware/interceptor chain, and handler validation before claiming exposure.
- Prove the boundary with a local harness when real keys are unnecessary: instantiate the public server with a fake backend and show a client with no metadata, no token, and no client certificate reaches the critical handler.
- Classify unauthenticated access to signing or key-use operations as `Missing Authentication for Critical Function (CWE-306)`.
- Impact wording must be precise: unauthorized signing capability is not the same as private-key extraction.
- Before reporting, verify there is no effective default-on mTLS, bearer token, peer allowlist, proxy auth, or deployment wrapper that blocks the handler.

## No-account / pre-login attack surface

Use this section when the user wants findings that do not require preparing a target account.
Typical targets:
- install/update scripts
- auth bootstrap flows before token issuance
- repo-local config ingestion that still runs before login
- downloadable executables and shell wrappers

What to verify first:
1. Whether the flow can be reached with only the shipped binary/script and no account.
2. Whether remote data becomes a shell command, file path, or executable payload.
3. Whether signature or checksum validation is actually enforced before execution.
4. Whether a browser-open / auth-url helper is just UX or a real trust boundary.
5. Whether the path still needs an existing token, project, config, or dashboard session.

Common pitfall:
- A remote install script is interesting only if you can prove a bypass of verification, path control, or command construction. "Downloads and executes remote script" alone is not enough.

Session note:
- See `references/doppler-no-account-audit.md` for the Doppler CLI no-account triage flow and the decisive file map.
- See `references/supabase-storage-x-forwarded-host.md` for a trusted-proxy-header tenant-routing example and two false leads from the same session.

## Signed webhook / callback replay triage

Use this when the target is a signed webhook, callback, or remote-signing handler:
- Signature validity is necessary, not sufficient.
- If the payload includes `timestamp`, prove whether the implementation enforces freshness.
- If the payload includes `event_id` / nonce / UUID / delivery id, prove whether replay dedupe exists.
- For action-executing handlers, prove the downstream side effect still fires on a replayed signed payload.
- When a fixture is shipped in the repo, recompute the signature independently with `node:crypto` first. Do not rely on workspace package-manager state for a basic HMAC proof.
- See `references/webhook-replay-triage.md` and `scripts/verify-webhook-replay.mjs`.

## Gread Pattern

Use `research/gread` for public GitHub source:

```bash
curl -s 'https://api.gread.dev/repo?name=owner/repo'
curl -s 'https://api.gread.dev/grep?name=owner/repo&q=execSync&i=true&F=true&C=3&path='
curl -s 'https://api.gread.dev/read?name=owner/repo&paths=path/to/file.ts'
```

If punctuation queries fail, retry simple tokens (`execSync`, `spawn`, `shell`) and narrow `path`.

## Command Injection Triage

High confidence requires all of:
- user-controlled CLI arg, env var, URL, config, file path, or repo content
- reaches shell string (`execSync(command)`, `exec(command)`, `spawn(..., {shell:true})`)
- no strict allowlist or argv separation before sink
- proof that metacharacters survive to shell (`$()`, backticks, `;`)

Local CLI RCE severity defaults:
- Weakness: `OS Command Injection (CWE-78)`
- CVSS 4.0: `AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`

## PoC Zip Pattern

Provide safe PoC zip with:
- `README.md`
- `poc-live.sh` when live package execution is practical
- `poc-offline.js` or equivalent proving vulnerable command construction

For signed webhook / callback replay findings, include a self-contained PoC zip even when package-manager installs are unavailable. The zip should prove all of:
- the shipped fixture or raw payload is valid under `node:crypto`
- the payload is stale/replayable because freshness is not enforced
- the downstream handler path is the one that would still execute after verification

Safe marker pattern:
```bash
PAYLOAD='$(touch ./poc-owned)'
```

Avoid destructive commands. Write only temp marker files.

Zip:
```bash
cd /path/to/poc-dir
zip -r ../finding-poc.zip .
unzip -l ../finding-poc.zip
```

When the user says they want "markdown" and "poc", create filesystem deliverables rather than only printing text in chat:
- one `.md` report per finding using the HackerOne template
- `poc/<finding>/README.md`
- one executable, deterministic PoC script per finding
- a zip containing all reports and PoCs
- run each PoC locally and include only decisive verification lines in the final response

For source-only SDK/client findings where live exploitation would require a link token, account, or mobile runtime, prefer static PoCs that prove the exact source sink and sensitive field shape. Label the runtime limitation in the report instead of overclaiming.

## CVSS 3.1 for bounty reports

When the platform asks for the eight CVSS 3.1 metrics, provide them explicitly before giving the score.

For client-side postMessage / popup trust bugs, default conservatively unless the proof shows token theft or transaction execution:
- Attack Vector: Network, if exploit is delivered through web content / browser messaging.
- Attack Complexity: Low, if a forged message with the right `type` is enough.
- Privileges Required: None, if no attacker account or target tenant access is needed.
- User Interaction: Required, if the victim must open the dApp or trigger the popup flow.
- Scope: Unchanged, unless the exploit crosses into a different security authority with proven downstream impact.
- Confidentiality: None unless secrets/tokens/user data are exposed.
- Integrity: Low for wallet identity spoof, forged connection state, or UI/security-state manipulation. High only with proven unauthorized transaction/signature execution.
- Availability: Low for forced flow failure/DoS of signing or transaction requests. High only if durable service outage is proven.

Always include the vector string, score, and severity label. Example:
`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:L = 5.4 Medium`.

## Weakness Classification Rules

The report `Weakness:` field must be a single clear weakness, not a slash-separated bundle.

Format:
`Weakness: <specific weakness name> (CWE-<id>) - <one concrete vulnerable action/surface>`

Good examples:
- `OS Command Injection (CWE-78) - CLI revision reaches shell command construction`
- `Missing Authentication for Critical Function (CWE-306) - unauthenticated access to validator signing`
- `Exposed Dangerous Method or Function (CWE-749) - public JSON-RPC exposes trace/debug/txpool methods`
- `Exposure of Sensitive Information to an Unauthorized Actor (CWE-200) - unauthenticated endpoint returns pending transaction contents`

Rules:
- Pick the CWE that matches the proven sink/impact, not the broadest narrative.
- If two CWEs seem plausible, choose the primary one and mention the secondary effect in Summary or Impact.
- Add one sentence in Summary: `The concrete weakness is CWE-...: ...`
- Avoid vague labels like `Improper Restriction`, `Information Exposure`, `Auth issue`, or `Access Control` unless the platform forces that exact taxonomy.

## HackerOne-Style Report Template

Use this exact markdown skeleton for submissions:

```markdown
# <descriptive title>

Asset: <scope asset root, e.g. https://github.com/vercel/next.js>
Weakness: <weakness name, e.g. OS Command Injection (CWE-78)>
Severity: <Low|Medium|High|Critical>
Affected version(s): <exact version or range>
Affected file: <blob URL to the vulnerable file>

## Summary
<1-3 short paragraphs. State the source, sink, and why it is unsafe.>

## Expected vs. Actual Behavior
Expected:
- <expected safe behavior>
- <validation or escaping that should happen>

Actual:
- <what really happens>
- <what the shell or runtime executes>

## Steps To Reproduce
1. <setup>
2. <command or request>
3. <observe result>
4. <explain why this proves the bug>

```bash
<exact reproduction command>
```

## Attack Scenario
<Explain how a realistic attacker influences the parameter: copied command, wrapper script, CI, docs, chat, issue comment, etc.>

## Impact
<Concise impact statement. Mention who is affected and what an attacker can do.>

## Supporting Material / References
- PoC zip: <local path or attachment reference>
- Repository file: <blob URL>
- Entry point: <blob URL>
```

## Description Field Rule

When the user asks for a bounty report `description`, output the full markdown body, not a prose-only paragraph. Always include these sections in order:

```markdown
## Summary
...

## Expected vs. Actual Behavior
Expected:
- ...

Actual:
- ...

## Steps To Reproduce
1. ...

```bash
...
```

## Attack Scenario
...

## Impact
...

## Supporting Material / References
- Asset: `...`
- Affected file: `...`
- Entry point: `...`
- Affected version: `...`
```

If the user says "description", assume the report platform's description/body field and provide this complete sectioned markdown block.

## Common Mistakes

- Do not leave report-platform default titles like `Report Intent #...`. Use a descriptive vuln title.
- For Asset, use the exact in-scope asset string from the scope table (often the repository root such as `https://github.com/org/repo`), then put file/blob URLs under affected files or references.
- Include Expected vs. Actual behavior in reproduction steps.
- Explain how an attacker realistically influences the vulnerable parameter.
- Use markdown code blocks for commands and vulnerable snippets.
- Do not report examples/tests unless they are shipped and reachable.
- Do not claim RCE from `execFileSync` with argv array unless a shell is involved.
- Do not rely on comments. Prove live source-to-sink flow.
- Do not paste massive logs. Include decisive lines and PoC zip.
- Do not over-sweep all repos before proving one chain.
- Do not leave `Weakness` vague or multi-headed. Use one CWE-backed weakness and make the vulnerable surface explicit.
- For signed webhook paths, do not stop at HMAC verification. Check freshness and replay uniqueness too.
- If the repo's package manager is unavailable, fall back to a self-contained `node:crypto` proof instead of treating that as a blocker.

## This Session Pattern

Confirmed examples:
- `@next/codemod upgrade [revision]`: `revision` -> `resolveSemanticRevision()` -> `execSync("npm view ...")`
- `svelte` playground download helper: URL owner/repo -> `repo_url` -> `execSync("git clone ...")`
- `@ai-sdk/codemod`: CLI args -> `buildCommand()` -> `execSync(command)`
- Remote signer public gRPC: default public listener + no auth interceptor + `Sign` only validates non-empty message -> `CWE-306`.
- Public blockchain JSON-RPC: source says public-safe modules exclude trace/debug/txpool, live read-only probes confirm exposed methods -> `CWE-749`.
