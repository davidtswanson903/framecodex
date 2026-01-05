# DocProfiles K1 — Document Profile Registry
<a id="spec-kernel-docs-docprofiles-k1-94593c23"></a>

## Overview
<a id="section-1-overview-80ccecc5"></a>

**intent** _(normative)_

`DocProfile`s are conventions layered on SpecFrame K1 to support consistent
authoring, deterministic rendering, and automated linting across many document types.

## Core Model
<a id="section-2-core-model-fd724e9a"></a>

**doc\_profile** _(normative)_


**ProfileId** _(normative)_


**ProfileRule** _(normative)_


**frame-metadata** _(informative)_

Frame-level tags such as `domain`, `depends_on`, and publishing hints **SHOULD** be stored
in `GraphFrameK0.attrs`. `MetaGraph`s are reserved for auxiliary structural subgraphs
(indexes/layout/nav) per GF0.

**profile-location** _(normative)_

A document selects a `DocProfile` by providing `doc_profile` as an attribute on
the root `spec` node (`id == graph_id`). Tooling **MAY** ignore unknown `doc_profile` values.

**profile-semantics** _(normative)_

A `doc_profile` **MUST NOT** change the underlying SpecFrame K1 validity rules.
It only adds conventions (required/recommended content and lint/render expectations).

## Profile Catalog
<a id="section-3-profile-catalog-caf7f658"></a>

**guide-k1** _(normative)_


**required\_properties** _(informative)_

**hardware\_spec-k1** _(normative)_


**required\_sections** _(normative)_

**math\_theory-k1** _(normative)_


**conventions** _(informative)_

**playbook-k1** _(normative)_


**software\_spec-k1** _(normative)_


**required\_properties** _(informative)_

**required\_sections** _(normative)_

**standard-k1** _(normative)_


**required\_properties** _(informative)_

**required\_sections** _(normative)_

## Lint Rules
<a id="section-4-lint-rules-2432e0a9"></a>

**lint-baseline** _(informative)_

Tooling **SHOULD** lint for: 1. all normative nodes reachable from the spec root via `contains` 2. stable ordering (`section.order` then lexical fallback) 3. valid edge types and node kinds

## Rendering Hints
<a id="section-5-rendering-hints-1ccc34d2"></a>

**render-baseline** _(informative)_

Rendering is implementation-defined but **SHOULD** be deterministic: same input graph → same output files.
Common render products: per-spec README, per-section pages, glossary from `term` nodes, and backlinks from refs.

## Examples
<a id="section-6-examples-8c29c76a"></a>

## References
<a id="refs-e812cd2d"></a>

- GraphFrame GF0 ()
- SpecFrame K1 ()
