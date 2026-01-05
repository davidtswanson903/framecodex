# Simple Markdown Renderer K1
<a id="render-kernel-md-simple-k1-6f548e7f"></a>

## Scope
<a id="section-1-scope-22c86ec9"></a>

**Scope** _(normative)_

This renderer **MUST** accept any valid `GraphFrame K0` (GF0) and **MUST** emit a single Markdown document representing the frame. It **MUST NOT** rely on higher-level frame semantics (SpecFrame, LawFrame, etc.) beyond what is present in the GF0 structure.

## Inputs
<a id="section-2-inputs-ffc16fdb"></a>

**Input must be valid GF0** _(normative)_

Inputs **MUST** be structurally valid GF0: `graph_id` and `version` non-empty, `attrs`/`nodes`/`edges`/`meta` lists present, node IDs unique, and edges must reference existing node IDs.

## Outputs
<a id="section-3-outputs-a2d6ae57"></a>

**Header section** _(normative)_

The output **MUST** begin with: - H1: `graph_id` - A short metadata block containing `version`, `node_count`, `edge_count`, `meta_count`.

**Required sections** _(normative)_

The output **MUST** include these sections in this order: 1) Header (H1 + metadata) 2) Nodes (index) 3) Edges (index) 4) Contains Tree (if any edges of type `contains` exist) 5) Meta Graphs (if `meta_count > 0`)

## Render Algorithm
<a id="section-4-algorithm-a93179e8"></a>

**Contains tree rendering** _(normative)_

If any edges exist with `type == property.contains_edge_type`, the renderer **MUST** attempt to render a tree rooted at node `id == graph_id` (if such a node exists), otherwise a forest. If cycles or multiple parents are detected, the renderer **MUST** still output a best-effort forest and **MUST** emit a warning (see Errors and Warnings).

**Edge rendering** _(normative)_

Edges **MUST** be rendered as a Markdown table in deterministic order with columns: `[from, to, type, id(optional), attrs(optional), metrics(optional)]`. If `attrs`/`metrics` exist, they **MUST** be rendered as compact JSON within the table cell.

**Node rendering** _(normative)_

Nodes **MUST** be rendered as a Markdown list in deterministic order. For each node: - heading line: `**<id>**  (kind: <kind>)` - if `label` exists: include `"label: <label>"` - `attrs` table if `attrs` present: columns `[key, value, vtype, desc]` - `metrics` table if `metrics` present: columns `[name, value, unit, desc]` - extra fields: any additional node keys (e.g. `title`/`status`/`text`/`summary`/`profile`/`order`) **MUST** be rendered under an "Extra fields" sub-bullet as a YAML code block.

## Determinism Rules
<a id="section-5-determinism-75229002"></a>

**Newlines and whitespace** _(normative)_

Output **MUST** use LF newlines. Trailing whitespace **MUST** be stripped from all lines. The document **MUST** end with exactly one LF.

**Deterministic ordering** _(normative)_

Node, edge, and meta ordering **MUST** follow `property.ordering`. Implementations in different languages **MUST** produce byte-identical Markdown for the same input frame.

## Meta Graph Rendering
<a id="section-6-meta-6ff97a68"></a>

**Meta graph rendering** _(normative)_

Each meta subgraph **MUST** be rendered after the primary frame, separated by a horizontal rule, using the same algorithm recursively. Meta graphs **MUST** be ordered deterministically.

## Errors and Warnings
<a id="section-7-errors-194a7125"></a>

**Warnings** _(normative)_

The renderer **SHOULD** emit warnings (non-fatal) for: - unknown/extra top-level keys on nodes/edges (still rendered under Extra fields) - `contains` cycles or multiple parents - missing root node `id == graph_id` (contains tree becomes a forest)

## Example Output Shape
<a id="section-8-examples-3bd695e4"></a>

**Contains edge type** _(normative)_

**Field exclusion list** _(normative)_

**Ordering keys** _(normative)_

**Output extension** _(normative)_

**Output path rule** _(normative)_

**Renderer ID** _(normative)_

## References
<a id="refs-e812cd2d"></a>

- GF0 schema ()
- SpecFrame K1 schema ()
