# Owned name-cursor prototype: bounded disposition and API

Coordinator, 2026-08-31. This authorizes one isolated T-only engineering
prototype, not a production port, cold review, acceptance run or source commit.
W remains rejected v20 e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
No authority store, production test expectation, generated file or cap changes.

Basis: engineer-storage-fitness-successor-v1.md SHA256
1307b0c2b10ab8fce5de974b26fdce5721969e599f6f121bf9b4ffe36747decb,
the construction inventory c5c949cca879d900dcffde0b1518aa9f2ac75f4f94346ec2da7eda43c377b6ba,
and the retained v20 diagnosis/public24 assessment. The universal AVL adapter
failed existing supported workloads. A mode exemption would not establish
whole-pipeline fitness; a bulk AVL builder leaves tree/read overhead; a fixed
partitioned map carries directory and collision-bucket copying. We select an
owned cursor over immutable dictionary snapshots as one coherent alternative.
Eight sealed layers plus at most one private tail is the representation bound,
not a new admission cap. Frequent publication may still defeat this design.

The original immutable storage API and its clarification remain in force:
engineer-storage-api-v1.md and engineer-storage-api-clarification-v1.md.
Preserve Meter's 0..262144 limit and spent/throwing charge semantics, immutable
Entry(value, no_work), MISSING, ordinary string equality/ordering, all
NameVersion operations, exact legacy multistate union order and pure callback
law. Do not restrict strings to exact str or redefine callback expectations.
Inter-name callback invocation order is not a primitive guarantee; input tuple
order and final exposed order are exact. Cross-meter joins remain refused.

Additional primitive API:

- NameCursor(version) creates an independent cursor over that NameVersion,
  using its meter. It does not transfer or normalize values.
- cursor.get(name, default=None) and len(cursor) inspect its current contents.
- cursor.set(name, value, *, no_work=False) and cursor.delete(name) mutate only
  that cursor and return None. Missing delete raises KeyError. Raw/default
  installation clears certification even for the identical value. Overwrites
  preserve key position; delete/reinsert appends.
- cursor.snapshot() returns an immutable NameVersion for the current contents.
  Later writes through this or any other cursor cannot alter it.
- cursor.fork() returns an independent NameCursor with identical current
  contents. It may publish shared immutable storage but must preserve both
  logical cursors and every previously returned snapshot.
- cursor.keys() and version.keys() return a genuine read-only dict_keys view
  in exact current order, backed by a dictionary that is never later mutated.
  This is a snapshot view, not a live view into a mutable cursor.
- cursor.ordered_items() has the existing immutable tuple/pair and value
  identity contract. It includes unpublished writes; it need not publish them.

No cursor update/adopt/clear API is needed in this prototype. Production
adoption remains a separately reviewed adapter operation. A later production
clear can install a fresh cursor over an empty, detached lineage; merely
emptying a tail while retaining unchanged ancestry would be incorrect.

Ownership and history requirements:

- Private delta dictionaries belong to one cursor. Publication relinquishes
  every mutable alias before a sealed layer becomes observable. Subsequent
  writes use a new private delta; snapshots expose no mutable backing aliases.
- Changed-name history is separate from data snapshots. It contains tokens
  and changed names, not prior full maps, cursors, Entries or values. Retained
  snapshots legitimately own their data, including overwritten entries in
  uncompacted layers. Do not promise immediate reclamation of those values.
- Deletes retain tombstones until all shadowed older layers are incorporated
  by complete compaction. Pending metadata must resolve the newest effective
  entry; raw same-object writes cannot borrow old certification.
- Order metadata depends on membership/order; item/value caches depend on
  current projected contents as well. Value-only writes may reuse exact key
  order, but may not expose stale item values. Certificate changes still
  affect pending/merge behavior even when item values are identical.
- Capture all source versions before join callbacks. No mutable cursor is
  accepted as an implicit NameVersion join input. Production transfer/cell
  purity proofs do not authorize arbitrary callback effects.

Operation-level failure contract:

snapshot(), fork(), keys() and ordered_items() stage publication, compaction,
history and memo changes until the whole requested operation succeeds.
A later charge failure in the same operation must not leave an earlier
successful seal/compaction/cache visible and cheaper to retry. A failed read
must not publish the cursor merely as a side effect. Immutable snapshot reads
retain the same failure rule as the original API.

After a supported injected failure, restoring the permitted meter limit and
retrying the SAME cursor/version must have the same retry units and category
deltas as a pristine identical operation, with the same subsequent fork/write/
read behavior. Spent work is never refunded. This does not add a general
rollback guarantee for semantic production writes or arbitrary callbacks.

Meter every actual dictionary attempt/entry visit/write/delete, allocation,
copied reference, layer/history/pending traversal, order realization and
returned-copy work. Publish/compact once per actual need; do not charge an
amortized discount. Preserve completed immutable key memos where valid and
avoid building an AVL index or a second complete name-value index just to
expose already ordered entries. Original authority consume/caps remain fixed
when a port is eventually proposed; prototype bookkeeping is not that port.

Measurement must retain publication frequency and tail-entry work, attempted
layers, compaction visits/copies, history/pending work, constructor versus
fork/join cost, terminal order realization and repeated reads. Existing
frequent-fork and dense-construction patterns must both be represented;
5415 production copies in public24 preclude assuming long private edit runs.
No runtime or physical-work ratio may be inferred from budget units alone.

Verification scope:

1. Keep all 20 compatibility and eight scaling cases from storage-oracle-v2
   byte-identical. The implementation author does not edit expected results.
2. The independent test author defines at most 16 additional cursor schedules
   before implementation is opened: retained snapshot/fork mutation, dense
   versus frequently published writes, tombstones across compaction,
   delete/reinsert, pending overwrite, exact ordered views and operation-level
   failure/retry. A retention sentinel must distinguish history-only retention
   from data still owned by an intentionally retained snapshot/layer.
3. Root reviews exact prototype, oracle and isolated control bytes before
   execution. Use actual 3.11.15 first, then 3.14.6, serially, fresh D-local
   snapshots and hash seeds 0/1/17. Retain every failure; stop on a mechanism
   failure before expanding runs. No automatic payload dispatch by authors.
4. Inspect whole storage-operation costs, including terminal/historical reads.
   This finite prototype cannot establish production fit. A separate bounded
   port requires the unchanged design53, authority matrix and public24 plus
   ordinary generation and downstream gates. No v21 production edit is
   authorized here.

Work allocation: authority_cost_audit authors the isolated prototype only;
r010_cold_a owns independent cases/oracle only; mapping_compatibility reviews
integration assumptions without editing source. Root owns dispatch and W.
These engineering participants remain ineligible as future cold reviewers.
