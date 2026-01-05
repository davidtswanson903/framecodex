# InlineMarkup-K1 Rollout Status

**Status Date**: 2026-01-04  
**Commit Count**: 15+ (since session start)

## ✅ COMPLETED FRAMES

### GF0-K1 (spec://_kernel/gf/gf0-k1 v0.3.0)
- **Status**: ✅ Complete
- **Clauses Marked**: 20+
- **Sections**: Overview, GraphFrame Structure, NodeK0, EdgeK0, Fractal Meta Graphs, Invariants, Extension
- **Format**: `md-inline` and `md-block` as appropriate
- **Markup Applied**: Backticks for identifiers, bold for MUST/MAY/SHOULD, structure preserved
- **Commits**: 
  - `feat: apply InlineMarkup-K1 to GF0-K1 spec frame`
  - `chore: regenerate gf0-k1 README with markup`

### SpecFrame-K1 (spec://_kernel/spec/specframe-k1 v0.3.0)
- **Status**: ✅ Complete
- **Clauses Marked**: 23
- **Sections**: Scope and Intent, Node Kinds, Edge Types, Attributes, Validation Invariants, Integration
- **Format**: `md-inline` for simple definitions, `md-block` for lists and structured content
- **Markup Applied**: Field names in backticks, MUST/MAY/SHOULD bolded, clear list formatting
- **Commits**:
  - `feat: apply InlineMarkup-K1 to SpecFrame-K1 spec`
  - `chore: regenerate specframe-k1 README with markup`

### ValidatorGroup-K1 (spec://_kernel/validator/validatorgroup-k1 v0.1.0)
- **Status**: ✅ Complete
- **Clauses Marked**: 35+
- **Sections**: 
  - Scope (2 clauses) + terms (9 definitions)
  - Inputs (3 clauses)
  - Stages (8 clauses)
  - Determinism (5 clauses)
  - Report (6 clauses)
  - Codes (12 code-definition clauses + requirement clause)
- **Format**: `md-inline` for simple text, `md-block` for lists and structured requirements
- **Markup Applied**: 
  - Backticked field names (`graph_id`, `version`, `render_plan`, etc.)
  - Bold for normative keywords (MUST, MUST NOT, MAY, SHOULD)
  - List formatting with proper indentation
  - Code identifiers properly backticked
- **Commits**:
  - `fix: renderframe and links clauses - correct inline markup backticks`
  - `feat: complete InlineMarkup-K1 for validatorgroup-k1 frame`
  - `chore: regenerate validatorgroup-k1 README with complete markup` (2 commits)

### RenderFrame-K1 (spec://_kernel/render/renderframe-k1 v0.1.0)
- **Status**: ✅ Complete
- **Clauses Marked**: 18 (all remaining clauses completed)
- **Sections**: Overview, Model, Node Kinds, Edge Types, Attributes, Validation, Integration, Examples
- **Format**: `md-inline` for simple constraints, `md-block` for attribute lists and structural rules
- **Markup Applied**:
  - Backticked field names (`render_plan`, `render_product`, `selector`, `emitter`, `template`, `transform`)
  - Bold for MUST/MAY/SHOULD/MUST NOT keywords
  - Backticked values and enum literals (`renderframe-k1`, `first_match`, `merge`, etc.)
  - Proper formatting of node kind/edge type lists
- **Commits**:
  - `Apply InlineMarkup-K1 markup to RenderFrame-K1...` (combined commit)

### DocProfiles-K1 (spec://_kernel/docs/docprofiles-k1 v0.1.0)
- **Status**: ✅ Complete
- **Terms Marked**: 8 (doc_profile, ProfileRule, ProfileId, plus 5 specific profiles)
- **Clauses Marked**: 6 (intent, profile-location, profile-semantics, frame-metadata, lint-baseline, render-baseline)
- **Format**: `md-inline` for all terms and simple clauses, `md-block` for list-based rules
- **Markup Applied**:
  - Profile identifiers backticked (`doc_profile`, `software_spec-k1`, `hardware_spec-k1`, etc.)
  - Normative keywords bolded
  - Arrow notation for determinism (`→` for input-output)
  - Proper list formatting for render products
- **Commits**:
  - `Apply InlineMarkup-K1 markup to RenderFrame-K1, DocProfiles-K1, and Software-Spec-K1...`

### Software-Spec-K1 (spec://_kernel/template/software-spec-k1 v0.1.0)
- **Status**: ✅ Complete
- **Terms Marked**: 3 (Module, Kernel, Interface)
- **Clauses Marked**: 11 (all template clauses updated)
- **Format**: `md-inline` for simple definitions and TODOs, `md-block` for structured sections
- **Markup Applied**:
  - Property references backticked (`property.api_surface`)
  - Framework/module terminology consistent with naming
  - TODOs preserved as instructional scaffolding
- **Commits**:
  - `Apply InlineMarkup-K1 markup to RenderFrame-K1, DocProfiles-K1, and Software-Spec-K1...`

## 🔍 VERIFICATION STATUS

**All completed frames pass:**
- ✅ `tools/validate_inline_markup/run.py` — No violations
- ✅ `tools/enforce_repo_law/run` — All gates passing
- ✅ `tools/render_docs/run` — Deterministic doc regeneration
- ✅ `tools/no_diff/run` — Byte-for-byte reproducibility confirmed

## 📋 CANDIDATES FOR NEXT ROLLOUT

### High Priority (Kernel Specs)

1. **FrameURL-K1** (`law://_kernel/id/frameurl-k1 v0.1.0`) — **NEXT TARGET**
   - Type: Law/Identity specification
   - Candidates: ~50+ nodes with markup opportunities
   - Focus: Definitions (6), Rules (15+), Examples (2)
   - Patterns: URLs, filesystem paths, grammar patterns
   - Recommendation: `md-inline` for most, `md-block` for grammar/examples
   - Status: Ready to apply

2. **LawFrame-K1** (`law://_kernel/law/lawframe-k1 v0.1.0`)
   - Type: Law/Metaspec
   - Candidates: ~35+ nodes
   - Focus: Law node kinds, attributes, profiles
   - Recommendation: `md-inline` for definitions, `md-block` for clauses

3. **DocLicense-K1** (`law://_kernel/law/ip/doclicense-k1 v0.1.0`)
   - Type: Law/IP
   - Candidates: ~25+ nodes
   - Focus: License terms, permissions, constraints

### Medium Priority (Supplementary)

4. **FrameMeta-K1** (`law://_kernel/law/meta/frame-meta-k1 v0.1.0`)
   - Type: Law/Metadata
   - Candidates: ~20+ nodes
   
5. **Simple Markdown Renderer K1** (`render://md/simple-k1 v0.1.0`)
   - Type: Render spec
   - Candidates: ~15+ nodes

### Domain-Specific Specs (Lower Priority)

- **Systemics Specs** (sigma-k1, sigma-composition-k1, systemics-core-k1, k0-k1)
  - Type: Spec/Domain
  - Candidates: Variable per spec

## 🎯 NEXT STEPS

1. Apply markup to **FrameURL-K1** (high-value, many opportunities)
   - All 6 definitions
   - All 15+ rules 
   - Both examples
   - Properties and codes

2. Continue with **LawFrame-K1** and **DocLicense-K1** to complete law/IP specs

3. Run comprehensive validation:
   - `tools/validate_inline_markup/run.py`
   - `tools/semantic_invariants/run.py` (before/after spot checks)
   - `tools/enforce_repo_law/run` (full gate)
   - `tools/render_docs/run` (docs regeneration)
   - `tools/no_diff/run` (determinism check)

4. Batch remaining frames systematically

5. Final git log and verification
  - Type: Domain specs
  - Total candidates: ~100+

- **RepoLaw-K1** (`law://repo/governance/repo-law-k1 v0.1.0`)
  - Type: Repository governance law
  - Candidates: ~40+ nodes

- **InlineMarkup-K1** (`law://_kernel/law/text/inline-markup-k1 v0.1.0`)
  - Type: Meta (this spec itself!)
  - Candidates: ~20+ nodes

## 🔍 VERIFICATION GATES

All changes verified with:
- ✅ `tools/validate_inline_markup/run.py` — InlineMarkup-K1 validation
- ✅ `tools/semantic_invariants/run.py` — Structural invariants (only safe field changes)
- ✅ `tools/render_docs/run` — Deterministic doc regeneration
- ✅ `tools/no_diff/run` — Reproducibility check (byte-for-byte identical)
- ✅ `tools/enforce_repo_law/run` — Repository law enforcement

## 📊 METRICS

### By Recommendation Type
- `plain`: 573 nodes (no markup needed)
- `md-inline`: 24 nodes (single-paragraph inline markup)
- `md-block`: 332 nodes (multi-paragraph or list-based markup)
- **Total candidates**: 929 nodes across all frames

### Completed Markup Coverage
- **Frames completed**: 3 (GF0-K1, SpecFrame-K1, ValidatorGroup-K1)
- **Total clauses/terms marked**: 78+
- **Remaining high-priority frames**: 4-5

## 🎯 NEXT STEPS

### Immediate (Next Session)
1. Apply markup to **FrameURL-K1** (law spec, ~50 candidates)
2. Apply markup to **RenderFrame-K1** (spec, ~40 candidates)
3. Verify all changes with gates, commit atomically

### Short Term
4. Complete **LawFrame-K1** and **DocProfiles-K1**
5. Secondary specs: **DocLicense-K1**, **FrameMeta-K1**, **SoftwareSpec-K1**

### Medium Term
6. Domain-specific specs (Systemics family)
7. Repository laws (RepoLaw-K1)
8. Self-referential specs (InlineMarkup-K1 itself)

## 📝 NOTES

- **Backtick Nesting**: Avoid backticks within code identifiers; use plain prose or restructure sentences
- **Normative Keywords**: Always bold MUST, MUST NOT, MAY, SHOULD, SHOULD NOT
- **Field Names**: Use backticks consistently for field names and identifiers
- **Lists**: Use `md-block` for any multi-line list or structured requirement
- **Determinism**: All changes maintain reproducibility; no timestamps or random ordering
- **Semantic Safety**: Only "safe" text fields are modified; structure (IDs, edges, kinds) preserved

## ✨ QUALITY ASSURANCE

All committed changes:
- Pass inline markup validation (no HTML, balanced delimiters)
- Preserve semantic invariants (no structural changes)
- Generate deterministic, byte-for-byte identical output
- Comply with repository laws
- Are committed atomically with clear messages
- Include regenerated docs in follow-up commits
