---
name: vibe-skills-gov-patterns
description: >
tags: 
version: 1
---


目标
- 吸收外部 skill OS 的治理方法，不引入第二控制面。
- 让 the agent 在 skill 数量增长后，仍保持低冲突、可验证、可冻结。

何时用
- 用户要研究或吸收 Vibe-Skills / VCO / 类 skill operating system 仓。
- 需要设计 skill promotion / freeze / destructive gate。
- 需要把“大量 skills 如何不互撞”落入 the agent 路由与治理。

默认立场
1. Learn + Absorb，非 direct-install。
2. 先做安全审查，再决定是否隔离安装。
3. 不把外部 runtime 当 the agent 第二 orchestrator。
4. 只吸收能降低未来 steering 的治理件。

高价值可迁移件
1. Primary route first
   - 先选一条主路由，再让 specialist 只在阶段内介入。
   - 避免多个同类 skill 同时争抢控制权。

2. Route 后再定执行级别
   - 先决定“谁负责”，再决定 M / L / XL。
   - the agent 可对应为：单代理 / 多步串行 / 可并行子任务。

3. Promotion metadata
   - 至少记录：promotion_eligible、contract_complete、destructive、snapshot_required、rollback_possible。
   - 没这些字段，不要谈自动 promotion。

4. Replay-ledger-first
   - 没有 replay / evidence ledger 的 adaptive routing 建议，不进入 promotion 讨论。
   - 先有证据，再有升格。

5. Destructive prompt gate
   - 对 delete / overwrite / reset / purge 类提示，单独打 destructive 标签。
   - destructive 命中时，不走无提示自动派发。
   - 需要确认、快照、回退条件三件套。

6. Proof bundle / execution manifest
   - done 不能只靠自然语言。
   - 要有测试、产物、验证路径、执行摘要等可检查证据。

7. Workspace memory plane
   - 可吸收“单控制面 + workspace 共享记忆”的思想。
   - 但 the agent 内必须保持 memory truth source 单一，不许第二 orchestrator 抢 authority。

the agent 落地规则
- 路由层：
  - 一个主 skill 负责总流程。
  - specialist 仅作为阶段/单元辅助，不夺全局调度权。
- 治理层：
  - promotion 必须 evidence-backed。
  - destructive 默认保守。
  - good skill freeze；middling 渐进修；bad 立即 patch 或停用。
  - 若先做轻量实现，优先把 promotion ledger 挂到现有安装/锁文件面，而非先造新运行时。
    - 在 the agent 当前代码中，优先落点是 `tools/skills_hub.py` 的 `HubLockFile.record_install()`。
    - 先记录 `eligible`、`proof_bundle_required`、`destructive_prompt_gate`、`source_origin`、`recorded_at` 即可。
    - 这些值应从 skill metadata 派生，如 `origin_repo`、`promotion_ledger_required`、`proof_bundle_required`、`destructive_prompt_gate`。
  - 配套测试优先补四类：
    1. guard 不误杀 replay ledger / destructive gate / workspace memory plane 等治理词
    2. skills index / meta dict 保真 `agent-created` trust level
    3. quarantine -> install -> lock file 路径上，promotion ledger 与 metadata 一并持久化
    4. CLI surfaced 面要能看见 ledger；至少补 `agent skills list` 与 `agent skills audit` 的断言
  - CLI 最小落地顺序：
    1. `agent_cli/skills_hub.py::do_list()` 增一列 `Promotion`
    2. hub skill 若有 ledger，显示 `ledger` / `proof` / `destructive` 三类短标签
    3. `do_audit()` 在 scan report 前打印 `Promotion Ledger` 与 `Promotion Source`
  - 测试实现时的经验坑：
    - CLI 层常是函数内局部 import；打桩时既要 patch `tools.skills_hub`，也可能要 patch `agent_cli.skills_hub` 当前模块名下符号
    - `Path.exists()` 若挡住 audit 路径，可在隔离测试里临时 monkeypatch；否则只会看到 path missing 警告
    - Rich 输出会自动换行，断言长串时宜拆成多个短断言，而非整行精确匹配
- 记忆层：
  - workspace memory 只做辅助读取/写入面。
  - 用户显式指令 > repo truth > memory policy > candidate advice。

不该照搬的东西
- 直接改写真实 host root 的安装器。
- 第二套 runtime authority。
- 未清洗即导入的上游 contract 名词与巨型 policy 面。
- 用“live degraded result”继续冒充完成。

实操顺序
1. 读 README / install path / governance config。
2. 找 host-root 写入点、upgrade/reset/uninstall 面。
3. 抽取 route / promotion / freeze / destructive / memory 五件套。
4. 只把能在 the agent 中机械执行的部分写入路由、skill、tests。
5. 若要新增治理规则，先补测试，再补实现。

验收
- 是否减少 skill 冲突？
- 是否让 promotion 更可证？
- 是否把 destructive 动作挡在更早处？
- 是否未引入第二控制面？
- 是否有 repo artifact / test 证明变更？

已知对 Vibe-Skills 的本机结论
- 适合吸收治理。
- 不适合默认直装到真实 `~/.codex` / `~/.the agent`。
- 其测试面暴露过 promotion metadata、freeze gate、macOS `/private/var` 路径一致性问题；故只取方法，不取现成运行面。
