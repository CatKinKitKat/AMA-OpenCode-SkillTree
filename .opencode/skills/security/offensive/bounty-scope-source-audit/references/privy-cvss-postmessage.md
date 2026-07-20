# Privy postMessage CVSS notes

Use this when scoring client-side Privy cross-app / popup trust bugs.

## Default CVSS 3.1 mapping

For forged `message` events that only spoof wallet connection state or force request failure:
- AV:N
- AC:L
- PR:N
- UI:R
- S:U
- C:N
- I:L
- A:L

Vector:
`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:L`

Base score:
- 5.4
- Medium

## Escalation rules

Raise Integrity to High only if the proof shows unauthorized signing, transaction execution, token minting, or durable account-state modification.
Raise Confidentiality only if a token, code, session, secret, or user data is shown to cross the boundary.
Raise Availability only if the bug causes durable service outage, not just one request failure.

## Evidence rule

Do not score from source alone if the issue depends on server-side redirect allowlists or a live popup flow. Confirm the browser-visible effect first.

## Session-specific note

The `@privy-io/cross-app-connect` handlers accepted forged `PRIVY_CROSS_APP_CONNECT_RESPONSE` and `PRIVY_CROSS_APP_ACTION_ERROR` messages without `origin`/`source` validation. That was enough for Medium 5.4, not High, because no secret leak or signed transaction execution was proven.
