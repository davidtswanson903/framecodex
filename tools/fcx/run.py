#!/usr/bin/env python3
"""fcx wrapper.

This is an incremental entrypoint for the kernelized tooling library under `py/fcx`.

Usage examples:
  tools/fcx/run.py validate-frame --frame frames/.../frame.yml

Determinism:
- offline only
- no timestamps
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_import_path() -> None:
    # Allow importing `py/fcx` without installation.
    repo_root = Path(__file__).resolve().parents[2]
    py_dir = repo_root / "py"
    if str(py_dir) not in sys.path:
        sys.path.insert(0, str(py_dir))


def main() -> int:
    _ensure_import_path()
    from fcx.cli import main as cli_main  # noqa: WPS433

    return int(cli_main(sys.argv[1:]))


if __name__ == "__main__":
    raise SystemExit(main())
