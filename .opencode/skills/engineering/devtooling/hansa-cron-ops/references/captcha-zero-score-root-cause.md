# Captcha 0 分根因深度分析

日期: 2026-05-25
Session Context: AgentHansa Arena 淘汰调查（captcha 被淘汰为啥，你研究明白）

---

## 用户问题
captcha 被淘汰为啥？

## 核心发现

### 1. 我们确实在 captcha 比赛中
`arena_state.json` 验证：`259d9bba-f897-4984-ad9b-29c6ffdf91de`
- `joined=True`
- `eliminated=True`
- `highest=None`: **0 轮存活**

### 2. 根本不在 leaderboard 上
现场 API 调查：
- `GET /api/arena/tournaments/259d9bba/leaderboard` → 返回 133 个 participants
- **agent_id `5ee4f3b0-e9ea-496e-94aa-5cd79b60c3e9` 不在其中**
- 说明加入后未产生任何有效提交（score=0 + place=末位）

### 3. 5164 次 cron = 0 次实际 vision_analyze
Cron 输出扫描结果：
```
参考文件: ~/.agent/cron/output/817d044f33c5/
文件数量: ~5164 个 .md 输出文件（*/2 频率，约 7 天累积）
匹配关键词: "vision_analyze" — 0 次实际工具调用
匹配关键词: "captcha" — 约 50 次（但全是 prompt 文本匹配，非执行）
匹配关键词: "captcha-submit" — 0 次 DRY RUN 记录
```

**关键区别**：
- Prompt 文本包含 `vision_analyze` 和 `captcha-submit` 说明
- 但 `817d044f33c5` job 的所有输出文件均为空或 `[SILENT]`
- 没有一个文件包含 `vision_analyze` 的实际工具调用记录

### 4. Captcha 分支缺少确定性推荐链
`hansa_arena_collect.py` 在 captcha 场景下输出：
```json
{
  "id": "...",
  "name": "...",
  "current_round": {"round_number": 1},
  "participants": [...],
  "captcha_image_url": "https://...",
  "captcha_note": "Select the trucks",
  "needs_action": true
}
```

**对比 coin_snipe / crash_pilot**：
- Coin snipe: `deterministic_recommendation.pick = 6`（明确数值）
- Crash pilot: `deterministic_recommendation.target = 1.30`（明确数值）
- Captcha: **只有 `captcha_image_url` + `captcha_note`**

### 5. Vision 能力可用性
虽然配置为 `model: kimi-k2.6`、`provider: httpszapiaicc0com`、`enabled_toolsets: [..., vision]`：
- kimi-k2.6 本身支持 vision（已通过 `image_url` 格式直接验证）
- 但 the agent cron 的 vision tool 从未被 arena 逻辑触发
- 原因：captcha 分支缺少 `vision_analyze` 调用触发条件

---

## 技术侧分析

### Vision Model 验证记录
```bash
# 直接 API 测试（通过）
curl https://zapi.aicc0.com/v1/chat/completions \
  -H "Authorization: Bearer ..." \
  -d '{"model":"kimi-k2.6","messages":[{"role":"user","content":[{"type":"text","text":"Describe this"},{"type":"image_url","image_url":{"url":"https://example.com/img.jpg"}}]}]}'
# Result: 正常返回图像描述
```

### Cron Job 配置
```yaml
job_id: 817d044f33c5
model: kimi-k2.6
provider: httpszapiaicc0com
enabled_toolsets: ["terminal", "file", "web", "vision"]
no_agent: false  # LLM-driven，非脚本
```

### 为什么 vision 没被调用？
1. **Prompt 模式问题**：旧 prompt 是 "decision maker" 模式 → LLM 需要先 "分析" → 再决定 → 再调用 → 但实际上 silence 了
2. **工具调用链断裂**：captcha 需要 LLM 主动调用 `vision_analyze`，但 arena 场景下 LLM 从未主动触发（对比 earning cron 的 vision 任务会主动调用）
3. **静默机制**：当 `actions_needed` 为空或 collector 报错时，cron 输出 `SILENT`，导致工具调用记录缺失

---

## 排除的其他假设

| 假设 | 验证 | 结论 |
|------|------|------|
| 根本没 join captcha | `joined=True` in state | ❌ 已 join |
| captcha 比赛不存在 | `GET /tournaments?status=live` 返回 captcha R4 | ❌ 存在 |
| vision model 不可用 | 直接 curl 测试通过 | ❌ 可用 |
| API 限流导致无法提交 | 有 throttle，但 captcha 无提交记录 | ❌ 无关 |
| 被对手淘汰 | 133 人榜中无我们，0 轮淘汰 | ❌ 自因 |

---

## 修复方案

### 方案 A（推荐）：跳过 captcha
在 `hansa_arena_collect.py` 的 `get_tournament_needs_action()` 中：
```python
if tid == captcha_tid:
    # Skip captcha — no vision execution in cron
    state['tournaments'].setdefault(tid, {})['skip_reason'] = 'captcha_no_vision_chain'
    return None
```
**代价**: 放弃 captcha 潜在收益（但当前收益为 0）
**收益**: 专注 coin_snipe + crash_pilot，确定性策略确保生存

### 方案 B：保留但接受 0 分
不修改 collector，但更新 prompt 明确说明 captcha 不可行。
**代价**: 每轮 captcha 0 分拖累总分
**收益**: 若 captcha 能偶尔命中（0.2% random），可能有微量收益

### 方案 C：修复 captcha vision 链
1. 在 collector 中下载 captcha 图片
2. 直接通过 HTTP POST（非 the agent vision tool）发送到 vision API
3. 将 vision 结果（tile indices）写入 `deterministic_recommendation`
4. LLM 只负责无脑提交

**技术难度**: 中（需要集成 vision API 到 Python 端）
**可靠性**: 高于 LLM 端 vision（避免工具调用链断裂）

---

## 2026-05-27 follow-up: captcha chain repaired, but local joined-state drift caused misses

### New evidence
- Current cron shape was healthy: exactly one arena job, `817d044f33c5`, `no_agent=true`, `script=hansa_arena_execute_silent.py`, schedule `*/2 * * * *`, model/provider null.
- `arena_state.json` showed captcha successes for `a581d6d7-0217-438d-a693-7da88633efa2` rounds 1, 2, and 4:
  - R1 `status=correct`, selected `[2,8]`, score 428
  - R2 `status=correct`, selected `[0,1,2,8]`, score 567
  - R4 `status=correct`, selected `[1,4]`, score 533
- Same tournament later had `tournaments[tid].joined=false`. The collector skipped live captcha before fetching pairing, despite the platform still serving `/rounds/{rnd}/my-pairing` for our agent.
- Manual repro after patch fetched R8 grid and vision solved `ANSWER=[0,2,3,4,8]`. Submit returned `409 not_live` because the round had already closed. Leaderboard showed `survived=false`, rank 24, cumulative 1528.

### Root cause refinement
The original no-vision-chain root cause is fixed in the fast executor: captcha images are downloaded and sent directly to `kimi-k2.6` from Python, and correct submissions are persisted only when response `status == "correct"`.

The new failure mode was local state drift:
```json
"tournaments": {"a581d6d7...": {"joined": false}}
```
This stale local marker overrode live evidence and caused the collector to skip future captcha rounds. Because `--silent` suppresses non-earning output, the cron looked healthy while it was no longer attempting live captcha.

### Fix applied
`hansa_arena_collect.py` now:
1. Does not skip a live tournament solely because local `joined=false` when prior successful submissions exist.
2. Probes live join/pairing first. If pairing is served, it proceeds.
3. Applies leaderboard elimination gating to captcha as well as coin/crash.
4. If leaderboard row has `survived=false`, marks eliminated and skips vision to avoid wasting a slow image solve after elimination.
5. Computes `highest_round_survived` from actual successful submitted rounds where available, not `current_round - 2`.

### Verification
- `python3 -m py_compile ~/.agent/scripts/hansa_arena_collect.py ~/.agent/scripts/hansa_arena_execute_silent.py` passed.
- `python3 ~/.agent/scripts/hansa_arena_collect.py --execute --silent` exited 0.
- Live cron state still has exactly four Hansa jobs and no duplicate arena job.
- Next joinable upcoming tournament `08e42fc4-795a-4475-9b3d-8a0c130fe749` is marked `joined=true`.

## 关联文件
- `hansa_arena_collect.py`: captcha vision + live joined-state drift fix
- `hansa_arena_execute_silent.py`: cron wrapper for execute+silent
- `arena_state.json`: 状态验证源
- `cron/output/817d044f33c5/`: 执行历史
