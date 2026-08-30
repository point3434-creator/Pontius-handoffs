# Cold A initial independent inventory — r006

Recorded before opening `handoff.md` or implementer claims. Read-only production review.

Candidate: refs/heads/review/v0a-i01-impl/r006
Commit: c74b80628a89938ca585ef3240b5c267a7174d0f
Manifest SHA-256: 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f
Comparison: r005 a8582e6d6b53b55415dab79c4a54e252d00b74ad
Assigned snapshot: D:/pontius-snapshots/v0a-r006-cold-a-98fee7dce06d4fcca2da4475c550b928/harness

Read first: candidate.json, manifest.sha256, frozen CLAUDE.md, workflow.md and its
2026-08-30 amendment, ADR-0485, increment-one brief, ADR-0484, relevant status and
architecture/charter index material. Git HEAD equals candidate; initial status is empty.
The r005-to-r006 changed surface is replay.py, runtime.py, and test_v0a_replay.py.

| Independent requirement/risk | Observable behavior | Related paths and intended evidence |
| --- | --- | --- |
| First-failure ownership | Receipt primary cause is the first actual typed cause; cleanup cannot overwrite or precede it | runtime dispatch/rejection/operation ownership; replay event, settlement and publication owners; real fault schedules |
| Ordered later failures | Each later typed failure occurrence is retained in temporal order, including repeated codes; no duplicate classification of one raise | closure journal, exception propagation, receipt assembly; trace cause compatibility; real body plus cleanup schedules |
| Body versus cleanup clock failures | A clock failure raised while executing a host operation is retained exactly once and a known-broken clock is never queried to repair evidence | clock witness, measured-operation context manager, replay evaluation and settlement; invalid/reversed fault schedules |
| Public host containment | Ordinary host body exceptions return a typed failed ReplayOutcome instead of escaping; no subsequent host input after failure | ReplayHost.run, event iteration/dispatch, independent showdown evaluator and chip-depth oracle, trace builder/write boundary |
| Delivery/accounting integrity | Previously accepted actions and completed timing remain; incomplete accounting cannot become success, and publication/finalization failures are separate later causes | runtime dispatch/emission, mailbox, accounting totals, ReplayOutcome/HostCompletionReceipt, trace terminal |
| Public cause semantics | Failure categories identify the operation that failed; invalid input remains input failure, host settlement work maps to settlement failure, publication work maps to trace failure | model.FailureCode; ADR-0485 failure/receipt contract; changed runtime/replay classification sites |
| Frozen identity | Blob-based no-renames whole-row manifest matches the pair; checked-out CRLF is compared after in-memory normalization only | git blobs, candidate and manifest, module-resolution proof |
| Focused runtime support | Exact CPython 3.11.15 runs first, then exact 3.14.6, from this snapshot under -B -P and scrubbed exact environment | environment identity receipts, affected existing suites, independent production-path diagnostic if coverage requires it |

Initial uncertainties to resolve: which host operations own exceptions and when they
record them relative to interval closure; whether OperationFailed is swallowed only at
appropriate owners; whether duplicate journal entries represent distinct failures;
whether trace publication attempted after an earlier failure can falsely report success.

No finding or verdict yet. Prior work outside FIX R2-03 remains deferred. No production,
test, configuration, lifecycle, installation, broad/GPU suite, integration, or commit work
is authorized. Diagnostics/receipts remain cold-a-prefixed and append-only once issued.
