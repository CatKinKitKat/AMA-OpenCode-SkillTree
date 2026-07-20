---
name: audiocraft
description: Music generation and audio processing with AudioCraft (MusicGen, AudioGen, Encodec, JASCO). Use when generating music from text prompts, audio effects, or compressing audio with neural codecs.
---
# AudioCraft

Music generation and audio processing with AudioCraft: MusicGen, AudioGen, Encodec, JASCO.

## When to Use

- [done] Generate music from text descriptions (MusicGen)
- [done] Generate sound effects and environmental audio (AudioGen)
- [done] Compress audio with neural codecs (Encodec)
- [done] Generate music with text + audio conditioning (JASCO)

## Tech Stack

- AudioCraft (Facebook Research)
- PyTorch
- HuggingFace Transformers / diffusers
- CUDA (GPU required. CPU fallback is slow)

## Workflow

### Install

```bash
pip install audiocraft
```

### MusicGen

```python
from audiocraft.models import MusicGen
model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=8)
descriptions = ["a calming lofi beat, 90 bpm, chillhop"]
wav = model.generate(descriptions)
```

### AudioGen

```python
from audiocraft.models import AudioGen
model = AudioGen.get_pretrained("facebook/audiogen-medium")
model.set_generation_params(duration=5)
wav = model.generate(["footsteps on a wooden floor"])
```

## Pitfalls

- GPU required for real-time use (~4GB VRAM for small, ~16GB for large)
- AudioGen outputs are monaural by default
- Generated audio may contain artifacts. Always post-process (EQ/compress) before use
- Commercial use: check AudioCraft license (RAIL license permits commercial)
