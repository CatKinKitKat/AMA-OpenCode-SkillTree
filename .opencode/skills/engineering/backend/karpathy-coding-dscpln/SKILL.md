---
name: karpathy-coding-dscpln
description: Compact coding-discipline overlay for the agent based on Karpathy-inspired guidelines: think before coding, simplicity first, surgical changes, and goal-driven verification. Use when doing non-trivial code edits, reviews, refactors, or debugging where overengineering, hidden assumptions, or diff sprawl are risks.
version: 1.0.0
author: the agent
license: MIT
---


# Karpathy Coding Discipline

适用：
- 非平凡代码改动
- bugfix
- refactor
- review 前自检
- repo intake 后想吸收 coding discipline，而非安装 runtime

## 四原则

### 1. Think Before Coding
- 先显式假设
- 有歧义则列解释，不要静默选一条
- 若更简单路径存在，要指出
- 若关键前提不明，停下查明

### 2. Simplicity First
- 只写完成任务所需最小代码
- 不预埋未来配置层
- 不为单次使用做抽象
- 若 200 行可成 50 行，重写

### 3. Surgical Changes
- 只改请求直接命中的面
- 不顺手美化邻近代码
- 不删与任务无关的旧代码
- 只清理由自己改动造成的 orphan

### 4. Goal-Driven Execution
- 把任务转成可验证目标
- bug -> 先造复现 / 验证，再修
- refactor -> 前后验证不变
- feature -> 定义成功标准与检查方式

## the agent 化约束
- 默认吸收为行为 discipline，不必安装任何插件或外部 skill runtime
- 更适合并入 repo 局部 `AGENTS.md` / `AGENTS.md` / docs 约束
- 若项目已有更强本地规则，以项目规则优先

## 最适合的吸收方式
1. repo 文档追加短规则
2. 作为 review checklist
3. 作为实现前自检模板
4. 作为 plan/verify 提示模板

## 不建议
- 不要把它扩成长篇流程官僚文档
- 不要在简单一行改动上过度套流程
- 不要把“谨慎”变成“停滞”
