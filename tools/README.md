# Tools

Bootstrap deterministic tools to satisfy RepoLaw K1 CI gate structure:

- `tools/validate_group/run`
- `tools/enforce_repo_law/run`
- `tools/validate_references/run`
- `tools/render_docs/run` (renders `docs/` deterministically)
- `tools/no_diff/run`

Additional deterministic renderer:

- `tools/render_simple_md/run` — renders each in-repo frame to `docs/<frameurl_path>/v<version>/README.md`.
