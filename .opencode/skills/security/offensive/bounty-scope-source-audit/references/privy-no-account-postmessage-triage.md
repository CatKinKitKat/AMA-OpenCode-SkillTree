# Privy no-account postMessage/package triage

Use for bounty scope rows that include public npm packages and web auth/cross-app assets where the user wants bugs that do not require prepared accounts.

## Scope shape observed

In-scope examples from Privy BBP CSV:
- `https://www.npmjs.com/package/@privy-io/react-auth` as `SOURCE_CODE`
- `@privy-io/js-sdk-core`, `@privy-io/expo`, `@privy-io/wagmi`, `@privy-io/cross-app-connect`, `@privy-io/cross-app-provider` as bounty-eligible `OTHER`
- `auth.privy.io`, `api.privy.io`, `home.privy.io`, `recovery.privy.io`, `demo.privy.io` as live URL assets

## Fast source acquisition

If GitHub repo metadata is absent from npm, audit shipped tarballs directly:

```bash
npm view @privy-io/react-auth version dist.tarball --json
mkdir -p /tmp/privy-audit/react-auth
curl -L -sS <tarball> -o /tmp/privy-audit/react-auth.tgz
tar -xzf /tmp/privy-audit/react-auth.tgz -C /tmp/privy-audit/react-auth
```

For scoped packages, registry URLs may be more reliable than `npm view` when npm has transient TLS failures:

```bash
curl -L -sS 'https://registry.npmjs.org/@privy-io%2freact-auth'
```

## High-yield no-account sinks

Search package bundles for browser trust-boundary issues:

```bash
rg -n "postMessage|addEventListener\(\"message|window\.open|opener|BroadcastChannel|requester_origin|callbackUrl|redirect_to|code_challenge|state_code" /tmp/privy-audit
```

Triage rule:
- If a popup/request library consumes `message` events, require `event.origin` and `event.source` checks before accepting `event.data.type`.
- If a provider posts back to `window.opener.postMessage(message, callbackUrl)`, verify how `callbackUrl`/`requester_origin` is derived and whether server state binds it to requester key/app id.
- If an OAuth helper sends arbitrary `redirect_to` to an init endpoint, live-test whether the server allowlists redirect origins before calling it a bug.

## Privy-specific candidates found

### 1. Cross-app connect response spoofing

Files:
- `@privy-io/cross-app-connect/dist/cjs/triggerPopup.js`
- `@privy-io/cross-app-connect/dist/cjs/request.js`

Observed pattern:
- `window.addEventListener("message", handler)`
- handler branches only on `event.data.type`
- no visible `event.origin` check
- no visible `event.source === popup` check

Candidate impact:
- spoofed `PRIVY_CROSS_APP_CONNECT_RESPONSE` may make an integrator accept attacker-chosen `address/providerPublicKey/exp`
- spoofed `PRIVY_CROSS_APP_ACTION_ERROR` can cause transaction/signing denial of service
- action success spoofing is less direct when `encryptedResult` is required, but still verify source/origin first

Minimal browser probe shape:

```js
window.postMessage({
  type: "PRIVY_CROSS_APP_CONNECT_RESPONSE",
  address: "0x1111111111111111111111111111111111111111",
  providerPublicKey: "AAAA...",
  exp: Date.now() + 1209600000
}, "*");
```

To confirm: run inside a page using the package, trigger connect popup, send the forged message from a sibling frame/popup or console, and observe whether provider state changes.

### 2. OAuth/recovery open redirect candidate

Files:
- `@privy-io/js-sdk-core/dist/cjs/client/auth/OAuthApi.js`
- `@privy-io/js-sdk-core/dist/cjs/client/recovery/RecoveryOAuthApi.js`

Observed pattern:
- client sends `redirect_to` plus `code_challenge` and `state_code` to init endpoint.

Do not report from source alone. Confirm server accepts an untrusted external origin and returns/redirects to it.

## Reporting guidance

For postMessage findings, weakness category usually fits:
- CWE-346 Origin Validation Error
- or CWE-345 Insufficient Verification of Data Authenticity

Report only after proving an integrator-visible state change or auth/transaction flow disruption from an untrusted message source.