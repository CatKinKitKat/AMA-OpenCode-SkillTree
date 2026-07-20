# Web3 wallet-gated flows via real browser

Use this when a target requires MetaMask, Phantom, Trust Wallet, Coinbase Wallet, Google/Discord login, or any wallet signature.

## Lesson

Isolated automation browsers can inspect Web3 pages, but usually cannot complete wallet-gated actions because wallet extensions and real user sessions are absent. In one session, GenLayer Portal showed all wallet options as `Not installed` in the isolated browser, and Browser Relay was unavailable because `127.0.0.1:18795` refused connections.

## Workflow

1. Recon with ordinary browser automation first:
   - capture page text, links, contribution types, issue trackers, points rules
   - find non-wallet actions such as public GitHub issues or docs feedback
2. Before wallet/login-gated work, check Browser Relay health:
   ```bash
   python3 - <<'PY'
   import urllib.request
   for path in ['/', '/api/debug', '/api/tabs']:
       try:
           print(path, urllib.request.urlopen('http://127.0.0.1:18795'+path, timeout=2).read().decode()[:500])
       except Exception as e:
           print(path, 'ERR', e)
   PY
   ```
3. If relay is down, report the exact blocker and ask the user to open real Chrome with the needed wallet/login state and relay extension.
4. Only after relay sees tabs, navigate the real tab and perform wallet-gated actions one step at a time.
5. Never sign wallet messages or submit irreversible transactions without the user's explicit confirmation at the signing step.

## Fallback

If wallet flow is blocked, look for public contribution channels that still count toward points:
- GitHub issues for portal bugs
- documentation mistakes
- reproducible broken links/deep links
- project submission forms that accept URLs after login later

Example: GenLayer Portal had path links such as `/testnets` and `/metrics` that returned server-side 404 when opened directly, while hash routes worked after SPA routing. A public GitHub issue was a valid contribution candidate pending portal wallet submission.
