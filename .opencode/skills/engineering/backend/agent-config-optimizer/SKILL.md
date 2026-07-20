---
name: agent-config-optmzr
triggers: 
category: software-development
description: the agent配置优化 - 精简路由文件、添加中文触发词、压缩memory，减少token消耗
---


# the agent 配置优化

优化 the agent 配置以减少 token 消耗，提高中文触发效率。

## 优化流程

### 1. 备份当前配置
```bash
cp -r ~/.agent/routing ~/.agent/routing-backup-$(date +%Y%m%d-%H%M%S)
```

### 2. 路由文件整合

**检查重复**:
- `unified-index.md` 与 `skill-index.md` 通常重叠 30-40%
- 删除 `unified-index.md` 和 `unified-index.json`

**精简 skill-router.md**:
- 移除行号标记（如 `28|`, `29|`）
- 合并相似触发词
- 使用更紧凑的格式
- 目标：从 13KB+ 压缩到 6-8KB

**验证**:
```bash
ls -la ~/.agent/routing/*.md
du -sh ~/.agent/routing/*.md
```

### 3. 触发词中文化

**识别纯英文触发词**:
```python
# 找出只有英文触发词的 skill
import re
pattern = r'\|\s*`([^`]+)`\s*\|[^|]*\|[^|]*\|\s*([^|]+)\s*\|'
# 检查是否有中文字符
has_chinese = bool(re.search(r'[\u4e00-\u9fff]', triggers))
```

**添加中文等价词**:
- `findmy` → `查找设备, 定位, 找手机`
- `codex` → `代码生成, AI编程, 代码代理`
- `excalidraw` → `手绘图, 流程图, 白板`
- `github-auth` → `GitHub认证, gh登录, git凭据`

**三文件同步更新流程**（新增 skill 或给已有 skill 加中文触发词时）:

1. **skill-index.json**: 主数据源。用 Python 脚本批量更新 triggers 数组，去重排序后写回。
2. **skill-router.md**: 路由表。在对应分类段落中更新触发词列表。
3. **skill-index.md**: 表格索引。在对应分类表格中更新触发词列。

**批量添加中文触发词的完整流程**:

```python
import json

# 1. 读取 skill-index.json
with open('~/.agent/routing/skill-index.json', 'r') as f:
    skills = json.load(f)

# 2. 检查哪些 skills 没有中文触发词
no_chinese = []
for skill in skills:
    triggers = skill.get('triggers', [])
    has_cn = any(any('\u4e00' <= c <= '\u9fff' for c in t) for t in triggers)
    if not has_cn:
        no_chinese.append(skill['name'])

print(f"没有中文触发词的 skills ({len(no_chinese)}):")
for s in sorted(no_chinese):
    print(f"  - {s}")

# 3. 定义中文触发词映射
chinese_triggers = {
    'apple-notes': ['苹果备忘录', '备忘录', 'Apple备忘录', '笔记'],
    'apple-rmndrs': ['苹果提醒', '提醒事项', 'Apple提醒', '待办'],
    # ... 为每个 skill 添加
}

# 4. 批量更新
for skill in skills:
    if skill['name'] in chinese_triggers:
        existing_triggers = skill.get('triggers', [])
        new_triggers = chinese_triggers[skill['name']]
        all_triggers = list(set(existing_triggers + new_triggers))
        skill['triggers'] = sorted(all_triggers)

# 5. 写回
with open('~/.agent/routing/skill-index.json', 'w') as f:
    json.dump(skills, f, indent=2, ensure_ascii=False)
```

**关键陷阱**:
- skill-index.json 中 skill 名称必须精确匹配，先用脚本检查哪些 skill 存在，哪些缺失
- 缺失的 skill 需要先添加完整条目（name/category/grade/priority/security_review/supersedes/triggers/description）
- skill-index.md 表格行格式不统一（有些用 `|` 开头有些用 `||`），patch 时需带上足够上下文避免多匹配
- open-computer-use 等 MCP 类 skill 归入 `mcp` 分类，不是 `apple` 或 `red-teaming`
- 批量更新后需要同步更新 skill-router.md 和 skill-index.md
- 最后记得 commit 到 git repo

### 4. Compression 阈值与上下文窗口校准

**核心发现（2026-04-27）**：the agent 的 auto-compress 触发点看 `主模型 context_length × compression.threshold`，不是看 `auxiliary.compression.extra_body.context_window`。

**判定公式**：
- 触发阈值 = `max(int(model.context_length * compression.threshold), 64000)`
- 例：`model.context_length: 2000000` 且 `compression.threshold: 0.5` → 约 `1000000` tokens 才触发 compress

**正确改法**：
1. 先看 `compression.threshold`（默认常见为 `0.5`）
2. 再看主模型实际 context 来源：
   - `model.context_length`
   - 或 `custom_providers[].models[<exact model name>].context_length`
3. 若当前模型名带别名/后缀（如 `gpt-5.4(xhigh)`），`custom_providers.models` 必须写**完全同名**键；只写 `gpt-5.4` 不够稳
4. 自定义端点 `/models` 不准或缺失时，直接在 `model.context_length` 明写整数，避免 the agent 回退到错误默认值

**不要混淆**：
- `auxiliary.compression.extra_body.context_window`：只影响摘要模型请求体参数
- `auxiliary.compression.context_length`：只用于辅助压缩模型可行性检查/覆盖
- **真正决定何时 auto-compress 的仍是主模型 context_length**

### 5. Memory 压缩（架构链格式）

**核心发现（2026-04-24）**：扁平条目 → 架构链，一条树状依赖替代 10+ 散装条目。

**架构链模板**：
```
元：[核心行为规则]→[次级规则]→[三级规则]
├─红线：[不可做]
├─重试：[失败策略]
├─[领域A]链：[约束]→[执行]→[验证]
└─[领域B]链：[约束]→[执行]→[验证]
```

**实例**：
```
元：长忆从严→直做勿问→效驱>轮询→全量不挑。
├─红线：勿删cron/自动化，清前确认存废。
├─重试：始后败不重（断线除外），败即弃。
├─cron链：模型驱→禁脚本→deliver=feishu→冲突必解→sniper参数分离不与长驻争。
├─Hansa链：只收不挪(无FluxA权)→cron走MCP→状态机→答题agent推理。
└─Quest链：禁Twitter/X→禁视频→Medium/Dev.to/gist可。
```

**USER.md 优化**：
- 10+ 扁平条目 → 1 条架构链
- 文言压缩，每条 ≤20 字
- 只存硬规则，删除项目细节

**MEMORY.md 优化**：
- 只保留跨项目稳定技术事实
- 删除所有项目细节 → 属 repo docs / session_search
- 目标：< 500 bytes

### 5. Skills 清理

```bash
# 1. 查大小排序
du -sh ~/.agent/skills/* | sort -rh | head -20

# 2. 统计每个目录 skill 数
for d in ~/.agent/skills/*/; do
  count=$(find "$d" -name "SKILL.md" | wc -l)
  size=$(du -sh "$d" | cut -f1)
  echo "$count skills, $size: $(basename $d)"
done | sort -t, -k1 -rn
```

**删除标准**：
- auto-installed 大包（>1M 且 >10 skills，从未手动加载）
- cloned repos（含 .git 目录）
- 空目录（0 skills）
- 用户不会用的领域

**删前边界确认（2026-04-25 复盘）**：
- 先按“功能域”列 inventory，再删；不要把“有重复”误判成“都可删”。
- 像 OpenChronicle 这类工具，只能对标同功能域：时间线记忆 / 活动回放 / 会话检索 / 个人行为归档。
- 不得顺手删除跨域生产力技能（如 codex / opencode / the agent-code 之类编码代理），除非用户明确把该域也纳入清理范围。
- 用户说“杀功能库/冲突项”时，默认解释为：只删目标工具的同功能冲突项；不是全局去重大清洗。
- 破坏性删除前，先给出“将删清单 + 保留理由”；未确认范围时宁可只加路由，不做删除。

### 6. 路由引用清理（删 skills 后必须做）

**⚠️ skill-index.json 顶层是数组 `[{skill}, ...]`，不是 dict `{"skills": [...]}`**

**Python 清理（sed 对多行 section 不可靠）**：
```python
import json, re

# skill-index.json
data = json.load(open('skill-index.json'))
data = [s for s in data if s.get('category') not in deleted_cats
        and s.get('name') not in deleted_skills]
json.dump(data, open('skill-index.json', 'w'), indent=2)

# skill-index.md — 删除 section + table rows
content = open('skill-index.md').read()
for cat in deleted_cats:
    pattern = rf'## {re.escape(cat)}\n.*?(?=\n## |\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
for skill in deleted_skills:
    lines = content.split('\n')
    content = '\n'.join(l for l in lines if skill not in l)
open('skill-index.md', 'w').write(content)

# skill-router.md — 删除对应行
lines = open('skill-router.md').readlines()
lines = [l for l in lines if not any(s in l for s in deleted_skills)]
open('skill-router.md', 'w').writelines(lines)
```

**验证**：
```bash
grep -c "DELETED_SKILL" skill-router.md skill-index.md
# 期望：0
```

## 预期收益

| 优化项 | 优化前 | 优化后 | 节省 |
|: : : : |: : : : |: : : : |: : : |
| routing 文件 | 90KB+ | 50-60KB | 30-40% |
| skill-router.md | 13KB | 6-8KB | 50%+ |
| 英文触发词 | 30+ 个 | <15 个 | 50%+ |
| USER.md | 1900 bytes | 1200 bytes | 37% |

**Token 节省**: 每次对话约 2000-3000 tokens

## 验证步骤

1. 检查文件大小
2. 验证触发词匹配
3. 测试路由功能
4. 监控 token 使用量

## 风险与 Pitfalls

- 删除 unified-index.md 可能导致某些路由失效
- 添加的中文触发词可能不被用户使用
- 需要备份以便回滚
- **删 skills 后必须同步清理路由引用**（skill-router.md, skill-index.md, skill-index.json）
- **skill-index.json 是数组不是 dict**：顶层 `[{...}]`，不是 `{"skills": [...]}`
- **sed 对多行 section 不可靠**：清理 skill-index.md 用 Python regex
- **MEMORY.md 用 write_file，user profile 用 memory() tool**：两个独立系统
- **先以 repo/AGENTS 现状为准**：路由真实落点须现场查证；不要把 `~/.agent/agent-runtime/routing/`、`~/.agent/routing/`、项目内 `.agent/routing/` 之一当成永真。当前任务若已存在项目内 `.agent/routing/`，优先更新其正式文件，不得把正式路由先写去 `/tmp/*` 再停在那里。
- **memory replace 需要精确匹配 old_text**：多条目无法一次 replace，需逐条 remove 再 add 新条目
- **架构链格式优于扁平列表**：树状依赖关系比 10+ 散装条目更省 token 且逻辑更清晰
- **改 `config.yaml` 时先读精确上下文再 patch**：含 `api_key`、`base_url`、内联 map（如 `providers: {}`）的 YAML 很易因模糊匹配误伤相邻键；不要凭脱敏片段或记忆直接替换
