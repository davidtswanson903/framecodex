# ValidatorGroup K1 — Deterministic Doc-Group Validation
<a id="spec-kernel-validator-validatorgroup-k1-244af442"></a>

## Scope and Intent
<a id="section-1-scope-22c86ec9"></a>

**CanonicalEquivalence** _(normative)_


**DocGroup** _(normative)_


**GraphRecord** _(normative)_


**Location** _(normative)_


**ProfileDetection** _(normative)_


**ValidationStage** _(normative)_


**Violation** _(normative)_


**Intent** _(normative)_

`ValidatorGroup K1` exists to ensure that independent implementations validate the same
`DocGroup` and produce identical canonical results, enabling deterministic CI, refactors,
and generator pipelines.

**Non-goals** _(normative)_

This spec does not mandate any particular programming language, IO mechanism, file layout,
or CLI UX. It does not mandate performance characteristics beyond bounded recursion.

## Inputs and Canonicalization
<a id="section-2-inputs-ffc16fdb"></a>

**graph\_id uniqueness across DocGroup** _(normative)_

Within a `DocGroup`, `graph_id` values **SHOULD** be unique. If duplicates exist: - the validator **MUST** emit at least one violation per duplicated `graph_id`, and - the validator **MUST NOT** arbitrarily choose one duplicate as canonical. Deterministic behavior rule: graphs with duplicated `graph_id` **MUST** be validated for GF0 structural integrity, but **MUST** be excluded from higher-level profile validation and excluded from cross-graph linking, to avoid nondeterministic resolution.

**GraphRecord input model** _(normative)_

A validator consumes a `DocGroup` expressed as a list of `GraphRecord`s: - `graph`: a GF0 `GraphFrameK0` value - `source_id`: optional string (e.g., file path, URL, label) `source_id` **MUST NOT** affect the canonical validation result.

**Meta recursion** _(normative)_

Validation **MUST** recursively validate each `MetaGraph` using the same GF0 rules, subject to
a maximum `meta` depth (see `clause.determinism.limits`). `MetaGraph`s **MUST** be treated as
structurally independent; parent references, if any, are purely attribute/semantics level.

## Validation Stages
<a id="section-3-stages-0349f45b"></a>

**Stage definition** _(normative)_

Validation proceeds in the stage order specified by `property.stage_order`.
Each stage **MAY** add violations. A stage **MAY** be skipped for a graph if prerequisites fail.

**Stage: gf0\_struct** _(normative)_

`gf0_struct` performs structural validation of each graph (and recursively its `MetaGraph`s): - required top-level fields are present and correctly typed; - `graph_id` and `version` are non-empty strings; - `NodeK0` IDs are unique within the frame; - `EdgeK0` endpoints refer to existing `NodeK0` IDs in the same frame. Any failure in `gf0_struct` **MUST** emit an error severity violation for that graph.

**Stage: links** _(normative)_

`links` performs cross-graph checks using only graphs that passed `gf0_struct` and have unique `graph_id`: - For SpecFrames: every `spec_ref.target_graph_id` **MUST** exist as a `graph_id` in the DocGroup. - Additional link rules **MAY** be implemented, but **MUST** be deterministic and **MUST** have stable codes. Links stage **MUST NOT** attempt network fetch or external resolution unless the caller explicitly provides those graphs in the DocGroup.

**Stage: profile\_detect** _(normative)_

`profile_detect` deterministically identifies which higher-level validators apply to a graph. Detection **MUST** be based only on the graph's own content (not filename or environment). Minimum required detection rules: - `SpecFrameK1` applies if the graph contains exactly one node with `id==graph_id`, `kind=='spec'`, and `profile=='specframe-k1'`. - `RenderFrameK1` applies if the graph contains exactly one node with `id==graph_id`, `kind=='render_plan'`, and `profile=='renderframe-k1'`. If a graph matches multiple profile rules, the validator **MUST** emit an error and **MUST NOT** proceed to the conflicting profile validators.

**Stage: renderframe\_k1** _(normative)_

`renderframe_k1` validates graphs detected as RenderFrames by checking: - allowed node kinds and edge types for RenderFrameK1 - exactly one `render_plan` root node (where id equals graph*id and profile equals renderframe-k1) - `contains` edges forming an acyclic tree rooted at the render*plan node - rule edges and reference targets are well-typed (selects→selector, emits→emitter, etc.) RenderFrameK1's detailed rules are defined by `spec://_kernel/render/renderframe-k1`. This stage **MUST** implement them when that spec is available in the DocGroup.

**Stage: specframe\_k1** _(normative)_

`specframe_k1` validates graphs detected as `SpecFrame`s: - `NodeK0.kind` is within the allowed `SpecFrame` kinds set; - `EdgeK0.type` is within the allowed `SpecFrame` edge types set; - `'contains'` edges form an acyclic tree (or forest) rooted at the spec node; - required attributes per node kind are present. Missing required attributes **MUST** be treated as errors.

**Stage enum** _(normative)_

**Stage evaluation order** _(normative)_

## Determinism and Ordering
<a id="section-4-determinism-17f2e1bf"></a>

**Details ordering** _(normative)_

`Violation.details` **MUST** be an ordered list of `{key, value}` pairs and **MUST** be sorted by `key`
ascending lexicographic order, with stable tie-breaker by `value` ascending lexicographic order,
unless a specific code explicitly requires a different order.

**Safety limits** _(normative)_

Implementations **MUST** protect against unbounded recursion and pathological inputs by enforcing: - `max_meta_depth`: default 16 (caller may lower or raise; if exceeded, emit `GF0.E.META_DEPTH_EXCEEDED`) - `max_nodes_per_graph`: default 1,000,000 (if exceeded, emit `GF0.E.GRAPH_TOO_LARGE`) - `max_edges_per_graph`: default 2,000,000 (if exceeded, emit `GF0.E.GRAPH_TOO_LARGE`) Limits **MUST** be applied deterministically and reported via stable codes.

**Canonical sorting rules** _(normative)_

To ensure identical outputs across implementations: - Graph processing order **MUST** be ascending lexicographic order of `graph_id`. - Within a graph, node lookup order **MUST** be ascending lexicographic order of `node.id`. - Edge lookup order **MUST** be ascending lexicographic order of (`edge.type`, `edge.from`, `edge.to`, `edge.id`). All violation lists **MUST** be sorted by the canonical violation ordering (see `clause.determinism.violation_order`).

**Canonical violation ordering** _(normative)_

Violations **MUST** be sorted ascending by the tuple: `(severity_rank, code, stage, location.graph_id, meta_path_join, node_id, edge_key, details_join)`

where: - `severity_rank(error) = 0`, `severity_rank(warning) = 1` - `meta_path_join` is `meta_path` joined by ` > ` (empty string if none) - `node_id` and `edge_key` are empty string if absent - `details_join` is details joined as `k=v` pairs in order with `;` separators

**Details are ordered KV pairs** _(normative)_

## Validation Report Model
<a id="section-5-report-000de1c7"></a>

**Canonical JSON serialization** _(normative)_

Canonical equivalence is defined by canonical JSON serialization of the report: - UTF-8 encoding - Object keys are sorted lexicographically (byte order of UTF-8) - Arrays preserve their specified order - No insignificant whitespace is permitted - Newlines in strings **MUST** be `\n` (LF)

`message` fields, if present, **MUST** be excluded from canonical serialization.

**Fingerprint** _(informative)_

Implementations **MAY** provide a `fingerprint` value computed as SHA-256 over the canonical JSON bytes
as a convenience for fast equivalence checks.

**Location model** _(normative)_

A `Location` object **MUST** have: - `graph_id`: string - `meta_path`: ordered list of string `graph_id`s from outermost graph to the graph where the violation occurred

It **MAY** have: - `node_id`: string - `edge_key`: string (canonical edge key in the form `type|from|to|id`, with empty `id` allowed)

**ValidationReportK1 model** _(normative)_

The validator produces a `ValidationReportK1` object with fields: - `version`: fixed string `validatorgroup-k1@0.1.0` - `ok`: boolean - `violations`: ordered list of Violation objects

`ok` **MUST** be true iff `violations` contains no entries with `severity == error`.

**Violation model** _(normative)_

A `Violation` object **MUST** have: - `severity`: `error` or `warning` - `code`: stable string code (see `section.6`) - `stage`: one of `property.stage_enum.stage_values` - `location`: Location object - `details`: ordered list of `{key, value}` pairs (not a map)

A `Violation` **MAY** have: - `message`: non-canonical human-readable string (**MUST** be ignored for canonical equivalence)

**Location fields** _(normative)_

**Required report fields** _(normative)_

**Severity enum** _(normative)_

**Required violation fields** _(normative)_

## Required Violation Codes
<a id="section-6-codes-001612f1"></a>

**GF0.E.BAD\_EDGE\_ENDPOINT** _(normative)_

Emitted when an edge endpoint references a missing node.
`details` **MUST** include: `edge_key`, `missing_endpoint` (either `from` or `to`), `missing_node_id`.

**GF0.E.DUP\_NODE\_ID** _(normative)_

Emitted when two or more nodes share the same `id` within one frame.
`details` **MUST** include: `node_id`.

**GF0.E.EMPTY\_GRAPH\_ID\_OR\_VERSION** _(normative)_

Emitted when `graph_id` or `version` is empty string.
`details` **MUST** include: `which` (either `graph_id` or `version`).

**GF0.E.MISSING\_FIELD** _(normative)_

Emitted when any required GF0 top-level field is missing in canonical form.
`details` **MUST** include: `field_name`.

**LINK.E.MISSING\_TARGET\_GRAPH** _(normative)_

Emitted when a `spec_ref.target_graph_id` does not exist in the DocGroup.
`details` **MUST** include: `node_id`, `target_graph_id`.

**LINK.W.UNREACHABLE\_NORMATIVE** _(normative)_

Emitted (as warning by default) when a normative node is unreachable from the SpecFrame root via `contains`.
`details` **MUST** include: `node_id`.

**Stable codes** _(normative)_

Codes **MUST** be stable across versions of implementations that claim conformance to this spec.
Codes **MUST NOT** include implementation-specific details (paths, line numbers, stack traces).

**SPEC.E.BAD\_EDGE\_TYPE** _(normative)_

Emitted when a SpecFrame contains an edge with `type` not in the SpecFrame allowed set.
`details` **MUST** include: `edge_key`, `edge_type`.

**SPEC.E.BAD\_NODE\_KIND** _(normative)_

Emitted when a SpecFrame contains a node with `kind` not in the SpecFrame allowed set.
`details` **MUST** include: `node_id`, `node_kind`.

**SPEC.E.CONTAINS\_CYCLE\_OR\_MULTIPARENT** _(normative)_

Emitted when `contains` edges are cyclic or a node has multiple `contains` parents.
`details` **MUST** include: `node_id`.
`details` **MAY** include: `parent_ids` (ordered list of parents), `cycle_hint` (string).

**SPEC.E.MISSING\_REQUIRED\_ATTR** _(normative)_

Emitted when a required attribute per SpecFrame node `kind` is missing.
`details` **MUST** include: `node_id`, `node_kind`, `attr_name`.

**Required violation codes** _(normative)_

## Examples
<a id="section-7-examples-ad6c9349"></a>

## Integration Notes
<a id="section-8-integration-7e6315ee"></a>

## References
<a id="refs-e812cd2d"></a>

- GraphFrame K0 schema (spec://\_kernel/gf/gf0-k1)
- RenderFrame K1 schema (spec://\_kernel/render/renderframe-k1)
- SpecFrame K1 schema (spec://\_kernel/spec/specframe-k1)
