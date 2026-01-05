# PLAN.md Implementation Summary

## Completed: Phase 1–3 of Systemic InlineMarkup-K1 Adoption

### What Was Done

#### 1. **Inventory Tool** (`tools/markup_audit/run.py`)
- Scans all frames and detects freeform text fields candidates for markup.
- Detects patterns: code backticks, file paths, emphasis, references, lists, multiline.
- Recommends `md-inline`, `md-block`, or `plain` based on patterns.

**Results:**
- **929 candidates** found across the repo
- **19 `md-inline`** (short inline markup)
- **337 `md-block`** (multiline, multiple paragraphs)
- **573 `plain`** (no obvious markup patterns)

**Output:**
- `out/markup_audit/report.json` — structured report
- `out/markup_audit/candidates.csv` — human-readable CSV for review

#### 2. **Semantic Invariants Checker** (`tools/semantic_invariants/run.py`)
- Verifies that frame edits change **only safe fields** (text, summary, title).
- Forbids changes to: graph_id, version, node IDs, kinds, statuses, edges, machine-consumed fields.
- Clear whitelist of safe vs. protected fields.

**Usage:**
```bash
./tools/semantic_invariants/run --before <old.yml> --after <new.yml> [--verbose]
```

#### 3. **Style Guide** (`MARKUP_STYLE_GUIDE.md`)
- Documents consistent conventions for markup application:
  - When to use `md-inline` vs. `md-block`
  - How to format identifiers, paths, code, emphasis, links
  - What fields are safe vs. forbidden to change
  - Workflow: audit → edit → verify → regenerate → check → commit

#### 4. **Demo Markup Pass on FrameURL-K1**
- Applied safe, high-value markup to `frames/_kernel/law/id/frameurl-k1/v0.1.0/frame.yml`:
  - Added `text.format: md-inline` to 5 definition/rule nodes
  - Wrapped technical identifiers in backticks: `` `graph_id` ``, `` `GF0.version` ``, `` `<scheme>` ``
  - Enhanced emphasis: `**MUST**` instead of plain `MUST`
  - Improved readability without changing semantics

**Verification:**
- ✅ Semantic invariants preserved (no structural changes)
- ✅ `tools/render_docs/run` regenerated markdown
- ✅ `tools/no_diff/run` confirmed reproducibility
- ✅ `tools/enforce_repo_law/run` passed

**Rendered output:**
- Before: Plain prose with implicit emphasis
- After: Code formatting, clear emphasis, readable backticks
- See: `docs/_kernel/law/id/frameurl-k1/v0.1.0/README.md`

---

## Key Tools Integrated

### `tools/markup_audit/run`
```bash
./tools/markup_audit/run
# Outputs:
#   out/markup_audit/report.json
#   out/markup_audit/candidates.csv
```

### `tools/semantic_invariants/run`
```bash
./tools/semantic_invariants/run --before old.yml --after new.yml --verbose
# Exit 0 if safe, 1 if violations
```

### Updated `tools/gen_copilot_instructions/run.py`
Now includes excerpts from new audit/invariants tool headers.

---

## Workflow Demonstrated

### Single Commit Workflow:
1. **Audit**: `./tools/markup_audit/run` → review `out/markup_audit/candidates.csv`
2. **Edit**: Apply markup to one frame (e.g., FrameURL-K1)
3. **Verify**: `./tools/semantic_invariants/run --before ... --after ...`
4. **Regen**: `./tools/render_docs/run`
5. **Gate**: `./tools/no_diff/run` + `./tools/enforce_repo_law/run`
6. **Commit**: Stage frame + regenerated docs

Example commits from this session:
- `feat: add markup_audit and semantic_invariants tools + demo markup edits on frameurl-k1`
- `docs: apply InlineMarkup-K1 to frameurl-k1 definitions and rules (readability only)`

---

## Next Steps (Recommended)

### Layer 1: Kernel specs (high leverage, small surface area)
- GF0-K1 (62 candidates)
- SpecFrame-K1 (64 candidates)
- Other `_kernel/**` specs

### Layer 2: Repo laws
- RepoLaw K1
- InlineMarkup-K1
- Other repo/**/* frames

### Layer 3: Domain specs
- Systemics specs (Sigma K1, Sigma Composition K1)
- Other domain frames

### Continuous Improvement
- As adoption grows, formalize markup requirements in a repo law or policy update.
- Possibly retire legacy "ASCII pseudo-formatting" patterns (plain CAPS for emphasis, etc.).

---

## Determinism & Gates

All three components are **deterministic**:
- `markup_audit`: stable ordering, offline-only, no timestamps
- `semantic_invariants`: clear whitelist, deterministic diff
- Existing `render_docs`, `no_diff`, `enforce_repo_law`: unchanged

All changes flow through **golden gates**:
1. `tools/enforce_repo_law/run` (policy validation)
2. `tools/render_docs/run` (deterministic regeneration)
3. `tools/no_diff/run` (reproducibility check)

---

## Summary

**Inventory + Safety Machinery:** ✅ Complete
- Found 929 candidates for markup
- Built semantic invariants checker to prevent accidental structural changes
- Demonstrated safe mechanical rewrite on high-impact frame

**Readability Improvements:** ✅ Visible
- FrameURL-K1 now has inline code backticks, bold emphasis
- Markdown rendering is cleaner and more scannable
- Regenerated docs reflect improvements

**Reproducibility:** ✅ Maintained
- All gates pass
- `no_diff` confirms determinism across regenerations
- Commits include both frame edits and regenerated docs

---

## Usage for Next Batch

To apply markup to a new frame (e.g., GF0-K1):

1. **Identify candidates:**
   ```bash
   grep "^frames/_kernel/spec/gf/gf0-k1" out/markup_audit/candidates.csv
   ```

2. **Apply markup** (see MARKUP_STYLE_GUIDE.md for conventions)

3. **Verify invariants:**
   ```bash
   cp frames/_kernel/spec/gf/gf0-k1/v0.3.0/frame.yml /tmp/gf0-before.yml
   # ... edit frame ...
   ./tools/semantic_invariants/run --before /tmp/gf0-before.yml --after frames/_kernel/spec/gf/gf0-k1/v0.3.0/frame.yml
   ```

4. **Regenerate & verify:**
   ```bash
   ./tools/render_docs/run
   ./tools/no_diff/run
   ./tools/enforce_repo_law/run
   ```

5. **Commit:**
   ```bash
   git add frames/_kernel/spec/gf/gf0-k1/v0.3.0/frame.yml docs/_kernel/spec/gf/gf0-k1/v0.3.0/README.md
   git commit -m "docs: apply InlineMarkup-K1 to gf0-k1 (readability only)"
   ```
