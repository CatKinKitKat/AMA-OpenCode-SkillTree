---
name: rust-modu-extr-mono
description: Extract structs and functions from a large Rust main.rs into dedicated module files without breaking compilation. Covers the analyze.rs vs analyze/mod.rs ambiguity pitfall and bottom-up dependency ordering.
---


# Rust Module Extraction from Monolith main.rs

## When to use
- Extracting structs/fns from a giant main.rs (or any monolith .rs) into submodule files
- Shrinking main.rs toward dispatch/orchestration only

## Steps

1. **Identify extraction candidates by dependency weight**
   - Search for struct/fn definitions still inline in main.rs
   - For each, grep which crate-internal types it references
   - Classify: "clean leaf" (only uses types already pub in lib) vs "heavy" (uses pipeline internals, private state)
   - Extract clean leaves first. Defer heavy ones

2. **Bottom-up ordering**
   - If struct A is nested inside struct B's fields, extract A first
   - Example: OptionsHedgingSection before TechnicalPriceSection (which embeds it)

3. **Create the new module file**
   - Place in the correct subdir (e.g., `src/analyze/price_action.rs`)
   - All extracted items must be `pub`
   - Import crate types via `crate::` paths (e.g., `crate::types::Candle`)
   - Use `use serde::Serialize;` etc. as needed: don't assume parent re-exports

4. **Register in mod.rs**
   - Add `pub mod new_module_name;` to the parent `mod.rs`

5. **CRITICAL PITFALL: analyze.rs vs analyze/mod.rs (E0761)**
   - If the module was originally a single file `src/analyze.rs` and you later created `src/analyze/mod.rs` to hold submodules, BOTH files cannot coexist
   - Rust error: `file for module found at both "src/analyze.rs" and "src/analyze/mod.rs"`
   - The old `src/analyze.rs` content should have been migrated into `src/analyze/mod.rs` (or split into submodules) and the flat file DELETED
   - This error may be HIDDEN by incremental compilation cache: the binary (`main.rs`) shows a confusing "unresolved import" while `cargo check --lib` passes fine
   - Fix: `rm src/analyze.rs` (after confirming mod.rs has its content), then `cargo clean` and rebuild
   - **Detection shortcut**: if `cargo check --lib` works but `cargo check --bin` fails with unresolved module, run `cargo clean` to surface the real E0761 error

6. **Wire imports in main.rs**
   - Replace inline struct/fn with `use crate_name::module::submodule::{StructName, fn_name};`
   - Delete the old inline code
   - Remove now-unused imports (compiler warns about these)


8. **Prefer wiring stable canonical subtrees before exporting more surface**
   - If `lib.rs` / crate exports start drifting while extracting, stop broadening the public surface.
   - Freeze already-stable canonical leaves/subtrees and wire them into real call sites first.
   - In `ict-engine`, this proved safer for `analyze/human_output`, `analyze/series`, and `analyze/multi_timeframe_parse` than continuing to widen exports around `AnalyzeMultiTimeframeInterval`.
   - Heuristic:
     - if the extracted module already compiles under `src/analyze/mod.rs`
     - and main.rs still contains duplicate logic
     - then replace the duplicate logic with imports from the stable subtree
     - and avoid new `lib.rs` export churn unless a consumer truly needs it

9. **Use compile errors as dependency-map hints during wiring**
   - After swapping main.rs to canonical modules, run `cargo fmt && cargo check` immediately.
   - Missing-type errors often reveal exactly which section structs still need importing from the new module files.
   - In this repo, wiring builder fns from canonical analyze modules required also importing sibling section structs such as:
     - `AnalyzeMultiTimeframeSection`
     - `TechnicalPriceSection`
     - `SmtCorrelationSection`
     - `OptionsHedgingSection`
   - Fix imports first. Only then remove now-unused legacy imports.

10. **When adding a human-readable surface, append before replacing**
   - If the repo already emits JSON reports used by tests/workflows, do not immediately replace that output with human text.
   - Safer pattern:
     - keep the canonical JSON `println!("{}", serde_json::to_string_pretty(&report)?);`
     - append a second human-readable rendering built from the canonical report object
   - This productizes the extracted human-output module without breaking downstream JSON consumers.
   - In `ict-engine`, a helper like `render_human_analyze_output(&report)` let `analyze` and `analyze-live` print the five-section human view after the JSON block.



12. **When rebuilding graphify from repo-local Python fails, report missing module exactly**
   - Project docs may require:
     - `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"`
   - In some environments this fails because the Python package is not importable even though project docs mention graphify.
   - Exact observed failure pattern:
     - `ModuleNotFoundError: No module named 'graphify'`
   - Do not claim graph rebuild succeeded if the import fails.
   - Finish other required verification (`cargo fmt`, `cargo check`, `cargo test`) and explicitly report the graphify rebuild failure verbatim so the user can fix environment/package wiring.

13. **For architecture refactors in drift-prone Rust monoliths, prefer parallel migration over hard replacement**
   - When introducing a new canonical object (for example a packet/bridge/core struct), do **not** immediately replace the old consumer-facing fields across the codebase.
   - Safer sequence that emerged in `ict-engine`:
     1. get the repo back to a green baseline first
     2. add the new canonical struct to stable shared types
     3. keep old fields/surfaces intact
     4. add the new canonical field as `Option<NewStruct>` or as an internal builder output alongside the old surface
     5. make the duplicated builders populate both old and new surfaces from one canonical builder
     6. only after all consumers migrate, delete the old fields
   - Reason: hard replacement in `main.rs` caused dozens of dependent call sites, tests, and report builders to break at once, obscuring the real migration path.
   - Heuristic:
     - if changing one field name on a central report struct would force many unrelated consumers to update immediately, stop and switch to additive migration
     - if the repo is already non-green, do not stack architectural replacement on top of existing compile drift
   - Phrase the work with positive constraints:
     - "keep old surface stable"
     - "populate new canonical packet in parallel"
     - "migrate consumers in batches"
     - "delete legacy surface only after green verification"

14. **When repeated module-extraction attempts fail, stop brute-forcing the headline module and extract dependency substrata first**
   - In `ict-engine`, trying to move large top-level clusters (`workflow`, then `factor_pipeline`, then full builder bodies) failed repeatedly because the visible target functions still depended on many `main.rs`-local helpers.
   - The robust sequence was:
     1. verify repo is green (`cargo fmt && cargo check && cargo test`)
     2. identify the repeated call-site duplication around the target surface
     3. extract adapter/re-export layers first into application modules
     4. extract pure helper substrata next (for example belief/pipeline shared helpers)
     5. only then attempt the real builder/body migration
   - Practical signs you are still too early to move the headline function:
     - new module compiles only if it references `crate::some_helper` where that helper exists only in `main.rs`
     - extraction succeeds only as a facade/re-export while the real implementation remains in `main.rs`
     - repeated retries keep restoring a green repo but do not reduce the true blocker list
   - In that situation, switch to a blocker-driven plan:
     - list the exact remaining local helpers
     - migrate the smallest pure subset first (math/normalization, trace builders, packet/debug adapters)
     - re-run full verification after every slice
   - `ict-engine` specific lesson:
     - moving `application/belief/shared.rs`, then a debug adapter layer, then `pipeline_shared.rs` reduced coupling safely
     - attempting to hard-move builder implementations before `infer_market_from_symbol`, `build_frame_features_for_market`, `pre_bayes_evidence_policy`, and `build_pre_bayes_evidence_filter` were lib-visible still failed
   - Rule of thumb:
     - a facade file is not proof of a real migration
     - only count the migration complete when the original `main.rs` function definitions are gone and search confirms that absence
   - Verification standard:
     - after each extraction slice, run `cargo fmt --all && cargo check && cargo test`
     - after a claimed hard move, also search the original file for the old `fn` definitions to confirm they were truly removed

14. **Do dependency-map discovery before extracting a giant `main.rs` cluster**
   - In `ict-engine`, an attempted first-slice extraction of the workflow/artifact cluster from `src/main.rs` looked locally contiguous but failed because the real dependency graph sprawled across analyze persistence, artifact diffs/decisions, lineage/trend helpers, prompt injection, and phase snapshot builders.
   - Key lesson: textual adjacency in a monolith is **not** a sufficient extraction boundary.
   - Before moving a large function family, first map:
     - direct callees inside the target span
     - helpers called outside the span
     - data types consumed from `state::*`
     - prompt/report builders that feed back into the same call path
   - Practical method:
     1. identify the intended seam from the main call site
     2. search for every callee used by that seam
     3. group the extraction candidate by dependency closure, not by nearby line numbers
     4. if the closure crosses multiple orchestration concerns, stop and pick an earlier / narrower seam
   - In this repo, `build_workflow_snapshot` was **not** the right first extraction slice even though it sat near related helpers.
   - Better-first heuristic for this style of monolith:
     - extract the cluster that already has a partial canonical surface nearby
     - e.g. `application/belief/*` adjacent factor-pipeline builders before workflow governance
   - Warning sign:
     - if a trial extraction requires creating a new module and then importing many unrelated main-local helpers, revert and choose a different slice rather than forcing a mega-move.

14. **When extracting duplicated names into sibling modules, avoid parent-level glob re-exports**
   - In `ict-engine`, `application::belief::debug_report` and `application::belief::pipeline_types` both defined `ExpansionLatestSignal`, `ExpansionProbabilitySupport`, and `ExpansionBbnSupport`.
   - A parent `mod.rs` with:
     - `pub use debug_report::*;`
     - `pub use pipeline_types::*;`
     created ambiguous glob re-exports and confused bin wiring during extraction.
   - Safer pattern:
     - keep sibling modules explicit
     - import concrete types from `debug_report::...` or `pipeline_types::...`
     - re-export only stable parent API surface, not every sibling symbol
   - Good `mod.rs` pattern:
     - re-export builder fns and top-level report structs explicitly
     - leave same-named helper types namespaced under their submodule
   - Example fix:
     - `pub use builder::{build_canonical_belief_report, build_canonical_belief_snapshot};`
     - `pub use debug_report::{build_factor_pipeline_debug_report, FactorPipelineDebugReport};`
     - `pub use pipeline_types::ExpansionFactorPipelineReport;`
   - Smell:
     - `cargo check` passes library but warns about ambiguous glob re-exports
     - main/bin imports need aliases like `AppExpansion...` / `DebugExpansion...`
     - tests start failing because one namespace silently changed while another stayed local

15. **When a struct family is split into two semantic surfaces, convert call sites by destination type, not by search-replace aliasing**
   - In `ict-engine`, one family of names served two different destinations:
     - `debug_report::Expansion*` for debug-report builder inputs
     - `pipeline_types::Expansion*` for persisted pipeline report fields
   - Naive aliasing in `main.rs` fixed compile errors in one path but broke tests and struct construction elsewhere.
   - Safer sequence:
     1. remove duplicate local structs from `main.rs`
     2. classify each call site by the destination field/function signature
     3. for builder-call inputs, use the debug-report namespaced types
     4. for stored struct fields, use fully qualified pipeline-types structs
     5. rerun `cargo check`, then `cargo test`, because test fixtures often still instantiate the old local type
   - Heuristic:
     - if one type name exists in two sibling modules, do not rely on a broad alias rename across the file
     - instead convert each usage based on the receiving API/field type
   - Practical shortcut:
     - use fully-qualified paths for the stored/canonical surface in fixtures and constructors to make the distinction visually obvious

16. **If the repo rejects a generated-orientation layer, remove both artifacts and workflow obligations**
   - In `ict-engine`, the user decided project-local `graphify` had no value.
   - Proper cleanup was not just deleting `graphify-out/`. It also required deleting the `AGENTS.md` section that mandated reading/rebuilding graphify artifacts.
   - Verification pattern:
     - remove `graphify-out/`
     - remove project instructions that require graphify use/rebuild
     - verify `test ! -e graphify-out`
     - verify no remaining project-local graphify obligations via search
   - This prevents future agents from resurrecting removed tooling because stale project instructions still mention it.

17. **When repeated extraction attempts fail, demote the target cluster and extract the shared substrate first**
   - In `ict-engine`, both of these seemingly natural "first slices" failed as direct extractions from `main.rs`:
     - workflow/artifact cluster
     - factor-pipeline builder cluster
   - Root cause was the same: the target cluster still depended on a web of `main.rs`-private helpers, types, and adapter functions.
   - Correct recovery pattern:
     1. try the intended slice once
     2. if compile errors reveal many private helper dependencies, stop forcing that slice
     3. identify the smallest reusable helper substrate shared by multiple future targets
     4. extract that substrate first into an application/library module
     5. keep the repo green after each failed experiment by reverting partial extraction attempts
   - Practical heuristic:
     - if the extraction candidate needs more than a few unrelated `main.rs` helpers imported into the new module, it is not yet the right slice
     - if multiple future slices depend on the same helper family, extract the helper family before any business cluster
   - In this repo, a workable first slice was a shared belief-helper substrate under `src/application/belief/shared.rs`, while direct workflow/factor-pipeline extraction was premature.

18. **Use re-export shims to preserve public API while relocating internal ownership**
   - After moving shared helpers in `ict-engine`, the cleanest low-drift pattern was:
     - move real implementation into a new canonical file
     - leave old sibling modules as tiny `pub use super::shared::{...};` shims
     - update parent `mod.rs` to declare the new module and export the intended stable API
   - This let the repo gain canonical ownership without forcing every downstream call site to change immediately.
   - Example pattern:
     - `shared.rs` owns the implementation
     - `builder.rs` becomes a re-export shim for canonical belief builders
     - `debug_report.rs` becomes a re-export shim for debug-report API/types
     - `mod.rs` declares `pub mod shared;` and re-exports the stable surface
   - Use this when:
     - the new module boundary is correct
     - but you want to avoid a broad call-site rewrite in the same commit
   - Verify with:
     1. `cargo fmt`
     2. `cargo check`
     3. `cargo test`

18b. **Do not create cyclical type ownership between sibling modules when deduping duplicated Rust structs**
   - In `ict-engine`, `pipeline_types.rs` was made to `pub use super::pipeline_shared::{ExpansionLatestSignal, ExpansionProbabilitySupport, ExpansionBbnSupport};` while `pipeline_shared.rs` still imported those same names from `pipeline_types.rs`.
   - This created an unresolved/circular ownership situation:
     - `pipeline_types` re-exported from `pipeline_shared`
     - `pipeline_shared` imported from `pipeline_types`
     - `cargo check` then failed with unresolved imports / private item import errors
   - Safe rule:
     - exactly one file owns the duplicated struct family
     - every other sibling only re-exports from that owner
     - the owner file must never import the same structs back through a sibling re-export
   - In this repo, the stable ownership was:
     - `pipeline_shared.rs` owns `ExpansionLatestSignal`, `ExpansionProbabilitySupport`, `ExpansionBbnSupport`
     - `pipeline_types.rs` owns only `ExpansionFactorPipelineReport`
     - `debug_report.rs` re-exports the debug/report-facing surface from `pipeline_shared.rs`
   - Practical migration order:
     1. pick canonical owner for the shared struct family
     2. move struct definitions there
     3. update all builder/internal imports to reference the owner directly
     4. only then add re-export shims in sibling modules
     5. run `cargo check`
     6. run `cargo test`
   - Smell:
     - unresolved imports appear immediately after replacing local definitions with `pub use ...`
     - compiler mentions private unresolved item import or suggests importing through another re-export
   - Fix:
     - break the cycle by changing the owner module to use local definitions directly, not sibling re-exports

18c. **After a type dedupe, test fixtures may need state-type imports that were previously leaked through local duplicates**
   - In `ict-engine`, removing duplicate local `ExpansionBbnSupport` ownership exposed test code in `main.rs` that instantiated `FactorPipelineLabelSource` without importing it.
   - Before dedupe, that dependency was easy to miss because nearby local structs visually carried the fields.
   - Safe check after moving a shared struct family:
     1. run `cargo check`
     2. run `cargo test`
     3. inspect test fixtures that manually construct the moved structs
     4. add explicit imports for embedded state/domain types such as `ict_engine::state::FactorPipelineLabelSource`
   - Heuristic:
     - if compile passes for lib but bin tests fail after a struct move, inspect fixture constructors before changing the moved structs again
   - This is often just missing fixture imports, not a bad extraction boundary.

19. **After the first shared shim works, split mixed-purpose `shared.rs` into purpose-named layers before larger extraction**

26. **When extracting a helper from `main.rs` that depends on monolith-local report structs, move logic behind a tiny trait instead of dragging those structs into the canonical module**
   - In `ict-engine`, `resolved_multi_timeframe_inputs_for_market` looked pure, but its parameter type was still a `main.rs`-local report struct family:
     - `MultiTimeframeCleanFuturesReport`
     - nested `CleanFuturesReport`
     - nested dataset structs
   - Directly moving the function into `application/multi_timeframe_inputs.rs` would have forced one of two bad moves:
     1. copy/paste those report structs into the module, creating ownership drift
     2. widen the extraction scope into a much larger report-struct migration than intended
   - Safer pattern:
     1. keep the canonical destination focused on the helper behavior
     2. define a tiny trait in the destination module that exposes only the data shape the helper actually needs
     3. implement that trait for the still-local `main.rs` report struct
     4. move the helper to operate on `T: Trait`
     5. rewire call sites, then delete the old local fn
   - Concrete shape that worked:
     - trait method returning an iterator of `(interval, output_path)` pairs
     - helper consumes the trait, not the report struct family
   - Why this is better:
     - reduces blast radius
     - avoids promoting temporary/report-only structs to canonical ownership prematurely
     - preserves monolith shrink progress without forcing a big data-model migration
   - Common pitfall:
     - the trait method may need the same explicit lifetime on both `&self` and other borrowed inputs (for example `market: &'a str`) if the iterator closure captures them together
     - if `cargo check` reports `lifetime may not live long enough`, align the trait method parameter lifetime with the returned iterator lifetime
   - Verification standard:
     - `cargo fmt --all && cargo check`
     - confirm the original helper body is gone from `main.rs`

   - In `ict-engine`, the first workable move was a broad `application/belief/shared.rs` that temporarily held:
     - canonical belief builders
     - debug-report structs/builders
     - pipeline/debug adapter logic
   - That was a useful intermediate state, but not the final architecture.
   - Better follow-up pattern:
     1. get a green repo with the first shared shim
     2. identify the stable sub-surface that is really shared by one concern cluster
     3. move that sub-surface into a purpose-named module
     4. leave existing entry modules as thin re-export shims
   - In this repo, the next refinement was:
     - create `application/belief/pipeline_shared.rs`
     - move pipeline/debug helper logic there
     - keep `builder.rs` and `debug_report.rs` as re-export surfaces
     - let `shared.rs` become thinner instead of growing into a junk drawer
   - Heuristic:
     - if a new `shared.rs` starts accumulating unrelated responsibilities, freeze and split it before attempting the next big business-cluster extraction
     - name the second-layer module after the concern (`pipeline_shared`, `workflow_shared`, etc.), not after a generic reuse concept
   - Benefit:
     - keeps the repo green while converging toward canonical ownership
     - reduces future extraction confusion because helpers are grouped by purpose instead of by "misc shared"

20. **When moving a real function out of `main.rs`, migrate its local helper closure too: or decouple it first**
   - In `ict-engine`, moving `build_pre_bayes_evidence_filter` into `src/config.rs` still failed at first because it secretly depended on a sibling helper, `pre_bayes_distribution`, that remained defined only in `main.rs`.
   - The safe checklist for a claimed "real move" is:
     1. search for the target fn body in `main.rs`
     2. inspect every non-stdlib helper it calls
     3. classify each helper as:
        - already lib-visible
        - must move together
        - must be replaced by a new module-local helper
     4. only then delete the old `main.rs` body
   - Do not assume compile errors will name the full dependency closure up front. The first removed function often exposes a second hidden local helper on the next `cargo check`.
   - Practical sign:
     - after the move, lib compilation fails with `cannot find function ... in the crate root` or similar visibility errors from the new module.
   - Fix pattern:
     - move the small helper into the same destination module if it is only used by the extracted function
     - update internal calls to plain module-local invocation rather than `crate::...` if the helper is not part of the crate root API
   - In this case, `pre_bayes_distribution` belonged with the extracted pre-Bayes filter logic inside `config.rs`.

21. **When a monolith slice has been successfully re-extracted once, a later emergency `git checkout -- file` revert can silently reintroduce the old duplicates. Re-audit from live files, not from memory**
   - In `ict-engine`, a full-file revert used to recover from an unrelated truncation/dirty-state problem restored old `main.rs` implementations that had already been migrated earlier:
     - `left_pad`
     - `infer_market_from_symbol`
     - `pre_bayes_evidence_policy`
     - `pre_bayes_distribution`
     - `pre_bayes_market_policy_override`
     - `build_pre_bayes_evidence_filter`
   - The dangerous trap is assuming the repo still contains the previously completed extraction just because the conversation remembers it.
   - Safe recovery sequence after any broad revert:
     1. re-read the destination module and `main.rs`
     2. search for the old `fn` definitions in `main.rs`
     3. confirm which migrations survived and which were rolled back
     4. resume with the *smallest* previously proven-safe slice, one function at a time
   - Practical heuristic:
     - after `git checkout -- src/main.rs` or any whole-file restore, treat all prior extractions touching that file as untrusted until verified by search
     - conversation history is not proof of repository state
   - In this repo, the stable recovery path was:
     - re-establish green baseline
     - re-move `left_pad`
     - re-move `infer_market_from_symbol`
     - re-move `pre_bayes_evidence_policy`
     - re-move `pre_bayes_distribution`
     - re-move `pre_bayes_market_policy_override`
     - re-move `build_pre_bayes_evidence_filter`
     - then re-move `FrameFeatures` / `INDICATOR_PERIOD` / `build_frame_features`
     - then re-move `build_frame_features_for_market`
   - Benefit:
     - avoids mixing recovery from state drift with fresh large-slice extraction
     - each re-applied step is independently validated with `cargo fmt && cargo check` (and targeted tests where available)

22. **When doing scripted block deletion in a huge Rust file, anchor on both start and end targets and immediately verify collateral loss**
   - In `ict-engine`, a scripted deletion that removed the old pre-Bayes block from `main.rs` also erased the adjacent `build_frame_features_for_market` function because the removal span was anchored too broadly.
   - For giant monolith edits, use this discipline:
     1. identify exact start marker for the first function to delete
     2. identify exact end marker for the next function that must remain
     3. after script/edit runs, search for adjacent keeper fns that should still exist
     4. run `cargo check` immediately. Missing adjacent helpers often surface faster than re-reading the whole file
   - Heuristic:
     - if using a script or broad text replace on a 10k+ line file, assume collateral deletion is possible
     - verify both:
       - removed target definitions are gone
       - neighboring required definitions still exist
   - Recovery pattern:
     - restore the missing neighbor function first
     - then rerun fmt/check/tests before declaring the extraction stable
   - In this case, `build_frame_features_for_market` had to be restored after the scripted deletion removed more than intended.

22. **If a nearby function cannot move cleanly because its core type still belongs to `main.rs`, use a temporary policy/helper extraction instead of forcing the full builder move**
   - In `ict-engine`, the next drift target after pre-Bayes was `build_frame_features_for_market`.
   - A full move was initially blocked because the function mutates `FrameFeatures`, and that struct still lived privately in `main.rs` alongside `build_frame_features`.
   - The low-drift intermediate pattern was:
     1. keep the thin wrapper fn in `main.rs`
     2. extract only the market-specific override policy into a lib module (`config.rs` in this case)
     3. have the wrapper compute/own `FrameFeatures`, clone the mutable labels, call the extracted helper, then write the labels back
     4. verify with `cargo fmt && cargo check`
   - This is not a "true move" of the wrapper, but it is still useful drift reduction because the branchy market policy leaves `main.rs`.
   - Rule of thumb:
     - if the function's main burden is policy logic and its remaining shell only adapts a local/private type, extract the policy first
     - defer the real move until the underlying struct and base builder are also ready to migrate
   - Naming guidance:
     - alias the extracted helper at import site to make the temporary layering explicit, e.g. `build_frame_features_for_market as apply_market_frame_overrides`
     - this reduces confusion while both a wrapper and a helper temporarily share similar names
   - Verification standard:
     - do not claim the original function is gone if a wrapper remains
     - instead report honestly: logic moved, thin wrapper remains, full migration requires moving the owning type next

23. **When a rollback wipes out prior successful micro-migrations, re-run the sequence as strict one-function slices and re-check live file state before every patch**
   - In `ict-engine`, a broad `git checkout -- main.rs config.rs` restored green state but also silently erased several already-successful extractions (`left_pad`, pre-Bayes helpers, frame helpers, trace helpers).
   - The robust recovery pattern was:
     1. re-read the live files first instead of assuming prior moves still exist
     2. search for exact remaining `fn ...` definitions in `main.rs`
     3. re-apply migrations in the smallest possible slices, one function at a time
     4. after each slice, run `cargo fmt && cargo check` and at least one focused regression test
   - Practical lesson:
     - after any full-file rollback, your earlier session memory is not source of truth. The repo is
     - always inspect current file contents before writing the next patch, even if you "just did" that migration earlier
   - Good micro-order from this run:
     - `left_pad`
     - `infer_market_from_symbol`
     - `pre_bayes_evidence_policy`
     - `pre_bayes_distribution`
     - `pre_bayes_market_policy_override`
     - `build_pre_bayes_evidence_filter`
     - `build_frame_features`
     - `build_frame_features_for_market`
     - trace helpers
     - `multi_timeframe_entry_quality_bias`
   - Why this worked:
     - each step had tiny blast radius
     - failures were attributable to the current slice, not hidden collateral from previous large edits
     - repeated verification kept the monolith green while shrinking it
   - Rule:
     - if a previous rollback or file truncation occurred, stop doing batch migrations. Switch to one-definition-at-a-time extraction until stability returns

24. **Patch tools may report false-positive lint noise after import-list edits. Trust live `cargo fmt && cargo check` over patch-tool diff formatting complaints**
   - In `ict-engine`, small import edits often came back with patch-tool lint output showing wrapped/reflowed import groups as if they were errors.
   - These were not semantic compile problems. The authoritative check remained `cargo fmt && cargo check`.
   - Use this discipline:
     1. apply the small textual patch
     2. ignore cosmetic import reflow warnings from the patch tool unless they indicate true parser failure
     3. immediately run `cargo fmt && cargo check`
     4. only treat the change as bad if the Rust toolchain rejects it
   - Especially common triggers:
     - removing a single symbol from a long `use ...::{...}` line
     - adding one more imported item that forces rustfmt to wrap the group
   - Rule of thumb:
     - patch-tool unified diff formatting complaints are advisory
     - Rust compiler + rustfmt are the real gate for extraction work

25. **When moving a helper that depends on a tiny local utility, inline the normalization locally if the dependency is otherwise not worth extracting yet**
   - In `ict-engine`, `multi_timeframe_entry_quality_bias` depended on `normalize_distribution(&mut bias)` which still lived in `main.rs`.
   - Instead of turning that into a blocker or widening the migration scope, the safe move was to inline the tiny normalization logic inside the migrated helper:
     - compute sum
     - divide by sum when non-zero
     - otherwise assign uniform weights
   - This preserved behavior while avoiding a premature extra extraction.
   - Rule:
     - if the only blocker is a tiny pure helper with obvious local behavior, consider inlining it into the new canonical module rather than expanding the migration surface
   - Prefer this only when:
     - the helper is short
     - semantics are obvious
     - duplication cost is lower than pulling another dependency chain across module boundaries
   - Verify with a focused unit test covering the moved helper's behavior.
23. **When a rollback is required mid-extraction, immediately re-scan live files before continuing: prior migration state may be gone**
   - In `ict-engine`, a broad `git checkout -- main.rs config.rs` used to recover a green repo also erased several already-completed extractions (`left_pad`, `infer_market_from_symbol`, `pre_bayes_evidence_policy`, `pre_bayes_distribution`, `pre_bayes_market_policy_override`, `build_pre_bayes_evidence_filter`, `build_frame_features`, `build_frame_features_for_market`, and trace helpers).
   - After any rollback or restore command:
     1. re-read the destination module and `main.rs`
     2. search for the exact `fn` definitions again
     3. treat the repo as a new baseline, not as if previous migration progress still exists
   - Do not stack new deletions/import rewires on top of remembered state. That caused duplicate imports, missing helpers, and confused retry sequences.
   - Practical rule:
     - after a rollback, the next step is always `search_files/read_file`, never assumption-based patching.

24. **For drift-prone monolith extraction, use a repeated 'single-function migration loop' instead of batch moves**
   - The stable loop that worked in `ict-engine` was:
     1. pick exactly one function/helper
     2. copy it to the target lib module with minimal imports
     3. rewire one import/use site in `main.rs`
     4. delete only that one original definition
     5. run `cargo fmt && cargo check`
     6. if relevant, run 1-3 focused tests
   - This succeeded repeatedly for:
     - `left_pad`
     - `infer_market_from_symbol`
     - `pre_bayes_evidence_policy`
     - `pre_bayes_distribution`
     - `pre_bayes_market_policy_override`
     - `build_pre_bayes_evidence_filter`
     - `build_frame_features`
     - `build_frame_features_for_market`
     - `raw_market_regime_trace`
     - `raw_liquidity_context_trace`
     - `raw_multi_timeframe_resonance_trace`
   - Heuristic:
     - if a migration candidate is larger than one function plus trivial import cleanup, split it again
     - prefer many green micro-moves over one ambitious cluster move
   - Benefit:
     - failures stay local
     - rollbacks cost less
     - the user gets truthful incremental progress without hidden drift

- **Visibility**: extracted structs need `pub` on both the struct and its fields if main.rs was constructing them directly. If fields were private (no `pub`), the builder fn must live in the same module.

   - Safer recovery rule:
     1. before any broad checkout/reset, note exactly which migrations already landed successfully
     2. prefer reverting only the latest target files or blocks, not the entire working tree slice, when earlier migrations are known-good
     3. after any broad rollback, assume earlier successful extractions may have been undone and re-audit current file state before continuing
   - Robust re-application pattern for a monolith shrink task:
     1. re-read the destination module and source monolith fresh after rollback
     2. search for the exact current inline definitions still present
     3. re-apply extractions one function at a time in ascending-risk order
     4. after each function, run `cargo fmt && cargo check` plus one focused regression test
   - Practical safe order discovered here:
     - `left_pad`
     - `infer_market_from_symbol`
     - `pre_bayes_evidence_policy`
     - `pre_bayes_distribution`
     - only then consider heavier functions like `pre_bayes_market_policy_override`, `build_pre_bayes_evidence_filter`, `build_frame_features`, and wrappers
   - Heuristic:
     - move the smallest pure helpers first
     - move already-lib-owned equivalents before policy-heavy builders
     - avoid touching trace helpers or multi-function clusters until the small helper ladder is re-established and green
   - Reporting rule:
     - after a destructive rollback, explicitly tell the user that prior true moves were reverted and that the task is restarting from current file reality, not prior chat history.

23. **In drift-heavy monolith extraction, if you must revert to recover green, assume every prior "moved" helper may have been silently undone and re-audit from live files before the next slice**
   - In `ict-engine`, a broad `git checkout -- src/main.rs src/config.rs` was the correct recovery after half-finished trace-helper extraction destabilized the repo.
   - But that reset also silently erased earlier successful mini-migrations (`left_pad`, `build_frame_features`, pre-Bayes helpers, promoted types/constants) because they were not yet committed separately.
   - The practical lesson:
     1. after any full-file rollback, do **not** trust conversational state or your own prior summary
     2. re-read the live destination/source files
     3. search for the exact `fn` definitions and imports you believe were moved
     4. only then pick the next slice
   - Good recovery checklist after a rollback:
     - `read_file` destination module to see what actually remains
     - `search_files` for the old `fn ...` definitions in `main.rs`
     - treat the current tree as ground truth, not prior chat memory
   - Strategy consequence:
     - when rollback risk is high, reduce extraction to one truly minimal helper per step (e.g. `left_pad` alone), verify, then proceed
     - avoid stacking several successful-but-uncommitted migrations in working tree state and then doing a broad file reset
   - Reporting rule:
     - if a rollback erased prior progress, say so explicitly. Do not pretend later steps are building on state that no longer exists.

24. **After a rollback, prefer re-entry through the smallest already-proven slice instead of resuming the ambitious target that triggered the reset**
   - In `ict-engine`, after reverting `main.rs` and `config.rs` to restore green, the correct re-entry was not "continue the trace-helper migration".
   - The stable re-entry path was:
     1. confirm green repo (`cargo fmt && cargo check`)
     2. re-audit actual file contents
     3. restart from the smallest safe helper (`left_pad`)
     4. re-verify
     5. only then consider the next slice (e.g. `infer_market_from_symbol`)
   - Heuristic:
     - if the previous attempt ended in a broad rollback, your next move should shrink scope, not match the prior scope
     - choose the smallest extraction that has low dependency surface and clear verification value
   - Benefit:
     - this re-establishes momentum while reducing the chance of another destabilizing revert cycle.

23. **When a rollback restores a monolith file, immediately reapply only the already-validated extractions in dependency order**
   - In `ict-engine`, recovering `src/main.rs` with `git checkout -- src/main.rs` fixed file corruption but also restored many previously removed inline helpers.
   - Blindly replaying the whole migration script reintroduced duplicate definitions and compile failures.
   - Safer recovery sequence:
     1. restore the corrupted file to a green baseline
     2. compare current `main.rs` against already-canonical lib surfaces
     3. reapply only the proven moves, in dependency order
     4. after each reapplication, run `cargo fmt && cargo check`
   - For this repo, the stable reapply order was:
     1. import canonical `config::{build_frame_features, build_pre_bayes_evidence_filter, left_pad, FrameFeatures, INDICATOR_PERIOD}`
     2. remove local `FrameFeatures` / `INDICATOR_PERIOD` / `build_frame_features`
     3. keep `build_frame_features_for_market` as a thin wrapper using the extracted override helper
     4. remove duplicated local pre-Bayes helpers only after canonical imports are present
     5. restore `application::belief::pre_bayes_evidence_policy` import if local policy builder was removed, but do **not** import `infer_market_from_symbol` if its local version still intentionally remains
   - Key lesson:
     - a rollback changes the dependency picture. Re-run discovery before editing
     - do not assume an earlier patch sequence is still safe after restore
   - Practical smell:
     - compile errors like `name X is defined multiple times` after rollback usually mean canonical imports and restored local defs now coexist
     - `cannot find function X in this scope` often means you removed the local def but forgot to restore the canonical import
   - Verification standard:
     - after rollback recovery, search for duplicate `fn` definitions for every migrated helper
     - then run targeted tests covering the migrated slice before moving on
23. **For staged Rust monolith shrinkage, migrate ownership prerequisites before the real builder body**
   - In `ict-engine`, a stable path emerged before attempting the true move of `build_frame_features`:
     1. first move the owning struct (`FrameFeatures`) out of `main.rs` into a lib-visible module
     2. then move related constants/utilities used by both the old and future call sites (`INDICATOR_PERIOD`, then `left_pad`)
     3. only after those ownership prerequisites are green should the real builder body be extracted
   - This avoids a common failure mode where the target function is nominally the next seam, but its value type, constants, and tiny helpers still anchor it to `main.rs`.
   - Practical heuristic:
     - if a function still depends on a private struct plus one or two local helpers/constants, do not extract the function first
     - instead promote the type ownership and tiny shared utilities in separate green commits
   - Benefits seen here:
     - each slice stayed verifiable with `cargo fmt && cargo check`
     - targeted tests for adjacent behavior (`build_frame_features_for_market`, pre-Bayes) still passed while ownership moved underneath
     - the next real extraction became mechanically simpler because imports already pointed at the canonical module
   - Reporting rule:
     - when only prerequisites moved, state that clearly. Do not over-claim the main function as migrated yet.

24. **For drift-prone Rust main.rs cleanup, use a leaf-helper ladder and verify after every single helper move**
   - In `ict-engine`, the most reliable recovery after rollback and partial corruption was not another large extraction. It was a strict smallest-first ladder.
   - The stable order proved to be:
     1. move `left_pad`
     2. move `infer_market_from_symbol`
     3. move `pre_bayes_evidence_policy`
     4. move `pre_bayes_distribution`
     5. move `pre_bayes_market_policy_override`
     6. move `build_pre_bayes_evidence_filter`
     7. move `FrameFeatures`
     8. move `INDICATOR_PERIOD`
     9. move `build_frame_features`
     10. move `build_frame_features_for_market`
     11. move `raw_market_regime_trace`
     12. move `raw_liquidity_context_trace`
     13. move `raw_multi_timeframe_resonance_trace`
     14. move `multi_timeframe_entry_quality_bias`
   - Only after each slice passed `cargo fmt && cargo check` plus at least one focused regression test did the next slice proceed.
   - Why this works:
     - each helper has an obvious destination and small dependency surface
     - later heavier builders become nearly mechanical once their supporting leaves are already canonical
     - if rollback happens, re-entry is obvious because the ladder can simply restart from the current live-file truth
   - Practical rule:
     - when several helpers in a monolith all look movable, do not jump to the biggest visible one
     - instead sort by: smallest body, fewest dependencies, already-existing canonical destination, lowest test blast radius
   - Verification pattern:
     - after every moved helper, run `cargo fmt && cargo check`
     - also run one nearby focused test, not only the full suite
     - before the next slice, search to confirm the old `fn ...` definition is truly gone from `main.rs`
   - Reporting rule:
     - describe each step as a single completed slice. Do not batch several unrelated helper moves into one claim unless they were actually verified together.

25. **Once a helper family is fully extracted, identify the next target as a same-domain cluster rather than jumping to a random large function**
   - After the pre-Bayes/frame/trace/multi-timeframe-bias chain was successfully removed from `main.rs` in `ict-engine`, the next low-coupling seam was not another isolated helper but the multi-timeframe input parsing cluster.
   - Good follow-up selection heuristic:
     - pick a cluster whose functions already sit together in `main.rs`
     - share one narrow purpose
     - mostly consume std/path/string data rather than broad trading state
   - In this repo, the next recommended cluster was:
     - `parse_cleaned_continuous_identity`
     - `auto_resolve_multi_timeframe_inputs`
     - `resolve_multi_timeframe_inputs`
     - `resolved_multi_timeframe_inputs_for_market`
     - `resolve_analyze_multi_timeframe_inputs`
     - `resolve_analyze_cli_inputs`
     - `detected_multi_timeframe_clean_root`
     - `is_multi_timeframe_clean_root`
   - Why this matters:
     - once a successful domain chain is done, continuing within that same local dependency neighborhood keeps token cost and regression risk low
     - it avoids the common mistake of switching to an unrelated huge orchestration function just because the previous cleanup succeeded
   - Rule:
     - after a green extraction run, spend one search pass to nominate the next same-domain low-coupling cluster before changing code again.

26. **When extracting a path/IO helper cluster, prefer extending the existing canonical domain module over creating another tiny sibling module**
   - In `ict-engine`, after moving the first multi-timeframe parsing helpers into `application/multi_timeframe_inputs.rs`, the next helpers in the same neighborhood were:
     - `resolved_multi_timeframe_inputs_for_market`
     - `resolve_analyze_cli_inputs`
     - `detected_multi_timeframe_clean_root`
     - `is_multi_timeframe_clean_root`
   - The low-drift move was to keep extending `application/multi_timeframe_inputs.rs` rather than inventing a new module for each tiny helper family.
   - Practical heuristic:
     - if the new helper still belongs to the same narrow domain surface already established by an application module
     - and its imports are std/path/result plus that module's existing types
     - append it to the existing canonical module
     - then rewire `main.rs` imports and delete the duplicate body
   - Benefits:
     - fewer module declarations / routing changes
     - clearer canonical ownership for one domain seam
     - easier repeated single-slice extraction loop
   - Verification pattern:
     - after each append-and-delete slice, run `cargo fmt --all && cargo check`
     - remove any now-unused imports immediately if the compiler warns

27. **Patch tools can duplicate a function header during repeated append-style edits. Re-read the destination file before trusting the patch result**
   - In `ict-engine`, appending `resolve_analyze_cli_inputs` plus adjacent helpers into `application/multi_timeframe_inputs.rs` produced an accidental duplicated function signature line:
     - `pub fn resolve_analyze_cli_inputs(` appeared twice in a row
   - The patch tool reported an unclosed delimiter, but the real cause was duplicate inserted text, not a logic problem.
   - Safe recovery pattern:
     1. if a patch introduces parser/unclosed-delimiter errors after a repeated replace/append
     2. immediately re-read the destination file around the edited span
     3. look for duplicated headers / duplicated context lines from the patch anchor
     4. delete only the accidental duplicate, then rerun `cargo fmt && cargo check`
   - Heuristic:
     - after a patch that targets text near a function signature already recently edited, suspect duplicate anchor insertion before suspecting deeper Rust syntax issues
   - Rule:
     - trust live file inspection plus compiler output over the patch tool's inferred cause label

- **Visibility**: extracted structs need `pub` on both the struct and its fields if main.rs was constructing them directly. If fields were private (no `pub`), the builder fn must live in the same module.
- **Serde derives**: `#[derive(Debug, Serialize)]` needs `use serde::Serialize;` in the new file: it won't inherit from main.rs.
- **Re-export gaps**: check if types like `AuxiliaryMarketEvidence` are actually re-exported from their parent mod.rs. If not, use full `crate::data::realtime::openalice::AuxiliaryMarketEvidence` path.
- **Incremental cache masking**: always `cargo clean` if you see contradictory errors between lib and bin targets.
- **Blank line lint**: after deleting blocks, collapse double blank lines to single.
