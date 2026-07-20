# Bulk-add API keys to a the agent custom provider credential pool

Use when a user asks to add many API keys under an existing the agent custom provider.

## Durable pattern

the agent stores configured providers in `~/.agent/config.yaml`, but the multi-key failover pool lives in `~/.agent/auth.json` under:

```json
credential_pool["custom:<provider-name>"]
```

For legacy/custom providers, the pool key is usually normalized from the custom provider `name`, not the display phrase the user uses. Example: provider name `httpsdchhhlcc` becomes `custom:httpsdchhhlcc`.

## Safe workflow

1. Resolve the provider:
   - inspect `custom_providers` in `~/.agent/config.yaml`
   - match by `name`, `base_url`, and user-facing nickname
   - inspect existing `credential_pool` keys in `~/.agent/auth.json`
2. Back up `auth.json` before mutation:
   - `~/.agent/auth.json.bak-pre-<tag>-YYYYmmddHHMMSS`
3. Append keys as manual pool entries, not as a YAML list in `custom_providers.api_key`. Current seeding code treats `api_key` as a single string.
4. Preserve existing entries and priorities. Assign new priorities after the current max.
5. Use unique `source` values such as `manual:<batch>-001`, `manual:<batch>-002`, etc.. Manual entries are retained by pool pruning.
6. Set `auth_type=api_key`, `base_url` to the resolved custom provider base URL, and reset status/error fields to null so old exhaustion state is not inherited.
7. Verify without printing secrets:
   - `python3 -m json.tool ~/.agent/auth.json >/dev/null`
   - load the pool from the agent source with `load_pool('custom:<provider-name>')`
   - report counts only: parsed keys, added keys, total pool size, unique token count, backup path.

## Minimal append shape

```json
{
  "id": "<6 hex>",
  "label": "<batch>-001",
  "auth_type": "api_key",
  "priority": 42,
  "source": "manual:<batch>-001",
  "access_token": "sk-...",
  "last_status": null,
  "last_status_at": null,
  "last_error_code": null,
  "last_error_reason": null,
  "last_error_message": null,
  "last_error_reset_at": null,
  "base_url": "https://example/v1",
  "request_count": 0
}
```

## Pitfalls

- Do not echo or summarize the actual keys back to the user.
- Do not overwrite `auth.json`. Merge and preserve existing pool entries.
- Do not rely only on `config.yaml.custom_providers[].api_key` for bulk keys. `_seed_custom_pool()` currently casts the field to a single string.
- Do not treat transient status fields on old credentials as applying to newly added credentials.
