---
name: lega-scri-thin-adap-brid
description: Wrap an existing standalone script or replay flow into a typed app adapter/orchestrator with minimal drift. Use when a repo already has working legacy automation that must be integrated into a new architecture without rewriting the old script first.
tags: 
version: 1
---


# lega-scri-thin-adap-brid

## When to use
Use when all are true:
- a legacy script already works well enough
- a new architecture now expects an interface/adapter/orchestrator
- user wants fast integration with low risk
- rewriting the old script would widen change surface too early

Typical triggers:
- "把旧脚本包进 adapter"
- "先接线，别重写"
- "thin wrapper"
- "legacy replay / browser flow 接入新 pipeline"

## Core rule
Do not rewrite the legacy script first.
First wrap it with a thin bridge that preserves old behavior and emits the new contract.

## Preferred integration order
1. Freeze the old script surface.
   - Identify the one callable entrypoint to reuse.
   - Treat its current return shape as external behavior.
2. Define the target contract.
   - List the exact fields the new adapter/orchestrator must return.
   - Keep key names stable even if some values are temporarily `None`.
3. Add one thin wrapper in the new architecture.
   - Example placement: `app/probes/`, `app/adapters/`, or `app/providers/`.
   - Wrapper should only:
     - call the legacy entrypoint
     - normalize result shape
     - apply narrow fallback semantics
     - avoid new business logic
4. Export the wrapper cleanly.
   - Add `__init__.py` export if the package uses explicit exports.
5. Verify with targeted tests before touching bootstrap/CLI wiring.
   - Monkeypatch the legacy entrypoint.
   - Assert contract keys and fallback behavior.
6. Run full tests after targeted tests pass.

## Change-surface discipline
Before coding, declare or update a change-surface artifact when the repo uses them.
Good minimal scope:
- docs/change-surface.md
- new thin wrapper file
- package export file
- targeted tests

Avoid touching in phase 1 unless required:
- legacy script internals
- database schema
- pipeline orchestration
- bootstrap/container wiring
- CLI flags

Those come in phase 2 after the bridge proves stable.

## Fallback pattern
When the legacy script does not fully satisfy the new contract yet:
- preserve required keys
- fill unknowns with `None`
- use the last trustworthy prior value from existing state only when explicitly safe
- keep status semantics honest

Example pattern:
- if new checkout URL exists -> set `status = "checkout_ready"`
- else -> fall back to existing persisted URL
- do not pretend the new flow succeeded if it only returned partial data

## Testing pattern
Use a narrow unit test around the wrapper first.
Good assertions:
- legacy entrypoint called with expected args
- normalized result contains every contract key
- fallback fields behave correctly on missing data
- no accidental dependency on live browser/network state

Then run:
- targeted test file
- full suite

## Reporting pattern
When done, report truthfully:
- legacy script untouched or touched
- wrapper path added
- contract keys stabilized
- targeted/full tests passed
- next safe integration step

## Anti-patterns
Do not:
- refactor the old script and the new adapter in one step
- widen scope into bootstrap/CLI/database before wrapper tests exist
- collapse old script semantics into a vague generic dict
- mark statuses as success when only fallback data exists
- change multiple layers just because the wrapper compiled

## Good outcome
A low-drift bridge that lets the new architecture call old automation now, while preserving freedom to replace the internals later.

## Proven pattern from use
In the windsurf auto-register repo, the safe first move was:
- keep `windsurf_trial_browser.py` unchanged
- add a `PaymentOrchestrator` thin wrapper under `app/probes/`
- normalize return keys to the new payment contract
- fall back to existing account checkout URL if browser flow returned none
- verify with a dedicated pytest file, then run full suite

This reduced risk and preserved momentum before bootstrap/CLI wiring.

## Additional proven pattern: phase-2 wiring after wrapper stabilizes
Once the thin wrapper tests pass, do container/CLI wiring as a separate phase.

Safe phase-2 order:
1. Add a backend selector in bootstrap/container, defaulting to stub.
2. Keep explicit dependency injection override higher priority than backend flags.
   - Example: `register_adapter` passed directly must win over `register_backend`.
3. Add only the minimum CLI flags needed to select the real backend and pass through stable parameters.
4. Add dedicated bootstrap/CLI tests for:
   - default stub backend
   - real backend selection
   - unknown backend rejection
   - explicit adapter override precedence
5. Run targeted tests first, then the full suite.

## Runtime-object reuse rule
When wrapping a large legacy script, prefer reusing its runtime classes/functions over importing its full CLI/config constructor surface.

Preferred order:
- reuse legacy runtime client classes/functions directly
- build a tiny compatibility config object in the new layer
- avoid depending on the legacy script's full argparse/AppConfig constructor unless field shapes are known stable

Reason:
- legacy CLI/config objects often drift faster than runtime call signatures
- thin wrappers should depend on the narrowest stable surface

## Config compatibility pattern
If the legacy runtime only needs attribute access, use a tiny compatibility object in the new layer instead of constructing the legacy dataclass wholesale.
Examples: `types.SimpleNamespace`, a small local dataclass, or a minimal config class.

Use this when:
- the legacy `AppConfig` constructor has many fields
- field names have already drifted from what the new layer guessed
- only a subset is actually needed by `WindsurfClient` or provider factory helpers

This avoids accidental coupling to unrelated legacy options while still letting the thin bridge call real runtime objects.

## Proven pattern from use: register replay bridge
In the same repo, the safe follow-up move was:
- keep `windsurf_auth_replay.py` unchanged
- add `WindsurfReplayRegisterAdapter` that creates a session, `WindsurfClient`, and mail provider at runtime
- delegate actual registration mapping to the narrower `WindsurfRpcRegisterAdapter`
- use a local compatibility config object rather than constructing legacy `AppConfig` directly after constructor drift was observed
- wire `stub` vs `windsurf_replay` selection in bootstrap/CLI only after adapter tests passed
- verify explicit adapter injection still overrides backend selection

This preserved low drift while allowing old replay logic to participate in the new architecture.