# v18 prerepair: eliminate redundant state-copy work

Date: 2026-08-31. Scoped engineering disposition before source modification, not
a cold review, release or acceptance claim. Exact v17 predecessor generator:
99cf67ff483244f1540f8d4959f1a84ba010a651de7ec51c228e207636815f84.
The separate C authority transfer replacement remains the only implementation scope.

Measured RED: tests-checks/red-budget-gen04-v4-311-receipt.json,
SHA-256 4b753726b3165bc5bf7b33df081329530f71a75c0f711a758ac253990b79e300.
The unchanged262144 budget fails at262145 in the review of
FreshActionWidthTransferStructureTests.test_complete_finite_inventories_have_no_
transfer_counterpart, tests/test_fresh_action_width_transfer_structures.py386,
while reaching _historical_inventory_sha256. The trace counts87844 ordinary map
lookups (62441 membership calls),58803 transfer units (54890 from state assignment),
21003 map-item units and12327 observation-constructor units. At least12045 of the
last category constructs empty maps discarded by an enabled state fork. The
observation compaction category is now248 units, not the dominant failure.
The third-level source of the54890 assignment transfers is not measured; do not
claim they all originate in the constructor or that this edit proves corpus GREEN.

Adopt only these four representation-preserving changes:

1. _AuthorityState.fork allocates a state wrapper directly, then forks the actual
   enabled tables. It no longer initializes empty tables only to discard them.
   Disabled forks still get fresh empty maps, preserving the previous policy even
   if a disabled source acquired scratch results. Charge the new wrapper and all
   explicitly allocated disabled empty maps; each actual map fork charges itself.
2. _merge_states skips the binding-table union only when both tables have the exact
   same backing dictionary. Contents and tuple values are then identical; no union
   work is performed. Divergent tables keep their old complete metered union, and
   projected names still use the existing setter/strong-or-weak cell write path.
3. __setitem__ and __delitem__ fetch the immutable binding tuple once with an empty
   default, instead of a membership lookup followed by indexing. Every cell write,
   alternative-cell merge, deletion value and transfer remains unchanged.
4. The constructor extends its existing exact-parent copy path to uncaptured names:
   the parent must be an _ExecutionState, the value must be the identical object
   currently under that name in the parent, and the name must not be a fresh local.
   The child has already forked that same parent's object/cell/binding tables. A
   constructor copy charges one unit per actual copied name. Changed or external
   values and every fresh local still use the complete transfer/refusal path.

Constructor safety audit: public flow values are immutable and ordinary state
assignment registers their authority. An exact-parent copy keeps the same records,
cell identities, aliases, dormant obligations and unknown/unbound status; it grants
no new proof. All explicit dict.__setitem__ sites were examined. Parameter injection
at v17:18393 belongs to the callee's local_names and therefore cannot use this fast
path. Captured-cell hydration14439 and post-helper projection18457 already have
bindings and used the predecessor fast path. Historical review-entry filtering
24761/25268 carries its exact parent store. Store joins retain inherited records;
there is no general record deletion. New local activation IDs are still allocated.
No guarantee is added for manually corrupted internal state; external values still
enter through transfer, including missing-reference obligations.

Boundaries unchanged: no projection-only merge, lazy cell allocation, generic
setter transfer skip, static-name cache, observation pruning or unrelated microfix.
The v17 observed map, evaluation-depth lifetime and all five analysis caps remain
byte-identical. No source/test/generated/baseline/controller files outside the
owned generator change. This edit is five existing method bodies, not new semantics.

Falsifiers: an inherited alias loses its cell relationship; a fresh parameter
updates a caller cell; unknown or missing external authority becomes proved; a
fork mutates its source snapshot; divergent binding alternatives disappear; or
strong/weak writes differ. Root will verify ordinary isolated generation first,
then the required focused public checks on actual3.11.15 before3.14.6. This engineer
runs no payloads. Fresh corpus/census, reviews and broad acceptance remain pending.
