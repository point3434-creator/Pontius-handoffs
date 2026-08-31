# R1 Task1 cost and ownership engineering review v1

Scope: read-only inspection of the 451-line, unwired state-primitives insertion.
This is not cold-review CLEAN, runtime verification or production fitness evidence.

Frozen handoff: H commit0223e38b933d5c0d1004ab2d26e261c3439b8870;
manifest rewrite-r1-task1-v1-manifest.sha256:
8c7ab0c6237c6518b0bcfab85be2157c0406ccc3c1a7e16c7323c2b5af5cab34.
Source rewrite-r1-task1-source-v1.py:
ff889b1ee3595d23d2109d15d87f80d8f5c153b3db524aaef3eb53b1797dcab1.
Diff rewrite-r1-task1-from-r010-v1.diff:
bdd2b7a0cd7c4985b26290e2a19592d6496e4ffa01607a316ab0bd32fb5438f1.
Companion ledger rewrite-r1-task1-ledger-v1.md:
7a660a6ead08338e840f6db0e9d6a1bcbc1258ef0ea3b271017746bd2c0bb592.

All five manifest entries were independently rehashed. Removing source lines
9077–9527 inclusive reproduced the exact r010 source29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
Thus every original byte, including budget/caps/binder/public execution, is
unchanged. Static parsing and hash inspection only; no primitive, candidate,
fixture, Model, test or controller payload was executed.

## Two pre-wiring corrections

1. _c_choice9485–9487 returns a reason-bearing unknown for an empty alternative
   set. That result does not itself retain an _CIssue or refuse; an ignored
   result could lose the impossible-state signal. Root identified this boundary
   and this review agrees. Use the approved explicit InventoryError path in a
   successor, not a harmless unknown or an assertion about future callers.
2. _c_choice9488 charges n final-copy visits before9489 container(n) performs
   the existing4096 size guard. If the size guard refuses, tuple(values) is
   never eligible for execution; the preliminary copy charge describes
   unperformed work and can make the work refusal precede the size refusal.
   Perform the container guard/charge first, then the additional copy-visit
   charge before tuple(values). Valid-input totals stay unchanged. This is
   distinct from retaining an actual throwing work request, which is required.

Root accepted both targeted corrections before evaluator wiring. They are
static contract/accounting findings, not claims of an executed product RED.
This review binds v1; it does not automatically approve the uninspected successor.

## Bounded design assessment

The implemented ownership mechanism is sound under the stated internal API
invariants. Snapshot9323 and fork9330 rotate the continuing parent's token.
Frozen wrappers are not retagged. Ownership helpers9339/9348 create a fresh
dictionary/wrapper when shared; cell write9391 separately checks and detaches
the addressed activation bank. A copied outer table alone does not authorize
mutating its still-shared banks. Current views and sibling states keep old data.

Current ctx supplies every charge. Tables, banks, views and arena store no
construction-time budget. Recursive/cross-stage callers must continue supplying
the correct existing owner, and the single arena per public analysis must remain
shared across all contexts; those future construction sites are not present yet.
Given that invariant, the monotonic allocator cannot collide across forks.

Copy cost3n+1 includes allocation, n entry visits and2n key/value references.
Fixed state16, snapshot6 and fork8 counts reconcile with their field/allocation
operations. Outer-table detachment costs6+3n including ownership check; addressed
bank copying is charged separately. These are semantic allocation/reference/
visit units, not Python allocator or CPU-instruction counts.

Trace link9503 retains two predecessor edges at fixed7 units including its
trace node; it does not flatten historical prefixes. Join9510 preserves ordered
tagged outcomes and deduplicates only object identity. For n supplied and m
unique outcomes its declared work is3+3n+6m. It introduces neither a fresh budget
nor a new path cap. Choice remains subject to the existing container guard.
Dataclasses use eq=False; choice keys contain scalar/type/identity components,
not nested semantic records. No implicit deep record equality was found.

## Remaining implementation obligations

Mapping-bearing records must use copied/proxied immutable contents; annotations
and frozen outer dataclasses alone do not make a supplied dictionary immutable.
The future mutation inventory must restrict all backing-table/bank writes to
the canonical helpers. Future constructors must separately meter their records,
fields, capture/default/member collections and exact scalar/reference domains;
the object insertion helpers intentionally do not charge an already-made record
twice. None of this future work is claimed implemented by this checkpoint.

Every call snapshot may force a full growing object/cell table copy on a later
write. That cost is visible and paid here. The design has no proved sparse-cost
or headroom claim; Gate B remains the real analyzer fitness checkpoint.
No additional current ownership blocker was found beyond the two corrections.
