# GraphFrame K0 — Canonical Fractal Graph Schema
<a id="spec-kernel-gf-gf0-k1-2fe6147f"></a>

## Overview
<a id="section-1-overview-80ccecc5"></a>

## GraphFrame Structure
<a id="section-2-structure-6f82a29d"></a>

**GraphFrameK0** _(normative)_

Minimal graph container with fields {graph_id, version, attrs, nodes, edges, meta}, where nodes and edges follow NodeK0 and EdgeK0, and meta is a list of sub-GraphFrameK0 instances.

**Graph-level attributes** _(normative)_

GraphFrameK0.attrs is an ordered slice of AttrK0 representing frame-level metadata (e.g. domain tags, doc build hints, repository routing hints, provenance). It MUST NOT be used to encode structural graph semantics; structural semantics are encoded only by nodes and edges. Duplicate keys are allowed and order is significant (list semantics).

**GraphFrameK0 Fields** _(normative)_

A GraphFrameK0 value MUST have the following top-level fields: - graph_id: non-empty string identifying the frame; - version: non-empty string identifying the frame's version (logical or semantic); - attrs: list of AttrK0 values (possibly empty); - nodes: list of NodeK0 values (possibly empty); - edges: list of EdgeK0 values (possibly empty); - meta: list of MetaGraph values (GraphFrameK0 instances), possibly empty. These fields MUST be present in the canonical form. Empty lists MUST be encoded as [] and MUST NOT be encoded as null or omitted.

**Graph Identity** _(normative)_

graph*id is a logical identifier for the frame. It MUST be stable within a given repository or namespace. Different versions of the same conceptual graph SHOULD share the same graph*id but use distinct version values.

## NodeK0 Structure
<a id="section-3-nodes-f18c3596"></a>

**AttrK0** _(normative)_

Simple key–value attribute struct with optional type and description, stored in a deterministic slice.

**MetricK0** _(normative)_

Simple name–value metric struct with optional unit and description, stored in a deterministic slice.

**NodeK0** _(normative)_

Node in a GraphFrameK0 with an ID, kind, optional label, and optional attrs/metrics slices. Node IDs are unique within a given GraphFrameK0.

**Slices, Not Maps** _(normative)_

AttrK0 and MetricK0 collections MUST be represented as ordered slices, not maps. This ensures deterministic ordering and stable serialization across implementations.

**AttrK0 Structure** _(normative)_

AttrK0 MUST at least contain: - key: non-empty string; - value: string (UTF-8). It MAY contain: - vtype: optional string naming the logical type (e.g. "string", "int", "target_ref"); - desc: optional description string.

**MetricK0 Structure** _(normative)_

MetricK0 MUST at least contain: - name: non-empty string; - value: numeric value (e.g. float64). It MAY contain: - unit: optional string; - desc: optional description.

**Node Attributes and Metrics** _(normative)_

Node attrs and metrics MUST be stored as slices and MUST NOT be represented as maps in the canonical form. Keys and names MUST be non-empty. The interpretation of specific keys is delegated to higher-level specs (SpecFrame, TaskFrame, etc.).

**NodeK0 Fields** _(normative)_

A NodeK0 MUST have: - id: non-empty string, unique within the containing GraphFrameK0; - kind: non-empty string describing the node's semantic role (e.g. spec, section, kernel); - label: optional human-readable string; - attrs: optional list of AttrK0; - metrics: optional list of MetricK0. The set of allowed NodeK0.kind values is not constrained by GF0; higher-level specs (SpecFrame, TaskFrame, etc.) MUST define their own allowed kinds.

## EdgeK0 Structure
<a id="section-4-edges-f8a0fc38"></a>

**EdgeK0** _(normative)_

Directed edge in a GraphFrameK0 with from, to, and type fields, and optional ID and attrs/metrics. from/to refer to NodeK0 IDs in the same frame.

**EdgeK0 Fields** _(normative)_

An EdgeK0 MUST have: - from: NodeK0 ID (string) in the same GraphFrameK0; - to: NodeK0 ID (string) in the same GraphFrameK0; - type: non-empty string describing the edge semantics (e.g. contains, depends_on); It MAY have: - id: optional string identifier; - attrs: optional list of AttrK0; - metrics: optional list of MetricK0. GF0 does not constrain the set of EdgeK0.type values beyond non-empty strings; higher- level specs MUST define allowed edge types where needed.

**Edge Integrity (Structural)** _(normative)_

EdgeK0.from and EdgeK0.to MUST reference existing NodeK0 IDs in the same GraphFrameK0. Edges that reference missing nodes violate structural integrity.

## Fractal Meta Graphs
<a id="section-5-meta-f38f37d1"></a>

**MetaGraph** _(normative)_

Subgraph stored in the meta list of a GraphFrameK0. Each MetaGraph is itself a GraphFrameK0 and can carry auxiliary structure or views without changing the primary frame.

**Fractal Meta Graphs** _(normative)_

The meta field of a GraphFrameK0 is a list of subgraphs, each of which is itself a GraphFrameK0 with the same fields {graph_id, version, attrs, nodes, edges, meta}. This recursive structure allows auxiliary views, indexes, or annotations to be attached without changing the primary frame.

**MetaGraph Scoping** _(normative)_

MetaGraphs MUST be structurally independent: their node IDs and edges are scoped within the subgraph. References from a MetaGraph into the parent graph MUST be expressed via attributes (e.g. parent*node*id) or well-defined edge types with explicit semantics.

**Examples of Meta Usage** _(informative)_

Common uses of meta include: alternative layout graphs, index structures, commentary layers, or regime annotations. Higher-level specs SHOULD document their usage of meta explicitly rather than overloading it.

## Invariants and Validation
<a id="section-6-invariants-6bcc8d37"></a>

**Edge Integrity (Validation Rule)** _(normative)_

A GraphFrameK0 validator MUST enforce clause.edgek0.integrity: for every EdgeK0, from and to MUST reference existing NodeK0 IDs in the same frame. Missing endpoints MUST cause validation failure.

**Graph ID and Version Non-Empty** _(normative)_

graph*id and version MUST be non-empty strings. Frames with empty graph*id or version MUST be rejected.

**Meta Recursion** _(normative)_

Validation of a GraphFrameK0 MUST recursively validate each MetaGraph according to the same GF0 rules. Implementations MUST protect against unbounded recursion (e.g. cycles via references) and MAY impose a maximum meta depth.

**Node ID Uniqueness** _(normative)_

Within a single GraphFrameK0, all NodeK0 IDs MUST be unique. Duplicate node IDs MUST cause validation failure.

## Extension and Specialization
<a id="section-7-extension-7459b37d"></a>

**Mapping to canon.Graph** _(informative)_

Implementations MAY embed or derive GF0 graphs from canon.Graph values. However, GF0 is defined at the YAML/JSON frame layer and does not require a one-to-one mapping to canon.Graph. When such a mapping exists, its semantics SHOULD be specified in a separate SpecFrame.

**Specialization via NodeK0.kind and EdgeK0.type** _(informative)_

Higher-level schemas (SpecFrame, TaskFrame, EvidenceFrame, KernelCore, etc.) MUST specialize GF0 by constraining NodeK0.kind, EdgeK0.type, and attribute conventions, rather than redefining graph structure. GF0 remains the single canonical graph schema.

## References
<a id="refs-e812cd2d"></a>

- Canon graph mapping spec ()
