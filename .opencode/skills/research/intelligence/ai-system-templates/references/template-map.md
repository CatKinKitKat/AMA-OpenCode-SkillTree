# Awesome Architecture AI Template Map

- Source repo: `~/.agent/external-repos/awesome-architecture`
- Source commit: `ab8267312cdb26df01de5b071bf112218dba4221`
- Scope: the AI-native templates under `templates/`.

## Template Map

- AI chat product: `templates/ai-chat-product/README.md`
  Use for chat surfaces with streaming output, context windows, RAG, and cost control.
- AI gateway: `templates/ai-gateway/README.md`
  Use for unified model access, routing, billing, caching, rate limits, and failover.
- RAG knowledge base: `templates/rag-knowledge-base/README.md`
  Use for chunking, hybrid retrieval, reranking, citation traceability, and refresh pipelines.
- AI agent platform: `templates/ai-agent-platform/README.md`
  Use for action loops, tool sandboxes, memory, fallback paths, and guardrails.
- Inference serving: `templates/inference-serving/README.md`
  Use for continuous batching, KV cache behavior, quantization, and multi-replica serving.
- Vector database: `templates/vector-database/README.md`
  Use for ANN choices, recall-latency trade-offs, and embedding retrieval infrastructure.

## Usage Notes

- Pair `ai-gateway` with `inference-serving` when the question spans both traffic control and model serving internals.
- Pair `rag-knowledge-base` with `vector-database` when the user is mixing retrieval pipeline design with storage/index design.
- Pair `ai-agent-platform` with `architecture-thinking` when the user still has unresolved control-boundary questions.

