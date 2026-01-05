# Continuation: Phase 4 & 5 — GF0-K1 and SpecFrame-K1 Markup Application

## Session: January 4, 2026

### Summary

Systematically applied **InlineMarkup-K1** formatting to two high-impact kernel specification frames:
1. **GF0-K1** (GraphFrame K0 spec)  
2. **SpecFrame-K1** (SpecFrame K1 spec)

Both frames are foundational to the GraphBrain ecosystem and serve as canonical references for other specs.

---

## Completed Work

### GF0-K1 (62 candidates)
**File:** `frames/_kernel/spec/gf/gf0-k1/v0.3.0/frame.yml`

**Applied:**
- Added `text.format` attrs to **20+ clauses** and **terms**
  - `md-block` for clauses with lists: GraphFrameK0 Fields, NodeK0 Fields, EdgeK0 Fields, AttrK0 Structure, MetricK0 Structure, etc.
  - `md-inline` for clauses without lists: Graph Identity, Graph-level attributes, Edge Integrity, Meta Fractal, Validation rules, etc.
- Enhanced inline markup:
  - Wrapped field names in backticks: `` `graph_id` ``, `` `version` ``, `` `attrs` ``, `` `nodes` ``, `` `edges` ``, `` `meta` ``
  - Wrapped type names in backticks: `` `GraphFrameK0` ``, `` `NodeK0` ``, `` `EdgeK0` ``, `` `AttrK0` ``, `` `MetricK0` ``
  - Bold for normative keywords: `**MUST**`, `**MUST NOT**`, `**MAY**`, `**SHOULD**`
  - Preserved examples and complex structures (e.g., `{graph_id, version, attrs, nodes, edges, meta}`)

**Verification:**
- ✅ Semantic invariants: NO structural changes (IDs, edges, statuses preserved)
- ✅ Reproducibility: `tools/no_diff/run` passed
- ✅ All gates: `tools/enforce_repo_law/run` passed
- ✅ Committed: `feat: apply InlineMarkup-K1 to gf0-k1 (readability + text.format attrs)`

**Rendered output:** `docs/_kernel/spec/gf/gf0-k1/v0.3.0/README.md`
- Backticks appear correctly in markdown
- Bold emphasis renders as expected
- List formatting improved via `md-block`

---

### SpecFrame-K1 (64 candidates)
**File:** `frames/_kernel/spec/spec/specframe-k1/v0.3.0/frame.yml`

**Applied:**
- Added `text.format` attrs to **23 clauses** and **terms**
  - `md-block` for: Node kinds (allowed), Attributes per node kind (spec, section, term, clause, property, example, spec_ref, required), Recommended attrs keys
  - `md-inline` for: Scope, Intended consumers, Edge semantics, Validation rules, Integration usage
- Enhanced inline markup:
  - Wrapped keywords: `` `'spec'` ``, `` `'section'` ``, `` `'term'` ``, `` `'clause'` ``, `` `'property'` ``, `` `'example'` ``, `` `'spec_ref'` ``
  - Wrapped field names: `` `kind` ``, `` `type` ``, `` `status` ``, `` `title` ``, `` `label` ``, etc.
  - Wrapped type names: `` `SpecFrame` ``, `` `NodeK0` ``, `` `EdgeK0` ``, `` `GraphFrameK0` ``
  - Bold: `**MUST**`, `**MUST NOT**`, `**MAY**`, `**SHOULD**`

**Verification:**
- ✅ Semantic invariants: NO structural changes
- ✅ Reproducibility: `tools/no_diff/run` passed
- ✅ All gates: `tools/enforce_repo_law/run` passed
- ✅ Committed: `feat: apply InlineMarkup-K1 to specframe-k1 (readability + text.format attrs)`

**Rendered output:** `docs/_kernel/spec/spec/specframe-k1/v0.3.0/README.md`
- Professional, scannable formatting
- Consistent with GF0-K1 style
- Examples and code-like structures preserved

---

## Mechanics

### Workflow
1. **Backup**: Copied original frame to `/tmp/` before editing
2. **Edits**: Applied replacements using `replace_string_in_file` tool
   - Each clause/term updated individually for precision
   - Text format selection based on content patterns (lists, paragraphs, etc.)
   - Inline markup improvements (backticks, bold, etc.)
3. **Verification**: `./tools/semantic_invariants/run --before <old> --after <new>`
   - Confirmed only safe fields changed (text, summary, attrs added)
   - No changes to IDs, edges, kinds, statuses
4. **Regeneration**: `./tools/render_docs/run`
   - Converted frame → DocIR → Markdown/LaTeX
   - Deterministic output
5. **Reproducibility**: `./tools/no_diff/run`
   - Rendered docs twice, confirmed byte-for-byte identity
6. **Commit**: Staged frame + regenerated docs + copilot instructions

### Tool Integration
- **Copilot Instructions**: Automatically regenerated to reflect GF0-K1 and SpecFrame-K1 improvements
  - Updated excerpts from frame yards are now rendered with proper markup
  - Readable inline code and emphasis in doc comments

---

## Metrics

| Frame | Candidates | Clauses Updated | Md-inline | Md-block | Status |
|-------|-----------|-----------------|-----------|----------|--------|
| GF0-K1 | 62 | 20+ | 12 | 8+ | ✅ Complete |
| SpecFrame-K1 | 64 | 23 | 13 | 10 | ✅ Complete |
| **Total** | **126** | **43+** | **25+** | **18+** | **✅** |

---

## Next Priority Targets (Per Audit)

### Remaining High-Impact Kernel Specs (by candidate count)
1. **ValidatorGroup-K1** (101 candidates) — validator group schema
2. **RenderFrame-K1** (77 candidates) — render frame schema
3. **FrameMeta-K1** (75 candidates) — frame metadata schema
4. **DocLicense-K1** (66 candidates) — doc licensing schema
5. **SoftwareSpec-K1** (50 candidates) — software spec schema

### Repo Law Specs (selected)
- **RepoLaw K1** — governance repo law
- **InlineMarkup-K1** — this markup system (ironically!)

### Domain Specs
- Systemics specs (Sigma K1, etc.)
- Other domain-specific frames

---

## Key Lessons & Patterns

### Patterns for Text Format Selection
- **`md-block`**: Use when text contains:
  - Lists of items (even if formatted as wrapped lines)
  - Multiple paragraphs separated by blank lines
  - Field definitions with `: ` notation
- **`md-inline`**: Use when text is:
  - Single conceptual statement
  - No breaks or multiple paragraphs
  - Can still benefit from backticks and bold

### Inline Markup Conventions
1. **Field/attribute names** → backticks: `` `graph_id` ``, `` `version` ``, `` `kind` ``
2. **Type/class names** → backticks: `` `GraphFrameK0` ``, `` `NodeK0` ``
3. **String literals** → backticks: `` `'spec'` ``, `` `'contains'` ``
4. **Paths/identifiers** → backticks: `` `frames/repo/law/**` ``, `` `law://repo/**` ``
5. **Normative keywords** → bold: `**MUST**`, `**MUST NOT**`, `**MAY**`, `**SHOULD**`
6. **Emphasis** → italic: *optional*, *e.g.*

### Quality Assurance
- Semantic invariants checker catches accidental structural changes
- Reproducibility gate ensures determinism
- Commits include both frame edits and regenerated docs (atomic)
- No manual edits to generated docs needed

---

## Reproducibility & Determinism

All changes are **deterministic and reproducible**:
- ✅ Markup audit is deterministic (stable ordering, offline-only)
- ✅ Semantic invariants checker is deterministic (whitelist-based)
- ✅ Render pipeline is deterministic (no timestamps, stable anchors)
- ✅ `tools/no_diff/run` confirms byte-for-byte reproducibility
- ✅ All golden gates pass:
  - `tools/enforce_repo_law/run`
  - `tools/render_docs/run`
  - `tools/no_diff/run`

---

## Next Steps

### Immediate (this session)
- [ ] Apply markup to ValidatorGroup-K1 and RenderFrame-K1 if time permits
- [ ] Document progress in this file

### Short-term (next session)
- Apply markup to remaining kernel specs (FrameMeta-K1, DocLicense-K1, SoftwareSpec-K1)
- Apply markup to repo law specs (RepoLaw K1, InlineMarkup-K1 itself!)
- Begin domain spec batch (Systemics, etc.)

### Medium-term
- Monitor adoption across batch rollout
- Gather feedback on readability improvements
- Possibly formalize markup requirements in repo law update

---

## Commits This Session

1. `feat: apply InlineMarkup-K1 to gf0-k1 (readability + text.format attrs)`
2. `docs: apply InlineMarkup-K1 to specframe-k1 (readability + text.format attrs)`
3. `chore: regenerate copilot instructions`

All gates passing. Working tree clean.
