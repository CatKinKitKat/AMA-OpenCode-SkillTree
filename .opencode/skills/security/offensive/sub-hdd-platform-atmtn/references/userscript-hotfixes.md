Absorbed from skills: sub-hdd-puzzle-solver-hotfixes, sub-hdd-userscript-hotfixes

This reference stores detailed recurring bug patterns and patch points for local sub.hdd.sb Tampermonkey solvers.

Themes preserved:
- hub-entry / iframe panel lifecycle bugs
- duplicate panel creation and stale close-state handling
- difficulty mismatch and start-game routing bugs
- puzzle15 invalid-sequence and move-semantic mismatches
- memory solver session-resume and state-desync bugs
- 2048 oscillation, corner-exit, and late-game scoring fixes
- direct API-vs-CLI workflow corrections and verification steps

Original narrow hotfix skills archived after consolidation. Load umbrella skill `sub-hdd-platform-automation` for the class-level workflow.

--- PRESERVED HIGHLIGHTS ---

1. Puzzle15 invalid-sequence fixes
- reverse and OPPOSITE-map goal-side path before concatenation in bidirectional/beam reconstruction
- distinguish local blank-motion semantics from API tile-slide semantics
- keep raw solver sequence and apiSequence separate during debugging
- add preview logging for both semantic layers

2. Memory solver fixes
- separate knownCards, revealedIndices, matchedIndices
- ingest session.board on resume before autoplay
- preserve selectedDifficulty on fresh start but not on live-session takeover
- filter planner candidates by playability, not just remembered symbol matches

3. 2048 fixes
- small boards need stability-aware penalties, reverse-move penalties, and expectation over spawn samples
- classic 4x4 late-game losses often need stronger low-empty / corner-exit / fragile-spawn penalties

4. Hub-entry and panel runtime
- existing panels should be restored and rebound, not always rebuilt
- clear stale hidden/manual-close flags on recovery paths
- if actual board is in same-origin iframe, search that document too
- high z-index, explicit min-height, and visible status/log blocks improve observability

5. Validation discipline
- read local userscript first
- patch minimally
- run node --check on each edited userscript
- verify against real page/runtime behavior, not only static inspection
