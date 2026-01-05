# spec://_kernel/spec/specframe-k1
- version: 0.3.0
- nodes: 38
- edges: 43
- meta: 0
## Nodes
- **clause.attrs.clause** (kind: clause)
  - label: Attributes for clause nodes
  - Extra fields:
    ```yml
    label: Attributes for clause nodes
    status: normative
    text: "A node with kind == 'clause' MUST provide:\n  - 'label' : short handle for the clause,\n\
      \  - 'status': SpecStatus.\nIt SHOULD provide:\n  - 'text'  : full clause text in natural\
      \ language.\n"
    എന്ത
- **clause.attrs.example** (kind: clause)
  - label: Attributes for example nodes
  - Extra fields:
    ```yml
    label: Attributes for example nodes
    status: informative
    text: "A node with kind == 'example' MUST provide:\n  - 'label' : short identifier for the\
      \ example,\n  - 'status': SpecStatus (typically 'informative').\nIt SHOULD provide:\n  -\
      \ 'text'  : free-form example text or code snippet.\n"
    എന്ത
- **clause.attrs.property** (kind: clause)
  - label: Attributes for property nodes
  - Extra fields:
    ```yml
    label: Attributes for property nodes
    status: normative
    text: "A node with kind == 'property' MUST provide:\n  - 'label' : short name of the property,\n\
      \  - 'status': SpecStatus.\nProperty nodes MAY carry arbitrary additional attributes (lists,\
      \ enums, thresholds) that are interpreted by tooling.\n"
    എന്ത
- **clause.attrs.required** (kind: clause)
  - label: Required attributes per node kind
  - Extra fields:
    ```yml
    label: Required attributes per node kind
    status: normative
    text: "A SpecFrame validator MUST treat missing required attributes as a hard validation error.\
      \ Required attributes per kind are:\n  - spec     : title, status, summary, profile\n  -\
      \ section  : title, status\n  - term     : label, status\n  - clause   : label, status\n\
      \  - property : label, status\n  - example  : label, status\n  - spec_ref : target_graph_id\n"
    എന്ത
- **clause.attrs.section** (kind: clause)
  - label: Attributes for section nodes
  - Extra fields:
    ```yml
    label: Attributes for section nodes
    status: normative
    text: "A node with kind == 'section' MUST provide:\n  - 'title' : short section title,\n \
      \ - 'status': SpecStatus.\nIt SHOULD provide:\n  - 'order' : integer for ordering sections\
      \ within the spec.\nSections MAY nest other sections via 'contains'.\n"
    എന്ത
- **clause.attrs.spec** (kind: clause)
  - label: Attributes for spec nodes
  - Extra fields:
    ```yml
    label: Attributes for spec nodes
    status: normative
    text: "A node with kind == 'spec' MUST provide at least:\n  - 'title'   : short human-readable\
      \ title,\n  - 'status'  : SpecStatus,\n  - 'summary' : short description of the spec's scope,\n\
      \  - 'profile' : string identifying the spec profile, e.g. 'specframe-k1'.\nThe spec node\
      \ MAY also include 'version_note', 'domain', and additional profile-specific attributes.\n"
    എന്ത
- **clause.attrs.spec_ref** (kind: clause)
  - label: Attributes for spec_ref nodes
  - Extra fields:
    ```yml
    label: Attributes for spec_ref nodes
    status: normative
    text: "A node with kind == 'spec_ref' MUST provide:\n  - 'target_graph_id' : canonical graph_id\
      \ of the referenced spec or frame.\nIt MAY provide:\n  - 'label' : short human-readable\
      \ label,\n  - 'note'  : explanatory text about the reference.\n"
    എന്ത
- **clause.attrs.status_enum** (kind: clause)
  - label: Allowed status values
  - Extra fields:
    ```yml
    label: Allowed status values
    status: normative
    text: "For all nodes in a SpecFrame, the status attribute MUST be one of:\n  - 'normative',\n\
      \  - 'informative',\n  - 'experimental'.\n"
    എന്ത
- **clause.attrs.term** (kind: clause)
  - label: Attributes for term nodes
  - Extra fields:
    ```yml
    label: Attributes for term nodes
    status: normative
    text: "A node with kind == 'term' MUST provide:\n  - 'label' : short name of the term,\n \
      \ - 'status': SpecStatus.\nThe primary definition text MAY be stored in 'text'. Terms are\
      \ usually linked via 'defines' edges from clauses that define them.\n"
    എന്ത
- **clause.edge.contains** (kind: clause)
  - label: contains edge semantics
  - Extra fields:
    ```yml
    label: contains edge semantics
    status: normative
    text: '''contains'' edges encode the structural tree of the spec. The root ''spec'' node MUST
      contain one or more ''section'' nodes. Section nodes MAY contain other sections, terms,
      clauses, properties, and examples. Contains edges MUST form an acyclic tree (or forest)
      rooted at the spec node.

      '
    എന്ത
- **clause.edge_types.allowed** (kind: clause)
  - label: Allowed edge types
  - Extra fields:
    ```yml
    label: Allowed edge types
    status: normative
    text: "Within a SpecFrame, EdgeK0.type MUST be one of:\n  - 'contains'   : structural containment\
      \ / hierarchy,\n  - 'depends_on' : spec-level dependency on another node or spec,\n  - 'defines'\
      \    : term or clause defines another concept,\n  - 'refines'    : clause refines or tightens\
      \ another clause,\n  - 'refers_to'  : non-normative reference to another node or spec,\n\
      \  - 'example_of' : examples illustrating a term or clause.\nAny other value MUST be reported\
      \ as a validation error.\n"
    എന്ത
- **clause.frame_metadata.location** (kind: clause)
  - label: Frame-level metadata location
  - Extra fields:
    ```yml
    label: Frame-level metadata location
    status: normative
    text: 'In SpecFrames, frame-level metadata (publish routing, domain tags, dependency tags,
      audience tags) SHOULD be stored in GraphFrameK0.attrs. GraphFrameK0.meta MUST be used only
      for true MetaGraphs (aux layout/index/view graphs) as defined by GF0. A SpecFrame validator
      MUST NOT require any particular GraphFrameK0.attrs keys; attrs is tooling- facing metadata
      and does not affect the node/edge validation rules.

      '
    എന്ത
- **clause.frame_metadata.recommended_keys** (kind: clause)
  - label: Recommended SpecFrame attrs keys
  - Extra fields:
    ```yml
    label: Recommended SpecFrame attrs keys
    status: informative
    text: "Tooling MAY adopt the following conventional GraphFrameK0.attrs keys for SpecFrames:\n\
      \  - domain\n  - depends_on (repeatable)\n  - intended_consumer (repeatable)\n  - publish.root\n\
      \  - publish.path\n  - publish.slug\n"
    എന്ത
- **clause.integration.usage** (kind: clause)
  - label: Use in GraphBrain and specgen
  - Extra fields:
    ```yml
    label: Use in GraphBrain and specgen
    status: informative
    text: 'GraphBrain and specgen SHOULD treat SpecFrame K1 as the canonical schema for specs.
      Specs for other domains (canon, CBF, GSKernel, TaskFrame, EvidenceFrame, KernelCore, regimes)
      SHOULD be represented as SpecFrames and validated against this schema so that they can be
      composed, diffed, and refactored uniformly.

      '
    എന്ത
- **clause.node_kinds.allowed** (kind: clause)
  - label: Allowed node kinds
  - Extra fields:
    ```yml
    label: Allowed node kinds
    status: normative
    text: "Within a SpecFrame, NodeK0.kind MUST be one of:\n  - 'spec'      : the root specification\
      \ node (exactly one per SpecFrame),\n  - 'section'   : top-level or nested sections grouping\
      \ terms and clauses,\n  - 'term'      : definitions of key concepts,\n  - 'clause'    :\
      \ normative or informative statements,\n  - 'property'  : small structured facts (enums,\
      \ lists, thresholds),\n  - 'example'   : worked examples illustrating other nodes,\n  -\
      \ 'spec_ref'  : references to other specs or frames.\nAny other value MUST be reported as\
      \ a validation error.\n"
    എന്ത
- **clause.node_kinds.root** (kind: clause)
  - label: Root spec node
  - Extra fields:
    ```yml
    label: Root spec node
    status: normative
    text: "Each SpecFrame MUST contain exactly one node with:\n  - id == graph_id,\n  - kind ==\
      \ 'spec',\n  - status in {'normative', 'informative', 'experimental'}.\nThis node is the\
      \ root of the spec and is the unique entry point for reachability and top-level attributes.\n"
    എന്ത
- **clause.scope.1** (kind: clause)
  - label: Scope of SpecFrame K1
  - Extra fields:
    ```yml
    label: Scope of SpecFrame K1
    status: normative
    text: 'SpecFrame K1 specifies the canonical schema for representing specifications as GraphFrame
      K0 graphs. A SpecFrame is any GF0 graph whose root node has kind = ''spec'' and profile
      = ''specframe-k1''. All such graphs MUST conform to the node, edge, and attribute conventions
      defined in this spec.

      '
    എന്ത
- **clause.scope.2** (kind: clause)
  - label: Intended consumers
  - Extra fields:
    ```yml
    label: Intended consumers
    status: informative
    text: 'SpecFrame K1 is intended for: (a) human spec authors, (b) GraphBrain kernels that load,
      validate, and refactor specs, and (c) LLM workers that generate or update specs from code,
      docs, or other frames.

      '
    എന്ത
- **clause.validation.contains_tree** (kind: clause)
  - label: Contains edges form a tree
  - Extra fields:
    ```yml
    label: Contains edges form a tree
    status: normative
    text: '''contains'' edges MUST form an acyclic tree (or forest) rooted at the spec node. Cycles
      or multiple parents for the same node via ''contains'' are considered hard validation failures.

      '
    എന്ത
- **clause.validation.edge_types** (kind: clause)
  - label: Edge type validation
  - Extra fields:
    ```yml
    label: Edge type validation
    status: normative
    text: 'A SpecFrame validator MUST reject any edge whose type attribute is not in the allowed
      set specified by property.edge_types. Unknown edge types are considered hard validation
      failures.

      '
    എന്ത
- **clause.validation.node_kinds** (kind: clause)
  - label: Node kind validation
  - Extra fields:
    ```yml
    label: Node kind validation
    status: normative
    text: 'A SpecFrame validator MUST reject any node whose kind attribute is not in the allowed
      set specified by property.node_kinds. Unknown or misspelled kinds are considered hard validation
      failures.

      '
    എന്ത
- **clause.validation.reachability** (kind: clause)
  - label: Reachability from root
  - Extra fields:
    ```yml
    label: Reachability from root
    status: normative
    text: 'All normative nodes in a SpecFrame SHOULD be reachable from the root spec node via
      one or more ''contains'' edges. Unreachable normative nodes SHOULD be treated as errors
      or at least strong warnings by tooling.

      '
    എന്ത
- **property.edge_types** (kind: property)
  - label: Allowed Edge Types
  - Extra fields:
    ```yml
    edge_types:
    - contains
    - depends_on
    - defines
    - refines
    - refers_to
    - example_of
    label: Allowed Edge Types
    status: normative
    എന്ത
- **property.node_kinds** (kind: property)
  - label: Allowed Node Kinds
  - Extra fields:
    ```yml
    label: Allowed Node Kinds
    node_kinds:
    - spec
    - section
    - term
    - clause
    - property
    - example
    - spec_ref
    status: normative
    എന്ത
- **property.status_enum** (kind: property)
  - label: Spec Status Enum
  - Extra fields:
    ```yml
    label: Spec Status Enum
    status: normative
    status_values:
    - normative
    - informative
    - experimental
    എന്ത
- **ref.spec.canon-k1** (kind: spec_ref)
  - label: Canon envelope mappings
  - Extra fields:
    ```yml
    label: Canon envelope mappings
    status: informative
    target_graph_id: spec://_kernel/canon/canon-k1
    എന്ത
- **ref.spec.gf0-k1** (kind: spec_ref)
  - label: GraphFrame K0 schema
  - Extra fields:
    ```yml
    label: GraphFrame K0 schema
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    എന്ത
- **ref.spec.targetref-k1** (kind: spec_ref)
  - label: TargetRef naming scheme
  - Extra fields:
    ```yml
    label: TargetRef naming scheme
    status: informative
    target_graph_id: spec://_kernel/targetref/targetref-k1
    എന്ത
- **section.1.scope** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Scope and Intent
    എന്ത
- **section.2.node_kinds** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Node Kinds
    എന്ത
- **section.3.edge_kinds** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Edge Types
    എന്ത
- **section.4.attributes** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: Attributes
    എന്ത
- **section.5.validation** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: Validation Invariants
    എന്ത
- **section.6.integration** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: informative
    title: Integration and Usage
    എന്ത
- **spec://_kernel/spec/specframe-k1** (kind: spec)
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'SpecFrame K1 defines how specifications themselves are represented as GraphFrame
      K0 graphs. It constrains node kinds, edge types, and attribute conventions so that specs
      can be encoded as sections, terms, clauses, and properties in a deterministic, machine-readable
      way suitable for GraphBrain kernels and LLM workers.

      '
    title: SpecFrame K1 — Canonical Specification Graph Schema
    എന്ത
- **term.edge_type** (kind: term)
  - label: EdgeK0.type in SpecFrames
  - Extra fields:
    ```yml
    label: EdgeK0.type in SpecFrames
    status: normative
    text: 'In SpecFrames, the EdgeK0.type field encodes structural and semantic relationships
      between nodes. Only a small fixed set of edge types is allowed.

      '
    എന്ത
- **term.node_kind** (kind: term)
  - label: NodeK0.kind in SpecFrames
  - Extra fields:
    ```yml
    label: NodeK0.kind in SpecFrames
    status: normative
    text: 'In SpecFrames, the NodeK0.kind field encodes the logical role of each node in the spec:
      spec, section, term, clause, property, example, or spec_ref.

      '
    എന്ത
- **term.status** (kind: term)
  - label: SpecStatus
  - Extra fields:
    ```yml
    label: SpecStatus
    status: normative
    text: "SpecStatus describes the normative weight of a node:\n  - 'normative'   : enforceable\
      \ spec law,\n  - 'informative' : non-binding explanatory material,\n  - 'experimental':\
      \ provisional or unstable guidance.\n"
    എന്ത

## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.scope | clause.scope.1 | contains |  |  |  |
| section.1.scope | clause.scope.2 | contains |  |  |  |
| section.2.node_kinds | clause.node_kinds.allowed | contains |  |  |  |
| section.2.node_kinds | clause.node_kinds.root | contains |  |  |  |
| section.2.node_kinds | property.node_kinds | contains |  |  |  |
| section.2.node_kinds | term.node_kind | contains |  |  |  |
| section.3.edge_kinds | clause.edge.contains | contains |  |  |  |
| section.3.edge_kinds | clause.edge_types.allowed | contains |  |  |  |
| section.3.edge_kinds | property.edge_types | contains |  |  |  |
| section.3.edge_kinds | term.edge_type | contains |  |  |  |
| section.4.attributes | clause.attrs.clause | contains |  |  |  |
| section.4.attributes | clause.attrs.example | contains |  |  |  |
| section.4.attributes | clause.attrs.property | contains |  |  |  |
| section.4.attributes | clause.attrs.required | contains |  |  |  |
| section.4.attributes | clause.attrs.section | contains |  |  |  |
| section.4.attributes | clause.attrs.spec | contains |  |  |  |
| section.4.attributes | clause.attrs.spec_ref | contains |  |  |  |
| section.4.attributes | clause.attrs.status_enum | contains |  |  |  |
| section.4.attributes | clause.attrs.term | contains |  |  |  |
| section.4.attributes | property.status_enum | refers_to |  |  |  |
| section.4.attributes | term.status | contains |  |  |  |
| section.5.validation | clause.validation.contains_tree | contains |  |  |  |
| section.5.validation | clause.validation.edge_types | contains |  |  |  |
| section.5.validation | clause.validation.node_kinds | contains |  |  |  |
| section.5.validation | clause.validation.reachability | contains |  |  |  |
| section.6.integration | clause.frame_metadata.location | contains |  |  |  |
| section.6.integration | clause.frame_metadata.recommended_keys | contains |  |  |  |
| section.6.integration | clause.integration.usage | contains |  |  |  |
| section.6.integration | ref.spec.canon-k1 | refers_to |  |  |  |
| section.6.integration | ref.spec.gf0-k1 | refers_to |  |  |  |
| section.6.integration | ref.spec.targetref-k1 | refers_to |  |  |  |
| spec://_kernel/spec/specframe-k1 | property.edge_types | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | property.node_kinds | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | property.status_enum | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | ref.spec.canon-k1 | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | ref.spec.gf0-k1 | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | ref.spec.targetref-k1 | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | section.1.scope | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | section.2.node_kinds | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | section.3.edge_kinds | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | section.4.attributes | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | section.5.validation | contains |  |  |  |
| spec://_kernel/spec/specframe-k1 | section.6.integration | contains |  |  |  |

## Contains Tree
- spec://_kernel/spec/specframe-k1
  - property.edge_types
  - property.node_kinds
  - property.status_enum
  - ref.spec.canon-k1
  - ref.spec.gf0-k1
  - ref.spec.targetref-k1
  - section.1.scope
    - clause.scope.1
    - clause.scope.2
  - section.2.node_kinds
    - clause.node_kinds.allowed
    - clause.node_kinds.root
    - property.node_kinds
    - term.node_kind
  - section.3.edge_kinds
    - clause.edge.contains
    - clause.edge_types.allowed
    - property.edge_types
    - term.edge_type
  - section.4.attributes
    - clause.attrs.clause
    - clause.attrs.example
    - clause.attrs.property
    - clause.attrs.required
    - clause.attrs.section
    - clause.attrs.spec
    - clause.attrs.spec_ref
    - clause.attrs.status_enum
    - clause.attrs.term
    - term.status
  - section.5.validation
    - clause.validation.contains_tree
    - clause.validation.edge_types
    - clause.validation.node_kinds
    - clause.validation.reachability
  - section.6.integration
    - clause.frame_metadata.location
    - clause.frame_metadata.recommended_keys
    - clause.integration.usage
