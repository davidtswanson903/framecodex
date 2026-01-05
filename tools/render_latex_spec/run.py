#!/usr/bin/env python3
"""Deterministically render a SpecFrame K1 'spec' node into a single LaTeX file.

This is intentionally minimal: it emits a self-contained 'main.tex' using stable ordering
(section order, then contains edges) and stable escaping.

Usage:
  tools/render_latex_spec/run.py --in <frame.yml> --out <dir>

Outputs:
  <out>/main.tex

Notes:
  - No timestamps are written inside the LaTeX source (determinism).
  - This renderer supports the node kinds used by SpecFrame K1 in this repo:
    section, clause, term, property, spec_ref.
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


_LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "#": r"\#",
    "%": r"\%",
    "&": r"\&",
    "_": r"\_",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
}


def latex_escape(text: str) -> str:
    # Preserve unicode math-ish symbols (Σ, χ, ⪯, →, ×). Escape only LaTeX specials.
    return "".join(_LATEX_SPECIALS.get(ch, ch) for ch in text)


def norm_ws(s: str) -> str:
    # Keep text blocks readable; avoid trailing whitespace churn.
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in s.split("\n")).strip("\n")


def load_frame(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    status: str
    title: Optional[str] = None
    label: Optional[str] = None
    order: Optional[int] = None
    text: Optional[str] = None
    summary: Optional[str] = None
    symbols: Optional[List[Dict[str, str]]] = None
    target_graph_id: Optional[str] = None


def parse_nodes(g: Dict[str, Any]) -> Dict[str, Node]:
    out: Dict[str, Node] = {}
    for raw in g.get("nodes", []):
        out[raw["id"]] = Node(
            id=raw["id"],
            kind=raw.get("kind", ""),
            status=raw.get("status", ""),
            title=raw.get("title"),
            label=raw.get("label"),
            order=raw.get("order"),
            text=raw.get("text"),
            summary=raw.get("summary"),
            symbols=raw.get("symbols"),
            target_graph_id=raw.get("target_graph_id"),
        )
    return out


def contains_children(edges: List[Dict[str, Any]], parent_id: str) -> List[str]:
    kids = [e["to"] for e in edges if e.get("type") == "contains" and e.get("from") == parent_id]
    return sorted(kids)


def get_sections(nodes: Dict[str, Node]) -> List[Node]:
    secs = [n for n in nodes.values() if n.kind == "section"]
    # stable order: by explicit order, then id
    secs.sort(key=lambda n: (n.order if n.order is not None else 10**9, n.id))
    return secs


def render_property(n: Node) -> str:
    lines: List[str] = []
    heading = n.label or n.id
    lines.append(r"\subsection*{" + latex_escape(heading) + "}")
    if n.symbols:
        lines.append(r"\begin{itemize}")
        for sym in n.symbols:
            s = latex_escape(sym.get("sym", ""))
            d = latex_escape(sym.get("desc", ""))
            lines.append(r"  \item " + s + ": " + d)
        lines.append(r"\end{itemize}")
    return "\n".join(lines)


def render_term(n: Node) -> str:
    heading = n.label or n.id
    body = latex_escape(norm_ws(n.summary or ""))
    return "\n".join(
        [
            r"\subsection*{" + latex_escape(heading) + "}",
            body,
        ]
    )


def render_clause(n: Node) -> str:
    heading = n.label or n.id
    body = latex_escape(norm_ws(n.text or ""))
    return "\n".join(
        [
            r"\subsection*{" + latex_escape(heading) + "}",
            body,
        ]
    )


def render_spec_ref(n: Node) -> str:
    label = n.label or n.id
    tgt = n.target_graph_id or ""
    return r"\item " + latex_escape(label) + " (" + latex_escape(tgt) + ")"


def render(g: Dict[str, Any]) -> str:
    nodes = parse_nodes(g)
    edges = g.get("edges", [])

    root_id = g.get("graph_id")
    root = nodes.get(root_id)
    if root is None:
        raise SystemExit(f"Root node not found: {root_id}")

    title = root.title or root_id

    refs = [n for n in nodes.values() if n.kind == "spec_ref"]
    refs.sort(key=lambda n: (n.label or "", n.id))

    parts: List[str] = []
    parts.append(r"\\documentclass[11pt]{article}")
    parts.append(r"\\usepackage[utf8]{inputenc}")
    parts.append(r"\\usepackage[T1]{fontenc}")
    parts.append(r"\\usepackage{geometry}")
    parts.append(r"\\geometry{margin=1in}")
    parts.append(r"\\usepackage{amsmath,amssymb,amsthm,mathtools}")
    parts.append(r"\\usepackage{hyperref}")
    parts.append(r"\\usepackage{enumitem}")
    parts.append(r"\\usepackage{microtype}")
    parts.append("")
    parts.append(r"\\title{" + latex_escape(title) + "}")
    parts.append(r"\\author{}");
    parts.append(r"\\date{}");
    parts.append("")
    parts.append(r"\\begin{document}")
    parts.append(r"\\maketitle")
    parts.append("")

    if refs:
        parts.append(r"\\section*{References}")
        parts.append(r"\\begin{itemize}")
        for r in refs:
            parts.append(render_spec_ref(r))
        parts.append(r"\\end{itemize}")
        parts.append("")

    for sec in get_sections(nodes):
        sec_title = sec.title or sec.id
        parts.append(r"\\section{" + latex_escape(sec_title) + "}")
        children = contains_children(edges, sec.id)
        for cid in children:
            child = nodes.get(cid)
            if child is None:
                continue
            if child.kind == "clause":
                parts.append(render_clause(child))
            elif child.kind == "term":
                parts.append(render_term(child))
            elif child.kind == "property":
                parts.append(render_property(child))
            else:
                # fallback
                parts.append(r"% Unhandled kind: " + latex_escape(child.kind) + " " + latex_escape(child.id))
        parts.append("")

    parts.append(r"\\end{document}")
    parts.append("")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True)
    ap.add_argument("--out", dest="out_dir", required=True)
    args = ap.parse_args()

    in_path = Path(args.in_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    g = load_frame(in_path)
    tex = render(g)
    (out_dir / "main.tex").write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
