---
name: systmt-dbggng
description: Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation — NO fixes without understanding the problem first.
version: 1.1.0
author: the agent (adapted from obra/superpowers)
license: MIT
metadata: 
tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
related_skills: [test-driven-dev, plans, subagent-driven-dev]
---


# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.: -

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess
- Create or update `DEBUG.md` immediately and keep the running evidence trail there

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] `DEBUG.md` started with observations and reproduction notes
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.: -

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim: read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?: -

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form Hypotheses Before Fixing

- List 3-5 plausible hypotheses before changing code
- For each hypothesis, record supporting evidence and conflicting evidence in `DEBUG.md`
- If one hypothesis has support and no conflicting evidence, test it first
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test one hypothesis
- One variable at a time
- Each experiment changes at most 5 lines
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more: -

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-dev` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work: Direction-Switch Rule

- **STOP.**
- If the same hypothesis direction failed twice, force a new hypothesis
- Return to observations and re-rank using the evidence in `DEBUG.md`
- **If ≥ 3 total fix attempts: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis: this is a wrong architecture.: -

## Red Flags: STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|: : : : |: : : : -|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|: : : -|: : : : : : : -|: : : : : : : : : |
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## the agent Integration

### Investigation Tools

Use these the agent tools during Phase 1:

- **`search_files`**: Find error strings, trace function calls, locate patterns
- **`read_file`**: Read source code with line numbers for precise analysis
- **`terminal`**: Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`**: Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systmt-dbggng skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-dev

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Tool-output redaction hazard during source inspection

Some tool surfaces may redact or mask source text when a line contains secret-like identifiers or values such as `token`, `auth`, `cookie`, or `session`.

Observed failure mode:
- a displayed source line can look syntactically impossible, for example showing `***` where the real code contains a harmless tuple/open paren/string list
- this can trick you into diagnosing a syntax error that does not actually exist
- `compileall`, import, or runtime evaluation may still succeed because the file on disk is valid

Safe pattern:
1. If a displayed line looks impossible, do not patch immediately.
2. Cross-check with one structural verification:
   - `python -m compileall ...`
   - direct import of the module
   - a tiny Python probe that reads the object/type/length instead of echoing the masked literal
3. Treat disagreements between displayed source and executable behavior as a redaction artifact first, not as proof the file is broken.
4. For Python repos, distinguish 3 layers before fixing:
   - parseability: `python -m compileall`
   - importability: direct `python -c 'import ...'`
   - test harness health: `python -m pytest`, `pytest`, `PYTHONPATH`, `pytest.ini` / `pyproject.toml` / `conftest.py`
5. Do not claim a test failure is a code regression until you separate code bugs from harness/env gaps.

## Large Rust repo drift / interrupted-session recovery

Use this addendum when a repo was green earlier in the session but later tool output shows old imports, missing fields, or vanished helper exports. This often means the working tree partially reverted, stash/pop restored stale files, or concurrent edits reintroduced older code.

### Recovery pattern that worked in ict-engine

1. Do not trust current assumptions. Re-read the exact files that fail to compile.
   - Especially entry surfaces like `src/main.rs`, `src/lib.rs`, `src/<module>/mod.rs`.
2. Before rollback or cherry-pick recovery, validate the supposed "good" baseline in an isolated worktree.
   - Use `git worktree add /tmp/<repo>-check-<sha> <sha>` and run at least `cargo check` there before resetting the main working tree.
   - If several candidate commits fail with the same surface mismatch, stop assuming there is a nearby green baseline.
   - Reclassify the problem as long-lived repository drift rather than a recent regression.
3. Distinguish 4 failure classes before patching:
   - entry-file drift: stale imports or old module paths
   - export-surface drift: helper exists but is no longer re-exported
   - call-site drift: function signature changed, old calls remain
   - initializer drift: a struct gained fields and one or more canonical constructors/builders/test literals still instantiate the older shape
3. Repair in this order:
   1. restore exports/re-exports
   2. restore imports/module paths
   3. repair struct initializers/builders/default constructors for newly added fields
   4. repair function signatures and all call sites
   5. only then rerun build/tests
4. For Rust structs used in persisted/state snapshots, when adding fields:
   - add the fields to the struct
   - update `Default`
   - update all explicit struct initializers in tests and snapshot builders
5. For status/JSON surfaces, if snapshot structs flatten fields rather than nesting sub-objects, do not reference imaginary nested fields. Read the actual struct and map to its real field names.
6. If you changed a function signature, search all call sites immediately and patch them in one pass before the next compile.
7. After recovery, run full verification, not only targeted tests:
   - `cargo fmt`
   - `cargo check`
   - targeted tests for the new feature
   - full `cargo test`
8. If the repo uses graphify, rebuild after code edits.
9. After restoring a green build, immediately sweep compiler warnings introduced or exposed by the drift repair.
   - In Rust, remove now-unused imports/helpers before declaring recovery complete.
   - Re-run `cargo check` after the warning cleanup, not only before it.

### Large-source snapshot hazard: do not rewrite a whole source file from truncated `read_file()` capture

A failure mode found live in ict-engine:
- a very large `src/main.rs` was inspected through `read_file()` / broad capture
- the returned content reflected only a partial/truncated view of the file
- writing that captured text back as if it were the full source silently corrupted the real file shape
- symptom looked like impossible line-count/offset mismatches and sudden parser errors in otherwise healthy code

Safe rule:
1. Before any full-file rewrite, compare the observed snapshot against reality:
   - if `read_file()` shows suspiciously small `total_lines` for a known-large file,
   - or offsets/results do not line up with earlier searches,
   - or file size and visible content scale do not match,
   treat the snapshot as partial and unsafe for rewrite.
2. Never use `execute_code`/`write_file` to overwrite a large source file from a `read_file()` capture unless you have verified the capture is complete.
3. For large Rust entry files, prefer:
   - narrow `read_file()` slices around exact anchors,
   - `patch` with small targeted hunks,
   - immediate `cargo check` after each small edit.
4. If a broad rewrite already happened and the repo was green before, revert the touched file to git baseline first, then resume with surgical patches.

Practical heuristic:
- `search_files` says a symbol exists at a huge line offset, but `read_file()` reports a much smaller total line count -> stop. Your current snapshot path is not trustworthy for full rewrite.

### Extra Rust lesson: signature-migration search must anchor on callee, not just trailing argument shape

When updating function signatures in a very large Rust file with many tests and helper calls:
- do not use broad `replace_all` on a trailing argument block alone
- similar call tails often appear in unrelated functions (`train_command`, `run_factor_backtest`, test helpers) and will be silently over-patched
- this creates fresh compile errors that look like more signature drift than actually exists

Safe pattern:
1. collect compiler error line numbers first
2. inspect each failing call site with narrow reads
3. patch only blocks that include the exact callee name
4. rerun compile after each batch

Heuristic:
- if a replacement pattern starts only from the last one or two arguments instead of the function name, it is too broad for a monolithic `main.rs`
- prefer search/patch anchored on `analyze_command(` or `WorkflowStatusCommandInput {` rather than `temp.path().to_str().unwrap(),` tails

### Small but common Rust drift subtype: extracted-module rename mismatch

When a function/struct was extracted out of `main.rs` or a monolith into a sibling module and later drift reintroduces the old path:
- check `src/<area>/mod.rs` for the real exported module name
- compare imports in `src/main.rs` / `src/lib.rs` against the actual file name
- fix the import path before chasing deeper errors

Example pattern:
- file exists as `technical_price_section.rs`
- `mod.rs` exports `pub mod technical_price_section;`
- stale caller still imports `analyze::technical_price::{...}`
- correct fix is the import path, not recreating the old module name

### Small but common Rust drift subtype: new struct fields added, builder left stale

If compile fails with `missing fields ... in initializer of <Struct>` right after a feature added persisted/status fields:
- find the canonical builder/constructor for that struct
- initialize the new fields there first, even with neutral defaults (`0`, `None`, empty map/vector) if the real population pass is not wired yet
- then search for explicit test literals / fixtures using the same struct and patch them

This is often the fastest path back to green because one stale builder can fan out into many misleading downstream errors.

### Specific reusable lesson from ict-engine timed-PDA integration

When extending a pipeline like pre-bayes/workflow status:
- add fields first to the persisted/state structs
- initialize new fields in every canonical constructor/builder, even if with neutral defaults
- restore missing imports/re-exports for any helper functions used by the new path before rerunning compile
- then populate them in canonical constructors and snapshot builders
- then route those fields into downstream evidence builders / status surfaces
- finally update tests and any manual struct literals that still instantiate the pre-change shape

If done in reverse, compile errors multiply and obscure the real source of drift.

### Extra Rust lesson: evidence-path mirroring

If one codepath already computes a derived summary (for example timed-PDA -> `entry_quality`) and another adjacent codepath still uses stale pre-summary evidence:
- do not patch only the display/status struct
- mirror the same derivation into the downstream evidence builder used by the alternate path
- add a regression test that asserts the derived evidence node value, not only that the extra fields are present

In ict-engine this meant:
- timed PDA summary fields had to be added to `PreBayesEvidenceFilter`
- factor-pipeline builders had to write those five fields
- `trade_evidence_from_pre_bayes_filter()` also had to derive `entry_quality` from those fields
- otherwise `bbn_support.pre_bayes_filter` looked correct while the actual BBN evidence path still ignored timed PDA

### Extra Rust lesson: adapter-input field additions must sweep constructors and tests, not just the builder body

When a Rust debug/report adapter gains a new input field:
- update the adapter input struct itself first
- then search every constructor/call site of that adapter input, including large `main.rs` command paths and inline tests there
- add a regression test that passes an explicit structured value and makes the fallback source intentionally conflicting, so precedence is proven rather than implied
- do not assume the upstream pipeline struct matches the final report/output struct. Build the test fixture from the real pipeline type, not from imagined report-only fields

Typical failure pattern:
- builder body starts reading `input.new_field`
- but `Adapt...Input` / call sites / embedded tests were not updated
- compile breaks in several places, and a hurried test may accidentally instantiate the output struct shape instead of the true upstream pipeline shape

Safe order:
1. add the field to the `Adapt...Input` struct
2. patch every constructor found by search
3. patch any inline `main.rs` tests using that adapter
4. write/repair the regression test against the real upstream type
5. run the focused test, then `cargo check`

### Extra Rust lesson: do not "fix reporting semantics" by washing out real gate state

When a user asks to make a debug/report surface use window-local semantics instead of full-series semantics:
- keep the original gate meaning intact unless the user explicitly asks to change the gate itself
- if the old helper mixes two responsibilities (for example history-quality gating + flatness diagnostics), split those responsibilities rather than forcing bad statuses back to `valid`
- never repair a misleading explanation by overwriting the underlying status to something stronger. That turns a reporting fix into a logic regression

Safe pattern:
1. identify which parts are true decision gates vs which parts are only diagnostics/explanations
2. preserve gate thresholds unless evidence says they were wrong
3. if window-local reporting is needed, compute a window-local report object directly instead of calling a series-level helper and then mutating its result back into shape
4. add or update a test that asserts both:
   - the window-local metadata fields (`aligned_length`, `primary_length`, `paired_length`)
   - the gate outcome still behaves correctly for flat / invalid / limited-overlap cases

### Extra Rust lesson: structured-field propagation is incomplete until the real runtime path carries it

If a report adapter now prefers a structured field over reparsing a string explanation:
- do not stop after adding the field to the adapter input and unit test
- trace the real runtime path from factor output -> pipeline struct -> command/report adapter -> final output
- add the structured field to the canonical upstream pipeline/state surface if that path currently drops it
- only keep explanation parsing as fallback for backward compatibility

Typical failure pattern:
- unit test proves `explicit_structured_value > explanation_fallback`
- but all production call sites still pass `None`
- runtime behavior still depends entirely on reparsing the explanation string

Safe pattern:
1. add the field to the upstream pipeline/report struct
2. populate it in the canonical builder path
3. thread it through real command/adaptor call sites
4. add one regression test for explicit adapter input precedence
5. add one regression test proving pipeline-carried structured data beats conflicting explanation text
6. rerun focused tests plus `cargo check`

### Extra Rust lesson: when introducing a canonical packet object, migrate by parallel surface first

If a monolith has a widely-read struct surface (for example `ExpansionBbnSupport.pre_bayes_filter`, `evidence_assignments`, `raw_*_trace`) and you want to replace it with a canonical nested packet object:
- do not delete or rename the old top-level fields in the first step
- first add the new packet object alongside the old fields
- make builders populate both from one canonical source
- migrate all readers/call sites to the packet in a dedicated pass
- only remove the old fields after the repo is green and searches show no remaining consumers

Reason:
- direct replacement explodes the dependency surface in large `main.rs`-heavy Rust repos
- compile errors fan out across status, report, tests, fixtures, and snapshot builders at once
- this obscures whether the new packet builder itself is correct

Safe order:
1. add packet type
2. add packet field alongside legacy fields
3. populate packet from one builder
4. migrate readers with search-driven sweep
5. remove duplicated legacy fields last
6. rerun `cargo check`, targeted tests, then full `cargo test`


From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
