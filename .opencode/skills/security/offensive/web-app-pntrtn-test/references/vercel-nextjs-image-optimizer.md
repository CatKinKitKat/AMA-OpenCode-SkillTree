# Vercel Next.js image optimizer notes

Scope: `vercel/next.js`.

Key path:
- `packages/next/src/server/next-server.ts`
- `packages/next/src/server/image-optimizer.ts`
- `packages/next/src/shared/lib/match-remote-pattern.ts`
- `packages/next/src/shared/lib/match-local-pattern.ts`

Observed chain:
- `validateParams()` checks `url`, `w`, `q`, local/remote allowlists.
- Absolute URL path goes to `fetchExternalImage()`.
- Relative URL path goes to `fetchInternalImage()` via `createRequestResponseMocks({ url: href })`.

Important pitfall:
- `fetchExternalImage()` checks resolved IPs first, then performs `fetch(href)` later. That leaves a DNS rebinding window when `dangerouslyAllowLocalIP` is false.
- Do not assume `remotePatterns` or `domains` block private IPs by themselves. They only pattern-match hostname/path/query.

Useful code anchors:
- `fetchExternalImage()` uses `lookup(hostname, { all: true, hints: ALL })`, then `fetch(href, { redirect: 'manual' })`.
- `fetchInternalImage()` replays the internal request through the router with `parseReqUrl(href)`.

Verification idea:
- Use a hostname that resolves public on first lookup and private on the fetch step, then confirm whether the image optimizer reaches the private target.
