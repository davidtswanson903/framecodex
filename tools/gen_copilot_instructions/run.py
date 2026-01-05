#!/usr/bin/env python3
"""Generate .github/copilot-instructions.md deterministically.

Strict autogen:
- The output file is entirely generated; do not edit by hand.

What gets embedded:
- High-level repo invariants + golden gates
- Normative law pointers (RepoLaw K1, InlineMarkup-K1)
- Tool entrypoints
- CI workflows (jobs + step names)
- Context pack (large): excerpts from key law frames + tool headers

Determinism:
- stable ordering
- offline only
- no timestamps
- deterministic truncation by max_chars budget

This file is intended to be large (up to a budget) so coding agents have
sufficient context without external browsing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def find_frame(path: Path) -> Tuple[str, str]:
    """Return (graph_id, version) for a GF0 frame.yml."""
    g = read_yaml(path)
    if not isinstance(g, dict):
        raise ValueError(f"frame is not a mapping: {path}")
    gid = g.get("graph_id")
    ver = g.get("version")
    if not isinstance(gid, str) or not isinstance(ver, str) or not gid or not ver:
        raise ValueError(f"missing graph_id/version: {path}")
    return gid, ver


def list_tools() -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    tools_dir = REPO_ROOT / "tools"
    if not tools_dir.exists():
        return out

    for d in sorted([p for p in tools_dir.iterdir() if p.is_dir()], key=lambda p: p.name):
        run = d / "run"
        run_py = d / "run.py"
        if run.exists() and run.is_file():
            out.append({"id": d.name, "entrypoint": str(run.relative_to(REPO_ROOT))})
        elif run_py.exists() and run_py.is_file():
            out.append({"id": d.name, "entrypoint": str(run_py.relative_to(REPO_ROOT))})

    return out


def _read_file_head(path: Path, *, max_lines: int) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ""
    head = "\n".join(lines[:max_lines]).rstrip() + "\n"
    return head


def list_tool_excerpts(*, max_lines: int = 80) -> List[Dict[str, str]]:
    """Return short deterministic excerpts for each tool.

    Preference:
    - tools/<id>/run.py: module docstring (first ~max_lines)
    - otherwise tools/<id>/run: first ~max_lines
    """

    out: List[Dict[str, str]] = []
    tools_dir = REPO_ROOT / "tools"
    if not tools_dir.exists():
        return out

    for d in sorted([p for p in tools_dir.iterdir() if p.is_dir()], key=lambda p: p.name):
        run = d / "run"
        run_py = d / "run.py"
        src_path = run_py if run_py.exists() else run if run.exists() else None
        if src_path is None:
            continue
        excerpt = _read_file_head(src_path, max_lines=max_lines)
        if not excerpt.strip():
            continue
        out.append(
            {
                "id": d.name,
                "path": str(src_path.relative_to(REPO_ROOT)),
                "excerpt": excerpt,
            }
        )

    return out


def list_workflows() -> List[Dict[str, Any]]:
    wf_dir = REPO_ROOT / ".github" / "workflows"
    out: List[Dict[str, Any]] = []
    if not wf_dir.exists():
        return out

    for p in sorted(wf_dir.glob("*.yml"), key=lambda x: x.name):
        data = read_yaml(p)
        name = str(data.get("name") or p.name) if isinstance(data, dict) else p.name
        jobs = []
        if isinstance(data, dict) and isinstance(data.get("jobs"), dict):
            for jid, j in sorted(data["jobs"].items(), key=lambda kv: str(kv[0])):
                if not isinstance(j, dict):
                    continue
                steps = []
                for s in (j.get("steps") or []):
                    if isinstance(s, dict):
                        nm = s.get("name")
                        if isinstance(nm, str) and nm.strip():
                            steps.append(nm.strip())
                jobs.append({"id": str(jid), "name": str(j.get("name") or ""), "steps": steps})
        out.append({"path": str(p.relative_to(REPO_ROOT)), "name": name, "jobs": jobs})

    return out


def frame_excerpt(
    frame_path: Path,
    *,
    title: str,
    section_ids: Optional[List[str]] = None,
    max_chars: int = 8000,
) -> Dict[str, str]:
    """Produce a deterministic excerpt from a GF0 frame.

    Strategy (best-effort):
    - If edges/contains exist, walk spine for selected section IDs (or all sections if None).
    - Include text from clause/term/paragraph nodes.
    - If structure can't be derived, fall back to a raw YAML head.

    Notes:
    - This is an excerpt for instruction-context, not a canonical render.
    - Truncation is deterministic (hard cut at max_chars).
    """

    g = read_yaml(frame_path)
    if not isinstance(g, dict):
        return {"title": title, "path": str(frame_path.relative_to(REPO_ROOT)), "text": ""}

    nodes = g.get("nodes") if isinstance(g.get("nodes"), list) else []
    by_id: Dict[str, Dict[str, Any]] = {}
    for n in nodes:
        if isinstance(n, dict) and isinstance(n.get("id"), str):
            by_id[n["id"]] = n

    # Build contains mapping
    children: Dict[str, List[str]] = {}
    edges = g.get("edges") if isinstance(g.get("edges"), list) else []
    for e in edges:
        if not isinstance(e, dict) or e.get("type") != "contains":
            continue
        frm = str(e.get("from"))
        to = str(e.get("to"))
        children.setdefault(frm, []).append(to)

    for k in list(children.keys()):
        children[k] = sorted(dict.fromkeys(children[k]))

    root = str(g.get("graph_id") or "")

    def node_order(nid: str) -> Tuple[int, str]:
        n = by_id.get(nid) or {}
        order = n.get("order")
        o = order if isinstance(order, int) else 10**9
        return (o, nid)

    out_lines: List[str] = []
    out_lines.append(f"### {title}")
    out_lines.append(f"Source: `{frame_path.relative_to(REPO_ROOT)}`")

    def emit_text(n: Dict[str, Any]) -> None:
        kind = str(n.get("kind") or "")
        nid = str(n.get("id") or "")
        label = str(n.get("label") or "")
        ttl = str(n.get("title") or "")
        hdr = label or ttl or nid
        if kind == "section":
            out_lines.append("")
            out_lines.append(f"#### {hdr}")
            return
        if kind in ("clause", "paragraph"):
            txt = str(n.get("text") or "").strip()
            if txt:
                out_lines.append("")
                out_lines.append(txt)
            return
        if kind == "term":
            summ = str(n.get("summary") or "").strip()
            if summ:
                out_lines.append("")
                out_lines.append(f"{hdr}: {summ}")

    if root and children:
        # Determine which sections to include
        root_kids = sorted(children.get(root, []), key=node_order)
        for kid in root_kids:
            n = by_id.get(kid)
            if not isinstance(n, dict):
                continue
            if str(n.get("kind")) != "section":
                continue
            if section_ids is not None and str(n.get("id")) not in section_ids:
                continue

            emit_text(n)
            sec_kids = sorted(children.get(str(n.get("id")), []), key=node_order)
            for sid in sec_kids:
                sn = by_id.get(sid)
                if isinstance(sn, dict):
                    emit_text(sn)

        text = "\n".join(out_lines).rstrip() + "\n"
        return {
            "title": title,
            "path": str(frame_path.relative_to(REPO_ROOT)),
            "text": text[:max_chars],
        }

    # Fallback: raw YAML head
    raw = _read_file_head(frame_path, max_lines=200)
    text = "\n".join(out_lines) + "\n\n```yaml\n" + raw + "```\n"
    return {"title": title, "path": str(frame_path.relative_to(REPO_ROOT)), "text": text[:max_chars]}


def apply_budget(sections: List[Tuple[str, str]], *, max_chars: int) -> Tuple[str, Dict[str, Any]]:
    """Concatenate (title, body) sections into a single markdown doc under a byte budget."""

    used = 0
    out: List[str] = []
    cuts: List[Dict[str, Any]] = []

    for title, body in sections:
        chunk = body
        if used + len(chunk) > max_chars:
            remain = max_chars - used
            if remain <= 0:
                cuts.append({"section": title, "included_chars": 0, "truncated": True})
                break
            chunk = chunk[:remain]
            cuts.append({"section": title, "included_chars": remain, "truncated": True})
            out.append(chunk)
            used += len(chunk)
            break
        out.append(chunk)
        used += len(chunk)
        cuts.append({"section": title, "included_chars": len(chunk), "truncated": False})

    meta = {"max_chars": max_chars, "used_chars": used, "sections": cuts}
    return "".join(out), meta


def render_markdown(report: Dict[str, Any], *, max_chars: int) -> Tuple[str, Dict[str, Any]]:
    laws = report.get("laws", {})
    tools = report.get("tools", [])
    workflows = report.get("workflows", [])

    tool_excerpts = report.get("tool_excerpts", [])
    law_excerpts = report.get("law_excerpts", [])

    sections: List[Tuple[str, str]] = []

    header: List[str] = []
    header.append("<!-- AUTOGENERATED: do not edit by hand. -->")
    header.append("# Copilot Instructions — framecodex")
    header.append("")

    header.append("## Project charter")
    header.append("This repository is a deterministic publication + documentation pipeline over GF0 frames.")
    header.append("Generated documentation and publication artifacts MUST be reproducible.")
    header.append("")

    header.append("## Non-negotiable invariants")
    header.append("- Frames are the single source of truth (`frames/**/v*/frame.yml`).")
    header.append("- Generated docs (`docs/**/README.md`, `docs/MANIFEST.json`) are produced by the pipeline, not edited manually.")
    header.append("- `out/` is transient and MUST remain gitignored.")
    header.append("")

    header.append("## Repo laws (normative)")
    for key in sorted(laws.keys()):
        l = laws[key]
        header.append(f"- **{key}**: `{l['graph_id']}` v{l['version']} (`{l['path']}`)")
    header.append("")

    header.append("## Golden gates (run before/after changes)")
    header.append("- `tools/enforce_repo_law/run` (policy + validators)")
    header.append("- `tools/render_docs/run` (regenerate docs deterministically)")
    header.append("- `tools/no_diff/run` (reproducibility check)")
    header.append("")

    header.append("## Tool entrypoints")
    for t in tools:
        header.append(f"- `{t['id']}`: `{t['entrypoint']}`")
    header.append("")

    header.append("## CI workflows")
    for wf in workflows:
        header.append(f"- `{wf['path']}` — {wf.get('name','')}")
        for j in wf.get("jobs", []):
            jname = j.get("name") or ""
            suffix = f" — {jname}" if jname else ""
            header.append(f"  - job `{j['id']}`{suffix}")
            steps = j.get("steps") or []
            if steps:
                for s in steps:
                    header.append(f"    - step: {s}")
    header.append("")

    header.append("## How to work in this repo")
    header.append("- Prefer editing source frames and tools; then regenerate docs.")
    header.append("- If asked to change a generated README, locate its frame under `frames/**/v*/frame.yml` and edit there.")
    header.append("- Keep builds deterministic: avoid timestamps, randomness, and network access in generators.")
    header.append("")

    sections.append(("header", "\n".join(header).rstrip() + "\n\n"))

    # Context pack
    cp: List[str] = []
    cp.append("## Context pack (autogenerated excerpts)")
    cp.append("This section embeds authoritative excerpts from repo laws and tooling to provide local, offline context for agents.")
    cp.append("")

    # Law excerpts
    for ex in law_excerpts:
        cp.append(ex.get("text", "").rstrip())
        cp.append("")

    # Tool excerpts
    cp.append("### Tool excerpts (headers)")
    cp.append("The following are short excerpts from tool entrypoints for quick orientation.")
    cp.append("")
    for t in tool_excerpts:
        cp.append(f"#### tools/{t['id']}")
        cp.append(f"Source: `{t['path']}`")
        cp.append("")
        cp.append("```")
        cp.append((t.get("excerpt") or "").rstrip())
        cp.append("```")
        cp.append("")

    sections.append(("context-pack", "\n".join(cp).rstrip() + "\n"))

    md, budget_meta = apply_budget(sections, max_chars=max_chars)
    return md, budget_meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO_ROOT / ".github" / "copilot-instructions.md"))
    ap.add_argument("--max-chars", type=int, default=180_000)
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    laws: Dict[str, Dict[str, str]] = {}

    law_paths = {
        "RepoLaw-K1": REPO_ROOT / "frames" / "repo" / "law" / "governance" / "repo-law-k1" / "v0.1.0" / "frame.yml",
        "InlineMarkup-K1": REPO_ROOT / "frames" / "repo" / "law" / "text" / "inline-markup-k1" / "v0.1.0" / "frame.yml",
    }

    # Kernel specs (extra context for agents)
    spec_paths = {
        "GF0-K1": REPO_ROOT / "frames" / "_kernel" / "spec" / "gf" / "gf0-k1" / "v0.3.0" / "frame.yml",
        "SpecFrame-K1": REPO_ROOT / "frames" / "_kernel" / "spec" / "spec" / "specframe-k1" / "v0.3.0" / "frame.yml",
    }

    for k in sorted(law_paths.keys()):
        p = law_paths[k]
        if p.exists():
            gid, ver = find_frame(p)
            laws[k] = {"graph_id": gid, "version": ver, "path": str(p.relative_to(REPO_ROOT))}
        else:
            laws[k] = {"graph_id": "", "version": "", "path": str(p.relative_to(REPO_ROOT))}

    workflows = list_workflows()
    tools = list_tools()

    # Excerpts (big context)
    law_excerpts = []
    if law_paths["RepoLaw-K1"].exists():
        law_excerpts.append(
            frame_excerpt(
                law_paths["RepoLaw-K1"],
                title="RepoLaw K1 (condensed excerpt)",
                section_ids=[
                    "section.1.charter",
                    "section.2.paths",
                    "section.3.frames_tree",
                    "section.4.docgroup",
                    "section.5.ci",
                    "section.6.receipts",
                    "section.7.violations",
                ],
                max_chars=20000,
            )
        )

    if law_paths["InlineMarkup-K1"].exists():
        law_excerpts.append(
            frame_excerpt(
                law_paths["InlineMarkup-K1"],
                title="InlineMarkup-K1 (primer excerpt)",
                section_ids=None,
                max_chars=12000,
            )
        )

    # IMPORTANT: include kernel spec context early (before tool excerpts)
    if spec_paths["GF0-K1"].exists():
        law_excerpts.append(
            frame_excerpt(
                spec_paths["GF0-K1"],
                title="GF0-K1 (excerpt)",
                section_ids=None,
                max_chars=22000,
            )
        )

    if spec_paths["SpecFrame-K1"].exists():
        law_excerpts.append(
            frame_excerpt(
                spec_paths["SpecFrame-K1"],
                title="SpecFrame-K1 (excerpt)",
                section_ids=None,
                max_chars=22000,
            )
        )

    report: Dict[str, Any] = {
        "tool": {"id": "gen_copilot_instructions", "version": "0.2.0"},
        "laws": laws,
        "tools": tools,
        "workflows": workflows,
        "law_excerpts": law_excerpts,
        "tool_excerpts": list_tool_excerpts(max_lines=80),
    }

    md, budget_meta = render_markdown(report, max_chars=int(args.max_chars))

    content = "".join(md)
    if len(content) > args.max_chars:
        content = content[: args.max_chars].rstrip() + "\n"

    out_path.write_text(content, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
