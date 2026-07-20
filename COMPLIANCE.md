# AMA Compliance Requirements

This repository and all skills within it are licensed under
**GNU Affero General Public License v3.0 (AGPL-3.0-or-later)**.

## What This Means

If you use, modify, or redistribute these skills:

- You must keep the AGPL-3.0 license on all copies and derivatives.
- If you run a modified version over a network (e.g., in an agent workflow),
  you must make the modified source code available under the same license.
- You must preserve attribution in every skill file.

## Required Attribution

Every `SKILL.md` must contain:

```markdown
> Transposed from [source name].
> Licensed under AGPL-3.0-or-later.
```

## Prohibited Actions

- Removing or altering the LICENSE file.
- Removing attribution headers from individual skills.
- Using the skills in proprietary software without releasing modifications
  under AGPL-3.0.

## Audit

Run the `license-compliance-audit` skill to verify compliance:

```
/run license-compliance-audit
```

Non-compliance will be reported explicitly. There is no silent pass.
