---
name: memos-memory-guide
description: Practical guide for using an external/shared memory system such as MemOS alongside the agent memory and session search.
---


# MemOS Memory Guide

Use this when the user references an external memory stack such as MemOS or wants cross-agent/shared recall beyond the agent built-in memory.

Principles:
- the agent built-in memory is best for compact durable facts about user preferences, environment, and conventions.
- the agent session_search is best for recalling prior work across past sessions.
- External systems like MemOS are useful for shared, local-first knowledge bases, SOPs, inboxes, and richer memory inspection outside the chat session.

When auto-recall is insufficient:
- Generate a short focused search query.
- Use the agent session_search first for past-session recall.
- If the workflow depends on a separate local knowledge base, inspect that system directly and summarize relevant findings.

Recommended workflow:
1. Use the agent memory for durable compact facts.
2. Use session_search when the user references earlier conversations or prior work.
3. Use external memory systems for larger knowledge bases, SOP storage, inbox capture, or multi-agent shared context.
4. Keep private and shared scopes distinct.

Operational guidance:
- Prefer short concrete search terms.
- Verify important hits before acting on them.
- Share only what is necessary across agents or systems.
- Treat local-first plain-text knowledge bases as inspectable source-of-truth artifacts.
