# CF 403 Debugging Session (2026-05-08)

## Problem Statement
User's the agent agent got HTTP 403 "Your request was blocked" when calling third-party relay endpoints. Playground on the same site worked fine.

## Debugging Path

1. **Initial hypothesis**: CF blocks SDK User-Agent headers
   - Verified: playground uses `/pg/chat/completions`, the agent uses `/v1/chat/completions`
   - Playground logs showed streaming SSE success

2. **First attempt**: Create user plugin with browser UA
   - Created `~/.agent/plugins/model-providers/jiuuij/` with `default_headers`
   - **Failed**: Provider showed as `custom`, not `jiuuij`: plugin not matched

3. **Second attempt**: Override `custom` profile in user plugins
   - Created `~/.agent/plugins/model-providers/custom/__init__.py`
   - Set `default_headers` as class attribute
   - **Failed**: `default_headers = {}`: dataclass field issue

4. **Root cause discovered**: 
   - `ProviderProfile` is a dataclass with `default_headers: dict = field(default_factory=dict)`
   - Class-level assignment is overridden by field default
   - Must pass `default_headers={...}` at instantiation

5. **Another root cause**:
   - `custom_providers[].headers` in config.yaml is **never read by code**
   - Only `name`, `base_url`, `api_key`, `models` are processed
   - Log warning: `providers.?: unknown config keys ignored: headers`

6. **Final fix**: Modify `run_agent.py` directly
   - Patch line ~1474: exception handler injects browser UA
   - Patch line ~6358: else branch injects browser UA instead of `.pop()`
   - **Result**: CF 403 resolved → new error: "Empty response from model" / 401 Invalid token

## Code Changes Applied

**run_agent.py line ~1466-1487** (init-time):
```python
elif "default_headers" not in client_kwargs:
    try:
        from providers import get_provider_profile as _gpf
        _ph = _gpf(self.provider)
        if _ph and _ph.default_headers:
            client_kwargs["default_headers"] = dict(_ph.default_headers)
        else:
            client_kwargs["default_headers"] = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
            }
    except Exception:
        client_kwargs["default_headers"] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }
```

**run_agent.py line ~6346-6360** (`_apply_client_headers_for_base_url`):
```python
else:
    _ph_headers = None
    try:
        from providers import get_provider_profile as _gpf2
        _ph2 = _gpf2(self.provider)
        if _ph2 and _ph2.default_headers:
            _ph_headers = dict(_ph2.default_headers)
    except Exception:
        pass
    if _ph_headers:
        self._client_kwargs["default_headers"] = _ph_headers
    else:
        self._client_kwargs["default_headers"] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }
```

## Lessons Learned

1. **Dataclass field gotcha**: `field(default_factory=dict)` overrides class-level assignment
2. **Config field that doesn't exist**: `custom_providers[].headers` is parsed but never used
3. **Provider resolution**: `provider == "custom"` catches all third-party endpoints regardless of `custom_providers[].name`
4. **Multiple code paths**: Headers must be injected in BOTH init-time and `_apply_client_headers_for_base_url`
5. **CF fingerprint depth**: UA alone may not be enough: TLS JA3, HTTP/2 fingerprints may also be checked

## Remaining Issue

After UA fix, got "Empty response from model" and 401 Invalid token errors. This indicates:
- CF is now bypassed (UA fix worked)
- The problem shifted to API key / authentication
- Different endpoints may have different key requirements

User needs to verify correct API key for the specific endpoint being used.
