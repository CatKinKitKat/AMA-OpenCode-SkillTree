---
name: qmd-eval-inst-intg
description: Evaluate the QMD repo/tool before adoption, install it safely on the host, and integrate it into an agent workflow without violating the repo's own automation constraints.
license: MIT
metadata: 
author: the agent
version: 1.0.0
tags: [qmd, mcp, local-search, bun, node, agent-integration, github]
---


# QMD: evaluate, install, integrate

Use when a user points the agent at `https://github.com/tobi/qmd` (or the npm package `@tobilu/qmd`) and asks whether to learn/install/clone/integrate it.

## Goals

1. Read the upstream README first.
2. Check the live machine for prerequisites before recommending install.
3. Clone the repo if source inspection matters.
4. Respect upstream agent instructions in `AGENTS.md` / `AGENTS.md`.
5. Prefer Bun for source workflow if upstream says so.
6. Do **not** auto-index the user's files if upstream explicitly forbids automatic `collection add`, `embed`, or `update`.

## Procedure

### 1. Inspect before acting

- Clone or shallow-clone the repo.
- Read:
  - `README.md`
  - `package.json`
  - any `AGENTS.md` / `AGENTS.md`
- Verify actual host tools, not assumptions:
  - `command -v qmd || true`
  - `command -v bun || true`
  - `command -v node || true`
  - `node -v 2>/dev/null || true`
  - `bun -v 2>/dev/null || true`
  - `npm view @tobilu/qmd version 2>/dev/null || true`

### 2. Decide route

Use this decision logic:

- If user only wants usage: recommend global install.
- If user wants architecture, adaptation, or deeper reuse: also clone source.
- If upstream docs say “Use Bun instead of Node.js”, follow that for repo-local dev/install.

For QMD specifically, note:
- published package: `@tobilu/qmd`
- current CLI entry: `qmd`
- source/dev path prefers `bun install` + `bun link`
- package build output required for linked CLI: run `bun run build` before relying on `qmd`

### 3. Handle broken existing global install

A common failure mode:
- `npm install -g @tobilu/qmd` fails with `EEXIST`
- existing `qmd` path is a broken symlink, e.g. under `~/.npm-global/bin/qmd`

Check with:
- `file ~/.npm-global/bin/qmd || true`
- `ls -l ~/.npm-global/bin/qmd || true`

If the existing global install is broken, do **not** keep insisting on npm.
Change course to repo-local Bun workflow:

```sh
git clone https://github.com/tobi/qmd ~/qmd
cd ~/qmd
bun install
bun run build
bun link
command -v qmd
qmd --help
```

Reason:
- `bun link` can produce a working `qmd` even when the old npm global path is stale.
- `bun link` alone may still fail at runtime if `dist/cli/qmd.js` has not been built yet.

### 4. Verify install, not just command presence

After install/link, verify with real execution:

```sh
command -v qmd
qmd --help | head -n 60
```

Do not trust `command -v qmd` alone.
A linked binary can exist but still fail due to missing `dist/cli/qmd.js`.

### 5. Respect upstream automation limits

QMD's `AGENTS.md` explicitly says:
- never run `qmd collection add` automatically
- never run `qmd embed` automatically
- never run `qmd update` automatically

Therefore:
- the agent may install, build, clone, inspect, and verify the CLI.
- the agent should **stop short** of indexing user content automatically.
- Instead, provide exact commands for the user to run manually.

### 6. Integration guidance to give user

Present three integration layers:

1. CLI layer
   - use `qmd search`, `qmd query`, `qmd get`, `qmd multi-get`
2. MCP layer
   - use `qmd mcp` or `qmd mcp --http --daemon`
   - recommend this as the cleanest agent integration path
3. SDK layer
   - mention `createStore`, `search`, `get`, `multiGet`, `update`, `embed`
   - use for deeper embedding into custom agent systems

### 7. Important architecture findings worth surfacing

When auditing QMD, call out:
- `src/store.ts` = search/index core
- `src/cli/qmd.ts` = CLI surface
- `src/mcp/server.ts` = MCP server
- `src/index.ts` = SDK exports
- `src/embedded-skills.ts` = packaged skill content for agent use

Useful insight:
- QMD is not just a CLI. It is a local search stack with CLI + SDK + MCP + packaged skill distribution.

## Reusable recommendations

If the user has multilingual/CJK corpora, recommend:

```sh
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
qmd embed -f
```

But only as a manual next step, not auto-run.

## 9. MLX-VLM local assistant sidecar for the agent/QMD on Apple Silicon

When the user wants a small local Gemma 4 assistant to complement the agent and QMD on macOS Apple Silicon, prefer an MLX-native E2B model instead of trying to force large Gemma 4 variants or CUDA/vLLM TurboQuant repos.

### What worked in practice

On this user's M1 8GB macOS host, the practical path was:

1. Create a dedicated venv:

```sh
python3 -m venv ~/.venvs/mlx-vlm
source ~/.venvs/mlx-vlm/bin/activate
pip install -U pip setuptools wheel
pip install -U mlx mlx-lm mlx-vlm
```

2. Verify MLX/Metal before touching any large model:

```sh
python - <<'PY'
import mlx.core as mx
print('metal', mx.metal.is_available() if hasattr(mx,'metal') else 'no-metal-api')
print('default_device', mx.default_device())
PY
```

3. Prefer small Gemma 4 variants for 8GB RAM:
- best practical base: `google/gemma-4-E2B-it`
- MLX quantized base: `mlx-community/gemma-4-e2b-it-4bit`
- user-selected local sidecar that fit the goal: `deadbydawn101/gemma-4-E2B-Heretic-Uncensored-mlx-4bit`

### Important model-selection lessons

- Do **not** recommend Gemma 4 31B adapters (including Opus/4.6-style PEFT adapters) for an 8GB M1 host.
- A PEFT/LoRA adapter built on `google/gemma-4-31B-it` is still effectively a 31B deployment requirement.
- For this class of machine, E2B is the realistic ceiling. E4B may be marginal, and 26B/31B are not practical daily-driver choices.

### TurboQuant lesson

The user referenced Google's TurboQuant and wanted it exploited. The important correction is:
- TurboQuant mainly compresses **KV cache**, not the entire model weights.
- Therefore it does **not** make overall memory usage become "one sixth" in general.
- It helps more for long-context / long-generation workloads than for short prompts.

### Repo-choice lesson

Two external repos were inspected:
- `0xSero/turboquant`: useful research implementation, but targeted at vLLM/CUDA/Triton/RTX workflows. **not** the right direct path for this Apple Silicon host.
- `Blaizzy/mlx-vlm`: the correct practical path on this host. Includes Gemma 4 support and server flags for KV quantization including `turboquant`.

So on Apple Silicon, prefer `mlx-vlm` instead of trying to transplant the CUDA-first TurboQuant repo.

### Server configuration that worked

After manually downloading the model snapshot to a local directory, the following sidecar config worked:

```sh
source ~/.venvs/mlx-vlm/bin/activate
python -m mlx_vlm server \
  --model ~/.cache/mlx-heretic-e2b \
  --host 127.0.0.1 \
  --port 18080 \
  --prefill-step-size 256 \
  --kv-bits 3.5 \
  --kv-quant-scheme turboquant \
  --max-kv-size 2048
```

Health check:

```sh
curl -s http://127.0.0.1:18080/health
```

Expected healthy response shape:

```json
{"status":"healthy","loaded_model":"...","loaded_adapter":null}
```

### Real-world pitfalls discovered

#### A. Port collision

Port `8080` may already be occupied by a prior `mlx-vlm` instance. Check first:

```sh
lsof -nP -iTCP:8080 -sTCP:LISTEN || true
```

If occupied, move to another local port such as `18080`.

#### B. Hugging Face SSL/download failures during preload

Observed failure while trying to let `mlx_vlm server` pull the model itself:
- `UNEXPECTED_EOF_WHILE_READING`
- `LocalEntryNotFoundError`

Better pattern on flaky networks:
1. pre-download snapshot to a local folder
2. point `--model` at the local folder

This avoids relying on server startup as the downloader.

#### C. Downloaded local model shape for MLX repos

A valid local MLX model directory looked like this:
- `model.safetensors`
- `model.safetensors.index.json`
- `config.json`
- `generation_config.json`
- `processor_config.json`
- `tokenizer.json`
- `tokenizer_config.json`
- `chat_template.jinja`

### Recommended role in the agent/QMD

Treat this MLX Gemma sidecar as a **local helper brain**, not the main heavy model.

Good uses:
- query rewrite / query expansion
- summarize QMD retrieval results
- produce concise answer drafts from top-k passages
- light reranking / preference shaping over already-retrieved snippets

Avoid using it as:
- a large-context primary reasoning engine
- the main code-generation brain
- a replacement for the full hosted frontier model

### Decision rule to reuse

On macOS Apple Silicon with <=8GB RAM:
1. choose E2B class Gemma 4
2. prefer MLX-native quantized repos
3. use `mlx-vlm server` as a localhost sidecar
4. enable TurboQuant only as KV optimization, not as a magical total-memory fix
5. keep QMD for retrieval and use the MLX sidecar only after retrieval

On this user's macOS host, QMD had multiple real-world failure modes that require a stricter routing policy than the original skill.

### A. Bun-linked CLI may be runnable but unusable for embeddings/vector DB

Observed failure from Bun-linked `qmd`:
- `sqlite-vec extension is unavailable`
- `no such module: vec0`

This happened even though:
- `qmd --help` worked
- the repo was built successfully with `bun run build`
- Homebrew `sqlite` was already installed

Implication:
- treat `bun link` as acceptable for source inspection / basic CLI smoke test only
- do **not** assume it is valid for real embedding/vector operations on macOS
- prefer npm-installed QMD for actual usage when vector/index features matter

### B. PATH precedence can silently keep invoking the wrong QMD

Observed state:
- Bun version at `~/.bun/bin/qmd`
- npm version at `~/.npm-global/bin/qmd`
- `PATH` preferred `~/.bun/bin`, so `which qmd` kept returning the Bun-linked one

Therefore after npm install, always verify:

```sh
which qmd
ls -l ~/.bun/bin/qmd ~/.npm-global/bin/qmd 2>/dev/null || true
```

If needed, temporarily force npm-first resolution:

```sh
export PATH="$HOME/.npm-global/bin:$PATH"
hash -r
which qmd
```

If the user wants the blunt fix:

```sh
rm -f ~/.bun/bin/qmd
hash -r
```

### C. npm-installed QMD can hit native ABI mismatch if built under a different Node ABI

Observed failure:
- `better_sqlite3.node was compiled against a different Node.js version`
- module expected one `NODE_MODULE_VERSION` but the active `node` required another

Implication:
- after `npm install -g @tobilu/qmd`, do not assume success just because the binary exists
- immediately run a real command such as `qmd status`
- if ABI mismatch appears, reinstall/rebuild under the currently active Node version before proceeding

### D. Embedding model override must be re-exported in the same shell actually running QMD

The user set `QMD_EMBED_MODEL=Qwen...`, but a later run still showed:
- `Model: hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf`

So when troubleshooting model mismatch / dimension mismatch, verify the effective runtime path and env in the same shell session that invokes `qmd`.

### E. Long embed runs can fail two different ways on macOS

Observed during `qmd embed -f`:
1. `Session expired — skipping ... remaining chunks/document batch`
2. crash at process exit from `ggml-metal-device.m` with `GGML_ASSERT([rsets->data count] == 0)`

Implication:
- partial embedding progress may still be committed before the crash
- the failure is not necessarily QMD indexing logic. It can be lower-level Metal / llama.cpp cleanup
- recommend CPU fallback and smaller batches for stability

Suggested recovery command:

```sh
export PATH="$HOME/.npm-global/bin:$PATH"
hash -r
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
export QMD_LLAMA_GPU=off
qmd embed -f --max-docs-per-batch 8 --max-batch-mb 16
```

If `off` is not accepted, try:

```sh
export QMD_LLAMA_GPU=cpu
```

### F. Updated install preference for macOS

For macOS adoption guidance, use this priority:

1. Read/evaluate repo via clone
2. Bun workflow is fine for source audit and local dev inspection
3. For real daily CLI usage, prefer npm global install
4. Verify active `qmd` path and runtime with `which qmd` + `qmd status`
5. If embeddings crash on Metal, rerun on CPU with reduced batch sizes

## 9. TurboQuant / MLX / Gemma 4 integration guidance

When a user wants to combine QMD with Google TurboQuant, MLX, or Gemma 4, do not collapse these into a single "just use MLX" answer. Distinguish the integration layers precisely.

### A. What TurboQuant actually is

If the user references Google's TurboQuant blog/paper (`TurboQuant: Redefining AI efficiency with extreme compression`), treat it as:
- a **KV cache compression** / vector compression method
- not a general MLX runtime
- not a Gemma model variant
- not a drop-in replacement for `node-llama-cpp`

Important implication:
- TurboQuant's most direct architectural fit is **vector / KV compression**, not first-line replacement of QMD's embedding model runtime.

### B. QMD integration priority when TurboQuant is mentioned

Use this priority order:

1. **Identify the user's real goal**
   - If they want better local generation/reasoning on Apple Silicon: Gemma 4 + MLX is the likely path.
   - If they want QMD's stored vectors/search memory reduced: TurboQuant-like vector codec is the path.
   - If they want both, separate them explicitly.

2. **For QMD proper, first inspect where embeddings enter storage**
   - `src/store.ts` around:
     - first-dimension bootstrap via `session.embed(...)`
     - batch embedding via `session.embedBatch(...)`
     - insertion via `insertEmbedding(... Float32Array(result.embedding) ...)`
   - This is the actual hook point for any future vector codec.

3. **Do not claim TurboQuant can be directly dropped into QMD**
   - The discovered `0xSero/turboquant` repo targets:
     - vLLM
     - CUDA / Triton
     - KV cache compression during inference
   - It is **not** a drop-in Apple/MLX/QMD embedding backend.

4. **Do not claim `mlx-vlm` is an embedding replacement for QMD**
   - The discovered `Blaizzy/mlx-vlm` repo is primarily:
     - MLX VLM / multimodal inference
     - includes Gemma 4 support
     - includes TurboQuant KV cache options for server inference
   - It is useful for Gemma 4 local generation, but is **not** a ready-made text embedding backend for QMD.

### C. Recommended architecture guidance

When the user wants "Gemma 4 + TurboQuant + QMD", give this architecture split:

- **QMD** keeps:
  - indexing
  - collections
  - sqlite / sqlite-vec
  - MCP / CLI / SDK
- **Gemma 4 via MLX-VLM** is best considered first for:
  - query expansion
  - reranking
  - reasoning / generation
- **TurboQuant** is best considered separately for:
  - KV cache compression in Gemma inference
  - future vector codec work if QMD later adopts compressed vector storage/search

### D. Practical model choice on Apple Silicon

If the user wants the strongest Gemma 4 they can realistically run locally, do not reflexively recommend the largest model.
Use discovered upstream memory guidance from `mlx_vlm/models/gemma4/README.md`:

- `google/gemma-4-e2b-it` ~5 GB
- `google/gemma-4-e4b-it` ~16 GB
- `google/gemma-4-26b-a4b-it` ~52 GB
- `google/gemma-4-31b-it` ~63 GB

On a typical Apple Silicon laptop, the practical recommendation is usually:
- start with `google/gemma-4-e4b-it`

Reason:
- best balance of capability vs feasibility
- stronger than 2B but far more realistic than 26B/31B

### E. Correct framing to avoid future confusion

If the user says "implement Turbo into QMD first", interpret that literally as:
- first-class integration point should be **vector/KV compression layer**, not "switch runtime to MLX"

If the user says they want "Gemma 4, strongest I can actually run", interpret that as:
- first operational milestone is **MLX-VLM + Gemma 4 local inference validation**
- not immediate deep modification of QMD internals

### F. Safe recommendation pattern

When advising next steps, prefer:
1. Evaluate the external repos before trusting them.
2. Distinguish runtime/inference tooling from vector-storage/search tooling.
3. Recommend `gemma-4-e4b-it` first for local Apple Silicon.
4. Treat TurboQuant repo as a research/integration reference, not a drop-in dependency.
5. Only propose QMD code changes after the exact desired integration layer is settled.


## 11. QMD model configuration on this host

When the user asks to change QMD's embedding/rerank/generation models, do **not** invent a `qmd config` command.
First verify the live CLI surface with:

```sh
qmd --help
```

### A. Actual config location and schema

On this host, QMD loads model config from YAML at:

```sh
~/.config/qmd/index.yml
```

The relevant schema is:

```yaml
models:
  embed: hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf
  rerank: hf:ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF/qwen3-reranker-0.6b-q8_0.gguf
  generate: hf:tobil/qmd-query-expansion-1.7B-gguf/qmd-query-expansion-1.7B-q4_k_m.gguf
```

This is grounded by `src/collections.ts` and `src/cli/qmd.ts`:
- config file defaults to `~/.config/qmd/index.yml`
- CLI loads YAML via `loadConfig()`
- if `config.models` exists, it constructs `new LlamaCpp({ embedModel, generateModel, rerankModel })`

### B. Safe write rule

Do **not** tell the user to append blindly with `cat >>` unless you have first confirmed no existing `models:` block.
A duplicate top-level `models:` key causes YAML parse failure:

- `YAMLParseError: Map keys must be unique`

Safer guidance:
- inspect the current file first
- if `models:` already exists, replace that block instead of appending another one
- if the file has no `models:` block, then append once

### C. Important runtime gotcha: status may silently fall back to defaults

Observed behavior on this host:
- `index.yml` contained valid custom `models:` entries
- `qmd status` still printed the old default models

Source inspection showed why:
- `src/cli/qmd.ts` wraps config-based model initialization in `try { ... } catch {}`
- therefore model-load errors can be swallowed and QMD silently falls back to built-in defaults

Implication:
- a correct YAML file does **not** prove the custom model stack loaded successfully
- always verify both:
  1. config file contents
  2. runtime behavior (`qmd status`, and if needed an actual query/embed command)

### D. Failure classification discovered here

On this macOS host, when custom model config seemed ignored, the more likely cause was runtime dependency failure rather than YAML syntax.
Observed warning:

```sh
sqlite-vec extension is unavailable. On macOS with Bun, install Homebrew SQLite: brew install sqlite
```

Therefore when custom models appear ignored:
1. verify `~/.config/qmd/index.yml`
2. run `qmd status`
3. if defaults still appear, treat it as runtime fallback
4. inspect dependency/runtime errors before claiming the config edit failed

### E. Recommendation style correction

If giving the user shell commands to edit config:
- prefer exact replacement or a small Python edit snippet
- avoid append-only instructions unless you explicitly checked there is no prior block
- mention that `>` overwrites and `>>` appends

This avoids a repeat of the duplicate-`models:` YAML failure.
