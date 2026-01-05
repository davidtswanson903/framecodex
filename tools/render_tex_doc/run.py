#!/usr/bin/env python3
"""Render DocIR JSON to a deterministic LaTeX bundle.

Outputs a directory containing:
- main.tex

Usage:
  tools/render_tex_doc/run.py --in <docir.json> --out-dir <latex_dir>

Notes:
- Pure pretty-printer over DocIR.
- Designed to be consumed by tools/pub_build_pdf/run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tex_escape(s: str) -> str:
    # Minimal escaping for plain text fields.
    return (
        s.replace("\\", r"\textbackslash{}")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("$", r"\$")
        .replace("&", r"\&")
        .replace("#", r"\#")
        .replace("%", r"\%")
        .replace("_", r"\_")
        .replace("~", r"\textasciitilde{}")
        .replace("^", r"\textasciicircum{}")
    )


def render_inline_nodes_tex(nodes: List[Dict[str, Any]]) -> str:
    out: List[str] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        t = n.get("t")
        if t == "text":
            out.append(tex_escape(str(n.get("s", ""))))
        elif t == "emph":
            out.append(r"\emph{" + render_inline_nodes_tex(n.get("c") or []) + "}")
        elif t == "strong":
            out.append(r"\textbf{" + render_inline_nodes_tex(n.get("c") or []) + "}")
        elif t == "code":
            out.append(r"\texttt{" + tex_escape(str(n.get("s", ""))) + "}")
        elif t == "math":
            out.append("$" + str(n.get("s", "")) + "$")
        elif t == "link":
            out.append(r"\href{" + tex_escape(str(n.get("url", ""))) + "}{" + render_inline_nodes_tex(n.get("c") or []) + "}")
        else:
            out.append(tex_escape(str(n.get("s", ""))))
    return "".join(out)


def render_inline_markup_k1_tex(ast: Dict[str, Any]) -> List[str]:
    out: List[str] = []
    blocks = ast.get("blocks") or []
    for b in blocks:
        if not isinstance(b, dict):
            continue
        t = b.get("t")
        if t == "code_fence":
            code = str(b.get("code") or "")
            out.append(r"\begin{verbatim}")
            out.extend(code.split("\n"))
            out.append(r"\end{verbatim}")
            out.append("")
        elif t == "paragraph":
            out.append(render_inline_nodes_tex(b.get("c") or []))
            out.append("")
        else:
            out.append(tex_escape(f"[unhandled:{t}]"))
            out.append("")
    return out


def render_body_tex(b: Dict[str, Any]) -> List[str]:
    bm = b.get("body_markup")
    if isinstance(bm, dict) and bm.get("kind") == "inline-markup-k1":
        return render_inline_markup_k1_tex(bm)

    body = str(b.get("body", "")).strip()
    return [tex_escape(body), ""] if body else [""]


def render_preamble(title: str) -> List[str]:
    t = tex_escape(title or "Document")
    return [
        r"\documentclass[11pt]{article}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{hyperref}",
        r"\usepackage{geometry}",
        r"\geometry{margin=1in}",
        "",
        rf"\title{{{t}}}",
        r"\author{}",
        r"\date{}",
        "",
        r"\begin{document}",
        r"\maketitle",
        "",
    ]


def render_block(b: Dict[str, Any]) -> List[str]:
    t = b.get("type")

    if t == "heading":
        level = int(b.get("level", 1))
        title = tex_escape(str(b.get("title", "")))
        if level <= 1:
            return [rf"\section*{{{title}}}", ""]
        if level == 2:
            return [rf"\subsection*{{{title}}}", ""]
        if level == 3:
            return [rf"\subsubsection*{{{title}}}", ""]
        return [rf"\paragraph*{{{title}}}", ""]

    if t == "paragraph":
        bm = b.get("body_markup")
        if isinstance(bm, dict) and bm.get("kind") == "inline-markup-k1":
            return render_inline_markup_k1_tex(bm)
        txt = str(b.get("text", "")).strip()
        return [tex_escape(txt), ""] if txt else [""]

    if t in ("definition", "clause"):
        label = tex_escape(str(b.get("label", "")))
        status = tex_escape(str(b.get("status", "")))
        head = rf"\textbf{{{label}}}" + (rf" \emph{{({status})}}" if status else "")
        out: List[str] = [head, ""]
        out.extend(render_body_tex(b))
        return out

    if t == "property":
        label = tex_escape(str(b.get("label", "")))
        status = tex_escape(str(b.get("status", "")))
        head = rf"\textbf{{{label}}}" + (rf" \emph{{({status})}}" if status else "")
        out: List[str] = [head, ""]
        symbols = b.get("symbols") or []
        if symbols:
            out.append(r"\begin{itemize}")
            for s in symbols:
                sym = tex_escape(str(s.get("sym", "")))
                desc = tex_escape(str(s.get("desc", "")))
                out.append(rf"  \item \texttt{{{sym}}}: {desc}")
            out.append(r"\end{itemize}")
            out.append("")
        return out

    if t == "list_item":
        txt = tex_escape(str(b.get("text", "")))
        return [rf"\item {txt}"]

    if t == "note":
        kind = tex_escape(str(b.get("kind", "note")))
        txt = tex_escape(str(b.get("text", "")))
        return [rf"\begin{{quote}}\textbf{{{kind}}}: {txt}\end{{quote}}", ""]

    return [
        rf"\begin{{quote}}\textbf{{unhandled block}}: {tex_escape(str(t))}\end{{quote}}",
        "",
    ]


def render_tex(docir: Dict[str, Any]) -> str:
    fm = docir.get("front_matter", {})
    title = str(fm.get("title", ""))

    lines: List[str] = []
    lines.extend(render_preamble(title))

    in_itemize = False
    for b in docir.get("blocks", []):
        if not isinstance(b, dict):
            continue

        # Ensure list items are wrapped in an itemize.
        if b.get("type") == "list_item" and not in_itemize:
            lines.append(r"\begin{itemize}")
            in_itemize = True

        if b.get("type") != "list_item" and in_itemize:
            lines.append(r"\end{itemize}")
            lines.append("")
            in_itemize = False

        lines.extend(render_block(b))

    if in_itemize:
        lines.append(r"\end{itemize}")
        lines.append("")

    lines.append(r"\end{document}")

    # Deterministic whitespace.
    return "\n".join(ln.rstrip() for ln in lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True)
    ap.add_argument("--out-dir", dest="out_dir", required=True)
    args = ap.parse_args()

    in_path = Path(args.in_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    docir = read_json(in_path)
    (out_dir / "main.tex").write_text(render_tex(docir), encoding="utf-8")


if __name__ == "__main__":
    main()
