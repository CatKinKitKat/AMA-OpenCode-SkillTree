---
name: model-fallback-router
description: Apply the user's preferred model/API fallback strategy when task execution may require provider rotation, retries, failover, or token-efficient routing.
---


# Model Fallback Router

Use this skill when model/provider choice matters.

Default routing policy:
1. Try GPT 5.4 first.
2. If that fails, degrades, stalls, rate-limits, or becomes uneconomical, try 4.6.
3. If that still fails, try 4.2.

API rotation rule:
- Do not burn through all GPT 5.4 capacity on a single API/provider first.
- Rotate across available APIs/providers progressively.
- Prefer one attempt per API/provider before repeatedly hitting the same one.
- Repeat on the same API only when there is a concrete reason, such as a transient timeout or the user explicitly asks.

Behavior:
- Use the cheapest reliable path that preserves output quality.
- Avoid long retry storms.
- Prefer deterministic completion over prestige routing.

Heuristics:
- Stay on GPT 5.4 when the task is high-stakes, ambiguous, or the first provider works normally.
- Fall back to 4.6 when GPT 5.4 is unavailable, repeatedly errors, or latency/rate limits make it inefficient.
- Fall back to 4.2 when both 5.4 and 4.6 are unavailable or the task is mostly executional, formatting, or lightweight transformation.

Retry discipline:
- Avoid more than one blind retry on the same API/provider/model combination.
- After one failed attempt, prefer provider rotation or model downgrade.
- If all practical paths are exhausted, report the blockage clearly instead of looping.

Compact internal rule:
5.4 -> 4.6 -> 4.2, rotating across APIs/providers, without exhausting one API's 5.4 first unless there is a specific reason.

Direct user instructions override this skill.
