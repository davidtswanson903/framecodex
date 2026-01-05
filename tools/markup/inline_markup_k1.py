#!/usr/bin/env python3
"""InlineMarkup-K1: deterministic, constrained markup parser/printer.

Goal
- Provide a tiny, normative subset of markup for GF0 freeform text fields.
- Deterministic parsing & rendering across targets (Markdown/LaTeX/Plain).
- Reject disallowed or ambiguous constructs (not a CommonMark parser).

Supported (v0.1)
- Inline: strong (**x**), emphasis (*x* or _x_), inline code (`x`), math ($x$), links ([label](url))
- Block (md-block only): fenced code blocks (```lang ... ```), blank-line separated paragraphs

Disallowed
- Raw HTML (any '<' or '>' characters)
- Headings/tables/etc (not recognized; authors must use structure, not markdown)

This module is intentionally small and strict.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import re


# -------------------------
# Errors / violation codes
# -------------------------


@dataclass(frozen=True)
class MarkupError:
    code: str
    message: str
    pos: int = 0


def _err(code: str, message: str, pos: int) -> MarkupError:
    return MarkupError(code=code, message=message, pos=pos)


# -------------------------
# AST helpers (JSON-serializable)
# -------------------------


def text_node(s: str) -> Dict[str, Any]:
    return {"t": "text", "s": s}


def wrap_node(t: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"t": t, "c": children}


def leaf_node(t: str, s: str) -> Dict[str, Any]:
    return {"t": t, "s": s}


def link_node(label_children: List[Dict[str, Any]], url: str) -> Dict[str, Any]:
    return {"t": "link", "c": label_children, "url": url}


_HTML_TAG_LIKE = re.compile(r"<\s*/?\s*(a|p|div|span|br|hr|img|code|pre|em|strong|ul|ol|li|table|thead|tbody|tr|td|th|h[1-6])\b[^>]*>", re.IGNORECASE)


# -------------------------
# Parsing (deterministic)
# -------------------------


def parse(text: str, *, mode: str) -> Tuple[Dict[str, Any], List[MarkupError]]:
    """Parse text to MarkupIR.

    mode:
      - plain: treat as raw text (no markup)
      - md-inline: allow only inline markup
      - md-block: allow fenced code blocks + paragraphs; inline markup inside paragraphs

    Return: (ast, errors)
      ast is a dict with keys: {"kind": "inline-markup-k1", "mode": <mode>, "blocks": [...]}
    """

    # Normalize newlines deterministically.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    errors: List[MarkupError] = []

    # Disallow raw HTML tags (but allow angle brackets used for grammar like <scheme>). 
    m = _HTML_TAG_LIKE.search(text)
    if m is not None:
        errors.append(
            _err(
                "TEXT.E.HTML_DISALLOWED",
                "Raw HTML tags are not allowed in InlineMarkup-K1",
                m.start(),
            )
        )

    if mode == "plain":
        return ({"kind": "inline-markup-k1", "mode": mode, "blocks": [{"t": "paragraph", "c": [text_node(text)]}]}, errors)

    if mode not in ("md-inline", "md-block"):
        errors.append(_err("TEXT.E.BAD_TEXT_FORMAT", f"Unknown text.format: {mode}", 0))
        return ({"kind": "inline-markup-k1", "mode": mode, "blocks": [{"t": "paragraph", "c": [text_node(text)]}]}, errors)

    if mode == "md-inline":
        # Inline fields are treated as a single paragraph.
        inl, e2 = _parse_inline(text)
        errors.extend(e2)
        return ({"kind": "inline-markup-k1", "mode": mode, "blocks": [{"t": "paragraph", "c": inl}]}, errors)

    # md-block
    blocks: List[Dict[str, Any]] = []
    i = 0
    n = len(text)

    def startswith_at(prefix: str, j: int) -> bool:
        return text.startswith(prefix, j)

    # Split into blocks: fenced code blocks and paragraphs separated by blank lines.
    while i < n:
        # Skip leading blank lines
        while i < n and text[i] == "\n":
            i += 1
        if i >= n:
            break

        # Code fence must be at start of line
        line_start = i == 0 or text[i - 1] == "\n"
        if line_start and startswith_at("```", i):
            # parse fence header
            j = i + 3
            # language until newline
            lang = ""
            while j < n and text[j] != "\n":
                lang += text[j]
                j += 1
            if j < n and text[j] == "\n":
                j += 1
            # find closing fence at line start
            code_start = j
            k = j
            close = None
            while k < n:
                if (k == 0 or text[k - 1] == "\n") and text.startswith("```", k):
                    close = k
                    break
                k += 1
            if close is None:
                errors.append(_err("TEXT.E.BAD_CODEFENCE", "Unterminated code fence", i))
                # treat rest as text
                rest = text[i:]
                inl, e2 = _parse_inline(rest)
                errors.extend(e2)
                blocks.append({"t": "paragraph", "c": inl})
                break

            code = text[code_start:close]
            # strip a single trailing newline in code for stability
            if code.endswith("\n"):
                code = code[:-1]
            blocks.append({"t": "code_fence", "lang": lang.strip() or "", "code": code})

            # consume closing fence line
            k2 = close + 3
            while k2 < n and text[k2] != "\n":
                k2 += 1
            if k2 < n and text[k2] == "\n":
                k2 += 1
            i = k2
            continue

        # Paragraph: consume until blank line or code fence at line start
        para_lines: List[str] = []
        while i < n:
            # stop at blank line
            if text[i] == "\n":
                # check if next is also newline (blank line)
                if i + 1 < n and text[i + 1] == "\n":
                    break
                # include single newline within paragraph as space
                para_lines.append("\n")
                i += 1
                continue
            # stop if next token is a code fence at line start
            if (i == 0 or text[i - 1] == "\n") and text.startswith("```", i):
                break
            # normal char
            para_lines.append(text[i])
            i += 1

        para = "".join(para_lines)
        # Normalize newlines within paragraph to single spaces for md output stability.
        # (LaTeX will treat this as a paragraph body too.)
        para = " ".join([ln.strip() for ln in para.split("\n")]).strip()
        inl, e2 = _parse_inline(para)
        errors.extend(e2)
        blocks.append({"t": "paragraph", "c": inl})

        # Consume blank lines
        while i < n and text[i] == "\n":
            i += 1

    return ({"kind": "inline-markup-k1", "mode": mode, "blocks": blocks}, errors)


def _parse_inline(s: str) -> Tuple[List[Dict[str, Any]], List[MarkupError]]:
    """Parse inline markup for a single line/paragraph.

    This is a strict parser with limited nesting and deterministic precedence.
    """

    errors: List[MarkupError] = []

    out: List[Dict[str, Any]] = []
    i = 0
    n = len(s)

    def emit_text(t: str) -> None:
        if not t:
            return
        # merge adjacent text nodes deterministically
        if out and out[-1].get("t") == "text":
            out[-1]["s"] = str(out[-1].get("s", "")) + t
        else:
            out.append(text_node(t))

    while i < n:
        ch = s[i]

        # inline code
        if ch == "`":
            j = s.find("`", i + 1)
            if j == -1:
                errors.append(_err("TEXT.E.UNBALANCED_DELIMS", "Unterminated inline code", i))
                emit_text(s[i:])
                break
            code = s[i + 1 : j]
            out.append(leaf_node("code", code))
            i = j + 1
            continue

        # math inline
        if ch == "$":
            j = s.find("$", i + 1)
            if j == -1:
                errors.append(_err("TEXT.E.UNBALANCED_DELIMS", "Unterminated inline math", i))
                emit_text(s[i:])
                break
            math = s[i + 1 : j]
            out.append(leaf_node("math", math))
            i = j + 1
            continue

        # strong (**...**)
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j == -1:
                errors.append(_err("TEXT.E.UNBALANCED_DELIMS", "Unterminated strong (**)", i))
                emit_text(s[i:])
                break
            inner = s[i + 2 : j]
            kids, e2 = _parse_inline(inner)
            errors.extend(e2)
            out.append(wrap_node("strong", kids))
            i = j + 2
            continue

        # emphasis (*...*) or _..._
        if ch in ("*", "_"):
            delim = ch
            j = s.find(delim, i + 1)
            if j == -1:
                # treat as literal
                emit_text(delim)
                i += 1
                continue
            inner = s[i + 1 : j]
            kids, e2 = _parse_inline(inner)
            errors.extend(e2)
            out.append(wrap_node("emph", kids))
            i = j + 1
            continue

        # link [label](url)
        if ch == "[":
            close = s.find("]", i + 1)
            if close != -1 and close + 1 < n and s[close + 1] == "(":
                end = s.find(")", close + 2)
                if end != -1:
                    label = s[i + 1 : close]
                    url = s[close + 2 : end]
                    kids, e2 = _parse_inline(label)
                    errors.extend(e2)
                    out.append(link_node(kids, url))
                    i = end + 1
                    continue
                errors.append(_err("TEXT.E.LINK_SYNTAX", "Unterminated link url", i))
            # fallthrough as literal

        # default: literal char
        emit_text(ch)
        i += 1

    return out, errors


# -------------------------
# Rendering
# -------------------------


def render_markdown(ast: Dict[str, Any]) -> str:
    """Render MarkupIR to Markdown deterministically."""

    blocks = ast.get("blocks") or []
    out: List[str] = []
    for b in blocks:
        if not isinstance(b, dict):
            continue
        t = b.get("t")
        if t == "code_fence":
            lang = str(b.get("lang") or "").strip()
            code = str(b.get("code") or "")
            out.append(f"```{lang}".rstrip())
            out.extend(code.split("\n"))
            out.append("```")
            out.append("")
            continue
        if t == "paragraph":
            out.append(_render_inline_md(b.get("c") or []))
            out.append("")
            continue
        # unknown block
        out.append(_render_inline_md([text_node(f"[unhandled:{t}]")]))
        out.append("")
    return "\n".join(ln.rstrip() for ln in out).rstrip() + "\n"


def _render_inline_md(nodes: List[Dict[str, Any]]) -> str:
    out: List[str] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        t = n.get("t")
        if t == "text":
            out.append(str(n.get("s", "")))
        elif t == "emph":
            out.append("*" + _render_inline_md(n.get("c") or []) + "*")
        elif t == "strong":
            out.append("**" + _render_inline_md(n.get("c") or []) + "**")
        elif t == "code":
            out.append("`" + str(n.get("s", "")) + "`")
        elif t == "math":
            out.append("$" + str(n.get("s", "")) + "$")
        elif t == "link":
            out.append("[" + _render_inline_md(n.get("c") or []) + "](" + str(n.get("url", "")) + ")")
        else:
            out.append(str(n.get("s", "")))
    return "".join(out)


_LATEX_ESC_MAP = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def _tex_escape(s: str) -> str:
    return "".join(_LATEX_ESC_MAP.get(ch, ch) for ch in s)


def render_latex(ast: Dict[str, Any]) -> str:
    """Render MarkupIR to LaTeX body content (not full document)."""

    blocks = ast.get("blocks") or []
    out: List[str] = []
    for b in blocks:
        if not isinstance(b, dict):
            continue
        t = b.get("t")
        if t == "code_fence":
            code = str(b.get("code") or "")
            out.append(r"\begin{verbatim}")
            out.extend(code.split("\n"))
            out.append(r"\end{verbatim}")
            out.append("")
            continue
        if t == "paragraph":
            out.append(_render_inline_tex(b.get("c") or []))
            out.append("")
            continue
        out.append(_tex_escape(f"[unhandled:{t}]"))
        out.append("")
    return "\n".join(ln.rstrip() for ln in out).rstrip() + "\n"


def _render_inline_tex(nodes: List[Dict[str, Any]]) -> str:
    out: List[str] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        t = n.get("t")
        if t == "text":
            out.append(_tex_escape(str(n.get("s", ""))))
        elif t == "emph":
            out.append(r"\emph{" + _render_inline_tex(n.get("c") or []) + "}")
        elif t == "strong":
            out.append(r"\textbf{" + _render_inline_tex(n.get("c") or []) + "}")
        elif t == "code":
            out.append(r"\texttt{" + _tex_escape(str(n.get("s", ""))) + "}")
        elif t == "math":
            # math content is not escaped; treated as math mode
            out.append("$" + str(n.get("s", "")) + "$")
        elif t == "link":
            out.append(r"\href{" + _tex_escape(str(n.get("url", ""))) + "}{" + _render_inline_tex(n.get("c") or []) + "}")
        else:
            out.append(_tex_escape(str(n.get("s", ""))))
    return "".join(out)
