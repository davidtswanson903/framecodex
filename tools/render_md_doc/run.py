#!/usr/bin/env python3
"""Render DocIR JSON to deterministic Markdown.

Usage:
  tools/render_md_doc/run.py --in <docir.json> --out <doc.md>

Notes:
- This is a pure pretty-printer over DocIR.
- Deterministic ordering comes from DocIR (already ordered blocks).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def md_escape(s: str) -> str:
    # Keep it simple; avoid changing unicode.
    return s


def render_block(b: Dict[str, Any]) -> List[str]:
    t = b.get("type")
    if t == "heading":
        level = int(b.get("level", 1))
        title = md_escape(str(b.get("title", "")))
        anchor = str(b.get("anchor", ""))
        # GitHub MD headings autogenerate ids; keep explicit anchor as HTML.
        out = [f"{'#' * max(1, min(6, level))} {title}"]
        if anchor:
            out.append(f"<a id=\"{anchor}\"></a>")
        out.append("")
        return out

    if t == "paragraph":
        txt = md_escape(str(b.get("text", "")))
        return [txt, ""] if txt else [""]

    if t == "definition":
        label = md_escape(str(b.get("label", "")))
        status = md_escape(str(b.get("status", "")))
        body = md_escape(str(b.get("body", "")))
        head = f"**{label}**" + (f" _({status})_" if status else "")
        return [head, "", body, ""] if body else [head, ""]

    if t == "clause":
        label = md_escape(str(b.get("label", "")))
        status = md_escape(str(b.get("status", "")))
        body = md_escape(str(b.get("body", "")))
        head = f"**{label}**" + (f" _({status})_" if status else "")
        return [head, "", body, ""] if body else [head, ""]

    if t == "property":
        label = md_escape(str(b.get("label", "")))
        status = md_escape(str(b.get("status", "")))
        symbols = b.get("symbols") or []
        head = f"**{label}**" + (f" _({status})_" if status else "")
        out = [head, ""]
        if symbols:
            for s in symbols:
                sym = md_escape(str(s.get("sym", "")))
                desc = md_escape(str(s.get("desc", "")))
                out.append(f"- `{sym}`: {desc}")
            out.append("")
        return out

    if t == "list_item":
        txt = md_escape(str(b.get("text", "")))
        return [f"- {txt}"]

    if t == "note":
        kind = md_escape(str(b.get("kind", "note")))
        txt = md_escape(str(b.get("text", "")))
        return [f"> **{kind}**: {txt}", ""]

    return [f"> **unhandled block**: `{t}`", ""]


def render(docir: Dict[str, Any]) -> str:
    lines: List[str] = []

    fm = docir.get("front_matter", {})
    title = str(fm.get("title", ""))
    if title:
        pass  # first heading block should already contain it

    for b in docir.get("blocks", []):
        if not isinstance(b, dict):
            continue
        lines.extend(render_block(b))

    # Normalize trailing whitespace and ensure newline at EOF.
    out = "\n".join(ln.rstrip() for ln in lines).rstrip() + "\n"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True)
    ap.add_argument("--out", dest="out_path", required=True)
    args = ap.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    docir = read_json(in_path)
    out_path.write_text(render(docir), encoding="utf-8")


if __name__ == "__main__":
    main()
