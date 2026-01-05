# Systemics Σ — Minimal Specification (K1)
<a id="spec-domains-systemics-sigma-k1-9c0dca86"></a>

## Charter
<a id="section-1-charter-6790fc7e"></a>

**Charter** _(normative)_

Σ specifies a contract-shaped kernel that produces decisions from posted evidence under benign variation, with replayable records, without making domain assumptions.

## Alphabet (Objects & Maps)
<a id="section-2-alphabet-2d2e0ec0"></a>

**Alphabet** _(normative)_

- `U`: universe of artifacts
- `V`: valuation space (any measurable space; commonly R^k × B^m)
- `2`: decision space 2 := {0,1}
- `Π`: frames / benign contexts
- `P_n`: probes / benign perturbations
- `Θ`: floors/thresholds (partially ordered set)
- `β`: invariance budgets (tolerances in a poset/lattice)
- `C`: capacity budgets (bits/time/energy constraints)
- `Γ`: envelope/meta (versions, seeds, numeric modes, commits)
- `R`: records (canonical map → bytes; hash/ledger optional)

## Definition: Systemic Kernel
<a id="section-3-kernel-706b1977"></a>

**Systemic Kernel** _(normative)_

A systemic kernel is the tuple: K^Σ_μ := (v, χ, Π, P_n, Θ, β, C, Γ), where v: U → V and χ: V × Θ × β → 2.

## Metrics & Order
<a id="section-4-metrics-orders-c4fd82d3"></a>

**Wobble and orderings** _(normative)_

Σ assumes a divergence ("wobble") w: V × V → R_{≥0} on decision-relevant coordinates. Orders: θ ⪯ θ' means tightening floors; β' ⪯ β means tightening budgets; C' ⪯ C means shrinking capacity.

## Axioms (Minimal Core)
<a id="section-5-axioms-15c13760"></a>

**Σ-A1 Well-typedness** _(normative)_

All maps are measurable/continuous as needed; χ is total on V × Θ × β.

**Σ-A2 Posting / Records-only** _(normative)_

For any run on u ∈ U, the record κ ∈ R contains (v(u), Θ, β, C, Π, P_n, Γ), and the decision equals χ*(u; κ) = χ(v(u), Θ, β), with no dependence on unposted data.

**Σ-A3 Benign invariance** _(normative)_

Let (π,p) ∈ Π × P_n act on the measurement/evaluation pathway to yield v_{π,p}(u). Define W(u) := sup_{(π,p)} w(v_{π,p}(u), v_{π0,p0}(u)). If W(u) ⪯ β then for all benign (π,p), χ(v_{π,p}(u), Θ, β) = χ(v_{π0,p0}(u), Θ, β).

**Σ-A4 Minimal sufficiency under capacity** _(normative)_

Among valuations preserving decisions under posted (Θ, β), v is minimal w.r.t. capacity cost subject to C: for all v', (χ ∘ v' = χ ∘ v) ⇒ cost(v') ⪰ cost(v), subject to C.

**Σ-A5 Reflexive reproducibility** _(normative)_

There exists an admissible, independently realized v' (different numeric/route) such that χ(v(u), Θ, β) = χ(v'(u), Θ, β), with both posted in κ (self-warrant).

**Σ-A6 Determinism & idempotence** _(normative)_

For fixed (v(u), Θ, β), the decision χ is unique and idempotent under re-evaluation.

**Σ-A7 Monotonicity** _(normative)_

Tightening floors or budgets cannot rescue a failure by hidden dependence. For θ ⪯ θ' and β' ⪯ β, χ(v, θ, β) = 1 implies χ(v, θ', β') ∈ {0,1} with no hidden rescue: tightening must not create a pass whose justification depends on data not posted in the record.

**Σ-A8 Isomorphism invariance** _(normative)_

If a frame π induces a structure-preserving isomorphism on representation, decisions are invariant.

## Conformance (Lawful Record)
<a id="section-6-conformance-4e35257c"></a>

**Σ-lawful record checklist** _(normative)_

A record κ ∈ R is Σ-lawful iff it includes: (1) contract (Θ, β, C, Π, P_n, Γ and guards), (2) valuation v(u) (decision-relevant coords), (3) decision χ(v(u), Θ, β) with reasons, (4) invariance evidence (wobble metrics + worst-case (π,p)), (5) reflexive warrant (v'(u) and agreement), (6) canonicalization: canonical bytes, digest d, and optional chain root.

## Morphisms of Systemics
<a id="section-7-morphisms-6f87b55c"></a>

**Morphism F: Σ → Σ'** _(normative)_

A morphism F: Σ → Σ' is a pair (φ_U, φ_V) such that the following commutation laws hold: v' ∘ φ_U = φ_V ∘ v, and χ' ∘ (φ_V × id) = χ. A morphism also maps contracts monotonically so that Σ axioms remain satisfied.

**Morphism preservation** _(normative)_

A morphism preserves valuation and decision structure by satisfying: v' ∘ φ_U = φ_V ∘ v, χ' ∘ (φ_V × id) = χ. It also maps contract parameters monotonically and preserves Σ-A1..Σ-A7.

## Instantiation Recipe (Domain-Agnostic)
<a id="section-8-recipe-2801220f"></a>

**Recipe** _(informative)_

Choose U,V,v,χ; post Θ,β,C,Π,P_n,Γ and wobble metric w; establish Σ-A1..Σ-A7 by construction/tests; emit lawful κ and optionally chain pages into books.

## Notes
<a id="section-9-notes-88cf718d"></a>

**Notes** _(informative)_

This specification does not fix what v measures, what χ decides, or how w is computed. It only requires posting, invariance under benign variation, minimal sufficiency under capacity, and reflexive reproducibility. Evidence Systemics is one instantiation where v encodes evidence gauges; other instances (Control, Protocol, Risk, Learning, etc.) keep the same Σ contract while choosing different v, Θ, β.

## References
<a id="refs-e812cd2d"></a>

- GraphFrame K0 (GF0) ()
- SpecFrame K1 ()
- Σ Composition (separate spec) ()
