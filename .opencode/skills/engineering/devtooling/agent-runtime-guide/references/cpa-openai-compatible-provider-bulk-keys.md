# Bulk-add keys to CPA OpenAI-compatible providers

Use when the user asks to add many API keys to CLI Proxy API / CPA Manager's AI Providers page, especially `management.html#/ai-providers` and OpenAI-compatible providers.

## Key distinction

Do not confuse this with the agent `~/.agent/auth.json` credential pools. CPA Manager has its own management API and auth key.

- UI: `http://127.0.0.1:<port>/management.html#/ai-providers`
- API base discovered from bundled frontend: `http://127.0.0.1:<port>/v0/management`
- Management key file often: `~/.config/cpa-manager/management-key`
- Manager config often: `~/.config/cpa-manager/config.json`
- Auth header: `Authorization: Bearer <management-key>`

## OpenAI-compatible provider endpoints

From the CPA Manager frontend bundle:

- `GET /v0/management/openai-compatibility`
- `PUT /v0/management/openai-compatibility` with the full provider array
- `PATCH /v0/management/openai-compatibility` with `{index, value}` for targeted update
- `DELETE /v0/management/openai-compatibility?name=<encoded>`

Provider shape uses dashed keys:

```json
{
  "name": "provider display name",
  "base-url": "https://example/v1/",
  "api-key-entries": [
    {"api-key": "sk-..."}
  ],
  "scheduler": {
    "cooldown": "32s",
    "admission-rate": 21,
    "max-queue-wait": "10s"
  },
  "models": [
    {"name": "model", "alias": "optional"}
  ],
  "priority": 999,
  "disabled": false
}
```

## Safe workflow

1. Fetch `/management.html` and inspect the bundle if endpoint names are unknown.
2. Read `~/.config/cpa-manager/config.json` for `httpAddr`, `cpaUpstreamUrl`, and `managementKeyFile`.
3. Read the management key file and call `/v0/management/openai-compatibility` with `Authorization: Bearer ...`.
4. Match provider by exact name first, then by a narrow substring if the UI/user name differs by a typo.
5. Back up the full provider array before mutation, e.g. `/tmp/cpa-openai-compatibility-backup-<epoch>.json`.
6. Append new key entries as `{"api-key": key}` while preserving all existing provider fields.
7. Prefer merging and deduping valid non-empty `api-key` values. Do not delete unknown/empty `auth-index` placeholder entries unless the user asks for cleanup.
8. Verify by refetching and counting only entries with a non-empty `api-key`. Report counts only, never print secrets.

## HHHL local pacing policy

Use this when maintaining the `hhhl` OpenAI-compatible provider for `https://dc.hhhl.cc/v1`.

- Live CPA config path observed locally: `/opt/homebrew/etc/cliproxyapi.conf`.
- LaunchAgent binary observed locally: `~/.local/bin/cliproxyapi-v7`.
- Key source files observed locally:
  - `~/Downloads/520个key 1分钟30次冷却20秒 (1).txt`
  - `~/Downloads/200张key -1分钟30次.txt`
- Expected pool size: 700 unique non-empty keys. Verify counts only. Never print keys.
- Required scheduler config:
  - `cooldown: "32s"`
  - `admission-rate: 21`
  - `max-queue-wait: "10s"`
- Operational invariant: assume any new upstream request refreshes that key's 30s cooling window. CPA must locally avoid selecting, probing, retrying, or health-checking a cooling key until its local `next_retry_after` expires.
- If all matching keys are cooling, return/propagate local cooldown (`Retry-After`) instead of sending a speculative upstream request.
- Do not document or implement JA4/IP/fingerprint bypass. The supported strategy is compliant local scheduling against the user's own configured key pool.

## Pitfalls

- CPA localStorage may store auth state as `enc::v1::...`. Do not rely on parsing browser storage when the management key file exists.
- The UI display name may have a one-character mismatch. In one session, user said `无限限时hhh` while the API provider name was `无限限时hhhl`. Report the mismatch and do not rename unless asked.
- Some entries may be placeholders with empty `api-key` and an `auth-index`. Keep them unless cleanup is explicitly in scope.
- Do not confuse CPA upstream port (`8317`) with CPA Manager port (`18317`).
- If editing the file config directly instead of the Management API, back up `/opt/homebrew/etc/cliproxyapi.conf` first and validate by parsing config plus counting the `hhhl` key entries without revealing secrets.
