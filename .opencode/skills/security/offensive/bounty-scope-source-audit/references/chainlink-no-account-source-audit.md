# Chainlink no-account source audit note

Session date: 2026-05-11
Scope file: `~/Downloads/scopes_for_chainlink_at_2026-05-11_05_55_58_UTC.csv`

## CSV triage rule

For bounty-scope CSVs, split rows in this order before reading code:
1. `eligible_for_bounty == true` and `eligible_for_submission == true`
2. `SOURCE_CODE` rows that are in scope but not bounty-eligible
3. non-source rows that still name repo paths or helper assets

In this Chainlink scope, the clean no-account source target was:
- `https://github.com/smartcontractkit/external-adapters-js/`

## Why it stood out

The repo contains a bootstrap server that exposes a public POST adapter entrypoint without an auth gate in the route path itself:
- `packages/core/bootstrap/src/lib/server.ts`
- route: `app.post(baseUrl, ...)`
- request flow: body merge -> `executeSync(...)`

Useful follow-up pivots for no-account source audits:
- check whether a route is reachable without session/token material
- search for default metrics or health endpoints on separate ports
- separate runtime impact from source-only risk until you prove deployment defaults

## Notes

This session also showed that scope CSVs may contain `SOURCE_CODE` assets with `eligible_for_bounty=false`. Those are still useful for orientation but should not be treated as the primary bounty target.
