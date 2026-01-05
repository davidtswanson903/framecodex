from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def stable_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str) -> str:
    return sha256_bytes(s.encode("utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text_deterministic(path: Path, s: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if not s.endswith("\n"):
        s += "\n"
    path.write_text(s, encoding="utf-8", newline="\n")
