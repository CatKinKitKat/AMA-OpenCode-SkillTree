---
name: prob-firs-cdp-paym-orch
description: 对真实 Chrome + CDP 的支付/回调编排，先固化 contract 与边界，再用 probes 采证；未知站点规则不得直接升入主线。
triggers:
---


# Probe-first CDP Payment Orchestration

适用场景：
- 仓内已有旧浏览器脚本，但目标架构要切到真实 Chrome + CDP。
- 流程含 Stripe/支付宝/扫码/callback 等长链路页面状态。
- 用户要求用真实浏览器登录态，不接受隔离 browser 冒充正式面。

## 核心原则

1. 正式浏览器面只认真实 Chrome + CDP remote debugging。
2. 一次 payment session 只占一个 tab。
3. tab 在 callback terminal state 前不得关闭。
4. dashboard 只展示和触发状态，不直接控制浏览器内部细节。
5. 旧巨石脚本或 legacy browser runner 只能当过渡桥或 experimental adapter，不得继续长成新业务主线。
6. 未经 probes 取证的 DOM selector、URL 规则、network matching、callback 判定，不得直接写进 core/services。

## Durable state contract

持久化只存这些：
- browser_profile_id
- tab_id
- account_id
- payment_session_id
- current_url / last_seen_url
- callback_status
- last_error
- created_at / updated_at

不要把这些当 durable state：
- runtime page/browser handle
- 临时 JS object 引用
- auth token
- 调试日志里的敏感 cookie / header

## 目录分层

正式层：
- core: 只消费已证实 contract
- services: 只做 orchestration 装配
- payment: tab registry / callback state / stable contracts
- storage: 持久态
- dashboard: 展示态

实验层：
- probes/: 只采证，不参与正式状态迁移
- adapters/experimental/: 站点未证实前的桥接实现

禁忌：
- dashboard -> browser direct control internals
- providers -> callback state decisions
- old giant script -> new business home
- probes -> production services hard dependency

## 迁移判定

若文档已定“real Chrome + CDP 为正式面”，但代码里唯一非 stub backend 仍桥到旧脚本：
- 视为 experimental/transition path
- 不要把它包装成正式 backend
- 最好显式改名为 `*_probe` / `legacy_*` / `experimental_*`

## 推荐推进顺序

1. 先落文档
   - browser control decision
   - state machine
   - architecture boundaries
2. 再落纯 contract 内核
   - tab registry
   - callback state machine
   - usage parser / payload preservation
3. 再写 probes
   - selector candidates
   - response URL capture
   - callback terminal evidence
   - usage/reset payload samples
4. 证据稳定后，才把规则提升到正式 adapter / worker

## Terminal-only closure reality check

当用户问“是不是终端里填一个 Gmail 就能躺平出 Stripe / dashboard / 扫码 / 自动整合”时：

不要只看 master plan。按下列顺序做机械核验：

1. 查 CLI 真入口
   - 看 `app/cli.py` 暴露了哪些 `register-backend` / `payment-backend`
   - 再看 `app/bootstrap.py` 实际把它们接到哪些实现
2. 跑一条最小 stub 闭环
   - 用仓内 venv，而不是系统 `python3` / 裸 `pytest`
   - 例：`.venv/bin/python -m app.cli run --count 1 --base-email <gmail> --register-backend stub --payment-backend stub`
3. 查真实链路缺口
   - 搜 `31tu` / `gmail.31tu.com` / `mail31tu`，确认是否真有 Gmail 收码 provider
   - 搜 `wind2api` / `windsurf2api`，确认是否真有自动整合面
4. 判 dashboard 是否只是落盘
   - 看 `app/services/dashboard_state.py` 之类是否只有 JSON/manifest writer
   - 若未见 HTTP server / UI / websocket 主线接线，就不要称其为“已能弹 dashboard”
5. 判 payment 是否仍属 experimental
   - 若非 stub backend 仍是 `legacy_*` / `*_probe`，或只会开 tab / 采证，不要称其为正式闭环

结论口径：
- stub 跑通 ≠ 真实闭环跑通
- 若真实 register 仍绑旧 mail provider、无 31tu provider、无 dashboard server、无 wind2api 集成，则只能说“stub 可闭；真实链未闭”
- 对外给用户时，应直接列 blocker，而不是复述计划愿景

## Phase gate（2026-04-27 实测补充）

把“纯 contract 阶段完成”定义清楚：
- 已有文档真相源：`browser-control-decision` 与 `state-machine`
- 已有纯内核 contract：`TabRegistry` 至少含 `register/get/keepalive/update_url/snapshot/from_snapshot`
- 已有 usage 解析 contract：能抽 `daily/weekly/reset` 候选 key，未知 payload 原样保留到 `raw_payload`
- 新测试先红后绿，且 targeted tests / 全量 tests / compile 校验都过

满足以上后：
- 下一层只许进入 `probe/experimental`
- 允许改动面：probe 文档、probe artifact、experimental adapter、对应测试
- 暂禁改动面：旧巨石脚本、真实浏览器 worker、storage schema、pipeline、dashboard/UI、正式 selector 规则

目的：
- 先把边界与 contract 锁死
- 再让 probes 只做采证，不借机偷渡主线逻辑

## Probe 输出最低要求

每次 probe 至少落盘：
- account/session context
- tab id
- current URL timeline
- decisive network response URL or body snippet
- selector candidates with page context
- callback success/failure evidence
- sample raw payload for usage/reset surfaces

## Minimal live-tab evidence increment

当 `real_chrome_cdp_probe` 已能 `version/new/activate`，但 `last_seen_url` 仍只信 `open_tab()` 返回值时，下一步最小安全增量是：

1. 先重开 `docs/change-surface.md`，把可改面收窄到：
   - `docs/change-surface.md`
   - `app/adapters/experimental/real_chrome_cdp_probe.py`
   - `tests/test_real_chrome_cdp_probe.py`
2. 先写红测，不先写实现。至少覆盖：
   - `CdpHttpClient.list_tabs()` 命中 `/json/list`
   - 无 live tab 命中时，`last_seen_url` 回退 `open_tab` 结果
   - 有 live tab 命中时，`last_seen_url` 取匹配 tab 的实时 URL
3. 匹配规则先用最窄 contract：按 `tab_id` 精确匹配，不引入 title/url 模糊规则。
4. `probe_artifact` 只允许追加最小观察字段：
   - `observed_tab_count`
   - `matched_tab_title`
   - `matched_tab_type`
   - `last_seen_url_source`
5. 禁止顺手扩大到：
   - CLI / bootstrap 改参
   - 正式 `payment/*` / `pipeline` / `storage`
   - DOM selector、callback 判定、network matching 规则
6. 验收至少包括：
   - `.venv/bin/python -m pytest tests/test_real_chrome_cdp_probe.py -q`
   - `.venv/bin/python -m pytest -q`
   - `.venv/bin/python -m compileall app tests`
   - 清理 `app/tests` 下 `__pycache__`

此步仍属 experimental evidence。若想把 `/json/list` 结果升格为正式 tab registry 或 callback 决策依据，必须另开 surface。

## Live snapshot failure fallback

当 `open_tab()` 与 `activate_tab()` 已成功，但 `/json/list` 取证临时失败时：

1. 把 live-tab snapshot 视为 advisory evidence，不是主路径硬依赖。
2. 在 experimental probe 内软失败回退：
   - `last_seen_url` 回退 `open_tab` 返回 URL（再退才用原始 `stripe_url`）
   - `observed_tab_count = 0`
   - `matched_tab_title = ""`
   - `matched_tab_type = ""`
   - `last_seen_url_source = "open_tab"`
3. 不要顺手污染正式面：
   - 不新增 durable error/state 字段
   - 不写 `last_error`
   - 不把 `/json/list` 异常升级成 callback / tab-registry 正式规则
4. 测试先行：先写一个 `list_tabs()` 抛错的 fake client 红测，再补最小实现过绿。

此类降级仍属 experimental resilience。若要记录异常原因、上报监控、或持久化失败状态，须另开 `change-surface`。

## Activate ack shape tolerance

当 `/json/activate/<tab_id>` 已返回 HTTP success，但响应体不是 JSON dict（空体、纯文本、布尔值等）时：

1. 把 activate 视为 ack surface，不是高价值证据面。
2. `CdpHttpClient.activate_tab()` 先保证 HTTP 成功，再单独处理响应体：
   - JSON 解析失败 -> 归一为 `{ "activated": true }`
   - 解析成功但不是 dict -> 归一为 `{ "activated": bool(payload) }`
3. `RealChromeCdpPaymentProbe` 内不要假定 `activate_tab()` 一定可 `.get(...)`；先做最小 dict 归一。
4. 不要顺手扩大：
   - 不新增 raw response 持久化字段
   - 不写 `last_error`
   - 不把 activate 响应形态差异升格为正式 callback / registry 规则
5. 测试先行，至少两条：
   - `CdpHttpClient` 命中 non-JSON activate response 时仍返回 `{ "activated": true }`
   - probe client 返回 non-dict activate payload 时，整条 payment payload 仍可落出

此类容错只为 experimental 开 tab 主路径保活。若要记录 activate 原始响应、异常分类、或做正式监控/告警，须另开 `change-surface`。

## Code review checklist

看到下列情况，应立即判为越界：
- core/services 里硬编码未经证实的 Stripe selector
- callback success 规则写死但无 probe evidence
- payment backend 直接持有 browser handle 并假定可恢复
- dashboard 直接操作浏览器而非走状态/command boundary
- legacy script 被继续加业务而不是被薄封装或降级

## Wind-down rule

若下一步需要碰：
- 旧巨石脚本大改
- 正式 payment worker
- storage schema 扩展
- dashboard server/UI 深改

先确认 change surface，再继续；不要借 probe 名义偷渡进主线。
