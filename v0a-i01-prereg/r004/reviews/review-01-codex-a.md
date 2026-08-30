REJECTED — one Important finding in the r004 handoff identity. Issuer: `/root/cold_review_r3_a`.

Declared pair:
- Commit: `98328440d4425fed1dbc7eb30b26b5f785709f05`
- Manifest: `402514df6aead93fc1495096d6f9647b0021992751b63566f90a695b89d2d8f0`

**I1 — Manifest rows use the wrong ordering. High confidence.**

[manifest.sha256](D:/Pontius-handoffs/v0a-i01-prereg/r004/manifest.sha256:1) lists STATUS, ADR, then amendment. The pinned [workflow](D:/Pontius-handoffs/v0a-i01-prereg/r004/inputs/workflow.md:97), including its `sorted(rows)` calculation at line 135, requires lexicographic ordering of entire rows. That puts the ADR hash `625…` first, amendment `c0f…` second, and STATUS `dcd…` last.

Concrete failure: independently hashing the frozen blobs and applying that required ordering yields:

`d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17`

This differs from [candidate.json:9](D:/Pontius-handoffs/v0a-i01-prereg/r004/candidate.json:9). A conforming verifier therefore rejects this handoff before accepting its bound verdicts. The individual file hashes are correct; their ordering causes the mismatch.

Smallest correction: publish an append-only corrected handoff with full-row sorting and the corrected manifest identity. Preserve r004 unchanged; no ADR source correction is needed for this finding.

I reviewed the whole candidate and found no additional material contract defect. Scope, base/tree identities, pinned-input hashes, LF/BOM checks, and `git diff --check` passed. Runtime behavior remains unverified; no tests, owners, or candidate edits were performed. The findings file and ledger append await their separate authorization.
