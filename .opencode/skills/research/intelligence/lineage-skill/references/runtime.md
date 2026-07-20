# Runtime Reference

Use this file only when `SKILL.md` does not contain enough detail for the selected workflow.

## Method

Operational method:

```text
Capture -> Cite -> Compress -> Connect -> Codify -> Evaluate
```

- **Capture**: keep original source order, filenames, lesson numbers, timestamps, screenshots, and OCR outputs when available.
- **Cite**: build evidence before broad summaries. Prefer source paths and lesson IDs over unsupported paraphrase.
- **Compress**: summarize in layers: lesson summary, concepts, topics, cases, methods, quotes, and study paths.
- **Connect**: rebuild relationships across lessons: prerequisites, repeated themes, aliases, examples, and workflows.
- **Codify**: package the course into a Skill with `SKILL.md`, `references/`, `scripts/`, and `agents/`.
- **Evaluate**: check completeness, citation strength, missing fields, and high-stakes boundaries.

Evidence strength:

- Strong: transcript segment, quote index, OCR text, screenshot, or lesson summary all support the claim.
- Medium: one direct source supports the claim.
- Weak: only course-level synthesis supports the claim.
- Unsupported: no packaged reference supports the claim. Say what is missing.

## Configuration

Read only the variables needed for the selected workflow.

```bash
# Audio transcription
AUDIO_TRANSCRIBE_API_KEY=
AUDIO_TRANSCRIBE_BASE_URL=https://api.siliconflow.cn/v1
AUDIO_TRANSCRIBE_MODEL=FunAudioLLM/SenseVoiceSmall

# Vision analysis. Use a model with video-understanding support.
LINEAGE_VISION_API_KEY=
LINEAGE_VISION_BASE_URL=https://your-openai-compatible-vision-endpoint/v1
LINEAGE_VISION_MODEL=gemini-3.1-pro-preview
LINEAGE_VISION_TIMEOUT=600

# Text distillation
LINEAGE_TEXT_API_KEY=
LINEAGE_TEXT_BASE_URL=https://api.openai.com/v1
LINEAGE_TEXT_MODEL=gpt5.5
LINEAGE_TEXT_MAX_TOKENS=4096
LINEAGE_TEXT_TIMEOUT=300

# Optional local extractive fallback
DISTILL_USE_LLM=1
DISTILL_CHUNK_SIZE=6000
DISTILL_CHUNK_OVERLAP=500

# Optional MinerU / OCR
MINERU_API_TOKEN=
```

If a provider is missing, continue with the smallest viable workflow:

- Existing transcripts, OCR, notes, or distillation files: skip missing capture stages.
- Raw audio/video without ASR: stop before transcription and list missing variables or tools.
- Raw video without vision: stop before visual analysis, or continue transcript-only if the user accepts.
- PDFs without MinerU: use existing OCR/text sources only and say scanned/image PDF evidence was not included.

## CoursePackage

`course_package.json` is the normalized middle layer between course materials and generated Skills.

Required top-level shape:

```json
{
  "schema_version": "0.1",
  "manifest": {},
  "lessons": [],
  "concepts": [],
  "topics": [],
  "cases": [],
  "methods": [],
  "learning_checks": [],
  "quotes": [],
  "evidence": [],
  "study_paths": [],
  "boundaries": [],
  "quality": {}
}
```

Minimum generated Skill references:

- `course_digest.md`
- `lesson_index.json`
- `concept_glossary.md`
- `evidence_map.json`
- `quote_index.md`
- `study_paths.md`
- `course_package.json`

## Roles

Default role: `mentor`.

| Role | Use when |
| --- | --- |
| `mentor` | Guided learning, practice, review, progress-aware study, and course-backed application |
| `expert` | Course Q&A, concept explanation, lesson lookup, and source-backed answers |
| `consultant` | Private consulting, scenario diagnosis, option comparison, and course-grounded advice |
| `practitioner` | SOPs, checklists, playbooks, templates, drafts, workflows, and work outputs |
| `custom` | User-defined role or workflow not covered above |

Scope, citation strictness, and learner progress are separate options. Do not encode them as fake role names.

## PDF / OCR

Use MinerU only when PDFs, scans, handouts, or slide exports should become evidence.

Workflow:

1. Check `MINERU_API_TOKEN`.
2. Run the full pipeline with `--documents-input`, or call `scripts/parse_mineru_documents.py`.
3. Confirm `documents/mineru_manifest.json` and `documents/mineru_supplement.md` exist.
4. Rebuild `course_package.json`.
5. Rebuild the target Skill.

Existing OCR output can be reused with `--skip-submit`.

## Outputs And Resume

Course build state belongs under `<base-dir>/<course-name>/`. Generated Skills belong under `<output-dir>/<skill-name>/`.

Expected course workspace:

```text
<course-name>/
├── transcripts/
├── analysis/
│   └── screenshots/
├── documents/
├── full_transcript.md
├── lesson_summaries.json
├── course_distillation_<date>.md
├── course_distillation_<date>.json
├── course_package.json
└── lineage_progress.json
```

Resume rules:

- Reuse existing transcripts, analyses, documents, distillation files, and CoursePackage when present.
- Do not mix multiple source courses in one `<course-name>` directory unless the user explicitly requests a combined package.
- Prefer rerunning the narrow missing stage over rebuilding the whole pipeline.
- Use `lineage_progress.json` to report what exists, what is missing, and what will run next.
