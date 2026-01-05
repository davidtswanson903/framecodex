# law://_kernel/meta/frame-meta-k1
- version: 0.1.0
- nodes: 46
- edges: 44
- meta: 0
## Nodes
- **code.bad_json_array** (kind: rule)
  - label: META.E.BAD_JSON_ARRAY
  - Extra fields:
    ```yml
    label: META.E.BAD_JSON_ARRAY
    modal: MUST
    text: 'Emit when doc.authors/doc.contact/doc.tags/doc.keywords is present but is not a JSON
      array string or contains empty elements. details MUST include: graph_id, key, value.

      '
    ```
- **code.bad_rfc3339** (kind: rule)
  - label: META.E.BAD_RFC3339
  - Extra fields:
    ```yml
    label: META.E.BAD_RFC3339
    modal: MUST
    text: 'Emit when doc.created or doc.updated is present but does not match prop.rfc3339_regex.
      details MUST include: graph_id, key, value.

      '
    ```
- **code.dupkey** (kind: rule)
  - label: META.E.DUPLICATE_META_KEY
  - Extra fields:
    ```yml
    label: META.E.DUPLICATE_META_KEY
    modal: MUST
    text: 'Emit when the root node contains duplicate occurrences of any key in prop.standard_keys.
      details MUST include: graph_id, key, count.

      '
    ```
- **code.nonroot** (kind: rule)
  - label: META.E.NONROOT_META_KEY
  - Extra fields:
    ```yml
    label: META.E.NONROOT_META_KEY
    modal: MUST
    text: 'Emit when any key in prop.standard_keys is found on a non-root node. details MUST include:
      graph_id, node_id, key.

      '
    ```
- **ex.1.minimal** (kind: example)
  - label: Minimal recommended metadata
  - Extra fields:
    ```yml
    label: Minimal recommended metadata
    status: informative
    text: "attrs:\n  - { key: \"doc.authors\", value: \"[\\\"David Swanson\\\"]\", vtype: \"json\"\
      \ }\n  - { key: \"doc.created\", value: \"2026-01-04T12:00:00-06:00\", vtype: \"rfc3339\"\
      \ }\n  - { key: \"doc.updated\", value: \"2026-01-04T12:00:00-06:00\", vtype: \"rfc3339\"\
      \ }\n  - { key: \"doc.license\", value: \"CC-BY-4.0\", vtype: \"spdx\" }\n"
    ```
- **ex.2.tags_contact** (kind: example)
  - label: Tags + contact
  - Extra fields:
    ```yml
    label: Tags + contact
    status: informative
    text: "attrs:\n  - { key: \"doc.tags\", value: \"[\\\"gf0\\\",\\\"governance\\\",\\\"rendering\\\
      \"]\", vtype: \"json\" }\n  - { key: \"doc.contact\", value: \"[\\\"email:you@example.com\\\
      \",\\\"handle:@plainstack\\\"]\", vtype: \"json\" }\n  - { key: \"doc.audience\", value:\
      \ \"public\" }\n"
    ```
- **law://_kernel/meta/frame-meta-k1** (kind: law)
  - Extra fields:
    ```yml
    law_id: frame-meta-k1
    law_version: 0.1.0
    profile: lawframe-k1
    status: normative
    summary: 'Defines a common, frame-level metadata surface for GF0 frames (author, created/updated,
      contact, tags, etc.). Metadata is expressed via AttrK0 on the root node (id==graph_id).
      This law defines keys, encoding, and stable violation codes; repo profiles may choose which
      fields are required.

      '
    title: FrameMeta K1 — Common Per-Frame Metadata Fields
    ```
- **prop.audience_enum** (kind: property)
  - label: Recommended audience values
  - Extra fields:
    ```yml
    label: Recommended audience values
    status: normative
    values:
    - self
    - public
    - collaborators
    - customers
    - academic
    - internal
    ```
- **prop.contact_entry_recommendation** (kind: property)
  - label: Recommended contact entry formats
  - Extra fields:
    ```yml
    label: Recommended contact entry formats
    status: informative
    values:
    - email:someone@example.com
    - url:https://example.com
    - handle:@name
    - Name <someone@example.com>
    ```
- **prop.json_array_string_regex** (kind: property)
  - label: Canonical JSON array string encoding
  - Extra fields:
    ```yml
    label: Canonical JSON array string encoding
    status: normative
    summary: 'We constrain structured values to JSON arrays (not objects) to keep determinism
      simple across implementations.

      '
    value: ^\[[^\s].*\]$
    ```
- **prop.meta_key_prefix** (kind: property)
  - label: Metadata key prefix
  - Extra fields:
    ```yml
    label: Metadata key prefix
    status: normative
    value: doc.
    ```
- **prop.recommended_keys_minset** (kind: property)
  - label: Recommended minimal set (repo may require)
  - Extra fields:
    ```yml
    keys:
    - doc.authors
    - doc.created
    - doc.updated
    - doc.license
    label: Recommended minimal set (repo may require)
    status: normative
    ```
- **prop.required_violation_codes** (kind: property)
  - label: Required violation codes
  - Extra fields:
    ```yml
    label: Required violation codes
    status: normative
    values:
    - META.E.NONROOT_META_KEY
    - META.E.DUPLICATE_META_KEY
    - META.E.BAD_RFC3339
    - META.E.BAD_JSON_ARRAY
    - META.W.MISSING_RECOMMENDED_KEY
    - META.W.UPDATED_BEFORE_CREATED
    ```
- **prop.rfc3339_regex** (kind: property)
  - label: RFC3339 timestamp regex (strict enough for offline validation)
  - Extra fields:
    ```yml
    label: RFC3339 timestamp regex (strict enough for offline validation)
    status: normative
    value: ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$
    ```
- **prop.standard_keys** (kind: property)
  - label: Standard metadata keys
  - Extra fields:
    ```yml
    keys:
    - doc.title
    - doc.summary
    - doc.author
    - doc.authors
    - doc.contact
    - doc.created
    - doc.updated
    - doc.tags
    - doc.keywords
    - doc.audience
    - doc.status
    - doc.note
    - doc.license
    label: Standard metadata keys
    status: normative
    ```
- **ref.doclicense** (kind: spec_ref)
  - label: DocLicense K1 (doc.license)
  - Extra fields:
    ```yml
    label: DocLicense K1 (doc.license)
    status: informative
    target_graph_id: law://_kernel/ip/doclicense-k1
    ```
- **ref.gf0** (kind: spec_ref)
  - label: GF0 (GraphFrameK0 / AttrK0)
  - Extra fields:
    ```yml
    label: GF0 (GraphFrameK0 / AttrK0)
    status: informative
    target_graph_id: spec://_kernel/gf/gf0-k1
    ```
- **rule.charter.uses_attrs** (kind: rule)
  - label: Metadata stored as AttrK0
  - Extra fields:
    ```yml
    label: Metadata stored as AttrK0
    modal: MUST
    text: 'Frame-level metadata MUST be represented using AttrK0 on NodeK0.attrs. AttrK0 is a
      simple key–value struct stored in a deterministic slice.

      '
    ```
- **rule.encoding.unique_keys** (kind: rule)
  - label: No duplicate doc.* keys on root
  - Extra fields:
    ```yml
    label: No duplicate doc.* keys on root
    modal: MUST
    text: 'On the root node, each key listed in prop.standard_keys MUST appear at most once in
      attrs. Duplicate keys are invalid (even though attrs are slices).

      '
    ```
- **rule.encoding.value_is_string** (kind: rule)
  - label: AttrK0 values remain strings
  - Extra fields:
    ```yml
    label: AttrK0 values remain strings
    modal: MUST
    text: 'AttrK0.value MUST remain a UTF-8 string; structured content (authors/tags/contact)
      MUST be encoded as JSON array strings per this law.

      '
    ```
- **rule.keys.audience_enum** (kind: rule)
  - label: doc.audience recommended enum
  - Extra fields:
    ```yml
    label: doc.audience recommended enum
    modal: SHOULD
    text: 'If doc.audience is present, its value SHOULD be one of prop.audience_enum. Repo policy
      MAY tighten this to MUST.

      '
    ```
- **rule.keys.author_shorthand** (kind: rule)
  - label: doc.author shorthand
  - Extra fields:
    ```yml
    label: doc.author shorthand
    modal: MAY
    text: 'doc.author MAY be used as a shorthand for a single author. If both doc.author and doc.authors
      are present, doc.authors is authoritative and doc.author SHOULD be treated as redundant.

      '
    ```
- **rule.keys.authors_format** (kind: rule)
  - label: doc.authors format
  - Extra fields:
    ```yml
    label: doc.authors format
    modal: MUST
    text: 'If doc.authors is present, its value MUST be a JSON array string (prop.json_array_string_regex)
      whose elements are non-empty strings. vtype SHOULD be ''json''.

      '
    ```
- **rule.keys.contact_format** (kind: rule)
  - label: doc.contact format
  - Extra fields:
    ```yml
    label: doc.contact format
    modal: MUST
    text: 'If doc.contact is present, its value MUST be a JSON array string (prop.json_array_string_regex)
      whose elements are non-empty strings. vtype SHOULD be ''json''.

      '
    ```
- **rule.keys.created_format** (kind: rule)
  - label: doc.created format
  - Extra fields:
    ```yml
    label: doc.created format
    modal: MUST
    text: 'If doc.created is present, it MUST match prop.rfc3339_regex. vtype SHOULD be ''rfc3339''.

      '
    ```
- **rule.keys.keywords_format** (kind: rule)
  - label: doc.keywords format
  - Extra fields:
    ```yml
    label: doc.keywords format
    modal: MUST
    text: 'If doc.keywords is present, its value MUST be a JSON array string (prop.json_array_string_regex)
      whose elements are non-empty strings. vtype SHOULD be ''json''.

      '
    ```
- **rule.keys.license_delegation** (kind: rule)
  - label: doc.license governed elsewhere
  - Extra fields:
    ```yml
    label: doc.license governed elsewhere
    modal: MUST
    text: 'doc.license semantics and validation are governed by DocLicense K1 (ref.doclicense).
      This law only reserves the key within prop.standard_keys.

      '
    ```
- **rule.keys.prefix** (kind: rule)
  - label: doc.* prefix
  - Extra fields:
    ```yml
    label: doc.* prefix
    modal: SHOULD
    text: 'Frame-level metadata keys SHOULD use the doc.* namespace (prop.meta_key_prefix). Repos
      MAY define additional namespaces, but doc.* is reserved for this law.

      '
    ```
- **rule.keys.tags_format** (kind: rule)
  - label: doc.tags format
  - Extra fields:
    ```yml
    label: doc.tags format
    modal: MUST
    text: 'If doc.tags is present, its value MUST be a JSON array string (prop.json_array_string_regex)
      whose elements are non-empty strings. vtype SHOULD be ''json''.

      '
    ```
- **rule.keys.updated_format** (kind: rule)
  - label: doc.updated format
  - Extra fields:
    ```yml
    label: doc.updated format
    modal: MUST
    text: 'If doc.updated is present, it MUST match prop.rfc3339_regex. vtype SHOULD be ''rfc3339''.

      '
    ```
- **rule.keys.updated_not_before_created** (kind: rule)
  - label: updated should not precede created
  - Extra fields:
    ```yml
    label: updated should not precede created
    modal: SHOULD
    text: 'If both doc.created and doc.updated are present and parseable as RFC3339, doc.updated
      SHOULD NOT be earlier than doc.created. Tooling MAY warn or error based on repo policy.

      '
    ```
- **rule.resolution.effective_metadata** (kind: rule)
  - label: Effective metadata resolution (optional)
  - Extra fields:
    ```yml
    label: Effective metadata resolution (optional)
    modal: MAY
    text: 'Tooling MAY compute EffectiveMetadata for missing keys using repo-provided defaults
      (e.g., default author/contact), but MUST NOT change the stored frame content when doing
      so. Defaults MUST be provided offline by repository governance.

      '
    ```
- **rule.resolution.no_network** (kind: rule)
  - label: No network fetch
  - Extra fields:
    ```yml
    label: No network fetch
    modal: MUST
    text: 'Implementations MUST NOT fetch external sources (Git history, APIs, remote services)
      to fill or validate doc.* metadata unless explicitly provided as inputs by the caller.

      '
    ```
- **rule.storage.attrs_slice_not_map** (kind: rule)
  - label: Attrs remain slices
  - Extra fields:
    ```yml
    label: Attrs remain slices
    modal: MUST
    text: 'Implementations MUST preserve attrs as ordered slices and MUST NOT canonicalize them
      into maps, even when interpreting metadata keys.

      '
    ```
- **rule.storage.root_only** (kind: rule)
  - label: Metadata keys live on root node only
  - Extra fields:
    ```yml
    label: Metadata keys live on root node only
    modal: MUST
    text: 'All keys listed in prop.standard_keys MUST be declared only on the root node where
      node.id == graph_id. Declaring these keys on non-root nodes is invalid.

      '
    ```
- **rule.violations.stable** (kind: rule)
  - label: Stable violations
  - Extra fields:
    ```yml
    label: Stable violations
    modal: MUST
    text: 'Implementations claiming conformance MUST emit the codes listed in prop.required_violation_codes
      with stable semantics and deterministic ordering.

      '
    ```
- **section.1.charter** (kind: section)
  - Extra fields:
    ```yml
    order: 1
    title: Charter
    ```
- **section.2.storage** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    title: Storage Location and Scope
    ```
- **section.3.keys** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    title: Standard Metadata Keys
    ```
- **section.4.encoding** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    title: Encoding and Normalization
    ```
- **section.5.resolution** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    title: Effective Metadata Resolution
    ```
- **section.6.violations** (kind: section)
  - Extra fields:
    ```yml
    order: 6
    title: Required Violation Codes
    ```
- **section.7.examples** (kind: section)
  - Extra fields:
    ```yml
    order: 7
    title: Examples
    ```
- **title.0** (kind: title)
  - Extra fields:
    ```yml
    text: FrameMeta K1
    ```
- **warn.missing_recommended** (kind: rule)
  - label: META.W.MISSING_RECOMMENDED_KEY
  - Extra fields:
    ```yml
    label: META.W.MISSING_RECOMMENDED_KEY
    modal: MAY
    text: 'Emit when a key in prop.recommended_keys_minset is missing from the root node. details
      SHOULD include: graph_id, missing_key.

      '
    ```
- **warn.updated_before_created** (kind: rule)
  - label: META.W.UPDATED_BEFORE_CREATED
  - Extra fields:
    ```yml
    label: META.W.UPDATED_BEFORE_CREATED
    modal: MAY
    text: 'Emit when both doc.created and doc.updated are present, parseable, and doc.updated
      < doc.created. details SHOULD include: graph_id, created, updated.

      '
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| law://_kernel/meta/frame-meta-k1 | ref.doclicense | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | ref.gf0 | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.1.charter | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.2.storage | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.3.keys | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.4.encoding | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.5.resolution | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.6.violations | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | section.7.examples | contains |  |  |  |
| law://_kernel/meta/frame-meta-k1 | title.0 | contains |  |  |  |
| section.1.charter | rule.charter.uses_attrs | contains |  |  |  |
| section.2.storage | rule.storage.attrs_slice_not_map | contains |  |  |  |
| section.2.storage | rule.storage.root_only | contains |  |  |  |
| section.3.keys | prop.audience_enum | contains |  |  |  |
| section.3.keys | prop.meta_key_prefix | contains |  |  |  |
| section.3.keys | prop.recommended_keys_minset | contains |  |  |  |
| section.3.keys | prop.standard_keys | contains |  |  |  |
| section.3.keys | rule.keys.audience_enum | contains |  |  |  |
| section.3.keys | rule.keys.author_shorthand | contains |  |  |  |
| section.3.keys | rule.keys.authors_format | contains |  |  |  |
| section.3.keys | rule.keys.contact_format | contains |  |  |  |
| section.3.keys | rule.keys.created_format | contains |  |  |  |
| section.3.keys | rule.keys.keywords_format | contains |  |  |  |
| section.3.keys | rule.keys.license_delegation | contains |  |  |  |
| section.3.keys | rule.keys.prefix | contains |  |  |  |
| section.3.keys | rule.keys.tags_format | contains |  |  |  |
| section.3.keys | rule.keys.updated_format | contains |  |  |  |
| section.3.keys | rule.keys.updated_not_before_created | contains |  |  |  |
| section.4.encoding | prop.json_array_string_regex | contains |  |  |  |
| section.4.encoding | prop.rfc3339_regex | contains |  |  |  |
| section.4.encoding | rule.encoding.unique_keys | contains |  |  |  |
| section.4.encoding | rule.encoding.value_is_string | contains |  |  |  |
| section.5.resolution | rule.resolution.effective_metadata | contains |  |  |  |
| section.5.resolution | rule.resolution.no_network | contains |  |  |  |
| section.6.violations | code.bad_json_array | contains |  |  |  |
| section.6.violations | code.bad_rfc3339 | contains |  |  |  |
| section.6.violations | code.dupkey | contains |  |  |  |
| section.6.violations | code.nonroot | contains |  |  |  |
| section.6.violations | prop.required_violation_codes | contains |  |  |  |
| section.6.violations | rule.violations.stable | contains |  |  |  |
| section.6.violations | warn.missing_recommended | contains |  |  |  |
| section.6.violations | warn.updated_before_created | contains |  |  |  |
| section.7.examples | ex.1.minimal | contains |  |  |  |
| section.7.examples | ex.2.tags_contact | contains |  |  |  |

## Contains Tree
- law://_kernel/meta/frame-meta-k1
  - ref.doclicense
  - ref.gf0
  - section.1.charter
    - rule.charter.uses_attrs
  - section.2.storage
    - rule.storage.attrs_slice_not_map
    - rule.storage.root_only
  - section.3.keys
    - prop.audience_enum
    - prop.meta_key_prefix
    - prop.recommended_keys_minset
    - prop.standard_keys
    - rule.keys.audience_enum
    - rule.keys.author_shorthand
    - rule.keys.authors_format
    - rule.keys.contact_format
    - rule.keys.created_format
    - rule.keys.keywords_format
    - rule.keys.license_delegation
    - rule.keys.prefix
    - rule.keys.tags_format
    - rule.keys.updated_format
    - rule.keys.updated_not_before_created
  - section.4.encoding
    - prop.json_array_string_regex
    - prop.rfc3339_regex
    - rule.encoding.unique_keys
    - rule.encoding.value_is_string
  - section.5.resolution
    - rule.resolution.effective_metadata
    - rule.resolution.no_network
  - section.6.violations
    - code.bad_json_array
    - code.bad_rfc3339
    - code.dupkey
    - code.nonroot
    - prop.required_violation_codes
    - rule.violations.stable
    - warn.missing_recommended
    - warn.updated_before_created
  - section.7.examples
    - ex.1.minimal
    - ex.2.tags_contact
  - title.0
