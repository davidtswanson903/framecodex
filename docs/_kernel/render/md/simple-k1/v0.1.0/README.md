# render://_kernel/md/simple-k1
- version: 0.1.0
- nodes: 29
- edges: 28
- meta: 0
## Nodes
- **clause.contains_tree** (kind: clause)
  - label: Contains tree rendering
  - Extra fields:
    ```yml
    label: Contains tree rendering
    status: normative
    text: 'If any edges exist with type == property.contains_edge_type, the renderer MUST attempt
      to render a tree rooted at node id == graph_id (if such a node exists), otherwise a forest.
      If cycles or multiple parents are detected, the renderer MUST still output a best-effort
      forest and MUST emit a warning (see Errors and Warnings).

      '
    ```
- **clause.determinism.newlines** (kind: clause)
  - label: Newlines and whitespace
  - Extra fields:
    ```yml
    label: Newlines and whitespace
    status: normative
    text: 'Output MUST use LF newlines. Trailing whitespace MUST be stripped from all lines. The
      document MUST end with exactly one LF.

      '
    ```
- **clause.determinism.sorting** (kind: clause)
  - label: Deterministic ordering
  - Extra fields:
    ```yml
    label: Deterministic ordering
    status: normative
    text: 'Node, edge, and meta ordering MUST follow property.ordering. Implementations in different
      languages MUST produce byte-identical Markdown for the same input frame.

      '
    ```
- **clause.edges.rendering** (kind: clause)
  - label: Edge rendering
  - Extra fields:
    ```yml
    label: Edge rendering
    status: normative
    text: "Edges MUST be rendered as a Markdown table in deterministic order with columns:\n \
      \ [from, to, type, id(optional), attrs(optional), metrics(optional)].\nIf attrs/metrics\
      \ exist, they MUST be rendered as compact JSON within the table cell.\n"
    ```
- **clause.errors.warn_codes** (kind: clause)
  - label: Warnings
  - Extra fields:
    ```yml
    label: Warnings
    status: normative
    text: "The renderer SHOULD emit warnings (non-fatal) for:\n  - unknown/extra top-level keys\
      \ on nodes/edges (still rendered under Extra fields)\n  - contains cycles or multiple parents\n\
      \  - missing root node id == graph_id (contains tree becomes a forest)\n"
    ```
- **clause.input.gf0_required** (kind: clause)
  - label: Input must be valid GF0
  - Extra fields:
    ```yml
    label: Input must be valid GF0
    status: normative
    text: 'Inputs MUST be structurally valid GF0: graph_id and version non-empty, attrs/nodes/edges/meta
      lists present, node IDs unique, and edges must reference existing node IDs.

      '
    ```
- **clause.meta.rendering** (kind: clause)
  - label: Meta graph rendering
  - Extra fields:
    ```yml
    label: Meta graph rendering
    status: normative
    text: 'Each meta subgraph MUST be rendered after the primary frame, separated by a horizontal
      rule, using the same algorithm recursively. Meta graphs MUST be ordered deterministically.

      '
    ```
- **clause.nodes.rendering** (kind: clause)
  - label: Node rendering
  - Extra fields:
    ```yml
    label: Node rendering
    status: normative
    text: "Nodes MUST be rendered as a Markdown list in deterministic order. For each node:\n\
      \  - heading line: **<id>**  (kind: <kind>)\n  - if label exists: include \"label: <label>\"\
      \n  - attrs table if attrs present: columns [key, value, vtype, desc]\n  - metrics table\
      \ if metrics present: columns [name, value, unit, desc]\n  - extra fields: any additional\
      \ node keys (e.g. title/status/text/summary/profile/order)\n    MUST be rendered under an\
      \ \"Extra fields\" sub-bullet as a YAML code block.\n"
    ```
- **clause.output.header** (kind: clause)
  - label: Header section
  - Extra fields:
    ```yml
    label: Header section
    status: normative
    text: "The output MUST begin with:\n  - H1: graph_id\n  - A short metadata block containing\
      \ version, node_count, edge_count, meta_count.\n"
    ```
- **clause.output.sections** (kind: clause)
  - label: Required sections
  - Extra fields:
    ```yml
    label: Required sections
    status: normative
    text: "The output MUST include these sections in this order:\n  1) Header (H1 + metadata)\n\
      \  2) Nodes (index)\n  3) Edges (index)\n  4) Contains Tree (if any edges of type 'contains'\
      \ exist)\n  5) Meta Graphs (if meta_count > 0)\n"
    ```
- **clause.scope** (kind: clause)
  - label: Scope
  - Extra fields:
    ```yml
    label: Scope
    status: normative
    text: 'This renderer MUST accept any valid GraphFrame K0 (GF0) and MUST emit a single Markdown
      document representing the frame. It MUST NOT rely on higher-level frame semantics (SpecFrame,
      LawFrame, etc.) beyond what is present in the GF0 structure.

      '
    ```
- **example.output_shape** (kind: example)
  - label: Markdown skeleton
  - Extra fields:
    ```yml
    label: Markdown skeleton
    status: informative
    text: "# <graph_id>\n- version: <version>\n- nodes: <n>\n- edges: <m>\n- meta: <k>\n\n## Nodes\n\
      - **node.a** (kind: section)\n  - attrs:\n    | key | value | vtype | desc |\n    | ---\
      \ | --- | --- | --- |\n    | ... | ... | ... | ... |\n  - Extra fields:\n    ```yml\n  \
      \  title: Example\n    order: 1\n    ```\n\n## Edges\n| from | to | type | id | attrs |\
      \ metrics |\n| --- | --- | --- | --- | --- | --- |\n| ... | ... | ... | ... | ... | ...\
      \ |\n\n## Contains Tree\n- <root>\n  - <child>\n\n## Meta Graphs\n---\n"
    ```
- **property.contains_edge_type** (kind: property)
  - label: Contains edge type
  - Extra fields:
    ```yml
    label: Contains edge type
    status: normative
    value: contains
    ```
- **property.field_exclusions** (kind: property)
  - label: Field exclusion list
  - Extra fields:
    ```yml
    excluded_edge_fields:
    - from
    - to
    - type
    - attrs
    - metrics
    excluded_node_fields:
    - id
    - kind
    - attrs
    - metrics
    label: Field exclusion list
    status: normative
    ```
- **property.ordering** (kind: property)
  - label: Ordering keys
  - Extra fields:
    ```yml
    edge_order: by (from,to,type,id) ascending (bytewise; missing id treated as empty)
    label: Ordering keys
    meta_order: by (graph_id,version) ascending (bytewise)
    node_order: by node.id ascending (bytewise)
    status: normative
    ```
- **property.output_extension** (kind: property)
  - label: Output extension
  - Extra fields:
    ```yml
    label: Output extension
    status: normative
    value: .md
    ```
- **property.output_path_rule** (kind: property)
  - label: Output path rule
  - Extra fields:
    ```yml
    label: Output path rule
    status: normative
    value: docs/{frameurl_path}/v{version}/README.md
    ```
- **property.renderer_id** (kind: property)
  - label: Renderer ID
  - Extra fields:
    ```yml
    label: Renderer ID
    status: normative
    value: simple-md-k1
    ```
- **ref.spec.gf0-k1** (kind: spec_ref)
  - label: GF0 schema
  - Extra fields:
    ```yml
    label: GF0 schema
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    ```
- **ref.spec.specframe-k1** (kind: spec_ref)
  - label: SpecFrame K1 schema
  - Extra fields:
    ```yml
    label: SpecFrame K1 schema
    status: informative
    target_graph_id: spec://_kernel/spec/specframe-k1
    ```
- **render://_kernel/md/simple-k1** (kind: spec)
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'Deterministic, profile-agnostic Markdown rendering for any GF0 frame. Produces a
      uniform human-readable view (header, node index, edge index, optional contains tree, and
      meta graphs).

      '
    title: Simple Markdown Renderer K1
    ```
- **section.1.scope** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Scope
    ```
- **section.2.inputs** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Inputs
    ```
- **section.3.outputs** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Outputs
    ```
- **section.4.algorithm** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: Render Algorithm
    ```
- **section.5.determinism** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: Determinism Rules
    ```
- **section.6.meta** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: normative
    title: Meta Graph Rendering
    ```
- **section.7.errors** (kind: section)
  - Extra fields:
    ```yml
    order: 7
    status: normative
    title: Errors and Warnings
    ```
- **section.8.examples** (kind: section)
  - Extra fields:
    ```yml
    order: 8
    status: informative
    title: Example Output Shape
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| render://_kernel/md/simple-k1 | property.contains_edge_type | contains |  |  |  |
| render://_kernel/md/simple-k1 | property.field_exclusions | contains |  |  |  |
| render://_kernel/md/simple-k1 | property.ordering | contains |  |  |  |
| render://_kernel/md/simple-k1 | property.output_extension | contains |  |  |  |
| render://_kernel/md/simple-k1 | property.output_path_rule | contains |  |  |  |
| render://_kernel/md/simple-k1 | property.renderer_id | contains |  |  |  |
| render://_kernel/md/simple-k1 | ref.spec.gf0-k1 | contains |  |  |  |
| render://_kernel/md/simple-k1 | ref.spec.specframe-k1 | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.1.scope | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.2.inputs | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.3.outputs | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.4.algorithm | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.5.determinism | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.6.meta | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.7.errors | contains |  |  |  |
| render://_kernel/md/simple-k1 | section.8.examples | contains |  |  |  |
| section.1.scope | clause.scope | contains |  |  |  |
| section.2.inputs | clause.input.gf0_required | contains |  |  |  |
| section.3.outputs | clause.output.header | contains |  |  |  |
| section.3.outputs | clause.output.sections | contains |  |  |  |
| section.4.algorithm | clause.contains_tree | contains |  |  |  |
| section.4.algorithm | clause.edges.rendering | contains |  |  |  |
| section.4.algorithm | clause.nodes.rendering | contains |  |  |  |
| section.5.determinism | clause.determinism.newlines | contains |  |  |  |
| section.5.determinism | clause.determinism.sorting | contains |  |  |  |
| section.6.meta | clause.meta.rendering | contains |  |  |  |
| section.7.errors | clause.errors.warn_codes | contains |  |  |  |
| section.8.examples | example.output_shape | contains |  |  |  |

## Contains Tree
- render://_kernel/md/simple-k1
  - property.contains_edge_type
  - property.field_exclusions
  - property.ordering
  - property.output_extension
  - property.output_path_rule
  - property.renderer_id
  - ref.spec.gf0-k1
  - ref.spec.specframe-k1
  - section.1.scope
    - clause.scope
  - section.2.inputs
    - clause.input.gf0_required
  - section.3.outputs
    - clause.output.header
    - clause.output.sections
  - section.4.algorithm
    - clause.contains_tree
    - clause.edges.rendering
    - clause.nodes.rendering
  - section.5.determinism
    - clause.determinism.newlines
    - clause.determinism.sorting
  - section.6.meta
    - clause.meta.rendering
  - section.7.errors
    - clause.errors.warn_codes
  - section.8.examples
    - example.output_shape
