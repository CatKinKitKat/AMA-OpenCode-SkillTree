---
name: json-firs-fnnc-cli-patt
description: Absorb agent-facing patterns from trading/financial CLIs such as kraken-cli without blindly integrating live execution. Use when evaluating exchange CLIs, paper-trading shells, MCP-enabled finance tools, or when porting their JSON-first subprocess contracts, stable error taxonomies, paper-first workflow patterns, and machine-readable tool catalogs into the agent or trading research systems like ict-engine.
version: 1.0.0
author: the agent
license: MIT
---


# JSON-first Financial CLI Patterns

适用：
- 外部金融 CLI / 交易 CLI / paper trading CLI 评估
- 吸收 exchange CLI 的 agent contract，而非直接接 live trading
- 为 ict-engine / the agent 设计 json-first adapter、stable error taxonomy、paper-first workflow

不适用：
- 直接下真实单
- 凭 README 盲信 live-trading 接入

## 核心原则

1. 先安全审查，再看功能。
2. 默认吸收“agent contract”，不默认吸收“live execution”。
3. 优先抽取：
   - JSON-first subprocess contract
   - stable error categories
   - paper/sim before live
   - machine-readable tool catalog
   - workflow skill/recipe packaging
4. 若工具可触真实资金、账户、提现、杠杆：视为高风险。

## 吸收清单

### 1. JSON-first subprocess contract
目标：stdout 只放结构化 payload；stderr 只放诊断；退出码表达成功/失败。

建议模式：
```bash
somecli <command> ... -o json 2>/dev/null
```

要求：
- success -> stdout valid JSON
- failure -> stdout JSON error envelope
- exit code 0 success, non-zero failure
- 不靠人类提示文字做路由

### 2. Stable error taxonomy
至少抽成稳定类别：
- `api`
- `auth`
- `network`
- `rate_limit`
- `validation`
- `config`
- `io`
- `parse`

规则：
- 路由看 category，不看 message 文案
- retry 只对明确可重试类开放

### 3. Paper-first workflow
若外部工具有 live 与 paper/sim 双面：
- 默认先 paper
- 任何 live path 都需额外确认与权限隔离
- 在研究系统中，paper/sim 是 first-class，不是附属脚本

### 4. Machine-readable tool contract
优先寻找：
- `tool-catalog.json`
- `error-catalog.json`
- `CONTEXT.md`
- `AGENTS.md`
- `AGENTS.md`

吸收用途：
- 参数 schema
- dangerous flags
- auth requirements
- output contracts
- retry guidance

### 5. Workflow skills / recipes
若上游已把多步流程打包成 skills/recipes：
- 抽 workflow boundary
- 抽 safety boundary
- 抽 reusable sequence
- 不盲搬交易策略本身

## 针对 ict-engine 的落地建议

优先可吸收面：
1. 外部 market-data / exchange adapter 的 JSON envelope 统一
2. adapter 错误分类统一
3. paper/backtest/sim 与任何未来 live path 对称化
4. 将常见研究流打包为 skills/prompts，而非只堆 CLI flags
5. 若未来暴露工具目录，做 machine-readable catalog

不建议默认吸收：
- live order execution
- withdrawal / transfer / staking
- shared MCP trading server
- 任何无用户明确批准的危险命令

## 评估结论模板

- Verdict: learn / absorb / install / reject
- Absorb:
  - json contract
  - error taxonomy
  - paper-first symmetry
  - skill packaging
- Reject:
  - unsafe live automation by default

## 产物建议

若任务命中 repo/documentation 吸收：
- 写 repo docs note
- 写 architecture boundary rule
- 只在用户明确要求时再做实际 live integration
