# spec://_kernel/render/renderframe-k1
- version: 0.1.0
- nodes: 45
- edges: 44
- meta: 0
## Nodes
- **clause.attrs.emitter** (kind: clause)
  - label: Attributes for emitter nodes
  - Extra fields:
    ```yml
    label: Attributes for emitter nodes
    status: normative
    text: "A node with kind=='emitter' MUST provide:\n  - label  : short emitter name,\n  - status\
      \ : RenderStatus.\nIt SHOULD provide:\n  - template_id : node id of a template node in the\
      \ same RenderFrame.\nIt MAY provide:\n  - pipeline : ordered list of transform node ids\
      \ to apply to the emitted text.\n"
    എന്ത
- **clause.attrs.plan** (kind: clause)
  - label: Attributes for render_plan nodes
  - Extra fields:
    ```yml
    label: Attributes for render_plan nodes
    status: normative
    text: "A node with kind=='render_plan' MUST provide:\n  - title   : short plan title,\n  -\
      \ status  : RenderStatus,\n  - summary : short description,\n  - profile : 'renderframe-k1'.\n\
      It MAY also provide:\n  - format_hint : string tag (e.g. 'markdown', 'latex', 'text'),\n\
      \  - applies_to_doc_profile : string tag used by tooling,\n  - on_missing_field : 'empty'\
      \ | 'error' (default: 'empty').\n"
    എന്ത
- **clause.attrs.product** (kind: clause)
  - label: Attributes for render_product nodes
  - Extra fields:
    ```yml
    label: Attributes for render_product nodes
    status: normative
    text: "A node with kind=='render_product' MUST provide:\n  - label  : short product name,\n\
      \  - status : RenderStatus.\nIt MAY provide:\n  - output_kind : 'file' | 'string' (default:\
      \ 'string'),\n  - output_path : string (required if output_kind=='file'),\n  - source_root_id\
      \ : string (parent graph node id) selecting a render root,\n  - resolution_mode : 'first_match'\
      \ | 'merge' (default: 'first_match').\n"
    എന്ത
- **clause.attrs.required** (kind: clause)
  - label: Required attributes per node kind
  - Extra fields:
    ```yml
    label: Required attributes per node kind
    status: normative
    text: "A RenderFrame validator MUST treat missing required attributes as a hard validation\
      \ error. Required attributes per kind are:\n  - render_plan    : title, status, summary,\
      \ profile\n  - render_product : label, status\n  - render_rule    : label, status\n  - selector\
      \       : label, status\n  - emitter        : label, status\n  - template       : label,\
      \ status, body\n  - transform      : label, status, op\n"
    എന്ത
- **clause.attrs.selector** (kind: clause)
  - label: Attributes for selector nodes
  - Extra fields:
    ```yml
    label: Attributes for selector nodes
    status: normative
    text: "A node with kind=='selector' MUST provide:\n  - label  : short selector name,\n  -\
      \ status : RenderStatus.\nIt SHOULD provide:\n  - predicates : ordered list of RenderPredicate\
      \ strings.\nSelector predicate syntax is implementation-defined but MUST be deterministic.\n"
    എന്ത
- **clause.attrs.template** (kind: clause)
  - label: Attributes for template nodes
  - Extra fields:
    ```yml
    label: Attributes for template nodes
    status: normative
    text: "A node with kind=='template' MUST provide:\n  - label  : short template name,\n  -\
      \ status : RenderStatus,\n  - body   : template text.\nTemplates MAY contain placeholders.\
      \ Placeholder syntax is implementation-defined, but MUST be deterministic and MUST define\
      \ behavior for missing fields (see render_plan.on_missing_field).\n"
    എന്ത
- **clause.attrs.transform** (kind: clause)
  - label: Attributes for transform nodes
  - Extra fields:
    ```yml
    label: Attributes for transform nodes
    status: normative
    text: "A node with kind=='transform' MUST provide:\n  - label  : short transform name,\n \
      \ - status : RenderStatus,\n  - op     : string naming a pure text transform operation.\n\
      It MAY provide:\n  - args : ordered list of string args (interpretation is op-specific).\n"
    എന്ത
- **clause.edge_types.allowed** (kind: clause)
  - label: Allowed edge types
  - Extra fields:
    ```yml
    label: Allowed edge types
    status: normative
    text: 'Within a RenderFrame, EdgeK0.type MUST be one of the values in property.renderframe.edge_types.
      Unknown edge types MUST be treated as hard validation failures.

      '
    എന്ത
- **clause.integration.attach** (kind: clause)
  - label: Attaching RenderFrames
  - Extra fields:
    ```yml
    label: Attaching RenderFrames
    status: informative
    text: 'RenderFrames SHOULD be attached to a source graph via GF0.meta (as a MetaGraph). Implementations
      MAY also store RenderFrames as standalone GF0 files and attach them at build time.

      '
    എന്ത
- **clause.integration.precedence** (kind: clause)
  - label: Precedence and overrides
  - Extra fields:
    ```yml
    label: Precedence and overrides
    status: informative
    text: 'If multiple RenderFrames apply, precedence SHOULD be deterministic: later MetaGraphs
      in the source graph''s meta list win, or explicit ''overrides'' edges define precedence.
      If both exist, explicit overrides SHOULD take precedence.

      '
    എന്ത
- **clause.model.definition** (kind: clause)
  - label: Definition
  - Extra fields:
    ```yml
    label: Definition
    status: normative
    text: "A RenderFrame is any GF0 graph that satisfies:\n  (1) It is a valid GraphFrameK0 (graph_id/version/attrs/nodes/edges/meta\
      \ present in canonical form);\n  (2) It contains exactly one root node with id==graph_id,\
      \ kind=='render_plan';\n  (3) That root node has profile=='renderframe-k1'.\n"
    എന്ത
- **clause.model.determinism** (kind: clause)
  - label: Determinism
  - Extra fields:
    ```yml
    label: Determinism
    status: normative
    text: 'For the same canonical source graph + the same canonical RenderFrame, an implementation
      MUST produce identical text outputs. Where ordering is required, it MUST be derived from
      explicit integer ''order'' attributes when present, otherwise from stable lexical ordering
      of node IDs.

      '
    എന്ത
- **clause.model.rule_resolution** (kind: clause)
  - label: Rule resolution
  - Extra fields:
    ```yml
    label: Rule resolution
    status: normative
    text: 'Within a RenderProduct, rules are evaluated in deterministic order. For a given source
      node, the first matching rule (by rule order) MUST be applied unless the product declares
      a different explicit resolution mode (e.g. ''merge'').

      '
    എന്ത
- **clause.model.scoping** (kind: clause)
  - label: Scoping into parent graphs
  - Extra fields:
    ```yml
    label: Scoping into parent graphs
    status: normative
    text: 'RenderFrames are structurally independent from their parent graphs. Any references
      from a RenderFrame into the source graph MUST be expressed via attributes (e.g. parent_graph_id,
      parent_node_id, source_root_id) or via explicit edge types with documented semantics.

      '
    എന്ത
- **clause.node_kinds.allowed** (kind: clause)
  - label: Allowed node kinds
  - Extra fields:
    ```yml
    label: Allowed node kinds
    status: normative
    text: 'Within a RenderFrame, NodeK0.kind MUST be one of the values in property.renderframe.node_kinds.
      Unknown or misspelled kinds MUST be treated as hard validation failures.

      '
    എന്ത
- **clause.overview.intent** (kind: clause)
  - label: Intent
  - Extra fields:
    ```yml
    label: Intent
    status: normative
    text: 'RenderFrame K1 specifies a portable, deterministic plan for rendering graphs into text.
      The plan MAY tag outputs with a ''format'' string (e.g. ''markdown'', ''latex''), but the
      core semantics are purely text-based.

      '
    എന്ത
- **clause.overview.meta_usage** (kind: clause)
  - label: RenderFrames are MetaGraphs
  - Extra fields:
    ```yml
    label: RenderFrames are MetaGraphs
    status: normative
    text: 'A RenderFrame is intended to be carried as a GF0 MetaGraph under the ''meta'' list
      of a source graph. This follows GF0''s intent for meta: attach auxiliary views, layouts,
      and indexes without changing the primary frame.

      '
    എന്ത
- **clause.validation.contains_tree** (kind: clause)
  - label: Contains edges form a tree
  - Extra fields:
    ```yml
    label: Contains edges form a tree
    status: normative
    text: '''contains'' edges in a RenderFrame MUST form an acyclic tree (or forest) rooted at
      the render_plan node. Cycles or multiple parents via ''contains'' are hard validation failures.

      '
    എന്ത
- **clause.validation.edge_integrity** (kind: clause)
  - label: Edge integrity
  - Extra fields:
    ```yml
    label: Edge integrity
    status: normative
    text: 'All edges MUST reference existing node IDs (EdgeK0.from/to integrity). Missing endpoints
      are hard validation failures.

      '
    എന്ത
- **clause.validation.reference_targets** (kind: clause)
  - label: Reference targets
  - Extra fields:
    ```yml
    label: Reference targets
    status: normative
    text: 'For every ''selects'' edge, the destination node MUST have kind==''selector''. For
      every ''emits'' edge, the destination node MUST have kind==''emitter''. For every emitter.template_id,
      the referenced node MUST exist and have kind==''template''. For every transform listed in
      an emitter pipeline, the referenced node MUST exist and have kind==''transform''.

      '
    എന്ത
- **clause.validation.root** (kind: clause)
  - label: Root plan node
  - Extra fields:
    ```yml
    label: Root plan node
    status: normative
    text: "Each RenderFrame MUST contain exactly one node with:\n  - id == graph_id,\n  - kind\
      \ == 'render_plan',\n  - profile == 'renderframe-k1'.\n"
    എന്ത
- **example.minimal_renderframe** (kind: example)
  - label: minimal_renderframe
  - Extra fields:
    ```yml
    label: minimal_renderframe
    status: informative
    text: "Minimal RenderFrame instance (as a MetaGraph):\n  graph_id: \"doc.my_spec::render::text\"\
      \n  version: \"0.1.0\"\n  attrs: []\n  nodes:\n    - id: \"doc.my_spec::render::text\"\n\
      \      kind: \"render_plan\"\n      profile: \"renderframe-k1\"\n      status: \"normative\"\
      \n      title: \"Default text render\"\n      summary: \"Renders each node via a kind->template\
      \ rule set.\"\n    - id: \"product.main\"\n      kind: \"render_product\"\n      status:\
      \ \"normative\"\n      label: \"main\"\n      output_kind: \"string\"\n    - id: \"sel.any\"\
      \n      kind: \"selector\"\n      status: \"normative\"\n      label: \"any\"\n      predicates:\
      \ [\"node.kind != ''\"]\n    - id: \"tpl.default\"\n      kind: \"template\"\n      status:\
      \ \"normative\"\n      label: \"default\"\n      body: \"[{{node.kind}}] {{node.id}}\"\n\
      \    - id: \"emit.default\"\n      kind: \"emitter\"\n      status: \"normative\"\n    \
      \  label: \"default\"\n      template_id: \"tpl.default\"\n    - id: \"rule.any\"\n    \
      \  kind: \"render_rule\"\n      status: \"normative\"\n      label: \"any\"\n      order:\
      \ 1\n  edges:\n    - { from: \"doc.my_spec::render::text\", to: \"product.main\", type:\
      \ \"contains\" }\n    - { from: \"doc.my_spec::render::text\", to: \"sel.any\", type: \"\
      contains\" }\n    - { from: \"doc.my_spec::render::text\", to: \"tpl.default\", type: \"\
      contains\" }\n    - { from: \"doc.my_spec::render::text\", to: \"emit.default\", type: \"\
      contains\" }\n    - { from: \"product.main\", to: \"rule.any\", type: \"contains\" }\n \
      \   - { from: \"rule.any\", to: \"sel.any\", type: \"selects\" }\n    - { from: \"rule.any\"\
      , to: \"emit.default\", type: \"emits\" }\n  meta: []\n"
    എന്ത
- **property.renderframe.edge_types** (kind: property)
  - label: Allowed RenderFrame edge types
  - Extra fields:
    ```yml
    edge_types:
    - contains
    - selects
    - emits
    - uses
    - extends
    - overrides
    label: Allowed RenderFrame edge types
    status: normative
    എന്ത
- **property.renderframe.node_kinds** (kind: property)
  - label: Allowed RenderFrame node kinds
  - Extra fields:
    ```yml
    label: Allowed RenderFrame node kinds
    node_kinds:
    - render_plan
    - render_product
    - render_rule
    - selector
    - emitter
    - template
    - transform
    status: normative
    എന്ത
- **property.renderframe.status_enum** (kind: property)
  - label: RenderStatus enum
  - Extra fields:
    ```yml
    label: RenderStatus enum
    status: normative
    status_values:
    - normative
    - informative
    - experimental
    എന്ത
- **ref.spec.gf0-k1** (kind: spec_ref)
  - label: GraphFrame K0 (GF0)
  - Extra fields:
    ```yml
    label: GraphFrame K0 (GF0)
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    എന്ത
- **ref.spec.specframe-k1** (kind: spec_ref)
  - label: SpecFrame K1
  - Extra fields:
    ```yml
    label: SpecFrame K1
    status: informative
    target_graph_id: spec://_kernel/spec/specframe-k1
    എന്ത
- **section.1.overview** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Overview
    എന്ത
- **section.2.model** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Model
    എന്ത
- **section.3.node_kinds** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: RenderFrame Node Kinds
    എന്ത
- **section.4.edge_types** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: RenderFrame Edge Types
    എന്ത
- **section.5.attributes** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: Required Attributes
    എന്ത
- **section.6.validation** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: normative
    title: Validation Invariants
    എന്ത
- **section.7.integration** (kind: section)
  - Extra fields:
    ```yml
    order: 7
    status: informative
    title: Integration and Usage
    എന്ത
- **section.8.examples** (kind: section)
  - Extra fields:
    ```yml
    order: 8
    status: informative
    title: Examples
    എന്ത
- **spec://_kernel/render/renderframe-k1** (kind: spec)
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'RenderFrame K1 defines a GF0 MetaGraph profile for describing deterministic rendering
      of a source graph into text. The output may later be interpreted as Markdown, LaTeX, or
      any other text format; RenderFrame itself is format-agnostic.

      '
    title: RenderFrame K1 — Text Rendering Plan MetaGraph Profile
    എന്ത
- **term.emitter** (kind: term)
  - label: Emitter
  - Extra fields:
    ```yml
    label: Emitter
    status: normative
    text: 'An emitter produces text by applying a template and optional transforms.

      '
    എന്ത
- **term.render_plan** (kind: term)
  - label: RenderPlan
  - Extra fields:
    ```yml
    label: RenderPlan
    status: normative
    text: 'The root node of a RenderFrame. A plan declares selection scope, rule resolution, and
      one or more render products.

      '
    എന്ത
- **term.render_predicate** (kind: term)
  - label: RenderPredicate
  - Extra fields:
    ```yml
    label: RenderPredicate
    status: normative
    text: 'A single match condition inside a selector, expressed as a short string DSL or a structured
      list (implementation-defined, but must be deterministic).

      '
    എന്ത
- **term.render_product** (kind: term)
  - label: RenderProduct
  - Extra fields:
    ```yml
    label: RenderProduct
    status: normative
    text: 'A named output unit produced by a plan (e.g. one file, one string, one stream). Products
      are made of ordered rules.

      '
    എന്ത
- **term.render_rule** (kind: term)
  - label: RenderRule
  - Extra fields:
    ```yml
    label: RenderRule
    status: normative
    text: 'A rule binds a selector to an emitter. During traversal, applicable rules determine
      how a source node is rendered to text.

      '
    എന്ത
- **term.renderframe_k1** (kind: term)
  - label: RenderFrameK1
  - Extra fields:
    ```yml
    label: RenderFrameK1
    status: normative
    text: 'A RenderFrame is a GF0 graph intended to live as a MetaGraph under a source graph''s
      meta list. Its root node has kind=''render_plan'' and profile=''renderframe-k1''.

      '
    എന്ത
- **term.selector** (kind: term)
  - label: Selector
  - Extra fields:
    ```yml
    label: Selector
    status: normative
    text: 'A predicate object that matches source nodes (and optionally local edge context). Selectors
      are intentionally simple and deterministic.

      '
    എന്ത
- **term.template** (kind: term)
  - label: Template
  - Extra fields:
    ```yml
    label: Template
    status: normative
    text: 'A text template with placeholders. Placeholder semantics are deterministic but implementation-defined;
      missing fields MUST be handled by an explicit policy.

      '
    എന്ത
- **term.transform** (kind: term)
  - label: Transform
  - Extra fields:
    ```yml
    label: Transform
    status: normative
    text: 'A pure text-to-text transform (escape, indent, wrap, join, etc.) referenced by emitters.

      '
    എന്ത

## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.overview | clause.overview.intent | contains |  |  |  |
| section.1.overview | clause.overview.meta_usage | contains |  |  |  |
| section.1.overview | term.renderframe_k1 | contains |  |  |  |
| section.2.model | clause.model.definition | contains |  |  |  |
| section.2.model | clause.model.determinism | contains |  |  |  |
| section.2.model | clause.model.rule_resolution | contains |  |  |  |
| section.2.model | clause.model.scoping | contains |  |  |  |
| section.2.model | term.emitter | contains |  |  |  |
| section.2.model | term.render_plan | contains |  |  |  |
| section.2.model | term.render_predicate | contains |  |  |  |
| section.2.model | term.render_product | contains |  |  |  |
| section.2.model | term.render_rule | contains |  |  |  |
| section.2.model | term.selector | contains |  |  |  |
| section.2.model | term.template | contains |  |  |  |
| section.2.model | term.transform | contains |  |  |  |
| section.3.node_kinds | clause.node_kinds.allowed | contains |  |  |  |
| section.3.node_kinds | property.renderframe.node_kinds | contains |  |  |  |
| section.4.edge_types | clause.edge_types.allowed | contains |  |  |  |
| section.4.edge_types | property.renderframe.edge_types | contains |  |  |  |
| section.5.attributes | clause.attrs.emitter | contains |  |  |  |
| section.5.attributes | clause.attrs.plan | contains |  |  |  |
| section.5.attributes | clause.attrs.product | contains |  |  |  |
| section.5.attributes | clause.attrs.required | contains |  |  |  |
| section.5.attributes | clause.attrs.selector | contains |  |  |  |
| section.5.attributes | clause.attrs.template | contains |  |  |  |
| section.5.attributes | clause.attrs.transform | contains |  |  |  |
| section.5.attributes | property.renderframe.status_enum | contains |  |  |  |
| section.6.validation | clause.validation.contains_tree | contains |  |  |  |
| section.6.validation | clause.validation.edge_integrity | contains |  |  |  |
| section.6.validation | clause.validation.reference_targets | contains |  |  |  |
| section.6.validation | clause.validation.root | contains |  |  |  |
| section.7.integration | clause.integration.attach | contains |  |  |  |
| section.7.integration | clause.integration.precedence | contains |  |  |  |
| section.8.examples | example.minimal_renderframe | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | ref.spec.gf0-k1 | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | ref.spec.specframe-k1 | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.1.overview | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.2.model | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.3.node_kinds | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.4.edge_types | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.5.attributes | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.6.validation | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.7.integration | contains |  |  |  |
| spec://_kernel/render/renderframe-k1 | section.8.examples | contains |  |  |  |

## Contains Tree
- spec://_kernel/render/renderframe-k1
  - ref.spec.gf0-k1
  - ref.spec.specframe-k1
  - section.1.overview
    - clause.overview.intent
    - clause.overview.meta_usage
    - term.renderframe_k1
  - section.2.model
    - clause.model.definition
    - clause.model.determinism
    - clause.model.rule_resolution
    - clause.model.scoping
    - term.emitter
    - term.render_plan
    - term.render_predicate
    - term.render_product
    - term.render_rule
    - term.selector
    - term.template
    - term.transform
  - section.3.node_kinds
    - clause.node_kinds.allowed
    - property.renderframe.node_kinds
  - section.4.edge_types
    - clause.edge_types.allowed
    - property.renderframe.edge_types
  - section.5.attributes
    - clause.attrs.emitter
    - clause.attrs.plan
    - clause.attrs.product
    - clause.attrs.required
    - clause.attrs.selector
    - clause.attrs.template
    - clause.attrs.transform
    - property.renderframe.status_enum
  - section.6.validation
    - clause.validation.contains_tree
    - clause.validation.edge_integrity
    - clause.validation.reference_targets
    - clause.validation.root
  - section.7.integration
    - clause.integration.attach
    - clause.integration.precedence
  - section.8.examples
    - example.minimal_renderframe
