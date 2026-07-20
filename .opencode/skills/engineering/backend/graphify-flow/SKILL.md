---
name: graphify-flow
description: Install and use graphify from the agent to build knowledge graphs for codebases, docs, papers, or mixed folders, then inspect GRAPH_REPORT.md and graph outputs.
---


# Graphify Workflow

Use this skill when the user wants structural understanding of a repo or folder.

Prerequisites:
- graphify CLI available on PATH
- Python package graphifyy installed

Quick checks:
- `graphify --help`
- `python3 -c "import graphify"`

Typical workflow:
1. Choose a target folder.
2. Run graphify on it:
   - `graphify install --platform codex` installs always-on instructions for Codex-style agents.
   - For graph generation itself, use the installed skill command in the target agent environment or run graphify-enabled workflows in the project.
3. Inspect outputs in `graphify-out/`:
   - `GRAPH_REPORT.md`
   - `graph.json`
   - `graph.html`
4. Summarize god nodes, communities, surprising connections, and suggested questions.

Recommended commands:
- `graphify --help`
- `graphify codex install`
- `graphify the agent install`
- `graphify hook install`

Notes:
- graphify is strongest for mixed corpora and unfamiliar codebases.
- It is useful as a structure-first orientation layer before raw grep/search.
- Keep output review focused on architecture, rationale, and cross-file relationships.

Important local finding:
- The packaged `graphify` CLI from `graphifyy` may expose only install/hook/benchmark commands, not a direct graph-build command.
- For one-shot local code-only graph generation, use the internal rebuild entrypoint instead:
  `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('/path/to/project'))"`
- This writes into `/path/to/project/graphify-out/` and at minimum produces `GRAPH_REPORT.md` and `graph.json`.

Compatibility pitfall discovered:
- On some environments, `graphifyy 0.3.1` can fail during JSON export because `networkx.readwrite.json_graph.node_link_data` may expect `link=` instead of `edges=`.
- If export fails with `node_link_data() got an unexpected keyword argument 'edges'`, patch `graphify/export.py` so `to_json()` tries `edges="links"` first and falls back to `link="links"` on `TypeError`.


Environment mismatch pitfall:
- Do not assume `python3 -c "from graphify.watch import _rebuild_code ..."` works in the user's interactive shell just because it works in the agent.
- the agent may have a different Python environment/site-packages than the user's terminal.
- Before giving a Python import-based rebuild command, first verify in the user's shell context with:
  `python3 -c "import graphify, sys; print(sys.executable); print(graphify.__file__)"`
- If the user's shell reports `ModuleNotFoundError: No module named 'graphify'`, stop suggesting Python import rebuild commands.

Method correction rule:
- Prefer the actual installed CLI/help output over assumptions from prior environments.
- Ask the user to run `graphify` or `graphify --help` first, then tailor instructions to the subcommands that really exist.
- If the local `graphify` binary exposes only installer/hook commands and no build/rebuild command, conclude that graph generation is not available from that installation and do not keep retrying fake rebuild invocations.
- In that case, explicitly tell the user the repo-local graphify rebuild rule is currently non-executable in their environment and continue the main task without blocking on graphify, unless they provide the real generator command/script.
