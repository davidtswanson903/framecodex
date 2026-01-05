"""InlineMarkup-K1 validator (deterministic, policy-driven)."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from fcx.kernel import KernelCtx
from fcx.util import read_text
from fcx.violations import Violation

try:
    from tools.markup.inline_markup_k1 import parse as parse_inline_markup  # type: ignore
except Exception:
    parse_inline_markup = None  # type: ignore


TEXT_E = {
    "HTML_DISALLOWED": "TEXT.E.HTML_DISALLOWED",
    "BAD_TEXT_FORMAT": "TEXT.E.BAD_TEXT_FORMAT",
    "BAD_CODEFENCE": "TEXT.E.BAD_CODEFENCE",
}

_TEX_PASSTHROUGH_FORMATS = {"tex-inline", "tex-block"}


def _is_str(x: Any) -> bool:
    return isinstance(x, str) and bool(x)


def _find_attr(attrs: Any, key: str) -> Optional[str]:
    if not isinstance(attrs, list):
        return None
    for a in attrs:
        if isinstance(a, dict) and a.get("key") == key:
            v = a.get("value")
            if isinstance(v, str):
                return v
    return None


def _iter_frames(root: Path) -> List[Path]:
    return sorted(root.glob("frames/**/v*/frame.yml"))


def validate_inline_markup_k1(ctx: KernelCtx) -> Tuple[List[Violation], List[Violation]]:
    """Validate InlineMarkup-K1 in all frames.
    
    Returns (violations, warnings).
    """
    root = Path(ctx.repo_root)
    violations: List[Violation] = []
    warnings: List[Violation] = []

    for frame_path in _iter_frames(root):
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
            text_format = _find_attr(attrs, "text.format")

            if text_format in _TEX_PASSTHROUGH_FORMATS:
                # Skip: TeX passthrough is intentional bypass
                continue

            if not text_format:
                # No explicit format; default is plain (no markup validation)
                continue

            if text_format not in ("plain", "md-inline", "md-block"):
                violations.append(
                    Violation(
                        code=TEXT_E["BAD_TEXT_FORMAT"],
                        path=rel,
                        node_id=str(node_id) if node_id else None,
                        message=f"unknown text.format: {text_format}",
                    )
                )
                continue

            # Validate text fields per format
            for field in ["text", "summary", "desc"]:
                value = n.get(field)
                if not _is_str(value):
                    continue

                # HTML check (basic: look for < or > outside inline code)
                if re.search(r'<(?!.*>.*[`])|>(?!.*[`].*)', value):
                    violations.append(
                        Violation(
                            code=TEXT_E["HTML_DISALLOWED"],
                            path=rel,
                            node_id=str(node_id) if node_id else None,
                            message=f"raw HTML-like characters in {field}",
                        )
                    )

                # If parse_inline_markup available, parse for errors
                if parse_inline_markup and text_format.startswith("md-"):
                    try:
                        ast, errs = parse_inline_markup(value, mode=text_format)
                        for err in errs or []:
                            violations.append(
                                Violation(
                                    code=TEXT_E["BAD_CODEFENCE"] if "fence" in str(err.code) else TEXT_E["BAD_TEXT_FORMAT"],
                                    path=rel,
                                    node_id=str(node_id) if node_id else None,
                                    message=f"{field}: {err.code} at {err.pos}",
                                )
                            )
                    except Exception as e:
                        violations.append(
                            Violation(
                                code=TEXT_E["BAD_TEXT_FORMAT"],
                                path=rel,
                                node_id=str(node_id) if node_id else None,
                                message=f"{field} parse error: {str(e)}",
                            )
                        )

    return violations, warnings
