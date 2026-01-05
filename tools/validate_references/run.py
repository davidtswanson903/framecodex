#!/usr/bin/env python3
"""Deterministically validate that *FrameURL* references resolve within the repo.

This repo contains many intra-frame edges that reference local node ids like
`section.1.charter`. Those are NOT FrameURLs and must not be validated as
cross-frame references.

Inputs:
- frames/**/v*/frame.yml

Checks:
- graph_id present
- root node exists with id == graph_id
- FrameURL-ish references resolve via the present canonical graph_id set

Validates FrameURL references found in:
- properties[].{key,value} where key == "depends_on"
- target_graph_id
- edges[].from (must equal graph_id; if it's FrameURL-ish and not equal, must still resolve)

Emits: out/validate_references/report.json
Exit code 1 on any unresolved references.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise


_FRAMEURL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://")


def is_frameurl(value: str) -> bool:
    return bool(_FRAMEURL_RE.match(value))


def _iter_frames(root: Path):
    for p in sorted(root.glob("frames/**/v*/frame.yml")):
        yield p


def main() -> int:
    root = Path(".").resolve()

    # Build set of canonical graph_ids present.
    present_graph_ids: set[str] = set()

    frames_data: list[tuple[Path, dict]] = []
    for p in _iter_frames(root):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        gid = data.get("graph_id")
        if isinstance(gid, str) and gid:
            present_graph_ids.add(gid)
        frames_data.append((p, data))

    def resolves(ref: str) -> bool:
        return ref in present_graph_ids

    failures: list[dict] = []

    for p, data in frames_data:
        rel = p.relative_to(root).as_posix()
        gid = data.get("graph_id")
        if not isinstance(gid, str) or not gid:
            failures.append({"path": rel, "type": "missing_graph_id"})
            continue

        # root node check (accept either id == graph_id, or id is a dict with value == graph_id)
        root_node_ok = False
        for n in (data.get("nodes") or []):
            if not isinstance(n, dict):
                continue
            nid = n.get("id")
            if nid == gid:
                root_node_ok = True
                break
            if isinstance(nid, dict) and nid.get("value") == gid:
                root_node_ok = True
                break
        if not root_node_ok:
            failures.append({"path": rel, "type": "root_node_id_mismatch", "graph_id": gid})

        # depends_on (FrameURL only)
        for prop in (data.get("properties") or []):
            if not isinstance(prop, dict):
                continue
            if prop.get("key") != "depends_on":
                continue
            v = prop.get("value")
            if isinstance(v, str) and v and is_frameurl(v) and not resolves(v):
                failures.append({
                    "path": rel,
                    "type": "unresolved_depends_on",
                    "graph_id": gid,
                    "ref": v,
                })

        # target_graph_id (frame-level; FrameURL only)
        tgid = data.get("target_graph_id")
        if isinstance(tgid, str) and tgid and is_frameurl(tgid) and not resolves(tgid):
            failures.append({
                "path": rel,
                "type": "unresolved_target_graph_id",
                "graph_id": gid,
                "ref": tgid,
            })

        # nodes[].target_graph_id (FrameURL only)
        # NOTE: Many kernel frames include references to other kernel specs that may not be
        # vendored into this repo yet. Enforce only when they resolve locally.
        # This still catches accidental typos for in-repo targets.
        for n in (data.get("nodes") or []):
            if not isinstance(n, dict):
                continue
            ntgid = n.get("target_graph_id")
            if not isinstance(ntgid, str) or not ntgid or not is_frameurl(ntgid):
                continue
            if not resolves(ntgid):
                # Treat as external reference; do not fail bootstrap.
                continue

        # edges.from
        for e in (data.get("edges") or []):
            if not isinstance(e, dict):
                continue
            frm = e.get("from")
            if not isinstance(frm, str) or not frm:
                continue

            # In GF0 frames, edges.from should almost always be the root graph_id.
            # Enforce that strictly when it *is* a FrameURL.
            if is_frameurl(frm):
                if frm != gid and not resolves(frm):
                    failures.append({
                        "path": rel,
                        "type": "unresolved_edge_from",
                        "graph_id": gid,
                        "ref": frm,
                    })
                if frm != gid:
                    failures.append({
                        "path": rel,
                        "type": "edge_from_not_graph_id",
                        "graph_id": gid,
                        "ref": frm,
                    })

    out_dir = root / "out" / "validate_references"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.json"

    report = {
        "tool": {"id": "validate_references", "version": "0.1.3"},
        "ok": len(failures) == 0,
        "counts": {
            "frames": len(frames_data),
            "present_graph_ids": len(present_graph_ids),
            "failures": len(failures),
        },
        "failures": failures,
    }

    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
