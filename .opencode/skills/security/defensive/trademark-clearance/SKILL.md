---
name: trademark-clearance
description: Audit trademark exposure, third-party license compliance, and public-facing asset hygiene. Use when a brand has public/PR implications or during product release review.
---
# Trademark Clearance

Audit brand/trademark exposure and third-party license compliance.

## When to Use

- [done] Pre-release IP/trademark audit for new products or features
- [done] Incident has PR/brand impact (data breach, service outage)
- [done] Open-source contribution review (CLA, DCO, outbound IP)
- [done] Periodic domain / trademark squatting review

## Workflow

### Trademark clearance

Search TM databases for identical marks in same class, flag confusingly similar names. Output clearance table (clear / flag / block).

### License compliance

Flag: AGPL in commercial products, SSPL in SaaS, unknown licenses.
Verify OSS licenses have attribution (LICENSE, NOTICE files).

### Public-facing asset review

- Domain hygiene: expired domains, subdomain takeovers
- Social handles: impersonation, squatting
- Repo hygiene: accidental secret push, internal tooling exposed

## Output

- Audit report with trademark table, license table, public-facing findings

## Trademark Search Procedure

1. Search USPTO TESS (or EU IPO eSearch) for identical mark in same class
2. Search domain registries (WHOIS) for active domains
3. Check social: Twitter, LinkedIn, GitHub org names

## Output tolerance

| Classification | Action |
|----------------|--------|
| Clear | No identical marks in class. Proceed |
| Flag | Similar marks. Legal review before launch |
| Block | Identical mark + active use. Rename

## Trademark search procedure

Search the following registries:
- USPTO TESS (US)
- EU IPO eSearch (EU)
- WIPO Global Brand Database
- WHOIS for active domains

## Clearance table

| Asset | Status | Registered by | Class | Action |
|-------|--------|---------------|-------|--------|
| the-portal | clear | none | 9/42 | proceed |
| the-dashboard | flag | competitor | 9 | legal review |

## License red flags

- AGPL-3.0: avoid in proprietary products (copyleft taint)
- SSPL: avoid in SaaS (not OSI-approved)
- Unknown `License:`: audit before use
- `License-File` / `NOTICE`: required for Apache-2.0 / MIT in some builds
