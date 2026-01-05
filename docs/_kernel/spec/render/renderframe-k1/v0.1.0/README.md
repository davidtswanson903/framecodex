# RenderFrame K1 — Text Rendering Plan MetaGraph Profile
<a id="spec-kernel-render-renderframe-k1-77128a96"></a>

## Overview
<a id="section-1-overview-80ccecc5"></a>

**RenderFrameK1** _(normative)_


**Intent** _(normative)_

RenderFrame K1 specifies a portable, deterministic plan for rendering graphs into text. The plan MAY tag outputs with a 'format' string (e.g. 'markdown', 'latex'), but the core semantics are purely text-based.

**RenderFrames are MetaGraphs** _(normative)_

A RenderFrame is intended to be carried as a GF0 MetaGraph under the 'meta' list of a source graph. This follows GF0's intent for meta: attach auxiliary views, layouts, and indexes without changing the primary frame.

## Model
<a id="section-2-model-d7d22876"></a>

**Emitter** _(normative)_


**RenderPlan** _(normative)_


**RenderPredicate** _(normative)_


**RenderProduct** _(normative)_


**RenderRule** _(normative)_


**Selector** _(normative)_


**Template** _(normative)_


**Transform** _(normative)_


**Definition** _(normative)_

A RenderFrame is any GF0 graph that satisfies: (1) It is a valid GraphFrameK0 (graph*id/version/attrs/nodes/edges/meta present in canonical form); (2) It contains exactly one root node with id==graph*id, kind=='render_plan'; (3) That root node has profile=='renderframe-k1'.

**Determinism** _(normative)_

For the same canonical source graph + the same canonical RenderFrame, an implementation MUST produce identical text outputs. Where ordering is required, it MUST be derived from explicit integer 'order' attributes when present, otherwise from stable lexical ordering of node IDs.

**Rule resolution** _(normative)_

Within a RenderProduct, rules are evaluated in deterministic order. For a given source node, the first matching rule (by rule order) MUST be applied unless the product declares a different explicit resolution mode (e.g. 'merge').

**Scoping into parent graphs** _(normative)_

RenderFrames are structurally independent from their parent graphs. Any references from a RenderFrame into the source graph MUST be expressed via attributes (e.g. parent*graph*id, parent*node*id, source*root*id) or via explicit edge types with documented semantics.

## RenderFrame Node Kinds
<a id="section-3-node-kinds-7f208afe"></a>

**Allowed node kinds** _(normative)_

Within a RenderFrame, NodeK0.kind MUST be one of the values in property.renderframe.node_kinds. Unknown or misspelled kinds MUST be treated as hard validation failures.

**Allowed RenderFrame node kinds** _(normative)_

## RenderFrame Edge Types
<a id="section-4-edge-types-4ab003f8"></a>

**Allowed edge types** _(normative)_

Within a RenderFrame, EdgeK0.type MUST be one of the values in property.renderframe.edge_types. Unknown edge types MUST be treated as hard validation failures.

**Allowed RenderFrame edge types** _(normative)_

## Required Attributes
<a id="section-5-attributes-9accd5df"></a>

**Attributes for emitter nodes** _(normative)_

A node with kind=='emitter' MUST provide: - label  : short emitter name, - status : RenderStatus. It SHOULD provide: - template_id : node id of a template node in the same RenderFrame. It MAY provide: - pipeline : ordered list of transform node ids to apply to the emitted text.

**Attributes for render\_plan nodes** _(normative)_

A node with kind=='render*plan' MUST provide: - title   : short plan title, - status  : RenderStatus, - summary : short description, - profile : 'renderframe-k1'. It MAY also provide: - format*hint : string tag (e.g. 'markdown', 'latex', 'text'), - applies*to*doc*profile : string tag used by tooling, - on*missing_field : 'empty' | 'error' (default: 'empty').

**Attributes for render\_product nodes** _(normative)_

A node with kind=='render*product' MUST provide: - label  : short product name, - status : RenderStatus. It MAY provide: - output*kind : 'file' | 'string' (default: 'string'), - output*path : string (required if output*kind=='file'), - source*root*id : string (parent graph node id) selecting a render root, - resolution*mode : 'first*match' | 'merge' (default: 'first_match').

**Required attributes per node kind** _(normative)_

A RenderFrame validator MUST treat missing required attributes as a hard validation error. Required attributes per kind are: - render*plan    : title, status, summary, profile - render*product : label, status - render_rule    : label, status - selector       : label, status - emitter        : label, status - template       : label, status, body - transform      : label, status, op

**Attributes for selector nodes** _(normative)_

A node with kind=='selector' MUST provide: - label  : short selector name, - status : RenderStatus. It SHOULD provide: - predicates : ordered list of RenderPredicate strings. Selector predicate syntax is implementation-defined but MUST be deterministic.

**Attributes for template nodes** _(normative)_

A node with kind=='template' MUST provide: - label  : short template name, - status : RenderStatus, - body   : template text. Templates MAY contain placeholders. Placeholder syntax is implementation-defined, but MUST be deterministic and MUST define behavior for missing fields (see render*plan.on*missing_field).

**Attributes for transform nodes** _(normative)_

A node with kind=='transform' MUST provide: - label  : short transform name, - status : RenderStatus, - op     : string naming a pure text transform operation. It MAY provide: - args : ordered list of string args (interpretation is op-specific).

**RenderStatus enum** _(normative)_

## Validation Invariants
<a id="section-6-validation-58aa1550"></a>

**Contains edges form a tree** _(normative)_

'contains' edges in a RenderFrame MUST form an acyclic tree (or forest) rooted at the render_plan node. Cycles or multiple parents via 'contains' are hard validation failures.

**Edge integrity** _(normative)_

All edges MUST reference existing node IDs (EdgeK0.from/to integrity). Missing endpoints are hard validation failures.

**Reference targets** _(normative)_

For every 'selects' edge, the destination node MUST have kind=='selector'. For every 'emits' edge, the destination node MUST have kind=='emitter'. For every emitter.template_id, the referenced node MUST exist and have kind=='template'. For every transform listed in an emitter pipeline, the referenced node MUST exist and have kind=='transform'.

**Root plan node** _(normative)_

Each RenderFrame MUST contain exactly one node with: - id == graph*id, - kind == 'render*plan', - profile == 'renderframe-k1'.

## Integration and Usage
<a id="section-7-integration-114f38a5"></a>

**Attaching RenderFrames** _(informative)_

RenderFrames SHOULD be attached to a source graph via GF0.meta (as a MetaGraph). Implementations MAY also store RenderFrames as standalone GF0 files and attach them at build time.

**Precedence and overrides** _(informative)_

If multiple RenderFrames apply, precedence SHOULD be deterministic: later MetaGraphs in the source graph's meta list win, or explicit 'overrides' edges define precedence. If both exist, explicit overrides SHOULD take precedence.

## Examples
<a id="section-8-examples-3bd695e4"></a>

## References
<a id="refs-e812cd2d"></a>

- GraphFrame K0 (GF0) ()
- SpecFrame K1 ()
