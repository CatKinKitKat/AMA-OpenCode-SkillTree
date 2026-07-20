Absorbed from skill: sub-hdd-memory-solver-debugging

This reference stores the narrow but valuable memory-card solver debugging knowledge for sub.hdd.sb.

Key contents preserved:
- session-resume board ingestion
- index-level state modeling for known / revealed / matched cards
- planner filtering to prevent replaying blocked cards
- compact logging strategy for diagnosing loops and stale caches
- why this class of bug is state-desync, not puzzle theory difficulty

Original narrow debugging skill archived after consolidation.

--- PRESERVED HIGHLIGHTS ---

Core model:
- knownCards: long-term remembered symbols by index
- revealedIndices: currently face-up, temporarily unplayable
- matchedIndices: permanently consumed positions

Required behaviors:
- parse session.board on resume before autoplay
- remove matched cards from candidate structures at index level
- clear temporary revealed state after mismatch delay while retaining historical memory
- filter every planner path by current playability

Typical failure signatures:
- flip loop on same index
- 409 already matched
- 409 already revealed
- replay of stale known-pair candidates
