---
name: paper-driven-plan-prompt
description: Create self-contained plan prompts that index papers and code repos without implementing anything
triggers:
---


# Paper-Driven Plan Prompt

## Purpose
Create self-contained "plan prompt" documents that index papers and code repos without implementing anything. These prompts are designed for other agents to execute.

## When to Use
- User asks for a "plan" about integrating external research into ict-engine
- User says "不要实现代码，只要plan prompt"
- User references `docs/plans/dna-sequence-inspired-pda-clustering-plan.md` as format template

## Format Template

```markdown
# [Topic] Plan

> [One-line summary with paper sources]

## 核心洞察
| 痛点 | 解法 | 映射 |
|------|------|------|

## 核心类比
| 概念 | 现状 | 目标 |

## [N]篇论文可吸收机制
### 1. [Paper/Repo Name] → [Mechanism]
**核心机制**: bullet points
**对 ict-engine 的价值**: bullet points
**可落点**: specific file paths
**代码索引**: repo URL + key files + line counts

## 公式索引
[actual formulas, not just names]

## 实施路径
### Phase 0: PoC (Python)
### Phase 1: Rust 实现
### Phase 2: 集成

## 约束
[numbered list of hard constraints]

## 对接映射
| 新模块 | 对接点 | 角色 |

## 成功标准
[phase-by-phase criteria]

## 参考文献
[numbered, with full URLs - arxiv/doi/github]
```

## Critical Rules
1. **NO CODE IMPLEMENTATION**: only reference paths to existing repos/files
2. **Paper links must be full URLs**: arxiv.org, doi.org, github.com
3. **Repo references need key file paths + line counts**: e.g. `hybrid_regime_infer.py` (1005行)
4. **Formulas must be included**: not just paper names, actual math
5. **Integration steps are conceptual**: not Rust code blocks

## User Correction Pattern
If user says "你不应该代码实现任何东西": you went too far. Clean up any created files and stick to indexing only.

## Output Location
`docs/plans/[topic]-plan.md`: not `docs/` root level.
