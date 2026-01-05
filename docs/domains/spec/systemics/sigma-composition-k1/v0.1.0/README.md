# spec://domains/systemics/sigma-composition-k1
- version: 0.1.0
- nodes: 17
- edges: 16
- meta: 0
## Nodes
- **clause.charter** (kind: clause)
  - label: Charter
  - Extra fields:
    ```yml
    label: Charter
    status: normative
    text: 'This spec defines how lawful Σ kernels compose in serial, parallel, and temporal forms,
      preserving Σ lawfulness via posted adapters/combinators and monotone contract combination.

      '
    ```
- **clause.invariant.records_only** (kind: clause)
  - label: Records-only preserved
  - Extra fields:
    ```yml
    label: Records-only preserved
    status: normative
    text: 'Composition MUST preserve Σ-A2 (records-only): any dependency introduced by composition
      must be posted.

      '
    ```
- **clause.invariant.replay_preserved** (kind: clause)
  - label: Replay preserved
  - Extra fields:
    ```yml
    label: Replay preserved
    status: normative
    text: 'Composition MUST preserve reflexive reproducibility and replayability obligations implied
      by the Σ contract.

      '
    ```
- **clause.parallel.comb_posted** (kind: clause)
  - label: Posted decision combinator
  - Extra fields:
    ```yml
    label: Posted decision combinator
    status: normative
    text: 'For parallel/product composition K1 ⊗ K2, both kernels evaluate and decisions are aggregated
      via a posted combinator comb: 2 × 2 → 2 (e.g., AND/OR). The choice of comb MUST be posted
      as part of the record/contract.

      '
    ```
- **clause.parallel.monotone_contracts** (kind: clause)
  - label: Monotone floors/budgets
  - Extra fields:
    ```yml
    label: Monotone floors/budgets
    status: normative
    text: 'Floors and budgets for parallel composition MUST be combined monotonically (tightening
      cannot rely on hidden slack).

      '
    ```
- **clause.serial.adapter_posted** (kind: clause)
  - label: Posted adapter requirement
  - Extra fields:
    ```yml
    label: Posted adapter requirement
    status: normative
    text: 'For serial composition with K1^Σ = (v1, χ1, …) and K2^Σ = (v2, χ2, …), any adapter
      f used to produce the second valuation MUST be posted as part of the record/contract. In
      particular, if v2 is defined from u and the upstream decision by: v2(u) = f(u, χ1(v1(u),
      Θ1, β1)), then f MUST be included in posted data so downstream decisions remain records-only.

      '
    ```
- **clause.serial.monotone_combine** (kind: clause)
  - label: Monotone contract combination
  - Extra fields:
    ```yml
    label: Monotone contract combination
    status: normative
    text: 'The composite kernel K2 ∘ K1 is lawful only if (Σ-A1 … Σ-A7) hold for the composite
      and if the combined contracts (Θ, β, C) are formed via a monotone operator ⊕ (domain-chosen),
      i.e. tightening in any component must not rely on hidden slack.

      '
    ```
- **clause.temporal.pages_books** (kind: clause)
  - label: Pages and books
  - Extra fields:
    ```yml
    label: Pages and books
    status: normative
    text: 'A page is a lawful record κ for one window. A book is an ordered sequence of pages;
      optionally, pages may be hash-chained. Chaining preserves replay and does not alter decisions.

      '
    ```
- **ref.gf0** (kind: spec_ref)
  - label: GraphFrame K0 (GF0)
  - Extra fields:
    ```yml
    label: GraphFrame K0 (GF0)
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    ```
- **ref.sigma** (kind: spec_ref)
  - label: Systemics Σ — Minimal Specification
  - Extra fields:
    ```yml
    label: Systemics Σ — Minimal Specification
    status: informative
    target_graph_id: spec://domains/systemics/sigma-k1
    ```
- **ref.specframe** (kind: spec_ref)
  - label: SpecFrame K1
  - Extra fields:
    ```yml
    label: SpecFrame K1
    status: informative
    target_graph_id: spec://_kernel/spec/specframe-k1
    ```
- **section.1.charter** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Charter
    ```
- **section.2.serial** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Serial Composition
    ```
- **section.3.parallel** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Parallel / Product Composition
    ```
- **section.4.temporal** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: Temporal Composition (window → page → book)
    ```
- **section.5.invariants** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: Composition Invariants
    ```
- **spec://domains/systemics/sigma-composition-k1** (kind: spec)
  - attrs:
    | key | value | vtype | desc |
    | --- | --- | --- | --- |
    | doc.title | Systemics Σ — Composition (K1) |  |  |
    | doc.authors | ["David Swanson"] | json |  |
    | doc.created | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.updated | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.license | CC-BY-4.0 | spdx |  |
    | doc.tags | ["systemics","sigma","composition"] | json |  |
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'Defines Σ composition forms: Serial composition (with posted adapter), Parallel/product
      composition (posted decision combinator), and Temporal composition (window→page→book). Constrains
      composition to preserve Σ lawfulness (axioms + contract monotonicity).

      '
    title: Systemics Σ — Composition (K1)
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.charter | clause.charter | contains |  |  |  |
| section.2.serial | clause.serial.adapter_posted | contains |  |  |  |
| section.2.serial | clause.serial.monotone_combine | contains |  |  |  |
| section.3.parallel | clause.parallel.comb_posted | contains |  |  |  |
| section.3.parallel | clause.parallel.monotone_contracts | contains |  |  |  |
| section.4.temporal | clause.temporal.pages_books | contains |  |  |  |
| section.5.invariants | clause.invariant.records_only | contains |  |  |  |
| section.5.invariants | clause.invariant.replay_preserved | contains |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | ref.gf0 | depends_on |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | ref.sigma | depends_on |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | ref.specframe | depends_on |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | section.1.charter | contains |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | section.2.serial | contains |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | section.3.parallel | contains |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | section.4.temporal | contains |  |  |  |
| spec://domains/systemics/sigma-composition-k1 | section.5.invariants | contains |  |  |  |

## Contains Tree
- spec://domains/systemics/sigma-composition-k1
  - section.1.charter
    - clause.charter
  - section.2.serial
    - clause.serial.adapter_posted
    - clause.serial.monotone_combine
  - section.3.parallel
    - clause.parallel.comb_posted
    - clause.parallel.monotone_contracts
  - section.4.temporal
    - clause.temporal.pages_books
  - section.5.invariants
    - clause.invariant.records_only
    - clause.invariant.replay_preserved
