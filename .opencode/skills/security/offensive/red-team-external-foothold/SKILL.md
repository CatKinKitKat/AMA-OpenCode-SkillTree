---
name: red-team-external-foothold
description: Establish and maintain an authorized initial access foothold: C2 infrastructure, phishing, drive-by, and implant management. Use when the red team needs stable foothold after initial compromise in an authorized engagement.
---
# Red Team - External Foothold

Establish, validate, and maintain an authorized external access foothold.

## When to Use

- [done] Post-recon: need stable external access
- [done] Authorized phishing simulation
- [done] Drive-by landing page validation (with scope approval)
- [done] C2 implant management

## Phishing (authorized only)

Tools: GoPhish, Evilginx.
Process: scope confirmation -> landing page -> campaign -> tracking -> credential validation -> cleanup.

## C2 Infrastructure

Recommended: Empire/Mythic/Sliver. HTTPS + domain fronting. Fallback beacons.

## Implant lifecycle

Deploy -> Register with C2 -> Beacon (jitter) -> Task -> Exfil -> Cleanup.

## Output

- c2/beacon-log-<timestamp>.md
- pentest/<eng-id>/findings.md (append)
- pentest/<eng-id>/evidence/ (payloads, C2 logs)

## C2 infrastructure options

| Tool | Pros | Cons |
|------|------|------|
| Empire | Mature, rich plugins | Requires C2 server, alerting |
| Mythic | Containerized, UI | Complex setup |
| Sliver | Lightweight, cross-compile | Less mature than Empire |
| Covenant | Modern UI, easy | DotNet dependency |

## Payload considerations

Payload types:
- Shellcode (Cobalt Strike beacon, Havoc, custom)
- Script languages (Go implant, Python implant, PowerShell)
- Living-off-the-land (LOLBins: mshta, rundll32, wscript)

## Engagement rules

- Must have explicit scope document allowing implant deployment
- Implant must have a defined kill date and kill command
- After engagement: collect all C2 server logs, destroy infrastructure, document
