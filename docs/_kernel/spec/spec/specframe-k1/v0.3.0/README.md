# SpecFrame K1 — Canonical Specification Graph Schema
<a id="spec-kernel-spec-specframe-k1-b5363150"></a>

## Scope and Intent
<a id="section-1-scope-22c86ec9"></a>

**Scope of SpecFrame K1** _(normative)_

SpecFrame K1 specifies the canonical schema for representing specifications as GraphFrame K0 graphs. A SpecFrame is any GF0 graph whose root node has kind = 'spec' and profile = 'specframe-k1'. All such graphs MUST conform to the node, edge, and attribute conventions defined in this spec.

**Intended consumers** _(informative)_

SpecFrame K1 is intended for: (a) human spec authors, (b) GraphBrain kernels that load, validate, and refactor specs, and (c) LLM workers that generate or update specs from code, docs, or other frames.

## Node Kinds
<a id="section-2-node-kinds-2e1d331b"></a>

**NodeK0.kind in SpecFrames** _(normative)_

**Allowed node kinds** _(normative)_

Within a SpecFrame, NodeK0.kind MUST be one of:
  - 'spec'      : the root specification node (exactly one per SpecFrame),
  - 'section'   : top-level or nested sections grouping terms and clauses,
  - 'term'      : definitions of key concepts,
  - 'clause'    : normative or informative statements,
  - 'property'  : small structured facts (enums, lists, thresholds),
  - 'example'   : worked examples illustrating other nodes,
  - 'spec_ref'  : references to other specs or frames.
Any other value MUST be reported as a validation error.

**Root spec node** _(normative)_

Each SpecFrame MUST contain exactly one node with:
  - id == graph_id,
  - kind == 'spec',
  - status in {'normative', 'informative', 'experimental'}.
This node is the root of the spec and is the unique entry point for reachability and top-level attributes.

**Allowed Node Kinds** _(normative)_

## Edge Types
<a id="section-3-edge-kinds-4fd13ee4"></a>

**EdgeK0.type in SpecFrames** _(normative)_

**contains edge semantics** _(normative)_

'contains' edges encode the structural tree of the spec. The root 'spec' node MUST contain one or more 'section' nodes. Section nodes MAY contain other sections, terms, clauses, properties, and examples. Contains edges MUST form an acyclic tree (or forest) rooted at the spec node.

**Allowed edge types** _(normative)_

Within a SpecFrame, EdgeK0.type MUST be one of:
  - 'contains'   : structural containment / hierarchy,
  - 'depends_on' : spec-level dependency on another node or spec,
  - 'defines'    : term or clause defines another concept,
  - 'refines'    : clause refines or tightens another clause,
  - 'refers_to'  : non-normative reference to another node or spec,
  - 'example_of' : examples illustrating a term or clause.
Any other value MUST be reported as a validation error.

**Allowed Edge Types** _(normative)_

## Attributes
<a id="section-4-attributes-d85afce6"></a>

**SpecStatus** _(normative)_

**Attributes for clause nodes** _(normative)_

A node with kind == 'clause' MUST provide:
  - 'label' : short handle for the clause,
  - 'status': SpecStatus.
It SHOULD provide:
  - 'text'  : full clause text in natural language.

**Attributes for example nodes** _(informative)_

A node with kind == 'example' MUST provide:
  - 'label' : short identifier for the example,
  - 'status': SpecStatus (typically 'informative').
It SHOULD provide:
  - 'text'  : free-form example text or code snippet.

**Attributes for property nodes** _(normative)_

A node with kind == 'property' MUST provide:
  - 'label' : short name of the property,
  - 'status': SpecStatus.
Property nodes MAY carry arbitrary additional attributes (lists, enums, thresholds) that are interpreted by tooling.

**Required attributes per node kind** _(normative)_

A SpecFrame validator MUST treat missing required attributes as a hard validation error. Required attributes per kind are:
  - spec     : title, status, summary, profile
  - section  : title, status
  - term     : label, status
  - clause   : label, status
  - property : label, status
  - example  : label, status
  - spec_ref : target_graph_id

**Attributes for section nodes** _(normative)_

A node with kind == 'section' MUST provide:
  - 'title' : short section title,
  - 'status': SpecStatus.
It SHOULD provide:
  - 'order' : integer for ordering sections within the spec.
Sections MAY nest other sections via 'contains'.

**Attributes for spec nodes** _(normative)_

A node with kind == 'spec' MUST provide at least:
  - 'title'   : short human-readable title,
  - 'status'  : SpecStatus,
  - 'summary' : short description of the spec's scope,
  - 'profile' : string identifying the spec profile, e.g. 'specframe-k1'.
The spec node MAY also include 'version_note', 'domain', and additional profile-specific attributes.

**Attributes for spec_ref nodes** _(normative)_

A node with kind == 'spec_ref' MUST provide:
  - 'target_graph_id' : canonical graph_id of the referenced spec or frame.
It MAY provide:
  - 'label' : short human-readable label,
  - 'note'  : explanatory text about the reference.

**Allowed status values** _(normative)_

For all nodes in a SpecFrame, the status attribute MUST be one of:
  - 'normative',
  - 'informative',
  - 'experimental'.

**Attributes for term nodes** _(normative)_

A node with kind == 'term' MUST provide:
  - 'label' : short name of the term,
  - 'status': SpecStatus.
The primary definition text MAY be stored in 'text'. Terms are usually linked via 'defines' edges from clauses that define them.

## Validation Invariants
<a id="section-5-validation-ae9a4b61"></a>

**Contains edges form a tree** _(normative)_

'contains' edges MUST form an acyclic tree (or forest) rooted at the spec node. Cycles or multiple parents for the same node via 'contains' are considered hard validation failures.

**Edge type validation** _(normative)_

A SpecFrame validator MUST reject any edge whose type attribute is not in the allowed set specified by property.edge_types. Unknown edge types are considered hard validation failures.

**Node kind validation** _(normative)_

A SpecFrame validator MUST reject any node whose kind attribute is not in the allowed set specified by property.node_kinds. Unknown or misspelled kinds are considered hard validation failures.

**Reachability from root** _(normative)_

All normative nodes in a SpecFrame SHOULD be reachable from the root spec node via one or more 'contains' edges. Unreachable normative nodes SHOULD be treated as errors or at least strong warnings by tooling.

## Integration and Usage
<a id="section-6-integration-541339b9"></a>

**Frame-level metadata location** _(normative)_

In SpecFrames, frame-level metadata (publish routing, domain tags, dependency tags, audience tags) SHOULD be stored in GraphFrameK0.attrs. GraphFrameK0.meta MUST be used only for true MetaGraphs (aux layout/index/view graphs) as defined by GF0. A SpecFrame validator MUST NOT require any particular GraphFrameK0.attrs keys; attrs is tooling- facing metadata and does not affect the node/edge validation rules.

**Recommended SpecFrame attrs keys** _(informative)_

Tooling MAY adopt the following conventional GraphFrameK0.attrs keys for SpecFrames:
  - domain
  - depends_on (repeatable)
  - intended_consumer (repeatable)
  - publish.root
  - publish.path
  - publish.slug

**Use in GraphBrain and specgen** _(informative)_

GraphBrain and specgen SHOULD treat SpecFrame K1 as the canonical schema for specs. Specs for other domains (canon, CBF, GSKernel, TaskFrame, EvidenceFrame, KernelCore, regimes) SHOULD be represented as SpecFrames and validated against this schema so that they can be composed, diffed, and refactored uniformly.

**Allowed Edge Types** _(normative)_

**Allowed Node Kinds** _(normative)_

**Spec Status Enum** _(normative)_

## References
<a id="refs-e812cd2d"></a>

- Canon envelope mappings ()
- GraphFrame K0 schema ()
- TargetRef naming scheme ()
