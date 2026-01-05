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
    # Conservative escaping for plain-text fields.
    # Avoid changing unicode.
    s = s.replace("\\", "\\\\")
    s = s.replace("`", "\\`")
    s = s.replace("*", "\\*")
    s = s.replace("_", "\\_")
    s = s.replace("[", "\\[").replace("]", "\\]")
    return s


def render_inline_markup_k1(ast: Dict[str, Any]) -> str:
    # InlineMarkup-K1 blocks -> Markdown
    # We render paragraphs separated by blank lines and code fences verbatim.
    out: List[str] = []
    blocks = ast.get("blocks") or []
    for b in blocks:
        if not isinstance(b, dict):
            continue
        t = b.get("t")
        if t == "code_fence":
            lang = str(b.get("lang") or "").strip()
            code = str(b.get("code") or "")
            out.append(f"```{lang}".rstrip())
            out.extend(code.split("\n"))
            out.append("```")
            out.append("")
        elif t == "paragraph":
            out.append(render_inline_nodes_md(b.get("c") or []))
            out.append("")
        else:
            out.append(f"[unhandled:{t}]")
            out.append("")
    return "\n".join(out).rstrip("\n")


def render_inline_nodes_md(nodes: List[Dict[str, Any]]) -> str:
    out: List[str] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        t = n.get("t")
        if t == "text":
            out.append(str(n.get("s", "")))
        elif t == "emph":
            out.append("*" + render_inline_nodes_md(n.get("c") or []) + "*")
        elif t == "strong":
            out.append("**" + render_inline_nodes_md(n.get("c") or []) + "**")
        elif t == "code":
            out.append("`" + str(n.get("s", "")) + "`")
        elif t == "math":
            out.append("$" + str(n.get("s", "")) + "$")
        elif t == "link":
            out.append("[" + render_inline_nodes_md(n.get("c") or []) + "](" + str(n.get("url", "")) + ")")
        else:
            out.append(str(n.get("s", "")))
    return "".join(out)


def render_body(docir_block: Dict[str, Any], field: str) -> List[str]:
    # Prefer structured markup if present; otherwise treat as plain text.
    # field is informational (may inform escaping later).
    bm = docir_block.get("body_markup")
    if isinstance(bm, dict) and bm.get("kind") == "inline-markup-k1":
        errors = bm.get("errors") or []
        # Do not fail rendering here; validators are responsible for enforcing.
        _ = errors
        return [render_inline_markup_k1(bm), ""]

    body = md_escape(str(docir_block.get("body", "")))
    return [body, ""] if body else [""]


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
        head = f"**{label}**" + (f" _({status})_" if status else "")
        out = [head, ""]
        out.extend(render_body(b, "body"))
        return out

    if t == "clause":
        label = md_escape(str(b.get("label", "")))
        status = md_escape(str(b.get("status", "")))
        head = f"**{label}**" + (f" _({status})_" if status else "")
        out = [head, ""]
        out.extend(render_body(b, "body"))
        return out

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
