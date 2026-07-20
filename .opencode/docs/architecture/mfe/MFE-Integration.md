# MFE Integration (example)

Generic notes on a micro-frontend (MFE) shell loading feature modules.
Fictional `the-project` example.

## Contract

- Shell exposes a `register(route, mountFn)` API.
- Features self-register at boot.
- Shared state via a tiny event bus.

## Loading

Features lazy-load from a CDN/registry. Versioned by semantic version.

(Replace `the-project` and the systems with your own. No real hosts here.)
