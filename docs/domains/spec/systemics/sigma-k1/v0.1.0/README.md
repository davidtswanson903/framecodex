# Systemics $\\Sigma$ --- Minimal Specification
<a id="spec-domains-systemics-sigma-k1-9c0dca86"></a>

## Charter
<a id="section-1-charter-6790fc7e"></a>

**Charter** _(normative)_

This document gives a domain-agnostic, minimal formal specification of Systemics $\\Sigma$. It treats any practice as a kernel-shaped contract that produces decisions from posted evidence under benign variation, with replayable records. No specific domain assumptions (physics, ML, audits, etc.) are required.

## Alphabet (Objects & Maps)
<a id="section-2-alphabet-2d2e0ec0"></a>

**Alphabet** _(normative)_

- `U`: Universe of artifacts.
- `\\mathbb{V}`: Valuation space (any measurable space; commonly \\mathbb{R}^k \\times \\mathbb{B}^m).
- `\\mathbf{2}`: Decision space \\mathbf{2} = {0,1}.
- `\\Pi`: Frames (benign contexts).
- `P\_n`: Probes (benign perturbations).
- `\\Theta`: Floors/thresholds (partially ordered set).
- `\\beta`: Invariance budgets (tolerances in a poset/lattice).
- `C`: Capacity budgets (bits/time/energy constraints).
- `\\Gamma`: Envelope/meta (versions, seeds, numeric modes, commits).
- `\\mathcal{R}`: Records (canonical map \\to bytes; hash/ledger optional).

## Definition: Systemic Kernel
<a id="section-3-kernel-706b1977"></a>

**Systemic Kernel** _(normative)_

A systemic kernel is the tuple
\begin{equation}
  K_\mu^\Sigma \;=\; \big(v,\, \chi,\, \Pi,\, P_n,\, \Theta,\, \beta,\, C,\, \Gamma\big),
\end{equation}
where $v:U\to \mathbb{V}$ is a valuation map and $\chi:\mathbb{V}\times\Theta\times\beta\to \mathbf{2}$ is a decision gate.

## Metrics & Order
<a id="section-4-metrics-orders-c4fd82d3"></a>

**Wobble and orderings** _(normative)_

\\begin{itemize}
  \\item A divergence ("wobble") $w:\\mathbb{V}\\times\\mathbb{V}\\to \\mathbb{R}\_{\\ge 0}$ on decision-relevant coordinates.
  \\item Orders: $\\theta\\preceq \\theta'$ means tightening floors; $\\beta'\\preceq\\beta'$ means loosening invariance budgets; $C'\\preceq C$ means reduced capacity.
  \\item Metrics: $\\rho$ is a metric on the decision space (e.g., $\\mathbb{R}\_{\\ge 0}$ for costs, $\\mathbf{2}$ for errors).
  \\item A (pseudo-)distance on systemic kernels is $d\_\\mu(K,K')=\\rho(v,v')+\\theta(\\chi,\\chi')+\\beta(C,C')$.
\\end{itemize}

## Axioms
<a id="section-5-axioms-15c13760"></a>

**Axiom 1: Existence of Valuation** _(normative)_

$\\forall u:U, \\exists! v:V, \\mathrm{val}(u,v)$.

**Axiom 2: Universal Decision Gate** _(normative)_

$\\forall \\theta:\\Theta, \\exists \\chi:\\mathbb{V}\\times\\Theta\\times\\beta\\to \\mathbf{2}, \\mathrm{gate}(\\chi,\\theta)$.

**Axiom 3: Invariance under Reparameterization** _(normative)_

If $\\beta' \\preceq \\beta$ and $\\theta' \\preceq \\theta$, then $\\chi'(\\cdot,\\theta')$ is equivalent to $\\chi(\\cdot,\\theta)$.

**Axiom 4: Capacity Constraints** _(normative)_

$\\forall t, \\exists c:C, \\mathrm{cap}(t,c)$.

**Axiom 5: Envelope Uniqueness** _(normative)_

If $\\gamma:\\mathcal{R}$ is a record, then $\\exists! \\mu:\\Gamma, \\mathrm{envelope}(\\mu,\\gamma)$.

**Axiom 6: Record-keeping** _(normative)_

$\\forall r:\\mathcal{R}, \\exists e:U\\to \\mathbb{V}, \\mathrm{record}(r,e)$.

**Axiom 7: Bounded Wobble** _(normative)_

$\\forall v,v':V, w(v,v')<\\infty$.

**Axiom 8: Tightening Floors** _(normative)_

$\\forall \\theta,\\theta':\\Theta, \\theta\\preceq\\theta' \\Rightarrow \\chi(\\cdot,\\theta')\\preceq\\chi(\\cdot,\\theta)$.

## Conformance
<a id="section-6-conformance-4e35257c"></a>

**Conformance** _(normative)_

A systemic kernel $K$ conforms to a contract $C$ if $\\forall t, \\mathrm{exec}(K,t) \\in C$.

## Morphisms
<a id="section-7-morphisms-6f87b55c"></a>

**Morphism** _(normative)_

A morphism between systemic kernels $K,K'$ is a tuple
\begin{equation}
  f = \big(f_v, f_\chi, f_\beta, f_C, f_\Gamma\big),
\end{equation}
where - $f_v:V\to V'$ is a valuation map, - $f_\chi:\mathbb{V}\times\Theta\times\beta\to \mathbb{V}'\times\Theta'\times\beta'$ is a compatible decision map, - $f_\beta:\beta\to\beta'$ and $f_C:C\to C'$ are invariance and capacity transformations, - $f_\Gamma:\Gamma\to\Gamma'$ is an envelope transformation.

**Equivalence of Morphisms** _(normative)_

Morphisms $f$ and $g$ are equivalent, written $f\\approx g$, if
\\begin{itemize}
  \\item $f\_v=g\_v$,
  \\item $f\_\\chi$ and $g\_\\chi$ are equivalent decision maps,
  \\item $f\_\\beta=g\_\\beta$ and $f\_C=g\_C$,
  \\item $f\_\\Gamma=g\_\\Gamma$.
\\end{itemize}

## Recipe
<a id="section-8-recipe-2801220f"></a>

**Systemics $\\Sigma$ Recipe** _(normative)_

To specify a Systemics $\\Sigma$ instance:
\\begin{enumerate}
  \\item Select a universe $U$ of artifacts.
  \\item Define a valuation map $v:U\\to \\mathbb{V}$.
  \\item Specify decision-relevant coordinates using floors $\\theta$ and invariance budgets $\\beta$.
  \\item Define capacity budgets $C$.
  \\item Specify an envelope/meta description $\\mu$.
  \\item Define a decision gate $\\chi$.
\\end{enumerate}

## Notes
<a id="section-9-notes-88cf718d"></a>

**Notes** _(informative)_

\\begin{itemize}
  \\item See also the separate specification for Σ Composition.
  \\item This specification is a work in progress; see GitHub for updates.
\\end{itemize}

## References
<a id="refs-e812cd2d"></a>

- GraphFrame K0 (GF0) ()
- SpecFrame K1 ()
- Σ Composition (separate spec) ()
