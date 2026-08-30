# v0a-i01-impl slice A — implementer self-report

Implementer: Claude (drafter/finalizer this checkpoint). Date: 2026-08-30.
Base: master `b357d333fc2393b7fc7dcf31f30c86616208c817`.
Worktree: `D:/Pontius-worktrees/v0a-increment-1`, branch `v0a/increment-1`.
Status: focused GREEN, not frozen, not committed, no authority claimed.

## What slice A contains

| File | Lines | Responsibility |
| --- | --- | --- |
| `src/pontius/v0a/__init__.py` | 1 | Inert package surface; no execution, no optional imports |
| `src/pontius/v0a/model.py` | 527 | Frozen event/action/envelope/receipt/record/outcome values with exact validation |
| `src/pontius/v0a/clock.py` | 69 | One validated monotonic witness, retained last sample, permanent failure |
| `src/pontius/v0a/runtime.py` | 781 | Visible-state transitions, blueprint outcomes, emission boundary |
| `tests/test_v0a_hand_replay.py` | 918 | 36 slice-A contract tests |

Total 2,296 new lines — inside the brief's 2,500–4,000 budget for the whole
increment, and below the ~3,000-line proactive-slicing threshold for this
candidate. No sealed byte changed; no file outside these five paths exists
in the worktree diff.

## Contract decisions worth the reviewer's attention

1. **Wall start.** `wall_start_ns` is the sealed ledger's own
   `boundary.started_ns` from `start_transition_boundary()`, which is the
   first runtime operation of every dispatch — before input validation,
   card construction, and V2 work. Emission time is
   `witness.last_returned_ns` immediately after `outer.finish_action()`,
   i.e. the exact sample the closing snapshot used, never a fresh read.
   The runtime then *enforces* `(emission - start)/1e9 ==
   snapshot.action_wall_elapsed_seconds` and fails closed with
   `clock_invalid` if they ever disagree.
2. **Cutoff predicate is ledger-derived**, not an ad hoc comparison:
   `snapshot.work_remaining_seconds <= 0.0` at the ready-to-emit checkpoint
   (after validation and envelope construction, before V2 emission). Given
   the sealed constants this fires at exactly 14.000000000 s and later,
   and the 14–15 s reserve remains lawful emission time.
3. **Blueprint classification uses the real table, never message text.**
   `select_blueprint_action` validates the decision context first
   (`BlueprintDecisionKey.from_state`), calls the unchanged `action_for`,
   then re-checks legality. When `action_for` refuses, the classifier asks
   whether a *matching* entry exists whose action is illegal in this exact
   decision: yes → `invalid_blueprint_entry`, no → `invalid_decision_context`.
4. **Delivery outcomes.** `MailboxRejectionError` → `delivery_rejected`
   (`rejected`, no delivered action); any other exception after publication
   → `delivery_ambiguous` (`unknown`, never retried). A clock failure after
   real acceptance keeps the full decision record with interrupted timing
   and `delivery_status=accepted`.
5. **Interrupted timing never lies.** Null emission/elapsed/seconds, and
   cutoff/deadline flags are `None` rather than `False` — the value object
   rejects a `False` flag on an interrupted record outright.

## Evidence

**RED before source.** The suite was written first and failed deterministically
with `ModuleNotFoundError: No module named 'pontius.v0a'`.

**Focused GREEN, disposable snapshot, dual interpreter** (fresh
`--no-hardlinks` clone with `core.autocrlf=false`, detached at the base
commit, working bytes overlaid, scrubbed environment, snapshot `PYTHONPATH`,
absolute `PONTIUS_GIT`, `-B -P`, child interpreter identity asserted before
payload execution):

| Interpreter | Identity | Result |
| --- | --- | --- |
| CPython 3.14.6 | asserted before run | 36 tests, exit 0 |
| CPython 3.11.15 | asserted before run | 36 tests, exit 0 |

Overlay digests are recorded per file with the base commit in the run
receipt. Nothing ran from the primary checkout.

**Mutation probes.** Because the suite passed on its first implementation
run, eight mutations were injected to prove the tests bite. Six were caught,
one was a clean no-op control, and one survived:

| Mutation | Result |
| --- | --- |
| Work cutoff never fires | CAUGHT (3 failures) |
| Deadline never fires | CAUGHT (2 failures) |
| Wall started at the decision instead of the event boundary | CAUGHT |
| No-op control | correctly clean |
| Private-pair ordering unchecked | CAUGHT |
| Raise-amount validation removed | CAUGHT |
| Clock-reversal check removed | CAUGHT |
| Controlled-seat-as-opponent guard removed | **SURVIVED** |

The first late-start probe was an equivalent mutant (both expressions read
the same sample); it was replaced with a genuine one — starting the wall at
the decision — and a `TickingClock` test that pins the wall to the ledger's
event-arrival observation now catches it.

## Open item for the reviewer

**The controlled-seat guard is unreachable independently.** In
`_dispatch_opponent_action`, the check "`event.seat == controlled_seat` →
`event_order`" can never fire distinctly: the controlled seat's decision runs
inline within the dispatch that makes it the actor, so it is never pending
between dispatches, and any such event is already caught by the wrong-actor
check with the same typed code. I kept it as defence in depth and documented
the subsumption in the test, but checklist v1 item 6 argues for either an
injected execution or removal. I did not manufacture a helper double to
"cover" it. Reviewer's call: keep with the comment, or delete as dead code.

## Not done in slice A

Trace serialization and digests, semantic projection and replay, the
explicit-deal host with fixtures A/B, the independent settlement oracle,
terminal accounting with the host completion receipt, boundary-policy
classification, inventory admission, and the CI gate. Those are slices B and
C. No rehearsal or production identity exists; no experiment authority is
claimed or implied.
