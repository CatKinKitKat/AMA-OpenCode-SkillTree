Absorbed from skill: sub-hdd-sb-puzzle-reverse

This reference stores the detailed platform/API reverse-engineering notes for sub.hdd.sb.

Key contents preserved:
- Platform identity, auth model, and shared game shell behavior
- Unified API patterns across puzzle2048, memory, puzzle15, and sudoku
- Difficulty configurations and reward structures
- Frontend file map and shared JS architecture
- API response examples and anti-cheat/session constraints
- Notes on server-authoritative gameplay, iframe access, and hub-entry behavior
- Historical automation notes and game-specific platform quirks

Original source skill archived after consolidation. Load umbrella skill `sub-hdd-platform-automation` for routing. Consult this file for deep platform details.

--- ORIGINAL SKILL CONTENT ---

sub.hdd.sb 号多多 AI API Gateway 的 4 款益智游戏逆向分析: API 端点、服务端权威机制、自动求解脚本。

Platform and unified route notes:
- domain: sub.hdd.sb
- auth via Bearer token / localStorage.auth_token / URL token / postMessage injection
- Vue SPA shell + native JS game pages
- shared CSS shell

Unified endpoints per game:
- GET /config
- GET /me
- GET /history
- POST /start
- POST /move|flip|fill
- POST /abandon

Important route-specific caveats:
- games are server-authoritative
- `daily_plays_remaining` is an object keyed by difficulty
- `auth_token` is a plain string, not JSON
- `@noframes` breaks embedded injection when actual gameplay lives in iframe
- userscripts should usually match `https://sub.hdd.sb/*`
- 2048 difficulty enums are mini/classic/jumbo, not easy/normal/hard
- puzzle15 uses direction semantics that may be inverse of local blank-motion solvers
- hub-entry pages permit same-origin iframe inspection for evidence gathering

Keep detailed examples and payload structures here when needed in future maintenance.