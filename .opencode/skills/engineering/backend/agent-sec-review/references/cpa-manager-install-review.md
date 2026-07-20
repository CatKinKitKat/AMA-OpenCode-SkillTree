# CPA-Manager / CLIProxyAPI install review note

Use this reference when installing `seakee/CPA-Manager` against an existing `router-for-me/CLIProxyAPI` (CPA) service.

## Security posture

Risk: MEDIUM by default.

Why:
- CPA-Manager Usage Service stores CPA URL and Management Key in SQLite/settings or config-driven state.
- It runs a long-lived local HTTP service and may be placed behind Docker/LaunchAgent.
- CPA Management API must be enabled. An empty `remote-management.secret-key` leaves management routes disabled (`404`).
- Usage stats require `usage-statistics-enabled: true` and exactly one consumer of the usage queue.

Safe defaults:
- Bind CPA-Manager to `127.0.0.1:18317` unless the user explicitly needs remote access.
- Store the Management Key in a chmod 600 file, not shell history or world-readable plist.
- Keep `/data` or SQLite dir private. It contains usage metadata and may contain saved Management Key.
- Prefer a LaunchAgent with explicit `CPA_MANAGER_CONFIG` over ad-hoc background processes.

## Version trap

CPA-Manager docs prefer CPA `>= v6.10.8` because it exposes:

`GET /v0/management/usage-queue?count=N`

Older Homebrew `cliproxyapi 6.9.25` can show:
- `/management.html` -> 200
- `/v0/management/config` -> 200 after key is enabled
- `/v0/management/usage` -> 200
- but no usable HTTP usage queue. CPA-Manager falls back to RESP and can fail with:

`auth: unsupported RESP prefix 'H'`

or stale error after startup:

`connect: dial tcp 127.0.0.1:8317: connect: connection refused`

Fix: upgrade CPA to a version with `/v0/management/usage-queue`, then restart CPA-Manager so auto mode switches to `transport":"http"`.

## OpenAI-compatible paced key pools

For providers that enforce a per-key cooldown after each request, prefer CPA local scheduling over retry probing.

Observed HHHL policy for `https://dc.hhhl.cc/v1`:
- Configure the provider under `openai-compatibility` with `scheduler.cooldown: "32s"`, `scheduler.admission-rate: 21`, and `scheduler.max-queue-wait: "10s"`.
- Treat 700 unique keys as an aggregate envelope of about 21 rps with safety margin.
- After a successful request, CPA should mark that credential/model locally unavailable until the cooldown expires.
- For 429 with a short `Retry-After`, CPA should keep the longer local scheduler cooldown.
- If every matching key is cooling, fail locally with retry-after/cooldown semantics. Do not send a request just to test whether upstream still rejects it.
- Do not use anti-fingerprint, JA4, or IP-bypass tactics in this workflow.

## Network/build workaround observed

When Release CDN / Homebrew bottle / Go toolchain downloads fail with TLS EOF/SIGSYSCALL:
- GitHub release asset download may fail at `release-assets.githubusercontent.com`.
- `brew upgrade go` may fail at `ghcr.io`.
- `go` auto toolchain may fail at `dl.google.com`.
- `proxy.golang.org` module downloads may timeout.

Workaround path used:
1. Clone `router-for-me/CLIProxyAPI`.
2. Build with existing Go 1.25 using `GOTOOLCHAIN=local GOPROXY=https://goproxy.cn,direct`.
3. Patch Go 1.26-only conveniences for Go 1.25 compatibility if needed:
   - replace `errors.AsType[T](err)` with a local generic helper using `errors.As`.
   - replace `new(expr)` patterns like `new(5 * time.Minute)` with `d := expr; return &d`.
4. Build `./cmd/server` to a user-local binary and run it via LaunchAgent.

This is a pragmatic fallback only. Prefer official release/bottle when network and toolchain allow verification.

## Verification probes

Use the real Management Key:

```sh
key=$(cat ~/.config/cpa-manager/management-key)
curl -sS -H "Authorization: Bearer $key" 'http://127.0.0.1:8317/v0/management/usage-queue?count=2'
curl -sS http://127.0.0.1:18317/health
curl -sS -H "Authorization: Bearer $key" http://127.0.0.1:18317/status
```

Good final state:
- `/v0/management/usage-queue?count=2` returns `[]` or JSON events, not HTML/404.
- CPA-Manager `/status` shows `collector":"running"` and `transport":"http"`.
- `lsof` shows CPA on `:8317` and CPA-Manager on `127.0.0.1:18317`.
