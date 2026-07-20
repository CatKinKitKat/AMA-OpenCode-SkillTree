---
name: skill-yaml-audit-fix
description: Use when auditing the agent SKILL.md files for YAML/frontmatter breakage and repairing invalid frontmatter safely at scale.
version: 1.0.0
author: the agent
license: MIT
metadata: 
tags: [skills, yaml, frontmatter, audit, repair]
related_skills: [agent-runtime-skill-athrn, systmt-dbggng]
---


# Audit and Repair SKILL.md YAML Frontmatter

## Overview

Use this when a the agent skill fails to load because its `SKILL.md` frontmatter is invalid YAML, malformed delimiters, or structurally inconsistent. The goal is to validate the whole skill tree, repair only the broken files, and keep the fixes narrow and reviewable.

## When to Use

- A skill loader reports `invalid YAML`.
- A specific `SKILL.md` fails to parse.
- The user wants a sweep across all local the agent skills for frontmatter issues.
- A large skill pack was bulk-edited and frontmatter drift is likely.

## Validation Rules

A valid `SKILL.md` must satisfy:
- Starts at byte 0 with `---`
- Has a closing `---` delimiter before the body
- Frontmatter parses as a YAML mapping
- Includes at least `name` and `description`
- Keeps the body non-empty

Common failure modes:
- Unquoted single-line `description:` containing `:`
- Folded text pasted onto one line with YAML-significant punctuation
- Missing closing delimiter
- Leading blank line before frontmatter
- Tabs or malformed indentation in `metadata`

## Audit Workflow

1. Enumerate all `SKILL.md` files under the the agent skill root.
2. Parse only frontmatter first. Do not rewrite healthy files.
3. Record each failure as:
   - path
   - failure class
   - parser error
4. Repair minimally:
   - prefer quoting or folded block scalars for long descriptions
   - preserve existing body content
   - avoid broad reformatting of unrelated sections
5. Re-run the full-tree validation after edits.
6. If no failures remain, report count scanned and count fixed.

## Safe Bulk Check Script

```bash
python - <<'PY'
import yaml, pathlib
root = pathlib.Path('~/.agent/skills').expanduser()
bad = []
for path in sorted(root.rglob('SKILL.md')):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        bad.append((path, 'frontmatter_start', 'does not start with ---'))
        continue
    parts = text.split('\n---\n', 1)
    if len(parts) < 2:
        bad.append((path, 'frontmatter_close', 'missing closing --- delimiter'))
        continue
    fm = parts[0][4:]
    try:
        data = yaml.safe_load(fm)
        if not isinstance(data, dict):
            bad.append((path, 'frontmatter_type', type(data).__name__))
    except Exception as e:
        bad.append((path, 'yaml', str(e)))
for item in bad:
    print('\t'.join(map(str, item)))
PY
```

## Repair Rules

- If a single-line `description:` contains an unescaped colon, convert it to either:
  - a quoted scalar, or
  - a folded block using `>-`
- Prefer `>-` for long prose descriptions.
- Keep line width reasonable and ASCII-first unless the file already uses non-ASCII.
- Do not rewrite the full skill body to fix a frontmatter-only issue.

## Example Fix

Bad:
```yaml
description: Long summary with a colon: and more prose that YAML misreads.
```

Good:
```yaml
description: >-
  Long summary with a colon: and more prose that YAML now treats
  as folded text.
```

## Verification Checklist

- [ ] Re-validated the edited file locally
- [ ] Re-ran whole-tree YAML/frontmatter audit
- [ ] Confirmed only broken skills changed
- [ ] Preserved body content unchanged unless body also needed repair
- [ ] Reported scanned count and fixed count

## Pitfalls

1. Do not assume the parser error line is the only bad line. Read the whole frontmatter block.
2. Do not mass-rewrite all skills just to normalize style.
3. Do not use line-number-prefixed text dumps as rewrite input.
4. Do not stop after fixing one file if the user asked for a sweep.
5. Do not claim success without re-running validation across the full skill tree.
