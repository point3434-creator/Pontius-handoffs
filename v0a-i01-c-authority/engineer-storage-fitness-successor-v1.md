# v20 storage fitness and coherent successor design v1

Status: read-only diagnosis and proposed replacement design. No production edit or further payload run is authorized by this note. The coordinator has rejected a disabled-only patch and holds v20.

## Bound evidence and verdict

- Exact v20 source: e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
- Floor chain32 receipt: engineer-checks/chain32-v20-diagnosis01-311-receipt.json, SHA256 03c82035d15ed8218e8a0ac9907eb189738402215e4bd4e93a72de6d81c14a47.
- Its raw log SHA256: f4f2a44d96667f8d2b13ccf4de816b1f18541e737381d010763c33762d5d876a. Expected diagnostic exit 2; original work counter 262144 + 1 = 262145.
- Floor public24 receipt: tests-checks/red-name-environment-v20-01-311-receipt.json, SHA256 073271c7de10694fa72d938c9babee4a21dacaa764eacac9241f623d8f80e2b1. Log SHA256 43d76a321846089bfc6b8ff5cb9b7f4ad97c2c9f019470287cab27ed1c882a81.
- Independent construction/mode inventory: engineer-storage-construction-inventory-v1.md, SHA256 c5c949cca879d900dcffde0b1518aa9f2ac75f4f94346ec2da7eda43c377b6ba.

**Verdict: the universal AVL backend is unsuitable for the measured pipeline under the unchanged work cap.** Sparse joins now avoid unchanged ambient transfers, but the chosen storage performs too much construction, lookup and ordered-read work. Preserve that semantic improvement and its proofs; replace the backend as one coherent change rather than adding another path-specific optimization.

## What chain32 actually measured

Failing original budget epoch 6 reconciles exactly:

| Exclusive phase | Units |
|---|---:|
| Join | 160983 |
| Ordered access | 60301 |
| Lookup | 27392 |
| Constructor | 4993 |
| Fork | 3264 |
| Assignment/overlay | 3705 |
| Other | 1507 |
| Total | 262145 |

NameMeter accounts for 250815 units (95.7%). These are actual calls to unchanged original consume, not an extrapolated cost model. The phase classifier gives ordered adapters their own bucket even when invoked inside a join; receipt caller/parent/third origins preserve that distinction.

The failing stack is _unittest_receiver_attributes (26711–26737), entered from unittest preflight. Its resolver omits helper_registry (26722), whose default becomes empty at 14791. Construction at 14967 therefore selects disabled authority. This is independently visible in all 1154 certificate checks: certificate_enabled_check occurs, but no identity/reference/provenance check does. _transfer_authority returns immediately at 14043; merge compatibility is false at 21842. There are no _join_name_versions accounting kinds in this budget.

All 31 multistate merges are merged_raises calls at 22115. They use the full fallback at 21876–21888: 62 key views visit 2170 input names, the union loops install 1085 names, and persistent setters allocate 6882 AVL nodes plus 1116 versions (1085 setters and 31 clears). This is repeated full reconstruction using a structure intended to share mostly unchanged environments. The 60301 ordering units include tree traversal, temporary name indexes, pair creation and adapter key dictionaries. The final refusal during _flow_aliases/_snapshot_call ordered access is the endpoint, not the root cause.

## Why disabled dicts alone are insufficient

Public24 passes all 24 semantic cases / 58 projections. A's independent attribution finds 5415 forks sharing names, and 115 enabled common-base joins performing 205 nonambient and zero ambient normalizations. The intended sparse-join mechanism works.

Nevertheless, original charged units total 1357663 versus v19's 168331. NameMeter contributes 1132376 (83.4%). Recorded phases include disabled legacy fallback 421629, construction 224800 and ordered access 195773. Removing the entire measured disabled phase arithmetically still leaves 936034 units; that subtraction is neither a repaired-run prediction nor an enabled-only budget total. Constructor/ordered/other phases mix modes.

The 8.065x ratio is budget consumption, **not** a runtime or physical-work ratio. V19's dict.__init__ copy at 14178 had no direct name-copy consume charge, whereas v20 charges actual new tree nodes, fields and traversals. A successor must charge its own dictionary operations, copies and visits honestly; reproducing v19's omitted charges is not an acceptable repair.

## Selected successor: owned cursor and immutable snapshots

Keep the externally observable immutable NameVersion API, four-fact no-work certificate, changed-name ancestry, exact legacy mapping order, and unchanged semantic transfer/cell-write boundaries. Replace only the name-store backing and production mutation interface. All authority object/cell/result/observation stores and all five caps remain unchanged.

Use these concrete roles:
1. An immutable NameVersion snapshot holds sealed dictionary layers, a lightweight history token, exact order recipe/memo, pending metadata and its meter.
2. A branch-owned NameCursor holds one snapshot plus an exclusively owned mutable delta dictionary, pending-name metadata and local order/change events. Only its owning ExecutionState mutates it.
3. Snapshot publication seals the current delta and creates immutable metadata. Subsequent writes receive a new private delta. Fork/adoption creates another cursor over the sealed snapshot; neither branch can mutate a published layer.
4. Keep immutable NameVersion.set/delete/fork/join as the reference API, implemented by a temporary cursor and publication. Old versions stay readable exactly as before. Production uses the explicit cursor to avoid publishing every private assignment or intermediate constructor entry.

Seal through an auditable ownership boundary: published dictionaries expose no mutable alias; a frozen/proxy layer wrapper is suitable if its allocation/reference cost is counted. A history token contains only parent tokens and changed names, not old full name maps. Retained snapshots own their data; ancestry alone must not keep every discarded intermediate environment alive. This separation preserves common-base discovery without weakening historical snapshots.

A suggested internal depth is eight sealed layers, including the base, plus at most one private mutable tail. This is a representation choice, not a refusal, admission limit or raised analysis budget. Snapshot lookup attempts at most eight dictionaries; cursor lookup at most nine. A same-key update overwrites only the private delta entry. Deletion records a tombstone; deleting/reinserting a key has separate ordered events.

When publishing would exceed the depth, compact all layers into a fresh flat base, oldest to newest. Charge every layer visit, physical entry visit, lookup/write/delete, copied reference and metadata allocation. Remove a tombstone only after the complete older chain it shadows has been incorporated. Previous snapshots keep their original layers. No authority value/reference is discarded from a retained snapshot, and no live authority store is pruned. Compaction work can exhaust the ordinary cap; there are no amortized discounts or refunds.

## Proof and pending tracking

Every normal semantic write still calls full _transfer_authority and then _write_cells in the existing sequence. Only its resulting entry can earn no_work after the existing four facts. Raw projections remain pending. Cursor storage does not infer normalization from equal-looking values or a shared name.

Each sealed layer records the names of its pending entries; the private tail maintains its own pending subset. Pending discovery visits those metadata entries, deduplicates by name and checks the newest effective entry, so an older pending value replaced or deleted is handled correctly. It may cost proportional to physical pending metadata across layers. Compaction rebuilds that metadata from effective entries, charging the complete traversal. No scan of all certified ambient entries is needed merely to discover pending values.

Changed-name history and pending metadata serve different purposes: every changed/deleted name participates in common-base join discovery, and every currently pending entry is normalized even if unchanged. Bound-cell writes survive independently of the name certificate.

## Exact ordered mapping and reads

Keep the actual legacy empty/singleton/multistate order rule, including literal built-in set union over ordered dict-key views. Source order, first-matching aliases and delete/reinsert position are not incidental.

Cache a completed ordered-key dictionary/memo whose backing is never mutated after publication. Its dict_keys view supplies the exact legacy union input type/order. Cursor edits invalidate only that cursor's memo. Unchanged immutable order can be shared across value-only changes, while item/value memo validity also depends on the name-value snapshot.

Ordered items follow the exact key sequence and look each key up in the bounded layers; they do not walk an AVL tree or construct a second whole-tree name index. Charge every attempted layer, key visit, pair/reference copy and returned tuple/view allocation. Repeated reads still pay their actual returned-copy costs. An unchanged immutable dict_keys view need not be rebuilt just because the caller requests keys again.

Order realization, compaction and publication must stage their caches/metadata until all required charges and construction succeed. A failed ordered read publishes no partial memo; retrying the same immutable snapshot must match pristine retry accounting. A returned view/snapshot may never observe later cursor mutation. Do not introduce a general rollback promise for semantic writes beyond the existing fail-closed analysis contract.

## Integration boundaries and fallback semantics

The mapping inventory covers six direct constructors plus copy, all 72 _fork_values uses and 14 state-capable updates. Production cursor integration belongs at _ExecutionState's constructor/copy/read/write/project/pop/clear/update methods and _merge_states; existing callers remain through that adapter.

Construction can use one private builder while preserving every required transfer and cell-write sequence. _transfer_authority reads authority, not partially installed names. Exact parent inheritance and raw projection remain distinct. Generic resolver construction has aliases/locals/order overlays and cannot simply inherit the parent map.

Authority mode comes from the actual adopted authority state: parent construction can override the enabled argument; update can adopt another mode; plain Mapping conversion still performs owed enabled transfers. Preserve authority-only adoption at 19020/23596 and ensure meter/snapshot ownership cannot drift. BoolOp/IfExp pre-entry plain dictionaries must not acquire execution stores incidentally.

Enabled compatible joins seal their inputs, discover changed/pending names and build one result delta. Every full transfer and required cell write remains. Overlapping or missing cells, disabled inputs, plain mappings and incompatible contexts retain the full legacy union/merge/transfer/cell-write sequence. A private builder can collect final names during this sequence and publish once, because the relevant merge/transfer/cell helpers do not read partially installed names. No projection-only substitute or broadened sparse fast path is needed.

Empty-destination adoption may share a sealed snapshot. Nonempty overlay retains destination positions and destination-only names; raw incoming entries stay pending. Cross-meter adoption must rebuild under the adopted meter, without importing foreign history or performing an extra semantic transfer.

## Actual costs and limits

Private writes are expected constant dictionary work plus bounded-layer presence checks/order metadata; dense construction is linear entry work until publication. Fork costs include sealing whatever private entries actually exist, copied layer/history references and wrapper allocation. A fork with no private change is fixed wrapper/reference work.

This is not a promise of giant savings. Public24 already has 5415 state copies; the interpreter may publish after nearly every assignment. In that workload tails can be tiny, layers fill quickly, and full compaction may recur frequently. Layer depth bounds lookup attempts, not total compaction work or retained-snapshot memory. Hash-table operations have their usual collision behavior; meter units describe semantic operations/visits, not CPython opcodes.

The replacement probe must record publication frequency and tail sizes, attempted-layer distributions, all compaction entry visits/copies, pending/history work, constructor/fallback work, first ordered realization and repeated reads separately. No terminal cost may be hidden by ending before realization.

## Rejected shortcuts and bounded falsifiers

- Disabled-only dict exemption closes the observed mode mismatch but leaves most aggregate costs unexplained; do not ship it as the structural solution.
- Bulk AVL construction can preserve exact fallback sequencing, but retains tree lookup/ordered traversal costs. Building a balanced lexical index from arbitrary legacy set order also needs sorting or a separately metered sorted traversal; it is not automatically linear.
- A layered dictionary substituted into immutable-per-set history without a production cursor still publishes each assignment and repeatedly compacts dense builds. Mutable layers shared with retained versions are unsound.
- Fixed partitioned dictionaries retain directory/bucket copies per publication and potentially large colliding buckets. They are another candidate requiring evidence, not a presumed cheaper implementation.

Before production integration, extend the independent storage oracle to cursors: retained forks after every write, many writes before one publication, delete/reinsert, overwritten pending entries, all-layer tombstones, meter/context adoption, exact union order for hash seeds 0/1/17, and failed realization/compaction followed by retry where supported. Compare immutable reference API and cursor outputs against the same built-in-dict oracle.

Then use the existing finite public24 pipeline to measure complete constructor/fallback/enabled-join/ordered costs; reuse the exact chain32 and deep-helper contracts on both interpreter slots. All current semantic/certificate/cell invariants and refusal contracts must hold with unchanged caps. If frequent publication/compaction or ordered consumers still exhaust a previously valid budget, stop and reject the successor's fitness before another production tweak. Ordinary corpus generation remains a separate necessary acceptance check, never implied by these finite cases.
