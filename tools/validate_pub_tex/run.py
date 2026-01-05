#!/usr/bin/env python3
"""Validate publication TeX inline IR (PubTeX Inline IR).

This gate enforces deterministic, safe publication inline TeX usage.

Inputs:
- frames/**/v*/frame.yml

Validates:
- JSON IR attrs: pub.tex.{text,summary,body} where vtype=json and kind=pub-tex-inline-v0
- Authoring shortcut: pub.tex.<field>.format == tex-inline-v0 with pub.tex.<field> as a string

Policy (v0):
- Parsing errors are violations.
- Math segments forbid obvious raw-TeX injection control sequences.
- Code segments forbid backslash control sequences (conservative).

Writes:
- out/validate_pub_tex/report.json

Exit codes:
- 0 if ok
- 1 if any violations
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Ensure repo root is on sys.path so we can import tools/* as modules.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.markup.pub_tex_inline_v0 import parse_tex_inline_v0, to_ir  # type: ignore


_FORBIDDEN_TEX_RE = re.compile(r"\\(input|include|write|openout|read|usepackage|catcode|def|edef|gdef)\b")
# Extra-conservative for code spans: disallow any backslash control sequence.
_FORBIDDEN_CODE_RE = re.compile(r"\\[A-Za-z@]+")


def _is_str(x: Any) -> bool:
    return isinstance(x, str)


def _find_attr(raw_attrs: Any, key: str) -> Optional[Dict[str, Any]]:
    if not isinstance(raw_attrs, list):
        return None
    for a in raw_attrs:
        if isinstance(a, dict) and a.get("key") == key:
            return a
    return None


def _find_attr_value(raw_attrs: Any, key: str) -> Optional[str]:
    a = _find_attr(raw_attrs, key)
    if not isinstance(a, dict):
        return None
    v = a.get("value")
    return v if isinstance(v, str) else None


def _find_attr_json_value(raw_attrs: Any, key: str) -> Optional[Any]:
    a = _find_attr(raw_attrs, key)
    if not isinstance(a, dict):
        return None
    v = a.get("value")
    if not isinstance(v, str):
        return None
    try:
        return json.loads(v)
    except Exception:
        return None


def _validate_ir(ir: Dict[str, Any], *, path: str, node_id: str, field: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if not isinstance(ir, dict) or ir.get("kind") != "pub-tex-inline-v0":
        violations.append(
            {
                "code": "PUBTEX.E.BAD_IR",
                "path": path,
                "node_id": node_id,
                "field": field,
                "message": "pub.tex IR must be kind=pub-tex-inline-v0",
            }
        )
        return violations

    nodes = ir.get("nodes")
    if not isinstance(nodes, list):
        violations.append(
            {
                "code": "PUBTEX.E.BAD_IR",
                "path": path,
                "node_id": node_id,
                "field": field,
                "message": "pub.tex IR must have nodes: [...]",
            }
        )
        return violations

    for idx, n in enumerate(nodes):
        if not isinstance(n, dict):
            continue
        t = n.get("t")
        s = n.get("s")
        if t == "math" and isinstance(s, str) and _FORBIDDEN_TEX_RE.search(s):
            violations.append(
                {
                    "code": "PUBTEX.E.FORBIDDEN_TEX",
                    "path": path,
                    "node_id": node_id,
                    "field": field,
                    "index": idx,
                    "message": "forbidden TeX control sequence in math segment",
                }
            )
        if t == "code" and isinstance(s, str) and _FORBIDDEN_CODE_RE.search(s):
            violations.append(
                {
                    "code": "PUBTEX.E.FORBIDDEN_CODE",
                    "path": path,
                    "node_id": node_id,
                    "field": field,
                    "index": idx,
                    "message": "forbidden backslash control sequence in code segment",
                }
            )
    return violations


def _compile_from_format(raw_attrs: Any, *, path: str, node_id: str, field: str) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    fmt = _find_attr_value(raw_attrs, f"pub.tex.{field}.format")
    if fmt != "tex-inline-v0":
        return None, []

    raw = _find_attr_value(raw_attrs, f"pub.tex.{field}")
    if raw is None:
        return None, [
            {
                "code": "PUBTEX.E.MISSING",
                "path": path,
                "node_id": node_id,
                "field": field,
                "message": f"pub.tex.{field}.format is set but pub.tex.{field} is missing",
            }
        ]

    nodes, errs = parse_tex_inline_v0(raw)
    violations: List[Dict[str, Any]] = []
    for e in errs:
        violations.append(
            {
                "code": e.code,
                "path": path,
                "node_id": node_id,
                "field": field,
                "pos": e.pos,
                "message": e.message,
            }
        )

    ir = to_ir(nodes)
    violations.extend(_validate_ir(ir, path=path, node_id=node_id, field=field))
    return ir, violations


def main() -> int:
    root = Path(".").resolve()
    frames = sorted(root.glob("frames/**/v*/frame.yml"))

    failures: List[Dict[str, Any]] = []

    for p in frames:
        rel = p.relative_to(root).as_posix()
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        nodes = data.get("nodes")
        if not isinstance(nodes, list):
            continue

        for n in nodes:
            if not isinstance(n, dict):
                continue
            nid = str(n.get("id") or "")
            raw_attrs = n.get("attrs")
            for field in ("text", "summary", "body"):
                # JSON IR form
                ir = _find_attr_json_value(raw_attrs, f"pub.tex.{field}")
                if isinstance(ir, dict):
                    failures.extend(_validate_ir(ir, path=rel, node_id=nid, field=field))
                    continue

                # Authoring shortcut form
                _, v = _compile_from_format(raw_attrs, path=rel, node_id=nid, field=field)
                failures.extend(v)

    out_dir = root / "out" / "validate_pub_tex"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "tool": {"id": "validate_pub_tex", "version": "0.1.0"},
        "ok": len(failures) == 0,
        "violations": failures,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        for f in failures[:50]:
            print(f"ERROR {f.get('code')}: {f.get('path')} {f.get('node_id')} {f.get('field')} - {f.get('message')}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
