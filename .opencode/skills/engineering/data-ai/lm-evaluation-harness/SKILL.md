---
name: lm-evaluation-harness
description: Benchmark LLMs with lm-eval-harness: MMLU, GSM8K, HellaSwag, TruthfulQA, and custom tasks. Use when evaluating model quality, comparing fine-tunes, or producing reproducible LLM benchmark reports.
---
# lm-evaluation-harness

Benchmark LLMs with lm-eval-harness: MMLU, GSM8K, HellaSwag, TruthfulQA, and custom tasks.

## When to Use

- [done] Comparing model quality (base vs fine-tune, model A vs model B)
- [done] Producing a reproducible benchmark report for stakeholders
- [done] Evaluating a model on organization-specific tasks (custom task)
- [done] Determining if a model meets a regulatory or quality gate

## Tech Stack

- lm-eval-harness (EleutherAI)
- HuggingFace Transformers
- PyTorch / vLLM / TGI (optional, for faster inference)
- Weights & Biases (optional, for experiment tracking)

## Workflow

### Install

```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness && pip install -e .
```

### Run benchmarks

```bash
lm_eval --model hf --model_args pretrained=org/model,tokenizer=org/model   --tasks mmlu,gsm8k,hellaswag --batch_size 8 --device cuda:0   --output_path results.json
```

### Custom task

```python
# lm_eval/tasks/my_custom/
def docs(self): return [...]
def has_training_docs(self): return False
def aggregation(self): return {"acc": mean}
def higher_is_better(self): return {"acc": True}
```

## Pitfalls

- MMLU: results vary by few-shot prompt. Always use same prompt for comparison
- GSM8K: use exact match only. Do not compare across different parsers
- Large models require multiple GPUs or use vLLM backend for memory efficiency
- Track random seed for reproducibility: `--seed 42`
