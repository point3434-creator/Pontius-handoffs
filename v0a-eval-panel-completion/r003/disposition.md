# r003 Codex finalizer disposition

Defect verdict: CLEAN. Design verdict: SOUND for the bounded raw-frame correction.
Review and broad-test gates are satisfied. Integration disposition: pending Claude's
controller-requested additional review and exact per-commit controller authorization.

Candidate: 7ca821802c949b047becf6599d603b3b63d51fa7
Parent: 430ad75de79cec13d66ff3dc4981dd3770a371b7
Tree: 3d2fe79d2af20125e322dd4a668335e789810863
Manifest: 1f48c97abcf4a0555418cd033bc9517292aac5d0188b1dfcf70b5e2b160d57fd
Ref: refs/heads/review/v0a-eval-panel-completion/r003

## Required correction and verdict basis

Parent I-01 is closed. frames_for now splits retained bytes on physical LF and admits
capture/frame limits before decoding. decode_frame enforces CR/BOM, byte, depth and
integer-token bounds, preserves duplicate/constant/finite-number checks, and translates
unexpected parser recursion to an unusable capture. Malformed raw input cannot acquire
chips or agreement credit merely because normalization produced a valid decoded record.

The received-record checks, kernel settlement replay, baseline divergence and later
agreement predicates have unchanged bytes. Valid CHECK hits, off-pool defaults and
reason-only disagreement preserve their original outcome/chip treatment. The actual
v2 premium control proves baseline divergence, not only a changed protocol label.

The r002 test-only RED has identical final test bytes against unchanged rejected code:
26 real-capture exclusion failures plus one missing-helper assertion, two unittest cases.
The integrated focused GREEN has 80 cases, zero skips, source verified on Python 3.14.6.
No count of subtests is presented as independent unittest cases or host campaigns.

The exact delta is two files: 37 additions/4 deletions in eval_agreement.py and 81 added
test lines in test_eval_protocol.py. Whole-slice totals are 2093 production and 1999 test
lines. The 3000 production ceiling is respected. Sealed host/session/codec, solver/export,
timing and ownership contracts are unchanged. No material r003 residual was established.

## Review qualification

Reviews 03 and 04 independently return CLEAN / SOUND, with no required findings. They
ran in separate ephemeral sessions with memory disabled per invocation, declared no
inherited history before reading, and sealed inventories before deferred coverage/checks.
Their hashes and launch-probe order are bound in checks/review-gate.json.

Reviews 01/02 also return CLEAN / SOUND, but inherited unrelated project memory summaries.
Their technical evidence and disclosures are retained unchanged. They are not counted
toward the strict cold gate. coordinator-note.md records the complete dispatch history,
including two pre-input utility failures, fresh replacement launches and exact-byte copies.
No other reviewer's verdict or inventory was provided as input to a qualifying reviewer.

## Nonblocking observations

Accept the following as evidence limits and future test opportunities, not new gates:
- The aggregate-cap negative also exceeds a frame bound; it does not isolate that guard.
- The Unicode-positive case uses escaped JSON. Literal UTF-8 string acceptance is static
  evidence; a future literal positive would improve symmetry with the separator negatives.
- The frozen host decoder is an independent authority for the changed classifier, while
  both share Python parsing. The wrapper does not execute the threaded stream reader.
- The deep-input case reaches the depth refusal, not an injected RecursionError handler.
- Retained host failure outcomes own transport, queue and cleanup facts absent from stdout.
- Generic summarize.complete resolves outcomes; primary campaign acceptance requires hits.

No observation demonstrates a surviving failure-before-credit violation. The explicit
raw admission boundary is simpler to verify than the previous normalization path. A
shared-parser extraction would alter sealed scope without a demonstrated necessary fix.
Future changes to the host contract must revisit the duplicated predicates and tests.

## Broad acceptance evidence

After both qualifying reports were issued, the full registered population ran in a fresh
detached snapshot at the candidate with locked dependencies and Python 3.14.6 only.
The scrubbed environment, -B -P, fatal ResourceWarning and fatal pytest unraisable warning
settings match the prescribed snapshot procedure. No selection filter was passed.

All 50 registered suites are accounted for: pytest 48 passed, 2 wholly skipped; unittest
633 total, 623 passed, 10 skipped, zero failures; exit 0. All skips explicitly name the
optional SciPy screen (2 sparse TT, 5 leaf CFR, 3 leaf evaluation). No eval-panel case
was skipped. Recorded test duration is 226.4005447 seconds; pytest wall is 227.07 seconds.

Source verification is true. Source-scope SHA-256:
bac14bea3e9a4e4c8c120556311447262d7775de54e39ef121c02bb2c59eb204
Retained result SHA-256:
3b9442a447501540168b3e755ae7d389c5bd8e3a3ae128e87bf0d4e5775e1152
checks/broad-gate.json records the exact retained result/journal paths, commands, source
identity, skip details and digests. Raw evidence remains in the evidence snapshot.

## Integration boundary

The controller asked for Claude's additional cold review while the Codex passes ran.
That report is pending at this disposition. Reconcile its findings against this same
frozen candidate before adoption; add a new disposition record if it changes this ruling.
Do not rewrite issued reviews or frozen input files. Another material residual returns
to the controller under the r003 stop rule; no implicit fourth correction round exists.

No ceremonial source commit, branch adoption, push or ref retirement occurred. Existing
master changes and other worktrees remain preserved. Any later adoption must name this
round/candidate explicitly after all requested review input has been reconciled.
Every retained solve/export/agreement phase still needs its own bound plan and one-shot
authorization. This disposition supplies no full-H, performance or playing-strength result.
