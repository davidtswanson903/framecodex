"""FrameURL reference validator (deterministic)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, List, Optional, Tuple

import yaml

from fcx.kernel import KernelCtx
from fcx.util import read_text
from fcx.violations import Violation


REF_E = {
    "MISSING_GRAPH_ID": "REF.E.MISSING_GRAPH_ID",
    "ROOT_NODE_MISSING": "REF.E.ROOT_NODE_MISSING",
    "UNRESOLVED_DEPENDS_ON": "REF.E.UNRESOLVED_DEPENDS_ON",
    "UNRESOLVED_TARGET_GRAPH_ID": "REF.E.UNRESOLVED_TARGET_GRAPH_ID",
    "UNRESOLVED_EDGE_FROM": "REF.E.UNRESOLVED_EDGE_FROM",
    "EDGE_FROM_NOT_GRAPH_ID": "REF.E.EDGE_FROM_NOT_GRAPH_ID",
}

_FRAMEURL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://")


def _is_frameurl(value: str) -> bool:
    return bool(_FRAMEURL_RE.match(value))


def _iter_frames(root: Path) -> List[Path]:
    return sorted(root.glob("frames/**/v*/frame.yml"))


def validate_references(ctx: KernelCtx) -> Tuple[List[Violation], List[Violation]]:
    """Validate FrameURL references resolve within the repo.
    
    Returns (violations, warnings).
    """
    root = Path(ctx.repo_root)
    violations: List[Violation] = []
    warnings: List[Violation] = []

    # Build canonical graph_ids set
    present_graph_ids: set[str] = set()
    frames_data: list[tuple[Path, dict]] = []

    for frame_path in _iter_frames(root):
        data = yaml.safe_load(read_text(frame_path))
        if not isinstance(data, dict):
            continue
        gid = data.get("graph_id")
        if isinstance(gid, str) and gid:
            present_graph_ids.add(gid)
        frames_data.append((frame_path, data))

    def resolves(ref: str) -> bool:
        return ref in present_graph_ids

    # Validate each frame
    for frame_path, data in frames_data:
        rel = str(frame_path.relative_to(root))
        gid = data.get("graph_id")

        if not isinstance(gid, str) or not gid:
            violations.append(Violation(code=REF_E["MISSING_GRAPH_ID"], path=rel, message="missing graph_id"))
            continue

        # Root node must exist with id == graph_id
        root_node_ok = False
        for n in data.get("nodes") or []:
            if not isinstance(n, dict):
                continue
            if n.get("id") == gid:
                root_node_ok = True
                break
        if not root_node_ok:
            violations.append(
                Violation(code=REF_E["ROOT_NODE_MISSING"], path=rel, message=f"root node with id={gid} not found")
            )

        # Validate depends_on (FrameURL only)
        for prop in data.get("properties") or []:
            if not isinstance(prop, dict):
                continue
            if prop.get("key") != "depends_on":
                continue
            v = prop.get("value")
            if isinstance(v, str) and v and _is_frameurl(v) and not resolves(v):
                violations.append(
                    Violation(
                        code=REF_E["UNRESOLVED_DEPENDS_ON"],
                        path=rel,
                        message=f"unresolved depends_on: {v}",
                    )
                )

        # Validate frame-level target_graph_id
        tgid = data.get("target_graph_id")
        if isinstance(tgid, str) and tgid and _is_frameurl(tgid) and not resolves(tgid):
            violations.append(
                Violation(
                    code=REF_E["UNRESOLVED_TARGET_GRAPH_ID"],
                    path=rel,
                    message=f"unresolved target_graph_id: {tgid}",
                )
            )

        # Validate node-level target_graph_id (external refs ok; only fail if in-repo typo)
        for n in data.get("nodes") or []:
            if not isinstance(n, dict):
                continue
            ntgid = n.get("target_graph_id")
            if not isinstance(ntgid, str) or not ntgid or not _is_frameurl(ntgid):
                continue
            if not resolves(ntgid):
                # External reference; don't fail bootstrap
                continue

        # Validate edges.from (FrameURL must resolve; if not root, warn)
        for e in data.get("edges") or []:
            if not isinstance(e, dict):
                continue
            frm = e.get("from")
            if not isinstance(frm, str) or not frm:
                continue

            if _is_frameurl(frm):
                if frm != gid and not resolves(frm):
                    violations.append(
                        Violation(
                            code=REF_E["UNRESOLVED_EDGE_FROM"],
                            path=rel,
                            message=f"unresolved edge.from: {frm}",
                        )
                    )
                if frm != gid:
                    violations.append(
                        Violation(
                            code=REF_E["EDGE_FROM_NOT_GRAPH_ID"],
                            path=rel,
                            message=f"edge.from={frm} != graph_id={gid}",
                        )
                    )

    return violations, warnings
