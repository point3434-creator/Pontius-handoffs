# Cold review: v0a-i01-impl/r003 — FIX round, slice 1 of 3

Candidate ref: `refs/heads/review/v0a-i01-impl/r003`
Candidate commit: `47d08d8c1556d776358e15811e3e98b859fd6a8b`
Manifest SHA-256: `cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a`
Base commit: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `35a6667ca3785e750324b3c93103a8994a6d7d6a`
Tier: C. Finalizer: Claude (first drafter). Reviewer: Codex.

**Round kind: FIX (scope-frozen).** This round changes only what the r002
findings in its slice require. No new surface was added — slice C admission,
boundary policy and CI remain outside, and their absence is scope, not a
finding. The ref is local and unpushed; r001, r002 and r003 are immutable.

## Slice

The r002 disposition proposed three correction slices. This is **slice 1 —
runtime authority and host failure closure: R2-01, R2-02, R2-03, R2-07,
R2-08.** Slice 2 (trace acceptance: R2-05, R2-06) and slice 3 (publication
and accounting: R2-04, R2-09, R2-10) are deliberately *not* in this candidate
and remain open. Reviewing them here is out of scope; their defects still
exist in the frozen bytes and are expected.

## Scope — four paths changed, six unchanged from r002

| Path | Status vs r002 |
| --- | --- |
| `src/pontius/v0a/runtime.py` | CHANGED |
| `src/pontius/v0a/replay.py` | CHANGED |
| `tests/test_v0a_contract_faults.py` | CHANGED |
| `tests/test_v0a_hand_replay.py` | CHANGED |
| `tests/test_v0a_replay.py` | CHANGED |
| `src/pontius/v0a/__init__.py` | UNCHANGED `86d349c4b79f150a4439df8d63c8d20854572895aaf7960f27647e7b1f198a8a` |
| `src/pontius/v0a/clock.py` | UNCHANGED `d229ca9a5a3f00ef73401b6aca415922840760dd62873759c50b3bfa95285ea4` |
| `src/pontius/v0a/model.py` | UNCHANGED `30aa2b8f7fbe86a7d106a27b3d52362b891a7ed0b222a858911e59e5d93301b0` |
| `src/pontius/v0a/trace.py` | UNCHANGED `ca994d35be0c2a2c368727cdc11abee7a71ba5e7f7d95e62fc24bc7e89ba03ed` |
| `tests/test_v0a_trace.py` | UNCHANGED `15b7cb1c06cf6468f7ec5dbab3e01366e177c76e806a7a61dfb6ac05387ef498` |

## Corrections

**R2-01 — policy authority.** Admission now requires the sealed
`ImmutableBlueprintActionSource` itself; an arbitrary object reporting the
right digest is refused with `TypeError` before a hand exists. Selection calls
the sealed implementation directly (`ImmutableBlueprintActionSource.action_for(
source, ...)`), so even a subclass override cannot answer a controlled
decision in place of the real table. The r002 false-hit delegate is rejected
at construction; a lying subclass is admitted but its override is bypassed and
the honest passive default is emitted. The digest is still bound once at hand
start and compared per selection — no second full-table rehash was added.

**R2-02 — established outer violations.** The snapshot returned by
`finish_transition_boundary` is a valid observation and is now latched through
a single `_record_established` helper, alongside the ready-to-emit checkpoint.
A deadline established at the boundary survives a clock failure on the very
next observation. `null` still means unknown, and `false` is never asserted.

**R2-03 — host closure.** A dead witness makes the ledger unusable, so
`bookkeeping` and `publication_interval` now degrade to explicitly unmeasured
instead of raising `RuntimeError` into the host — that raise was the escape
path. Every caught clock fault marks the ledger dead, finalization refuses to
drive a dead clock, and host success requires post-finalization accounting to
be complete. Faults injected at five points across a full fixture run — the
first observation, quarter, half, three-quarter, and the final two — never
escape and never report success.

**R2-07 — full settlement comparison.** The oracle now returns a complete
`OracleSettlement` (payouts, final stacks, pots with eligible seats) and the
host compares every field plus chip conservation. Oracles differing *only* in
final stacks, or *only* in pot eligibility, are each rejected.

**R2-08 — counting known deliveries.** The runtime tracks acknowledged
deliveries and exposes `accepted_delivery_count`; the terminal row uses it
instead of counting responses whose `failure_reason` is null. A real mailbox
acceptance followed by a sixteen-second acknowledgement now yields a failed
hand with `decision_count = 1`, end to end.

## Test rework this round required

Three delegate probes in `test_v0a_contract_faults.py` and one in
`test_v0a_hand_replay.py` asserted typed failures from objects the constructor
no longer admits. Their contract — a substituted policy must never answer — is
now enforced earlier and tested in `R2_01PolicyAuthorityTests`, including that
a sealed subclass override cannot intercept the sealed lookup. Those four
probes were removed rather than left broken, with a comment at each site
naming where the contract moved.

Timing injection moved out of the policy object entirely: both test clocks
gained `jump_at(read, ns)`, so elapsed time is scheduled at an exact
observation rather than inside a fake `action_for`. This is why the policy
input can now be sealed without losing any delay coverage.

## Evidence

RED before source: the five findings were reproduced as public-boundary
regressions against r002 (`checks/r002-RED.txt`). Focused GREEN from a fresh
disposable snapshot with asserted interpreter identity, scrubbed environment,
`-B -P`:

| Suite | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `test_v0a_hand_replay.py` | 35 | 35 |
| `test_v0a_trace.py` | 25 | 25 |
| `test_v0a_replay.py` | 25 | 25 |
| `test_v0a_contract_faults.py` | 22 | 22 |

107 tests per interpreter. Receipts in `checks/r003-receipts.json`.

Mutation probes (`checks/mutation-slice1.txt`): eleven mutations, eight
caught. Three survivors are all in the R2-03 accounting guards and are
**confirmed redundancy, not gaps** — removing both host guards *together* is
caught (recorded in the same file), so each single-guard mutation survives
only because the other still enforces the outcome. One earlier survivor was a
real gap — nothing bound the *host's* terminal count to a late delivery — and
is closed by the new end-to-end test.

## Open, by design

R2-04, R2-05, R2-06, R2-09 and R2-10 are untouched in these bytes. The
`settlement_oracle` seam the r002 disposition accepted is retained, and
`ReplayHost` now takes an optional `mailbox` on the same footing, so an
end-to-end late delivery can be exercised without a helper double replacing
the mailbox contract — the real `ActionMailbox` still performs acceptance in
that test.

## Review contract

Judge only slice 1. Weigh whether policy authority can still be defeated,
whether any valid outer snapshot's established truth is still discarded,
whether a clock fault at any stage can escape the host or produce a successful
receipt, whether the settlement comparison now covers the full contract, and
whether delivery counting matches acknowledged reality. CLEAN requires no
material finding in this slice surviving verification. Bind findings to this
commit and manifest, cite frozen locations, give a concrete failing scenario,
and name the smallest correction. Return attributed findings to
`reviews/review-<NN>-<reviewer>.md` and append one verdict line to
`../progress.md`.
