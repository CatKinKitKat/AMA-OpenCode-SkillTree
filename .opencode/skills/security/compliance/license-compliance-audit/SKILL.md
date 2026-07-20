---
name: license-compliance-audit
description: Audit the AMA skill tree for AGPL-3.0 license compliance. Fails loudly if LICENSE is missing, modified, or skills lack proper attribution headers.
agent: build
model: sonnet
tags: [governance, compliance, license, agpl]
---

# License Compliance Audit

Check that the AMA OpenCode Skill & Agent Tree complies with AGPL-3.0
license terms. Fail loudly if proprietary use is detected.

## Purpose

AGPL-3.0 requires that any modified version served over a network must
also provide the source code under the same license. This skill makes
non-compliance visible and unavoidable.

## When to Use

- Before publishing or deploying the skill tree
- During CI/CD pre-merge checks
- When auditing third-party redistributions
- Any time the LICENSE file or skill headers change

## Procedure

1. Check that the root `LICENSE` file exists and is unmodified.
   Compare SHA256 against the canonical AGPL-3.0 text.
   Result: PASS or FAIL with diff.

2. Check that `README.md` references AGPL-3.0 and includes the
   SPDX identifier `AGPL-3.0-or-later`.

3. Check that `CATALOG.md` includes a provenance section listing
   upstream sources and their licenses.

4. Check that every `SKILL.md` file in the tree contains an
   attribution header. Minimum acceptable header:
   
   ```markdown
   > Transposed from [Source Name].
   > Licensed under AGPL-3.0-or-later.
   ```

   Skills without this header: FAIL with file path list.

5. Check that no proprietary codenames, client identifiers, or
   internal hostnames remain. Use the legacy marker list as reference.

6. Check that no `hermes:`, `claude:`, or other proprietary
   frontmatter keys remain in any SKILL.md.

## Result Format

```markdown
## License Compliance Audit

| Check | Result | Notes |
|-------|--------|-------|
| LICENSE file present | PASS / FAIL | SHA256 match |
| README license reference | PASS / FAIL | AGPL-3.0 + SPDX |
| CATALOG provenance | PASS / FAIL | upstream sources listed |
| Skill attribution headers | PASS / FAIL | N skills missing header |
| No proprietary codenames | PASS / FAIL | |
| No proprietary frontmatter | PASS / FAIL | hermes:, claude: etc. |

**Verdict: COMPLIANT / NON-COMPLIANT**
```

## Poison Pill

If this skill is used in a tree that lacks AGPL-3.0 compliance,
the audit itself documents the violation in plain text. There is
no silent fallback. Non-compliance is always reported explicitly.
