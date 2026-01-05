# InlineMarkup-K1 Adoption Style Guide

## Overview
This guide defines conventions for applying **InlineMarkup-K1** to freeform text fields across the framecodex repository.

Goal: **Improve readability of rendered docs (Markdown, LaTeX) without changing semantics.**

---

## When to Use Markup

### Use `text.format: md-inline`
- Single paragraph with **inline elements only**
- Emphasis, code, links, inline math
- **Examples**: short definitions, labels, one-liners

### Use `text.format: md-block`
- Multiple paragraphs separated by blank lines
- Fenced code blocks
- Lists (though native markup lists are NOT supported; use fenced blocks or paragraph formatting)
- **Examples**: detailed explanations, examples, multi-step descriptions

### Use `text.format: plain` (or omit `text.format`)
- Plain text with no markup
- When field contains YAML syntax or parser-sensitive content
- When no markup patterns are beneficial

---

## Markup Conventions

### Identifiers & Paths
Use **inline code backticks** for:
- File/directory paths: `` `frames/repo/law/**` ``
- Command-line flags: `` `--flag` ``
- Identifiers: `` `graph_id` ``, `` `node.id` ``
- FrameURLs (when short): `` `law://repo/governance/repo-law-k1` ``

### Emphasis
- **Bold** for strong emphasis: `**MUST**, **MUST NOT**, **required**`
- *Italic* for loose emphasis: `*e.g.*, *optional*`

### Code & Examples
- Inline code: `` `snake_case`, `const_LIKE_THIS`, `CamelCase` ``
- Fenced code blocks for multi-line examples:
  ```
  ```yaml
  key: value
  nested:
    field: 123
  ```
  ```

### Links
Format: `[label](url)`

Examples:
- `[RepoLaw K1](law://repo/governance/repo-law-k1)`
- `[Section 2](law://_kernel/spec/gf/gf0-k1#section.2.graph_frame_structure)`

*Note:* GitHub Markdown won't resolve `law://` URLs, but renderers (LaTeX, custom renderers) will handle them. Text is always readable.

### Lists
InlineMarkup-K1 does **not** support native Markdown lists (lines starting with `-`, `*`, or `+`).

**Instead:**

Option A: Use a fenced code block if list structure is important:
```
```
- item 1
- item 2
- item 3
```
```

Option B: Prose with paragraph breaks:
```
Item 1 description. Item 2 description. Item 3 description.
```

### Math
Inline math using `$...$`:
- `$E = mc^2$`
- `$\sigma, \chi, \Gamma$` (Greek letters)

---

## What NOT to Change

**NEVER modify:**
- node `id`, `kind`, `status`, `profile`
- `graph_id`, `version`
- edge structure (`from`, `to`, `type`)
- machine-consumed fields (e.g., `symbols`, validator code patterns, regex)
- Literal code snippets that validation or tools depend on (keep exact bytes if possible; use code fences for formatting)

**SAFE to modify:**
- `text`, `summary`, `title`, `label`, `desc` (content only)
- Add `text.format` attribute when enabling markup
- Doc-oriented attrs (description strings, not structural/semantic fields)

---

## Workflow

1. **Audit**: Run `tools/markup_audit/run` to discover candidates.
2. **Edit**: Apply markup to a small batch (e.g., one frame).
3. **Verify invariants**: Run `tools/semantic_invariants/run --before <old> --after <new>`.
4. **Regenerate**: Run `tools/render_docs/run` to update docs.
5. **Check reproducibility**: Run `tools/no_diff/run`.
6. **Commit**: Include both frame changes and regenerated docs.

---

## Example: Before & After

### Before
```yaml
nodes:
  - id: clause.1.example
    kind: clause
    status: informative
    label: A simple example
    text: "This is a clause text. The law applies to frames/ directory. See law://repo/governance/repo-law-k1 for details."
```

### After
```yaml
nodes:
  - id: clause.1.example
    kind: clause
    status: informative
    label: A simple example
    text: "This is a clause text. The law applies to `frames/` directory. See [RepoLaw K1](law://repo/governance/repo-law-k1) for details."
    attrs:
      - key: text.format
        value: md-inline
```

Rendered Markdown:
> This is a clause text. The law applies to `frames/` directory. See [RepoLaw K1](law://repo/governance/repo-law-k1) for details.

---

## FAQ

**Q: Should I rewrite ALL text?**
A: No. Focus on high-value improvements (code, paths, emphasis). Plain prose without markup patterns is fine as-is.

**Q: What if I'm unsure?**
A: Run the audit tool; it recommends `md-inline` or `md-block` based on detected patterns. Review manually before committing.

**Q: Can I use headings?**
A: **No.** InlineMarkup-K1 is intentionally small; headings are not allowed. Use frame structure (sections, nodes) instead.

**Q: What about tables?**
A: **Not supported.** Use fenced code blocks or structure as multiple clause nodes.

**Q: How do I test my changes?**
A: Use the semantic invariants checker, render docs, run no_diff, and review the generated Markdown.
