"""Publication TeX inline IR validator (PubTeX Inline IR)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from fcx.kernel import KernelCtx
from fcx.util import read_text
from fcx.violations import Violation

try:
    from tools.markup.pub_tex_inline_v0 import parse_tex_inline_v0, to_ir  # type: ignore
except Exception:
    parse_tex_inline_v0 = None  # type: ignore
    to_ir = None  # type: ignore


PUBTEX_E = {
    "PARSE_ERROR": "PUBTEX.E.PARSE_ERROR",
    "FORBIDDEN_CONTROL_SEQ": "PUBTEX.E.FORBIDDEN_CONTROL_SEQ",
    "JSON_MALFORMED": "PUBTEX.E.JSON_MALFORMED",
}

_FORBIDDEN_TEX_RE = re.compile(r"\\(input|include|write|openout|read|usepackage|catcode|def|edef|gdef)\b")
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


def validate_pub_tex_inline_v0(ctx: KernelCtx) -> Tuple[List[Violation], List[Violation]]:
    """Validate PubTeX Inline IR in all frames.
    
    Returns (violations, warnings).
    """
    root = Path(ctx.repo_root)
    violations: List[Violation] = []
    warnings: List[Violation] = []

    for frame_path in sorted(root.glob("frames/**/v*/frame.yml")):
        rel = str(frame_path.relative_to(root))
        data = yaml.safe_load(read_text(frame_path))
        if not isinstance(data, dict):
            continue

        nodes = data.get("nodes")
        if not isinstance(nodes, list):
            continue

        for n in nodes:
            if not isinstance(n, dict):
                continue

            node_id = n.get("id")
            attrs = n.get("attrs")

            # Check for pub.tex.* attrs with format=tex-inline-v0
            for field in ["summary", "text", "body"]:
                fmt_key = f"pub.tex.{field}.format"
                fmt_val = _find_attr_value(attrs, fmt_key)

                if fmt_val != "tex-inline-v0":
                    continue

                # Must have the corresponding pub.tex.<field> attr
                val_key = f"pub.tex.{field}"
                val = _find_attr_value(attrs, val_key)
                if not val:
                    violations.append(
                        Violation(
                            code=PUBTEX_E["PARSE_ERROR"],
                            path=rel,
                            node_id=str(node_id) if node_id else None,
                            message=f"missing {val_key} with format={fmt_val}",
                        )
                    )
                    continue

                # Parse and validate
                if parse_tex_inline_v0 is None:
                    violations.append(
                        Violation(
                            code=PUBTEX_E["PARSE_ERROR"],
                            path=rel,
                            node_id=str(node_id) if node_id else None,
                            message="pub_tex_inline_v0 parser unavailable",
                        )
                    )
                    continue

                try:
                    nodes_parsed, errs = parse_tex_inline_v0(val)
                    for err in errs or []:
                        violations.append(
                            Violation(
                                code=PUBTEX_E["PARSE_ERROR"],
                                path=rel,
                                node_id=str(node_id) if node_id else None,
                                message=f"{val_key}: {err.code} at {err.pos}",
                            )
                        )
                    
                    # Validate parsed nodes for forbidden sequences
                    for seg in nodes_parsed or []:
                        if not isinstance(seg, dict):
                            continue
                        t = seg.get("t")
                        s = seg.get("s", "")
                        
                        if t == "math":
                            if _FORBIDDEN_TEX_RE.search(s):
                                violations.append(
                                    Violation(
                                        code=PUBTEX_E["FORBIDDEN_CONTROL_SEQ"],
                                        path=rel,
                                        node_id=str(node_id) if node_id else None,
                                        message=f"{val_key} math: forbidden control sequence",
                                    )
                                )
                        elif t == "code":
                            if _FORBIDDEN_CODE_RE.search(s):
                                violations.append(
                                    Violation(
                                        code=PUBTEX_E["FORBIDDEN_CONTROL_SEQ"],
                                        path=rel,
                                        node_id=str(node_id) if node_id else None,
                                        message=f"{val_key} code: forbidden backslash sequence",
                                    )
                                )
                except Exception as e:
                    violations.append(
                        Violation(
                            code=PUBTEX_E["PARSE_ERROR"],
                            path=rel,
                            node_id=str(node_id) if node_id else None,
                            message=f"{val_key}: {str(e)}",
                        )
                    )

            # Also check canonical JSON form: pub.tex.<field> with vtype=json
            for field in ["summary", "text", "body"]:
                val_key = f"pub.tex.{field}"
                ir = _find_attr_json_value(attrs, val_key)
                if not isinstance(ir, dict) or ir.get("kind") != "pub-tex-inline-v0":
                    continue

                # Validate nodes in IR
                for seg in ir.get("nodes") or []:
                    if not isinstance(seg, dict):
                        continue
                    t = seg.get("t")
                    s = seg.get("s", "")
                    
                    if t == "math" and _FORBIDDEN_TEX_RE.search(s):
                        violations.append(
                            Violation(
                                code=PUBTEX_E["FORBIDDEN_CONTROL_SEQ"],
                                path=rel,
                                node_id=str(node_id) if node_id else None,
                                message=f"{val_key} (JSON IR) math: forbidden control sequence",
                            )
                        )
                    elif t == "code" and _FORBIDDEN_CODE_RE.search(s):
                        violations.append(
                            Violation(
                                code=PUBTEX_E["FORBIDDEN_CONTROL_SEQ"],
                                path=rel,
                                node_id=str(node_id) if node_id else None,
                                message=f"{val_key} (JSON IR) code: forbidden backslash sequence",
                            )
                        )

    return violations, warnings
