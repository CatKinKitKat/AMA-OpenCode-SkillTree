# Batch external skill-pack intake pattern

Session pattern captured from a 7-repo intake into the agent runtime.

## Repos handled
- Plain skill packs: `planning-with-files`, `stop-slop`, `taste-skill`.
- Large skill OS pack: `ECC`.
- Reference/runtime repos without the agent-native skills: `the agent-code-harness`, `ai-engineering-from-scratch`, `codex-session-patcher`.

## Durable pattern
1. Clone/update sources under `~/.agent/external-repos/<repo>` and record commit SHAs.
2. For repos with canonical `skills/*/SKILL.md`, copy only that canonical skill root, not hidden host-specific mirrors (`.opencode/`, `.cursor/`, `.kiro/`, docs translations) unless the user explicitly asks for those surfaces.
3. For large packs likely to collide with existing skill basenames, rewrite imported frontmatter names and directory basenames with a pack prefix (example: `ecc-<skill>`), then route through a class alias (`comm/ecc/...`).
4. For repos that are useful but high-side-effect or not the agent-native, create a class-level wrapper skill instead of running installers or copying host hooks. Include upstream URL, local source path, reviewed commit, safe-use rules, and explicit non-execution notes.
5. Update all four routing surfaces together: `skill-router.md`, `project-router.md`, `skill-index.json`, and `skill-index.md`.
6. Run `python3 -m json.tool ~/.agent/routing/skill-index.json` and `python3 ~/.agent/routing/verify-skill-index-parity.py` before reporting completion.
7. If parity reveals pre-existing missing live skills, repair those index entries in the same pass. Do not leave global parity red because the current batch succeeded.

## Safety notes
- Do not run upstream installers, package managers, bundled binaries, hook activation, MCP launch, Web UI launch, session patching, or prompt injection during intake unless explicitly approved.
- Treat session patchers and prompt-injection/profile-injection tools as HIGH-risk runtime tools even when installing only a wrapper.
- Wrapper-only install can satisfy routing/index discovery while preserving a human approval gate for runtime mutation.

## Verification evidence to record
- Source roots and commit SHAs.
- Runtime counts per pack.
- Route alias families.
- JSON parse pass.
- Parity output with `missing=0` and `stale=0`.
- Representative `skill_view` probes for copied pack, wrapper, and prefixed large-pack skill.
