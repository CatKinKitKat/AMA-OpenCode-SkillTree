---
name: herm-feis-gate-dbgg
description: Debug the agent gateway when Feishu/Lark credentials appear configured but the bot does not reply. Covers stale launchd env, platform-not-enabled states, websocket startup failure, and duplicate local gateway conflicts.
---


# the agent Feishu gateway debugging

用时机：
- 用户说“飞书联系 the agent 他不理我”
- 已配置 Feishu app 凭据，但无回复
- `agent gateway status` 显示服务在跑，仍怀疑飞书未接入

## 目标

先判定故障层：
1. the agent 运行时未读到 Feishu 配置
2. 平台未启用
3. 旧 gateway 未重载新配置
4. Feishu websocket/connect 失败
5. 另一个本地 gateway 占用同一 `app_id`

## 步骤

1. 验证 the agent 运行时实际读到的 Feishu 环境变量，而非只看磁盘上的配置文件：

```bash
cd ~/.agent/agent-runtime
. venv/bin/activate
python - <<'PY'
import os
from pathlib import Path
from agent_cli.env_loader import load_agent_dotenv
from agent_constants import get_agent_home
load_agent_dotenv(agent_home=get_agent_home(), project_env=Path('~/.agent/agent-runtime/.env').expanduser())
for k in ['FEISHU_APP_ID','FEISHU_APP_SECRET','FEISHU_DOMAIN','FEISHU_CONNECTION_MODE']:
    v=os.getenv(k,'')
    if 'SECRET' in k and v:
        v=v[:4]+'***'+v[-4:]
    print(k, bool(os.getenv(k)), v)
PY
```

2. 看 gateway 常驻实例是否真在跑：

```bash
agent gateway status
ps -p <PID> -o pid=,ppid=,etime=,command=
```

3. 先查日志，不要只信 status：

```bash
grep -n "Feishu\|No messaging platforms enabled\|failed to connect any configured messaging platform" ~/.agent/logs/gateway.log | tail -n 50
grep -n "Feishu\|No messaging platforms enabled\|failed to connect any configured messaging platform" ~/.agent/logs/gateway.error.log | tail -n 50
```

4. 若日志出现：
- `No messaging platforms enabled.`

则结论优先为：当前常驻 gateway 进程启动时未载入 Feishu 配置；常见于配置后未重启、launchd 旧进程仍在跑。

5. 若日志出现 Feishu 相关连接失败，再细分：
- `[Feishu] FEISHU_APP_ID or FEISHU_APP_SECRET not set` → env 未被进程读到
- `[Feishu] lark-oapi not installed` → 缺依赖
- `Unsupported FEISHU_CONNECTION_MODE` → 模式值错，只支持 `websocket` / `webhook`
- `Another local the agent gateway is already using this Feishu app_id` → 本机另一实例占锁
- `Gateway failed to connect any configured messaging platform:` → 平台启用但连接失败

6. 若怀疑是旧进程未重载配置，直接重启并验收：

```bash
cd ~/.agent/agent-runtime
. venv/bin/activate
agent gateway restart
```

7. 验收标准：

```bash
tail -f ~/.agent/logs/gateway.log
```

应看到近似：
- `[Feishu] Connected in websocket mode`
- `Gateway running with 1 platform(s)`

## 关键代码定位

- `~/.agent/agent-runtime/gateway/config.py`
  - Feishu 平台启用条件：`FEISHU_APP_ID` + `FEISHU_APP_SECRET`
- `~/.agent/agent-runtime/gateway/platforms/feishu.py`
  - `connect()` 内含依赖、凭据、连接模式、app_id 锁检查
- `~/.agent/agent-runtime/gateway/run.py`
  - 若 `connected_count == 0` 且 `enabled_platform_count == 0`，会写：`No messaging platforms enabled.`

## 实战判据

若同时满足：
- 运行时 env 检查里 `FEISHU_APP_ID/SECRET` 为真
- `agent gateway status` 显示服务 loaded/running
- 日志却写 `No messaging platforms enabled.`

则不要先怀疑用户消息格式；先判为“当前 launchd/gateway 进程未载入新 Feishu 配置”，重启 gateway 优先。

## 易错点

- 只看配置文件，不验证 the agent 实际加载结果
- 只看 `agent gateway status`，不看 `gateway.error.log`
- 自己再起一个 `python -m gateway.run`，却被已有 PID 挡住，误判为 Feishu 故障
- 误把 provider 429/timeout 当成飞书未接通；二者可并存，需分开看日志
