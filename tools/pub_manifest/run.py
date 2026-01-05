#!/usr/bin/env python3
"""Write a deterministic publication manifest.

Usage:
  tools/pub_manifest/run.py --frame <frame.yml> --src <srcdir> --pdf <pdfpath> --out <MANIFEST.json>

The manifest records hashes and build context (commit SHA if available).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head_sha(root: Path) -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(root))
        return out.decode("utf-8").strip()
    except Exception:
        return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo_root = Path.cwd()
    frame = Path(args.frame)
    src = Path(args.src)
    pdf = Path(args.pdf)
    out = Path(args.out)

    data: Dict[str, Any] = {
        "version": "0.1.0",
        "commit": git_head_sha(repo_root),
        "inputs": {
            "frame_path": str(frame),
            "frame_sha256": sha256_file(frame),
        },
        "outputs": {
            "main_tex_path": str(src / "main.tex"),
            "main_tex_sha256": sha256_file(src / "main.tex"),
            "pdf_path": str(pdf),
            "pdf_sha256": sha256_file(pdf),
        },
        "tooling": {
            "render_latex_spec": "0.1.0",
            "pub_build_pdf": "0.1.0",
        },
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
