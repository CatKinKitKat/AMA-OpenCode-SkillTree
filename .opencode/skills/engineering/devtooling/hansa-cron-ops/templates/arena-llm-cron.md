# Arena LLM-driven Cron Job Template

## Job Name
`hansa-arena(LLM决策)`

## Schedule
`*/2 * * * *`

## Toolsets
`["terminal", "file", "web", "vision"]`

## Model
默认用户当前主模型。若需要 captcha 支持，切换到 kimi-k2.6：
```
agent cron update <job_id> --model kimi-k2.6 --provider httpszapiaicc0com
```

## Prompt Template

```
AgentHansa Arena — LLM-driven decision maker.

STEP 1 — Collect arena data:
terminal: python3 ~/.agent/scripts/hansa_arena_collect.py

STEP 2 — Parse output between ARENA_DATA_START and ARENA_DATA_END markers.

STEP 3 — For each action in actions_needed:

**coin_snipe decisions:**
- Analyze opponent career_pick_distribution and prior_submissions
- Counter their most common pick (undercut by 1-2)
- If opponent is balanced: use Nash-aware mixed strategy
  - Early rounds (alive>80): 5/6/10 mix (50%/30%/20%)
  - Mid rounds (20-80): 6/10/5/4 mix (45%/25%/15%/15%)
  - Late rounds (alive<20): above cutoff→safe(4/5), below→aggressive(10/6/9)
- Submit: terminal with curl POST /api/arena/tournaments/{tid}/rounds/{rnd}/submission
  Body: {"submission": <int 1-10>, "message": "agent adaptive arena strategy"}

**crash_pilot decisions:**
- Phase-based target: alive>100→1.30x, alive>40→1.55x, alive>12→1.75x, alive>4→1.82x, else→2.0x
- Add small jitter (±0.15 early, ±0.3 late) for anti-tie
- Avoid repeating last 3 targets (check arena_state.json crash_targets)
- Submit: terminal with curl POST /api/arena/tournaments/{tid}/rounds/{rnd}/submission
  Body: {"submission": <int target×100>, "message": "agent adaptive arena strategy"}
  e.g. 1.82x → submission 182

**captcha decisions:**
- Fetch image: terminal curl -o /tmp/captcha_arena.png "{captcha_image_url}" (URL from data)
- Use vision: vision_analyze the /tmp/captcha_arena.png image, identify which tiles contain the target object
- Submit: terminal with curl POST /api/arena/tournaments/{tid}/rounds/{rnd}/captcha-submit
  Body: {"selected": [tile_indices]} where indices 0-8 row-major
- If wrong (429 cooldown): wait 5s and retry with corrected answer
- If no vision capability: skip (don't waste API calls)

**bye_submit:**
- Submit safe default directly via terminal curl

STEP 4 — After submitting, update state:
- terminal: python3 -c "
import json
s = json.load(open('~/.agent-hansa/arena_state.json'))
s.setdefault('submitted_rounds', {})['{tid}:{rnd}'] = {'pick': <value>, 'status': <http_status>, 'game': '<game_key>'}
if '<game_key>' == 'crash_pilot':
    s.setdefault('crash_targets', {}).setdefault('{tid}', {}).setdefault('used_targets', []).append(<value>)
s['tournaments'].setdefault('{tid}', {})['highest_round_survived'] = max(s['tournaments'].get('{tid}', {}).get('highest_round_survived', 0), {rnd})
json.dump(s, open('~/.agent-hansa/arena_state.json', 'w'), indent=2, sort_keys=True)
"

STEP 5 — Report only meaningful events:
- resolved_results from the data (elimination/survival/champion/earnings)
- For coin_snipe: report "coin_snipe R{rnd}: pick={N} vs opponent={name}"
- For crash_pilot: report "crash_pilot R{rnd}: target={X}x"
- For captcha: report "captcha R{rnd}: selected={tiles}"
- If no actions needed and no results: output nothing (empty = silent)

CRITICAL RULES:
- ALWAYS run STEP 1 first — the collector script does all API calls efficiently
- Do NOT call Arena APIs directly — let the collector handle data gathering
- Only call submission APIs after making a decision
- For coin_snipe: submission is integer 1-10
- For crash_pilot: submission is int(target * 100)
- Both games require {"submission": <int>, "message": "<string>"} body
- Captcha requires {"selected": [int]} body to /captcha-submit endpoint
- Never submit the same round twice — check submitted_rounds in state
- If you can't decide (e.g. captcha without vision), just skip that action
```
