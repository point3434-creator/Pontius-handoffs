# v26 remedy clarification v2: A+B only

Addendum to engineer-v26-cost-remedy-plan-v1.md, SHA256
e32d45c914cf9422429f493b3dfec475e23d05d58f957dca896ec95b75bb2d93.
Root verification remains coordinator-v26-depth-budget-verification-v1.json,
SHA256 2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30.
All anchors below bind exact v26 source
1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951.

This narrows the proposed next candidate to T/engineer-generator-v28-storage.py
from v26, A+B only. It does not grant source or dispatch authority. Semantic v25/
v27 remains separate; existing issued sources, artifacts and expectations remain
immutable. C is reserved for a later explicitly approved experiment.

## A: existing-branch freeze, ownership and accounting

For an existing immutable radix branch, copy its packed children into unpublished
working storage. Read the immutable base bitmap/pending total once, then visit
each changed slot once. Freeze only changed descendants. The old child for that
slot comes from the immutable base; do not subtract an already-updated pending
count. Rank insertion/deletion/replacement against the evolving working bitmap,
not stale original indices. Derive pending total from base plus old/new changed-
child deltas. Preserve ascending slot order and the exact resulting bitmap.

Charge actual copied references, visits, bitmap/rank operations, pending reads,
list insertion/deletion shifts, allocations and final tuple reference copies.
Read the immutable base child at most once per changed slot. No mutation of base,
early publication, threshold change, cap change or new backend. The existing
new-branch construction may remain unchanged. Keep failed preparation atomic;
a failing staged freeze cannot alter a retained snapshot or lower retry work.

## B: choose the late splice, retaining all earlier setup

Use the point of self.values.update(entry_values or {}) at15333. Keep all earlier
initialization and evaluation exactly in place. Inspect the actual prepared
mapping there; no early-constructor restructure or all-input emptiness inference
is needed. Eligibility is an exact empty prepared dict, exact ExecutionState entry,
and inactive subsequent lexical local/nonlocal/global name-producing loops.

Actual intervening accesses:
-15334-15351: local loop contains setdefault, assignment and possible evaluation.
-15352-15380: nonlocal loop contains entry reads, builtin markers and assignments.
-15382-15392: global loop contains membership and fallback assignment.
-15395-15398: final _ExecutionState call reads values, budget, parent and local names,
  and evaluates bool(self.helper_registry). No other self.values access intervenes.

Require the three binding sets to be exact empty frozensets, rather than assuming
arbitrary iterable emptiness prevents callbacks. Existing exact dict/_ReviewRegistry
uses plain dict truthiness at the final enabled argument; exclude arbitrary custom
registry Mapping/subclasses from this fastpath to avoid a reentrant mutation of
borrowed entry before the final fork. Leave generic/custom entry Mapping and
ExecutionState subclasses on the exact old update expression.

Preserve entry_values-or-empty semantics. Within the eligible exact-type branch,
evaluate entry truthiness once. Borrow only its nonempty case; if false, perform
the original empty-dict update and final detached construction. Do not evaluate a
custom Mapping's truthiness twice or silently make falsey input into borrowed
history. Charge new guard operations and all actual existing forks.

Borrowing means assigning self.values=entry_values only for the zero-write window
above. Do not update the borrowed wrapper. The final constructor still allocates
a fresh ExecutionState, forks authority/bindings, and takes its existing exact-
parent/no-locals name fork at14957-14959. Parent mode, Entry proof/pending flags,
order and snapshots are inherited by that existing mechanism. Do not infer a new
normalization certificate or skip a transfer owed to a changed name.

The preceding ordinary name-building loops only install entries; a nonempty result
falls back, regardless of why it was produced. Earlier effects, registry and
exception setup are not skipped. If implementation inspection finds any extra
intervening name mutation/callback or raw prepared-dict escape, tighten the guard
or stop; do not generalize borrowing to that path.

## C: deferred; no implementation in v28

Potential shared-root fastpath only after the original state snapshots have been
taken and original authority/binding joins retained. Require exact compatible
inputs, all-disabled mode, same budget/meter, immutable root identity, and
pending_count==size (including the empty case). Roots are compared after sealing;
equal73 cardinalities are not evidence of shared roots or utility.

Retain all-parent legacy union-order recipe, invalidate the reordered items cache,
and preserve every pending flag/debt and ownership boundary. No disabled no_work.
The observed counters did not record root identity: useful hits remain unproven.

Different roots keep the old path. A wider context-local disabled-transfer proof
must be explicitly reconciled with the current every-transfer contract before
any source change; no silent callback-law exception or mode exemption. There is
no such authorization in this clarification.

## Fixed verification order and stop boundary

After separate source GO, author only retained v28 A+B with exact v26 delta,
binding-aware primitive comparison and protected AST/source checks. Root inspects
before dispatch. Existing actual design53 is the first integrated check: its RED
already exists. Then existing primitive order/collision/retention/failure-atomicity
oracles verify changed freeze mechanics. Do not expand the test population or
substitute primitive success for analyzer fitness.

Keep all five caps, old source cases and exact expected refusals. No W/main edits,
semantic merge, additional probe or automatic continuation is authorized here.
Stop on failed ownership/order/debt proof or newly uncharged work.

