# law://_kernel/ip/doclicense-k1
- version: 0.1.0
- nodes: 40
- edges: 38
- meta: 0
## Nodes
- **code.bad_expr** (kind: rule)
  - label: IP.E.BAD_LICENSE_EXPR
  - Extra fields:
    ```yml
    label: IP.E.BAD_LICENSE_EXPR
    modal: MUST
    text: 'Emit when doc.license is present but fails rule.fields.doc_license_format. details
      MUST include: frame graph_id and the invalid doc.license string.

      '
    ```
- **code.inherited_warning** (kind: rule)
  - label: IP.W.INHERITED_LICENSE
  - Extra fields:
    ```yml
    label: IP.W.INHERITED_LICENSE
    modal: MAY
    text: 'Emit when EffectiveLicense was taken from package_default_license or repo_default_license
      (i.e., doc.license was not explicitly set). details SHOULD include: frame graph_id and source
      (package|repo).

      '
    ```
- **code.missing_effective** (kind: rule)
  - label: IP.E.MISSING_EFFECTIVE_LICENSE
  - Extra fields:
    ```yml
    label: IP.E.MISSING_EFFECTIVE_LICENSE
    modal: MUST
    text: 'Emit when EffectiveLicense cannot be computed (e.g., doc.license absent, package default
      absent, and repo_default_license missing/empty). details MUST include: frame graph_id.

      '
    ```
- **code.missing_repo_default** (kind: rule)
  - label: IP.E.MISSING_REPO_DEFAULT_LICENSE
  - Extra fields:
    ```yml
    label: IP.E.MISSING_REPO_DEFAULT_LICENSE
    modal: MUST
    text: 'Emit when repo_default_license is absent or empty at resolution time. details MUST
      include: frame graph_id.

      '
    ```
- **code.nonroot** (kind: rule)
  - label: IP.E.LICENSE_ON_NONROOT
  - Extra fields:
    ```yml
    label: IP.E.LICENSE_ON_NONROOT
    modal: MUST
    text: 'Emit when any of the keys in prop.license_attr_keys are found on a non-root node. details
      MUST include: frame graph_id, offending node id, and key.

      '
    ```
- **def.doc_license_attr** (kind: definition)
  - label: doc.license
  - Extra fields:
    ```yml
    label: doc.license
    text: 'An AttrK0 on the root node (node.id == graph_id) whose value is a license expression
      string. This value determines the license for the document unless overridden by higher-precedence
      rules.

      '
    ```
- **def.effective_license** (kind: definition)
  - label: EffectiveLicense
  - Extra fields:
    ```yml
    label: EffectiveLicense
    text: 'The resolved license string produced by applying the deterministic resolution algorithm
      in section.4.

      '
    ```
- **def.license_expression** (kind: definition)
  - label: LicenseExpression
  - Extra fields:
    ```yml
    label: LicenseExpression
    text: 'A string representing the license terms for a document. This law prefers SPDX license
      identifiers and SPDX-like expressions, but also permits a bounded set of non-SPDX sentinel
      values.

      '
    ```
- **def.package_default** (kind: definition)
  - label: Package default license
  - Extra fields:
    ```yml
    label: Package default license
    text: 'An optional default license associated with the document''s package scope. How package
      scope is determined is a repository concern (typically via filesystem projection or FrameURL
      package path).

      '
    ```
- **def.repo_default** (kind: definition)
  - label: Repo default license
  - Extra fields:
    ```yml
    label: Repo default license
    text: 'A required default license configured by repository governance (e.g., RepoLaw/Profile).
      Used when doc.license is absent and no package default is provided.

      '
    ```
- **ex.1.explicit_spdx** (kind: example)
  - label: Explicit SPDX license
  - Extra fields:
    ```yml
    label: Explicit SPDX license
    text: "root.attrs:\n  - { key: \"doc.license\", value: \"CC-BY-4.0\", vtype: \"spdx\" }\n\
      \  - { key: \"doc.copyright\", value: \"© 2026 David Swanson\" }\n"
    ```
- **ex.2.inherit_repo_default** (kind: example)
  - label: Inherited repo default
  - Extra fields:
    ```yml
    label: Inherited repo default
    text: '# doc.license omitted on the frame

      repo_default_license: "CC-BY-4.0"

      EffectiveLicense: "CC-BY-4.0"  # source: repo-default

      '
    ```
- **ex.3.proprietary** (kind: example)
  - label: Proprietary sentinel
  - Extra fields:
    ```yml
    label: Proprietary sentinel
    text: "root.attrs:\n  - { key: \"doc.license\", value: \"Proprietary\" }\n  - { key: \"doc.license.note\"\
      , value: \"Do not redistribute without permission.\" }\n"
    ```
- **law://_kernel/ip/doclicense-k1** (kind: law)
  - Extra fields:
    ```yml
    law_id: doclicense-k1
    law_version: 0.1.0
    profile: lawframe-k1
    status: normative
    summary: 'Defines a per-document license attribute for GF0 frames. Establishes required keys,
      a deterministic effective-license resolution algorithm (explicit > package default > repo
      default), and stable violation codes.

      '
    title: DocLicense K1 — Per-Document Licensing Metadata
    ```
- **prop.attr_json_array_regex** (kind: property)
  - label: Canonical JSON array encoding (for future multi-value attrs)
  - Extra fields:
    ```yml
    label: Canonical JSON array encoding (for future multi-value attrs)
    value: ^\[[^\s].*\]$
    ```
- **prop.default_repo_license_recommendation** (kind: property)
  - label: Recommended repo default (free/open)
  - Extra fields:
    ```yml
    label: Recommended repo default (free/open)
    value: CC-BY-4.0
    ```
- **prop.license_attr_keys** (kind: property)
  - label: License attribute keys
  - Extra fields:
    ```yml
    label: License attribute keys
    values:
    - doc.license
    - doc.license.note
    - doc.copyright
    ```
- **prop.license_regex_spdx_like** (kind: property)
  - label: SPDX-like license expression regex (permissive)
  - Extra fields:
    ```yml
    label: SPDX-like license expression regex (permissive)
    value: ^[A-Za-z0-9.+-]+([ ]+(AND|OR|WITH)[ ]+[A-Za-z0-9.+-]+)*$
    ```
- **prop.non_spdx_sentinels** (kind: property)
  - label: Permitted non-SPDX sentinel values
  - Extra fields:
    ```yml
    label: Permitted non-SPDX sentinel values
    values:
    - Proprietary
    - Public-Domain
    - Unlicensed
    ```
- **prop.required_violation_codes** (kind: property)
  - label: Required violation codes
  - Extra fields:
    ```yml
    label: Required violation codes
    values:
    - IP.E.MISSING_REPO_DEFAULT_LICENSE
    - IP.E.MISSING_EFFECTIVE_LICENSE
    - IP.E.BAD_LICENSE_EXPR
    - IP.E.LICENSE_ON_NONROOT
    - IP.W.INHERITED_LICENSE
    ```
- **rule.charter.default_open** (kind: rule)
  - label: Default should be free/open
  - Extra fields:
    ```yml
    label: Default should be free/open
    modal: SHOULD
    text: 'Repository governance SHOULD set repo_default_license to a free/open license (recommended:
      prop.default_repo_license_recommendation) unless the repository explicitly targets restricted
      content.

      '
    ```
- **rule.charter.per_doc_license** (kind: rule)
  - label: Per-document license metadata
  - Extra fields:
    ```yml
    label: Per-document license metadata
    modal: MUST
    text: 'A repository adopting DocLicense K1 MUST treat each GF0 frame as a licensable document
      and MUST compute an EffectiveLicense for the frame using section.4.

      '
    ```
- **rule.fields.copyright_format** (kind: rule)
  - label: doc.copyright
  - Extra fields:
    ```yml
    label: doc.copyright
    modal: MAY
    text: 'doc.copyright MAY be present as a free-form string.

      '
    ```
- **rule.fields.doc_license_format** (kind: rule)
  - label: doc.license format
  - Extra fields:
    ```yml
    label: doc.license format
    modal: MUST
    text: "If doc.license is present, its value MUST either:\n  (a) match prop.license_regex_spdx_like,\
      \ OR\n  (b) equal one of prop.non_spdx_sentinels.\nAny other value is invalid.\n"
    ```
- **rule.fields.doc_license_note_format** (kind: rule)
  - label: doc.license.note
  - Extra fields:
    ```yml
    label: doc.license.note
    modal: MAY
    text: 'doc.license.note MAY be present as a free-form string. Tooling MUST NOT interpret it
      for resolution, but MAY render it.

      '
    ```
- **rule.fields.root_only** (kind: rule)
  - label: License attrs live on root node
  - Extra fields:
    ```yml
    label: License attrs live on root node
    modal: MUST
    text: 'doc.license, doc.license.note, and doc.copyright (if present) MUST be declared only
      on the root node where node.id == graph_id. Declaring these keys on non-root nodes is invalid.

      '
    ```
- **rule.rendering.must_show_effective** (kind: rule)
  - label: Renderers must show EffectiveLicense
  - Extra fields:
    ```yml
    label: Renderers must show EffectiveLicense
    modal: MUST
    text: 'Any renderer used to publish or display a frame MUST include EffectiveLicense near
      the top of the rendered output, along with an indication of whether it was explicit, package-default,
      or repo-default.

      '
    ```
- **rule.rendering.should_show_note** (kind: rule)
  - label: Renderers should show license notes
  - Extra fields:
    ```yml
    label: Renderers should show license notes
    modal: SHOULD
    text: 'If doc.license.note is present, renderers SHOULD include it near the license display.

      '
    ```
- **rule.resolution.deterministic** (kind: rule)
  - label: Deterministic resolution algorithm
  - Extra fields:
    ```yml
    label: Deterministic resolution algorithm
    modal: MUST
    text: "EffectiveLicense MUST be computed deterministically using this precedence order:\n\
      \  1) If root has doc.license, EffectiveLicense := doc.license\n  2) Else if package_default_license\
      \ is provided by the caller, EffectiveLicense := package_default_license\n  3) Else EffectiveLicense\
      \ := repo_default_license\nIf repo_default_license is absent/empty, this is an error.\n"
    ```
- **rule.resolution.no_implicit_fetch** (kind: rule)
  - label: Offline resolution
  - Extra fields:
    ```yml
    label: Offline resolution
    modal: MUST
    text: 'Resolution MUST be offline. Implementations MUST NOT fetch external metadata to determine
      the license. Any package_default_license or repo_default_license inputs MUST be supplied
      by repository governance.

      '
    ```
- **rule.resolution.repo_default_required** (kind: rule)
  - label: Repo default required
  - Extra fields:
    ```yml
    label: Repo default required
    modal: MUST
    text: 'Repository governance MUST define a non-empty repo_default_license string. This value
      is used when doc.license is absent and no package default is provided.

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
- **section.2.model** (kind: section)
  - Extra fields:
    ```yml
    order: 2
    title: Model
    ```
- **section.3.fields** (kind: section)
  - Extra fields:
    ```yml
    order: 3
    title: Required and Optional Fields
    ```
- **section.4.resolution** (kind: section)
  - Extra fields:
    ```yml
    order: 4
    title: Effective License Resolution
    ```
- **section.5.rendering** (kind: section)
  - Extra fields:
    ```yml
    order: 5
    title: Renderer Requirements
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
    text: DocLicense K1
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| law://_kernel/ip/doclicense-k1 | section.1.charter | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | section.2.model | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | section.3.fields | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | section.4.resolution | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | section.5.rendering | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | section.6.violations | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | section.7.examples | contains |  |  |  |
| law://_kernel/ip/doclicense-k1 | title.0 | contains |  |  |  |
| section.1.charter | rule.charter.default_open | contains |  |  |  |
| section.1.charter | rule.charter.per_doc_license | contains |  |  |  |
| section.2.model | def.doc_license_attr | contains |  |  |  |
| section.2.model | def.effective_license | contains |  |  |  |
| section.2.model | def.license_expression | contains |  |  |  |
| section.2.model | def.package_default | contains |  |  |  |
| section.2.model | def.repo_default | contains |  |  |  |
| section.2.model | prop.default_repo_license_recommendation | contains |  |  |  |
| section.2.model | prop.license_attr_keys | contains |  |  |  |
| section.2.model | prop.license_regex_spdx_like | contains |  |  |  |
| section.2.model | prop.non_spdx_sentinels | contains |  |  |  |
| section.3.fields | rule.fields.copyright_format | contains |  |  |  |
| section.3.fields | rule.fields.doc_license_format | contains |  |  |  |
| section.3.fields | rule.fields.doc_license_note_format | contains |  |  |  |
| section.3.fields | rule.fields.root_only | contains |  |  |  |
| section.4.resolution | rule.resolution.deterministic | contains |  |  |  |
| section.4.resolution | rule.resolution.no_implicit_fetch | contains |  |  |  |
| section.4.resolution | rule.resolution.repo_default_required | contains |  |  |  |
| section.5.rendering | rule.rendering.must_show_effective | contains |  |  |  |
| section.5.rendering | rule.rendering.should_show_note | contains |  |  |  |
| section.6.violations | code.bad_expr | contains |  |  |  |
| section.6.violations | code.inherited_warning | contains |  |  |  |
| section.6.violations | code.missing_effective | contains |  |  |  |
| section.6.violations | code.missing_repo_default | contains |  |  |  |
| section.6.violations | code.nonroot | contains |  |  |  |
| section.6.violations | prop.required_violation_codes | contains |  |  |  |
| section.6.violations | rule.violations.stable | contains |  |  |  |
| section.7.examples | ex.1.explicit_spdx | contains |  |  |  |
| section.7.examples | ex.2.inherit_repo_default | contains |  |  |  |
| section.7.examples | ex.3.proprietary | contains |  |  |  |

## Contains Tree
- law://_kernel/ip/doclicense-k1
  - section.1.charter
    - rule.charter.default_open
    - rule.charter.per_doc_license
  - section.2.model
    - def.doc_license_attr
    - def.effective_license
    - def.license_expression
    - def.package_default
    - def.repo_default
    - prop.default_repo_license_recommendation
    - prop.license_attr_keys
    - prop.license_regex_spdx_like
    - prop.non_spdx_sentinels
  - section.3.fields
    - rule.fields.copyright_format
    - rule.fields.doc_license_format
    - rule.fields.doc_license_note_format
    - rule.fields.root_only
  - section.4.resolution
    - rule.resolution.deterministic
    - rule.resolution.no_implicit_fetch
    - rule.resolution.repo_default_required
  - section.5.rendering
    - rule.rendering.must_show_effective
    - rule.rendering.should_show_note
  - section.6.violations
    - code.bad_expr
    - code.inherited_warning
    - code.missing_effective
    - code.missing_repo_default
    - code.nonroot
    - prop.required_violation_codes
    - rule.violations.stable
  - section.7.examples
    - ex.1.explicit_spdx
    - ex.2.inherit_repo_default
    - ex.3.proprietary
  - title.0
