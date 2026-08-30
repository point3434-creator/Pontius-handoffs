# v0a-i01-impl/r006 disposition

Coordinator: Codex /root, 2026-08-30. Finalizer for this candidate: Claude.
NOT CLEAN: two Important failure mechanisms of the same R2-03 contract.
Design: STRAINED. No source integration or broad-suite advancement.

Candidate: c74b80628a89938ca585ef3240b5c267a7174d0f
Manifest SHA-256: 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f
Ref: refs/heads/review/v0a-i01-impl/r006
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: a22414541973b76ddd1efa1ca8fc41f51b7a4065

Full blob identity and manifest verify; only runtime.py, replay.py and
test_v0a_replay.py changed from r005. Both cold reviewers recorded independent
inventories before reading the coverage narrative. The coordinator's additional
checks and post-review scope adjudication are not a third cold review.

## R6-01 — failed-witness refusal invents a second clock cause

Important / Medium, high confidence. Attribution: cold B B1, independently
reproduced afterward by coordinator C03. Frozen runtime.py:414-416, interacting
with the entry-failure branch at :337-344.

Fail the real shared witness at settlement interval entry, then sample it from
the public oracle. The underlying source fails once and is never retried.
The later refusal from the dead witness is nonetheless journalled as a new
clock_invalid cause. Expected one cause; actual [clock_invalid, clock_invalid]
or [clock_reversed, clock_invalid]. A/B and all three source fault kinds
reproduce on both interpreters. Four/two prior deliveries survive.

Required: distinguish the genuine original occurrence from the synthetic refusal.
Do not replace this with enum deduplication, and do not drop fresh body-origin
clock faults; those are the opposing r005 controls that r006 now fixes.

## R6-02 — failure normalization can escape without a completion receipt

Important / Medium, high confidence. Attribution: cold A R6-A01, cold B B2,
and coordinator C02. Frozen runtime.py:416 and duplicated conversion at :429.

The owner evaluates str(error) while constructing OperationFailed. A body
ValueError with an argument whose string conversion raises escapes run() after
the original settlement_mismatch was recorded. The caller gets no completion
receipt after real actions were delivered. Both cold reviewers and coordinator
confirm the escape on 3.11.15 and 3.14.6. Ordinary message controls are contained.
Cold A's immutable-blob r005 comparison is a counterfactual diagnostic, not
separate baseline acceptance evidence.

Required: the adapter must retain and transfer the original body failure without
depending on fallible diagnostic rendering. Return the failed host outcome,
preserve accepted actions and retain genuine later causes in order.

The coordinator additionally exercises exception-defined __class__ during the
new isinstance classification: it can raise before a cause is retained or
mislabel an ordinary Exception as clock_reversed. These observations inform
the same error-inspection boundary; they are not a third contract. Inspect the
whole conversion/propagation route, including context-manager behavior, rather
than treating removal of one str call as proof of class closure.

## Scope adjudication — no third gate from fabricated markers

The coordinator's initial report counted an unowned/foreign OperationFailed
marker as required C01. The append-only review-04 addendum withdraws that required
status. OperationFailed documents that retention has already happened; direct
fabrication violates that meaning, and supported cross-runtime propagation has
not been established. Cold B's post-verdict scope advice informed this decision.
The observations remain design advice about owner-bound provenance, not a new
acceptance gate. No issued report, receipt or ledger was rewritten.

Same-runtime nested preparation intervals are also not a new requirement: the
sealed ledger does not promise nested intervals. Unchanged event/trace/
pre-settlement observations stay deferred. Policy authority and
R2-04/05/06/09/10, plus the separate value audit, retain their prior standing.

## What passed and what the evidence establishes

Both r005 mechanisms are fixed: a normal body exception precedes its cleanup
fault, and a genuinely fresh body witness failure reaches the receipt.
All three passes ran the four focused suites: 123 tests per interpreter
(35 hand replay, 25 trace, 41 replay, 22 contract faults).

Coordinator repeats 628 single-clock fault schedules, 56 rejected-event clock
schedules, real writer refusals, 56 body-error/entry/exit/writer combinations,
and direct-witness controls. The new entry-echo schedules expose R6-01; exception
normalization probes expose R6-02. Detailed counts and explicit unadjudicated
observations are in review-03 and its receipts. Do not sum overlapping campaigns.

Tests passing by presence alone can miss extra causes. Retain independent
observations of actual source faults and compare the complete cause sequence.
The AST guard catches raw-interval spellings; it is useful supporting coverage,
not proof of origin, retention or a safe error adapter.

Actual CPython3.11.15 ran first, then3.14.6; identities were asserted before
payload imports. Fresh D-local clones, -B -P, exact snapshot cwd/src PYTHONPATH,
scrubbed environments and absolute Git were used. Source snapshots stayed
unchanged. No production edits, optional dependencies, GPU, broad suites,
experiments, source commits or performance/acceptance claims.

## Design and next ownership

The contract itself is coherent (cold B calls that SOUND); the implementation
design is STRAINED in both cold reports. Placement inside the measurement
boundary and the journal are worth retaining. The bounded redesign target is
the error adapter: carry verifiable origin/retention state, make classification
and transfer safe, and share the rule across both owned operations. Preserve
the hand loop, sealed ledgers/spine, timing ownership and complete deliveries.

Verification must cover fresh fault versus failed-witness refusal, normal versus
fallible message/metadata, before versus after cleanup, and exact multiplicity.
This is advisory technique; the required outcomes above bind the successor.

R2-03 remains open for a fourth residual. The r006 handoff records the controller's
condition that another unresolved attempt changes implementation hands. Carry
that condition forward: no fifth attempt is assigned to the current author.
The next owner should receive the frozen pair, this disposition, the failing
diagnostics and passing controls. No new implementer is appointed and no rewrite
is started by this review. Replacement is bounded to failure handling; the
evidence does not justify throwing away the complete hand implementation.

## Issued records

- review-01-codex-a.md:
  db1a8022b8765891e7f401ff8944d6f0245e587a56b7b31cc3406e8c82b1eab4
- review-02-codex-b.md:
  88a5e3f0e29e30942a5afbb011049efdadf55daf59761f01cc4e93da1436d3dd
- review-03-codex-coordinator.md:
  647df51dedb689cc9f05d014d9f4d7dac84f3884d954329ceb8ab601126c7142
- review-04-codex-coordinator-addendum.md (effective scope correction):
  6f755df555c516c686fde6f4d27b34992748803f9cfb880a613aa6555c6aa382

All reports are under reviews/. Each issuer appends its own bound task verdict;
this is the single program disposition. Routine packet publication commits only
review records and navigation, never the primary source candidate.
