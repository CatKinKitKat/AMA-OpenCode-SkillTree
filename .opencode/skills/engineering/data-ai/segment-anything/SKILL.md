---
name: segment-anything
description: Zero-shot image segmentation with Meta's Segment Anything Model (SAM). Use when segmenting objects in images without training data, generating masks from points/boxes, or building interactive image annotation tools.
---
# Segment Anything (SAM)

Zero-shot image segmentation with Meta's Segment Anything Model.

## When to Use

- [done] Segment any object in an image without training
- [done] Generate masks from point clicks or bounding boxes
- [done] Build an interactive image annotation tool
- [done] Pre-segment images for downstream CV tasks (object detection, OCR pre-processing)

## Tech Stack

- Segment Anything Model (SAM)
- PyTorch
- OpenCV / Pillow

## Workflow

### Load SAM

```python
import torch
from segment_anything import sam_model_registry, SamPredictor

sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h.pth")
predictor = SamPredictor(sam)
predictor.set_image(image)
```

### Prompt with point

```python
masks, scores, logits = predictor.predict(
  point_coords=[[300, 200]],
  point_labels=[1],         # 1 = foreground, 0 = background
  multimask_output=True
)
```

### Prompt with box

```python
masks, scores, logits = predictor.predict(
  box=[100, 100, 400, 400],  # [x1, y1, x2, y2]
  multimask_output=True
)
```

## Pitfalls

- vit_h requires ~16GB VRAM. Use vit_l or vit_b if VRAM is limited
- For video: use SAM2 (Segment Anything 2) for temporal consistency
- Point prompts are more reliable than box prompts for fine-grained segmentation
- Output masks are binary. Convert to COCO RLE or polygon as needed
