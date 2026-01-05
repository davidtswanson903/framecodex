# spec://domains/systemics/sigma-k1
- version: 0.1.0
- nodes: 30
- edges: 29
- meta: 0
## Nodes
- **clause.a1** (kind: clause)
  - label: Σ-A1 Well-typedness
  - Extra fields:
    ```yml
    label: Σ-A1 Well-typedness
    status: normative
    text: 'All maps are measurable/continuous as needed; χ is total on V × Θ × β.

      '
    ```
- **clause.a2** (kind: clause)
  - label: Σ-A2 Posting / Records-only
  - Extra fields:
    ```yml
    label: Σ-A2 Posting / Records-only
    status: normative
    text: 'For any run on u ∈ U, the record κ ∈ R contains (v(u), Θ, β, C, Π, P_n, Γ), and the
      decision equals χ*(u; κ) = χ(v(u), Θ, β), with no dependence on unposted data.

      '
    ```
- **clause.a3** (kind: clause)
  - label: Σ-A3 Benign invariance
  - Extra fields:
    ```yml
    label: Σ-A3 Benign invariance
    status: normative
    text: 'Let (π,p) ∈ Π × P_n act on the measurement/evaluation pathway to yield v_{π,p}(u).
      Define W(u) := sup_{(π,p)} w(v_{π,p}(u), v_{π0,p0}(u)). If W(u) ⪯ β then for all benign
      (π,p), χ(v_{π,p}(u), Θ, β) = χ(v_{π0,p0}(u), Θ, β).

      '
    ```
- **clause.a4** (kind: clause)
  - label: Σ-A4 Minimal sufficiency under capacity
  - Extra fields:
    ```yml
    label: Σ-A4 Minimal sufficiency under capacity
    status: normative
    text: 'Among valuations preserving decisions under posted (Θ, β), v is minimal w.r.t. capacity
      cost subject to C: for all v'', (χ ∘ v'' = χ ∘ v) ⇒ cost(v'') ⪰ cost(v), subject to C.

      '
    ```
- **clause.a5** (kind: clause)
  - label: Σ-A5 Reflexive reproducibility
  - Extra fields:
    ```yml
    label: Σ-A5 Reflexive reproducibility
    status: normative
    text: 'There exists an admissible, independently realized v'' (different numeric/route) such
      that χ(v(u), Θ, β) = χ(v''(u), Θ, β), with both posted in κ (self-warrant).

      '
    ```
- **clause.a6** (kind: clause)
  - label: Σ-A6 Determinism & idempotence
  - Extra fields:
    ```yml
    label: Σ-A6 Determinism & idempotence
    status: normative
    text: 'For fixed (v(u), Θ, β), the decision χ is unique and idempotent under re-evaluation.

      '
    ```
- **clause.a7** (kind: clause)
  - label: Σ-A7 Monotonicity
  - Extra fields:
    ```yml
    label: Σ-A7 Monotonicity
    status: normative
    text: 'Tightening floors or budgets cannot rescue a failure by hidden dependence. For θ ⪯
      θ'' and β'' ⪯ β, χ(v, θ, β) = 1 implies χ(v, θ'', β'') ∈ {0,1} with no hidden rescue: tightening
      must not create a pass whose justification depends on data not posted in the record.

      '
    ```
- **clause.a8** (kind: clause)
  - label: Σ-A8 Isomorphism invariance
  - Extra fields:
    ```yml
    label: Σ-A8 Isomorphism invariance
    status: normative
    text: 'If a frame π induces a structure-preserving isomorphism on representation, decisions
      are invariant.

      '
    ```
- **clause.charter** (kind: clause)
  - label: Charter
  - Extra fields:
    ```yml
    label: Charter
    status: normative
    text: 'Σ specifies a contract-shaped kernel that produces decisions from posted evidence under
      benign variation, with replayable records, without making domain assumptions.

      '
    ```
- **clause.conformance** (kind: clause)
  - label: Σ-lawful record checklist
  - Extra fields:
    ```yml
    label: Σ-lawful record checklist
    status: normative
    text: 'A record κ ∈ R is Σ-lawful iff it includes: (1) contract (Θ, β, C, Π, P_n, Γ and guards),
      (2) valuation v(u) (decision-relevant coords), (3) decision χ(v(u), Θ, β) with reasons,
      (4) invariance evidence (wobble metrics + worst-case (π,p)), (5) reflexive warrant (v''(u)
      and agreement), (6) canonicalization: canonical bytes, digest d, and optional chain root.

      '
    ```
- **clause.metrics_orders** (kind: clause)
  - label: Wobble and orderings
  - Extra fields:
    ```yml
    label: Wobble and orderings
    status: normative
    text: 'Σ assumes a divergence ("wobble") w: V × V → R_{≥0} on decision-relevant coordinates.
      Orders: θ ⪯ θ'' means tightening floors; β'' ⪯ β means tightening budgets; C'' ⪯ C means
      shrinking capacity.

      '
    ```
- **clause.morphism.eq** (kind: clause)
  - label: Morphism preservation
  - Extra fields:
    ```yml
    label: Morphism preservation
    status: normative
    text: 'A morphism preserves valuation and decision structure by satisfying: v'' ∘ φ_U = φ_V
      ∘ v, χ'' ∘ (φ_V × id) = χ. It also maps contract parameters monotonically and preserves
      Σ-A1..Σ-A7.

      '
    ```
- **clause.notes** (kind: clause)
  - label: Notes
  - Extra fields:
    ```yml
    label: Notes
    status: informative
    text: 'This specification does not fix what v measures, what χ decides, or how w is computed.
      It only requires posting, invariance under benign variation, minimal sufficiency under capacity,
      and reflexive reproducibility. Evidence Systemics is one instantiation where v encodes evidence
      gauges; other instances (Control, Protocol, Risk, Learning, etc.) keep the same Σ contract
      while choosing different v, Θ, β.

      '
    ```
- **clause.recipe** (kind: clause)
  - label: Recipe
  - Extra fields:
    ```yml
    label: Recipe
    status: informative
    text: 'Choose U,V,v,χ; post Θ,β,C,Π,P_n,Γ and wobble metric w; establish Σ-A1..Σ-A7 by construction/tests;
      emit lawful κ and optionally chain pages into books.

      '
    ```
- **property.alphabet** (kind: property)
  - label: Alphabet
  - Extra fields:
    ```yml
    label: Alphabet
    status: normative
    symbols:
    - desc: universe of artifacts
      sym: U
    - desc: valuation space (any measurable space; commonly R^k × B^m)
      sym: V
    - desc: decision space 2 := {0,1}
      sym: '2'
    - desc: frames / benign contexts
      sym: Π
    - desc: probes / benign perturbations
      sym: P_n
    - desc: floors/thresholds (partially ordered set)
      sym: Θ
    - desc: invariance budgets (tolerances in a poset/lattice)
      sym: β
    - desc: capacity budgets (bits/time/energy constraints)
      sym: C
    - desc: envelope/meta (versions, seeds, numeric modes, commits)
      sym: Γ
    - desc: records (canonical map → bytes; hash/ledger optional)
      sym: R
    ```
- **ref.gf0** (kind: spec_ref)
  - label: GraphFrame K0 (GF0)
  - Extra fields:
    ```yml
    label: GraphFrame K0 (GF0)
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    ```
- **ref.sigma.composition** (kind: spec_ref)
  - label: Σ Composition (separate spec)
  - Extra fields:
    ```yml
    label: Σ Composition (separate spec)
    status: informative
    target_graph_id: spec://domains/systemics/sigma-composition-k1
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
- **section.2.alphabet** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Alphabet (Objects & Maps)
    ```
- **section.3.kernel** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: 'Definition: Systemic Kernel'
    ```
- **section.4.metrics_orders** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: Metrics & Order
    ```
- **section.5.axioms** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: Axioms (Minimal Core)
    ```
- **section.6.conformance** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: normative
    title: Conformance (Lawful Record)
    ```
- **section.7.morphisms** (kind: section)
  - Extra fields:
    ```yml
    order: 7
    status: normative
    title: Morphisms of Systemics
    ```
- **section.8.recipe** (kind: section)
  - Extra fields:
    ```yml
    order: 8
    status: informative
    title: Instantiation Recipe (Domain-Agnostic)
    ```
- **section.9.notes** (kind: section)
  - Extra fields:
    ```yml
    order: 9
    status: informative
    title: Notes
    ```
- **spec://domains/systemics/sigma-k1** (kind: spec)
  - attrs:
    | key | value | vtype | desc |
    | --- | --- | --- | --- |
    | doc.title | Systemics Σ — Minimal Specification (K1) |  |  |
    | doc.authors | ["David Swanson"] | json |  |
    | doc.created | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.updated | 2026-01-04T00:00:00-06:00 | rfc3339 |  |
    | doc.license | CC-BY-4.0 | spdx |  |
    | doc.tags | ["systemics","sigma","spec"] | json |  |
  - Extra fields:
    ```yml
    profile: specframe-k1
    status: normative
    summary: 'Domain-agnostic minimal specification of Systemics Σ: alphabet, systemic kernel
      tuple, metrics/orders, axioms Σ-A1..Σ-A8, conformance (lawful record), morphisms, and an
      instantiation recipe.

      '
    title: Systemics Σ — Minimal Specification (K1)
    ```
- **term.morphism** (kind: term)
  - label: Morphism F: Σ → Σ'
  - Extra fields:
    ```yml
    label: 'Morphism F: Σ → Σ'''
    status: normative
    summary: 'A morphism F: Σ → Σ'' is a pair (φ_U, φ_V) such that the following commutation laws
      hold: v'' ∘ φ_U = φ_V ∘ v, and χ'' ∘ (φ_V × id) = χ. A morphism also maps contracts monotonically
      so that Σ axioms remain satisfied.

      '
    ```
- **term.systemic_kernel** (kind: term)
  - label: Systemic Kernel
  - Extra fields:
    ```yml
    label: Systemic Kernel
    status: normative
    summary: 'A systemic kernel is the tuple: K^Σ_μ := (v, χ, Π, P_n, Θ, β, C, Γ), where v: U
      → V and χ: V × Θ × β → 2.

      '
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| section.1.charter | clause.charter | contains |  |  |  |
| section.2.alphabet | property.alphabet | contains |  |  |  |
| section.3.kernel | term.systemic_kernel | contains |  |  |  |
| section.4.metrics_orders | clause.metrics_orders | contains |  |  |  |
| section.5.axioms | clause.a1 | contains |  |  |  |
| section.5.axioms | clause.a2 | contains |  |  |  |
| section.5.axioms | clause.a3 | contains |  |  |  |
| section.5.axioms | clause.a4 | contains |  |  |  |
| section.5.axioms | clause.a5 | contains |  |  |  |
| section.5.axioms | clause.a6 | contains |  |  |  |
| section.5.axioms | clause.a7 | contains |  |  |  |
| section.5.axioms | clause.a8 | contains |  |  |  |
| section.6.conformance | clause.conformance | contains |  |  |  |
| section.7.morphisms | clause.morphism.eq | contains |  |  |  |
| section.7.morphisms | term.morphism | contains |  |  |  |
| section.8.recipe | clause.recipe | contains |  |  |  |
| section.9.notes | clause.notes | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | ref.gf0 | depends_on |  |  |  |
| spec://domains/systemics/sigma-k1 | ref.sigma.composition | refers_to |  |  |  |
| spec://domains/systemics/sigma-k1 | ref.specframe | depends_on |  |  |  |
| spec://domains/systemics/sigma-k1 | section.1.charter | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.2.alphabet | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.3.kernel | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.4.metrics_orders | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.5.axioms | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.6.conformance | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.7.morphisms | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.8.recipe | contains |  |  |  |
| spec://domains/systemics/sigma-k1 | section.9.notes | contains |  |  |  |

## Contains Tree
- spec://domains/systemics/sigma-k1
  - section.1.charter
    - clause.charter
  - section.2.alphabet
    - property.alphabet
  - section.3.kernel
    - term.systemic_kernel
  - section.4.metrics_orders
    - clause.metrics_orders
  - section.5.axioms
    - clause.a1
    - clause.a2
    - clause.a3
    - clause.a4
    - clause.a5
    - clause.a6
    - clause.a7
    - clause.a8
  - section.6.conformance
    - clause.conformance
  - section.7.morphisms
    - clause.morphism.eq
    - term.morphism
  - section.8.recipe
    - clause.recipe
  - section.9.notes
    - clause.notes
