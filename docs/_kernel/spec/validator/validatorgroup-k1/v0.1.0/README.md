# spec://_kernel/validator/validatorgroup-k1
- version: 0.1.0
- nodes: 60
- edges: 59
- meta: 0
## Nodes
- **clause.codes.gf0_bad_edge** (kind: clause)
  - label: GF0.E.BAD_EDGE_ENDPOINT
  - Extra fields:
    ```yml
    label: GF0.E.BAD_EDGE_ENDPOINT
    status: normative
    text: 'Emitted when an edge endpoint references a missing node. details MUST include: edge_key,
      missing_endpoint (''from''|''to''), missing_node_id.

      '
    ```
- **clause.codes.gf0_dup_node** (kind: clause)
  - label: GF0.E.DUP_NODE_ID
  - Extra fields:
    ```yml
    label: GF0.E.DUP_NODE_ID
    status: normative
    text: 'Emitted when two or more nodes share the same id within one frame. details MUST include:
      node_id.

      '
    ```
- **clause.codes.gf0_empty_id_ver** (kind: clause)
  - label: GF0.E.EMPTY_GRAPH_ID_OR_VERSION
  - Extra fields:
    ```yml
    label: GF0.E.EMPTY_GRAPH_ID_OR_VERSION
    status: normative
    text: 'Emitted when graph_id or version is empty string. details MUST include: which (''graph_id''|''version'').

      '
    ```
- **clause.codes.gf0_missing_field** (kind: clause)
  - label: GF0.E.MISSING_FIELD
  - Extra fields:
    ```yml
    label: GF0.E.MISSING_FIELD
    status: normative
    text: 'Emitted when any required GF0 top-level field is missing in canonical form. details
      MUST include: field_name.

      '
    ```
- **clause.codes.link_missing_target_graph** (kind: clause)
  - label: LINK.E.MISSING_TARGET_GRAPH
  - Extra fields:
    ```yml
    label: LINK.E.MISSING_TARGET_GRAPH
    status: normative
    text: 'Emitted when a spec_ref.target_graph_id does not exist in the DocGroup. details MUST
      include: node_id, target_graph_id.

      '
    ```
- **clause.codes.link_unreachable_normative** (kind: clause)
  - label: LINK.W.UNREACHABLE_NORMATIVE
  - Extra fields:
    ```yml
    label: LINK.W.UNREACHABLE_NORMATIVE
    status: normative
    text: 'Emitted (as warning by default) when a normative node is unreachable from the SpecFrame
      root via ''contains''. details MUST include: node_id.

      '
    ```
- **clause.codes.requirement** (kind: clause)
  - label: Stable codes
  - Extra fields:
    ```yml
    label: Stable codes
    status: normative
    text: 'Codes MUST be stable across versions of implementations that claim conformance to this
      spec. Codes MUST NOT include implementation-specific details (paths, line numbers, stack
      traces).

      '
    ```
- **clause.codes.spec_bad_edge_type** (kind: clause)
  - label: SPEC.E.BAD_EDGE_TYPE
  - Extra fields:
    ```yml
    label: SPEC.E.BAD_EDGE_TYPE
    status: normative
    text: 'Emitted when a SpecFrame contains an edge with type not in the SpecFrame allowed set.
      details MUST include: edge_key, edge_type.

      '
    ```
- **clause.codes.spec_bad_kind** (kind: clause)
  - label: SPEC.E.BAD_NODE_KIND
  - Extra fields:
    ```yml
    label: SPEC.E.BAD_NODE_KIND
    status: normative
    text: 'Emitted when a SpecFrame contains a node with kind not in the SpecFrame allowed set.
      details MUST include: node_id, node_kind.

      '
    ```
- **clause.codes.spec_contains_cycle** (kind: clause)
  - label: SPEC.E.CONTAINS_CYCLE_OR_MULTIPARENT
  - Extra fields:
    ```yml
    label: SPEC.E.CONTAINS_CYCLE_OR_MULTIPARENT
    status: normative
    text: 'Emitted when ''contains'' edges are cyclic or a node has multiple ''contains'' parents.
      details MUST include: node_id. details MAY include: parent_ids (ordered list of parents),
      cycle_hint (string).

      '
    ```
- **clause.codes.spec_missing_attr** (kind: clause)
  - label: SPEC.E.MISSING_REQUIRED_ATTR
  - Extra fields:
    ```yml
    label: SPEC.E.MISSING_REQUIRED_ATTR
    status: normative
    text: 'Emitted when a required attribute per SpecFrame node kind is missing. details MUST
      include: node_id, node_kind, attr_name.

      '
    ```
- **clause.determinism.details_order** (kind: clause)
  - label: Details ordering
  - Extra fields:
    ```yml
    label: Details ordering
    status: normative
    text: 'Violation.details MUST be an ordered list of {key,value} pairs and MUST be sorted by
      key ascending lexicographic order, with stable tie-breaker by value ascending lexicographic
      order, unless a specific code explicitly requires a different order.

      '
    ```
- **clause.determinism.limits** (kind: clause)
  - label: Safety limits
  - Extra fields:
    ```yml
    label: Safety limits
    status: normative
    text: "Implementations MUST protect against unbounded recursion and pathological inputs by\
      \ enforcing:\n  - max_meta_depth: default 16 (caller may lower or raise; if exceeded, emit\
      \ GF0.E.META_DEPTH_EXCEEDED)\n  - max_nodes_per_graph: default 1,000,000 (if exceeded, emit\
      \ GF0.E.GRAPH_TOO_LARGE)\n  - max_edges_per_graph: default 2,000,000 (if exceeded, emit\
      \ GF0.E.GRAPH_TOO_LARGE)\nLimits MUST be applied deterministically and reported via stable\
      \ codes.\n"
    ```
- **clause.determinism.sorting** (kind: clause)
  - label: Canonical sorting rules
  - Extra fields:
    ```yml
    label: Canonical sorting rules
    status: normative
    text: "To ensure identical outputs across implementations:\n  - Graph processing order MUST\
      \ be ascending lexicographic order of graph_id.\n  - Within a graph, node lookup order MUST\
      \ be ascending lexicographic order of node.id.\n  - Edge lookup order MUST be ascending\
      \ lexicographic order of (edge.type, edge.from, edge.to, edge.id).\nAll violation lists\
      \ MUST be sorted by the canonical violation ordering (clause.determinism.violation_order).\n"
    ```
- **clause.determinism.violation_order** (kind: clause)
  - label: Canonical violation ordering
  - Extra fields:
    ```yml
    label: Canonical violation ordering
    status: normative
    text: "Violations MUST be sorted ascending by the tuple:\n  (severity_rank, code, stage, location.graph_id,\
      \ meta_path_join, node_id, edge_key, details_join)\nwhere:\n  - severity_rank(error)=0,\
      \ severity_rank(warning)=1\n  - meta_path_join is meta_path joined by ' > ' (empty string\
      \ if none)\n  - node_id and edge_key are empty string if absent\n  - details_join is details\
      \ joined as 'k=v' pairs in order with ';' separators\n"
    ```
- **clause.inputs.graph_id_uniqueness_across_group** (kind: clause)
  - label: graph_id uniqueness across DocGroup
  - Extra fields:
    ```yml
    label: graph_id uniqueness across DocGroup
    status: normative
    text: "Within a DocGroup, graph_id values SHOULD be unique. If duplicates exist:\n  - the\
      \ validator MUST emit at least one violation per duplicated graph_id, and\n  - the validator\
      \ MUST NOT arbitrarily choose one duplicate as canonical.\nDeterministic behavior rule:\
      \ graphs with duplicated graph_id MUST be validated for GF0 structural integrity, but MUST\
      \ be excluded from higher-level profile validation and excluded from cross-graph linking,\
      \ to avoid nondeterministic resolution.\n"
    ```
- **clause.inputs.graphrecord** (kind: clause)
  - label: GraphRecord input model
  - Extra fields:
    ```yml
    label: GraphRecord input model
    status: normative
    text: "A validator consumes a DocGroup expressed as a list of GraphRecords:\n  - graph: a\
      \ GF0 GraphFrameK0 value\n  - source_id: optional string (e.g. file path, URL, label)\n\
      source_id MUST NOT affect the canonical validation result.\n"
    ```
- **clause.inputs.meta_recursion** (kind: clause)
  - label: Meta recursion
  - Extra fields:
    ```yml
    label: Meta recursion
    status: normative
    text: 'Validation MUST recursively validate each MetaGraph using the same GF0 rules, subject
      to a maximum meta depth (see clause.determinism.limits). MetaGraphs MUST be treated as structurally
      independent; parent references, if any, are purely attribute/semantics level.

      '
    ```
- **clause.report.canonical_json** (kind: clause)
  - label: Canonical JSON serialization
  - Extra fields:
    ```yml
    label: Canonical JSON serialization
    status: normative
    text: "Canonical equivalence is defined by canonical JSON serialization of the report:\n \
      \ - UTF-8 encoding\n  - Object keys are sorted lexicographically (byte order of UTF-8)\n\
      \  - Arrays preserve their specified order\n  - No insignificant whitespace is permitted\n\
      \  - Newlines in strings MUST be '\\n' (LF)\nmessage fields, if present, MUST be excluded\
      \ from canonical serialization.\n"
    ```
- **clause.report.fingerprint** (kind: clause)
  - label: Fingerprint
  - Extra fields:
    ```yml
    label: Fingerprint
    status: informative
    text: 'Implementations MAY provide a ''fingerprint'' value computed as SHA-256 over the canonical
      JSON bytes as a convenience for fast equivalence checks.

      '
    ```
- **clause.report.location_model** (kind: clause)
  - label: Location model
  - Extra fields:
    ```yml
    label: Location model
    status: normative
    text: "A Location object MUST have:\n  - graph_id: string\n  - meta_path: ordered list of\
      \ string graph_ids from outermost graph to the graph where the violation occurred\nIt MAY\
      \ have:\n  - node_id: string\n  - edge_key: string (canonical edge key 'type|from|to|id',\
      \ with empty id allowed)\n"
    ```
- **clause.report.model** (kind: clause)
  - label: ValidationReportK1 model
  - Extra fields:
    ```yml
    label: ValidationReportK1 model
    status: normative
    text: "The validator produces a ValidationReportK1 object with fields:\n  - version: fixed\
      \ string 'validatorgroup-k1@0.1.0'\n  - ok: boolean\n  - violations: ordered list of Violation\
      \ objects\nok MUST be true iff violations contains no entries with severity == 'error'.\n"
    ```
- **clause.report.violation_model** (kind: clause)
  - label: Violation model
  - Extra fields:
    ```yml
    label: Violation model
    status: normative
    text: "A Violation object MUST have:\n  - severity: 'error' | 'warning'\n  - code: stable\
      \ string code (see section.6)\n  - stage: one of property.stage_enum.stage_values\n  - location:\
      \ Location object\n  - details: ordered list of {key,value} pairs (not a map)\nA Violation\
      \ MAY have:\n  - message: non-canonical human-readable string (MUST be ignored for canonical\
      \ equivalence)\n"
    ```
- **clause.scope.intent** (kind: clause)
  - label: Intent
  - Extra fields:
    ```yml
    label: Intent
    status: normative
    text: 'ValidatorGroup K1 exists to ensure that independent implementations validate the same
      DocGroup and produce identical canonical results, enabling deterministic CI, refactors,
      and generator pipelines.

      '
    ```
- **clause.scope.non_goals** (kind: clause)
  - label: Non-goals
  - Extra fields:
    ```yml
    label: Non-goals
    status: normative
    text: 'This spec does not mandate any particular programming language, IO mechanism, file
      layout, or CLI UX. It does not mandate performance characteristics beyond bounded recursion.

      '
    ```
- **clause.stages.definition** (kind: clause)
  - label: Stage definition
  - Extra fields:
    ```yml
    label: Stage definition
    status: normative
    text: 'Validation proceeds in the stage order specified by property.stage_order. Each stage
      MAY add violations. A stage MAY be skipped for a graph if prerequisites fail.

      '
    ```
- **clause.stages.gf0_struct** (kind: clause)
  - label: Stage: gf0_struct
  - Extra fields:
    ```yml
    label: 'Stage: gf0_struct'
    status: normative
    text: "gf0_struct performs structural validation of each graph (and recursively its MetaGraphs):\n\
      \  - required top-level fields are present and correctly typed;\n  - graph_id and version\
      \ are non-empty strings;\n  - NodeK0 IDs are unique within the frame;\n  - EdgeK0 endpoints\
      \ refer to existing NodeK0 IDs in the same frame.\nAny failure in gf0_struct MUST emit an\
      \ error severity violation for that graph.\n"
    ```
- **clause.stages.links** (kind: clause)
  - label: Stage: links
  - Extra fields:
    ```yml
    label: 'Stage: links'
    status: normative
    text: "links performs cross-graph checks using only graphs that passed gf0_struct and have\
      \ unique graph_id:\n  - For SpecFrames: every spec_ref.target_graph_id MUST exist as a graph_id\
      \ in the DocGroup.\n  - Additional link rules MAY be implemented, but MUST be deterministic\
      \ and MUST have stable codes.\nLinks stage MUST NOT attempt network fetch or external resolution\
      \ unless the caller explicitly provides those graphs in the DocGroup.\n"
    ```
- **clause.stages.profile_detect** (kind: clause)
  - label: Stage: profile_detect
  - Extra fields:
    ```yml
    label: 'Stage: profile_detect'
    status: normative
    text: "profile_detect deterministically identifies which higher-level validators apply to\
      \ a graph. Detection MUST be based only on the graph's own content (not filename or environment).\
      \ Minimum required detection rules:\n  - SpecFrameK1 applies if the graph contains exactly\
      \ one node with id==graph_id, kind=='spec',\n    and profile=='specframe-k1'.\n  - RenderFrameK1\
      \ applies if the graph contains exactly one node with id==graph_id,\n    kind=='render_plan',\
      \ and profile=='renderframe-k1'.\nIf a graph matches multiple profile rules, the validator\
      \ MUST emit an error and MUST NOT proceed to the conflicting profile validators.\n"
    ```
- **clause.stages.renderframe** (kind: clause)
  - label: Stage: renderframe_k1
  - Extra fields:
    ```yml
    label: 'Stage: renderframe_k1'
    status: normative
    text: "renderframe_k1 validates graphs detected as RenderFrames:\n  - allowed node kinds and\
      \ edge types for RenderFrameK1;\n  - exactly one render_plan root node with id==graph_id\
      \ and profile=='renderframe-k1';\n  - 'contains' edges form an acyclic tree rooted at the\
      \ render_plan node;\n  - rule edges and reference targets are well-typed (selects->selector,\
      \ emits->emitter, etc.).\n(RenderFrameK1's detailed rules are defined by spec://_kernel/render/renderframe-k1;\
      \ this stage MUST implement them when that spec is available in the DocGroup.)\n"
    ```
- **clause.stages.specframe** (kind: clause)
  - label: Stage: specframe_k1
  - Extra fields:
    ```yml
    label: 'Stage: specframe_k1'
    status: normative
    text: "specframe_k1 validates graphs detected as SpecFrames:\n  - NodeK0.kind is within the\
      \ allowed SpecFrame kinds set;\n  - EdgeK0.type is within the allowed SpecFrame edge types\
      \ set;\n  - 'contains' edges form an acyclic tree (or forest) rooted at the spec node;\n\
      \  - required attributes per node kind are present.\nMissing required attributes MUST be\
      \ treated as errors.\n"
    ```
- **example.group_dedup_behavior** (kind: example)
  - label: Duplicate graph_id behavior
  - Extra fields:
    ```yml
    label: Duplicate graph_id behavior
    status: informative
    text: "If two GraphRecords share graph_id=\"spec.dup\", the validator MUST:\n  - emit an error\
      \ violation for the duplicated graph_id, and\n  - run gf0_struct on both,\n  - skip specframe/renderframe/links\
      \ stages for graph_id=\"spec.dup\".\n"
    ```
- **example.minimal_report** (kind: example)
  - label: Minimal ValidationReportK1
  - Extra fields:
    ```yml
    label: Minimal ValidationReportK1
    status: informative
    text: "version: \"validatorgroup-k1@0.1.0\"\nok: false\nviolations:\n  - severity: \"error\"\
      \n    code: \"GF0.E.BAD_EDGE_ENDPOINT\"\n    stage: \"gf0_struct\"\n    location:\n    \
      \  graph_id: \"spec.some-doc\"\n      meta_path: [\"spec.some-doc\"]\n      edge_key: \"\
      contains|spec.some-doc|section.1.scope|\"\n    details:\n      - { key: \"missing_endpoint\"\
      , value: \"to\" }\n      - { key: \"missing_node_id\", value: \"section.1.scope\" }\n"
    ```
- **property.details_kv** (kind: property)
  - label: Details are ordered KV pairs
  - Extra fields:
    ```yml
    details_shape: 'details MUST be an ordered list of {key,value} pairs (not a map), with stable
      ordering.

      '
    label: Details are ordered KV pairs
    status: normative
    ```
- **property.location_fields** (kind: property)
  - label: Location fields
  - Extra fields:
    ```yml
    fields:
    - graph_id
    - meta_path
    - node_id
    - edge_key
    label: Location fields
    status: normative
    ```
- **property.report_fields** (kind: property)
  - label: Required report fields
  - Extra fields:
    ```yml
    label: Required report fields
    required_fields:
    - version
    - ok
    - violations
    status: normative
    ```
- **property.required_codes** (kind: property)
  - label: Required violation codes
  - Extra fields:
    ```yml
    codes:
    - GF0.E.MISSING_FIELD
    - GF0.E.EMPTY_GRAPH_ID_OR_VERSION
    - GF0.E.DUP_NODE_ID
    - GF0.E.BAD_EDGE_ENDPOINT
    - GF0.E.META_DEPTH_EXCEEDED
    - GF0.E.GRAPH_TOO_LARGE
    - PROF.E.MULTIPLE_PROFILE_MATCH
    - PROF.E.BAD_ROOT_NODE
    - SPEC.E.BAD_NODE_KIND
    - SPEC.E.BAD_EDGE_TYPE
    - SPEC.E.CONTAINS_CYCLE_OR_MULTIPARENT
    - SPEC.E.MISSING_REQUIRED_ATTR
    - LINK.E.MISSING_TARGET_GRAPH
    - LINK.W.UNREACHABLE_NORMATIVE
    label: Required violation codes
    status: normative
    ```
- **property.severity_enum** (kind: property)
  - label: Severity enum
  - Extra fields:
    ```yml
    label: Severity enum
    severity_values:
    - error
    - warning
    status: normative
    ```
- **property.stage_enum** (kind: property)
  - label: Stage enum
  - Extra fields:
    ```yml
    label: Stage enum
    stage_values:
    - gf0_struct
    - profile_detect
    - specframe_k1
    - renderframe_k1
    - links
    status: normative
    ```
- **property.stage_order** (kind: property)
  - label: Stage evaluation order
  - Extra fields:
    ```yml
    label: Stage evaluation order
    stage_order:
    - gf0_struct
    - profile_detect
    - specframe_k1
    - renderframe_k1
    - links
    status: normative
    ```
- **property.violation_fields** (kind: property)
  - label: Required violation fields
  - Extra fields:
    ```yml
    label: Required violation fields
    required_fields:
    - severity
    - code
    - stage
    - location
    - details
    status: normative
    ```
- **ref.spec.gf0-k1** (kind: spec_ref)
  - label: GraphFrame K0 schema
  - Extra fields:
    ```yml
    label: GraphFrame K0 schema
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    ```
- **ref.spec.renderframe-k1** (kind: spec_ref)
  - label: RenderFrame K1 schema
  - Extra fields:
    ```yml
    label: RenderFrame K1 schema
    status: informative
    target_graph_id: spec://_kernel/render/renderframe-k1
    ```
- **ref.spec.specframe-k1** (kind: spec_ref)
  - label: SpecFrame K1 schema
  - Extra fields:
    ```yml
    label: SpecFrame K1 schema
    status: informative
    target_graph_id: spec://_kernel/spec/specframe-k1
    ```
- **section.1.scope** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Scope and Intent
    ```
- **section.2.inputs** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Inputs and Canonicalization
    ```
- **section.3.stages** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Validation Stages
    ```
- **section.4.determinism** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: Determinism and Ordering
    ```
- **section.5.report** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: Validation Report Model
    ```
- **section.6.codes** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: normative
    title: Required Violation Codes
    ```
- **section.7.examples** (kind: section)
  - Extra fields:
    ```yml
    order: 7
    status: informative
    title: Examples
    ```
- **section.8.integration** (kind: section)
  - Extra fields:
    ```yml
    order: 8
    status: informative
    title: Integration Notes
    ```
- **spec://_kernel/validator/validatorgroup-k1** (kind: spec)
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'ValidatorGroup K1 defines a deterministic validation contract for a group of GF0
      graphs. It specifies (a) validation stages from GF0 up through higher-level profiles, (b)
      a canonical violation model, and (c) canonical ordering/serialization rules so that independent
      implementations (Python, Go, etc.) produce identical results.

      '
    title: ValidatorGroup K1 — Deterministic Doc-Group Validation
    ```
- **term.canonical_equivalence** (kind: term)
  - label: CanonicalEquivalence
  - Extra fields:
    ```yml
    label: CanonicalEquivalence
    status: normative
    text: 'Two ValidationReports are canonically equivalent if their canonical serialization bytes
      are identical (see clause.report.canonical_json).

      '
    ```
- **term.doc_group** (kind: term)
  - label: DocGroup
  - Extra fields:
    ```yml
    label: DocGroup
    status: normative
    text: 'A DocGroup is an unordered set of GF0 graphs validated together to enable cross-graph
      checks (e.g., referenced spec existence, shared profiles, render plans).

      '
    ```
- **term.graph_record** (kind: term)
  - label: GraphRecord
  - Extra fields:
    ```yml
    label: GraphRecord
    status: normative
    text: 'A GraphRecord is a GF0 graph plus optional source metadata. Source metadata MUST NOT
      affect validation semantics or canonical outputs, except where explicitly stated.

      '
    ```
- **term.location** (kind: term)
  - label: Location
  - Extra fields:
    ```yml
    label: Location
    status: normative
    text: 'A structured pointer identifying where a violation occurred: graph_id plus optional
      node_id, edge_key, and meta_path.

      '
    ```
- **term.profile_detection** (kind: term)
  - label: ProfileDetection
  - Extra fields:
    ```yml
    label: ProfileDetection
    status: normative
    text: 'The deterministic process of deciding which higher-level validators apply to a graph,
      based on its root node and attributes.

      '
    ```
- **term.validation_stage** (kind: term)
  - label: ValidationStage
  - Extra fields:
    ```yml
    label: ValidationStage
    status: normative
    text: 'A named stage of validation. Stages are evaluated in deterministic order and MAY be
      skipped for a graph if prerequisite stages failed.

      '
    ```
- **term.violation** (kind: term)
  - label: Violation
  - Extra fields:
    ```yml
    label: Violation
    status: normative
    text: 'A structured, canonical report entry describing a validation failure or warning at
      a specific stage. A violation is identified by (code, stage, location, details).

      '
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.scope | clause.scope.intent | contains |  |  |  |
| section.1.scope | clause.scope.non_goals | contains |  |  |  |
| section.1.scope | term.canonical_equivalence | contains |  |  |  |
| section.1.scope | term.doc_group | contains |  |  |  |
| section.1.scope | term.graph_record | contains |  |  |  |
| section.1.scope | term.location | contains |  |  |  |
| section.1.scope | term.profile_detection | contains |  |  |  |
| section.1.scope | term.validation_stage | contains |  |  |  |
| section.1.scope | term.violation | contains |  |  |  |
| section.2.inputs | clause.inputs.graph_id_uniqueness_across_group | contains |  |  |  |
| section.2.inputs | clause.inputs.graphrecord | contains |  |  |  |
| section.2.inputs | clause.inputs.meta_recursion | contains |  |  |  |
| section.3.stages | clause.stages.definition | contains |  |  |  |
| section.3.stages | clause.stages.gf0_struct | contains |  |  |  |
| section.3.stages | clause.stages.links | contains |  |  |  |
| section.3.stages | clause.stages.profile_detect | contains |  |  |  |
| section.3.stages | clause.stages.renderframe | contains |  |  |  |
| section.3.stages | clause.stages.specframe | contains |  |  |  |
| section.3.stages | property.stage_enum | contains |  |  |  |
| section.3.stages | property.stage_order | contains |  |  |  |
| section.4.determinism | clause.determinism.details_order | contains |  |  |  |
| section.4.determinism | clause.determinism.limits | contains |  |  |  |
| section.4.determinism | clause.determinism.sorting | contains |  |  |  |
| section.4.determinism | clause.determinism.violation_order | contains |  |  |  |
| section.4.determinism | property.details_kv | contains |  |  |  |
| section.5.report | clause.report.canonical_json | contains |  |  |  |
| section.5.report | clause.report.fingerprint | contains |  |  |  |
| section.5.report | clause.report.location_model | contains |  |  |  |
| section.5.report | clause.report.model | contains |  |  |  |
| section.5.report | clause.report.violation_model | contains |  |  |  |
| section.5.report | property.location_fields | contains |  |  |  |
| section.5.report | property.report_fields | contains |  |  |  |
| section.5.report | property.severity_enum | contains |  |  |  |
| section.5.report | property.violation_fields | contains |  |  |  |
| section.6.codes | clause.codes.gf0_bad_edge | contains |  |  |  |
| section.6.codes | clause.codes.gf0_dup_node | contains |  |  |  |
| section.6.codes | clause.codes.gf0_empty_id_ver | contains |  |  |  |
| section.6.codes | clause.codes.gf0_missing_field | contains |  |  |  |
| section.6.codes | clause.codes.link_missing_target_graph | contains |  |  |  |
| section.6.codes | clause.codes.link_unreachable_normative | contains |  |  |  |
| section.6.codes | clause.codes.requirement | contains |  |  |  |
| section.6.codes | clause.codes.spec_bad_edge_type | contains |  |  |  |
| section.6.codes | clause.codes.spec_bad_kind | contains |  |  |  |
| section.6.codes | clause.codes.spec_contains_cycle | contains |  |  |  |
| section.6.codes | clause.codes.spec_missing_attr | contains |  |  |  |
| section.6.codes | property.required_codes | contains |  |  |  |
| section.7.examples | example.group_dedup_behavior | contains |  |  |  |
| section.7.examples | example.minimal_report | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | ref.spec.gf0-k1 | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | ref.spec.renderframe-k1 | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | ref.spec.specframe-k1 | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.1.scope | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.2.inputs | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.3.stages | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.4.determinism | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.5.report | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.6.codes | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.7.examples | contains |  |  |  |
| spec://_kernel/validator/validatorgroup-k1 | section.8.integration | contains |  |  |  |

## Contains Tree
- spec://_kernel/validator/validatorgroup-k1
  - ref.spec.gf0-k1
  - ref.spec.renderframe-k1
  - ref.spec.specframe-k1
  - section.1.scope
    - clause.scope.intent
    - clause.scope.non_goals
    - term.canonical_equivalence
    - term.doc_group
    - term.graph_record
    - term.location
    - term.profile_detection
    - term.validation_stage
    - term.violation
  - section.2.inputs
    - clause.inputs.graph_id_uniqueness_across_group
    - clause.inputs.graphrecord
    - clause.inputs.meta_recursion
  - section.3.stages
    - clause.stages.definition
    - clause.stages.gf0_struct
    - clause.stages.links
    - clause.stages.profile_detect
    - clause.stages.renderframe
    - clause.stages.specframe
    - property.stage_enum
    - property.stage_order
  - section.4.determinism
    - clause.determinism.details_order
    - clause.determinism.limits
    - clause.determinism.sorting
    - clause.determinism.violation_order
    - property.details_kv
  - section.5.report
    - clause.report.canonical_json
    - clause.report.fingerprint
    - clause.report.location_model
    - clause.report.model
    - clause.report.violation_model
    - property.location_fields
    - property.report_fields
    - property.severity_enum
    - property.violation_fields
  - section.6.codes
    - clause.codes.gf0_bad_edge
    - clause.codes.gf0_dup_node
    - clause.codes.gf0_empty_id_ver
    - clause.codes.gf0_missing_field
    - clause.codes.link_missing_target_graph
    - clause.codes.link_unreachable_normative
    - clause.codes.requirement
    - clause.codes.spec_bad_edge_type
    - clause.codes.spec_bad_kind
    - clause.codes.spec_contains_cycle
    - clause.codes.spec_missing_attr
    - property.required_codes
  - section.7.examples
    - example.group_dedup_behavior
    - example.minimal_report
  - section.8.integration
