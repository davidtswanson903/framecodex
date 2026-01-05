#!/usr/bin/env python3
"""Deterministically render a GF0 frame to Markdown (Simple Markdown Renderer K1).

This is a repo-local deterministic renderer.

Input:
- frame file path (YAML) OR reads all frames in frames/**/v*/frame.yml when no args are given.

Output (default):
- docs/<frameurl_path>/v<version>/README.md

Also writes:
- out/render_simple_md/report.json

Notes:
- LF newlines
- strip trailing whitespace
- exactly one trailing LF
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise


_FRAME_LEAF = "frame.yml"


def _is_str(x) -> bool:
    return isinstance(x, str) and bool(x)


def _as_list(x):
    return x if isinstance(x, list) else []


def _stable_json(x) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _frameurl_path(graph_id: str) -> str:
    # render://_kernel/md/simple-k1 -> _kernel/render/md/simple-k1
    # <scheme>://<scope>/<segments...>
    if "://" not in graph_id:
        return graph_id
    scheme, rest = graph_id.split("://", 1)
    return f"{rest.split('/',1)[0]}/{scheme}/{rest.split('/',1)[1] if '/' in rest else ''}".rstrip("/")


def _yaml_block(obj: dict) -> str:
    # Deterministic YAML code block: stable key order.
    # PyYAML doesn't guarantee ordering; we pre-sort dict keys recursively.
    def sort_obj(o):
        if isinstance(o, dict):
            return {k: sort_obj(o[k]) for k in sorted(o.keys())}
        if isinstance(o, list):
            return [sort_obj(i) for i in o]
        return o

    s = yaml.safe_dump(
        sort_obj(obj),
        sort_keys=False,  # already sorted
        allow_unicode=True,
        default_flow_style=False,
        width=88,
    )
    return s.rstrip("\n")


def _validate_gf0(frame: dict) -> list[dict]:
    errs: list[dict] = []

    # Accept either:
    # - root-level graph_id/version (preferred GF0 container form)
    # - legacy/spec form where the root node id is the graph_id and root node carries version
    gid = frame.get("graph_id")
    ver = frame.get("version")

    if not _is_str(gid):
        # Fall back to first node that looks like a root spec/law/etc node.
        nodes0 = _as_list(frame.get("nodes"))
        if isinstance(nodes0, list):
            for n in nodes0:
                if isinstance(n, dict) and _is_str(n.get("id")):
                    gid = n.get("id")
                    break

    if not _is_str(ver):
        # Some frames carry version only at the root container; don't guess if absent.
        # But for robustness, if the root node exists and has a version, use it.
        nodes0 = _as_list(frame.get("nodes"))
        if isinstance(nodes0, list) and _is_str(gid):
            for n in nodes0:
                if isinstance(n, dict) and n.get("id") == gid and _is_str(n.get("version")):
                    ver = n.get("version")
                    break

    if not _is_str(gid):
        errs.append({"type": "missing_graph_id"})
    if not _is_str(ver):
        errs.append({"type": "missing_version"})

    nodes = _as_list(frame.get("nodes"))
    edges = _as_list(frame.get("edges"))
    meta = _as_list(frame.get("meta"))
    if not isinstance(nodes, list):
        errs.append({"type": "nodes_not_list"})
        nodes = []
    if not isinstance(edges, list):
        errs.append({"type": "edges_not_list"})
        edges = []
    if not isinstance(meta, list):
        errs.append({"type": "meta_not_list"})

    node_ids: list[str] = []
    for n in nodes:
        if not isinstance(n, dict) or not _is_str(n.get("id")):
            errs.append({"type": "bad_node", "node": n})
            continue
        node_ids.append(n["id"])

    if len(node_ids) != len(set(node_ids)):
        errs.append({"type": "duplicate_node_ids"})

    node_id_set = set(node_ids)
    for e in edges:
        if not isinstance(e, dict):
            errs.append({"type": "bad_edge", "edge": e})
            continue
        frm = e.get("from")
        to = e.get("to")
        typ = e.get("type")
        if not _is_str(frm) or not _is_str(to) or not _is_str(typ):
            errs.append({"type": "bad_edge_fields", "edge": e})
            continue
        if frm not in node_id_set:
            errs.append({"type": "edge_from_missing_node", "from": frm})
        if to not in node_id_set:
            errs.append({"type": "edge_to_missing_node", "to": to})

    # meta elements are frames; we validate during rendering recursively.
    return errs


def _contains_forest(nodes: list[dict], edges: list[dict], root_id: str, contains_type: str) -> tuple[list[str], dict[str, list[str]], list[dict]]:
    warnings: list[dict] = []

    node_ids = sorted([n["id"] for n in nodes if isinstance(n, dict) and _is_str(n.get("id"))])
    node_set = set(node_ids)

    children: dict[str, list[str]] = {nid: [] for nid in node_ids}
    indegree: dict[str, int] = {nid: 0 for nid in node_ids}

    for e in edges:
        if not isinstance(e, dict):
            continue
        if e.get("type") != contains_type:
            continue
        frm = e.get("from")
        to = e.get("to")
        if not (_is_str(frm) and _is_str(to)):
            continue
        if frm in node_set and to in node_set:
            children[frm].append(to)
            indegree[to] += 1

    # determinism
    for k in children.keys():
        children[k] = sorted(set(children[k]))

    multi_parents = sorted([nid for nid, d in indegree.items() if d > 1])
    if multi_parents:
        warnings.append({"type": "contains_multiple_parents", "nodes": multi_parents})

    # roots
    if root_id in node_set:
        roots = [root_id]
    else:
        roots = sorted([nid for nid, d in indegree.items() if d == 0 and children.get(nid)])
        if roots:
            warnings.append({"type": "missing_root_node_for_contains", "root": root_id})

    # cycle detection (DFS)
    temp: set[str] = set()
    perm: set[str] = set()

    def dfs(nid: str):
        if nid in perm:
            return
        if nid in temp:
            warnings.append({"type": "contains_cycle", "at": nid})
            return
        temp.add(nid)
        for c in children.get(nid, []):
            dfs(c)
        temp.remove(nid)
        perm.add(nid)

    for r in roots:
        dfs(r)

    return roots, children, warnings


def render_frame(frame: dict, *, heading_level: int = 1) -> tuple[str, list[dict]]:
    warnings: list[dict] = []
    errors = _validate_gf0(frame)
    if errors:
        # Hard error: spec says input MUST be valid GF0.
        raise ValueError(_stable_json({"errors": errors}))

    # Use canonical gid/ver if present; otherwise rely on the same fallback rules used by validation.
    gid = frame.get("graph_id")
    ver = frame.get("version")
    if not _is_str(gid) or not _is_str(ver):
        gid2 = gid if _is_str(gid) else None
        ver2 = ver if _is_str(ver) else None
        nodes0 = _as_list(frame.get("nodes"))
        if isinstance(nodes0, list) and not _is_str(gid2):
            for n in nodes0:
                if isinstance(n, dict) and _is_str(n.get("id")):
                    gid2 = n.get("id")
                    break
        if isinstance(nodes0, list) and _is_str(gid2) and not _is_str(ver2):
            for n in nodes0:
                if isinstance(n, dict) and n.get("id") == gid2 and _is_str(n.get("version")):
                    ver2 = n.get("version")
                    break
        gid = gid2
        ver = ver2

    nodes = _as_list(frame.get("nodes"))
    edges = _as_list(frame.get("edges"))

    # NOTE: In GF0, `meta` is a list of MetaGraph values. Some canonical specs store
    # informative metadata objects here that are not GraphFrameK0 instances.
    # We only recursively render meta entries that look like frames.
    meta_raw = _as_list(frame.get("meta"))
    if not isinstance(meta_raw, list):
        meta_raw = []

    meta_frames: list[dict] = []
    meta_nonframes: list[dict] = []
    for m in meta_raw:
        if isinstance(m, dict) and _is_str(m.get("graph_id")) and _is_str(m.get("version")):
            meta_frames.append(m)
        else:
            if isinstance(m, dict):
                meta_nonframes.append(m)

    # Order
    # ...existing code...
    meta_sorted = sorted(
        [m for m in meta_frames if isinstance(m, dict)],
        key=lambda m: ((m.get("graph_id") or ""), (m.get("version") or "")),
    )

    # Ordering
    nodes_sorted = sorted([n for n in nodes if isinstance(n, dict) and _is_str(n.get("id"))], key=lambda n: n["id"])

    def edge_key(e: dict):
        return (
            e.get("from") or "",
            e.get("to") or "",
            e.get("type") or "",
            e.get("id") or "",
        )

    edges_sorted = sorted([e for e in edges if isinstance(e, dict)], key=edge_key)
    meta_sorted = sorted(
        [m for m in meta_frames if isinstance(m, dict)],
        key=lambda m: ((m.get("graph_id") or ""), (m.get("version") or "")),
    )

    excl_node = {"id", "kind", "attrs", "metrics"}

    h = "#" * max(1, heading_level)
    lines: list[str] = []
    lines.append("# " + gid)
    lines.append(f"- version: {ver}")
    lines.append(f"- nodes: {len(nodes_sorted)}")
    lines.append(f"- edges: {len(edges_sorted)}")
    lines.append(f"- meta: {len(meta_raw)}")

    # Nodes
    lines.append(f"{h}# Nodes")
    for n in nodes_sorted:
        nid = n["id"]
        kind = n.get("kind") if _is_str(n.get("kind")) else ""
        lines.append(f"- **{nid}** (kind: {kind})")

        if _is_str(n.get("label")):
            lines.append(f"  - label: {n['label']}")

        attrs = n.get("attrs")
        if isinstance(attrs, list) and attrs:
            lines.append("  - attrs:")
            lines.append("    | key | value | vtype | desc |")
            lines.append("    | --- | --- | --- | --- |")
            for a in attrs:
                if not isinstance(a, dict):
                    continue
                k = a.get("key") or ""
                v = a.get("value")
                vt = a.get("vtype") or ""
                d = a.get("desc") or ""
                vv = _stable_json(v) if not isinstance(v, str) else v
                lines.append(f"    | {k} | {vv} | {vt} | {d} |")

        metrics = n.get("metrics")
        if isinstance(metrics, list) and metrics:
            lines.append("  - metrics:")
            lines.append("    | name | value | unit | desc |")
            lines.append("    | --- | --- | --- | --- |")
            for m in metrics:
                if not isinstance(m, dict):
                    continue
                name = m.get("name") or ""
                val = m.get("value")
                unit = m.get("unit") or ""
                desc = m.get("desc") or ""
                vv = _stable_json(val) if not isinstance(val, str) else val
                lines.append(f"    | {name} | {vv} | {unit} | {desc} |")

        extra = {k: v for k, v in n.items() if k not in excl_node}
        if extra:
            lines.append("  - Extra fields:")
            lines.append("    ```yml")
            lines.extend(["    " + ln for ln in _yaml_block(extra).split("\n")])
            lines.append("    ```")

    # Edges
    lines.append(f"{h}# Edges")
    lines.append("| from | to | type | id | attrs | metrics |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for e in edges_sorted:
        frm = e.get("from") or ""
        to = e.get("to") or ""
        typ = e.get("type") or ""
        eid = e.get("id") or ""
        attrs = e.get("attrs")
        metrics = e.get("metrics")
        attrs_s = _stable_json(attrs) if attrs else ""
        metrics_s = _stable_json(metrics) if metrics else ""
        lines.append(f"| {frm} | {to} | {typ} | {eid} | {attrs_s} | {metrics_s} |")

    lines.append("")

    # Contains tree
    contains_type = "contains"
    roots, children, w = _contains_forest(nodes_sorted, edges_sorted, gid, contains_type)
    warnings.extend(w)
    if any(e.get("type") == contains_type for e in edges_sorted):
        lines.append(f"{h}# Contains Tree")

        def emit(nid: str, depth: int):
            indent = "  " * depth
            lines.append(f"{indent}- {nid}")
            for c in children.get(nid, []):
                emit(c, depth + 1)

        if roots:
            for r in roots:
                emit(r, 0)
        else:
            lines.append("- (none)")
        lines.append("")

    # Meta graphs
    if meta_sorted:
        lines.append(f"{h}# Meta Graphs")
        for m in meta_sorted:
            lines.append("---")
            # Keep same algorithm; demote headings for readability.
            md, w2 = render_frame(m, heading_level=heading_level + 2)
            warnings.extend(w2)
            lines.append(md.rstrip("\n"))
        lines.append("")

    # Render meta non-frames (if any)
    if meta_nonframes:
        lines.append("")
        lines.append("## Meta")
        for i, m in enumerate(sorted(meta_nonframes, key=_stable_json), start=1):
            lines.append(f"- meta[{i}]")
            lines.append("  - Extra fields:")
            lines.append("    ```yml")
            lines.append("\n".join((" " * 4) + ln if ln else "" for ln in _yaml_block(m).splitlines()))
            lines.append("    ```")

    # normalize whitespace
    out_lines = [ln.rstrip() for ln in lines]
    return ("\n".join(out_lines).rstrip("\n") + "\n", warnings)


def main() -> int:
    root = Path('.').resolve()
    args = sys.argv[1:]

    if args:
        # Normalize provided paths to absolute so relative_to() is stable.
        frames = [Path(a).resolve() for a in args]
    else:
        frames = sorted(root.glob('frames/**/v*/frame.yml'))

    failures: list[dict] = []
    outputs: list[dict] = []

    docs_root = root / "docs"
    out_dir = root / "out" / "render_simple_md"
    out_dir.mkdir(parents=True, exist_ok=True)

    for p in frames:
        try:
            rel = p.relative_to(root).as_posix()
        except Exception:
            rel = p.as_posix()

        try:
            data = yaml.safe_load(p.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                continue

            md, warnings = render_frame(data)
            gid = data.get('graph_id')
            ver = data.get('version')
            if not _is_str(gid) or not _is_str(ver):
                # mimic render_frame fallback for output path
                nodes0 = _as_list(data.get('nodes'))
                if isinstance(nodes0, list) and not _is_str(gid):
                    for n in nodes0:
                        if isinstance(n, dict) and _is_str(n.get('id')):
                            gid = n.get('id')
                            break
                if isinstance(nodes0, list) and _is_str(gid) and not _is_str(ver):
                    for n in nodes0:
                        if isinstance(n, dict) and n.get('id') == gid and _is_str(n.get('version')):
                            ver = n.get('version')
                            break

            out_path = docs_root / _frameurl_path(gid) / f"v{ver}" / "README.md"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8", newline="\n")

            outputs.append({
                "graph_id": gid,
                "version": ver,
                "input": p.relative_to(root).as_posix(),
                "output": out_path.relative_to(root).as_posix(),
                "warnings": warnings,
            })
        except Exception as e:
            failures.append({"path": rel, "error": str(e)})
            ok = False
            continue

    report = {
        "tool": {"id": "render_simple_md", "version": "0.1.0"},
        "ok": len(failures) == 0,
        "outputs": outputs,
        "failures": failures,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
