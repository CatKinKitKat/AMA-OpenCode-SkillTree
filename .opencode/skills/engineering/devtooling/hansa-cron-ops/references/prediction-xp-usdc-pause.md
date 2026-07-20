# Prediction XP betting when USDC is paused

## Trigger
AgentHansa prediction bet returns HTTP 503 with text like:

```json
{"detail":"USDC betting is temporarily paused while we reconcile prediction-market balances. XP betting is still open — set stake_currency='xp' to keep playing."}
```

## Durable fix
Update the prediction cron script to use XP while USDC is paused:

```json
{"outcome":"yes","stake":1,"currency":"xp","stake_currency":"xp"}
```

Use `available_xp` from `/api/prediction/balance`. Do not gate on `available_usdc >= 0.5` during this mode.

On success, persist:

```json
{
  "last_bet_date": "<local-date>",
  "last_market_id": "<market-id>",
  "stake_currency": "xp",
  "last_response": {"pick": {"stake_currency": "xp"}}
}
```

This prevents duplicate same-day bets.

## Cron shape
Keep the job script-only/no-agent:

- `script=hansa_prediction_rebate.py`
- `no_agent=true`
- `enabled_toolsets=["terminal"]`
- daily schedule remains `31 0 * * *`
- prompt/name should say XP, not USDC rebate, while USDC remains paused

## Verification

```bash
python3 -m py_compile ~/.agent/scripts/hansa_prediction_rebate.py
python3 ~/.agent/scripts/hansa_prediction_rebate.py
```

Expected first successful run:

```text
✅ 预测 XP 下注完成: market=<prefix>... stake=1 XP
```

A later same-day run should be silent because `last_bet_date` is already recorded.
