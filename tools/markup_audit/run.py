#!/usr/bin/env python3
"""Inventory and audit freeform text fields for InlineMarkup-K1 adoption.

This tool scans all frames and reports:
- Which nodes have text/summary/title/label/desc fields
- Current text.format usage
- Obvious candidates for markup (code patterns, paths, emphasis, etc.)

Usage:
  tools/markup_audit/run.py [--out <report.json>]

Writes:
  out/markup_audit/report.json - structured report
  out/markup_audit/candidates.csv - human-readable candidate list

Design:
- Deterministic (stable ordering)
- No modifications, scan-only
- Best-effort heuristics for code patterns, paths, refs
"""

from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@dataclass
class FieldCandidate:
    """A single text field with markup opportunity."""
    frame_path: str
    node_id: str
    node_kind: str
    field_name: str
    current_format: str  # "plain", "md-inline", "md-block", or inferred
    has_code_backticks: bool
    has_paths: bool
    has_emphasis: bool
    has_references: bool
    has_lists: bool
    text_length: int
    recommendation: str  # "md-inline", "md-block", or "review"


def is_str(x: Any) -> bool:
    return isinstance(x, str) and bool(x)


def find_attr(attrs: Any, key: str) -> Optional[str]:
    if not isinstance(attrs, list):
        return None
    for a in attrs:
        if isinstance(a, dict) and a.get("key") == key:
            v = a.get("value")
            if isinstance(v, str):
                return v
    return None


def detect_patterns(text: str) -> Dict[str, bool]:
    """Detect markup-friendly patterns in text."""
    return {
        "code_backticks": "`" in text,
        "paths": bool(re.search(r"(frames|tools|docs|\.github)/[\w/\-\.]+", text)),
        "emphasis": bool(re.search(r"\*\*\w+\*\*|\*\w+\*|__\w+__|_\w+_", text)),
        "references": bool(re.search(r"(law|spec|frame)://\S+", text)),
        "lists": bool(re.search(r"^[\s]*[-*+]\s+\w", text, re.MULTILINE)),
        "multiline": "\n" in text,
    }


def recommend_format(text: str, patterns: Dict[str, bool]) -> Tuple[str, str]:
    """Recommend text.format and rationale."""
    if patterns["multiline"] or patterns["lists"]:
        return "md-block", "multiple paragraphs or lists"
    if patterns["code_backticks"] or patterns["paths"] or patterns["references"]:
        return "md-inline", "inline code/refs/paths"
    if patterns["emphasis"]:
        return "md-inline", "inline emphasis"
    return "plain", "no markup patterns detected"


def scan_frame(path: Path) -> List[FieldCandidate]:
    """Scan a frame.yml and yield field candidates."""
    candidates: List[FieldCandidate] = []
    try:
        data = read_yaml(path)
    except Exception:
        return candidates

    if not isinstance(data, dict):
        return candidates

    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        return candidates

    frame_path = str(path.relative_to(REPO_ROOT))

    for node in nodes:
        if not isinstance(node, dict):
            continue

        node_id = str(node.get("id") or "")
        node_kind = str(node.get("kind") or "")

        # Check for text.format in this node's attrs
        current_format = find_attr(node.get("attrs"), "text.format") or "plain"

        for field_name in ("text", "summary", "title", "label", "desc"):
            field_value = node.get(field_name)
            if not is_str(field_value):
                continue

            patterns = detect_patterns(field_value)
            rec_fmt, rec_reason = recommend_format(field_value, patterns)

            candidates.append(
                FieldCandidate(
                    frame_path=frame_path,
                    node_id=node_id,
                    node_kind=node_kind,
                    field_name=field_name,
                    current_format=current_format,
                    has_code_backticks=patterns["code_backticks"],
                    has_paths=patterns["paths"],
                    has_emphasis=patterns["emphasis"],
                    has_references=patterns["references"],
                    has_lists=patterns["lists"],
                    text_length=len(field_value),
                    recommendation=f"{rec_fmt} ({rec_reason})",
                )
            )

    return candidates


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO_ROOT / "out" / "markup_audit" / "report.json"))
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Scan all frames
    frames = sorted(REPO_ROOT.glob("frames/**/v*/frame.yml"))
    all_candidates: List[FieldCandidate] = []

    for frame_path in frames:
        all_candidates.extend(scan_frame(frame_path))

    # Sort for determinism
    all_candidates.sort(
        key=lambda c: (c.frame_path, c.node_id, c.field_name)
    )

    # Emit JSON report
    report = {
        "tool": {"id": "markup_audit", "version": "0.1.0"},
        "summary": {
            "total_frames": len(frames),
            "total_candidates": len(all_candidates),
            "by_recommendation": {},
        },
        "candidates": [asdict(c) for c in all_candidates],
    }

    # Count by recommendation
    rec_counts: Dict[str, int] = {}
    for c in all_candidates:
        base_rec = c.recommendation.split(" ")[0]  # e.g., "md-block" from "md-block (reason)"
        rec_counts[base_rec] = rec_counts.get(base_rec, 0) + 1

    report["summary"]["by_recommendation"] = rec_counts

    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Report: {out_path}")
    print(f"Total candidates: {len(all_candidates)}")
    print(f"By recommendation: {rec_counts}")

    # Emit CSV for human review
    csv_path = out_path.parent / "candidates.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "frame_path",
                "node_id",
                "node_kind",
                "field_name",
                "current_format",
                "text_length",
                "has_code_backticks",
                "has_paths",
                "has_emphasis",
                "has_references",
                "has_lists",
                "recommendation",
            ],
        )
        writer.writeheader()
        for c in all_candidates:
            writer.writerow(asdict(c))

    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
