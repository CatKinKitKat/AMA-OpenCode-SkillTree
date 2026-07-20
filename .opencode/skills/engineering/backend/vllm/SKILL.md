---
name: vllm
description: >-
  vLLM serving integration: configure endpoints, run OpenAI-compatible inference,
  apply quantization, profile throughput/latency, and troubleshoot GPU/CPU mode
  issues.
model: sonnet
permission:
  edit: allow
  bash: allow
---

# vLLM

## Overview
This skill covers deploying and operating **vLLM** for high-throughput LLM serving,
whether on-prem GPU hosts or CPU-based inference nodes. It focuses on the
OpenAI-compatible server mode, quantization workflows, autoscaling, and common
runtime issues.

## When to Use This Skill
- [done] Starting or tuning a local vLLM endpoint for an the-project inference workload.
- [done] Exposing an OpenAI-compatible API from an the-project model-queue cluster.
- [done] Comparing FP16, INT8, or INT4 serving performance/quality on the-project hardware.
- [done] Diagnosing latency spikes, OOM failures, or scheduling conflicts in the-project
  inference environments.

## Prerequisites / Tech Stack
- **Python**: 3.10+
- **Model source**: local `/opt/models/` directory or compatible registry endpoint.
- **Hardware**: discrete GPU for primary use case. CPU fallback supported.
- **Execution stage**: runtime only, local development, and CI inference checks.

## Workflow / Steps
1. **Select a model format**  
   Preferred: Hugging Face-compatible weights only, such as `/opt/models/service-a/`
   or `models/service-b/`.

2. **Install and verify dependencies**  
   Verify CUDA or ROCm toolchain compatibility before runtime work.

3. **Build the serve target**  
   Start the server in `python -m vllm.entrypoints.openai.api_server` style or
   `vllm serve` syntax.

4. **Test the OpenAI-compatible endpoint**  
   Validate `/v1/chat/completions`, `/v1/completions`, and `/v1/models` routes.

5. **Apply quantization and profiling**  
   Swap to GGUF/awq/gptq modes and throughput-test with a representative synthetic or
   recorded enabled traffic trace.

6. **Add logging and alerting hooks**  
   Emit request latency, queue depth, and token-throughput logs in JSON Lines.

## Examples
```bash
# Disable portal access and start the local service endpoint.
# the-project example runs on the local development loopback; do not bind on the wildcard.
vllm serve /opt/models/service-a \
  --host 127.0.0.1 \
  --port 8000 \
  --dtype half \
  --max-model-len 4096
```

```bash
# Health check the local endpoint.
curl -sS http://127.0.0.1:8000/health
# Expected: {"status":"healthy"} or equivalent healthy response.
```

## Common Pitfalls / Best Practices

### Avoid
- Exposing the inference pipeline on the public internet by default.
- Hardcoding the model path if you plan to reuse this workflow across models.
- Ignoring GPU host firewall or ACL preflight checks on the the-project software-defined
  network.

### Prefer
- Monitoring request lifecycle and token-throughput logs in structured form.
- Running saturation tests before production hand-off.
- Storing raw model assets externally from the container image for easier audits.

## References

- vLLM docs: https://docs.vllm.ai/
- OpenAI API reference: https://platform.openai.com/docs/api-reference
- GGUF/ Llama.cpp context: https://github.com/ggerganov/llama.cpp
