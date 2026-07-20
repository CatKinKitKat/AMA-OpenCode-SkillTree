# Plaid no-account triage notes

Session: 2026-05-11

Scope source rows checked:
- `https://github.com/plaid/plaid-link-ios`
- `https://github.com/plaid/plaid-link-android`
- `https://github.com/plaid/plaid-ruby`
- `https://github.com/plaid/react-native-plaid-link-sdk`
- `https://github.com/plaid/react-plaid-link`

Useful findings:
- `react-plaid-link/src/react-script-hook/index.tsx` loads `https://cdn.plaid.com/link/v2/stable/link-initialize.js` with no SRI/pinning.
- `react-plaid-link/src/usePlaidLink.ts` and `src/PlaidEmbeddedLink.tsx` trust `window.Plaid` after script load. Existing DOM `<script>` tags with the same `src` are also trusted.
- `react-native-plaid-link-sdk/android/src/main/java/com/plaid/PlaidModule.kt` only checks that the token starts with `link` before constructing `LinkTokenConfiguration`.
- `react-native-plaid-link-sdk/ios/RNLinksdk.mm` defaults unexpected environment strings to sandbox.
- `react-native-plaid-link-sdk/ios/PLKEmbeddedView.swift` and the Android embedded view bridge tokens directly into native Link creation and event callbacks.

Outcome:
- No confirmed no-account vuln was proven in this pass.
- Best candidates remained `high-risk design` because the real security boundary sits in Plaid-hosted script/token semantics, not in repo-local enforcement.
- A useful triage rule from this session: for SDK repositories, prefer trust-boundary review over route/auth sweeps. Look for remote loaders, redirect handling, existing-script reuse, and whether a weak local token check is just shape validation.
