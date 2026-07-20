# React app API fallback when browser automation hangs

Use when an ordinary browser task (fill form, click submit, start mining/job) times out but the page is a client-rendered app with static JS assets.

Observed pattern
- `browser_type`, `browser_snapshot`, or `browser_console` timed out after page load.
- Entry HTML still exposed the bundled asset path, e.g. `/assets/index-*.js`.
- The minified bundle contained API route strings and enough client logic to reproduce the intended UI flow through HTTP.

Workflow
1. Fetch the entry HTML without cookies if no sensitive session is needed.
2. Extract module asset paths (`/assets/index-*.js`).
3. Download the JS bundle and search for `/api/` endpoints, form field names, and submit payloads.
4. Use a cookie jar / session-aware opener for the same origin.
5. Reproduce only the user-requested UI action through the documented endpoints.
6. Verify with a read endpoint or the API response, not with assumed UI state.

Concrete b-money example
- Create account: `POST /api/accounts` with `{"pseudonym":"...","passphrase":"..."}`.
- Login/unlock: `POST /api/auth/login` with `{"accountId":11010,"passphrase":"..."}`.
- Mining challenge: `GET /api/mining/challenge` returns `challengeId`, `prefix`, `difficulty`.
- Proof: find `nonce` such that `sha256(prefix + str(nonce)).hexdigest().startswith('0' * difficulty)`.
- Submit: `POST /api/mining/submit` with `{"challengeId":"...","accountId":11010,"nonce":N,"hash":"..."}`.

Pitfalls
- Challenges can be globally solved by another node before submission. Retry from a fresh challenge.
- Rate limits may return `429 Rate exceeded`. Back off instead of hammering.
- The accounts list endpoint may be rate limited even when create/login succeeded. Use create/login responses for account ID when possible.
- Keep credentials task-scoped and report them to the user only when the user asked you to create the account.
