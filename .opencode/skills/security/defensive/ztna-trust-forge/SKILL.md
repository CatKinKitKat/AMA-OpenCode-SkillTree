---
name: ztna-trust-forge
description: Manage device attestation, cross-domain trust rules, and least-privilege access policies in a Zero Trust Network Access (ZTNA) architecture. Use when onboarding new devices, evaluating access tokens, or responding to a trust-boundary violation.
---
# ZTNA Trust Forge

Manage device attestation and trust rules in a ZTNA architecture.

## When to Use

- [done] Onboarding a new device to the trust fabric
- [done] Evaluating access token validity before granting access
- [done] Responding to a trust-boundary violation (lost device, revoked cert)
- [done] Periodic review of trust policies (least-privilege audit)

## Workflow

### Device attestation

Verify device health before granting access:
- OS version + patch level
- Disk encryption status
- MDM enrollment status
- Approved software list (MDM-installed, not user-installed)
- Geolocation / network posture (if policy requires)

### Access token evaluation

Per `token` claim:
- `aud` / `iss`: matches expected provider
- `sub`: mapped to a known identity (not a guest/anonymous)
- `exp` / `nbf`: token in valid window
- `scope` / `roles`: at minimum required scope
- `jti`: not revoked (check revocation list)

### Trust policy review

Review active trust policies quarterly:
- Remove stale device attestations (expired, decommissioned, lost)
- Remove overly permissive rules (no `trust_all` in production)
- Ensure logging is active for all trust decisions

## Output

- ZTNA trust policy review table
- Device attestation summary
- Recommended rule changes

## Best Practices

- Prefer MFA-attested sessions over password-only
- Add continuous re-evaluation (not just at login)
- Log every trust decision (allow + deny both)
- Rotate trust roots on every employee departure / MDM wipe
