# InlineMarkup-K1 — Deterministic Inline/Block Markup for Freeform Text
<a id="law-repo-text-inline-markup-k1-6221b519"></a>

## Charter
<a id="section-1-charter-6790fc7e"></a>

InlineMarkup-K1 is a **deterministic** and **constrained** markup subset for GF0 freeform text fields.

It is designed to:

```
- eliminate ambiguous CommonMark behaviors
- guarantee deterministic rendering across Markdown and LaTeX
- prevent unsafe raw-HTML injection in documentation outputs
```

InlineMarkup-K1 is intentionally small; authors MUST prefer frame structure (sections, paragraphs, lists as structure where available) over rich Markdown syntax.

## Text Format Modes
<a id="section-2-modes-0d54ca89"></a>

A freeform text field that participates in InlineMarkup-K1 MUST declare a `text.format` mode:

```
- plain: treat as raw text (no markup parsing)
- md-inline: parse as a single paragraph with inline constructs
- md-block: parse paragraphs and fenced code blocks; inline constructs allowed inside paragraphs
```

## Allowed Constructs (v0.1)
<a id="section-3-allowed-c2fad31a"></a>

Inline constructs (v0.1):

```
- strong: **x**
- emphasis: *x* or _x_
- inline code: `x`
- inline math: $x$
- links: [label](url)
```

Block constructs (md-block only):

```
- fenced code blocks: ```lang\n...\n```
- paragraphs separated by blank lines
```

## Disallowed Constructs
<a id="section-4-disallowed-fda64806"></a>

The following are disallowed under this law:

```
- raw HTML tags (validator MUST reject HTML-tag-like sequences)
- headings, tables, and other rich Markdown block constructs
```

Note: Angle brackets used for grammar/metasyntax (e.g., `<scheme>`) are not intrinsically disallowed; only HTML-tag-like sequences are rejected.

## Validation Requirements
<a id="section-5-validation-ae9a4b61"></a>

The repository MUST validate InlineMarkup-K1 wherever it is enabled.

Minimum required violation codes (stable identifiers):

```
- TEXT.E.HTML_DISALLOWED
- TEXT.E.BAD_TEXT_FORMAT
- TEXT.E.BAD_CODEFENCE
```

Validation MUST be deterministic and MUST NOT depend on locale, time, network, or unstable parser behaviors.

## Deterministic Rendering Requirements
<a id="section-6-rendering-7b891664"></a>

Render projections MUST be derived from a structured MarkupIR AST (not raw Markdown).

```
- DocIR projection MUST include the MarkupIR structure for InlineMarkup-K1 fields
- Markdown rendering MUST be deterministic from MarkupIR
- LaTeX rendering MUST be deterministic from MarkupIR
```

## Repo Integration
<a id="section-7-integration-114f38a5"></a>

Repo enforcement MUST run InlineMarkup-K1 validation as part of repo law gates.

This law is intended to be applied under RepoLaw K1 (see: `law://repo/governance/repo-law-k1`).

Specifically:

```
- tools/enforce_repo_law/run MUST execute tools/validate_inline_markup/run.py
- CI MUST fail if InlineMarkup-K1 validation fails
```

## Changelog
<a id="section-8-changelog-4986b171"></a>

- v0.1.0 (2026-01-04): initial normative definition and enforcement requirements.

## Examples
<a id="section-3-1-examples-3446b206"></a>

**Example: InlineMarkup-K1** _(normative)_

This clause demonstrates InlineMarkup-K1 rendering across targets.

Inline: - strong: **bold** - emphasis: *emph* - code: `x := 1` - math: $E=mc^2$ - link: [FrameURL K1](law://_kernel/id/frameurl-k1)

Block code fence:

```python
def f(x: int) -> int:
    return x + 1
```

DocIR render pipeline: tools/render_docir

FrameURL K1: law://_kernel/id/frameurl-k1

GF0 K1: spec://_kernel/gf/gf0-k1

LawFrame K1: law://_kernel/law/lawframe-k1

DocIR → Markdown renderer: tools/render*md*doc

DocIR → LaTeX renderer: tools/render*tex*doc

RepoLaw K1: law://repo/governance/repo-law-k1

InlineMarkup-K1 validator: tools/validate*inline*markup

## InlineMarkup-K1
<a id="title-0-52934cc7"></a>
