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
import re
from pathlib import Path
from typing import Any, Dict, List


# Deterministic normalization for common unicode math symbols to TeX.
# This is intentionally small and conservative (repo determinism + stability).
_UNICODE_TO_TEX = {
    # Greek (uppercase)
    "Σ": r"\Sigma",
    "Π": r"\Pi",
    "Θ": r"\Theta",
    "Γ": r"\Gamma",
    "Δ": r"\Delta",
    "Λ": r"\Lambda",
    "Ω": r"\Omega",
    # Greek (lowercase)
    "β": r"\beta",
    "χ": r"\chi",
    "π": r"\pi",
    "θ": r"\theta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "λ": r"\lambda",
    "ω": r"\omega",
    # Operators / relations
    "→": r"\to",
    "↦": r"\mapsto",
    "×": r"\times",
    "∘": r"\circ",
    "≤": r"\le",
    "≥": r"\ge",
    "≼": r"\preceq",
    "⪯": r"\preceq",
    "∈": r"\in",
}

# Minimal pattern lift for R_{≥0} -> \mathbb{R}_{\ge 0}.
# Keep this tight to avoid surprising conversions.
_R_GE0_RE = re.compile(r"R_\{\s*≥\s*0\s*\}")


def normalize_tex_unicode(s: str) -> str:
    """Normalize common Unicode math glyphs into TeX macros.

    NOTE: This does not add math-mode delimiters; callers decide whether
    the string is emitted into text mode or math mode.
    """

    if not s:
        return ""

    # Specific, deterministic rewrite(s) first.
    # Use escaped backslashes in the replacement so `re` doesn't treat `\m` as an escape.
    s = _R_GE0_RE.sub(r"\\mathbb{R}_{\\ge 0}", s)

    # Character-by-character rewrite for stable behavior.
    out: List[str] = []
    for ch in s:
        rep = _UNICODE_TO_TEX.get(ch)
        if rep is None:
            out.append(ch)
        else:
            out.append(rep)
    return "".join(out)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tex_escape(s: str) -> str:
    # Minimal escaping for plain text fields.
    # IMPORTANT: do not inject TeX macros here; escaping will corrupt them.
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


def tex_escape_with_unicode_norm(s: str) -> str:
    """Escape plain text after normalizing unicode into TeX macros.

    This is ONLY safe when the resulting string is emitted into a TeX context
    that expects commands (typically math mode), or when the caller trusts that
    macros are desired.
    """

    return tex_escape(normalize_tex_unicode(s))


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
            out.append("$" + normalize_tex_unicode(str(n.get("s", ""))) + "$")
        elif t == "link":
            out.append(
                r"\href{" + tex_escape(str(n.get("url", ""))) + "}{" + render_inline_nodes_tex(n.get("c") or []) + "}"
            )
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
            # Use fancyvrb for better control and to avoid edge cases with verbatim.
            out.append(r"\begin{Verbatim}[commandchars=\\\{\},fontsize=\small]")
            out.extend(code.split("\n"))
            out.append(r"\end{Verbatim}")
            out.append("")
        elif t == "paragraph":
            out.append(render_inline_nodes_tex(b.get("c") or []))
            out.append("")
        else:
            out.append(tex_escape(f"[unhandled:{t}]"))
            out.append("")
    return out


def _render_inline_block_or_plain(value: Any) -> str:
    """Render a field that can be either plain text or InlineMarkup-K1 AST."""

    if isinstance(value, dict) and value.get("kind") == "inline-markup-k1":
        # InlineMarkup-K1 may produce multiple paragraphs; join with newlines.
        return "\n".join(render_inline_markup_k1_tex(value)).rstrip("\n")
    if isinstance(value, str):
        return tex_escape(value)
    return ""


def render_body_tex(b: Dict[str, Any]) -> List[str]:
    bm = b.get("body_markup")
    if isinstance(bm, dict) and bm.get("kind") == "inline-markup-k1":
        return render_inline_markup_k1_tex(bm)

    body = str(b.get("body", "")).strip()
    return [tex_escape(body), ""] if body else [""]


def render_preamble(title: str) -> List[str]:
    # Title should be treated as plain text (no TeX macro injection).
    t = tex_escape(title or "Document")
    return [
        r"\documentclass[11pt]{article}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{hyperref}",
        r"\usepackage{geometry}",
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}",
        r"\usepackage{fancyvrb}",
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

        # Optional property body text (often present when symbols need context).
        body_markup = b.get("body_markup")
        body = str(b.get("body", "")).strip()
        if (isinstance(body_markup, dict) and body_markup.get("kind") == "inline-markup-k1") or body:
            out.extend(render_body_tex(b))

        symbols = b.get("symbols") or []
        if symbols:
            out.append(r"\begin{itemize}")
            for s in symbols:
                sym_raw = str(s.get("sym", ""))
                sym_math = normalize_tex_unicode(sym_raw)

                # Prefer markup-aware descriptions when present.
                desc_rendered = _render_inline_block_or_plain(s.get("desc_markup") or s.get("desc"))
                if sym_math:
                    out.append(rf"  \item \({sym_math}\): {desc_rendered}")
                else:
                    out.append(rf"  \item {desc_rendered}")
            out.append(r"\end{itemize}")
            out.append("")
        return out

    if t == "math_block":
        # DocIR may emit display math explicitly.
        expr = normalize_tex_unicode(str(b.get("text", "") or b.get("expr", "") or "").strip())
        if not expr:
            return [""]
        return [r"\[", expr, r"\]", ""]

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
    skipped_title_heading = False

    for b in docir.get("blocks", []):
        if not isinstance(b, dict):
            continue

        # Avoid duplicate top-level heading:
        # DocIR commonly emits a first level-1 heading that equals the document title,
        # but we already render `\title{...}` + `\maketitle` in the preamble.
        if not skipped_title_heading and b.get("type") == "heading":
            try:
                level = int(b.get("level", 1))
            except Exception:
                level = 1
            if level <= 1:
                htitle = str(b.get("title", ""))
                if title and htitle.strip() == title.strip():
                    skipped_title_heading = True
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
