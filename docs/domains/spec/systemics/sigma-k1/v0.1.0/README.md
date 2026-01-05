# spec://domains/systemics/sigma-k1
- version: 0.1.0
- nodes: 28
- edges: 27
- meta: 0
## Nodes
- **clause.a1** (kind: clause)
  - label: Σ-A1 Well-typedness
  - Extra fields:
    ```yml
    label: Σ-A1 Well-typedness
    status: normative
    text: 'All maps are well-defined (measurable/continuous as needed); χ is total on V×Θ×β.

      '
    ```
- **clause.a2** (kind: clause)
  - label: Σ-A2 Posting / Records-only
  - Extra fields:
    ```yml
    label: Σ-A2 Posting / Records-only
    status: normative
    text: 'For any run on u∈U, the record κ∈R includes (v(u), Θ, β, C, Π, P_n, Γ), and the decision
      depends only on posted data: χ*(u;κ)=χ(v(u),Θ,β).

      '
    ```
- **clause.a3** (kind: clause)
  - label: Σ-A3 Benign invariance
  - Extra fields:
    ```yml
    label: Σ-A3 Benign invariance
    status: normative
    text: 'Under benign frame/probe variations (π,p)∈Π×P_n producing v_{π,p}(u), if worst-case
      wobble W(u) is within β then decisions are invariant across those variations.

      '
    ```
- **clause.a4** (kind: clause)
  - label: Σ-A4 Minimal sufficiency under capacity
  - Extra fields:
    ```yml
    label: Σ-A4 Minimal sufficiency under capacity
    status: normative
    text: 'Among valuations that preserve decisions under posted (Θ,β), v is minimal with respect
      to capacity cost subject to C.

      '
    ```
- **clause.a5** (kind: clause)
  - label: Σ-A5 Reflexive reproducibility
  - Extra fields:
    ```yml
    label: Σ-A5 Reflexive reproducibility
    status: normative
    text: 'There exists an independently realized valuation v'' (different numeric route/implementation)
      such that χ(v(u),Θ,β)=χ(v''(u),Θ,β), with both posted in κ (self-warrant).

      '
    ```
- **clause.a6** (kind: clause)
  - label: Σ-A6 Determinism & idempotence
  - Extra fields:
    ```yml
    label: Σ-A6 Determinism & idempotence
    status: normative
    text: 'For fixed (v(u),Θ,β), χ yields a unique decision and is idempotent under re-evaluation.

      '
    ```
- **clause.a7** (kind: clause)
  - label: Σ-A7 Monotonicity
  - Extra fields:
    ```yml
    label: Σ-A7 Monotonicity
    status: normative
    text: 'Tightening floors or budgets cannot rescue a failure by hidden dependence: tightening
      cannot create a pass that relies on unposted slack.

      '
    ```
- **clause.a8** (kind: clause)
  - label: Σ-A8 Isomorphism invariance
  - Extra fields:
    ```yml
    label: Σ-A8 Isomorphism invariance
    status: normative
    text: 'If a frame induces a structure-preserving isomorphism of representation, decisions
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
    text: 'A record κ∈R is Σ-lawful iff it includes: (1) contract (Θ,β,C,Π,P_n,Γ and guards),
      (2) valuation v(u) (decision-relevant coords), (3) decision χ(v(u),Θ,β) with reasons, (4)
      invariance evidence (wobble metrics + worst-case (π,p)), (5) reflexive warrant (v''(u) and
      agreement), (6) canonicalization bytes/digest and optional chaining root.

      '
    ```
- **clause.metrics_orders** (kind: clause)
  - label: Wobble and orderings
  - Extra fields:
    ```yml
    label: Wobble and orderings
    status: normative
    text: 'Σ assumes a divergence / wobble metric w: V×V→R_{≥0} on decision-relevant coordinates,
      and partial orders expressing tightening floors, tightening budgets, and shrinking capacity.

      '
    ```
- **clause.morphism.eq** (kind: clause)
  - label: Morphism preservation
  - Extra fields:
    ```yml
    label: Morphism preservation
    status: normative
    text: 'Morphisms preserve valuation/decision structure (up to φ mappings) and map contract
      parameters monotonically, preserving Σ-A1..Σ-A7.

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
    - desc: valuation space (measurable space)
      sym: V
    - desc: decision space {0,1}
      sym: '2'
    - desc: frames / benign contexts
      sym: Π
    - desc: probes / benign perturbations
      sym: P_n
    - desc: floors/thresholds (poset)
      sym: Θ
    - desc: invariance budgets (tolerances)
      sym: β
    - desc: capacity budgets (bits/time/energy)
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
    summary: 'A morphism is a pair (φ_U, φ_V) preserving valuation/decision structure and mapping
      contracts monotonically so that Σ axioms remain satisfied.

      '
    ```
- **term.systemic_kernel** (kind: term)
  - label: Systemic Kernel
  - Extra fields:
    ```yml
    label: Systemic Kernel
    status: normative
    summary: 'A systemic kernel is K^Σ_μ = (v, χ, Π, P_n, Θ, β, C, Γ) where v:U→V is a valuation
      map and χ:V×Θ×β→2 is a decision gate.

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
