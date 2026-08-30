# Cold review: v0a-i01-impl/r004 — FIX round, R3-02 only

Candidate ref: `refs/heads/review/v0a-i01-impl/r004`
Candidate commit: `0207430a37e1e5b31c8da8da7aa57da1bc5c88ee`
Manifest SHA-256: `ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef`
Base commit: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `c5cf6cc281d2800727029737fd4ee05bd20ebbd3`
Tier: C. Finalizer: Claude (first drafter). Reviewer: Codex.

**Round kind: FIX (scope-frozen).** One contract only: **R3-02** — host closure
must report its typed cause. R3-01 (policy authority) is deliberately absent;
it is a second residual, its root-cause note is published at
`../R2-01-root-cause.md`, and it gets its own candidate.

Correction to the r003 handoff, which is preserved unedited: its heading said
"four paths changed and six unchanged" where the table and manifest correctly
showed five and five. Prose error only; identity was unaffected.

## Scope — three paths changed, seven unchanged from r003

| Path | Status vs r003 |
| --- | --- |
| `src/pontius/v0a/runtime.py` | CHANGED |
| `src/pontius/v0a/replay.py` | CHANGED |
| `tests/test_v0a_replay.py` | CHANGED |
| `src/pontius/v0a/__init__.py` | UNCHANGED `86d349c4b79f150a4439df8d63c8d20854572895aaf7960f27647e7b1f198a8a` |
| `src/pontius/v0a/clock.py` | UNCHANGED `d229ca9a5a3f00ef73401b6aca415922840760dd62873759c50b3bfa95285ea4` |
| `src/pontius/v0a/model.py` | UNCHANGED `30aa2b8f7fbe86a7d106a27b3d52362b891a7ed0b222a858911e59e5d93301b0` |
| `src/pontius/v0a/trace.py` | UNCHANGED `ca994d35be0c2a2c368727cdc11abee7a71ba5e7f7d95e62fc24bc7e89ba03ed` |
| `tests/test_v0a_hand_replay.py` | UNCHANGED `8603e88be2d874c77a6e9d2b732508f42be68a4fcd45d7921f30725810d8dfc3` |
| `tests/test_v0a_trace.py` | UNCHANGED `15b7cb1c06cf6468f7ec5dbab3e01366e177c76e806a7a61dfb6ac05387ef498` |
| `tests/test_v0a_contract_faults.py` | UNCHANGED `85c15ae71e6e5685124c7c9d276a94dd593ef96a0dd7a131e27b3ac8d0fd87e9` |

## Correction

Each of the five closure seams now routes its caught exception through
`_record_closure_failure`, which classifies it exactly as the dispatch path
does — `ClockReversedError` to `clock_reversed`, anything the witness has
normalized to `clock_invalid` — and appends it to an ordered list exposed as
`closure_failures`. The witness is never resampled to obtain a code; it comes
from the exception in hand. The r003 dead-clock and no-success guards are
unchanged; this round adds reporting only.

The host merges those causes with its own. Ordering is **correct by
construction** rather than by placing flush points well: `note()` drains any
already-retained runtime cause before appending a host-detected one, so the
sequence is real. The first non-reporting cause becomes `failure_reason` and
everything else keeps its order in `secondary_failures`.

An interpretation worth your explicit judgement: a post-delivery
`trace_write_failed` is never promoted to primary, even when it is the only
cause. ADR-0485 describes `secondary_failures` as preserving reporting failures
"without replacing the first cause", and a write failure occurs after the
hand's outcome is already determined. The consequence is a receipt with
`passed=false`, `failure_reason=null`, and the write failure in
`secondary_failures`. If you read the ADR as requiring a non-null
`failure_reason` on every unsuccessful receipt, say so — it is a one-line
change and I would rather be told than guess.

A `RuntimeError` from the ledger marks the ledger dead and accounting
incomplete but appends no code, because the frozen vocabulary has none for it
and inventing one would be a lie. In practice it only follows an earlier clock
fault whose code is already retained; I could not construct a case where it
occurs first.

## Evidence

RED against r003 first. Focused GREEN from a fresh disposable snapshot with
asserted interpreter identity, scrubbed environment, `-B -P`:

| Suite | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `test_v0a_hand_replay.py` | 35 | 35 |
| `test_v0a_trace.py` | 25 | 25 |
| `test_v0a_replay.py` | 31 | 31 |
| `test_v0a_contract_faults.py` | 22 | 22 |

113 tests per interpreter; receipts in `checks/r004-receipts.json`.

The load-bearing test is the **sweep**: every observation of fixture A, faulted
three ways (invalid sample, reversed sample, raising source) — 414 runs —
asserting that any receipt with `passed=false` names a cause. That generalises
instead of pinning the five positions the r003 review reported, which is the
mistake that produced this residual in the first place.

Also covered: both clock kinds at each of the five seams; both orderings
(clock-before-mismatch keeps the clock primary and the mismatch secondary;
mismatch-before-clock keeps the mismatch primary); no resampling after death;
and accepted actions plus their decision records surviving a closure fault.

Mutation probes (`checks/mutation-r004.txt`): six mutations, all six caught.
An earlier design had three redundant flush points, two of which survived
mutation because a later drain recovered the same causes; rather than document
that redundancy I removed the flush points and made ordering correct by
construction, after which every mutation bites.

## Review contract

Judge R3-02 only. Weigh whether any fault position can still produce an
unexplained failure, whether the ordering is genuinely occurrence-based rather
than reconstructed, whether a dead witness is ever resampled, and whether the
trace-write interpretation above is right. R3-01 and the deferred R2-04/05/06/
09/10 are out of scope and their defects are expected in these bytes.

Please also state the required design verdict — SOUND, STRAINED, or WRONG
SHAPE — under the amended `docs/workflow.md`, even if the defect verdict is
CLEAN. Given this contract's history I would rather hear "wrong shape" now than
after a third attempt.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md` and append
one verdict line to `../progress.md`.
