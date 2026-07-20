# Plaid no-account source audit pattern (2026-05-11)

Scope CSV had SOURCE_CODE rows for Plaid SDK/client repos. The user wanted findings that do not require preparing another account, then asked for ready markdown plus PoC files.

## Reusable workflow

1. Parse CSV first and select `asset_type == SOURCE_CODE` rows.
2. Clone in-scope repos into `/tmp/<program>-audit`. Keep originals untouched.
3. Parallelize independent repo families with `delegate_task`:
   - React/web package: script loading, postMessage, OAuth redirect, package scripts.
   - React Native/mobile bridge: Android/iOS callback bridges, logs, Activity results, embedded views.
   - Server/API client package: generated client logging, file packaging, TLS/defaults, dynamic calls.
   - Sample apps: treat as weak unless they create a no-account exploit path.
4. Classify strictly: confirmed / actionable / weak design / false lead.
5. When user asks for report, create filesystem deliverables, not chat-only prose:
   - one `.md` report per finding
   - `poc/<finding>/README.md`
   - executable PoC script
   - zip archive containing reports and PoCs
6. Run every PoC locally and include decisive output in final response.

## Findings worth reusing as patterns

### Ruby gem package pollution
Signal:
- gemspec uses broad shell listing: `s.files = \`find *\``
- release target installs dependencies or build artifacts inside repo, e.g. `bundle config set --local path 'vendor/bundle'`

PoC:
- create `vendor/bundle/.../SHIPPED_IN_GEM`
- load `Gem::Specification.load('plaid.gemspec').files`
- prove marker appears in `s.files`

Report weakness:
- CWE-538 or CWE-200
- Usually Medium if official release flow can publish local artifacts.

### Mobile SDK callback data logging
Signal:
- bridge callbacks convert success/exit result to map/dict, then `print(result)` / `Log.*` before app callback.
- result contains public tokens, account metadata, request/session IDs.

PoC:
- static source PoC is acceptable when native live flow needs account/link token.
- grep exact sink and sensitive field shape from adjacent bridge code.

Report weakness:
- CWE-532
- Usually Low/Medium depending default release-log exposure.

### Generated API client debug raw-body logging
Signal:
- `config.debugging` enables full request/response body logging.
- no redaction near debug sinks.
- logger defaults to Rails logger or STDOUT.

PoC:
- static source probe plus simulated log body containing `secret` / `access_token`.
- mark as lower confidence if debugging default is false.

Report weakness:
- CWE-532
- Usually Low. Call out dependence on debug mode.

## False leads from this session

- Dynamic Plaid CDN script with no SRI: weak unless there is a concrete CDN/script substitution path.
- Trusting existing same-src `<script>` in page: requires prior same-origin DOM/script control. Collapses into XSS/supply-chain compromise.
- OAuth sample storing link_token in localStorage: example-level. Needs real link_token or origin compromise.
- Android embedded token prefix inconsistency: wrapper consistency issue unless underlying SDK impact is proven.
- Sample app cleartext localhost server: requires dashboard credentials. Sample-only.

## Final-response pattern

Keep final concise:
- directory path
- zip path
- markdown file paths
- PoC paths
- verification summary
- recommended submission order
