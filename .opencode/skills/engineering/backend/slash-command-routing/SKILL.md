---
name: slash-command-routing
description: Route user intent to the agent slash commands before normal tool or skill execution. Use when the request is really a session-control, backgrounding, planning, queueing, resume, rollback, config, or gateway command trigger.
---


# Slash Command Routing

Goal
- Treat the agent slash commands as a first-class routing surface.
- When the user intent is really a slash command, prefer the slash command path over ad hoc tool behavior.

Use when
- The user asks for background execution, session control, queueing, plan mode, rollback, resume, status, model/provider toggles, or other the agent command-surface actions.
- The user mentions words like `后台`, `slash`, `斜杠命令`, `用 /background`, `先计划别执行`, `恢复会话`, `撤销刚才`, `压缩上下文`, `排队`, `暂停提问`, `快模式`, `reasoning`, `yolo`, `reload mcp`, `debug report`.

Core rule
- If a built-in slash command matches the user intent well, route to that command surface first instead of approximating the behavior with ordinary tool calls.
- For long-running autonomous work that should continue outside the current turn, prefer `/background` over only starting a raw background process.

Primary mappings

## 1. Background / asynchronous work
Trigger phrases:
- `后台`
- `后台跑`
- `后台监控`
- `继续盯`
- `跑完回报`
- `必要时介入`
- `先后台`
- `/background`

Route:
- `/background <self-contained prompt>`

Rules:
- The prompt must be self-contained: goal, workdir, commands, state files, expected output, failure handling.
- Do not use `/background` for trivial one-shot checks.
- If the user wants the current session free while work continues, `/background` is the default.

## 2. Plan mode instead of execution
Trigger phrases:
- `先计划`
- `别执行`
- `写方案`
- `plan mode`
- `/plan`

Route:
- `/plan [request]`

## 3. Queue next prompt
Trigger phrases:
- `排队`
- `下一轮再做`
- `等当前完成后再问`
- `/queue`

Route:
- `/queue <prompt>`

Important:
- Prefer `/queue`, not `/q`, because `/q` conflicts with `/quit` in practice.

## 4. Session reset / branch / resume / undo / retry
Trigger phrases and routes:
- `新开会话` / `重开` / `清空重来` -> `/new` or `/clear`
- `撤销刚才` -> `/undo`
- `重试上一条` -> `/retry`
- `恢复会话` / `继续之前那个` -> `/resume [name]`
- `分支试另一条路` / `fork this` -> `/branch [name]`
- `压缩上下文` / `对话太长` -> `/compress [focus topic]`
- `回滚 checkpoint` / `恢复快照` -> `/rollback` or `/snapshot`

Guideline:
- `/rollback` is for filesystem checkpoints.
- `/snapshot` is for the agent config/state snapshots.
- Distinguish them explicitly.

## 5. Status / usage / debug
Trigger phrases and routes:
- `状态` / `当前会话` -> `/status`
- `token 用量` / `费用` / `成本` -> `/usage`
- `debug report` / `上传日志` -> `/debug`
- `近 30 天分析` -> `/insights`

## 6. Model / provider / speed / reasoning / personality
Trigger phrases and routes:
- `切模型` -> `/model`
- `看 provider` -> `/provider`
- `快一点` / `fast mode` -> `/fast`
- `reasoning 高一点/低一点` -> `/reasoning`
- `换人格` -> `/personality`

## 7. Tools / browser / MCP / skills / cron / reload
Trigger phrases and routes:
- `开关工具` -> `/tools`
- `看 toolsets` -> `/toolsets`
- `接浏览器` -> `/browser`
- `技能搜索/安装/审计` -> `/skills`
- `定时任务` -> `/cron`
- `重载 MCP` -> `/reload-mcp`
- `重载 env` -> `/reload`
- `插件状态` -> `/plugins`

## 8. High-risk explicit override
Trigger phrases:
- `别再问审批`
- `全自动`
- `YOLO`
- `/yolo`

Route:
- `/yolo`

Safety:
- Only route here when the user explicitly asks.
- Do not infer it from impatience alone.

## 9. Messaging-only commands
When operating in chat/gateway contexts, these are first-class and should be recognized:
- `/approve`
- `/deny`
- `/commands`
- `/update`
- `/restart`
- `/sethome`

Do not suggest them in pure CLI-only contexts unless relevant.

Source of truth
- Slash command reference: `~/.agent/agent-runtime/website/docs/reference/slash-commands.md`
- Central registry: `~/.agent/agent-runtime/agent_cli/commands.py`

Router discipline
1. First ask: is this really a slash-command intent?
2. If yes, route to the slash command before generic tool use.
3. If no, continue normal skill/tool routing.
4. For slash-command routing updates, keep this skill and `.agent/routing/slash-command-router.md` in sync.

Pitfalls
- Do not approximate `/background` with only a raw background process when the user wants autonomous monitoring.
- Do not use `/q`. Use `/queue` explicitly.
- Do not confuse `/rollback` with `/snapshot`.
- Do not route to `/yolo` without explicit user intent.
