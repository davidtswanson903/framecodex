# framecodex

A governed, deterministic **frame corpus** (GF0 / SpecFrame) with a **hybrid publication pipeline**:

- **Repo-level citation**: Zenodo archives GitHub Releases using `.zenodo.json`.
- **Doc-level artifacts**: selected “citable” specs are rendered (LaTeX → PDF) and published as reproducible artifacts (PDF + manifest).

## Start here

- **Human index**: see [`INDEX.md`](INDEX.md) for hyperlinks into frames, publications, and governance.
- **Citation**: see [`CITATION.cff`](CITATION.cff) (GitHub citation panel).
- **Zenodo metadata**: see [`.zenodo.json`](.zenodo.json).

## What’s in the repo

- `frames/` — source-of-truth frames (GF0 / SpecFrame YAML)
- `docs/` — human docs (not required for publication; may be used for narrative support)
- `governance/` — repo law, registries (incl. doc publication registry)
- `tools/` — validators + render/build tooling
- `pub/` — **build output** (CI artifacts / release assets / GitHub Pages); not committed
- `.github/workflows/` — CI pipelines (gates, pubs, releases)

## Publications

Rendered PDFs are published in two ways:

- **GitHub Pages** (branch `gh-pages`): built from `pub-docs`.
- **GitHub Releases**: version tags trigger auto-release + asset uploads.

Doc-level Zenodo deposits are tracked in `governance/publications/registry.yml` (records/DOIs to be filled after deposits).

## Release workflow (maintainers)

- Push a version tag `vX.Y.Z`.
- CI runs gates, builds publication artifacts, and creates a GitHub Release with attached assets.
- Zenodo (if configured) archives the GitHub Release for the repo-level DOI.

## Repo governance

This repo is governed by the active law/profile selected under `governance/`.
Core constraints include:

- deterministic structure + FrameURL IDs
- validation gates enforced in CI
- required publication metadata/files for releases
