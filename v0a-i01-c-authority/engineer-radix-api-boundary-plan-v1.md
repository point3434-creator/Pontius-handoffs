# Isolated radix name-store API and production boundary plan v1

Proposal only. No prototype, payload, W mutation or production port is authorized.
Proposed source, after frozen schedules and coordinator review:
T/engineer-name-radix-prototype-v1.py. Production comparison remains retained
v22 SHA61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3.
The two-case diagnosis8ac28ed870ecd2fcf5c516aa034357f7d634b14181501960fc6bc44f76b384b6
motivates this experiment; neither it nor a pure-store pass proves corpus fit.

## API: preserve old behavior, add one explicit bulk factory

Preserve Meter(limit/used/counts/charge), BudgetExceeded, Entry(value,no_work),
MISSING, NameVersion.empty/get/set/delete/fork/keys/ordered_items/len,
NameCursor(version)/get/set/delete/snapshot/fork/keys/ordered_items/len, and
join(meter, immutable_versions, pure_merge). Meter remains0..262144.
Cross-meter joins remain errors. Existing input order, value identity, raw-write
proof invalidation and pure/idempotent callback law remain unchanged.
No arbitrary cursor input is silently snapshotted by join.

Add only NameVersion.from_unique_entries(meter, entries) -> NameVersion.
entries is an ordered iterable consumed once, containing two-element tuples
(name, Entry). Entry must be exact Entry and no_work an exact bool. Name keeps
the existing ordinary-string equality/hash-law contract. Bad shape/type raises
TypeError; duplicate names raise ValueError after one explicitly charged
membership attempt in the name-only order staging dict. There is no per-entry
radix absence lookup or repeated immutable set. Preserve supplied Entry/value
identities; do not normalize, transfer, merge, or invoke a callback.

The factory returns a fresh detached history root and exact input key order.
All work is staged until successful return; it mutates no source or live owner.
Input iteration is not transactional. Fault/retry comparisons use a fresh
iteration of the same immutable sequence, not a half-consumed generator.
The production adapter guarantees source enumeration/callback effects finish
before this factory and does not offer external iterators its owned buffers.

## One indexed representation

Replace data layers only; retain Version/Cursor, name-only history and order.
Immutable leaf: read-only dictionary name -> Entry plus effective pending-name
tuple. Immutable branch: bitmap, packed immutable child tuple, pending count.
Empty root is None. Branch positions consume successive four-bit groups of
hash(name), normalized to sys.hash_info.width; iteration order never comes
from this index. Leaves split above16 entries, a fixed structural choice for
this experiment, not a refusal threshold or tuning knob.
Split recursively by further hash groups. At hash-width exhaustion, retain an
ordinary collision dictionary. Colliding keys remain distinct by normal
dictionary equality; all actual bucket visits/copies are charged. A collision
bucket may be large and exhaust the existing budget, never a new storage cap.
Do not compress away one-child levels unless their consumed hash bits remain
explicit; the initial implementation can simply retain those levels.

A cursor owns its current private delta, key-order recipe and items cache.
It shares only the immutable base root/version. A raw overwrite replaces Entry
even for identical value identity; a delete is private until publication.
No mutable dictionary/list backing a published branch or leaf remains exposed.
No global cache, weak-owner heuristic, refcount ownership inference or
authority-store ancestry optimization is introduced.

## Staged publication and lifetime

1. snapshot/fork prepares a plan without changing the cursor, old roots, history
   or order memos. Capture changed names and preserve their current order.
2. Apply only private changes to a transient radix editor over the old root.
   The editor owns its temporary paths/leaves. Untouched immutable siblings
   are shared; a touched leaf is copied once per publication before editing.
   Branch edits keep only owned changed-child slots until finalization, avoiding
   a full mutable child-array copy followed by another immutable array copy.
3. Finalize touched paths bottom-up into immutable nodes. Charge each old-child
   read, dirty-slot lookup, copied reference, leaf entry visit/write, allocation,
   pending traversal and returned wrapper. Any split routes every actual entry
   and charges those hash/route operations. No repeated whole-root resealing.
4. Prepare a new Version, names-only history, fresh empty private delta, and
   fork cursor when requested. Charge all remaining return/publication work.
5. Only after every charge succeeds, replace the owner's base/tail together.
   Discarded plans leave no shared mutation and no cheaper subsequent retry.

Private never-published overwrites release replaced values as before.
After publication, the current radix root contains only effective entries;
obsolete values survive only through real old snapshots or other live owners.
History links contain names/tokens only, never previous versions, roots,
Entries or values. Order recipes/memos contain names only. Temporary editor
references are scoped to the operation and cannot escape through a cache.

Each leaf's pending tuple contains exactly its current no_work=False keys.
Branch pending counts allow skipping an all-certified subtree; every visited
node/count is charged. Pending enumeration does not rediscover hidden stale
layers. New raw writes remain pending; no disabled-mode certification occurs.
Join captures all immutable inputs before callbacks, uses unchanged history
candidate rules plus effective pending keys, and returns the same exposed
mapping/proof result. Storage traversal order is not callback order authority.

keys/ordered_items keep the existing staged exact legacy-order realization.
Reads include private changes but do not force publication. Item tuples and
genuine read-only dict_keys snapshot views remain stable; production live
Mapping views stay adapter-owned. Failure publishes no order/item memo.
The bulk factory creates a known name-only order memo directly; it does not
construct N insert recipes or cache Entry/value objects in an order table.

## Production bulk adapter, separately reviewed after prototype

Preserve existing exact-parent sharing, raw projection, semantic setter,
copy/adoption/update and view boundaries; replace only their underlying index.
Preserve all authority stores, _transfer_authority, _write_cells, caps and
class/helper/exception/recursive semantics. No singleton-wrapper move.

At the full _merge_states fallback: capture sources as already required, form
the literal legacy set union, then visit names in its exact iteration order.
Perform each original _merge_flow_values, full transfer and name validation,
construct its Entry and perform every existing strong/weak cell write in the
same cross-name order. Collect unique final entries privately. Build the index
and known order once, then install the result cursor. The delayed projected
map installation is allowed only where the complete seam inventory proves
transfer/cell logic cannot read the partially built name map. Preserve that
proof; do not generalize it to update or generic __setitem__.
Storage charge timing changes with actual construction, but no partial failed
result is returned or extra semantic rollback guarantee is claimed.

Constructors may use the same bulk boundary only after preserving local-name
capture/allocation order, inherited exact Entry versus semantic transfer, name
validation, and cell effects. Plain mappings remain plain until their existing
conversion boundary. Disabled/full/overlapping/missing-cell fallbacks keep their
full semantic path; the bulk factory neither changes mode nor certifies entries.
Nonempty overlays and arbitrary live updates retain sequential behavior.
No new _ExecutionState source edits before independent port review.

## Oracle boundary and stop rules

The old storage-oracle-v2's34 runs use only preserved public APIs and can run
unchanged. The old cursor-oracle-v1's28 runs use the same APIs, but retention
case at lines368–380 explicitly demands compaction_entry_visits>0. This radix
store performs no full compaction; running that unchanged runner must retain
its UnmetStructuralPrecondition and stop, not fabricate charges or claim62/62.
All original files/results remain frozen. Coordinator has asked the independent
oracle author for a neutral successor preserving actual overwrite, retained
snapshot positive ownership, release-after-owner-drop, and failure invariants.
Report separately unchanged old results and successor results; do not call the
changed oracle byte-identical. Every original semantic obligation survives.

Use the reviewed snapshot/custody procedure: fresh r010 D-local snapshot,
explicit retained prototype/oracle/case overlays and hashes, actual3.11.15
before3.14.6, seeds0/1/17, serial root-owned dispatch, current watchdog and
preimport identity. No hidden probe-time source mutation or production import.
New growth/collision/bulk/retention/atomicity cases freeze before source begins.
Report every construction, private edit, publication, terminal/historical read
and retry unit; no runtime-ratio or cap-fit claim from abstract copy counts.

Stop before implementation if API/case contracts conflict; stop after one
prototype if preserving order/proof/lifetime or exact failure retry needs
broader interpreter changes. No collision exclusion, threshold sweep, cap
change, discounting real copies, or silent oracle weakening is permitted.
