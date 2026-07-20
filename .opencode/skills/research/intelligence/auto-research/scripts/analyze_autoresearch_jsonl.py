#!/usr/bin/env python3
import argparse
import json
import math
import pathlib
import statistics
import sys
from typing import Any


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(statistics.median(values))


def mad(values: list[float]) -> float:
    if not values:
        return 0.0
    m = median(values)
    deviations = [abs(v - m) for v in values]
    return median(deviations)


def is_better(candidate: float, current: float, direction: str) -> bool:
    return candidate < current if direction == "lower" else candidate > current


def improvement(baseline: float, best: float, direction: str) -> float:
    return (baseline - best) if direction == "lower" else (best - baseline)


def load_segments(path: pathlib.Path) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            raise SystemExit(f"bad json at line {lineno}: {e}")
        if obj.get("type") == "config":
            current = {"config": obj, "results": []}
            segments.append(current)
            continue
        if obj.get("type") == "result":
            if current is None:
                current = {
                    "config": {
                        "name": "implicit",
                        "metric_name": "metric",
                        "metric_unit": "",
                        "direction": "lower",
                        "timestamp": None,
                    },
                    "results": [],
                }
                segments.append(current)
            current["results"].append(obj)
    return segments


def summarize_segment(segment: dict[str, Any], index: int) -> dict[str, Any]:
    cfg = segment["config"]
    results = segment["results"]
    direction = cfg.get("direction", "lower")
    metric_name = cfg.get("metric_name", "metric")
    metric_unit = cfg.get("metric_unit", "")

    metrics = [float(r["metric"]) for r in results if isinstance(r.get("metric"), (int, float))]
    baseline = metrics[0] if metrics else None
    best = None
    best_row = None
    for row in results:
        value = row.get("metric")
        if not isinstance(value, (int, float)):
            continue
        value = float(value)
        if best is None or is_better(value, best, direction):
            best = value
            best_row = row

    conf = None
    if len(metrics) >= 3 and best is not None and baseline is not None:
        noise = mad(metrics)
        delta = abs(improvement(baseline, best, direction))
        if noise > 0:
            conf = delta / noise

    status_counts: dict[str, int] = {}
    for row in results:
        status = str(row.get("status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "segment": index,
        "name": cfg.get("name"),
        "metric_name": metric_name,
        "metric_unit": metric_unit,
        "direction": direction,
        "runs": len(results),
        "baseline": baseline,
        "best": best,
        "improvement": None if baseline is None or best is None else improvement(baseline, best, direction),
        "confidence": conf,
        "best_commit": None if best_row is None else best_row.get("commit"),
        "best_description": None if best_row is None else best_row.get("description"),
        "status_counts": status_counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize autoresearch.jsonl segments and MAD confidence.")
    parser.add_argument("path", nargs="?", default="autoresearch.jsonl", help="Path to autoresearch.jsonl")
    parser.add_argument("--latest", action="store_true", help="Print only the latest segment")
    args = parser.parse_args()

    path = pathlib.Path(args.path)
    if not path.exists():
        raise SystemExit(f"not found: {path}")

    segments = load_segments(path)
    summaries = [summarize_segment(seg, i) for i, seg in enumerate(segments, start=1)]
    if args.latest and summaries:
        print(json.dumps(summaries[-1], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summaries, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
