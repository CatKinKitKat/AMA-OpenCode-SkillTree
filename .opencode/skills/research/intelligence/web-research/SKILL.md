---
name: web-research
description: Search the web, scrape documentation, analyze competitor/OSS projects, and produce research briefs with sources. Use when gathering information for a new skill, validating a technology choice, or building a market map.
---
# Web Research

Systematic web research: query building, result triage, content extraction, and research brief production.

## When to Use

- [done] Gathering information for a new skill (benchmark against existing implementations)
- [done] Validating a technology or tool choice before adoption
- [done] Building a market map or competitor landscape
- [done] Finding CLI patterns or API examples for integration skills
- [done] Producing a research brief with verifiable sources

## Workflow

### 1. Query design

Build 3-5 focused queries instead of one broad query:
- "OpenCode SKILL.md structure site:github.com"
- "OpenCode skill template site:github.com"
- "OpenCode agent workflow site:github.com"

Rule: include the tool name + use case + platform for precision.

### 2. Triage results

Per result, assign:
- **Primary source**: official repo, official docs (preferred)
- **Secondary source**: community examples (valuate quality, check dates)
- **Discard**: vague blog posts with no code, outdated (prior to 2024)

### 3. Extraction

For each chosen source:
- URL + title + date
- Key patterns (file structure, frontmatter, trigger keywords, section order)
- Code snippets (verbatim, with attribution)
- Pros / cons vs our current approach

### 4. Synthesis

State concisely:
- What is the current canonical structure / pattern?
- What do we do differently / better?
- What will we adopt?

## Output: Research Brief

```markdown
# Research Brief - <topic>

## Query
...queries used...

## Findings

| Source | URL | Pattern found | Adopt? |
|--------|-----|---------------|--------|
| official | ... | ... | yes / no |

## Recommendation
...

## Open questions
...
```

## Voice

Citations first. No em-dashes. Tables over prose.
