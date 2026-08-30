# r004 coordinator addendum — abort closure

Reviewer: Codex /root, 2026-08-30. Additional verification after cold A identified
the abort path; not an independent cold discovery.
Defect verdict remains NOT CLEAN. Design verdict remains STRAINED, now with
a broader bounded cause-flow correction than receipt projection alone.

Candidate: 0207430a37e1e5b31c8da8da7aa57da1bc5c88ee
Manifest SHA-256: ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef
Ref: refs/heads/review/v0a-i01-impl/r004

This append-only addendum preserves review-03-codex-coordinator.md unchanged.
It qualifies the earlier engineering recommendation with an additional verified
runtime closure path; it adds no new contract beyond R3-02.

## C-02 — Important: an abort-close clock cause is discarded

Frozen location: runtime.py:424-437, particularly _release_boundary's combined
except branch. The runtime detects _HandFailure, then closes its active boundary
before returning the first failure to the host. A clock exception during that
close is swallowed and never enters closure_failures.

Real public reproduction: create an ordinary Fixture via dataclasses.replace,
changing only fixture A's first scripted opponent seat from 4 to 5. This reaches
a validly constructed wrong-turn event after one genuine controlled action.
The normal host reports event_order. No subclass validation bypass, private
state mutation, method patch or fixture-schema defect is used.

Inject a raising, boolean or reversed public clock sample at read 16, which
is the real outer abort_transition_boundary closure following that event error.
Both interpreter slots return:
- failure_reason=event_order
- secondary_failures=()
- runtime.closure_failures=()
- accounting_complete=false; passed=false
- one real accepted action and one retained decision
- exactly 16 underlying source calls, with no retry.

Expected secondary is clock_invalid for a raising/boolean source and
clock_reversed for a reversed sample. The original event_order stays primary.
The first failure still returns honestly; the later closure cause is missing.

Controls: clock faults at reads 17, 18 and 19 on this same already-rejected
hand are retained correctly as secondary by the new publication/finalization
paths. Earlier faults retain the appropriate first clock cause. The standalone
wrong-turn control has no clock cause. No exception escapes the 56-fault sweep
(19 raising + 19 boolean + 18 reversal positions), plus one control, per slot.

## Required correction and refined design advice

Preserve all actual typed causes in their occurrence order, including failure
while aborting an already-rejected input. Do not promote cleanup failure above
the input failure that caused cleanup, and do not manufacture a second cause
by probing a witness already known to be dead.

Merely calling _record_closure_failure in _release_boundary is not sufficient:
the host currently drains runtime closure codes before appending the returned
dispatch failure, although that dispatch failure occurred before abort began.
Such a patch would exchange a missing secondary for a wrong primary.

The earlier report's drain-before-note advice remains valid for a genuinely
later host-detected cause, such as settlement comparison after bookkeeping
entry. It is not a general ordering proof for runtime failures reported after
cleanup. Prefer a bounded explicit ordered-cause transfer across the
runtime/host boundary: record the initiating failure before cleanup, append
actual cleanup failures once, and project first/rest without category priority.
A single owner or an immutable ordered batch are possible implementation
choices. Avoid parallel primary and closure lists whose chronology must be
guessed from when the host happens to receive them.

This changes cause accounting within the declared fix scope; it does not
require a whole ReplayHost/runtime rewrite or any sealed ledger change.
Preserve delivery records, clock-death behavior, outer intervals and existing
successful paths. Acceptance requires real public failed-input plus abort-fault
cases in addition to the happy-path clock sweep and both writer/clock orders.
Check duplicate-code preservation and no double insertion.

Evidence: checks/coordinator-abort-probe.py, coordinator-abort-run.py,
coordinator-311-abort.txt, coordinator-314-abort.txt and matching JSON receipts.
Actual CPython3.11.15 first, then3.14.6; exact preimport identity, -B -P,
snapshot cwd/src PYTHONPATH, scrubbed environment, absolute Git. Both snapshots
checks remained clean. Diagnostics assert/record observed behavior, not GREEN.
The primary coordinator report's 113 focused tests per slot remain valid.
