# Root-cause note — R2-03 host failure closure, before a third fix attempt

Author: Claude, 2026-08-30. Required by `docs/workflow.md`: second residual on
one contract (r002 R2-03 → r003 R3-02 → r004 R4-01/R4-02). No source edited;
this note is the precondition, not the attempt.

**Design verdict I accept: STRAINED**, as the coordinator reconciled it. Cold
reviewer B's SOUND dissent is preserved and is not unreasonable — the queue and
cursor shape is fine in isolation. What is strained is the *plumbing between
three channels*, and R4-02 is the proof: the host receipt's order cannot
recover the runtime's own initiating-then-cleanup order, because by the time
the host learns of the initiating failure the cleanup cause is already sitting
in the shared list.

## 1. Why r003 and r004 both missed — one error, twice

**r003** was told the host swallowed clock faults and produced false success. It
fixed exactly that: guards that prevent escape and prevent `passed=true`. The
typed cause was discarded because I was working the symptom list I had been
handed — escapes, false success — and treated "what went wrong" as incidental
to "did it fail safely".

**r004** was told the cause was missing at five named seams. It retained causes
at those five seams. The abort path is also a closure seam; it was not on the
list, so it was never considered.

The shared error: **I worked from the reviewer's enumerated positions instead
of from a definition of the category.** r003's list became r004's world. This
is the same error as R2-01's, in a different subsystem — fix the reproduction,
inherit its boundaries, miss the sibling case. Two contracts have now failed
this way, which makes it a habit rather than an accident.

A second, independent error compounds it: **every fault schedule I have ever
written injects exactly one fault into an otherwise-valid hand.** Even the
r004 sweep — which I offered as the general test — is 414 *single-fault* runs.
A single-fault suite verifies single-fault behaviour and says nothing about
interaction. Both r004 findings are compound: a write failure *then* a clock
fault, and a rejected input *then* a cleanup fault. Neither could have been
caught by any test in the suite, however many positions it swept.

Third, on R4-01 specifically: I derived a category rule — reporting failures
never become primary — from one ambiguous ADR sentence, and shipped it as the
default while asking for a ruling. Flagging it was right; making it the
implemented behaviour rather than taking the conservative reading was not. The
conservative reading was available and simpler: first cause wins, no
categories. Where an ADR is ambiguous, the implementation should take the
reading that adds no new rule.

## 2. The structural cause

Three channels carry failure information and they are merged by collection
time, not occurrence time:

| Channel | Produced at | Reaches the host |
| --- | --- | --- |
| initiating failure | inside `dispatch`, returned as `DispatchOutcome.failure` | when the host inspects the return value |
| cleanup failure | inside the same `dispatch`, during `_release_boundary` / interval close | via the shared `closure_failures` list |
| host failure | in `ReplayHost.run` itself | appended directly |

Within one dispatch the initiating failure happens *first* and its cleanup
failure *second*, but the cleanup cause lands in the shared list immediately
while the initiating cause only surfaces on return. My `note()`-drains-first
rule then flushes the cleanup cause ahead of the initiating one — correct for
every schedule I tested, wrong for exactly the schedule I did not.

"Correct by construction" was true only for the construction I had in mind.

## 3. What the next attempt must do

The coordinator's bounded refactor is the proportionate intervention and I
adopt it. A whole-host rewrite would disturb working event, delivery and
timing paths for no evidence-backed reason; another isolated catch would leave
the cross-channel ordering intact.

1. **An operation retains its initiating cause before it runs cleanup.** The
   failing operation owns its own ordering: initiating cause first, then any
   cleanup causes it actually produced, appended once.
2. **The ordered sequence transfers explicitly to the host** as one immutable
   batch per operation, rather than the host reconstructing order from a
   shared list plus a return value.
3. **The host appends its own later causes and derives first/rest with no type
   ranking.** R4-01 disappears because the category rule disappears.
4. **The abort path is inside the contract**, not adjacent to it: every place
   the runtime closes a boundary or interval is a closure seam, defined as such
   rather than enumerated.

Preserved unchanged: sealed ledgers and spine, timing ownership, the
dead-clock and no-success guards, delivered envelopes and their decision
records, successful fixture behaviour, and the existing frozen failure codes.
Named transition risks: duplicate causes, wrong order across the runtime/host
boundary, synthetic codes from re-querying a dead clock, and dropping a
decision record during transfer.

## 4. How to test the class rather than the positions

The test change matters more than the code change, because the code has now
been correct-for-the-tested-cases twice.

- **Compound schedules are the default, not an extra.** Generate pairs: a
  rejected input whose cleanup faults; clock-then-mismatch and
  mismatch-then-clock; write-only; write-then-clock and clock-then-write;
  repeated identical codes, asserting they are not silently deduplicated.
- **Order is asserted against occurrence, not against my expectation.** Each
  compound schedule states which event genuinely happened first and asserts the
  receipt agrees.
- **Seams are discovered, not listed.** A test that enumerates every call site
  where the runtime closes a boundary or interval and asserts each is routed
  through the cause-retaining helper would have caught the abort omission
  statically, without knowing it existed.
- **No-fault controls stay**, so the refactor cannot buy correctness by
  reporting failures that did not occur.

The third item is the one that generalises: it converts "did we remember this
seam?" from a matter of recall into something the suite checks.

## 5. Residual risk and honest limits

The bare ledger `RuntimeError` still has no typed code, and both the reviewers
and I failed to construct a schedule where it occurs as a first fault. It
remains unrepresented rather than mislabelled, which I believe is right, but it
is an untested corner.

The compound space is combinatorial and I will not enumerate all of it. I plan
to cover ordered pairs across the distinct channels plus the specific triples
the reviewers named; three-fault interactions beyond those are not covered, and
I will say so in the candidate rather than imply completeness.

Finally: two contracts have now failed twice each with the same underlying
habit. If the next attempt on either one leaves it open, the honest conclusion
is not a fourth patch but that I am the wrong shape for this work — at which
point the controller should consider whether these contracts want a different
implementer or a different decomposition.
