---
name: memory-skills-cleanup
description: >
tags:
---


## 触发条件

- 用户说记忆臃肿/太胖/需要减肥
- 用户说 skills 太多/磁盘满/清理
- MEMORY.md 或 user profile 接近容量上限
- skills 目录 >20M

## 四层清理流程

### 1. MEMORY.md（系统记忆）

路径：`~/.agent/memories/MEMORY.md`

规则：
- 只保留跨项目稳定技术事实（如 the agent 403 UA fix）
- 删除所有项目细节（ict-engine、arXiv paper ID 等）→ 属 repo docs / session_search
- 删除已过时的工作记录
- 文言压缩，每条 ≤30 字

### 2. User Profile（用户偏好）

路径：`memory(target='user')`

规则：
- 合并 10+ 散装条目为 1 条架构链
- 格式：树状依赖（`元→├─链→└─链`），非扁平列表
- 只存硬规则（红线、偏好、禁止项）
- 删除已变质的条目（如旧 cron 架构描述）
- 文言压缩

架构链模板：
```
元：[核心行为规则]
├─红线：[不可做]
├─重试：[失败策略]
├─[领域A]链：[约束→执行→验证]
└─[领域B]链：[约束→执行→验证]
```

### 3. Skills 目录

路径：`~/.agent/skills/`

清理步骤：
```bash
# 1. 查大小排序
du -sh ~/.agent/skills/* | sort -rh | head -20

# 2. 统计每个目录 skill 数
for d in ~/.agent/skills/*/; do
  count=$(find "$d" -name "SKILL.md" | wc -l)
  size=$(du -sh "$d" | cut -f1)
  echo "$count skills, $size: $(basename $d)"
done | sort -t, -k1 -rn

# 3. 识别可删除项
# - auto-installed 大包（>1M 且 >10 skills，从未手动加载）
# - cloned repos（含 .git 目录）
# - 空目录（0 skills）
# - 用户不会用的领域（gaming、leisure 等）

# 4. 删除
rm -rf ~/.agent/skills/CATEGORY/UNWANTED_PACK

# 5. 验证
du -sh ~/.agent/skills/
find ~/.agent/skills -name "SKILL.md" | wc -l
```

### 4. 路由引用清理

删除 skills 后必须清理引用，否则路由指向不存在的 skill。

文件：
- `~/.agent/agent-runtime/routing/skill-router.md`: 删除对应行
- `~/.agent/agent-runtime/routing/skill-index.md`: 删除对应 section + table rows
- `~/.agent/agent-runtime/routing/skill-index.json`: 删除对应 entries

方法：
```python
# skill-index.json 清理
import json
data = json.load(open('skill-index.json'))
# 过滤掉已删除的 category 和 skill name
data = [s for s in data if s.get('category') not in deleted_cats 
        and s.get('name') not in deleted_skills]
json.dump(data, open('skill-index.json', 'w'), indent=2)
```

验证：
```bash
grep -c "DELETED_SKILL_NAME" skill-router.md skill-index.md
# 期望：0
```

## Pitfalls

- **skill-index.json 是数组不是 dict**：顶层直接是 `[{skill}, ...]`，不是 `{"skills": [...]}`
- **sed 对多行 section 不可靠**：清理 skill-index.md 用 Python regex 而非 sed
- **删 skills 前先查路由引用**：确认哪些需要同步清理
- **MEMORY.md 和 user profile 是独立系统**：MEMORY.md 用 write_file，user profile 用 memory() tool
- **不要删用户手动创建的 skills**：只删 auto-installed / cloned repos
- **路由文件在 agent-runtime repo 里**：`~/.agent/agent-runtime/routing/`，不是 `~/.agent/routing/`
