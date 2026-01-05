# spec://_kernel/docs/docprofiles-k1
- version: 0.1.0
- nodes: 31
- edges: 33
- meta: 0
## Nodes
- **clause.core_model.frame_metadata** (kind: clause)
  - label: frame-metadata
  - Extra fields:
    ```yml
    label: frame-metadata
    status: informative
    text: 'Frame-level tags such as ''domain'', ''depends_on'', and publishing hints SHOULD be
      stored in GraphFrameK0.attrs. MetaGraphs are reserved for auxiliary structural subgraphs
      (indexes/layout/nav) per GF0.

      '
    എന്ത
- **clause.core_model.profile_location** (kind: clause)
  - label: profile-location
  - Extra fields:
    ```yml
    label: profile-location
    status: normative
    text: 'A document selects a DocProfile by providing ''doc_profile'' as an attribute on the
      root ''spec'' node (id == graph_id). Tooling MAY ignore unknown doc_profile values.

      '
    എന്ത
- **clause.core_model.profile_semantics** (kind: clause)
  - label: profile-semantics
  - Extra fields:
    ```yml
    label: profile-semantics
    status: normative
    text: 'A doc_profile MUST NOT change the underlying SpecFrame K1 validity rules. It only adds
      conventions (required/recommended content and lint/render expectations).

      '
    എന്ത
- **clause.lint.baseline** (kind: clause)
  - label: lint-baseline
  - Extra fields:
    ```yml
    label: lint-baseline
    status: informative
    text: 'Tooling SHOULD lint for: (1) all normative nodes reachable from the spec root via ''contains'',
      (2) stable ordering (section.order then lexical fallback), (3) valid edge types and node
      kinds.

      '
    എന്ത
- **clause.overview.intent** (kind: clause)
  - label: intent
  - Extra fields:
    ```yml
    label: intent
    status: normative
    text: 'DocProfiles are conventions layered on SpecFrame K1 to support consistent authoring,
      deterministic rendering, and automated linting across many document types.

      '
    എന്ത
- **clause.rendering.baseline** (kind: clause)
  - label: render-baseline
  - Extra fields:
    ```yml
    label: render-baseline
    status: informative
    text: 'Rendering is implementation-defined but SHOULD be deterministic: same input graph ->
      same output files. Common render products: per-spec README, per-section pages, glossary
      from term nodes, and backlinks from refs.

      '
    എന്ത
- **property.profile.guide-k1.required_properties** (kind: property)
  - label: required_properties
  - Extra fields:
    ```yml
    label: required_properties
    profile_id: guide-k1
    required_properties:
    - property.prereqs
    - property.steps
    - property.pitfalls
    status: informative
    എന്ത
- **property.profile.hardware_spec-k1.required_sections** (kind: property)
  - label: required_sections
  - Extra fields:
    ```yml
    label: required_sections
    profile_id: hardware_spec-k1
    required_sections:
    - section.1.overview
    - section.scope
    - section.interfaces
    - section.constraints
    - section.testing
    status: normative
    എന്ത
- **property.profile.math_theory-k1.conventions** (kind: property)
  - label: conventions
  - Extra fields:
    ```yml
    clause_kinds:
    - axiom
    - definition
    - theorem
    - lemma
    - proof
    - corollary
    label: conventions
    profile_id: math_theory-k1
    status: informative
    എന്ത
- **property.profile.software_spec-k1.required_properties** (kind: property)
  - label: required_properties
  - Extra fields:
    ```yml
    label: required_properties
    profile_id: software_spec-k1
    required_properties:
    - property.api_surface
    - property.invariants
    - property.compat
    status: informative
    എന്ത
- **property.profile.software_spec-k1.required_sections** (kind: property)
  - label: required_sections
  - Extra fields:
    ```yml
    label: required_sections
    profile_id: software_spec-k1
    required_sections:
    - section.1.overview
    - section.goals
    - section.definitions
    - section.architecture
    - section.interfaces
    - section.invariants
    - section.testing
    - section.versioning
    status: normative
    എന്ത
- **property.profile.standard-k1.required_properties** (kind: property)
  - label: required_properties
  - Extra fields:
    ```yml
    label: required_properties
    profile_id: standard-k1
    required_properties:
    - property.versioning
    - property.keywords
    status: informative
    എന്ത
- **property.profile.standard-k1.required_sections** (kind: property)
  - label: required_sections
  - Extra fields:
    ```yml
    label: required_sections
    profile_id: standard-k1
    required_sections:
    - section.1.overview
    - section.scope
    - section.definitions
    - section.requirements
    - section.conformance
    status: normative
    എന്ത
- **ref.spec.gf0-k1** (kind: spec_ref)
  - label: GraphFrame GF0
  - Extra fields:
    ```yml
    label: GraphFrame GF0
    note: Base graph substrate.
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    എന്ത
- **ref.spec.specframe-k1** (kind: spec_ref)
  - label: SpecFrame K1
  - Extra fields:
    ```yml
    label: SpecFrame K1
    note: 'Document spine: sections/terms/clauses/properties/examples.'
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
- **section.2.core_model** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Core Model
    എന്ത
- **section.3.profile_catalog** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Profile Catalog
    എന്ത
- **section.4.lint_rules** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: informative
    title: Lint Rules
    എന്ത
- **section.5.rendering_hints** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: informative
    title: Rendering Hints
    എന്ത
- **section.6.examples** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: informative
    title: Examples
    എന്ത
- **spec://_kernel/docs/docprofiles-k1** (kind: spec)
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'A registry of document profiles (doc_profile) layered on top of SpecFrame K1. Profiles
      are conventions: required sections, required properties, recommended lint rules, and optional
      rendering hints.

      '
    title: DocProfiles K1 — Document Profile Registry
    എന്ത
- **term.doc_profile** (kind: term)
  - label: doc_profile
  - Extra fields:
    ```yml
    label: doc_profile
    status: normative
    text: 'A secondary profile selector used by tooling to apply conventions for a particular
      document type while remaining a valid SpecFrame K1 graph.

      '
    എന്ത
- **term.profile.guide-k1** (kind: term)
  - label: guide-k1
  - Extra fields:
    ```yml
    label: guide-k1
    status: normative
    text: 'How-to guides: prerequisites, steps, pitfalls, verification.'
    എന്ത
- **term.profile.hardware_spec-k1** (kind: term)
  - label: hardware_spec-k1
  - Extra fields:
    ```yml
    label: hardware_spec-k1
    status: normative
    text: 'Hardware specs: interfaces/pinout, electrical/mechanical constraints, tolerances, tests.'
    എന്ത
- **term.profile.math_theory-k1** (kind: term)
  - label: math_theory-k1
  - Extra fields:
    ```yml
    label: math_theory-k1
    status: normative
    text: 'Math/theory docs: definitions, axioms, theorems, proofs, corollaries, examples.'
    എന്ത
- **term.profile.playbook-k1** (kind: term)
  - label: playbook-k1
  - Extra fields:
    ```yml
    label: playbook-k1
    status: normative
    text: 'Operational playbooks: triggers, runbook steps, rollback, metrics, comms.'
    എന്ത
- **term.profile.software_spec-k1** (kind: term)
  - label: software_spec-k1
  - Extra fields:
    ```yml
    label: software_spec-k1
    status: normative
    text: 'Software framework/module specs: APIs, data model, invariants, compatibility, tests.'
    എന്ത
- **term.profile.standard-k1** (kind: term)
  - label: standard-k1
  - Extra fields:
    ```yml
    label: standard-k1
    status: normative
    text: 'Normative standards and laws: MUST/SHOULD language, conformance and compliance focus.'
    എന്ത
- **term.profile_id** (kind: term)
  - label: ProfileId
  - Extra fields:
    ```yml
    label: ProfileId
    status: normative
    text: 'A stable identifier string for a doc_profile (e.g. ''software_spec-k1'').

      '
    എന്ത
- **term.profile_rule** (kind: term)
  - label: ProfileRule
  - Extra fields:
    ```yml
    label: ProfileRule
    status: normative
    text: 'A conventional rule attached to a doc_profile, typically expressed as required sections,
      required properties, lint expectations, and rendering hints.

      '
    എന്ത

## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| clause.core_model.profile_location | term.doc_profile | defines |  |  |  |
| clause.core_model.profile_location | term.profile_id | defines |  |  |  |
| clause.core_model.profile_semantics | term.profile_rule | defines |  |  |  |
| section.1.overview | clause.overview.intent | contains |  |  |  |
| section.2.core_model | clause.core_model.frame_metadata | contains |  |  |  |
| section.2.core_model | clause.core_model.profile_location | contains |  |  |  |
| section.2.core_model | clause.core_model.profile_semantics | contains |  |  |  |
| section.2.core_model | term.doc_profile | contains |  |  |  |
| section.2.core_model | term.profile_id | contains |  |  |  |
| section.2.core_model | term.profile_rule | contains |  |  |  |
| section.3.profile_catalog | term.profile.guide-k1 | contains |  |  |  |
| section.3.profile_catalog | term.profile.hardware_spec-k1 | contains |  |  |  |
| section.3.profile_catalog | term.profile.math_theory-k1 | contains |  |  |  |
| section.3.profile_catalog | term.profile.playbook-k1 | contains |  |  |  |
| section.3.profile_catalog | term.profile.software_spec-k1 | contains |  |  |  |
| section.3.profile_catalog | term.profile.standard-k1 | contains |  |  |  |
| section.4.lint_rules | clause.lint.baseline | contains |  |  |  |
| section.5.rendering_hints | clause.rendering.baseline | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | ref.spec.gf0-k1 | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | ref.spec.specframe-k1 | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | section.1.overview | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | section.2.core_model | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | section.3.profile_catalog | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | section.4.lint_rules | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | section.5.rendering_hints | contains |  |  |  |
| spec://_kernel/docs/docprofiles-k1 | section.6.examples | contains |  |  |  |
| term.profile.guide-k1 | property.profile.guide-k1.required_properties | contains |  |  |  |
| term.profile.hardware_spec-k1 | property.profile.hardware_spec-k1.required_sections | contains |  |  |  |
| term.profile.math_theory-k1 | property.profile.math_theory-k1.conventions | contains |  |  |  |
| term.profile.software_spec-k1 | property.profile.software_spec-k1.required_properties | contains |  |  |  |
| term.profile.software_spec-k1 | property.profile.software_spec-k1.required_sections | contains |  |  |  |
| term.profile.standard-k1 | property.profile.standard-k1.required_properties | contains |  |  |  |
| term.profile.standard-k1 | property.profile.standard-k1.required_sections | contains |  |  |  |

## Contains Tree
- spec://_kernel/docs/docprofiles-k1
  - ref.spec.gf0-k1
  - ref.spec.specframe-k1
  - section.1.overview
    - clause.overview.intent
  - section.2.core_model
    - clause.core_model.frame_metadata
    - clause.core_model.profile_location
    - clause.core_model.profile_semantics
    - term.doc_profile
    - term.profile_id
    - term.profile_rule
  - section.3.profile_catalog
    - term.profile.guide-k1
      - property.profile.guide-k1.required_properties
    - term.profile.hardware_spec-k1
      - property.profile.hardware_spec-k1.required_sections
    - term.profile.math_theory-k1
      - property.profile.math_theory-k1.conventions
    - term.profile.playbook-k1
    - term.profile.software_spec-k1
      - property.profile.software_spec-k1.required_properties
      - property.profile.software_spec-k1.required_sections
    - term.profile.standard-k1
      - property.profile.standard-k1.required_properties
      - property.profile.standard-k1.required_sections
  - section.4.lint_rules
    - clause.lint.baseline
  - section.5.rendering_hints
    - clause.rendering.baseline
  - section.6.examples
