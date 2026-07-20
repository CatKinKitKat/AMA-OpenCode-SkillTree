# External skill repo intake: routes + index

Use when importing GitHub repos that ship plain `SKILL.md` trees and need Chinese trigger routing.

Pattern proven in session:
1. Route first: read `skill-router.md`, `project-router.md`, nearest `AGENTS.md`. Choose `agent-runtime-sec-review` primary for external repos, then `agent-runtime` + `skill-routing-gov` for the agent routing work.
2. Claim shared worklog before changes when AGENTS requires coordination. Use `~/.agent/routing/skill-governance.md` if no more specific doc exists.
3. Clone source under `~/.agent/external-repos/<repo>`. Do not run installers before review.
4. Review minimum: `README*`, `SKILL.md`, executable scripts, dependency manifests, CI workflows, outbound URLs, local writes, credential/env handling.
5. Classify risk. Markdown-only skill repos with local scripts and outbound public fetches are commonly MEDIUM, not LOW, when they can mutate local agent state or deliver to Telegram/email.
6. Before copying, scan live `~/.agent/skills/**/SKILL.md` frontmatter names for collisions with incoming skill names. If a collision exists, choose a pack-scoped runtime basename (for example `finance-skill-creator`), rename both the directory and frontmatter `name:`, and record the upstream name in the worklog/index.
7. Copy runtime skill into class namespace under `~/.agent/skills/<category>/<pack>/<skill-name>`. Keep source clone separate. Copy only reviewed skill directories, not repo-level OpenCLI adapters, install scripts, or web apps unless the user explicitly asks for runtime/tool installation.
8. If scripts have a lockfile and are needed for verification, install deps in the copied runtime skill with `npm ci --ignore-scripts`. Avoid lifecycle-script execution unless reviewed and necessary. If the task only installs markdown skills, do not run package managers.
9. Patch `skill-router.md` with compact high-value Chinese triggers.
10. Patch `project-router.md` with source root, runtime root, route alias, rename notes, and external-source security note.
11. Patch/create `skill-index.json`. If active `skill-index.json` is absent but a trusted backup exists, rebuild active index from the backup plus new entries, then generate `skill-index.md` from JSON. Mark entries `security_review: true` when future use may touch APIs, browser/CDP state, social accounts, credentials, wallet/funds, or trading/market-data tools.
12. Verify both runtime loading and behavior:
    - count copied `*/SKILL.md` files per pack.
    - assert every index path exists and the new pack has no duplicate runtime `name:` collisions.
    - `skill_view(<basename>)` works even if router alias is shorter/different. Use it as the authoritative runtime probe if broad `agent skills list` is slow or times out.
    - `agent skills list` shows representative enabled skills when it completes.
    - run bundled smoke tests or deterministic read-only/report commands only if they do not require unreviewed adapters, credentials, browser sessions, API calls, or side effects.
    - grep router/index for new trigger phrases and paths.
13. Mark worklog Done with outputs and verification evidence.

Pitfalls:
- Do not mirror into another host agent's skill directory unless explicitly requested.
- Do not conflate route alias with runtime basename. Record both where they differ.
- Do not make `skill-index.md` the source of truth. Generate it from JSON or keep it clearly secondary.
- Do not schedule cron/delivery as part of install unless the user asked for onboarding/operation.
