# Systemics — Kernel Axiom K0 (K1)
<a id="spec-domains-systemics-k0-k1-7030db39"></a>

## Definitions
<a id="section-1-definitions-9169a94c"></a>

**Kernel** _(normative)_

A kernel is a tuple K=(S,I,O,B,E,F) with admissible transitions (s_in, i, b_in, s_out, o, b_out, e) ∈ F.

**Kernel Tuple Fields** _(normative)_

## Axiom K0
<a id="section-2-axiom-1b1ec435"></a>

**Axiom K0 (Kernel axiom)** _(normative)_

Every system of interest decomposes into a finite collection of kernels {K_i} satisfying K1–K4.

**K1 Records-first** _(normative)_

Each kernel application emits a receipt e ∈ E sufficient to later reconstruct and audit the transition.

**K2 Replayability** _(normative)_

There exists a (possibly partial) replay operator R that, given an initial state and a sequence of receipts, reconstructs final state and outputs.

**K3 Budgeted behavior** _(normative)_

Transitions respect budgets: b_out ⪯ b_in for a well-founded preorder ⪯ on B.

**K4 Composability** _(normative)_

Kernels compose along interfaces to form larger systems without breaking records-first behavior.

## Notes
<a id="section-3-notes-608a515f"></a>

**Domain-agnostic** _(informative)_

K0 does not constrain domain: kernels may represent software, human workflows, simulation steps, or hybrid configurations.

## References
<a id="refs-e812cd2d"></a>

- GraphFrame K0 (GF0) ()
- SpecFrame K1 ()
