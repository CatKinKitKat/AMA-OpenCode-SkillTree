---
name: phishing-mailpath-analysis
description: Analyze phishing campaign mail paths: SPF, DKIM, DMARC, header analysis, MTA logs, and payload indicators. Use when investigating suspicious email campaigns in a blue-team context or validating phishing simulations.
---
# Phishing Mailpath Analysis

Analyze email paths, authentication records, and payload indicators for phishing and mail-based social engineering campaigns.

## When to Use

- [done] Investigating a suspicious email campaign (blue team)
- [done] Reviewing phishing-simulation evidence (red team context)
- [done] Analyzing SPF/DKIM/DMARC failures
- [done] Triageing user-reported suspicious messages

## Workflow

### Header analysis

Check Received chain for missing hops, reveal mailer tooling, validate Message-ID domain, Verify Return-Path aligns with From.

### Authentication checks

Check Authentication-Results header: SPF, DKIM, DMARC pass/fail and policy.

### Link analysis

Extract URLs, evaluate domain age/reputation, resolve redirect chains, detect typosquatting.

### Payload analysis

Attachment hash: VirusTotal / Hybrid-Analysis. Office macros: olevba/oleid. PDF: pdfid.

## Output

- Header chain (verbatim)
- Authentication verdict
- Links table (URL, redirect target, reputation, verdict)
- Payload verdict (clean / malicious / sandbox)
- Mailpath diagram (Mermaid sequence)

## Authentication verdict table

| Mechanism | Result | Impact |
|-----------|--------|--------|
| SPF | pass / fail / softfail | Sender not authorized to send from domain |
| DKIM | pass / fail / neutral | Message tampered or sent without signing |
| DMARC | pass / fail / quarantine | Domain policy violated |

## Phishing analysis kit

Recommended tools:
- `phishing-email-analyzer` (Python tool that parses MIME, checks headers)
- URLhaus / VT for link reputation
- `james` (mail server) for controlled replay

## Red-team context

If authorizing a phishing simulation:
- Must include `phishing-mailpath-analysis` skill in scope
- Log all sent mail to `pentest/<eng-id>/artifacts/phishing-mails.json`
- Provide user instruction on how to report findings (support email, Slack)
