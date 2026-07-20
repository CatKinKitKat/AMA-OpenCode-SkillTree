---
name: research-knowledge-ops
description: Use when doing research or knowledge-work from the agent: arXiv discovery, prediction-market data, wiki/markdown knowledge bases, Obsidian notes, or DSPy-style research/prototyping of LM programs.
version: 1.0.0
author: the agent
license: MIT
---


# Research and Knowledge Operations

Umbrella for research retrieval, knowledge-base work, and research-prototype loops.

## Academic and web research
- arXiv: search papers by keyword, author, category, or ID. Retrieve paper metadata and links. Use scripts/references when needing structured queries or domain notes.
- Polymarket: query public prediction-market data, prices, orderbooks, and history. Read-only and usually no auth.

## Knowledge bases and notes
- LLM Wiki: build/query interlinked markdown knowledge bases for compounding research context.
- Obsidian: filesystem-first vault operations: read, search, create, append, edit, wikilink.

## LM research/prototyping
- DSPy: declarative LM programs, prompt/RAG optimization, module and optimizer experiments.

## Workflow
1. Clarify the research question or knowledge operation.
2. Use the narrow subsection/tool best suited to the data source.
3. Save durable notes only when the user requested a knowledge-base update or the content is meant to persist.
4. For current facts, fetch live data and cite the source/tool output.

## Verification
- For papers/data: include identifiers, dates, URLs, or market slugs.
- For note edits: read back the changed file or returned object.
- For experiments: report exact command, metric, and output artifact.
