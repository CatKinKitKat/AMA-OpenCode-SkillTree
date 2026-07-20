# External wrapper route/index parity

Use when routing or installing an external repo wrapper skill (for example a tool repo that does not ship the agent skills, but has a local wrapper under `~/.agent/skills/<category>/<name>/SKILL.md`).

Session-derived pattern
- A wrapper skill can be installed and present in `skill-router.md` / `project-router.md` while still missing from the machine-readable indexes.
- If `skill-index.json` lacks the route, downstream routing/search may fail even though `skill_view(<basename>)` works.

Parity checklist
1. Confirm `skill-router.md` has a compact high-value route line.
2. Confirm `project-router.md` records source root, runtime root, route alias, and external-source security note.
3. Confirm `skill-index.json` has exactly one entry with:
   - `name`: route alias such as `devops/cloakbrowser`
   - `path`: installed runtime `SKILL.md`
   - `source_repo` and `source_path` for external wrappers
   - `security_review: true` when future use may download binaries, run browsers, touch profiles, call APIs, or use proxies.
4. Confirm `skill-index.md` mirrors the JSON entry for human scan.
5. Verify JSON parses and paths exist.
6. Verify the runtime skill can still be loaded by basename if CLI/tooling lists only basenames.

Security note pattern
- For browser/runtime wrappers, record what was *not* run: no package install, Docker pull, binary download, profile launch, CDP server, proxy config, live-site test, credential mutation, or persistent service.

Pitfall
- Do not stop after seeing a working router line. Index absence is a real routing defect.