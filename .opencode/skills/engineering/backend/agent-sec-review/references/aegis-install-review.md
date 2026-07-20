# Aegis Method Pack Install Review

**Repo**: https://github.com/GanyuanRan/Aegis
**Commit reviewed**: `c7537ec` (Release v1.4.3)
**Date**: 2026-05-15

## Summary

Aegis is a pure markdown skill pack (19 SKILL.md files). No install scripts, package managers, binaries, or runtime executables.

## Review findings

| # | Check | Result |
|---|-------|--------|
| 1 | README / install entrypoints | README offers `aegis-doctor.py` verification script: not executed. Only SKILL.md files were synced |
| 2 | Executable / runtime files | None found in `skills/` directory. All 19 entries are `SKILL.md` only |
| 3 | Dependency manifests | No `package.json`, `requirements.txt`, `Cargo.toml`, or `setup.py` in `skills/` |
| 4 | Outbound network | No curl/fetch/requests patterns in any SKILL.md |
| 5 | Config mutation | No writes to home config, shell rc, cron, launch agents, MCP config, or auth stores |
| 6 | Credential access | None |
| 7 | Prompt injection risk | SKILL.md files contain workflow guidance only. No hostile instructions detected |

## Risk rating

**LOW**: information-only markdown skill pack with no execution surface.

## Safe install method

```bash
# Clone source (read-only review)
git clone https://github.com/GanyuanRan/Aegis.git ~/.agent/external-repos/Aegis

# Sync only skill documents to runtime
rsync -a --delete ~/.agent/external-repos/Aegis/skills/ ~/.agent/skills/aegis/
```

Do NOT run `python scripts/aegis-doctor.py` or any other executable from the repo without separate review.

## New skills in v1.4.3

- `first-principles-review`: decision review before directional choices
- `goal-framing`: thin goal frame before execution (opt-in boundary-setting)

Both are pure markdown workflow guides with no execution surface.
