# spec://domains/systemics/k0-k1
- version: 0.1.0
- nodes: 14
- edges: 13
- meta: 0
## Nodes
- **clause.domain_agnostic** (kind: clause)
  - label: Domain-agnostic
  - Extra fields:
    ```yml
    label: Domain-agnostic
    status: informative
    text: 'K0 does not constrain domain: kernels may represent software, human workflows, simulation
      steps, or hybrid configurations.

      '
    ```
- **clause.k0** (kind: clause)
  - label: Axiom K0 (Kernel axiom)
  - Extra fields:
    ```yml
    label: Axiom K0 (Kernel axiom)
    status: normative
    text: 'Every system of interest decomposes into a finite collection of kernels {K_i} satisfying
      K1–K4.

      '
    ```
- **clause.k1.records_first** (kind: clause)
  - label: K1 Records-first
  - Extra fields:
    ```yml
    label: K1 Records-first
    status: normative
    text: 'Each kernel application emits a receipt e ∈ E sufficient to later reconstruct and audit
      the transition.

      '
    ```
- **clause.k2.replayability** (kind: clause)
  - label: K2 Replayability
  - Extra fields:
    ```yml
    label: K2 Replayability
    status: normative
    text: 'There exists a (possibly partial) replay operator R that, given an initial state and
      a sequence of receipts, reconstructs final state and outputs.

      '
    ```
- **clause.k3.budgeted** (kind: clause)
  - label: K3 Budgeted behavior
  - Extra fields:
    ```yml
    label: K3 Budgeted behavior
    status: normative
    text: 'Transitions respect budgets: b_out ⪯ b_in for a well-founded preorder ⪯ on B.

      '
    ```
- **clause.k4.composability** (kind: clause)
  - label: K4 Composability
  - Extra fields:
    ```yml
    label: K4 Composability
    status: normative
    text: 'Kernels compose along interfaces to form larger systems without breaking records-first
      behavior.

      '
    ```
- **property.kernel.fields** (kind: property)
  - label: Kernel Tuple Fields
  - Extra fields:
    ```yml
    fields:
    - desc: internal state space
      name: S
    - desc: input space
      name: I
    - desc: output space
      name: O
    - desc: budget space (resource envelopes)
      name: B
    - desc: evidence/receipt space
      name: E
    - desc: admissible transition relation over (S,I,B,S,O,B,E)
      name: F
    label: Kernel Tuple Fields
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
- **section.1.definitions** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Definitions
    ```
- **section.2.axiom** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Axiom K0
    ```
- **section.3.notes** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: informative
    title: Notes
    ```
- **spec://domains/systemics/k0-k1** (kind: spec)
  - attrs:
    | key | value | vtype | desc |
    | --- | --- | --- | --- |
    | doc.title | Systemics — Kernel Axiom K0 (K1) |  |  |
    | doc.authors | ["David Swanson"] | json |  |
    | doc.created | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.updated | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.license | CC-BY-4.0 | spdx |  |
    | doc.tags | ["systemics","k0","kernel","axiom"] | json |  |
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'Defines the Systemics kernel model K=(S,I,O,B,E,F) and Axiom K0 (K1–K4): records-first,
      replayability, budgeted behavior, composability.

      '
    title: Systemics — Kernel Axiom K0 (K1)
    ```
- **term.kernel** (kind: term)
  - label: Kernel
  - Extra fields:
    ```yml
    label: Kernel
    status: normative
    summary: 'A kernel is a tuple K=(S,I,O,B,E,F) with admissible transitions (s_in, i, b_in,
      s_out, o, b_out, e) ∈ F.

      '
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.definitions | property.kernel.fields | contains |  |  |  |
| section.1.definitions | term.kernel | contains |  |  |  |
| section.2.axiom | clause.k0 | contains |  |  |  |
| section.2.axiom | clause.k1.records_first | contains |  |  |  |
| section.2.axiom | clause.k2.replayability | contains |  |  |  |
| section.2.axiom | clause.k3.budgeted | contains |  |  |  |
| section.2.axiom | clause.k4.composability | contains |  |  |  |
| section.3.notes | clause.domain_agnostic | contains |  |  |  |
| spec://domains/systemics/k0-k1 | ref.gf0 | depends_on |  |  |  |
| spec://domains/systemics/k0-k1 | ref.specframe | depends_on |  |  |  |
| spec://domains/systemics/k0-k1 | section.1.definitions | contains |  |  |  |
| spec://domains/systemics/k0-k1 | section.2.axiom | contains |  |  |  |
| spec://domains/systemics/k0-k1 | section.3.notes | contains |  |  |  |

## Contains Tree
- spec://domains/systemics/k0-k1
  - section.1.definitions
    - property.kernel.fields
    - term.kernel
  - section.2.axiom
    - clause.k0
    - clause.k1.records_first
    - clause.k2.replayability
    - clause.k3.budgeted
    - clause.k4.composability
  - section.3.notes
    - clause.domain_agnostic
