# GF0 Frames Repo (bootstrapped)

This repository is bootstrapped to conform to:

- `law://repo/governance/repo-law-k1` (Repo structure, DocGroup selection, CI gates)
- `law://_kernel/id/frameurl-k1` (canonical FrameURL IDs and file projection)

## Key paths

- `frames/` — canonical GF0 frames (source of truth)
- `governance/ACTIVE.yml` — selects the active law/profile pointers
- `ci/contract.yml` — minimal CI gates contract
- `out/` — build artifacts (must be gitignored)
- `docs/` — rendered docs outputs (committed when output_mode=commit_docs)
