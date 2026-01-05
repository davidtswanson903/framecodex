# law://_kernel/id/frameurl-k1
- version: 0.1.0
- nodes: 44
- edges: 40
- meta: 0
## Nodes
- **def.frameurl** (kind: definition)
  - label: FrameURL
  - Extra fields:
    ```yml
    label: FrameURL
    status: normative
    text: 'A canonical, URL-like identifier used as GF0 graph_id. FrameURL K1 uses a strict grammar:
      <scheme>://<scope>/<segment>/<segment>/.../<name>. FrameURL is versionless.

      '
    ```
- **def.name** (kind: definition)
  - label: Name
  - Extra fields:
    ```yml
    label: Name
    status: normative
    text: 'The final segment of a FrameURL. Name is semantically the artifact identifier within
      its package path.

      '
    ```
- **def.pkg** (kind: definition)
  - label: Package Path (pkg)
  - Extra fields:
    ```yml
    label: Package Path (pkg)
    status: normative
    text: 'The ordered list of segments that define where a frame lives in the fractal tree. For
      FrameURL, pkg == [scope] + [segment...name] (excluding scheme).

      '
    ```
- **def.scheme** (kind: definition)
  - label: Scheme
  - Extra fields:
    ```yml
    label: Scheme
    status: normative
    text: 'The FrameURL scheme indicates the frame class. Schemes are an enum defined by prop.scheme_enum.

      '
    ```
- **def.scope** (kind: definition)
  - label: Scope
  - Extra fields:
    ```yml
    label: Scope
    status: normative
    text: 'The first path segment after ''://''. Scope is used as the top-level shard for filesystem
      layout.

      '
    ```
- **def.segment** (kind: definition)
  - label: Segment
  - Extra fields:
    ```yml
    label: Segment
    status: normative
    text: 'A single FrameURL path component. Segment charset is restricted for determinism and
      portability.

      '
    ```
- **ex.1.frameurl** (kind: example)
  - label: Canonical FrameURL
  - Extra fields:
    ```yml
    label: Canonical FrameURL
    status: informative
    text: 'law://repo/governance/repo-k1

      spec://_kernel/gf/gf0-k1

      render://repo/docs/default

      '
    ```
- **ex.2.path_projection** (kind: example)
  - label: Projected path
  - Extra fields:
    ```yml
    label: Projected path
    status: informative
    text: 'graph_id:  law://repo/governance/repo-k1

      version:   1.0.0

      path:      frames/repo/law/governance/repo-k1/v1.0.0/frame.yml

      '
    ```
- **law://_kernel/id/frameurl-k1** (kind: law)
  - Extra fields:
    ```yml
    law_id: frameurl-k1
    law_version: 0.1.0
    profile: lawframe-k1
    status: normative
    summary: 'Defines a strict URL-like canonical identifier (FrameURL) for GF0 frames and a deterministic
      projection from (graph_id, version) to a repository filesystem path.

      '
    title: FrameURL K1 — Canonical Identity and Filesystem Projection
    ```
- **prop.forbidden_segments** (kind: property)
  - label: Forbidden segments
  - Extra fields:
    ```yml
    label: Forbidden segments
    status: normative
    values:
    - .
    - ..
    ```
- **prop.leaf_filename** (kind: property)
  - label: Leaf filename
  - Extra fields:
    ```yml
    label: Leaf filename
    status: normative
    value: frame.yml
    ```
- **prop.path_root** (kind: property)
  - label: Repository frames root
  - Extra fields:
    ```yml
    label: Repository frames root
    status: normative
    value: frames
    ```
- **prop.required_root_node_invariant** (kind: property)
  - label: Root node invariant
  - Extra fields:
    ```yml
    label: Root node invariant
    status: normative
    value: Each frame MUST contain a root node where node.id == graph_id.
    ```
- **prop.required_violation_codes** (kind: property)
  - label: Required violation codes
  - Extra fields:
    ```yml
    label: Required violation codes
    status: normative
    values:
    - ID.E.BAD_FRAMEURL
    - ID.E.BAD_SCHEME
    - ID.E.BAD_SEGMENT
    - ID.E.FORBIDDEN_SEGMENT
    - ID.E.BAD_VERSION_FOLDER
    - ID.E.PATH_MISMATCH
    - ID.E.MISSING_ROOT_NODE
    - ID.E.UNKNOWN_REFERENCE
    ```
- **prop.scheme_enum** (kind: property)
  - label: Allowed schemes
  - Extra fields:
    ```yml
    label: Allowed schemes
    status: normative
    values:
    - law
    - spec
    - profile
    - render
    - fixture
    ```
- **prop.segment_regex** (kind: property)
  - label: Segment regex
  - Extra fields:
    ```yml
    label: Segment regex
    status: normative
    value: ^[a-z0-9][a-z0-9._-]{0,63}$
    ```
- **prop.version_folder_prefix** (kind: property)
  - label: Version folder prefix
  - Extra fields:
    ```yml
    label: Version folder prefix
    status: normative
    value: v
    ```
- **rule.charter.graph_id_is_frameurl** (kind: rule)
  - label: graph_id is canonical FrameURL
  - Extra fields:
    ```yml
    label: graph_id is canonical FrameURL
    modal: MUST
    status: normative
    text: 'A frame claiming conformance to FrameURL K1 MUST use a canonical FrameURL as graph_id.

      '
    ```
- **rule.charter.root_node_id** (kind: rule)
  - label: Root node id equals graph_id
  - Extra fields:
    ```yml
    label: Root node id equals graph_id
    modal: MUST
    status: normative
    text: 'Each frame MUST contain exactly one root node where node.id == graph_id. The root node
      MUST be treated as the canonical identity-bearing node.

      '
    ```
- **rule.charter.version_is_separate** (kind: rule)
  - label: Version is separate from FrameURL
  - Extra fields:
    ```yml
    label: Version is separate from FrameURL
    modal: MUST
    status: normative
    text: 'FrameURL is versionless. Version MUST be expressed only via GF0.version, not embedded
      into graph_id.

      '
    ```
- **rule.code.bad_frameurl** (kind: rule)
  - label: ID.E.BAD_FRAMEURL
  - Extra fields:
    ```yml
    label: ID.E.BAD_FRAMEURL
    modal: MUST
    status: normative
    text: 'Emit when graph_id fails FrameURL parsing under rule.grammar.strict_form or rule.grammar.no_query_fragment
      or rule.grammar.no_percent_encoding or rule.norm.*. details MUST include: graph_id.

      '
    ```
- **rule.code.path_mismatch** (kind: rule)
  - label: ID.E.PATH_MISMATCH
  - Extra fields:
    ```yml
    label: ID.E.PATH_MISMATCH
    modal: MUST
    status: normative
    text: 'Emit when an on-disk frame path does not equal the canonical projection under rule.path.projection_function.
      details MUST include: graph_id, version, expected_path, actual_path.

      '
    ```
- **rule.code.unknown_reference** (kind: rule)
  - label: ID.E.UNKNOWN_REFERENCE
  - Extra fields:
    ```yml
    label: ID.E.UNKNOWN_REFERENCE
    modal: MUST
    status: normative
    text: 'Emit when a FrameRef is not a valid FrameURL. details MUST include: reference.

      '
    ```
- **rule.codes.stable** (kind: rule)
  - label: Stable codes
  - Extra fields:
    ```yml
    label: Stable codes
    modal: MUST
    status: normative
    text: 'Implementations claiming conformance MUST emit the violation codes listed in prop.required_violation_codes
      with stable semantics.

      '
    ```
- **rule.grammar.no_percent_encoding** (kind: rule)
  - label: No percent-encoding
  - Extra fields:
    ```yml
    label: No percent-encoding
    modal: MUST
    status: normative
    text: 'FrameURL MUST NOT use percent-encoding. All segments must be representable using the
      restricted segment charset.

      '
    ```
- **rule.grammar.no_query_fragment** (kind: rule)
  - label: No query or fragment
  - Extra fields:
    ```yml
    label: No query or fragment
    modal: MUST
    status: normative
    text: 'FrameURL MUST NOT contain ''?'', ''#'', or any query/fragment component. The identifier
      is purely hierarchical.

      '
    ```
- **rule.grammar.strict_form** (kind: rule)
  - label: Strict FrameURL grammar
  - Extra fields:
    ```yml
    label: Strict FrameURL grammar
    modal: MUST
    status: normative
    text: "FrameURL MUST match: <scheme>://<scope>/<segment>.../<name> where:\n  - scheme is one\
      \ of prop.scheme_enum\n  - scope and all segments (including name) match prop.segment_regex\n\
      \  - forbidden segments prop.forbidden_segments are disallowed\n  - there is at least one\
      \ segment after scope (i.e., name exists)\n"
    ```
- **rule.norm.canonical_slashes** (kind: rule)
  - label: Canonical slashes
  - Extra fields:
    ```yml
    label: Canonical slashes
    modal: MUST
    status: normative
    text: 'FrameURL MUST use exactly one ''://'' delimiter and ''/'' as the only segment separator.
      Repeated slashes ''//'' in the path portion are forbidden.

      '
    ```
- **rule.norm.lowercase_only** (kind: rule)
  - label: Lowercase only
  - Extra fields:
    ```yml
    label: Lowercase only
    modal: MUST
    status: normative
    text: 'FrameURL MUST be lowercase ASCII only. Uppercase letters are forbidden.

      '
    ```
- **rule.norm.no_whitespace** (kind: rule)
  - label: No whitespace
  - Extra fields:
    ```yml
    label: No whitespace
    modal: MUST
    status: normative
    text: 'FrameURL MUST NOT contain whitespace. Leading/trailing whitespace MUST be treated as
      invalid (not auto-trimmed).

      '
    ```
- **rule.norm.scheme_validation** (kind: rule)
  - label: Scheme validation
  - Extra fields:
    ```yml
    label: Scheme validation
    modal: MUST
    status: normative
    text: 'scheme MUST be in prop.scheme_enum. Unknown schemes are invalid.

      '
    ```
- **rule.path.leaf_filename** (kind: rule)
  - label: Leaf filename
  - Extra fields:
    ```yml
    label: Leaf filename
    modal: MUST
    status: normative
    text: 'The leaf filename MUST be prop.leaf_filename (''frame.yml'') for canonical projection.
      Repositories MAY provide a compatibility mode that also accepts <graph_id_sanitized>.yml,
      but canonical projection remains authoritative.

      '
    ```
- **rule.path.must_match_on_disk** (kind: rule)
  - label: On-disk path must match projection
  - Extra fields:
    ```yml
    label: On-disk path must match projection
    modal: MUST
    status: normative
    text: 'If a repository uses FrameURL K1 as its on-disk convention, each frame file MUST be
      located at the canonical projected path derived from (graph_id, version). Deviations are
      invalid.

      '
    ```
- **rule.path.projection_function** (kind: rule)
  - label: Canonical path projection
  - Extra fields:
    ```yml
    label: Canonical path projection
    modal: MUST
    status: normative
    text: "The canonical relative filesystem path for a frame is a pure function of (graph_id,\
      \ version):\n  frames/<scope>/<scheme>/<segments...>/<name>/v<version>/frame.yml\nwhere\
      \ scope and segments are derived from parsing graph_id.\n"
    ```
- **rule.path.version_folder** (kind: rule)
  - label: Version folder format
  - Extra fields:
    ```yml
    label: Version folder format
    modal: MUST
    status: normative
    text: 'The version folder name MUST be ''v'' + version (prop.version_folder_prefix), with
      no additional decoration. Example: v1.2.0.

      '
    ```
- **rule.ref.frameref_is_frameurl** (kind: rule)
  - label: FrameRef must be a canonical FrameURL
  - Extra fields:
    ```yml
    label: FrameRef must be a canonical FrameURL
    modal: MUST
    status: normative
    text: 'A FrameRef consumed by tools MUST be a canonical FrameURL.

      '
    ```
- **rule.ref.no_external_fetch** (kind: rule)
  - label: No external fetch
  - Extra fields:
    ```yml
    label: No external fetch
    modal: MUST
    status: normative
    text: 'Reference normalization MUST be offline. Implementations MUST NOT fetch or infer missing
      frames from network sources unless explicitly provided by the caller.

      '
    ```
- **section.1.charter** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    status: normative
    title: Charter
    ```
- **section.2.grammar** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    status: normative
    title: FrameURL Grammar
    ```
- **section.3.normalization** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    status: normative
    title: Normalization Rules
    ```
- **section.4.path_projection** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    status: normative
    title: Filesystem Path Projection
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
    status: informative
    text: FrameURL K1
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| law://_kernel/id/frameurl-k1 | section.1.charter | contains |  |  |  |
| law://_kernel/id/frameurl-k1 | section.2.grammar | contains |  |  |  |
| law://_kernel/id/frameurl-k1 | section.3.normalization | contains |  |  |  |
| law://_kernel/id/frameurl-k1 | section.4.path_projection | contains |  |  |  |
| law://_kernel/id/frameurl-k1 | section.7.violations | contains |  |  |  |
| law://_kernel/id/frameurl-k1 | section.8.examples | contains |  |  |  |
| law://_kernel/id/frameurl-k1 | title.0 | contains |  |  |  |
| section.1.charter | def.frameurl | contains |  |  |  |
| section.1.charter | rule.charter.graph_id_is_frameurl | contains |  |  |  |
| section.1.charter | rule.charter.root_node_id | contains |  |  |  |
| section.1.charter | rule.charter.version_is_separate | contains |  |  |  |
| section.2.grammar | def.name | contains |  |  |  |
| section.2.grammar | def.pkg | contains |  |  |  |
| section.2.grammar | def.scheme | contains |  |  |  |
| section.2.grammar | def.scope | contains |  |  |  |
| section.2.grammar | def.segment | contains |  |  |  |
| section.2.grammar | prop.forbidden_segments | contains |  |  |  |
| section.2.grammar | prop.scheme_enum | contains |  |  |  |
| section.2.grammar | prop.segment_regex | contains |  |  |  |
| section.2.grammar | rule.grammar.no_percent_encoding | contains |  |  |  |
| section.2.grammar | rule.grammar.no_query_fragment | contains |  |  |  |
| section.2.grammar | rule.grammar.strict_form | contains |  |  |  |
| section.3.normalization | rule.norm.canonical_slashes | contains |  |  |  |
| section.3.normalization | rule.norm.lowercase_only | contains |  |  |  |
| section.3.normalization | rule.norm.no_whitespace | contains |  |  |  |
| section.3.normalization | rule.norm.scheme_validation | contains |  |  |  |
| section.4.path_projection | prop.leaf_filename | contains |  |  |  |
| section.4.path_projection | prop.path_root | contains |  |  |  |
| section.4.path_projection | prop.version_folder_prefix | contains |  |  |  |
| section.4.path_projection | rule.path.leaf_filename | contains |  |  |  |
| section.4.path_projection | rule.path.must_match_on_disk | contains |  |  |  |
| section.4.path_projection | rule.path.projection_function | contains |  |  |  |
| section.4.path_projection | rule.path.version_folder | contains |  |  |  |
| section.7.violations | prop.required_violation_codes | contains |  |  |  |
| section.7.violations | rule.code.bad_frameurl | contains |  |  |  |
| section.7.violations | rule.code.path_mismatch | contains |  |  |  |
| section.7.violations | rule.code.unknown_reference | contains |  |  |  |
| section.7.violations | rule.codes.stable | contains |  |  |  |
| section.8.examples | ex.1.frameurl | contains |  |  |  |
| section.8.examples | ex.2.path_projection | contains |  |  |  |

## Contains Tree
- law://_kernel/id/frameurl-k1
  - section.1.charter
    - def.frameurl
    - rule.charter.graph_id_is_frameurl
    - rule.charter.root_node_id
    - rule.charter.version_is_separate
  - section.2.grammar
    - def.name
    - def.pkg
    - def.scheme
    - def.scope
    - def.segment
    - prop.forbidden_segments
    - prop.scheme_enum
    - prop.segment_regex
    - rule.grammar.no_percent_encoding
    - rule.grammar.no_query_fragment
    - rule.grammar.strict_form
  - section.3.normalization
    - rule.norm.canonical_slashes
    - rule.norm.lowercase_only
    - rule.norm.no_whitespace
    - rule.norm.scheme_validation
  - section.4.path_projection
    - prop.leaf_filename
    - prop.path_root
    - prop.version_folder_prefix
    - rule.path.leaf_filename
    - rule.path.must_match_on_disk
    - rule.path.projection_function
    - rule.path.version_folder
  - section.7.violations
    - prop.required_violation_codes
    - rule.code.bad_frameurl
    - rule.code.path_mismatch
    - rule.code.unknown_reference
    - rule.codes.stable
  - section.8.examples
    - ex.1.frameurl
    - ex.2.path_projection
  - title.0
