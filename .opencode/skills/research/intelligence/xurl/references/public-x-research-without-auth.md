# Public X research without API auth

Use this when the user asks to inspect X/Twitter for public market/project leads, but `xurl auth status` shows no registered app/token or the browser redirects `/search` to login.

Observed pattern:
- `xurl auth status` may print: `No apps registered. Use 'xurl auth apps add' to register one.`
- Public X search pages can redirect to `https://x.com/i/flow/login?...` in browser automation.
- Do not read `~/.xurl` or ask for pasted secrets.

Fallback workflow:
1. Search indexed public results with DuckDuckGo/Google using `site:x.com` queries.
2. Treat X snippets as leads only, not evidence.
3. Open official project pages linked from the lead or from search results.
4. Verify decisive claims on live official pages: title, docs, app UI, tasks, faucet, points/XP/rewards, waitlist/invite requirements.
5. Rank results by user constraints, not tweet hype. For low-cost web3/agent scouting, prefer: free/testnet/faucet, explicit points/XP, clear agent/on-chain role, no paid validator hardware, official task portal.

Useful queries:
- `site:x.com agent onchain testnet free points airdrop`
- `site:x.com AI agent crypto testnet points free`
- `site:x.com "AI agents" "airdrop" "testnet"`
- `site:x.com "agent" "faucet" "leaderboard" "testnet"`

Session examples verified by official pages:
- Knidos: `https://testnet.knidos.xyz/`: on-chain AI fund manager. Onboarding missions, AP, faucet, leaderboard/referrals. Invite/waitlist gating.
- dFusion AI: `https://testnet.dfusion.ai/login`: AI/data contribution flow. Uploads/URLs/docs/audio/video. Wallet/Google/Discord login.
- GenLayer: `https://www.genlayer.com/testnet`: AI consensus testnet. XP/points, quests, validator/builder tracks.
- Allora: `https://app.allora.network/points/campaign/run-inference-10m`: run worker/model inference for points. Faucet exists but compute/setup cost may make it not strictly zero-cost.
- Ritual: `https://faucet.ritualfoundation.org/`: testnet faucet. Access-code gated.

Pitfalls:
- Do not present indexed X snippets as current truth. Verify on official domains.
- Do not recommend paid validator tracks as "0 cost" unless faucet-only and no meaningful compute spend.
- If the user wants write actions, replies, likes, DMs, or timeline/mentions, stop and require proper `xurl` auth setup.
