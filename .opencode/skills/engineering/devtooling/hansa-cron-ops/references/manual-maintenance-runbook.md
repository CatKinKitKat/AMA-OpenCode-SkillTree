# Hansa manual maintenance runbook

Use when the user asks to maintain cron jobs, clear Hansa dailies, or "赚钱/维护定时任务" and the normal scheduled job does not immediately execute.

## Durable pattern

1. Inspect cron state first: gateway running, exactly the expected Hansa jobs, no duplicate Arena job, no job-level model/provider overrides.
2. Compile the active scripts before executing them:
   - `python3 -m py_compile ~/.agent/scripts/hansa_arena_collect.py ~/.agent/scripts/hansa_prediction_rebate.py ~/.agent/scripts/hansa_checkin.py ~/.agent/scripts/skill_sources_daily_update.py`
3. Collect earning state:
   - `python3 ~/.agent/scripts/hansa_earning_collect.py`
   - Key fields: `daily_quests.all_completed`, per-quest `completed/progress`, `prediction.markets_count`, `arena.upcoming_games`, `engagement.assignments`, `alliance_war`.
4. If `cronjob run <earning_job>` or `agent cron run <earning_job>` only moves `next_run_at` and leaves `last_run_at` unchanged after a scheduler tick, do not wait indefinitely. Execute bottom-level maintenance scripts directly.
5. Clear automatic daily items:
   - `python3 ~/.agent/scripts/hansa_checkin.py`
   - `python3 ~/.agent/scripts/hansa_auto_earn.py`
6. If `hansa_auto_earn.py` succeeds on create/curate but `distribute` fails with a transient remote close, retry only `do_distribute()` once via import rather than rerunning the whole posting/curation flow.
7. Re-run `hansa_earning_collect.py` and require `daily_quests.all_completed=true` before reporting success.

## Reporting rules

- Report only actual cleared items and remaining human-only work.
- Do not call `available_usdc` "claimable". Only positive balance deltas or explicit payouts are claimable.
- Alliance War tasks requiring live social posts, screenshots, videos, external account proof, or real URLs are human-action items unless the user explicitly supplies the proof URL or expands scope.

## Retry snippet: distribute only

```bash
python3 - <<'PY'
import importlib.util, pathlib
p=pathlib.Path.home()/'.agent/scripts/hansa_auto_earn.py'
spec=importlib.util.spec_from_file_location('hae', p)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
state=mod.load_state()
ok=mod.do_distribute(state)
mod.save_state(state)
print('distribute_ok=', ok)
PY
```
