"""Publication TeX Inline authoring shortcut: tex-inline-v0.

This implements a tiny deterministic parser that converts a single string into
PubTeX Inline IR (canonical: kind=pub-tex-inline-v0, nodes=[...]).

Authoring form:
- {{m:...}} : math segment (validated later; renderer emits in math mode)
- {{c:...}} : code segment (inline monospaced)
- everything else: text segment (escaped in TeX renderer)

Escapes (v0):
- \{{ renders literal '{{'
- \}} renders literal '}}'

Constraints (v0):
- No nesting of {{...}} blocks.
- Blocks must be closed with '}}'.

Determinism:
- Single-pass scan
- No regex backtracking needed
- No normalization besides coalescing adjacent text segments
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass(frozen=True)
class PubTexParseError:
    code: str
    message: str
    pos: int


def _coalesce_text(nodes: List[Dict[str, str]]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        if n.get("t") == "text" and out and out[-1].get("t") == "text":
            out[-1]["s"] = (out[-1].get("s") or "") + (n.get("s") or "")
        else:
            out.append({"t": str(n.get("t")), "s": str(n.get("s", ""))})
    return out


def parse_tex_inline_v0(s: str) -> Tuple[List[Dict[str, str]], List[PubTexParseError]]:
    """Parse authoring string into PubTeX inline nodes.

    Returns (nodes, errors). On error, best-effort nodes may still be returned,
    but callers should treat any error as fatal in repo gates.
    """

    src = s or ""
    nodes: List[Dict[str, str]] = []
    errs: List[PubTexParseError] = []

    i = 0
    n = len(src)

    def emit_text(t: str) -> None:
        if t:
            nodes.append({"t": "text", "s": t})

    buf: List[str] = []

    while i < n:
        ch = src[i]

        # Escaped literal delimiters.
        if src.startswith(r"\{{", i):
            buf.append("{{")
            i += 3
            continue
        if src.startswith(r"\}}", i):
            buf.append("}}")
            i += 3
            continue

        # Start of a typed block.
        if src.startswith("{{", i):
            emit_text("".join(buf))
            buf = []

            start = i
            i += 2

            # Must have tag prefix like 'm:' or 'c:'.
            if i + 1 >= n:
                errs.append(PubTexParseError("PUBTEX.E.BAD_DELIM", "unterminated '{{'", start))
                break

            tag = src[i]
            if i + 1 >= n or src[i + 1] != ":":
                errs.append(PubTexParseError("PUBTEX.E.BAD_TAG", "expected '{{m:...}}' or '{{c:...}}'", start))
                # best-effort: treat '{{' literally
                buf.append("{{")
                i = start + 2
                continue

            if tag not in ("m", "c"):
                errs.append(PubTexParseError("PUBTEX.E.UNKNOWN_TAG", f"unknown tag '{tag}'", start))
                buf.append("{{")
                i = start + 2
                continue

            i += 2  # consume '<tag>:'

            # Scan until matching '}}' (no nesting allowed).
            j = src.find("}}", i)
            if j == -1:
                errs.append(PubTexParseError("PUBTEX.E.BAD_DELIM", "missing closing '}}'", start))
                break

            content = src[i:j]
            i = j + 2

            if tag == "m":
                nodes.append({"t": "math", "s": content})
            else:
                nodes.append({"t": "code", "s": content})
            continue

        buf.append(ch)
        i += 1

    emit_text("".join(buf))

    return _coalesce_text(nodes), errs


def to_ir(nodes: List[Dict[str, str]]) -> Dict[str, object]:
    return {"kind": "pub-tex-inline-v0", "nodes": nodes}
