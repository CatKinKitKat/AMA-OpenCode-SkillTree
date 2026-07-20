# CAPTCHA vision provider stalls in Hansa Arena cron

## Trigger
Use this reference when `hansa-arena(快速执行静默)` starts reporting skipped ticks, long CAPTCHA attempts, or repeated `previous arena tick still running` after a CAPTCHA tournament.

## Durable pattern
The Arena cron must remain a fast `no_agent` job. CAPTCHA vision is allowed only if it cannot block the 2-minute schedule.

## Evidence shape
Typical log sequence:

```text
[CAPTCHA] Provider OK: https://jiuuij.de5.net/v1, model=mimo-v2.5
[CAPTCHA] POST .../chat/completions ...
timeout after 105s
skip: previous arena tick still running
```

Other bad responses include empty/malformed provider payloads that surface as:

```text
TypeError: 'NoneType' object is not subscriptable
ANSWER=[2,3,5,
FAIL: could not parse JSON array from response
```

## Fix pattern
1. Kill stale collector/wrapper processes before validating:

```bash
pkill -9 -f 'hansa_arena_collect.py|hansa_arena_execute_silent.py' || true
```

2. In `~/.agent/scripts/hansa_arena_collect.py`, do not let an unstable vision route monopolize the cron tick:
   - skip known-stalling `mimo-v2.5` for grid CAPTCHA and fall back to `kimi-k2.6` when configured.
   - wrap blocking vision calls with a hard wall-clock timeout.
   - on timeout / 5xx / model_not_found / unstable provider, return `vision_unavailable_*` and set `captcha_vision_cooldown_until` for 1 hour.
   - parse truncated `ANSWER=[...]` conservatively only when the prefix is clearly present.

3. Validate locally:

```bash
python3 -m py_compile ~/.agent/scripts/hansa_arena_collect.py ~/.agent/scripts/hansa_arena_execute_silent.py
python3 ~/.agent/scripts/hansa_arena_execute_silent.py
```

4. Validate scheduler state:

```text
cronjob run 817d044f33c5
cronjob list
```

Expected: job remains enabled, `last_status=ok`, no lingering `hansa_arena_*` process, no user-facing output unless the silent-output rules are met.

## Pitfalls
- Do not convert Arena back to an LLM-driven cron just to solve CAPTCHA. That reintroduces scheduling latency.
- Do not keep retrying a stalled vision provider every 2 minutes. Use cooldown.
- Do not treat Feishu delivery fallback as the root cause if the cron itself is timing out or lock-skipping.
- Do not preserve failed CAPTCHA attempts in `submitted_rounds`. Only 200/201 with correct status counts.