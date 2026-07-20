---
name: skill-routing-gov
description: >
tags: 
version: 1
---


Goal
- Turn a pile of skills into a routed system.
- Ensure the agent loads the right skill early instead of vaguely knowing many skills exist.
- Keep AGENTS.md thin while making routing durable and updateable.

Use when
- The user wants broad routing coverage across many skills.
- New skills are being added and trigger rules are starting to drift.
- AGENTS.md needs a central routing table or references to routing docs.
- You want every non-trivial task type to have a preferred skill path.

Do not use when
- There are only a few skills and routing can remain implicit.

Core routing policy
1. Separate hard rules from routing tables.
2. Keep AGENTS.md compact:
   - global hard rules
   - graphify/project rules
   - one short mandatory skill-routing section
3. Put large routing catalogs in a dedicated markdown file.
4. Create one canonical router skill that explains:
   - how to choose a skill
   - which domains map to which skills
   - how to update routes when a new skill appears
5. New skill rule:
   - when creating a durable new skill, also update the central routing catalog if the skill has clear trigger conditions.
   - when routing a local external skill tree, write the stable absolute skill-root path into the routing catalog. Do not leave the mapping in `/tmp/*`, chat text, or one-off shell heredocs.
   - if the packaged skill registry may not contain that skill, the router must say to load the local `SKILL.md` directly from the mapped path.
   - when the same external skill exists both in an installed the agent runtime tree and in an upstream local repo clone, record both roots and state which one is runtime truth.
   - if a user reports a recurring skill-load failure, record the exact accepted call-name form and any forbidden aliases in the router docs.
   - if skill docs themselves mention slash commands or trigger commands, normalize those examples to include both the the agent runtime route name and the slash-command form when that distinction matters.
   - when you bulk-normalize command references across a skill pack, also normalize frontmatter `触发方式` / trigger lines so the header does not drift from the body.
   - for large-scale header rewrites, do not rely on tool outputs that inject line-number prefixes into file text. First verify the read path returns raw frontmatter bytes or switch to a file-access method that preserves exact content.
   - if generic slash aliases do not actually exist for a skill, encode the fallback explicitly as `通用 slash command /skill <route>` instead of inventing a dedicated slash command.
   - for any new skill, the canonical full route name (short prefix + basename, or full path if unshortened) must stay under 64 characters.
   - target <=60 characters by default. Prefer <=50 when practical to preserve buffer for future namespace changes.
   - if a proposed route would exceed 60, shorten category prefixes and/or basename before the skill is published or routed.
   - for local CLI tools, MCP servers, binaries, or editor/tooling repos that are not the agent skills but have stable high-value trigger phrases, install/configure the tool itself when requested and add a pseudo-route in `skill-router.md`, `project-router.md`, and `skill-index.{json,md}` with `category: local-tool`, absolute repo path, installed binary paths, first probe commands, and safety notes. Do not create a the agent `SKILL.md` wrapper just to make a tool visible. Only create a wrapper when the user explicitly wants reusable workflow instructions rather than the tool. Example classes: port/process inspection CLIs such as `ports`/`whoisonport`, and MCP server binaries such as `fff-mcp`.
6. Shared iteration feedback rule:
- when an external agent discovers a missing step, better trigger phrase, or workflow/routing gap, write it first to a governance inbox candidate instead of silently losing it.
   - when a user corrects a routing mistake, stale gate/readback interpretation, deleted/retired field, trigger wording, or reusable workflow rule, update the governing skill/rule in the same task so the lesson becomes durable.
   - every durable skill-related change has two sync checks: update the relevant runtime `SKILL.md` or reference for reusable knowledge, and update `skill-router.md` / `project-router.md` / `skill-index.{json,md}` when discovery, aliases, paths, or trigger behavior changed.
   - do not acknowledge a correction in chat while leaving the active runtime skill stale. Either patch the relevant runtime skill/reference before finishing, or explicitly report why no durable skill surface exists.

Routing design pattern
- Layer 1: universal priorities
  - security review before trusting external repos/tools/skills
  - project-specific mandatory skills before generic ones
  - compact/cheap paths before expansive ones
- Layer 2: domain router
  - software-development
  - github
  - research
  - productivity
  - media
  - apple
  - etc.
- Layer 3: task trigger phrases
  - concrete user intents, artifacts, file types, repo states, or failure modes that should activate a skill

Required outputs when applying this skill
1. Audit current skills.
2. Group them by domain and trigger condition.
3. Produce a canonical routing markdown file.
4. Produce a skill index (`.agent/routing/skill-index.json` and/or `.md`) that records, at minimum, for each skill: grade (good/middling/bad), trigger phrases, priority, supersedes/overlaps, and whether security review is required first.
5. If working under `~`, also produce a local-project router at `.agent/routing/project-router.md` covering high-value repos, nearest `AGENTS.md`/`AGENTS.md`, project-specific command constraints, and preferred project-local skills.
6. If package-manager-installed workspaces are in play (Homebrew, npm global, npx cache, site-packages), also add package-prefix routing and, for npm global, a dedicated `.agent/routing/npm-global-router.md` catalog when package count is non-trivial.
   - For npm CLIs that ship their own agent skill/extension paths (e.g. commands with `info`, `path`, or `skill` subcommands), record the exact global binary, package version, shipped `SKILL.md`, extension/server path, health endpoint, trigger phrases, and first probe command in `npm-global-router.md`.
   - Add a short backlink in the central `skill-router.md` so generic trigger phrases (for example real-browser/CDP/relay wording) route to the npm-global router instead of staying implicit.
7. Update AGENTS.md with a thin routing rule that points to the canonical router and, for `~`, also to the project router.
8. Add thin global-routing backlink sections to high-value local project entry docs (`AGENTS.md` / `AGENTS.md`) so repo-local instructions point back to the canonical global routers without copying their full contents.
9. If needed, create or patch a router skill so the agent can explicitly load it.
10. State the maintenance rule: any new skill with stable triggers must also update routing docs. Any newly identified high-value local project with stable workflow rules must update the project router in the same task. Meaningful npm global package routes must update the npm-global router in the same task.
11. If the user bulk-renamed skills, rebuild routing by the current runtime path names, not by remembered historical names.
12. For full-library refreshes, treat `category/.../basename` as canonical runtime identity. `skill-index.json` must cover every live non-archived `SKILL.md`, and `skill-index.md` must mirror that set for human scan.
13. If archives or retired trees live under the same skill root, exclude them from active routing unless the user explicitly asks to route archives.
14. Verification must include set equality: active skill paths on disk == names listed in `skill-index.json`.
   - On this host, run `python3 ~/.agent/routing/verify-skill-index-parity.py` after any skill add/remove/rename or any routing/index edit.
   - Treat non-zero output from that parity check as a hard stop: update `skill-index.json` and regenerate `skill-index.md` before reporting the routing work as complete.
15. When broad routing is requested, do not stop after curating a high-value subset. Rebuild the full index and then keep the narrative router compact, pointing to the machine index for exhaustive coverage.
16. When a user asks to maintain all skills, the minimum audit is: parity check, stale high-risk token/schema scan for the reported issue, targeted runtime skill/reference patch if needed, and a final parity check if any skill or routing file changed.

Recommended files
- `.agent/routing/skill-router.md`
- top-level `AGENTS.md` with a short route-to-router rule
- optional skill: `skill-routing-gov`

Minimal AGENTS.md pattern
- Before choosing a workflow skill, read `.agent/routing/skill-router.md` when the task is non-trivial, cross-domain, or likely covered by an existing skill.
- When creating a new durable skill, update `.agent/routing/skill-router.md` in the same task.

Maintenance checklist
- Does each high-value skill have explicit trigger phrases?
- Are overlapping skills ordered by preference?
- Are project-specific skills preferred over generic skills where appropriate?
- Are stale or low-quality skills demoted in routing?
- Did a newly created skill get a routing entry?
- If a route depends on a local external skill tree, is the real absolute path recorded in router docs?
- Did any user-reported routing failure get folded back into the governing skill in the same task?
- If the user explicitly rejects or uninstalls a skill pack, remove active runtime paths, symlinks, caches, and index/router references. Verify active routing no longer matches it. Record a compact preference/memory so future agents do not restore it. Do not delete unrelated historical backups or source mentions unless they are active routing/install surfaces.

External skill-system intake pattern
- Reference: `references/external-skill-intake-routes-index.md` captures the concrete GitHub `SKILL.md` repo intake pattern for source clone, security review, runtime copy, Chinese routing, index rebuild, and verification.
- Reference: `references/external-wrapper-index-parity.md` captures the parity check for external repo wrapper skills: router line + project-router record + `skill-index.json` + `skill-index.md` must all agree. A working `skill_view` is not enough.
- For external "skill OS" / agent-runtime repos, prefer Learn + Absorb before Install.
- Treat host-target installers that write into real agent homes (`~/.codex`, `~/.the agent`, `~/.cursor`, etc.) as security-sensitive. Require isolated `--target-root` or equivalent before any install.
- Absorb governance contracts before runtime stacks: primary route before specialist dispatch, M/L/XL-style execution grades, promotion eligibility metadata, destructive-prompt blocks, replay-ledger-before-promotion, proof bundles, and workspace/shared-memory single-control-plane rules.
- If targeted verification exposes failing promotion gates, live degraded-result freeze failures, or host-path canonicalization mismatches (e.g. macOS `/private/var` vs `/var`), classify the repo as reference-only until fixed.

External repo-to-the agent skill intake pattern
- Reference: `references/batch-external-skill-pack-intake.md` captures the multi-repo batch pattern: canonical skill-root selection, large-pack prefixing, wrapper-only installs for high-side-effect repos, four-surface routing/index sync, and parity repair.
- For GitHub repos that ship plain `SKILL.md` trees, clone source under `~/.agent/external-repos/<repo>` first, then copy only the skill directories into a class namespace under `~/.agent/skills/<category>/<pack>/<skill-name>`. Do not run package-manager installs just to make markdown skills visible.
- For repos with many host-specific mirrors or translated docs, prefer the canonical top-level `skills/*/SKILL.md` tree. Do not copy `.opencode/`, `.cursor/`, `.kiro/`, docs translation skill mirrors, or generated outputs unless the user explicitly asks for that surface.
- For large imported packs likely to collide with existing basenames, prefix imported runtime names/directories (for example `ecc-<skill>`) and expose them through a compact class alias (`comm/ecc/...`) in the index.
- For repos that are useful runtime/tools but do not ship the agent skills, first decide whether the user asked to install the tool or to create durable workflow instructions. If they asked for the tool, install/configure the binary/MCP/server and record a `local-tool` pseudo-route. Do not fabricate a `SKILL.md` wrapper. Create a class-level wrapper skill only for reusable operating procedures that the agent should load as instruction text.
- For imported packs, rebuild both `skill-index.json` and `skill-index.md` with route aliases, source paths, stable trigger phrases, and `security_review` status. Include Chinese triggers for the user's likely phrasing, not only upstream English names.
- Patch `skill-router.md` with compact high-value routes, and patch `project-router.md` with source roots, runtime skill roots, route aliases, and the security rule for external sources.
- Verify after intake with: source repo existence, copied `*/SKILL.md` counts, wrapper `SKILL.md` existence, index entries, missing path scan, and at least one `skill_view` load from each new pack/wrapper.
- If a CLI listing only shows basename skills (not route aliases), treat `skill_view(<basename>)` as the runtime probe while preserving shorter aliases in router/index docs.

Pitfalls
- Do not dump all skill contents into AGENTS.md.
- Do not create vague routes like "use for coding".
- Do not leave routing implicit once skill count is large.
- Do not add a new skill without deciding whether it needs a router entry.
- Do not install polished external skill/runtime repos just because their README promises governance. Verify installer side effects and at least one targeted gate.
