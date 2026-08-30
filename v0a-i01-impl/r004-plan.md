# r004 plan — R3-02 host closure must report its typed cause

Author: Claude. Date: 2026-08-30. Status: plan only; no source edited yet.
Contract: R3-02 (maps to R2-03), **first residual** — no isolation required,
so this proceeds as an ordinary scope-frozen FIX round in its own candidate.
R3-01 (policy authority, second residual) is deliberately **not** in this
candidate; it is blocked behind its own root-cause note.

## What r003 got right and what it left undone

The r003 guards achieved what they were written for: across the coordinator's
1,256 fault schedules there was no ordinary exception escape, no false success,
and no lost accepted-decision record. What they did not do is *say what went
wrong*. At `runtime.py:288, :298, :321, :331, :364` the caught clock exception
sets dead-clock and incomplete-accounting state and is then discarded, so the
receipt built at `replay.py:571-585` carries `failure_reason=null` and
`secondary_failures=()` for a hand that demonstrably died on its clock.

ADR-0485:269-280 requires the primary cause to be retained and later typed
failures to be collected in order. Silence is not fail-closed; it is a hand
that failed without saying why.

The coordinator's missing-cause positions are the last five observations of
each fixture (A: 134–138 of 138; B: 68–72 of 72) — exactly the post-terminal
bookkeeping, publication, and finalization seams, which is where r003 added
degradation and therefore where the cause is dropped.

## The five seams

| Seam | Location | Currently |
| --- | --- | --- |
| bookkeeping entry | `runtime.py:288` | cause discarded |
| bookkeeping exit | `runtime.py:298` | cause discarded |
| publication entry | `runtime.py:321` | cause discarded |
| publication exit | `runtime.py:331` | cause discarded |
| finalization | `runtime.py:364` | cause discarded |

## Correction

The runtime accumulates an **ordered tuple of typed closure failures**. Each of
the five catch sites classifies its exception exactly as the dispatch path
already does — `ClockReversedError` to `clock_reversed`, everything else the
witness normalizes to `clock_invalid` — and appends it. The witness is never
sampled again to obtain it; the code is derived from the exception in hand.

The host reads that ordered tuple when building the receipt and merges it under
ADR-0485's rule: if no primary cause exists yet, the first closure failure
becomes `failure_reason`; every remaining one, and every closure failure that
arrives after a primary already exists, appends to `secondary_failures` in
occurrence order. A pre-existing primary is never overwritten — the mismatch
case must keep reporting `settlement_mismatch` first and gain the later clock
code as a secondary, and the clock-first case must keep `clock_invalid` as
primary and report the later mismatch as secondary.

Both orderings the reviewers reproduced are therefore covered explicitly:

- bookkeeping clock fault → settlement mismatch: primary stays `clock_invalid`,
  secondary gains `settlement_mismatch`;
- settlement mismatch → publication clock fault: primary stays
  `settlement_mismatch`, secondary gains the clock code.

The r003 dead-clock and no-success guards stay exactly as they are; this round
adds reporting, it does not relax any protection.

## Test plan (RED against r003 first)

1. Every one of the five seams, faulted with **both** an invalid sample and a
   reversed sample — ten cases — asserting the exact `failure_reason` and
   `secondary_failures`, not merely `passed=false`.
2. The two orderings above, asserting primary retention and secondary append.
3. Accepted-action retention across a closure fault: the decision record and
   the mailbox acceptance both survive, unchanged from r003.
4. No further witness read after failure — assert the observation count does
   not advance once the clock has died.
5. A sweep over every observation of fixture A, asserting that a fault at any
   position yields a receipt whose cause is non-null. This is the coordinator's
   own probe shape and is the test that would have caught the r003 gap; it
   generalises rather than pinning the five known positions.

Item 5 is the one that matters for not repeating the pattern: pinning only the
five reported positions would be another point fix.

## Not in this candidate

R3-01 policy authority; R2-04/05/06/09/10; slice C admission, boundary policy
and CI. The sealed kernels and the legacy dependency baseline stay untouched.
