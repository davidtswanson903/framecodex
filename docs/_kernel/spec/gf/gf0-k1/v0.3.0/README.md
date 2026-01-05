# spec://_kernel/gf/gf0-k1
- version: 0.3.0
- nodes: 35
- edges: 37
- meta: 1
## Nodes
- **clause.attr_metric.slice_not_map** (kind: clause)
  - label: Slices, Not Maps
  - Extra fields:
    ```yml
    label: Slices, Not Maps
    status: normative
    text: 'AttrK0 and MetricK0 collections MUST be represented as ordered slices, not maps. This
      ensures deterministic ordering and stable serialization across implementations.

      '
    ```
- **clause.attrk0.structure** (kind: clause)
  - label: AttrK0 Structure
  - Extra fields:
    ```yml
    label: AttrK0 Structure
    status: normative
    text: "AttrK0 MUST at least contain:\n  - key: non-empty string;\n  - value: string (UTF-8).\n\
      It MAY contain:\n  - vtype: optional string naming the logical type (e.g. \"string\", \"\
      int\", \"target_ref\");\n  - desc: optional description string.\n"
    ```
- **clause.edgek0.fields** (kind: clause)
  - label: EdgeK0 Fields
  - Extra fields:
    ```yml
    label: EdgeK0 Fields
    status: normative
    text: "An EdgeK0 MUST have:\n  - from: NodeK0 ID (string) in the same GraphFrameK0;\n  - to:\
      \ NodeK0 ID (string) in the same GraphFrameK0;\n  - type: non-empty string describing the\
      \ edge semantics (e.g. contains, depends_on);\nIt MAY have:\n  - id: optional string identifier;\n\
      \  - attrs: optional list of AttrK0;\n  - metrics: optional list of MetricK0.\nGF0 does\
      \ not constrain the set of EdgeK0.type values beyond non-empty strings; higher- level specs\
      \ MUST define allowed edge types where needed.\n"
    ```
- **clause.edgek0.integrity** (kind: clause)
  - label: Edge Integrity (Structural)
  - Extra fields:
    ```yml
    label: Edge Integrity (Structural)
    status: normative
    text: 'EdgeK0.from and EdgeK0.to MUST reference existing NodeK0 IDs in the same GraphFrameK0.
      Edges that reference missing nodes violate structural integrity.

      '
    ```
- **clause.extension.canon_mapping** (kind: clause)
  - label: Mapping to canon.Graph
  - Extra fields:
    ```yml
    label: Mapping to canon.Graph
    status: informative
    text: 'Implementations MAY embed or derive GF0 graphs from canon.Graph values. However, GF0
      is defined at the YAML/JSON frame layer and does not require a one-to-one mapping to canon.Graph.
      When such a mapping exists, its semantics SHOULD be specified in a separate SpecFrame.

      '
    ```
- **clause.extension.specialization** (kind: clause)
  - label: Specialization via NodeK0.kind and EdgeK0.type
  - Extra fields:
    ```yml
    label: Specialization via NodeK0.kind and EdgeK0.type
    status: informative
    text: 'Higher-level schemas (SpecFrame, TaskFrame, EvidenceFrame, KernelCore, etc.) MUST specialize
      GF0 by constraining NodeK0.kind, EdgeK0.type, and attribute conventions, rather than redefining
      graph structure. GF0 remains the single canonical graph schema.

      '
    ```
- **clause.graphframe.attrs** (kind: clause)
  - label: Graph-level attributes
  - Extra fields:
    ```yml
    label: Graph-level attributes
    status: normative
    text: 'GraphFrameK0.attrs is an ordered slice of AttrK0 representing frame-level metadata
      (e.g. domain tags, doc build hints, repository routing hints, provenance). It MUST NOT be
      used to encode structural graph semantics; structural semantics are encoded only by nodes
      and edges. Duplicate keys are allowed and order is significant (list semantics).

      '
    ```
- **clause.graphframe.fields** (kind: clause)
  - label: GraphFrameK0 Fields
  - Extra fields:
    ```yml
    label: GraphFrameK0 Fields
    status: normative
    text: "A GraphFrameK0 value MUST have the following top-level fields:\n  - graph_id: non-empty\
      \ string identifying the frame;\n  - version: non-empty string identifying the frame's version\
      \ (logical or semantic);\n  - attrs: list of AttrK0 values (possibly empty);\n  - nodes:\
      \ list of NodeK0 values (possibly empty);\n  - edges: list of EdgeK0 values (possibly empty);\n\
      \  - meta: list of MetaGraph values (GraphFrameK0 instances), possibly empty.\nThese fields\
      \ MUST be present in the canonical form. Empty lists MUST be encoded as [] and MUST NOT\
      \ be encoded as null or omitted.\n"
    ```
- **clause.graphframe.identity** (kind: clause)
  - label: Graph Identity
  - Extra fields:
    ```yml
    label: Graph Identity
    status: normative
    text: 'graph_id is a logical identifier for the frame. It MUST be stable within a given repository
      or namespace. Different versions of the same conceptual graph SHOULD share the same graph_id
      but use distinct version values.

      '
    ```
- **clause.meta.fractal** (kind: clause)
  - label: Fractal Meta Graphs
  - Extra fields:
    ```yml
    label: Fractal Meta Graphs
    status: normative
    text: 'The meta field of a GraphFrameK0 is a list of subgraphs, each of which is itself a
      GraphFrameK0 with the same fields {graph_id, version, attrs, nodes, edges, meta}. This recursive
      structure allows auxiliary views, indexes, or annotations to be attached without changing
      the primary frame.

      '
    ```
- **clause.meta.scoping** (kind: clause)
  - label: MetaGraph Scoping
  - Extra fields:
    ```yml
    label: MetaGraph Scoping
    status: normative
    text: 'MetaGraphs MUST be structurally independent: their node IDs and edges are scoped within
      the subgraph. References from a MetaGraph into the parent graph MUST be expressed via attributes
      (e.g. parent_node_id) or well-defined edge types with explicit semantics.

      '
    ```
- **clause.meta.usage** (kind: clause)
  - label: Examples of Meta Usage
  - Extra fields:
    ```yml
    label: Examples of Meta Usage
    status: informative
    text: 'Common uses of meta include: alternative layout graphs, index structures, commentary
      layers, or regime annotations. Higher-level specs SHOULD document their usage of meta explicitly
      rather than overloading it.

      '
    ```
- **clause.metrick0.structure** (kind: clause)
  - label: MetricK0 Structure
  - Extra fields:
    ```yml
    label: MetricK0 Structure
    status: normative
    text: "MetricK0 MUST at least contain:\n  - name: non-empty string;\n  - value: numeric value\
      \ (e.g. float64).\nIt MAY contain:\n  - unit: optional string;\n  - desc: optional description.\n"
    ```
- **clause.nodek0.attrs_metrics** (kind: clause)
  - label: Node Attributes and Metrics
  - Extra fields:
    ```yml
    label: Node Attributes and Metrics
    status: normative
    text: 'Node attrs and metrics MUST be stored as slices and MUST NOT be represented as maps
      in the canonical form. Keys and names MUST be non-empty. The interpretation of specific
      keys is delegated to higher-level specs (SpecFrame, TaskFrame, etc.).

      '
    ```
- **clause.nodek0.fields** (kind: clause)
  - label: NodeK0 Fields
  - Extra fields:
    ```yml
    label: NodeK0 Fields
    status: normative
    text: "A NodeK0 MUST have:\n  - id: non-empty string, unique within the containing GraphFrameK0;\n\
      \  - kind: non-empty string describing the node's semantic role (e.g. spec, section, kernel);\n\
      \  - label: optional human-readable string;\n  - attrs: optional list of AttrK0;\n  - metrics:\
      \ optional list of MetricK0.\nThe set of allowed NodeK0.kind values is not constrained by\
      \ GF0; higher-level specs (SpecFrame, TaskFrame, etc.) MUST define their own allowed kinds.\n"
    ```
- **clause.validation.attrs_backcompat** (kind: clause)
  - label: Back-compat for legacy frames missing attrs
  - Extra fields:
    ```yml
    label: Back-compat for legacy frames missing attrs
    status: informative
    text: 'Loaders MAY accept legacy GF0 frames that omit the top-level attrs field and treat
      it as an empty list. Canonical serialization MUST emit attrs explicitly (attrs: []) in the
      canonical form.

      '
    ```
- **clause.validation.edge_integrity** (kind: clause)
  - label: Edge Integrity (Validation Rule)
  - Extra fields:
    ```yml
    label: Edge Integrity (Validation Rule)
    status: normative
    text: 'A GraphFrameK0 validator MUST enforce clause.edgek0.integrity: for every EdgeK0, from
      and to MUST reference existing NodeK0 IDs in the same frame. Missing endpoints MUST cause
      validation failure.

      '
    ```
- **clause.validation.graph_id_version** (kind: clause)
  - label: Graph ID and Version Non-Empty
  - Extra fields:
    ```yml
    label: Graph ID and Version Non-Empty
    status: normative
    text: 'graph_id and version MUST be non-empty strings. Frames with empty graph_id or version
      MUST be rejected.

      '
    ```
- **clause.validation.meta_recursion** (kind: clause)
  - label: Meta Recursion
  - Extra fields:
    ```yml
    label: Meta Recursion
    status: normative
    text: 'Validation of a GraphFrameK0 MUST recursively validate each MetaGraph according to
      the same GF0 rules. Implementations MUST protect against unbounded recursion (e.g. cycles
      via references) and MAY impose a maximum meta depth.

      '
    ```
- **clause.validation.node_id_uniqueness** (kind: clause)
  - label: Node ID Uniqueness
  - Extra fields:
    ```yml
    label: Node ID Uniqueness
    status: normative
    text: 'Within a single GraphFrameK0, all NodeK0 IDs MUST be unique. Duplicate node IDs MUST
      cause validation failure.

      '
    ```
- **ref.spec.canon-k1** (kind: spec_ref)
  - label: Canon graph mapping spec
  - Extra fields:
    ```yml
    label: Canon graph mapping spec
    status: informative
    target_graph_id: spec://_kernel/canon/canon-k1
    ```
- **section.1.overview** (kind: section)
  - Extra fields:
    ```yml
    status: normative
    title: Overview
    ```
- **section.2.structure** (kind: section)
  - Extra fields:
    ```yml
    status: normative
    title: GraphFrame Structure
    ```
- **section.3.nodes** (kind: section)
  - Extra fields:
    ```yml
    status: normative
    title: NodeK0 Structure
    ```
- **section.4.edges** (kind: section)
  - Extra fields:
    ```yml
    status: normative
    title: EdgeK0 Structure
    ```
- **section.5.meta** (kind: section)
  - Extra fields:
    ```yml
    status: normative
    title: Fractal Meta Graphs
    ```
- **section.6.invariants** (kind: section)
  - Extra fields:
    ```yml
    status: normative
    title: Invariants and Validation
    ```
- **section.7.extension** (kind: section)
  - Extra fields:
    ```yml
    status: informative
    title: Extension and Specialization
    ```
- **spec://_kernel/gf/gf0-k1** (kind: spec)
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'GraphFrame K0 (GF0) defines the canonical graph container used by GraphBrain. It
      is a minimal, fractal schema with fields {graph_id, version, attrs, nodes, edges, meta},
      where meta is a list of subgraphs with the same structure. GF0 provides the substrate for
      SpecFrames, TaskFrames, EvidenceFrames, and other higher-level frames.

      '
    title: GraphFrame K0 — Canonical Fractal Graph Schema
    ```
- **term.attr_k0** (kind: term)
  - label: AttrK0
  - Extra fields:
    ```yml
    label: AttrK0
    status: normative
    summary: 'Simple key–value attribute struct with optional type and description, stored in
      a deterministic slice.

      '
    ```
- **term.edge_k0** (kind: term)
  - label: EdgeK0
  - Extra fields:
    ```yml
    label: EdgeK0
    status: normative
    summary: 'Directed edge in a GraphFrameK0 with from, to, and type fields, and optional ID
      and attrs/metrics. from/to refer to NodeK0 IDs in the same frame.

      '
    ```
- **term.graphframe_k0** (kind: term)
  - label: GraphFrameK0
  - Extra fields:
    ```yml
    label: GraphFrameK0
    status: normative
    summary: 'Minimal graph container with fields {graph_id, version, attrs, nodes, edges, meta},
      where nodes and edges follow NodeK0 and EdgeK0, and meta is a list of sub-GraphFrameK0 instances.

      '
    ```
- **term.meta_graph** (kind: term)
  - label: MetaGraph
  - Extra fields:
    ```yml
    label: MetaGraph
    status: normative
    summary: 'Subgraph stored in the meta list of a GraphFrameK0. Each MetaGraph is itself a GraphFrameK0
      and can carry auxiliary structure or views without changing the primary frame.

      '
    ```
- **term.metric_k0** (kind: term)
  - label: MetricK0
  - Extra fields:
    ```yml
    label: MetricK0
    status: normative
    summary: 'Simple name–value metric struct with optional unit and description, stored in a
      deterministic slice.

      '
    ```
- **term.node_k0** (kind: term)
  - label: NodeK0
  - Extra fields:
    ```yml
    label: NodeK0
    status: normative
    summary: 'Node in a GraphFrameK0 with an ID, kind, optional label, and optional attrs/metrics
      slices. Node IDs are unique within a given GraphFrameK0.

      '
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| clause.edgek0.fields | term.edge_k0 | defines |  |  |  |
| clause.graphframe.fields | term.graphframe_k0 | defines |  |  |  |
| clause.meta.fractal | term.meta_graph | defines |  |  |  |
| clause.nodek0.fields | term.node_k0 | defines |  |  |  |
| section.2.structure | clause.graphframe.attrs | contains |  |  |  |
| section.2.structure | clause.graphframe.fields | contains |  |  |  |
| section.2.structure | clause.graphframe.identity | contains |  |  |  |
| section.2.structure | term.graphframe_k0 | contains |  |  |  |
| section.3.nodes | clause.attr_metric.slice_not_map | contains |  |  |  |
| section.3.nodes | clause.attrk0.structure | contains |  |  |  |
| section.3.nodes | clause.metrick0.structure | contains |  |  |  |
| section.3.nodes | clause.nodek0.attrs_metrics | contains |  |  |  |
| section.3.nodes | clause.nodek0.fields | contains |  |  |  |
| section.3.nodes | term.attr_k0 | contains |  |  |  |
| section.3.nodes | term.metric_k0 | contains |  |  |  |
| section.3.nodes | term.node_k0 | contains |  |  |  |
| section.4.edges | clause.edgek0.fields | contains |  |  |  |
| section.4.edges | clause.edgek0.integrity | contains |  |  |  |
| section.4.edges | term.edge_k0 | contains |  |  |  |
| section.5.meta | clause.meta.fractal | contains |  |  |  |
| section.5.meta | clause.meta.scoping | contains |  |  |  |
| section.5.meta | clause.meta.usage | contains |  |  |  |
| section.5.meta | term.meta_graph | contains |  |  |  |
| section.6.invariants | clause.validation.edge_integrity | contains |  |  |  |
| section.6.invariants | clause.validation.graph_id_version | contains |  |  |  |
| section.6.invariants | clause.validation.meta_recursion | contains |  |  |  |
| section.6.invariants | clause.validation.node_id_uniqueness | contains |  |  |  |
| section.7.extension | clause.extension.canon_mapping | contains |  |  |  |
| section.7.extension | clause.extension.specialization | contains |  |  |  |
| section.7.extension | ref.spec.canon-k1 | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.1.overview | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.2.structure | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.3.nodes | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.4.edges | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.5.meta | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.6.invariants | contains |  |  |  |
| spec://_kernel/gf/gf0-k1 | section.7.extension | contains |  |  |  |

## Contains Tree
- spec://_kernel/gf/gf0-k1
  - section.1.overview
  - section.2.structure
    - clause.graphframe.attrs
    - clause.graphframe.fields
    - clause.graphframe.identity
    - term.graphframe_k0
  - section.3.nodes
    - clause.attr_metric.slice_not_map
    - clause.attrk0.structure
    - clause.metrick0.structure
    - clause.nodek0.attrs_metrics
    - clause.nodek0.fields
    - term.attr_k0
    - term.metric_k0
    - term.node_k0
  - section.4.edges
    - clause.edgek0.fields
    - clause.edgek0.integrity
    - term.edge_k0
  - section.5.meta
    - clause.meta.fractal
    - clause.meta.scoping
    - clause.meta.usage
    - term.meta_graph
  - section.6.invariants
    - clause.validation.edge_integrity
    - clause.validation.graph_id_version
    - clause.validation.meta_recursion
    - clause.validation.node_id_uniqueness
  - section.7.extension
    - clause.extension.canon_mapping
    - clause.extension.specialization
    - ref.spec.canon-k1


## Meta
- meta[1]
  - Extra fields:
    ```yml
    depends_on:
    - spec://_kernel/spec/specframe-k1
    - spec://_kernel/canon/canon-k1
    domain: graphbrain.gf0
    intended_consumers:
    - SpecFrame
    - TaskFrame
    - EvidenceFrame
    - KernelCore
    notes: 'GF0 is the single canonical graph schema for GraphBrain. All higher-level frames MUST
      treat GF0 as their structural base and specialize it only via NodeK0.kind, EdgeK0.type,
      and attribute conventions.

      '
    profile: specframe-k1
    ```
