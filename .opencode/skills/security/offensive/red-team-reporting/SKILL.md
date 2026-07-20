---
name: red-team-reporting
description: Produce structured red-team engagement reports: executive summary, attack path narrative, findings with CVSS/severity, evidence pack, and remediation roadmap. Use when a pentest or red-team engagement ends.
---
# Red Team Reporting

Produce structured red-team / pentest engagement reports from raw findings.

## When to Use

- [done] End of a red-team engagement
- [done] User requests an interim report
- [done] Executive summary needed for stakeholders
- [done] Remediation roadmap for technical teams

## Report Structure

```markdown
# Red Team Report - <eng-id>

## Executive Summary
Engagement dates, scope, critical/high findings count, overall risk.

## Attack Path Summary
1. Reconnaissance
2. Initial Access
3. Lateral Movement
4. Persistence
5. Data Access
6. Cleanup

## Findings Matrix
| # | Title | Severity | CVSS | MITRE | System | Remediation |

## Finding Detail (per finding)
Severity, CVSS, MITRE technique, system, proof of concept, impact, remediation.

## Evidence Pack
Screenshot/log paths.

## Remediation Roadmap
P0 (24-48h), P1 (next sprint), P2 (next quarter).
```

## Output

- pentest/<eng-id>/executive-summary.md
- pentest/<eng-id>/findings.md (full detail)
- pentest/<eng-id>/remediation.md
- pentest/<eng-id>/artifacts/
