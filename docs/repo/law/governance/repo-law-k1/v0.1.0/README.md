# law://repo/governance/repo-law-k1
- version: 0.1.0
- nodes: 60
- edges: 59
- meta: 0
## Nodes
- **def.active_pointer** (kind: definition)
  - label: Active Pointer
  - Extra fields:
    ```yml
    label: Active Pointer
    status: normative
    text: 'governance/ACTIVE.yml selects the active RepoLaw and (optionally) an active RepoProfile,
      by referencing FrameURLs and explicit versions.

      '
    ```
- **def.docgroup** (kind: definition)
  - label: DocGroup
  - Extra fields:
    ```yml
    label: DocGroup
    status: normative
    text: 'The set of frames considered authoritative inputs to validation and generation, selected
      deterministically from the repository according to section.4 rules.

      '
    ```
- **def.frame_file** (kind: definition)
  - label: FrameFile
  - Extra fields:
    ```yml
    label: FrameFile
    status: normative
    text: 'A file that contains exactly one GF0 graph. Under this repo law, canonical frames are
      stored as frame.yml at a path derived from (graph_id, version) per FrameURL K1.

      '
    ```
- **ex.active_yml** (kind: example)
  - label: governance/ACTIVE.yml
  - Extra fields:
    ```yml
    label: governance/ACTIVE.yml
    status: informative
    text: 'active_law: "law://repo/governance/repo-law-k1"

      active_law_version: "0.1.0"

      active_profile: "profile://repo/governance/default"

      active_profile_version: "0.1.0"

      '
    ```
- **ex.projected_path** (kind: example)
  - label: Projected frame path
  - Extra fields:
    ```yml
    label: Projected frame path
    status: informative
    text: 'graph_id: law://repo/governance/repo-law-k1

      version:  0.1.0

      path:     frames/repo/law/governance/repo-law-k1/v0.1.0/frame.yml

      '
    ```
- **law://repo/governance/repo-law-k1** (kind: law)
  - Extra fields:
    ```yml
    law_id: repo-law-k1
    law_version: 0.1.0
    profile: lawframe-k1
    status: normative
    summary: 'Governs the repository that stores GF0 frames (laws/specs/profiles/render plans/etc).
      Defines canonical folder structure, required files, DocGroup selection, CI gates, and enforcement
      rules. Uses FrameURL K1 for canonical graph_id and deterministic path projection.

      '
    title: RepoLaw K1 — Repository Structure, Frame Layout, and CI Gates
    ```
- **param.adapter_mode** (kind: parameter)
  - Extra fields:
    ```yml
    allowed:
    - none
    - github
    default: github
    key: adapter_mode
    status: normative
    ```
- **param.docgroup_include_fixtures** (kind: parameter)
  - Extra fields:
    ```yml
    allowed:
    - 'false'
    - 'true'
    default: 'false'
    key: docgroup_include_fixtures
    status: normative
    ```
- **param.frames_root** (kind: parameter)
  - Extra fields:
    ```yml
    allowed:
    - frames
    default: frames
    key: frames_root
    status: normative
    ```
- **param.index_mode** (kind: parameter)
  - Extra fields:
    ```yml
    allowed:
    - none
    - optional
    - required
    default: optional
    key: index_mode
    status: normative
    ```
- **param.output_mode** (kind: parameter)
  - Extra fields:
    ```yml
    allowed:
    - commit_docs
    - artifact_only
    default: commit_docs
    key: output_mode
    status: normative
    ```
- **prop.allowed_frame_schemes** (kind: property)
  - label: Allowed frame schemes (must match FrameURL K1)
  - Extra fields:
    ```yml
    label: Allowed frame schemes (must match FrameURL K1)
    status: normative
    values:
    - law
    - spec
    - profile
    - render
    - fixture
    ```
- **prop.allowed_root_paths** (kind: property)
  - label: Allowed repo root entries
  - Extra fields:
    ```yml
    label: Allowed repo root entries
    status: normative
    values:
    - frames/
    - governance/
    - tools/
    - ci/
    - docs/
    - out/
    - .github/
    - README.md
    - LICENSE
    - .gitignore
    ```
- **prop.forbidden_paths** (kind: property)
  - label: Forbidden paths
  - Extra fields:
    ```yml
    label: Forbidden paths
    status: normative
    values:
    - frames
    - out
    - docs
    ```
- **prop.frames_leaf_filename** (kind: property)
  - label: Canonical leaf filename for frames
  - Extra fields:
    ```yml
    label: Canonical leaf filename for frames
    status: normative
    value: frame.yml
    ```
- **prop.frames_version_prefix** (kind: property)
  - label: Canonical version folder prefix
  - Extra fields:
    ```yml
    label: Canonical version folder prefix
    status: normative
    value: v
    ```
- **prop.required_ci_gates** (kind: property)
  - label: Minimal required CI gates
  - Extra fields:
    ```yml
    label: Minimal required CI gates
    status: normative
    values:
    - validate_group
    - enforce_repo_law
    ```
- **prop.required_ci_gates_if_commit_docs** (kind: property)
  - label: Additional CI gates when output_mode=commit_docs
  - Extra fields:
    ```yml
    label: Additional CI gates when output_mode=commit_docs
    status: normative
    values:
    - render_docs
    - no_diff
    ```
- **prop.required_frames_scopes** (kind: property)
  - label: Required top-level scopes under frames/
  - Extra fields:
    ```yml
    label: Required top-level scopes under frames/
    status: normative
    values:
    - _kernel
    - repo
    - domains
    - projects
    ```
- **prop.required_paths** (kind: property)
  - label: Required paths
  - Extra fields:
    ```yml
    label: Required paths
    status: normative
    values:
    - frames/
    - governance/ACTIVE.yml
    - ci/contract.yml
    - tools/
    - out/
    - .gitignore
    - README.md
    - LICENSE
    ```
- **prop.required_paths_if_commit_docs** (kind: property)
  - label: Required paths when output_mode=commit_docs
  - Extra fields:
    ```yml
    label: Required paths when output_mode=commit_docs
    status: normative
    values:
    - docs/
    - docs/MANIFEST.json
    ```
- **prop.required_violation_codes** (kind: property)
  - label: Required RepoLaw violation codes
  - Extra fields:
    ```yml
    label: Required RepoLaw violation codes
    status: normative
    values:
    - REPO.E.MISSING_PATH
    - REPO.E.BAD_PATH_TYPE
    - REPO.E.OUT_NOT_IGNORED
    - REPO.E.BAD_FRAME_LEAF
    - REPO.E.UNVERSIONED_FRAME
    - REPO.E.DOCGROUP_DUP_GRAPH_ID
    - REPO.E.FRAME_PARSE_ERROR
    - REPO.E.ACTIVE_MISSING_KEYS
    - REPO.E.ACTIVE_UNRESOLVED_POINTER
    - REPO.E.PROFILE_WEAKENING
    - REPO.W.UNKNOWN_ROOT_ENTRY
    ```
- **ref.frameurl-k1** (kind: reference)
  - label: FrameURL K1
  - Extra fields:
    ```yml
    label: FrameURL K1
    status: informative
    target: law://_kernel/id/frameurl-k1
    ```
- **ref.validatorgroup-k1** (kind: reference)
  - label: ValidatorGroup K1
  - Extra fields:
    ```yml
    label: ValidatorGroup K1
    status: informative
    target: spec://_kernel/validator/validatorgroup-k1
    ```
- **rule.active.must_resolve** (kind: rule)
  - label: ACTIVE pointers must resolve
  - Extra fields:
    ```yml
    label: ACTIVE pointers must resolve
    modal: MUST
    status: normative
    text: 'ACTIVE.yml pointers MUST resolve to canonical frames present in DocGroup (by FrameURL
      and version). Unresolvable pointers are hard errors.

      '
    ```
- **rule.active.profile_nonweakening** (kind: rule)
  - label: Profiles must not weaken law
  - Extra fields:
    ```yml
    label: Profiles must not weaken law
    modal: MUST
    status: normative
    text: 'If an active profile is declared, it MUST NOT weaken or disable any RepoLaw MUST requirements.
      Any attempt to do so is a hard error.

      '
    ```
- **rule.active.required** (kind: rule)
  - label: ACTIVE.yml required
  - Extra fields:
    ```yml
    label: ACTIVE.yml required
    modal: MUST
    status: normative
    text: 'governance/ACTIVE.yml MUST exist and MUST declare active_law and active_law_version.
      It MAY declare active_profile and active_profile_version.

      '
    ```
- **rule.charter.frameurl_required** (kind: rule)
  - label: FrameURL required for canonical frames
  - Extra fields:
    ```yml
    label: FrameURL required for canonical frames
    modal: MUST
    status: normative
    text: 'All canonical frames in this repository MUST use FrameURL K1 as graph_id and MUST obey
      FrameURL K1 filesystem projection rules (graph_id+version -> frames/.../v<version>/frame.yml).

      '
    ```
- **rule.charter.offline_repo** (kind: rule)
  - label: Offline and self-contained
  - Extra fields:
    ```yml
    label: Offline and self-contained
    modal: MUST
    status: normative
    text: 'Validation and governance enforcement MUST be offline. The repository MUST contain
      all frames required to validate itself and MUST NOT require network fetch to resolve references.

      '
    ```
- **rule.charter.single_source_of_truth** (kind: rule)
  - label: frames/ is source of truth
  - Extra fields:
    ```yml
    label: frames/ is source of truth
    modal: MUST
    status: normative
    text: 'Canonical GF0 frames MUST live under frames/ and MUST NOT live outside frames/. Any
      GF0-like files outside frames/ are non-authoritative and MUST be ignored by DocGroup selection.

      '
    ```
- **rule.ci.enforce_repo_law** (kind: rule)
  - label: Gate: enforce_repo_law
  - Extra fields:
    ```yml
    label: 'Gate: enforce_repo_law'
    modal: MUST
    status: normative
    text: "enforce_repo_law MUST verify:\n  - required paths exist\n  - out/ is gitignored\n \
      \ - DocGroup selection matches rule.docgroup.scan_rule\n  - each frame obeys FrameURL K1\
      \ projected path\n  - ACTIVE.yml pointers resolve and do not weaken the law\n"
    ```
- **rule.ci.no_diff_if_commit** (kind: rule)
  - label: Gate: no_diff (conditional)
  - Extra fields:
    ```yml
    label: 'Gate: no_diff (conditional)'
    modal: MUST
    status: normative
    text: 'If output_mode == ''commit_docs'', no_diff MUST prove that the generated docs/ tree
      matches the committed docs/ tree exactly (byte-for-byte), excluding any explicitly law-permitted
      exceptions.

      '
    ```
- **rule.ci.render_docs_if_commit** (kind: rule)
  - label: Gate: render_docs (conditional)
  - Extra fields:
    ```yml
    label: 'Gate: render_docs (conditional)'
    modal: MUST
    status: normative
    text: 'If output_mode == ''commit_docs'', render_docs MUST deterministically generate docs/
      from DocGroup and the applicable RenderFrames, and MUST produce docs/MANIFEST.json.

      '
    ```
- **rule.ci.required_gates** (kind: rule)
  - label: Required CI gates
  - Extra fields:
    ```yml
    label: Required CI gates
    modal: MUST
    status: normative
    text: 'CI MUST run all gates listed in prop.required_ci_gates. If output_mode == ''commit_docs'',
      CI MUST also run all gates listed in prop.required_ci_gates_if_commit_docs.

      '
    ```
- **rule.ci.validate_group** (kind: rule)
  - label: Gate: validate_group
  - Extra fields:
    ```yml
    label: 'Gate: validate_group'
    modal: MUST
    status: normative
    text: 'validate_group MUST run the DocGroup validator (ValidatorGroup K1 or successor) and
      MUST produce a canonical ValidationReport artifact.

      '
    ```
- **rule.docgroup.parse_each_frame** (kind: rule)
  - label: Each frame parses as GF0
  - Extra fields:
    ```yml
    label: Each frame parses as GF0
    modal: MUST
    status: normative
    text: 'Each selected FrameFile MUST parse as exactly one GF0 graph and MUST pass GF0 structural
      validation prior to any higher-level profile validation.

      '
    ```
- **rule.docgroup.scan_rule** (kind: rule)
  - label: DocGroup scan rule
  - Extra fields:
    ```yml
    label: DocGroup scan rule
    modal: MUST
    status: normative
    text: "DocGroup MUST be selected deterministically as:\n  - all files named frame.yml under\
      \ frames/**/v*/frame.yml\n  - excluding frames/**/fixture/** unless docgroup_include_fixtures\
      \ == 'true'\nThe scan order MUST be lexicographic by relative path (bytewise) to ensure\
      \ stable behavior.\n"
    ```
- **rule.docgroup.unique_graph_id** (kind: rule)
  - label: graph_id uniqueness
  - Extra fields:
    ```yml
    label: graph_id uniqueness
    modal: MUST
    status: normative
    text: 'Within DocGroup, graph_id MUST be unique. Duplicate graph_id is a hard error.

      '
    ```
- **rule.frames.canonical_leaf** (kind: rule)
  - label: Canonical leaf filename
  - Extra fields:
    ```yml
    label: Canonical leaf filename
    modal: MUST
    status: normative
    text: 'Canonical frame files MUST be named prop.frames_leaf_filename (frame.yml) and MUST
      live under a version folder named prop.frames_version_prefix + <version> (e.g., v1.0.0).

      '
    ```
- **rule.frames.no_unversioned_frames** (kind: rule)
  - label: No unversioned canonical frames
  - Extra fields:
    ```yml
    label: No unversioned canonical frames
    modal: MUST
    status: normative
    text: 'No canonical frame.yml may exist under frames/ outside a v<version>/ directory.

      '
    ```
- **rule.frames.optional_indexes** (kind: rule)
  - label: Indexes
  - Extra fields:
    ```yml
    label: Indexes
    modal: MAY
    status: normative
    text: 'If index_mode is ''required'', each frames/<scope>/ subtree MUST include an index file
      (e.g., _index.yml) listing FrameURLs and paths. If index_mode is ''optional'', indexes may
      exist and MUST be treated as non-authoritative accelerators.

      '
    ```
- **rule.frames.projected_path_must_match** (kind: rule)
  - label: Projected path must match
  - Extra fields:
    ```yml
    label: Projected path must match
    modal: MUST
    status: normative
    text: 'Each canonical frame file path MUST equal the canonical projection derived from its
      (graph_id, version) under FrameURL K1. Mismatches are hard errors.

      '
    ```
- **rule.frames.scheme_folder_matches_graph_id** (kind: rule)
  - label: Scheme folder matches graph_id scheme
  - Extra fields:
    ```yml
    label: Scheme folder matches graph_id scheme
    modal: MUST
    status: normative
    text: 'The directory immediately under frames/<scope>/ MUST be the scheme (law/spec/profile/render/fixture)
      and MUST match the FrameURL scheme parsed from graph_id.

      '
    ```
- **rule.frames.scopes_exist** (kind: rule)
  - label: Required frames scopes
  - Extra fields:
    ```yml
    label: Required frames scopes
    modal: MUST
    status: normative
    text: 'frames/ MUST contain the scope directories listed in prop.required_frames_scopes.

      '
    ```
- **rule.manifest.docs** (kind: rule)
  - label: docs/MANIFEST.json (conditional)
  - Extra fields:
    ```yml
    label: docs/MANIFEST.json (conditional)
    modal: MUST
    status: normative
    text: "If output_mode == 'commit_docs', docs/MANIFEST.json MUST exist and MUST include, at\
      \ minimum:\n  - active law + profile pointers (FrameURL + version)\n  - inputs list (graph_id,\
      \ version, sha256)\n  - outputs list (path, sha256)\nThe manifest MUST be deterministic\
      \ and stable across implementations.\n"
    ```
- **rule.paths.allowed_root_entries** (kind: rule)
  - label: Allowed root entries
  - Extra fields:
    ```yml
    label: Allowed root entries
    modal: SHOULD
    status: normative
    text: 'The repository root SHOULD NOT contain entries outside prop.allowed_root_paths. Tooling
      MAY warn on unknown root entries, but the law does not forbid them unless explicitly listed.

      '
    ```
- **rule.paths.commit_docs_paths** (kind: rule)
  - label: Required docs paths if committing docs
  - Extra fields:
    ```yml
    label: Required docs paths if committing docs
    modal: MUST
    status: normative
    text: 'If output_mode == ''commit_docs'', the repository MUST contain all paths listed in
      prop.required_paths_if_commit_docs.

      '
    ```
- **rule.paths.out_gitignored** (kind: rule)
  - label: out/ is gitignored
  - Extra fields:
    ```yml
    label: out/ is gitignored
    modal: MUST
    status: normative
    text: 'out/ MUST be excluded from version control via .gitignore.

      '
    ```
- **rule.paths.required_paths** (kind: rule)
  - label: Required repo paths
  - Extra fields:
    ```yml
    label: Required repo paths
    modal: MUST
    status: normative
    text: 'The repository MUST contain all paths listed in prop.required_paths.

      '
    ```
- **rule.receipts.required_artifacts** (kind: rule)
  - label: Receipts
  - Extra fields:
    ```yml
    label: Receipts
    modal: SHOULD
    status: normative
    text: "Each CI gate SHOULD emit a receipt containing:\n  - ordered list of input (graph_id,\
      \ version, sha256 over canonical bytes)\n  - tool_id and tool_version\n  - ordered list\
      \ of output (path, sha256 over file bytes)\nReceipt serialization SHOULD be canonical (stable\
      \ key order, stable list order, LF newlines).\n"
    ```
- **rule.violations.stable** (kind: rule)
  - label: Stable violations
  - Extra fields:
    ```yml
    label: Stable violations
    modal: MUST
    status: normative
    text: 'Implementations claiming conformance to this RepoLaw MUST emit the codes listed in
      prop.required_violation_codes with stable semantics and deterministic ordering.

      '
    ```
- **section.1.charter** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Charter
    ```
- **section.2.paths** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: Canonical Repository Paths
    ```
- **section.3.frames_tree** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Frames Tree and Fractal Sharding
    ```
- **section.4.docgroup** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: DocGroup Selection
    ```
- **section.5.ci** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    status: normative
    title: CI Gates
    ```
- **section.6.receipts** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    status: normative
    title: Receipts and Manifests
    ```
- **section.7.violations** (kind: section)
  - Extra fields:
    ```yml
    order: 7
    status: normative
    title: Required Violation Codes
    ```
- **section.8.examples** (kind: section)
  - Extra fields:
    ```yml
    order: 8
    status: informative
    title: Examples
    ```
- **title.0** (kind: title)
  - Extra fields:
    ```yml
    status: normative
    text: RepoLaw K1
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| law://repo/governance/repo-law-k1 | ref.frameurl-k1 | contains |  |  |  |
| law://repo/governance/repo-law-k1 | ref.validatorgroup-k1 | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.1.charter | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.2.paths | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.3.frames_tree | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.4.docgroup | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.5.ci | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.6.receipts | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.7.violations | contains |  |  |  |
| law://repo/governance/repo-law-k1 | section.8.examples | contains |  |  |  |
| law://repo/governance/repo-law-k1 | title.0 | contains |  |  |  |
| section.1.charter | def.active_pointer | contains |  |  |  |
| section.1.charter | def.docgroup | contains |  |  |  |
| section.1.charter | def.frame_file | contains |  |  |  |
| section.1.charter | rule.charter.frameurl_required | contains |  |  |  |
| section.1.charter | rule.charter.offline_repo | contains |  |  |  |
| section.1.charter | rule.charter.single_source_of_truth | contains |  |  |  |
| section.2.paths | param.adapter_mode | contains |  |  |  |
| section.2.paths | param.frames_root | contains |  |  |  |
| section.2.paths | param.index_mode | contains |  |  |  |
| section.2.paths | param.output_mode | contains |  |  |  |
| section.2.paths | prop.allowed_root_paths | contains |  |  |  |
| section.2.paths | prop.forbidden_paths | contains |  |  |  |
| section.2.paths | prop.required_paths | contains |  |  |  |
| section.2.paths | prop.required_paths_if_commit_docs | contains |  |  |  |
| section.2.paths | rule.paths.allowed_root_entries | contains |  |  |  |
| section.2.paths | rule.paths.commit_docs_paths | contains |  |  |  |
| section.2.paths | rule.paths.out_gitignored | contains |  |  |  |
| section.2.paths | rule.paths.required_paths | contains |  |  |  |
| section.3.frames_tree | prop.allowed_frame_schemes | contains |  |  |  |
| section.3.frames_tree | prop.frames_leaf_filename | contains |  |  |  |
| section.3.frames_tree | prop.frames_version_prefix | contains |  |  |  |
| section.3.frames_tree | prop.required_frames_scopes | contains |  |  |  |
| section.3.frames_tree | rule.frames.canonical_leaf | contains |  |  |  |
| section.3.frames_tree | rule.frames.no_unversioned_frames | contains |  |  |  |
| section.3.frames_tree | rule.frames.optional_indexes | contains |  |  |  |
| section.3.frames_tree | rule.frames.projected_path_must_match | contains |  |  |  |
| section.3.frames_tree | rule.frames.scheme_folder_matches_graph_id | contains |  |  |  |
| section.3.frames_tree | rule.frames.scopes_exist | contains |  |  |  |
| section.4.docgroup | param.docgroup_include_fixtures | contains |  |  |  |
| section.4.docgroup | rule.active.must_resolve | contains |  |  |  |
| section.4.docgroup | rule.active.profile_nonweakening | contains |  |  |  |
| section.4.docgroup | rule.active.required | contains |  |  |  |
| section.4.docgroup | rule.docgroup.parse_each_frame | contains |  |  |  |
| section.4.docgroup | rule.docgroup.scan_rule | contains |  |  |  |
| section.4.docgroup | rule.docgroup.unique_graph_id | contains |  |  |  |
| section.5.ci | prop.required_ci_gates | contains |  |  |  |
| section.5.ci | prop.required_ci_gates_if_commit_docs | contains |  |  |  |
| section.5.ci | rule.ci.enforce_repo_law | contains |  |  |  |
| section.5.ci | rule.ci.no_diff_if_commit | contains |  |  |  |
| section.5.ci | rule.ci.render_docs_if_commit | contains |  |  |  |
| section.5.ci | rule.ci.required_gates | contains |  |  |  |
| section.5.ci | rule.ci.validate_group | contains |  |  |  |
| section.6.receipts | rule.manifest.docs | contains |  |  |  |
| section.6.receipts | rule.receipts.required_artifacts | contains |  |  |  |
| section.7.violations | prop.required_violation_codes | contains |  |  |  |
| section.7.violations | rule.violations.stable | contains |  |  |  |
| section.8.examples | ex.active_yml | contains |  |  |  |
| section.8.examples | ex.projected_path | contains |  |  |  |

## Contains Tree
- law://repo/governance/repo-law-k1
  - ref.frameurl-k1
  - ref.validatorgroup-k1
  - section.1.charter
    - def.active_pointer
    - def.docgroup
    - def.frame_file
    - rule.charter.frameurl_required
    - rule.charter.offline_repo
    - rule.charter.single_source_of_truth
  - section.2.paths
    - param.adapter_mode
    - param.frames_root
    - param.index_mode
    - param.output_mode
    - prop.allowed_root_paths
    - prop.forbidden_paths
    - prop.required_paths
    - prop.required_paths_if_commit_docs
    - rule.paths.allowed_root_entries
    - rule.paths.commit_docs_paths
    - rule.paths.out_gitignored
    - rule.paths.required_paths
  - section.3.frames_tree
    - prop.allowed_frame_schemes
    - prop.frames_leaf_filename
    - prop.frames_version_prefix
    - prop.required_frames_scopes
    - rule.frames.canonical_leaf
    - rule.frames.no_unversioned_frames
    - rule.frames.optional_indexes
    - rule.frames.projected_path_must_match
    - rule.frames.scheme_folder_matches_graph_id
    - rule.frames.scopes_exist
  - section.4.docgroup
    - param.docgroup_include_fixtures
    - rule.active.must_resolve
    - rule.active.profile_nonweakening
    - rule.active.required
    - rule.docgroup.parse_each_frame
    - rule.docgroup.scan_rule
    - rule.docgroup.unique_graph_id
  - section.5.ci
    - prop.required_ci_gates
    - prop.required_ci_gates_if_commit_docs
    - rule.ci.enforce_repo_law
    - rule.ci.no_diff_if_commit
    - rule.ci.render_docs_if_commit
    - rule.ci.required_gates
    - rule.ci.validate_group
  - section.6.receipts
    - rule.manifest.docs
    - rule.receipts.required_artifacts
  - section.7.violations
    - prop.required_violation_codes
    - rule.violations.stable
  - section.8.examples
    - ex.active_yml
    - ex.projected_path
  - title.0
