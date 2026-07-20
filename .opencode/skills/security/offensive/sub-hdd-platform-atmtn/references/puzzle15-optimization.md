Absorbed from skill: sub-hdd-puzzle15-userscript-optimization

This reference stores the game-specific optimization guidance for the sub.hdd.sb sliding-puzzle / puzzle15 userscript.

Key contents preserved:
- exact-vs-fallback search strategy by board size
- IDA* + beam/bidirectional fallback pattern
- heuristic composition guidance
- worker/main-thread synchronization concerns
- iframe debugging and CSS collision pitfalls
- API/local direction semantic mapping details
- 3x3 / 4x4 / 5x5 practical limits and tuning envelope

Original narrow optimization skill archived after consolidation.

--- PRESERVED HIGHLIGHTS ---

- 3x3 usually stays exact-search friendly.
- 4x4 may begin with exact search, then fall back to beam/bidirectional search.
- 5x5 in userscript context should prioritize executable approximate solutions over optimality claims.
- Embedded iframe page inspection is mandatory for many visual/debug issues.
- Avoid reusing site CSS class names like `.p15-board` for script-owned preview elements.
- API direction mapping often needs:
  up -> down
  down -> up
  left -> right
  right -> left
- Normalize active_session.board before use. It may be flat or 2D.
- Keep worker source synchronized with main-thread solver changes.
