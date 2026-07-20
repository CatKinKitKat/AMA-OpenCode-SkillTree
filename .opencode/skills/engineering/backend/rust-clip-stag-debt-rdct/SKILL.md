---
name: rust-clip-stag-debt-rdct
description: Staged workflow for clearing Rust clippy debt in large repos without thrashing — compile/API migration first, then low-risk mechanical lints in batches, then signature/type refactors, with cargo check between phases.
---


# rust clippy staged debt reduction

何时用：
- 大型 Rust 仓 `cargo clippy -- -D warnings` 爆出成批告警。
- 仓内同时存在编译迁移债、机械 lint、签名/结构重构债。
- 需要压低来回 thrash。

核心法则：
1. 先绿 `cargo check`，后打 clippy。
2. 先 API/编译迁移，后机械 lint，最后结构性 lint。
3. 机械债按文件簇分批清；每批后复验。
4. 若修完一层告警，clippy 常会暴露下一层；属常态，不算回退。
5. 对机械批次，优先用子代理并行；对签名/结构批次，集中主线处理。

推荐阶段：

## 阶段 0：基线
- 跑 `cargo check`
- 若不绿：只修编译/API 迁移
- 典型迁移：多参函数改 input struct、builder/adapter 调用面统一、import/re-export 收口
- 未回绿前，不做 clippy 清债

## 阶段 1：低风险机械债
优先处理：
- `needless_range_loop`
- `if_same_then_else`
- `redundant_field_names`
- `needless_borrows_for_generic_args`
- `cloned_ref_to_slice_refs`
- `useless_conversion`
- `useless_format`
- `needless_option_as_deref`
- `filter_map_bool_then`
- `nonminimal_bool`

做法：
- 按模块簇分批：如 `hmm/*`、`ict/*`、`math/indicators/*`
- `needless_range_loop` 只改成 `iter()/iter_mut()/enumerate()/skip()/take()`，不混入业务改动
- 每批后：
  - `cargo check`
  - `cargo clippy --all-targets --all-features -- -D warnings`
- 若全量 clippy 太吵，可先过滤目标文件确认该批告警已消失，但最终仍要回全量 clippy

## 阶段 2：中等结构债
典型：
- `type_complexity`
- `field_reassign_with_default`
- 测试/fixture 的旧式调用残留

做法：
- `type_complexity`：优先 `type alias`
- `field_reassign_with_default`：改 struct literal + `..Default::default()`
- 若测试区仍有旧 API 调用，先同步测试，再复验

## 阶段 3：高改动签名债
典型：
- `too_many_arguments`
- `large_enum_variant`

做法：
- 引入小型 `Input` struct / config struct / param packet
- 先改定义，再一次性 sweep 全部 call site（生产代码 + tests）
- 同步更新 re-export 与 import
- 每次签名改动后立刻全仓搜索剩余旧调用

## ict-engine 实战教训
1. `AgentPrompt::new(...)` 迁移完，不代表 clippy 可打；先再跑 `cargo check`，让更早 adapter/input 迁移先浮出。
2. 大仓 clippy 清债宜拆三刀：
   - API 迁移收口
   - 机械 loop/lint 批量清
   - input struct / type alias 收尾
3. 子代理适合处理低风险机械 clippy 批次；主线程保留给跨文件签名改动。
4. 当“最后几条”清完后，clippy 可能继续暴露 `main.rs`/tests 的深层旧债；需接受分层暴露，而非误判前面修错。
5. 若剩余主要集中在 `main.rs` 的 `too_many_arguments`，不要随机挑函数；按调用层级分波次拆：
   - 先 CLI/command 入口
   - 再 live/ingest 与 workflow snapshot 等共享入口
   - 再 research/backtest/update 主链
   - 最后 analyze/backtest 深层 builder/helper
   - `large_enum_variant` 通常最后做，避免过早扩散 call site
6. 对 `too_many_arguments`，优先引入局部 `Input` struct/args struct，并在函数体开头一次性解构；这样最稳，行为面最小。
7. 每拆完一波 command/input struct，要同步 sweep：生产调用点 + tests；否则 `cargo check` 常会先被测试区旧签名挡住。
8. 若某轮把 builder / adapter / artifact 构造器改成 `Input` struct，不要只改库内定义；要立刻 sweep 三类面：
   - `src/main.rs` / bin 入口旧调用
   - tests / fixtures 旧调用
   - `mod.rs` re-export 与顶层 import
   否则 `cargo check` 常会卡在“函数现只收 1 参，但旧 callsite 仍传 N 参”与“新 Input struct 未导出/未导入”。
9. 当 clippy 清单已从目标模块转移到 `main.rs` / tests，大多表示原定尾盘模块已基本清完；不要误判为回退。此时应切换策略：先扫旧 callsite 与机械 lint，再决定是否继续做 `too_many_arguments` input struct 化。
10. 全量 `cargo clippy` 若仍未绿，但只剩 warning，可先用不带 `-D warnings` 的全量 clippy 观察“剩余唯一告警清单”，避免被 bin/bin test duplicate 噪声误判规模。
9. 若用脚本/批量替换把多参函数改成 input struct 调用，禁做过宽尾部替换（尤其把普通函数调用尾部统一改成 `})?;` 这类模式）。Rust 大仓里 `append_*` / `save_*` / `persist_*` 等普通调用很多，极易被误伤成括号错配。更稳顺序：
   - 只对明确命中的函数名做替换，不做全局尾部模式替换
   - 每做完一批 callsite 立刻跑 `cargo check`
   - 若怀疑误伤，先全仓搜 `})?;` / `})` 异常尾部，再逐处核对是否真是 struct-literal 调用
   - 对测试区与辅助持久化函数同样复验；这些地方最易被漏扫或误改
10. 在长时清债后若用户要求 `commit`，不要直接提交当前脏树；先审 `git status --short` 与 `git show --stat` 预期范围。大型 Rust 仓常混入先前未跟踪 docs/scripts/debug 产物或相邻任务改动。更稳顺序：
   - 先只提交本轮核心清债文件
   - 若已误混入，`git reset --mixed HEAD~1`
   - 再按“核心源码变更 / 杂项文档脚本”分拆 commit
   - 若用户只要本轮结果，直接清掉工作区杂项，保持树干净
10. 当把 builder/adapter/constructor 改成 `Input` struct 后，不要只改定义与局部测试；立刻全仓 sweep 三类残留：
   - `main.rs`/bin 级旧 callsite
   - 模块 `pub use` / re-export 缺口
   - 兄弟 adapter 模块里仍按旧多参签名调用的 helper
   否则 `cargo check` 会从“too_many_arguments 已修”转成“大量 E0061/E0432 残留”，表面像新故障，实为 callsite 尾扫未完成。
11. 对超大 `main.rs` 仓，input-struct 化后常见真实阻塞不是下一批 clippy lint，而是 bin 侧旧调用洪峰。此时先停机械 lint，先清 `main.rs`/integration callsite，再回到 clippy 批次；收益最高。
12. 若为旧多参函数保留了一个“adapter / compat wrapper”并继续让它接收 8+ 参，clippy 仍会卡在该 wrapper 本身。不要只把深层 builder 改成 `Input` struct；连同外层 `adapt_*` / `build_*_compat` / trace builder 也要一起 packet 化，否则只是把 `too_many_arguments` 往外推一层。
13. `cargo check` 回绿后，下一次 `cargo clippy -D warnings` 常会立刻把剩余面压缩成“少数真正结构债清单”：兼容 wrapper 的 `too_many_arguments`、共享 trace builder 的多参签名、以及独立 `type_complexity`。此时应顺势改成：
   - 先把 wrapper / orchestration builder 继续 input-struct 化
   - 再用 `type alias` 收掉孤立 `type_complexity`
   - 最后回头扫剩余 public API
   不要误以为前一轮 callsite 清扫失败。
14. 当 `main.rs` 成为主要 clippy 债源，先按“命令入口 -> 主链 helper -> 深层 builder”分批：
   - 第一批适合 packet 化：`workflow_status_command`、`factor_pipeline_debug_command`、`backtest_command`、`update_command`
   - 每个命令入口新增 `*CommandInput<'a>` 后，在函数开头解构到旧局部变量，避免扩大 diff
   - 同步改 CLI match arms 与测试区直接调用；测试残留旧调用常不会被普通 lib `cargo check` 提前暴露，必须跑 `--all-targets`
15. 可用脚本批量迁移明显同构 callsite，但必须立刻跑 `cargo check`，并检查是否误伤相邻闭包/表达式。实战误伤例：把无关 `BTreeMap::from([...])` 前缀错改成字段名（如 `raw_pre_bayes_labels:`），导致“struct literal body without path”。批量替换只适合低歧义模式；复杂多行调用优先人工 patch。
16. 对 `adapt_*` / `build_*` callsite 从多参改 input struct 时，Rustfmt 会重排大块代码；不要把 formatter diff 当作语义变更。先保持行为等价，再用 clippy 输出确认剩余唯一债。
17. 在超大 `main.rs` 的第二波 `too_many_arguments` 清债里，命令入口常有更高收益批次顺序：
   - 第一批：`workflow_status_command`、`factor_pipeline_debug_command`、`backtest_command`、`update_command`
   - 第二批：`factor_research_command`、`run_factor_research`、`artifact_status_command`
   - 第三批再进 analyze/live 主链：`persist_live_data_source`、`analyze_live_command`、`build_analyze_report`、`run_probabilistic_backtest`
   这样可先压掉 CLI/测试直接调用最密的面，再进入更耦合的分析链。
18. 当批量把 `run_*` / `*_status_command` 调用改成 input struct 时，常见新编译错误不是类型设计错，而是 callsite 文本迁移残留：
   - 旧局部名未替换成 `input.*`（如 `mutation_spec_path`）
   - 自动替换后缺尾逗号，导致 struct literal 语法错
   - 旧测试调用仍保留多参形式
   碰到这类错误，先局部读回源码，修字段名与尾逗号，再跑 `cargo check`；不要急着回退整个 packet 化策略。
19. 绝不要对超大 `main.rs` 做“把 `) ?;` / `)?;` 一把替成 `})?;`”这类宽匹配收口替换。实战会误伤无关函数调用（如 `save_state(...)`、`append_*_history(...)`、artifact ledger 写入），制造大面积 delimiter 破坏。更稳做法：
   - 只对明确已改成 `*Input { ... }` 的 callsite 做定点替换
   - 每做一小批就立刻 `cargo check`
   - 若出现 `mismatched closing delimiter`，优先全局搜最近误改的 `})?;`，而不是怀疑新 input struct 设计本身
20. 当批量修 delimiter 误伤时，先把 `search_files(pattern="\}\)\?;")` 结果按两类分开：
   - 合法：已改成 `SomeFunc(SomeInput { ... })?;`
   - 非法：普通函数/append/save 调用被误改成 `})?;`
   只回滚第二类。否则很容易把刚改好的 input-struct callsite 又反向破坏。
21. 测试里若为了消 `needless_update` / `field_reassign_with_default` 去改 `..Default::default()`，先确认该 struct 不是“字段持续增长”的状态对象（如 `DatasetComparability`）。这类测试 fixture 更稳策略：
   - 若只改少数字段，保留 `..Default::default()`
   - 仅在确知所有必填字段都已显式列出时，再移除 update 语法
   否则 clippy 可能刚清一条，编译立刻因新增必填字段失败。
22. 用脚本把多参 callsite 改成 `SomeFunc(SomeInput { ... })` 时，常见误伤不是字段值本身，而是尾部括号数：会生成 `}});` / `}})?;` 这类多一个 `}` 的闭合。批量改完后先全局搜：
   - `}});`
   - `}})?;`
   - `state_dir: ...` / `artifact_ledger: ...` 这类最后字段缺尾逗号
   再跑 `cargo check`。这比盯错误栈逐个修更快。
23. 当 `cargo clippy -D warnings` 已压缩到只剩极少数结构债时，超大 `main.rs` 的高收益最终顺序通常是：
   - 先清机械尾巴（`redundant_field_names`、残余测试旧调用、`nonminimal_bool`）
   - 再把 `large_enum_variant` 通过 `Box<...>` 收掉
   - 最后只留 1~2 个真正的 `too_many_arguments`（如 workflow snapshot / finalize backtest report）做 packet 化
   这样最稳，且便于在最后一次 clippy 验证里快速归零。

验证纪律：
- 每个批次至少跑：`cargo check`
- 进入 clippy 阶段后，反复跑：`cargo clippy --all-targets --all-features -- -D warnings`
- 若只做机械改写，应确保行为不变，不夹带重构

禁忌：
- 编译未绿就硬打 clippy
- 在机械 lint 批次混入业务逻辑改动
- 改函数签名后不立刻 sweep 全部 call site
- 只看单文件过滤结果就宣布 clippy 完成
