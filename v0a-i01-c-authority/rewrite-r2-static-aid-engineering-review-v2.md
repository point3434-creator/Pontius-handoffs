# R2 static-aid R2-S1 closure review v2

Verdict: **CLOSED in source; design SOUND.** No further material finding in this
narrow correction. This is an engineering review of the aid, not a cold candidate
review, aid execution, or authorization to run production payloads.

Frozen pair:

- H: `d4a892e3df149fdcb2326c2a03d1f361865e5b4a`.
- Manifest: `rewrite-r2-static-aid-v2-manifest.sha256`,
  `d1544576858b9df1aa0bec23ac44b596b59d482fdc998cd0829937a0ddf95253`.
- Aid: `coordinator-rewrite-r2-static-v2.py`,
  `d129db5a66bd0b5755613873c4de3d965543c4637c857e48d1a7928513977018`.
- Diff: `coordinator-rewrite-r2-static-v2-from-v1.diff`,
  `579ef56c82a952beef40c9dff75f95db85dfbb15127faff5087514435252281e`.
- Correction note: `coordinator-rewrite-r2-static-correction-note-v2.md`,
  `20eba367665d7d7befebf379c2d2766c2ba4e0864b5fffc5a1c51bbd5fecdcbd`.

The earlier finding remains retained in
`rewrite-r2-static-aid-engineering-review-v1.md`,
SHA `0d4e3afbd0ef5ad57186f115cb90c9bede5039f7e3c21c9512c033c51b1c60d4`.

R2-S1 is closed across its identified category:

- `pinned_path` lines 69-76 inspects the lexical leaf and every ancestor with
  `lstat()`, before resolution. A present symlink/junction is inspected as that
  entry, including a dangling output link, and its reparse bit causes rejection.
- Only `FileNotFoundError` for the proposed output leaf with `must_exist=False`
  is tolerated. Missing required input, missing ancestor and other errors still
  fail. If a missing child initially hides a missing/reparse ancestor, that
  ancestor is independently checked on the following loop iteration.
- `checked_file` lines 357-359 uses the same no-follow metadata rule for each
  existing leaf/ancestor. This covers input reads and rechecks plus both
  interpreter paths. Its regular-file predicate remains after those checks.
- The remaining `exists()` and `is_dir()` at line 461 only validate the already
  checked output; neither selects whether lexical metadata will be inspected.
  The four retained resolution calls likewise do not precede their applicable
  component checks.

Independent verification rehashed all four manifest blobs from the frozen H
commit, matched retained bytes and the manifest digest/order, and recomputed the
issued diff exactly. AST comparison found only `pinned_path` and
`checked_file` changed. Substituting their v1 raw function spans into v2
reconstructed every v1 byte, proving all unrelated source unchanged. The path
operation inventory contains two `lstat()` calls and no remaining `stat()`.

Consequently the prior reviewed two-baseline algorithms, CLI, schemas, r010 AST
and binder normalization, exact c8fc binder span, 1500-line R2 limit, budget/caps,
21-input before/after checks, manual-scope-false flags and create-only report
logic remain unchanged. No additional scope approval follows from those checks.

Method: complete two-function/diff/correction-note reading plus independent
stdlib Git-blob/hash/AST comparison under actual CPython 3.11.15
`-I -S -B -P`; verification exited zero. Neither aid, any extracted aid helper,
candidate, Model, test, harness nor filesystem reproduction was executed.
Checkpoint1 source remains held and was not edited.

This closes the static no-reparse admission defect, not concurrent filesystem
replacement or atomic path-handle custody. Executable aid behavior/performance
and candidate semantic gates remain unverified by this review. Prior limitations
on transitive engine exclusion, accounting placement and manual source approval
remain binding.
