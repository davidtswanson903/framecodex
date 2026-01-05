# law://_kernel/law/lawprofile-k1
- version: 0.1.0
- nodes: 4
- edges: 3
- meta: 0
## Nodes
- **def.profile_root** (kind: definition)
  - label: LawProfile root
  - Extra fields:
    ```yml
    label: LawProfile root
    text: A LawProfile is a GF0 graph whose root node has id==graph_id, kind=='law_profile', profile=='lawprofile-k1'.
    ```
- **law://_kernel/law/lawprofile-k1** (kind: law)
  - Extra fields:
    ```yml
    law_id: lawprofile-k1
    law_version: 0.1.0
    profile: lawframe-k1
    status: normative
    summary: Defines how profiles bind parameters and (optionally) override permitted rule parameters.
    title: LawProfile K1 — Parameterization over LawDocs
    ```
- **rule.profile_binding** (kind: rule)
  - label: Profiles bind parameters deterministically
  - Extra fields:
    ```yml
    label: Profiles bind parameters deterministically
    modal: MUST
    text: 'Parameter bindings MUST be represented as ordered nodes (kind==''parameter'') with
      explicit keys. Implementations MUST resolve bindings by key lexicographic order.

      '
    ```
- **rule.profile_no_weakening** (kind: rule)
  - label: Profiles must not weaken laws
  - Extra fields:
    ```yml
    label: Profiles must not weaken laws
    modal: MUST
    text: 'A LawProfile MUST NOT disable or weaken any law requirement unless the target LawDoc
      explicitly grants that override via a declared parameter.

      '
    ```
## Edges
| from | to | type | id | attrs | metrics |
| --- | --- | --- | --- | --- | --- |
| law://_kernel/law/lawprofile-k1 | def.profile_root | contains |  |  |  |
| law://_kernel/law/lawprofile-k1 | rule.profile_binding | contains |  |  |  |
| law://_kernel/law/lawprofile-k1 | rule.profile_no_weakening | contains |  |  |  |

## Contains Tree
- law://_kernel/law/lawprofile-k1
  - def.profile_root
  - rule.profile_binding
  - rule.profile_no_weakening
