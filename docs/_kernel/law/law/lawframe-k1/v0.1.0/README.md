# law://_kernel/law/lawframe-k1
- version: 0.1.0
- nodes: 23
- edges: 23
- meta: 0
## Nodes
- **def.lawdoc** (kind: definition)
  - label: LawDoc
  - Extra fields:
    ```yml
    label: LawDoc
    text: A GF0 graph whose root node has id==graph_id, kind='law', profile='lawframe-k1'.
    ```
- **def.lawprofile** (kind: definition)
  - label: LawProfile
  - Extra fields:
    ```yml
    label: LawProfile
    text: A GF0 graph whose root node has id==graph_id, kind='law_profile', profile='lawprofile-k1'.
    ```
- **def.location** (kind: definition)
  - label: Location
  - Extra fields:
    ```yml
    label: Location
    text: 'A pointer into a law graph: graph_id, optional node_id, optional edge_key, optional
      meta_path.'
    ```
- **def.modal** (kind: definition)
  - label: Modal
  - Extra fields:
    ```yml
    label: Modal
    text: 'A fixed enum controlling normative force: MUST, MUST_NOT, SHOULD, SHOULD_NOT, MAY.'
    ```
- **def.rule** (kind: definition)
  - label: Rule
  - Extra fields:
    ```yml
    label: Rule
    text: A normative statement with a modal (MUST/MUST_NOT/SHOULD/SHOULD_NOT/MAY) and text.
    ```
- **law://_kernel/law/lawframe-k1** (kind: law)
  - Extra fields:
    ```yml
    law_id: lawframe-k1
    law_version: 0.1.0
    profile: lawframe-k1
    status: normative
    summary: Defines a GF0 profile for expressing laws, policies, and governance as graphs.
    title: LawFrame K1 — Generic Law Graph Profile over GF0
    ```
- **prop.allowed_edge_types** (kind: property)
  - label: Allowed edge types
  - Extra fields:
    ```yml
    label: Allowed edge types
    values:
    - contains
    - defines
    - refers_to
    - applies_to
    - exception_of
    - supersedes
    - amends
    - enables
    - disables
    ```
- **prop.allowed_node_kinds** (kind: property)
  - label: Allowed node kinds
  - Extra fields:
    ```yml
    label: Allowed node kinds
    values:
    - law
    - title
    - section
    - definition
    - rule
    - exception
    - parameter
    - reference
    - example
    ```
- **prop.modal_enum** (kind: property)
  - label: Modal enum
  - Extra fields:
    ```yml
    label: Modal enum
    values:
    - MUST
    - MUST_NOT
    - SHOULD
    - SHOULD_NOT
    - MAY
    ```
- **rule.contains_tree** (kind: rule)
  - label: Structural containment
  - Extra fields:
    ```yml
    label: Structural containment
    modal: MUST
    text: '''contains'' edges MUST be acyclic and define the primary structural tree rooted at
      the law root. Multiple ''contains'' parents for the same node are forbidden.

      '
    ```
- **rule.deterministic_order** (kind: rule)
  - label: Deterministic ordering
  - Extra fields:
    ```yml
    label: Deterministic ordering
    modal: MUST
    text: 'Where ordering is required, implementations MUST order by explicit integer ''order''
      if present; otherwise by lexicographic ordering of node IDs; otherwise by lexicographic
      ordering of edge keys.

      '
    ```
- **rule.edge_restriction** (kind: rule)
  - label: Edge type restriction
  - Extra fields:
    ```yml
    label: Edge type restriction
    modal: MUST
    text: 'Edge types within a LawDoc MUST be limited to prop.allowed_edge_types unless an extension
      mechanism is explicitly invoked (see rule.extensions).

      '
    ```
- **rule.extensions** (kind: rule)
  - label: Extension mechanism
  - Extra fields:
    ```yml
    label: Extension mechanism
    modal: MAY
    text: 'Extensions MAY introduce additional node kinds and edge types if the LawDoc includes
      an explicit extension declaration node with kind==''parameter'' and key==''extensions''
      listing allowed additions.

      '
    ```
- **rule.gf0_conformance** (kind: rule)
  - label: GF0 conformance
  - Extra fields:
    ```yml
    label: GF0 conformance
    modal: MUST
    text: 'Every LawDoc MUST be a valid GraphFrameK0: fields {graph_id, version, attrs, nodes,
      edges, meta} MUST be present and empty lists encoded as [].

      '
    ```
- **rule.kind_restriction** (kind: rule)
  - label: Node kind restriction
  - Extra fields:
    ```yml
    label: Node kind restriction
    modal: MUST
    text: 'Node kinds within a LawDoc MUST be limited to prop.allowed_node_kinds unless an extension
      mechanism is explicitly invoked (see rule.extensions).

      '
    ```
- **rule.meta_usage** (kind: rule)
  - label: Meta usage
  - Extra fields:
    ```yml
    label: Meta usage
    modal: SHOULD
    text: 'Non-authoritative overlays (commentary, provenance, index, CI receipts) SHOULD be carried
      in GF0 meta as MetaGraphs, which are structurally independent from the parent graph.

      '
    ```
- **rule.root_shape** (kind: rule)
  - label: Root law node
  - Extra fields:
    ```yml
    label: Root law node
    modal: MUST
    text: 'A LawDoc MUST contain exactly one root node where id==graph_id, kind==''law'', profile==''lawframe-k1''.

      '
    ```
- **rule.rule_fields** (kind: rule)
  - label: Rule required fields
  - Extra fields:
    ```yml
    label: Rule required fields
    modal: MUST
    text: 'A node with kind==''rule'' MUST have: label (string), modal (Modal), text (string).
      It MAY have: scope, applies_to, params, and references.

      '
    ```
- **rule.supersession** (kind: rule)
  - label: Supersession is explicit
  - Extra fields:
    ```yml
    label: Supersession is explicit
    modal: MUST
    text: 'Supersession MUST be expressed explicitly via ''supersedes'' edges (or ''amends'' for
      partial changes). Implicit supersession by timestamps or filenames is forbidden.

      '
    ```
- **section.1.charter** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    title: Charter
    ```
- **section.2.model** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    title: Model
    ```
- **section.3.invariants** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    title: Invariants
    ```
- **title.0** (kind: title)
  - Extra fields:
    ```yml
    text: LawFrame K1
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| law://_kernel/law/lawframe-k1 | section.1.charter | contains |  |  |  |
| law://_kernel/law/lawframe-k1 | section.2.model | contains |  |  |  |
| law://_kernel/law/lawframe-k1 | section.3.invariants | contains |  |  |  |
| law://_kernel/law/lawframe-k1 | title.0 | contains |  |  |  |
| rule.root_shape | def.lawdoc | refers_to |  |  |  |
| rule.rule_fields | def.rule | refers_to |  |  |  |
| section.2.model | def.lawdoc | contains |  |  |  |
| section.2.model | def.lawprofile | contains |  |  |  |
| section.2.model | def.modal | contains |  |  |  |
| section.2.model | def.rule | contains |  |  |  |
| section.2.model | prop.allowed_edge_types | contains |  |  |  |
| section.2.model | prop.allowed_node_kinds | contains |  |  |  |
| section.2.model | prop.modal_enum | contains |  |  |  |
| section.3.invariants | rule.contains_tree | contains |  |  |  |
| section.3.invariants | rule.deterministic_order | contains |  |  |  |
| section.3.invariants | rule.edge_restriction | contains |  |  |  |
| section.3.invariants | rule.extensions | contains |  |  |  |
| section.3.invariants | rule.gf0_conformance | contains |  |  |  |
| section.3.invariants | rule.kind_restriction | contains |  |  |  |
| section.3.invariants | rule.meta_usage | contains |  |  |  |
| section.3.invariants | rule.root_shape | contains |  |  |  |
| section.3.invariants | rule.rule_fields | contains |  |  |  |
| section.3.invariants | rule.supersession | contains |  |  |  |

## Contains Tree
- law://_kernel/law/lawframe-k1
  - section.1.charter
  - section.2.model
    - def.lawdoc
    - def.lawprofile
    - def.modal
    - def.rule
    - prop.allowed_edge_types
    - prop.allowed_node_kinds
    - prop.modal_enum
  - section.3.invariants
    - rule.contains_tree
    - rule.deterministic_order
    - rule.edge_restriction
    - rule.extensions
    - rule.gf0_conformance
    - rule.kind_restriction
    - rule.meta_usage
    - rule.root_shape
    - rule.rule_fields
    - rule.supersession
  - title.0
