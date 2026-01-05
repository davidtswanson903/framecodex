#!/usr/bin/env python3
"""Render a GF0/SpecFrame YAML into a deterministic DocIR JSON.

DocIR is a linear intermediate representation intended for human-doc projections.
Target renderers (Markdown/LaTeX/plaintext) should be pure printers over DocIR.

Usage:
  tools/render_docir/run.py --in <frame.yml> --out <docir.json>

Determinism:
- stable ordering (order -> id)
- no timestamps
- stable anchor derivation

This first implementation supports the SpecFrame-ish subset used in this repo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Ensure repo root is on sys.path so we can import tools/* as modules.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# InlineMarkup-K1 (deterministic tiny markup subset)
try:
    from tools.markup.inline_markup_k1 import parse as parse_inline_markup  # type: ignore
except Exception:  # pragma: no cover
    parse_inline_markup = None  # type: ignore

# PubTeX authoring shortcut (tex-inline-v0 -> pub-tex-inline-v0 IR)
try:
    from tools.markup.pub_tex_inline_v0 import parse_tex_inline_v0, to_ir as pub_tex_to_ir  # type: ignore
except Exception:  # pragma: no cover
    parse_tex_inline_v0 = None  # type: ignore
    pub_tex_to_ir = None  # type: ignore


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_bytes(p: Path) -> bytes:
    return p.read_bytes()


_LATEXISH_WS = re.compile(r"\s+")


def norm_text(s: str) -> str:
    # Preserve newlines as paragraph boundaries; normalize CRLF.
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    # Trim trailing whitespace per line.
    s = "\n".join(ln.rstrip() for ln in s.split("\n"))
    return s.strip("\n")


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "x"


def stable_anchor(node_id: str) -> str:
    # Anchor should be readable but collision-resistant.
    base = slugify(node_id)
    h = hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:8]
    return f"{base}-{h}"


def find_attr(attrs: Any, key: str) -> Optional[str]:
    if not isinstance(attrs, list):
        return None
    for a in attrs:
        if isinstance(a, dict) and a.get("key") == key:
            v = a.get("value")
            return v if isinstance(v, str) else None
    return None


def find_attr_json(attrs: Any, key: str) -> Optional[Any]:
    v = find_attr(attrs, key)
    if v is None:
        return None
    try:
        return json.loads(v)
    except Exception:
        return None


def find_attr_json_strict(attrs: Any, key: str) -> Optional[Any]:
    """Parse JSON from an attr value. Returns None on any failure."""

    v = find_attr(attrs, key)
    if v is None:
        return None
    try:
        return json.loads(v)
    except Exception:
        return None


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
    attrs: Optional[List[Dict[str, Any]]] = None
    target: Optional[str] = None  # for reference nodes


def parse_nodes(g: Dict[str, Any]) -> Dict[str, Node]:
    out: Dict[str, Node] = {}
    for raw in g.get("nodes", []):
        if not isinstance(raw, dict) or "id" not in raw:
            continue
        out[str(raw["id"])] = Node(
            id=str(raw["id"]),
            kind=str(raw.get("kind", "")),
            status=str(raw.get("status", "")),
            title=raw.get("title"),
            label=raw.get("label"),
            order=raw.get("order"),
            text=raw.get("text"),
            summary=raw.get("summary"),
            symbols=raw.get("symbols"),
            attrs=raw.get("attrs"),
            target=raw.get("target"),
        )
    return out


def edges_of_type(edges: Any, edge_type: str) -> List[Dict[str, Any]]:
    if not isinstance(edges, list):
        return []
    out = [e for e in edges if isinstance(e, dict) and e.get("type") == edge_type]
    # stable
    out.sort(key=lambda e: (str(e.get("from", "")), str(e.get("to", "")), str(e.get("type", ""))))
    return out


def contains_children(edges: List[Dict[str, Any]], parent_id: str) -> List[str]:
    kids = [str(e.get("to")) for e in edges if e.get("from") == parent_id]
    # stable order by (node.order, node.id) applied later
    return sorted(set(kids))


_KIND_PRECEDENCE = {
    "section": 10,
    "term": 20,
    "clause": 30,
    "property": 40,
    "example": 50,
    "spec_ref": 60,
}


def kind_rank(kind: str) -> int:
    return _KIND_PRECEDENCE.get(kind, 999)


def stable_node_sort(nodes: Dict[str, Node], ids: List[str]) -> List[str]:
    def key(nid: str) -> Tuple[int, int, str]:
        n = nodes.get(nid)
        if n is None:
            return (999, 10**9, nid)
        order = n.order if isinstance(n.order, int) else 10**9
        return (kind_rank(n.kind), order, n.id)

    return sorted(ids, key=key)


def build_spine(g: Dict[str, Any], nodes: Dict[str, Node]) -> Tuple[str, Dict[str, List[str]]]:
    """Return (root_id, children_map) for the spine.

    Prefer explicit `contains` edges. If no `contains` edges exist, synthesize a
    spine with pseudo-sections by node kind.
    """

    root_id = str(g.get("graph_id") or "")
    if not root_id or root_id not in nodes:
        raise SystemExit(f"Root node not found: {root_id}")

    contains = edges_of_type(g.get("edges"), "contains")
    if contains:
        children_map: Dict[str, List[str]] = {}
        for e in contains:
            frm = str(e.get("from"))
            to = str(e.get("to"))
            children_map.setdefault(frm, []).append(to)
        # stable child ordering later
        return root_id, children_map

    # Synthetic spine: root -> kind groups -> ids
    # We emit pseudo section headings in DocIR without fabricating nodes.
    return root_id, {}


def to_markup(value: str, *, text_format: str) -> Optional[Dict[str, Any]]:
    """Parse value into MarkupIR if enabled.

    Returns a JSON-serializable MarkupIR dict, or None if parsing is unavailable.
    Parsing errors are embedded as `errors` for downstream validation/reporting.
    """

    if parse_inline_markup is None:
        return None
    ast, errs = parse_inline_markup(value, mode=text_format)
    return {
        "kind": "inline-markup-k1",
        "mode": text_format,
        "blocks": ast.get("blocks", []),
        "errors": [
            {"code": e.code, "message": e.message, "pos": e.pos}
            for e in (errs or [])
        ],
    }


def _pub_tex_inline_from_node(n: Node, *, field: str) -> Optional[Dict[str, Any]]:
    """Return publication TeX inline IR attached to a node.

    Supported forms:

    (A) Canonical JSON IR (preferred storage):
      - attr key: `pub.tex.<field>` where field in {"summary","text","body"}
      - value: JSON encoding of {"kind":"pub-tex-inline-v0","nodes":[...]}

    (B) Authoring shortcut (compiled deterministically at render time):
      - attr key: `pub.tex.<field>.format` == "tex-inline-v0"
      - attr key: `pub.tex.<field>` is a string containing typed segments:
          {{m:...}} for math, {{c:...}} for code, everything else is text.
        Escapes: \\{{ and \\}} for literal delimiters.

    We do not deeply validate here; gates + renderer validate further.
    """

    if not n.attrs:
        return None

    k = f"pub.tex.{field}"

    # (A) canonical JSON form
    v = find_attr_json_strict(n.attrs, k)
    if isinstance(v, dict) and v.get("kind") == "pub-tex-inline-v0":
        return v

    # (B) authoring shortcut
    fmt = find_attr(n.attrs, f"pub.tex.{field}.format")
    if fmt != "tex-inline-v0":
        return None

    if parse_tex_inline_v0 is None or pub_tex_to_ir is None:
        raise SystemExit("PubTeX tex-inline-v0 parsing unavailable (import failed)")

    raw = find_attr(n.attrs, k)
    if raw is None:
        raise SystemExit(f"Missing required attr: {k} (pub.tex.{field}.format=tex-inline-v0)")

    nodes, errs = parse_tex_inline_v0(raw)
    if errs:
        # Fail hard with deterministic error text.
        head = errs[0]
        raise SystemExit(f"pub.tex.{field} parse error {head.code} at pos {head.pos}: {head.message} (node={n.id})")

    return pub_tex_to_ir(nodes)  # kind=pub-tex-inline-v0


def to_docir(g: Dict[str, Any], src_bytes: bytes) -> Dict[str, Any]:
    nodes = parse_nodes(g)
    root_id, children_map = build_spine(g, nodes)
    root = nodes[root_id]

    # Deterministic lookup table for raw node mappings (needed for fields not
    # included in the Node dataclass, e.g. spec_ref.target_graph_id).
    raw_nodes_list = g.get("nodes") if isinstance(g.get("nodes"), list) else []
    raw_nodes: Dict[str, Dict[str, Any]] = {
        str(r.get("id")): r for r in raw_nodes_list if isinstance(r, dict) and isinstance(r.get("id"), str)
    }

    anchors: Dict[str, str] = {nid: stable_anchor(nid) for nid in sorted(nodes.keys())}

    front = {
        "graph_id": root_id,
        "frame_version": str(g.get("version") or ""),
        "title": root.title or root_id,
        "authors": find_attr_json(root.attrs, "doc.authors") or [],
        "created": find_attr(root.attrs, "doc.created") or "",
        "updated": find_attr(root.attrs, "doc.updated") or "",
        "license": find_attr(root.attrs, "doc.license") or "",
        "profile": str(root.profile) if hasattr(root, "profile") else "",
    }

    blocks: List[Dict[str, Any]] = []

    # References from spec_ref nodes
    refs: List[Dict[str, str]] = []
    for n in sorted(nodes.values(), key=lambda x: (x.kind, x.label or "", x.id)):
        if n.kind != "spec_ref":
            continue
        label = n.label or n.id
        target = ""
        # spec_ref in current frames uses `target_graph_id` on node.
        # The Node model used by this tool does not currently include it, so we
        # read it from the raw mapping deterministically.
        raw = raw_nodes.get(n.id) if isinstance(raw_nodes, dict) else None
        if isinstance(raw, dict):
            tgid = raw.get("target_graph_id")
            if isinstance(tgid, str):
                target = tgid
        refs.append({"label": label, "target": target})

    # Emit title heading
    blocks.append({"type": "heading", "level": 1, "title": front["title"], "anchor": anchors[root_id]})

    contains_edges = edges_of_type(g.get("edges"), "contains")

    if contains_edges:
        # traverse sections under root if present
        root_children = children_map.get(root_id, [])
        root_children = stable_node_sort(nodes, root_children)

        def walk(nid: str, depth: int) -> None:
            n = nodes.get(nid)
            if n is None:
                return

            # Determine desired text.format for this node.
            # Defaults are conservative: inline for summaries, block for clause.text.
            node_fmt = find_attr(n.attrs, "text.format") or "plain"

            if n.kind == "section":
                blocks.append(
                    {
                        "type": "heading",
                        "level": min(6, depth + 1),
                        "title": n.title or n.label or n.id,
                        "anchor": anchors[n.id],
                        "text_format": node_fmt,
                    }
                )
            elif n.kind == "title":
                # Title nodes are typically already represented by the root heading; preserve as a subheading
                # only when explicitly included in the contains spine.
                blocks.append(
                    {
                        "type": "heading",
                        "level": min(6, depth + 1),
                        "title": n.text or n.title or n.label or n.id,
                        "anchor": anchors[n.id],
                        "text_format": node_fmt,
                    }
                )
            elif n.kind == "paragraph":
                body = norm_text(n.text or "")
                fmt = node_fmt if node_fmt != "plain" else "md-block"
                pub_tex = _pub_tex_inline_from_node(n, field="text")
                blocks.append(
                    {
                        "type": "paragraph",
                        "anchor": anchors[n.id],
                        "text_format": fmt,
                        "text": body,
                        "body_markup": to_markup(body, text_format=fmt) if body else None,
                        "pub_tex_inline": pub_tex,
                    }
                )
            elif n.kind == "reference":
                # Render references as a simple paragraph link line.
                label = n.label or n.title or n.id
                target = n.target or ""
                body = f"{label}: {target}" if target else label
                blocks.append(
                    {
                        "type": "paragraph",
                        "anchor": anchors[n.id],
                        "text_format": "md-inline",
                        "text": body,
                        "body_markup": to_markup(body, text_format="md-inline") if body else None,
                    }
                )
            elif n.kind == "term":
                body = norm_text(n.summary or "")
                pub_tex = _pub_tex_inline_from_node(n, field="summary")
                blocks.append(
                    {
                        "type": "definition",
                        "label": n.label or n.id,
                        "status": n.status,
                        "anchor": anchors[n.id],
                        "text_format": node_fmt or "plain",
                        "body": body,
                        "body_markup": to_markup(body, text_format=node_fmt or "plain") if body else None,
                        "pub_tex_inline": pub_tex,
                    }
                )
            elif n.kind == "clause":
                body = norm_text(n.text or "")
                # Default clauses to md-block unless explicit override.
                fmt = node_fmt if node_fmt != "plain" else "md-block"
                pub_tex = _pub_tex_inline_from_node(n, field="text")
                blocks.append(
                    {
                        "type": "clause",
                        "label": n.label or n.id,
                        "status": n.status,
                        "anchor": anchors[n.id],
                        "text_format": fmt,
                        "body": body,
                        "body_markup": (to_markup(body, text_format=fmt) if (body and fmt.startswith("md-")) else None),
                        "pub_tex_inline": pub_tex,
                    }
                )
            elif n.kind == "property":
                blocks.append(
                    {
                        "type": "property",
                        "label": n.label or n.id,
                        "status": n.status,
                        "anchor": anchors[n.id],
                        "text_format": node_fmt,
                        "symbols": n.symbols or [],
                    }
                )
            # spec_ref is folded into references section

            kids = stable_node_sort(nodes, children_map.get(nid, []))
            for kid in kids:
                walk(kid, depth + 1)

        for c in root_children:
            walk(c, 1)
    else:
        # Synthetic spine: emit grouped sections by kind
        groups: Dict[str, List[str]] = {}
        for nid, n in nodes.items():
            if nid == root_id:
                continue
            if n.kind == "spec_ref":
                continue
            groups.setdefault(n.kind or "other", []).append(nid)

        for kind in sorted(groups.keys(), key=lambda k: (kind_rank(k), k)):
            blocks.append(
                {
                    "type": "heading",
                    "level": 2,
                    "title": f"{kind}" if kind != "other" else "Other",
                    "anchor": stable_anchor(f"kind:{kind}"),
                }
            )
            for nid in stable_node_sort(nodes, groups[kind]):
                n = nodes[nid]
                node_fmt = find_attr(n.attrs, "text.format") or "plain"
                if n.kind == "term":
                    body = norm_text(n.summary or "")
                    blocks.append(
                        {
                            "type": "definition",
                            "label": n.label or n.id,
                            "status": n.status,
                            "anchor": anchors[n.id],
                            "text_format": node_fmt or "plain",
                            "body": body,
                            "body_markup": (to_markup(body, text_format=node_fmt or "plain") if (body and (node_fmt or "plain").startswith("md-")) else None),
                        }
                    )
                elif n.kind == "clause":
                    body = norm_text(n.text or "")
                    fmt = node_fmt if node_fmt != "plain" else "md-block"
                    blocks.append(
                        {
                            "type": "clause",
                            "label": n.label or n.id,
                            "status": n.status,
                            "anchor": anchors[n.id],
                            "text_format": fmt,
                            "body": body,
                            "body_markup": (to_markup(body, text_format=fmt) if (body and fmt.startswith("md-")) else None),
                        }
                    )
                elif n.kind == "paragraph":
                    body = norm_text(n.text or "")
                    fmt = node_fmt if node_fmt != "plain" else "md-block"
                    blocks.append(
                        {
                            "type": "paragraph",
                            "anchor": anchors[n.id],
                            "text_format": fmt,
                            "text": body,
                            "body_markup": (to_markup(body, text_format=fmt) if (body and fmt.startswith("md-")) else None),
                        }
                    )
                elif n.kind == "reference":
                    label = n.label or n.title or n.id
                    target = n.target or ""
                    body = f"{label}: {target}" if target else label
                    blocks.append(
                        {
                            "type": "paragraph",
                            "anchor": anchors[n.id],
                            "text_format": "md-inline",
                            "text": body,
                            "body_markup": to_markup(body, text_format="md-inline") if body else None,
                        }
                    )
                elif n.kind == "title":
                    blocks.append(
                        {
                            "type": "heading",
                            "level": 3,
                            "title": n.text or n.title or n.label or n.id,
                            "anchor": anchors[n.id],
                            "text_format": node_fmt,
                        }
                    )
                elif n.kind == "property":
                    blocks.append(
                        {
                            "type": "property",
                            "label": n.label or n.id,
                            "status": n.status,
                            "anchor": anchors[n.id],
                            "text_format": node_fmt,
                            "symbols": n.symbols or [],
                        }
                    )
                else:
                    blocks.append(
                        {
                            "type": "note",
                            "kind": "unhandled-node",
                            "anchor": anchors[n.id],
                            "text": f"{n.kind} {n.id}",
                        }
                    )

    # Back matter: references + graph appendix-ish
    if refs:
        blocks.append({"type": "heading", "level": 2, "title": "References", "anchor": stable_anchor("refs")})
        for r in refs:
            label = (r.get("label") or "").strip()
            target = (r.get("target") or "").strip()
            text = f"{label} ({target})" if target else label
            if text:
                blocks.append({"type": "list_item", "text": text})

    docir = {
        "docir_version": "0.2.0",
        "front_matter": front,
        "anchors": anchors,
        "blocks": blocks,
        "sha256": sha256_bytes(src_bytes),
    }

    return docir


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True)
    ap.add_argument("--out", dest="out_path", required=True)
    args = ap.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    src = read_bytes(in_path)
    g = yaml.safe_load(src.decode("utf-8"))
    if not isinstance(g, dict):
        raise SystemExit("Input frame must be a YAML mapping")

    docir = to_docir(g, src)
    out_path.write_text(json.dumps(docir, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
