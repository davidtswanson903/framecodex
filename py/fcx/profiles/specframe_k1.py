from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from fcx.kernel import KernelCtx
from fcx.violations import Violation


SPEC_E = {
    "BAD_ROOT": "SPEC.E.BAD_ROOT",
    "BAD_KIND": "SPEC.E.BAD_KIND",
    "BAD_EDGE_TYPE": "SPEC.E.BAD_EDGE_TYPE",
    "MISSING_REQUIRED_ATTR": "SPEC.E.MISSING_REQUIRED_ATTR",
    "CONTAINS_CYCLE": "SPEC.E.CONTAINS_CYCLE",
    "MULTI_PARENT": "SPEC.E.CONTAINS_MULTI_PARENT",
    "BAD_STATUS": "SPEC.E.BAD_STATUS",
}

ALLOWED_NODE_KINDS_SPECFRAME = {"spec", "section", "term", "clause", "property", "example", "spec_ref"}
ALLOWED_EDGE_TYPES_SPECFRAME = {"contains", "depends_on", "defines", "refines", "refers_to", "example_of"}
REQUIRED_ATTRS_BY_KIND: Dict[str, set[str]] = {
    "spec": {"title", "status", "summary", "profile"},
    "section": {"title", "status"},
    "term": {"label", "status"},
    "clause": {"label", "status"},
    "property": {"label", "status"},
    "example": {"label", "status"},
    "spec_ref": {"target_graph_id"},
}
ALLOWED_STATUS = {"normative", "informative", "experimental"}


def _is_str(x: Any) -> bool:
    return isinstance(x, str) and bool(x)


def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def _node_attr_map(node: Dict[str, Any]) -> Dict[str, Any]:
    m = dict(node)
    attrs = node.get("attrs")
    if isinstance(attrs, list):
        for a in attrs:
            if isinstance(a, dict) and isinstance(a.get("key"), str):
                m.setdefault(a["key"], a.get("value"))
    return m


def infer_profile(g: Any) -> str:
    if not isinstance(g, dict):
        return ""
    gid = g.get("graph_id")
    if not _is_str(gid):
        return ""
    for n in _as_list(g.get("nodes")):
        if isinstance(n, dict) and n.get("id") == gid:
            nm = _node_attr_map(n)
            p = nm.get("profile")
            return p if _is_str(p) else ""
    return ""


def validate_specframe_k1(ctx: KernelCtx, g: Any, frame_path: str) -> List[Violation]:
    if not isinstance(g, dict):
        return [Violation(code=SPEC_E["BAD_ROOT"], path=frame_path, message="frame not a mapping")]

    gid = g.get("graph_id")
    nodes = _as_list(g.get("nodes"))
    edges = _as_list(g.get("edges"))

    nd: Dict[str, Dict[str, Any]] = {}
    for raw in nodes:
        if isinstance(raw, dict) and _is_str(raw.get("id")):
            nd[raw["id"]] = raw

    root = nd.get(gid) if _is_str(gid) else None
    if not root:
        return [Violation(code=SPEC_E["BAD_ROOT"], path=frame_path, message="missing root node with id == graph_id")]

    rootm = _node_attr_map(root)
    if rootm.get("kind") != "spec":
        return [
            Violation(
                code=SPEC_E["BAD_ROOT"],
                path=frame_path,
                node_id=str(root.get("id") or "") or None,
                message="root kind must be 'spec'",
            )
        ]

    violations: List[Violation] = []

    for nid, raw in nd.items():
        nm = _node_attr_map(raw)
        kind = nm.get("kind")
        if kind not in ALLOWED_NODE_KINDS_SPECFRAME:
            violations.append(Violation(code=SPEC_E["BAD_KIND"], path=frame_path, node_id=nid, message=f"unknown kind: {kind}"))
            continue

        for req in REQUIRED_ATTRS_BY_KIND.get(str(kind), set()):
            if not _is_str(nm.get(req)):
                violations.append(
                    Violation(
                        code=SPEC_E["MISSING_REQUIRED_ATTR"],
                        path=frame_path,
                        node_id=nid,
                        message=f"missing required attr {req} for kind {kind}",
                    )
                )

        st = nm.get("status")
        if kind != "spec_ref":
            if not _is_str(st) or st not in ALLOWED_STATUS:
                violations.append(
                    Violation(
                        code=SPEC_E["BAD_STATUS"],
                        path=frame_path,
                        node_id=nid,
                        message=f"bad or missing status: {st}",
                    )
                )

    contains_edges: List[tuple[str, str]] = []
    parent_of: Dict[str, str] = {}

    for e in edges:
        if not isinstance(e, dict):
            continue
        et = e.get("type")
        if et not in ALLOWED_EDGE_TYPES_SPECFRAME:
            violations.append(Violation(code=SPEC_E["BAD_EDGE_TYPE"], path=frame_path, message=f"unknown edge type: {et}"))
            continue

        frm, to = e.get("from"), e.get("to")
        if et == "contains" and _is_str(frm) and _is_str(to):
            contains_edges.append((frm, to))
            if to in parent_of and parent_of[to] != frm:
                violations.append(
                    Violation(
                        code=SPEC_E["MULTI_PARENT"],
                        path=frame_path,
                        node_id=to,
                        message=f"node has multiple parents via contains: {parent_of[to]} and {frm}",
                    )
                )
            else:
                parent_of[to] = frm

    children: Dict[str, List[str]] = {}
    for frm, to in contains_edges:
        children.setdefault(frm, []).append(to)
    for k in children:
        children[k] = sorted(children[k])

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(nid: str) -> Optional[str]:
        if nid in visiting:
            return nid
        if nid in visited:
            return None
        visiting.add(nid)
        for ch in children.get(nid, []):
            cyc = dfs(ch)
            if cyc:
                return cyc
        visiting.remove(nid)
        visited.add(nid)
        return None

    root_id = str(root.get("id") or "")
    cyc = dfs(root_id)
    if cyc:
        violations.append(Violation(code=SPEC_E["CONTAINS_CYCLE"], path=frame_path, node_id=cyc, message="contains cycle detected"))

    return violations


@dataclass(frozen=True)
class ProfileValidator:
    profile: str
    validate: Callable[[KernelCtx, Any, str], List[Violation]]


PROFILE_VALIDATORS: Dict[str, ProfileValidator] = {
    "specframe-k1": ProfileValidator(profile="specframe-k1", validate=validate_specframe_k1),
}
