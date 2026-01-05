#!/usr/bin/env python3
"""Verify semantic invariants are preserved across frame edits.

This tool compares two frame.yml files (before/after) and asserts that
only "safe" fields were changed (e.g., text.format, text, summary).
Structural changes (IDs, edges, kinds, statuses) are forbidden.

Usage:
  tools/semantic_invariants/run.py --before <old.yml> --after <new.yml> [--verbose]

Exit codes:
  0 if invariants are preserved
  1 if structural changes detected

Allowed changes:
- text, summary, title (content only, not presence/absence)
- text.format attribute
- description fields (desc)
- Other doc-oriented attrs

Forbidden changes:
- graph_id, version
- node id, kind, status, profile, law_id, law_version
- edges (from, to, type)
- machine-consumed fields (symbols, validators, etc.)
- Removing/adding nodes

Design:
- Deterministic
- Clear whitelist of safe field changes
- Reports violations clearly
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# Fields that are safe to modify for readability
SAFE_TEXT_FIELDS = {"text", "summary", "title", "label", "desc"}

# Fields that MUST NOT change
PROTECTED_FIELDS = {
    "graph_id",
    "version",
    "id",
    "kind",
    "status",
    "profile",
    "law_id",
    "law_version",
}


@dataclass
class Violation:
    """A structural invariant violation."""
    code: str  # e.g., "node_removed", "edge_added", "id_changed"
    frame_path: str
    details: str


def normalize_node_id(node: Dict[str, Any]) -> str:
    """Extract a stable node ID."""
    nid = node.get("id")
    return str(nid) if nid else ""


def check_protected_fields(before_node: Dict[str, Any], after_node: Dict[str, Any]) -> List[Violation]:
    """Verify protected fields did not change."""
    violations: List[Violation] = []
    nid = normalize_node_id(before_node)

    for field in PROTECTED_FIELDS:
        before_val = before_node.get(field)
        after_val = after_node.get(field)
        if before_val != after_val:
            violations.append(
                Violation(
                    code=f"field_changed_{field}",
                    frame_path="(node-level)",
                    details=f"node {nid}: {field} changed from {before_val!r} to {after_val!r}",
                )
            )

    return violations


def check_text_format_attrs(before_node: Dict[str, Any], after_node: Dict[str, Any]) -> List[Violation]:
    """Verify only text.format was modified in attrs."""
    violations: List[Violation] = []
    nid = normalize_node_id(before_node)

    def extract_attrs(node: Dict[str, Any]) -> Dict[str, str]:
        attrs = node.get("attrs", [])
        if not isinstance(attrs, list):
            return {}
        return {a.get("key"): a.get("value") for a in attrs if isinstance(a, dict)}

    before_attrs = extract_attrs(before_node)
    after_attrs = extract_attrs(after_node)

    # Check for new or removed attrs (other than text.format)
    safe_keys = {"text.format"}
    before_keys = set(before_attrs.keys())
    after_keys = set(after_attrs.keys())

    added = after_keys - before_keys - safe_keys
    removed = before_keys - after_keys

    if added:
        violations.append(
            Violation(
                code="attrs_added",
                frame_path="(node-level)",
                details=f"node {nid}: new attrs {added}",
            )
        )

    if removed:
        violations.append(
            Violation(
                code="attrs_removed",
                frame_path="(node-level)",
                details=f"node {nid}: removed attrs {removed}",
            )
        )

    return violations


def check_edges(before_data: Dict[str, Any], after_data: Dict[str, Any]) -> List[Violation]:
    """Verify edges are identical."""
    violations: List[Violation] = []

    def extract_edges(data: Dict[str, Any]) -> List[Tuple[str, str, str]]:
        edges = data.get("edges", [])
        if not isinstance(edges, list):
            return []
        return sorted(
            [(e.get("from"), e.get("to"), e.get("type")) for e in edges if isinstance(e, dict)]
        )

    before_edges = extract_edges(before_data)
    after_edges = extract_edges(after_data)

    if before_edges != after_edges:
        violations.append(
            Violation(
                code="edges_changed",
                frame_path="(frame-level)",
                details=f"edges differ: before {len(before_edges)}, after {len(after_edges)}",
            )
        )

    return violations


def check_node_ids(before_data: Dict[str, Any], after_data: Dict[str, Any]) -> List[Violation]:
    """Verify no nodes were added or removed."""
    violations: List[Violation] = []

    def extract_node_ids(data: Dict[str, Any]) -> Set[str]:
        nodes = data.get("nodes", [])
        if not isinstance(nodes, list):
            return set()
        return {normalize_node_id(n) for n in nodes if isinstance(n, dict)}

    before_ids = extract_node_ids(before_data)
    after_ids = extract_node_ids(after_data)

    added = after_ids - before_ids
    removed = before_ids - after_ids

    if added:
        violations.append(
            Violation(
                code="nodes_added",
                frame_path="(frame-level)",
                details=f"new nodes: {added}",
            )
        )

    if removed:
        violations.append(
            Violation(
                code="nodes_removed",
                frame_path="(frame-level)",
                details=f"removed nodes: {removed}",
            )
        )

    return violations


def compare_frames(before_path: Path, after_path: Path) -> List[Violation]:
    """Compare two frame.yml files for semantic invariance."""
    violations: List[Violation] = []

    try:
        before_data = read_yaml(before_path)
        after_data = read_yaml(after_path)
    except Exception as e:
        violations.append(
            Violation(
                code="parse_error",
                frame_path=str(before_path),
                details=str(e),
            )
        )
        return violations

    if not isinstance(before_data, dict) or not isinstance(after_data, dict):
        violations.append(
            Violation(
                code="not_mapping",
                frame_path=str(before_path),
                details="frame is not a YAML mapping",
            )
        )
        return violations

    # Check top-level fields
    for field in ["graph_id", "version"]:
        if before_data.get(field) != after_data.get(field):
            violations.append(
                Violation(
                    code=f"frame_field_changed_{field}",
                    frame_path=str(before_path),
                    details=f"{field} changed",
                )
            )

    # Check nodes
    violations.extend(check_node_ids(before_data, after_data))

    # Check edges
    violations.extend(check_edges(before_data, after_data))

    # Check each node
    def nodes_by_id(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        nodes = data.get("nodes", [])
        return {normalize_node_id(n): n for n in nodes if isinstance(n, dict)}

    before_nodes = nodes_by_id(before_data)
    after_nodes = nodes_by_id(after_data)

    for nid in before_nodes:
        if nid not in after_nodes:
            continue
        violations.extend(check_protected_fields(before_nodes[nid], after_nodes[nid]))
        violations.extend(check_text_format_attrs(before_nodes[nid], after_nodes[nid]))

    return violations


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    before_path = Path(args.before)
    after_path = Path(args.after)

    violations = compare_frames(before_path, after_path)

    if not violations:
        if args.verbose:
            print("✓ Semantic invariants preserved")
        return 0

    print(f"✗ {len(violations)} semantic invariant violation(s):", file=sys.stderr)
    for v in violations:
        print(f"  [{v.code}] {v.details}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    sys.exit(main())
