#!/usr/bin/env python3
"""Render DocIR JSON to a deterministic LaTeX bundle using PubTeX Inline IR.

This renderer is intended for publication-grade TeX output.

Key idea (Option A): frames may attach a publication-specific inline IR via attrs
(e.g. `pub.tex.summary`, `pub.tex.text`) that is carried into DocIR as
`pub_tex_inline` and preferred over InlineMarkup-K1.

TeX passthrough (opt-in):
- If a DocIR block has `text_format == 'tex-inline'` or `text_format == 'tex-block'`,
  the corresponding string payload is emitted **verbatim** (no escaping).
- This is intentionally unsafe unless paired with a dedicated validator gate.
  For now we keep this mode opt-in and leave enforcement to future tooling.

Input:
- DocIR JSON (tools/render_docir/run.py output)

Output:
- a directory containing `main.tex`

Determinism:
- stable ordering (comes from DocIR)
- no timestamps
- conservative escaping (except for explicit tex-* passthrough)

Security/safety:
- PubTeX IR is treated as *data*, not raw TeX injection. We only accept a
  constrained set of inline nodes.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


# Minimal TeX escaping for text segments.
_LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex_escape(s: str) -> str:
    return "".join(_LATEX_SPECIALS.get(ch, ch) for ch in s)


# Strongly disallow obvious raw-TeX injection in math strings.
# (This is intentionally conservative; expand only with policy.)
_FORBIDDEN_TEX_RE = re.compile(r"\\(input|include|write|openout|read|usepackage|catcode|def|edef|gdef)\b")

# Extra-conservative for code spans: disallow any backslash control sequence.
_FORBIDDEN_CODE_RE = re.compile(r"\\[A-Za-z@]+")


def validate_math_tex(s: str) -> None:
    if _FORBIDDEN_TEX_RE.search(s or ""):
        raise ValueError("PubTeXIR: forbidden control sequence in math segment")


def validate_code_tex(s: str) -> None:
    if _FORBIDDEN_CODE_RE.search(s or ""):
        raise ValueError("PubTeXIR: forbidden control sequence in code segment")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_tex_passthrough(text_format: Any) -> bool:
    return text_format in ("tex-inline", "tex-block")


def _read_passthrough_block_text(b: Dict[str, Any]) -> str:
    """Pick the correct string payload for passthrough blocks."""

    # DocIR uses:
    # - paragraph: `text`
    # - clause/definition: `body`
    # Keep this deterministic and explicit.
    t = b.get("type")
    if t == "paragraph":
        return str(b.get("text", ""))
    if t in ("clause", "definition"):
        return str(b.get("body", ""))
    return str(b.get("text", "") or b.get("body", ""))


def render_tex_inline(nodes: List[Dict[str, Any]]) -> str:
    """Render constrained publication inline nodes."""

    out: List[str] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        t = n.get("t")
        if t == "text":
            out.append(tex_escape(str(n.get("s", ""))))
        elif t == "math":
            s = str(n.get("s", ""))
            validate_math_tex(s)
            out.append(r"\\(" + s + r"\\)")
        elif t == "code":
            # Inline code (not block). Keep it simple and deterministic.
            s = str(n.get("s", ""))
            validate_code_tex(s)
            out.append(r"\\texttt{" + tex_escape(s) + "}")
        elif t == "strong":
            out.append(r"\textbf{" + render_tex_inline(n.get("c") or []) + "}")
        elif t == "emph":
            out.append(r"\emph{" + render_tex_inline(n.get("c") or []) + "}")
        elif t == "link":
            url = tex_escape(str(n.get("url", "")))
            label = render_tex_inline(n.get("c") or [])
            out.append(r"\href{" + url + "}{" + label + "}")
        else:
            # Unknown nodes are rendered as escaped text for robustness.
            out.append(tex_escape(str(n.get("s", ""))))
    return "".join(out)


def render_preamble(title: str) -> List[str]:
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
        if _is_tex_passthrough(b.get("text_format")):
            raw = _read_passthrough_block_text(b).rstrip()
            return [raw, ""] if raw else [""]

        pub = b.get("pub_tex_inline")
        if isinstance(pub, dict) and pub.get("kind") == "pub-tex-inline-v0":
            return [render_tex_inline(pub.get("nodes") or []), ""]
        txt = str(b.get("text", "")).strip()
        return [tex_escape(txt), ""] if txt else [""]

    if t in ("definition", "clause"):
        label = tex_escape(str(b.get("label", "")))
        status = tex_escape(str(b.get("status", "")))
        head = rf"\textbf{{{label}}}" + (rf" \emph{{({status})}}" if status else "")
        out: List[str] = [head, ""]

        if _is_tex_passthrough(b.get("text_format")):
            raw = _read_passthrough_block_text(b).rstrip()
            out.extend([raw, ""] if raw else [""])
            return out

        pub = b.get("pub_tex_inline")
        if isinstance(pub, dict) and pub.get("kind") == "pub-tex-inline-v0":
            out.append(render_tex_inline(pub.get("nodes") or []))
            out.append("")
            return out

        body = str(b.get("body", "")).strip()
        out.extend([tex_escape(body), ""] if body else [""])
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
                if sym:
                    out.append(rf"  \item \({sym}\): {desc}")
                else:
                    out.append(rf"  \item {desc}")
            out.append(r"\end{itemize}")
            out.append("")
        return out

    if t == "list_item":
        return [r"\item " + tex_escape(str(b.get("text", "")))]

    return [rf"\begin{{quote}}\textbf{{unhandled block}}: {tex_escape(str(t))}\end{{quote}}", ""]


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
