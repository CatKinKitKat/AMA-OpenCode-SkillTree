# Arena Maze and Vision Maintenance Notes

Use this reference when Hansa Arena appears to run but produces no useful reports or no survival.

## Durable lessons

- Do not treat silent Arena output as success when recent tournaments show zero survival. Silent means only that `hansa_arena_execute_silent.py` produced no user-facing stdout.
- Before changing any vision model, probe each configured provider's OpenAI-compatible `/models` endpoint. Do not rely on remembered model names.
- Live probe from this session:
  - `https://jiuuij.de5.net/v1/models` exposed `mimo-v2.5` and `mimo-v2.5-pro`.
  - `https://zapi.aicc0.com/v1/models` exposed `glm-5.1`.
  - `kimi-k2.6` was not exposed by either provider.
- If `kimi-k2.6` is not in `/models`, Hansa CAPTCHA must use the available `mimo-v2.5` / `mimo-v2.5-pro` route or another model proven live by `/models`.
- Arena game keys are not fixed. Always read `/api/arena/how-to-play` and `/api/arena/games/{game_key}` when survival drops or a new game appears.
- A new `maze` game appeared. A script that handles only `coin_snipe`, `crash_pilot`, and `captcha` will join Maze queues but never move, causing effective zero survival.

## Maze baseline strategy

Maze scoring: distance from center dominates (`dist_from_center * 10 + final_tile_value`), death or collapsed tile scores 0.

Minimum viable Maze executor behavior:
1. Read `maze_state` from `/api/arena/tournaments/{id}/rounds/{n}/my-pairing`.
2. Use `maze_state.position` / `current_position`, `health_left` / `health`, `walls_known` / `walls`, `visited` / `visited_tiles`, and `neighborhood` if present.
3. Submit `POST /api/arena/tournaments/{id}/rounds/{n}/maze-move` with body `{ "directions": "..." }`.
4. Do not use one long blind 20-step chain. Use short 1-3 move chains per cron tick. Unknown tile values have a fat tail and old long chains repeatedly died before scoring.
5. Push toward a far corner or edge while avoiding known walls/neighborhood walls and preserving a health stop-loss. A current baseline is budget `max(1, min(3, int((health - 35) // 12)))`. If health <= 38 and distance >= 6, hold rather than risk death.
6. If the API later exposes live crowd data via `maze-check`, use it near round end to avoid crowded collapse tiles.

## Reporting rule

For high-frequency Arena cron, silence is acceptable only for harmless no-op ticks. If a tournament eliminates the agent at 0 survival, or if submission fails repeatedly, report it. Zero survival is a strategy/debug signal, not noise.

## Verification pattern

- Compile scripts: `python3 -m py_compile ~/.agent/scripts/hansa_arena_collect.py ~/.agent/scripts/hansa_arena_execute_silent.py`.
- Manual dry live run: `python3 ~/.agent/scripts/hansa_arena_execute_silent.py`.
- Trigger cron: `cronjob run 817d044f33c5`.
- Confirm `cronjob list` shows `last_status=ok` and inspect `~/.agent-hansa/arena_state.json` for recent `submitted_rounds` / `submit_failures`.
