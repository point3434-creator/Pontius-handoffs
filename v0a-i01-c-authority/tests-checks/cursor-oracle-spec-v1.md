# Independent owned-cursor extension: frozen specification v1

Engineering test specification only. No prototype implementation has been read,
authored by this reviewer, imported or executed. No production behavior, source,
test expectation, admission rule or cap is changed by this pack. The coordinator
must review the executable oracle/control before dispatch. Existing storage
oracle v2 and its 28-case pack remain separate and byte-identical.

Scope authority: coordinator-name-cursor-prototype-disposition-v1.md SHA256
973191b8b26c71132185d42203a720bdc5b28d4fd23fc1bc4b9c9ec4da46a7b7.
Design challenged: engineer-storage-fitness-successor-v1.md SHA256
1307b0c2b10ab8fce5de974b26fdce5721969e599f6f121bf9b4ffe36747decb.

## Qualified design finding

The successor is coherent as a bounded storage experiment if publication really
relinquishes every mutable alias and all four publication/read operations stage
their entire transaction. A successful internal seal followed by a failing pair,
view, fork or metadata allocation is not an atomic public operation. The exact
same object must be retryable at pristine cost, including every charged category;
eventual equal values alone cannot establish this. Spent charges remain spent.

A key memo may survive a value-only edit, but item values and effective pending
metadata cannot. A deleted key must shadow every older layer until complete
compaction. Changed-name ancestry must not retain maps/values merely to remember
names. A retained snapshot may legitimately retain overwritten values in its data
layers; the reclamation assertions below deliberately distinguish those owners.

The original pure callback and no-work proof remain unchanged. All changed or
currently pending names must be merged using input-state tuple order. Optional
callbacks for unchanged certified names are allowed. No inter-name callback order
is asserted. Exact final order comes from an independently evaluated builtin
set().union(*(reference_dict.keys() for reference_dict in inputs)) in each child.
No values are transferred or normalized by a cursor constructor.

## Finite extension and counts

The separate JSON casepack contains 16 schedules. Twelve run once. Four operation
atomicity schedules each run a pristine baseline and three fresh replays (first,
middle, last injected failure), for 28 runs per child. With the old independent
28-case/34-run oracle, a complete child has 44 schedules and 62 runs. This is not a
new giant cross product. Six coordinated children would have 372 completed runs.

Each repeat in the case JSON expands its fixed count with i and next=i+1 string
substitutions; no data-dependent random scheduling. All keys are builtin str.
No collision-subclass coverage is claimed and the API is not narrowed to exact
str. Expected values use independently interned harmless token identities; no
production source fixture or owner body is executed.

1. cursor-empty-boundaries: empty keys/items, default identity, missing delete,
   empty publication/fork and an independent write.
2. cursor-dense-private-64: 64 private inserts, terminal and repeated reads,
   publication and later overwrite while retaining the old snapshot.
3. cursor-fork-per-write-64: same 64 inserts, publishing/forking after each write,
   retaining all earlier cursors; terminal/repeated and historical read costs.
4. cursor-retained-sibling-isolation: snapshot, two fork branches, overwrite,
   delete/reinsert and a cursor reconstructed from the old immutable snapshot.
5. cursor-view-and-value-memo: retained real dict_keys views and item tuples,
   value-only overwrite, then membership/order-changing delete/reinsert.
6. cursor-tombstones-through-publication: old pending victim deleted, 18 dirty
   publications, absent lookup after each, final reinsertion appended. Retained
   older snapshots still expose their own victim. This crosses the layer bound
   without inferring a precise implementation-specific compaction charge.
7. cursor-newest-effective-pending: older pending replacement/deletion, then a
   new raw replacement. Callback argument identity and required pending names
   come from the current builtin reference, never the historical layer.
8. cursor-raw-identical-clears-certificate: raw installation of the identical
   token, metadata-only difference, cursor fork and a later merge. These names
   must invoke the callback; optional already-certified callbacks remain allowed.
9. cursor-branch-and-unrelated-joins: sibling snapshots and unrelated roots,
   delete/reinsert edits between joins, exact terminal/repeated union order.
10. cursor-invalid-join-boundaries: existing join rejects a mutable cursor and
    cross-meter versions before invoking merge. Exception spelling is recorded,
    not prescribed. No BudgetExceeded is accepted as the intended rejection.
    Source states are audited afterward. No adopt/clear/update API is invented.
11. cursor-private-tail-retention: overwrite one never-published weak-reference
    sentinel with 12 new values in the same private tail. No reference model,
    saved returned tuple, snapshot or token registry owns the sentinel. After gc
    it must be gone. A separately retained current value remains readable.
12. cursor-history-retention-after-compaction: publish a weak-reference sentinel
    and retain that original snapshot as an explicit positive owner. Overwrite
    victim and perform 24 dirty publications while retaining only the latest
    working cursor plus the original snapshot. At this point the original must
    still return that exact object. Drop that one old snapshot and collect; the
    obsolete sentinel must be gone. The 24 publications exceed the selected
    eight-sealed-layer/full-compaction regime; this is not immediate reclamation
    of arbitrary values in still-owned uncompacted data. Accounting must disclose
    whether full compaction occurred. If it did not, report the unmet structural
    precondition rather than call ordinary data ownership a history leak.
13–16. cursor-atomic-snapshot/fork/keys/ordered-items: the exact operation named
    by the case, with one shared bounded preparation and three fault offsets.

## Atomic operation oracle

Build a cursor with alpha, beta, gamma, then seven dirty publications with
step-name additions. Retain the first immutable snapshot and first returned key
view/item tuple as old witnesses. Apply an unpublished overwrite of alpha, delete
beta and insertion tail. Only the target primitive call is included in pristine
calibration: capture meter.used and meter.counts immediately before and after it.
Len, content checks and subsequent reads are outside that transaction delta.

For each replay rebuild that preparation from scratch. Just before the target
operation, lower the writable meter limit to used_before plus 0, floor(C/2), or
C-1, where C is the pristine target cost. The identical target must throw
BudgetExceeded and spend a charge beyond the configured limit. Restore only the
permitted 262144 limit, without refunds/reset. Retry the SAME cursor. Its exact
used delta and per-category delta must equal pristine C and counts. This checks
all requested operation types, not only immutable ordered_items.

Validate the return against ordinary dict behavior (a snapshot/fork result is
read through its public API; keys must be genuine dict_keys; items must be a
tuple of pairs with value identity). Then run the same continuation for baseline
and replay: fork current cursor; parent inserts after-parent; child deletes and
reinserts alpha with after-child; publish both; read keys/items twice; re-read old
witnesses and the original operation result. Compare each continuation primitive
cost and observable output with pristine. Validation charges are labeled
separately. The failed attempt remains in total work but not in the equality of
pristine-versus-retry or continuation deltas. No general write rollback or
arbitrary-callback-effects contract is inferred.

The preparation aims at a dirty publication boundary, but does not assert
whether the particular target also compacted. Actual accounting must name that
work before a report claims compaction-failure coverage. Full compaction semantics
are independently exercised by the publication and retention schedules. Broader
fault-prefix expansion is not silently admitted.

## Measurement and limitations

Record each public operation, phase, charged units and category deltas, including
construction/private writes, publication/fork frequency, joins, lookup,
terminal/repeated keys/items, retained-state audits, failures and continuations.
Keep every Meter within its immutable maximum. Foreign-meter setup is a distinct
auxiliary meter, not an unrecorded increase to the main meter's cap.

Expose raw category totals so source review can map tail-entry, layer, compaction,
history, pending, allocation and returned-reference work. Public operation
counts alone cannot establish all physical internal visits; no uncharged
diagnostic counter will be presented as charged budget. No absolute cost ratio or
runtime/production-fitness pass threshold is invented. Cached immutable return
objects are allowed; no dummy returned copy or charge is required.

This finite pack checks storage semantics and the stated operation-failure
contract. It cannot prove production adoption/clear boundaries, live authority
cells, actual consumer safety, all hash collision patterns, concurrent mutation,
or universal memory reclamation. Those remain separately reviewed/integrated.
No prototype payload may run until root approves exact oracle/prototype/control.
