#!/usr/bin/env python3
"""Validate InlineMarkup-K1 in frames.

This is a lightweight gate that enforces:
- Disallow raw HTML-ish characters (< or >)
- Disallow block constructs in md-inline
- Ensure delimiters are balanced for supported constructs

Policy (v0.1):
- If node attrs contain text.format, validate the relevant text-like fields.
- Fields validated: text, summary, desc

NOTE (repo-local extension):
- `text.format` values `tex-inline` and `tex-block` are treated as explicit
  *passthrough* modes and are not parsed as InlineMarkup-K1.
  InlineMarkup validation is therefore skipped for those fields.

Exit codes:
- 0 if ok
- 1 if any violations

Writes:
- out/validate_inline_markup/report.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

# Ensure repo root is on sys.path so we can import tools/* as modules.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.markup.inline_markup_k1 import parse  # type: ignore


_TEX_PASSTHROUGH_FORMATS = {"tex-inline", "tex-block"}


def is_str(x: Any) -> bool:
    return isinstance(x, str) and bool(x)


def find_attr(attrs: Any, key: str) -> str | None:
    if not isinstance(attrs, list):
        return None
    for a in attrs:
        if isinstance(a, dict) and a.get("key") == key:
            v = a.get("value")
            if isinstance(v, str):
                return v
    return None


def iter_frames(root: Path) -> List[Path]:
    return sorted(root.glob("frames/**/v*/frame.yml"))


def validate_frame(path: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Return (violations, warnings)."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ([{"code": "TEXT.E.BAD_FRAME", "message": "Frame is not a mapping"}], [])

    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        return ([], [])

    violations: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    for n in nodes:
        if not isinstance(n, dict):
            continue
        nid = str(n.get("id") or "")
        fmt = find_attr(n.get("attrs"), "text.format") or "plain"

        # Opt-out for explicit TeX passthrough blocks.
        if fmt in _TEX_PASSTHROUGH_FORMATS:
            continue

        for field in ("text", "summary", "desc"):
            v = n.get(field)
            if not is_str(v):
                continue
            ast, errs = parse(v, mode=fmt)
            _ = ast
            for e in errs:
                violations.append(
                    {
                        "code": e.code,
                        "message": e.message,
                        "pos": e.pos,
                        "node": nid,
                        "field": field,
                        "format": fmt,
                    }
                )

    return (violations, warnings)


def main() -> int:
    root = Path(".").resolve()
    out_dir = root / "out" / "validate_inline_markup"
    out_dir.mkdir(parents=True, exist_ok=True)

    failures: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    for p in iter_frames(root):
        rel = p.relative_to(root).as_posix()
        try:
            v, w = validate_frame(p)
            for x in v:
                x["path"] = rel
            for x in w:
                x["path"] = rel
            failures.extend(v)
            warnings.extend(w)
        except Exception as e:
            failures.append({"code": "TEXT.E.EXCEPTION", "message": str(e), "path": rel})

    report = {
        "tool": {"id": "validate_inline_markup", "version": "0.1.0"},
        "ok": len(failures) == 0,
        "violations": failures,
        "warnings": warnings,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        # concise stderr
        print(f"validate_inline_markup: {len(failures)} violation(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
