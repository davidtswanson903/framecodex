# Systemics Σ — Composition (K1)
<a id="spec-domains-systemics-sigma-composition-k1-28f7befd"></a>

## Charter
<a id="section-1-charter-6790fc7e"></a>

**Charter** _(normative)_

This spec defines how lawful Σ kernels compose in serial, parallel, and temporal forms, preserving Σ lawfulness via posted adapters/combinators and monotone contract combination.

## Serial Composition
<a id="section-2-serial-2bd4b5bb"></a>

**Posted adapter requirement** _(normative)_

For serial composition with K1^Σ = (v1, χ1, …) and K2^Σ = (v2, χ2, …), any adapter f used to produce the second valuation MUST be posted as part of the record/contract. In particular, if v2 is defined from u and the upstream decision by: v2(u) = f(u, χ1(v1(u), Θ1, β1)), then f MUST be included in posted data so downstream decisions remain records-only.

**Monotone contract combination** _(normative)_

The composite kernel K2 ∘ K1 is lawful only if (Σ-A1 … Σ-A7) hold for the composite and if the combined contracts (Θ, β, C) are formed via a monotone operator ⊕ (domain-chosen), i.e. tightening in any component must not rely on hidden slack.

## Parallel / Product Composition
<a id="section-3-parallel-3cf76437"></a>

**Posted decision combinator** _(normative)_

For parallel/product composition K1 ⊗ K2, both kernels evaluate and decisions are aggregated via a posted combinator comb: 2 × 2 → 2 (e.g., AND/OR). The choice of comb MUST be posted as part of the record/contract.

**Monotone floors/budgets** _(normative)_

Floors and budgets for parallel composition MUST be combined monotonically (tightening cannot rely on hidden slack).

## Temporal Composition (window → page → book)
<a id="section-4-temporal-95a10ed1"></a>

**Pages and books** _(normative)_

A page is a lawful record κ for one window. A book is an ordered sequence of pages; optionally, pages may be hash-chained. Chaining preserves replay and does not alter decisions.

## Composition Invariants
<a id="section-5-invariants-b60be1d8"></a>

**Records-only preserved** _(normative)_

Composition MUST preserve Σ-A2 (records-only): any dependency introduced by composition must be posted.

**Replay preserved** _(normative)_

Composition MUST preserve reflexive reproducibility and replayability obligations implied by the Σ contract.

## References
<a id="refs-e812cd2d"></a>

- GraphFrame K0 (GF0) (spec://\_kernel/gf/gf0-k1)
- SpecFrame K1 (spec://\_kernel/spec/specframe-k1)
- Systemics Σ — Minimal Specification (spec://domains/systemics/sigma-k1)
