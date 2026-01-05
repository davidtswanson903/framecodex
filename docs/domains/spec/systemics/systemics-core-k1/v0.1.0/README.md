# spec://domains/systemics/systemics-core-k1
- version: 0.1.0
- nodes: 10
- edges: 9
- meta: 0
## Nodes
- **clause.charter.scope** (kind: clause)
  - label: Scope
  - Extra fields:
    ```yml
    label: Scope
    status: normative
    text: 'Systemics Core currently includes only: (1) Kernel Axiom K0, (2) Systemics Σ Minimal
      Specification, and (3) Σ Composition. Other Systemics meta-algebras and instantiations are
      out of scope for this domain version.

      '
    ```
- **property.specs.list** (kind: property)
  - label: Spec List
  - Extra fields:
    ```yml
    label: Spec List
    specs:
    - spec://domains/systemics/k0-k1
    - spec://domains/systemics/sigma-k1
    - spec://domains/systemics/sigma-composition-k1
    status: normative
    ```
- **ref.gf0** (kind: spec_ref)
  - label: GraphFrame K0 (GF0)
  - Extra fields:
    ```yml
    label: GraphFrame K0 (GF0)
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    ```
- **ref.specframe** (kind: spec_ref)
  - label: SpecFrame K1
  - Extra fields:
    ```yml
    label: SpecFrame K1
    status: informative
    target_graph_id: spec://_kernel/spec/specframe-k1
    ```
- **ref.systemics.k0** (kind: spec_ref)
  - label: Systemics — Kernel Axiom K0
  - Extra fields:
    ```yml
    label: Systemics — Kernel Axiom K0
    status: informative
    target_graph_id: spec://domains/systemics/k0-k1
    ```
- **ref.systemics.sigma** (kind: spec_ref)
  - label: Systemics Σ — Minimal Specification
  - Extra fields:
    ```yml
    label: Systemics Σ — Minimal Specification
    status: informative
    target_graph_id: spec://domains/systemics/sigma-k1
    ```
- **ref.systemics.sigma.composition** (kind: spec_ref)
  - label: Systemics Σ — Composition
  - Extra fields:
    ```yml
    label: Systemics Σ — Composition
    status: informative
    target_graph_id: spec://domains/systemics/sigma-composition-k1
    ```
- **section.1.charter** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Charter
    ```
- **section.2.specs** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Included Specs
    ```
- **spec://domains/systemics/systemics-core-k1** (kind: spec)
  - attrs:
    | key | value | vtype | desc |
    | --- | --- | --- | --- |
    | doc.title | Systemics Core — Domain Index (K1) |  |  |
    | doc.summary | Landing index for Systemics Core specs (K0 + Σ). |  |  |
    | doc.authors | ["David Swanson"] | json |  |
    | doc.created | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.updated | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.license | CC-BY-4.0 | spdx |  |
    | doc.tags | ["systemics","domain","index"] | json |  |
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'Index/landing SpecFrame for the Systemics core domain in framecodex. Canonical in-repo
      source for the minimal Systemics core set: Kernel Axiom K0, Systemics Σ, and Σ Composition.

      '
    title: Systemics Core — Domain Index (K1)
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.charter | clause.charter.scope | contains |  |  |  |
| section.2.specs | property.specs.list | contains |  |  |  |
| section.2.specs | ref.systemics.k0 | contains |  |  |  |
| section.2.specs | ref.systemics.sigma | contains |  |  |  |
| section.2.specs | ref.systemics.sigma.composition | contains |  |  |  |
| spec://domains/systemics/systemics-core-k1 | ref.gf0 | depends_on |  |  |  |
| spec://domains/systemics/systemics-core-k1 | ref.specframe | depends_on |  |  |  |
| spec://domains/systemics/systemics-core-k1 | section.1.charter | contains |  |  |  |
| spec://domains/systemics/systemics-core-k1 | section.2.specs | contains |  |  |  |

## Contains Tree
- spec://domains/systemics/systemics-core-k1
  - section.1.charter
    - clause.charter.scope
  - section.2.specs
    - property.specs.list
    - ref.systemics.k0
    - ref.systemics.sigma
    - ref.systemics.sigma.composition
