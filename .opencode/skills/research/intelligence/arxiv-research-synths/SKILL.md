---
name: arxiv-research-synths
description: Gap-driven arXiv research: identify gaps in project docs, search arXiv API for papers, extract key sections via ar5iv HTML fallback, write structured synthesis md, convert best paper to Python. Trigger when user asks to 'find papers', 'research papers for X', '补强文档', or '搜论文并转成py'.
tags: [arxiv, research, paper, synthesis, gap-analysis]
---


# arxiv-research-synths

Research pipeline: project gap analysis → arXiv paper discovery → section extraction → synthesis md → paper2code.

## When to use
- User wants to strengthen project docs with external research
- User asks to search arXiv for papers on specific topics
- User wants "find papers and convert to code"
- Evaluating a project's theoretical foundations

## Pipeline

### Stage 1: Gap analysis

1. Read all project docs (README, architecture, plans, research notes)
2. Identify missing theoretical foundations, unvalidated assumptions, missing risk controls
3. Rank gaps by severity (critical / medium / low)
4. Output gap list with: gap description, why it matters, what kind of paper would fix it

### Stage 2: arXiv search

**Use arXiv API directly** (not web_search for arXiv: API is faster and structured):

```bash
curl -s "https://export.arxiv.org/api/query?search_query=id:{ARXIV_ID}" | grep -E '<id>http|<title>|<summary>'
```

**Search by topic** (use specific terms, avoid generic words):

```bash
# Good: specific, returns relevant results
curl -s "https://export.arxiv.org/api/query?search_query=all:ornstein-uhlenbeck+AND+all:microstructure&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"

# Bad: too generic, returns physics/astro noise
curl -s "https://export.arxiv.org/api/query?search_query=all:regime+OR+all:switching"
```

**Key rules**:
- Use `AND` (not `OR`) between terms for precision
- Search by exact arXiv ID when you already have a reference: `id:2602.19419`
- `cat:q-fin.TR` / `cat:q-fin.ST` / `cat:q-fin.MF` for finance-specific filtering
- `sortBy=submittedDate&sortOrder=descending` for latest papers
- If API search returns noise, switch to `id:` lookups from reference lists

**Multiple topic search**: run 3-5 API queries in parallel for different gap areas.

### Stage 3: Paper extraction (ar5iv fallback)

When `pip install pymupdf4llm` fails (common in sandboxed environments):

```bash
curl -sL "https://ar5iv.labs.arxiv.org/html/{ARXIV_ID}v{VERSION}" -o /tmp/{slug}.html
```

Then extract with Python html.parser (see paper2code skill for full TextExtractor class).

**Section map**: after extraction, scan for section titles and print line numbers:
```
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['abstract','introduction','method','experiment','result','conclusion']):
        if len(line) < 100:
            print(f"L{i}: {line}")
```

**Must-read sections for each paper**:
- Abstract + Intro → one-sentence contribution
- Method/Model → what to implement
- Experiment/Results → key numbers to cite
- Appendix → hidden implementation details

**Rate limiting**: ar5iv may throttle. Add 1-2s delay between fetches if hitting many papers.

### Stage 4: Synthesis writing

Write `docs/{project}-research-synthesis.md` with this structure:

```markdown
# Research Gaps & Paper Synthesis

> 评估日期：YYYY-MM-DD

## 一、文档已做到位的
(brief positive assessment)

## 二、核心不足（按影响排序）
### A. Gap title [severity]
- What's missing
- Why it matters
- Root cause

## 三、论文补强矩阵
### 3.1 Paper Title — relevance tag [relevance stars]
- arXiv ID + PDF link
- Core contribution (2-3 sentences)
- Direct application to project (specific modules/features)
- Actionable insights

## 四、发散性跨领域思路
(cross-domain inspirations from the papers)

## 五、论文 PDF 汇总
| # | 论文 | arXiv ID | PDF 链接 | 相关度 |

## 六、建议阅读顺序
1. Paper with highest relevance
2. ...

## 七、建议行动
### 立即可做（1-2 天）
### Sprint N 内做
### 远期做
```

### Stage 5: Paper2code conversion

For the **highest-relevance paper**, use the paper2code skill to convert to Python:

1. Write `contribution.md`: one-sentence summary, paper type, implementation scope
2. Write `ambiguity_audit.md`: specified vs unspecified items
3. Write `configs/base.yaml`: all hyperparameters with paper citations
4. Write core `src/*.py` modules: one module per paper concept
5. Write `REPRODUCTION_NOTES.md`: explain all unspecified choices
6. Test OU/statistics modules without torch (sandbox constraint)
7. Write `README.md` with ict-engine integration example

**Output directory**: `paper2code/{paper_slug}/`

### Stage 6: Integration bridge

For each paper implementation, write a bridge function showing how it maps to the project:

```python
def state_to_execution_features(state) -> dict:
    """Map paper's state vector to project's domain types."""
    return {
        "ou_theta": state.theta,
        "regime_laziness_score": state.theta * state.active_frac,
        ...
    }
```

## Key learnings from past runs

- **arXiv API `OR` operator is broken**: returns results from any field, not just specified ones. Always use `AND`.
- **ar5iv HTML has formula rendering issues**: but section structure is preserved. Good enough for contribution analysis and code skeleton.
- **Read specific line ranges, not full papers**: papers are 20-40 pages. Use the section map to read only what you need.
- **Python tests without torch**: if torch not installed, test statistics/estimation modules standalone. DDQN agent can be verified structurally (imports, shapes) without running training.
- **3 papers in parallel**: optimal batch size for research. More than 3 overwhelms context, fewer misses connections.
- **Multi-paper session (7 papers)**: feasible if you do: fetch all HTML → extract sections → read key sections → write all implementations → batch test. Don't interleave read-implement-read across papers.
- **Paper priority**: implement papers that are directly mappable to existing project modules first (e.g., OU estimator → existing `ou.rs`), then defensive/safety modules, then speculative/upgrade-path papers.
- **"Defensive" papers are high value**: papers describing system failures (Red Queen's Trap) produce safety modules that are immediately usable. They require less interpretation than novel-method papers.
- **arXiv search query patterns for finance**: `all:ornstein-uhlenbeck+AND+all:microstructure`, `all:ising+AND+all:financial+AND+cat:q-fin.ST`, `id:{EXACT_ID}` for known papers. Avoid broad terms like "regime" without finance qualifier: returns physics/astro noise.
- **Finance market-regime / strategy source scans**: when the user wants papers plus repos/forums/scripts for profitable factors, options, VRP, or market shape classification, use `references/finance-regime-strategy-source-scan.md` for source mix, query patterns, output shape, and validation gates.

## Stage 6: Architecture bridge (per paper)

For each paper implementation, write bridge functions showing how paper concepts map to project domain types:

```python
def state_to_execution_features(state) -> dict:
    """Map paper's state vector to project's domain types."""
    return {
        "ou_theta": state.theta,
        "regime_laziness_score": state.theta * state.active_frac,
        ...
    }
```

Pattern: each paper module should expose one `apply_to_ict_*()` or `state_to_*()` function that translates paper-specific types into the project's existing type system. This makes integration testable independently of the paper's full implementation.

## Stage 7: Batch test & summary

After all papers implemented, run all tests in one pass:
```bash
cd paper2code && for d in */; do python3 $d/src/*.py 2>&1 | tail -1; done
```

Then produce final summary table:
```
| 论文 | arXiv | 实现 | 行数 | 测试 | 核心迁移点 |
```

## Fallback: no arXiv access
If ar5iv and arXiv API both fail:
1. Use abstract page (arxiv.org/abs/{ID}) for contribution summary
2. Search for paper title on Google Scholar → "All versions" → find free PDF
3. Check SSRN for working paper versions
4. Ask user to provide PDF path
