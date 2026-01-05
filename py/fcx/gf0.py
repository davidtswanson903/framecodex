from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from fcx.kernel import Budget
from fcx.violations import Violation
from fcx.util import read_text


GF0_E = {
    "BAD_FRAME": "GF0.E.BAD_FRAME",
    "MISSING_GRAPH_ID": "GF0.E.MISSING_GRAPH_ID",
    "MISSING_VERSION": "GF0.E.MISSING_VERSION",
    "MISSING_FIELD": "GF0.E.MISSING_FIELD",
    "BAD_FIELD_TYPE": "GF0.E.BAD_FIELD_TYPE",
    "DUP_NODE_ID": "GF0.E.DUP_NODE_ID",
    "EDGE_MISSING_ENDPOINT": "GF0.E.EDGE_MISSING_ENDPOINT",
    "META_DEPTH": "GF0.E.META_DEPTH_EXCEEDED",
}


def load_frame_yaml(path: Path) -> Any:
    return yaml.safe_load(read_text(path))


def _is_list(x: Any) -> bool:
    return isinstance(x, list)


def _is_str(x: Any) -> bool:
    return isinstance(x, str) and bool(x)


def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def validate_gf0_struct(g: Any, *, frame_path: str, budget: Budget, meta_depth: int = 0) -> List[Violation]:
    v: List[Violation] = []

    if meta_depth > budget.max_meta_depth:
        v.append(
            Violation(
                code=GF0_E["META_DEPTH"],
                path=frame_path,
                message=f"meta depth exceeded: {meta_depth} > {budget.max_meta_depth}",
            )
        )
        return v

    if not isinstance(g, dict):
        return [Violation(code=GF0_E["BAD_FRAME"], path=frame_path, message="frame is not a mapping")]

    required_fields = ["graph_id", "version", "attrs", "nodes", "edges", "meta"]
    for f in required_fields:
        if f not in g:
            v.append(Violation(code=GF0_E["MISSING_FIELD"], path=frame_path, message=f"missing field: {f}"))

    gid = g.get("graph_id")
    ver = g.get("version")
    if not _is_str(gid):
        v.append(Violation(code=GF0_E["MISSING_GRAPH_ID"], path=frame_path, message="graph_id must be non-empty string"))
    if not _is_str(ver):
        v.append(Violation(code=GF0_E["MISSING_VERSION"], path=frame_path, message="version must be non-empty string"))

    for lf in ["attrs", "nodes", "edges", "meta"]:
        if lf in g and not _is_list(g.get(lf)):
            v.append(Violation(code=GF0_E["BAD_FIELD_TYPE"], path=frame_path, message=f"{lf} must be a list"))

    nodes = _as_list(g.get("nodes"))
    edges = _as_list(g.get("edges"))

    seen: set[str] = set()
    for n in nodes:
        if not isinstance(n, dict):
            continue
        nid = n.get("id")
        if not _is_str(nid):
            v.append(Violation(code=GF0_E["BAD_FIELD_TYPE"], path=frame_path, message="node.id must be non-empty string"))
            continue
        if nid in seen:
            v.append(Violation(code=GF0_E["DUP_NODE_ID"], path=frame_path, node_id=nid, message="duplicate node id"))
        seen.add(nid)

    for e in edges:
        if not isinstance(e, dict):
            continue
        frm = e.get("from")
        to = e.get("to")
        et = e.get("type")
        if not _is_str(et):
            v.append(Violation(code=GF0_E["BAD_FIELD_TYPE"], path=frame_path, message="edge.type must be non-empty string"))
        if _is_str(frm) and frm not in seen:
            v.append(
                Violation(
                    code=GF0_E["EDGE_MISSING_ENDPOINT"],
                    path=frame_path,
                    edge_id=str(e.get("id") or "") or None,
                    message=f"edge.from missing node: {frm}",
                )
            )
        if _is_str(to) and to not in seen:
            v.append(
                Violation(
                    code=GF0_E["EDGE_MISSING_ENDPOINT"],
                    path=frame_path,
                    edge_id=str(e.get("id") or "") or None,
                    message=f"edge.to missing node: {to}",
                )
            )

    for mg in _as_list(g.get("meta")):
        v.extend(validate_gf0_struct(mg, frame_path=frame_path, budget=budget, meta_depth=meta_depth + 1))

    return v
