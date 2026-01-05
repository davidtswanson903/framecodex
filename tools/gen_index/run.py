#!/usr/bin/env python3
"""Generate a human-friendly root index of frames and publications.

Writes `INDEX.md` at repo root.

Design goals:
- Deterministic output (stable ordering).
- No external dependencies.
- Best-effort: includes a "Core publications" section based on `pub.*` attrs
  found on root `spec` nodes.

This is intentionally conservative: it only relies on:
- `governance/publications/registry.yml`
- `frames/**/frame.yml`

If you later want richer navigation (grouping by domain/version), extend the
`collect_frames()` step.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml_minimal(path: Path) -> Any:
    """Minimal YAML loader.

    This repo already depends on YAML in other tooling, but this generator should
    not assume PyYAML is installed. We therefore only parse the small registry
    file using a very small subset.

    Supported:
    - top-level mappings
    - nested mappings
    - scalar strings

    If parsing fails, we raise with a clear message.

    NOTE: If you prefer, we can switch this to PyYAML and add it as a dependency.
    """

    # Very small indentation-based parser for `registry.yml` shape.
    lines = [ln.rstrip("\n") for ln in read_text(path).splitlines()]
    stack: List[Tuple[int, Dict[str, Any]]] = [(0, {})]

    for raw in lines:
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Unsupported YAML line (no ':'): {raw}")

        indent = len(raw) - len(raw.lstrip(" "))
        key, rest = line.split(":", 1)
        key = key.strip()
        value = rest.strip()

        # find parent
        while stack and indent < stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"Bad indentation in {path}: {raw}")

        cur = stack[-1][1]

        if value == "":
            nxt: Dict[str, Any] = {}
            cur[key] = nxt
            stack.append((indent + 2, nxt))
        else:
            # strip quotes if present
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            cur[key] = value

    return stack[0][1]


def find_attr(attrs: Any, key: str) -> Optional[str]:
    if not isinstance(attrs, list):
        return None
    for a in attrs:
        if isinstance(a, dict) and a.get("key") == key:
            v = a.get("value")
            return v if isinstance(v, str) else None
    return None


def find_attrs_json(attrs: Any, key: str) -> Optional[Any]:
    v = find_attr(attrs, key)
    if v is None:
        return None
    try:
        return json.loads(v)
    except Exception:
        return None


@dataclass(frozen=True)
class PubDoc:
    graph_id: str
    version: str
    title: str
    bundle_path: str
    pdf_name: str
    pub_version: str


def collect_pub_docs(frames_root: Path) -> List[PubDoc]:
    docs: List[PubDoc] = []

    for frame_path in sorted(frames_root.glob("**/frame.yml")):
        # Parse as YAML-ish by a minimal heuristic: this file is real YAML, but
        # we only need a few top-level fields and the root node attrs.
        text = read_text(frame_path)
        if "graph_id:" not in text or "nodes:" not in text:
            continue

        # crude extraction: load via json-like scanning is hard; simplest is to
        # rely on python's stdlib only by using a tiny bit of YAML parsing logic.
        # Here we take an easier path: import yaml if available.
        data: Dict[str, Any]
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(text)
        except Exception:
            # If PyYAML isn't available, skip (CI environments typically have it
            # via other tooling, but we remain safe).
            continue

        graph_id = str(data.get("graph_id") or "")
        version = str(data.get("version") or "")
        nodes = data.get("nodes")
        if not graph_id or not isinstance(nodes, list):
            continue

        root = None
        for n in nodes:
            if isinstance(n, dict) and n.get("kind") == "spec" and n.get("id") == graph_id:
                root = n
                break
        if root is None:
            continue

        attrs = root.get("attrs")
        pub_kind = find_attr(attrs, "pub.kind")
        pub_track = find_attr(attrs, "pub.track")
        bundle_path = find_attr(attrs, "pub.bundle.path")
        pub_version = find_attr(attrs, "pub.version")

        if pub_kind != "spec-paper" or pub_track != "zenodo-record":
            continue
        if not bundle_path or not pub_version:
            continue

        title = str(root.get("title") or graph_id)
        pdf_name = bundle_path.rstrip("/").split("/")[-1] + f"-v{pub_version}"
        # Keep current convention used by workflow names:
        # sigma-k1-v0.1.0, sigma-composition-k1-v0.1.0
        # derive from last two components (name + version) when possible.
        parts = bundle_path.strip("/").split("/")
        if len(parts) >= 2:
            pdf_name = f"{parts[-2]}-v{parts[-1]}" if parts[-1].startswith("v") else f"{parts[-2]}-v{parts[-1]}"
        # but existing uses `...-v0.1.0` (no leading 'v' in version dir). Keep:
        if len(parts) >= 1:
            # last is version like 0.1.0
            # second last is spec name
            if len(parts) >= 2:
                pdf_name = f"{parts[-2]}-v{parts[-1]}"

        docs.append(
            PubDoc(
                graph_id=graph_id,
                version=version,
                title=title,
                bundle_path=bundle_path,
                pdf_name=pdf_name,
                pub_version=pub_version,
            )
        )

    # stable ordering by graph_id
    docs.sort(key=lambda d: d.graph_id)
    return docs


def gh_pages_base() -> str:
    # Best-effort: infer from CITATION.cff repository-code if present.
    cff = REPO_ROOT / "CITATION.cff"
    if cff.exists():
        txt = read_text(cff)
        for ln in txt.splitlines():
            if ln.startswith("repository-code:"):
                url = ln.split(":", 1)[1].strip().strip('"').strip("'")
                # https://github.com/<owner>/<repo>
                parts = url.rstrip("/").split("/")
                if len(parts) >= 2:
                    owner = parts[-2]
                    repo = parts[-1]
                    return f"https://{owner}.github.io/{repo}"
    return ""


def write_index(pub_docs: List[PubDoc], registry: Dict[str, Any]) -> None:
    base = gh_pages_base()
    out = REPO_ROOT / "INDEX.md"

    lines: List[str] = []
    lines.append("# framecodex Index")
    lines.append("")
    lines.append("Human-readable entry points into the `framecodex` corpus.")
    lines.append("")

    lines.append("## Core publications (rendered PDFs)")
    lines.append("")
    if not pub_docs:
        lines.append("(No publication-marked specs found.)")
        lines.append("")
    else:
        for d in pub_docs:
            frame_link = (
                f"[{d.graph_id}]({path_from_root_for_graph(d.graph_id)})"
                if path_from_root_for_graph(d.graph_id)
                else d.graph_id
            )

            # Expected PDF naming convention from workflows:
            #   <spec-name>-v<version>.pdf
            bp = d.bundle_path.strip("/").split("/")
            spec_name = bp[-2] if len(bp) >= 2 else "document"
            ver = bp[-1] if bp else ""
            # Some bundle paths may use either "0.1.0" or "v0.1.0"; workflows name PDFs as -v<semver>.
            ver = ver[1:] if ver.startswith("v") else ver
            pdf_filename = f"{spec_name}-v{ver}.pdf"
            pdf_rel = f"/{d.bundle_path}/out/{pdf_filename}"
            pdf_url = f"{base}{pdf_rel}" if base else pdf_rel

            lines.append(f"- **{d.title}**")
            lines.append(f"  - Frame: {frame_link}")
            lines.append(f"  - PDF (Pages): {pdf_url}")
            lines.append(f"  - Bundle path: `{d.bundle_path}`")

            # registry fields if provided
            pub_docs_reg = registry.get("pub_docs", {}) if isinstance(registry, dict) else {}
            reg_entry = pub_docs_reg.get(d.graph_id)
            if not reg_entry and isinstance(pub_docs_reg, dict):
                reg_entry = pub_docs_reg.get(d.graph_id)
            if isinstance(reg_entry, dict):
                concept = (reg_entry.get("concept_doi") or "").strip()
                latest = (reg_entry.get("latest_version_doi") or "").strip()
                if concept or latest:
                    lines.append("  - Zenodo:")
                    if concept:
                        lines.append(f"    - Concept DOI: {concept}")
                    if latest:
                        lines.append(f"    - Latest version DOI: {latest}")
            lines.append("")

    lines.append("## Kernel specs")
    lines.append("")
    lines.append("- [GF0 (GraphFrame K0)](frames/_kernel/spec/gf/gf0-k1/v0.3.0/frame.yml)")
    lines.append("- [SpecFrame K1](frames/_kernel/spec/spec/specframe-k1/v0.3.0/frame.yml)")
    lines.append("")

    lines.append("## Repository governance")
    lines.append("")
    lines.append("- [Repo law](frames/repo/law/governance/repo-law-k1/v0.1.0/frame.yml)")
    lines.append("- [Publication registry](governance/publications/registry.yml)")
    lines.append("")

    lines.append("## Directories")
    lines.append("")
    lines.append("- [`frames/`](frames/) — source-of-truth specs")
    lines.append("- [`docs/`](docs/) — human docs (if present)")
    lines.append("- [`tools/`](tools/) — validators, renderers, publication tooling")
    lines.append("- [`governance/`](governance/) — policy, registries")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")


def path_from_root_for_graph(graph_id: str) -> str:
    # best-effort: only for the two known core specs we care about right now.
    mapping = {
        "spec://domains/systemics/sigma-k1": "frames/domains/spec/systemics/sigma-k1/v0.1.0/frame.yml",
        "spec://domains/systemics/sigma-composition-k1": "frames/domains/spec/systemics/sigma-composition-k1/v0.1.0/frame.yml",
    }
    return mapping.get(graph_id, "")


def main() -> None:
    frames_root = REPO_ROOT / "frames"
    registry_path = REPO_ROOT / "governance" / "publications" / "registry.yml"

    registry: Dict[str, Any] = {}
    if registry_path.exists():
        try:
            registry = load_yaml_minimal(registry_path)
        except Exception as e:
            raise SystemExit(f"Failed to parse {registry_path}: {e}")

    pub_docs = collect_pub_docs(frames_root)
    write_index(pub_docs, registry)


if __name__ == "__main__":
    main()
