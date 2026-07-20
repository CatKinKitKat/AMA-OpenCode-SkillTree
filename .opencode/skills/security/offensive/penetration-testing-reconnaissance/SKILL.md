---
name: penetration-testing-reconnaissance
description: High-level pentest methodology: scope validation, threat modeling, and execution workflow (recon -> enumeration -> exploitation -> reporting). Use when starting a new engagement or briefing the methodology to stakeholders.
---
# Penetration Testing Reconnaissance

High-level methodology: scoping, recon, enumeration, exploitation, and reporting.

## When to Use

- [done] Starting a new authorized pentest engagement
- [done] Briefing stakeholders on testing methodology
- [done] Planning multi-phase red team engagements
- [done] Setting up the engagement workspace

## Scope Validation

Before any scan verify: authorized IPs/domains, authorized techniques, off-limits systems, communication protocol, evidence handling.

## Methodology

### Recon
Passive: ViewDNS, SecurityTrails, Shodan, Archive.org
Light active: nmap top-1000, nuclei, subfinder

### Enumeration
Per service: HTTP - WhatWeb/ffuf/wpscan/nuclei. SMB - smbclient/smbmap. LDAP - ldapsearch. SSH - ssh-audit

### Vulnerability Identification
CVE lookup: searchsploit, Nuclei, OpenVAS (if authorized). Manual verify every auto-reported finding.

### Exploitation
Tools: Metasploit, sqlmap, Burp Suite, manual PoC. Capture evidence for every finding.

### Post-Exploitation / Cleanup
Remove all artifacts: shells, scripts, modified configs. Document persistence vectors found.

## Output

- recon/ - raw scan data
- findings.md - raw findings
- executive-summary.md - stakeholder summary
- remediation.md - per-finding remediation

## Scope validation template

```markdown
## Engagement scope

| Authorized targets | scope-ips.txt, scope-domains.txt |
| Off-limits | 10.0.0.1 (DC), *.example.internal |
| Authorized techniques | Active scan, manual exploit, social engineering (phishing only) |
| Not authorized | DoS, social engineering (physical), ransomware sim, data exfil |
| Communication | #eng-id in Slack, eng-id@example.com | 
| Evidence handling | Encrypted at rest, audit log to S3 |
```

## Phase gates

Each phase ends with a gate review:
- Recon: passes if nmap/nuclei reports complete and no out-of-scope hits
- Enumeration: passes if every open service has at least one entry in `findings.md`
- Exploitation: passes if every critical finding has a PoC and evidence path
