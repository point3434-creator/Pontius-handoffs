# Owned name-cursor production adapter proposal v1

Status: T-only proposal, not a source lease or implementation. No W edit, test change, generated-file change or payload execution is authorized here. The class-body semantic finding reproduced on v19 is a separate repair and remains unchanged by this proposal.

## Exact bases and proposed edit boundary

- Candidate target, only after a new coordinator lease: D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py.
- Mechanical predecessor: retained v20, SHA256 e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679. All line anchors below use this file.
- Semantic comparison: retained v19, SHA256 3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1. Do not restore its omitted name-copy accounting or retired sparse-cell planner.
- Storage source to port: engineer-name-cursor-prototype-v1.py, SHA256 67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a. Independent runs are coordinator-owned; no whole-pipeline fitness is inferred here.
- Complete construction/call inventory: engineer-storage-construction-inventory-v1.md, SHA256 c5c949cca879d900dcffde0b1518aa9f2ac75f4f94346ec2da7eda43c377b6ba. This covers six direct constructors, copy, 72 _fork_values uses, 14 state-capable updates and the additional pre-entry dict update.

Replace v20's AVL name-storage region with namespaced prototype primitives. Retain the existing _NameMeter adapter: charge delegates directly to unchanged _AnalysisBudget.consume. Do not port the prototype's separate Meter, BudgetExceeded or MAXIMUM_WORK into production. MappingProxyType is already imported.

Suggested symbols: _NameEntry, _NameHistory, _NameLayer, _NameOrder, _NameVersion, _NameCursor, _NamePublication, _NAME_MISSING, _NAME_DELETED and _MAXIMUM_NAME_SEALED_LAYERS=8; private functions use _name_ prefixes. The eight-layer setting remains a compaction threshold, never an admission gate.

The production _ExecutionState._names field becomes an exclusively owned _NameCursor. No two live wrappers may share that mutable cursor. They may share immutable versions/layers/order memos. The cursor's meter must be identical to the lineage's existing name meter, and that meter's budget must match the adopted authority budget.

## Adapter operations

| Boundary | Planned implementation and invariant |
|---|---|
| Constructor 14564 | Establish/fork authority and bindings exactly as before; select the existing parent name meter or one new _NameMeter. Allocate enabled local cells first, in existing local_names order. Then build names privately in values.items() order, preserving the inherited-entry versus semantic-write distinction. |
| Exact parent inheritance | If parent is an ExecutionState, name is not a fresh local, and parent._names._entry(name).value is the same input object, install that exact Entry via cursor._replace_entry. Preserve proof OR pending debt; no extra transfer or cell write. All other entries use the ordinary semantic setter. |
| __getitem__/contains/get/len 14586 | Use cursor entry/get/size access. Keep ordinary-string checking and missing behavior. Reads must not publish a cursor or compact its layers. |
| items/keys 14606 | Delegate to cursor.ordered_items()/keys(). These return immutable item tuples and genuine snapshot dict_keys views. Remove only the old AVL key-index/dict(items) reconstruction that is no longer performed. |
| values 14618 | Retain the existing ordered item traversal and actual new value-tuple/reference charges. No additional value cache is proposed. |
| Semantic setter 14665 | Keep full _transferred_name_entry(value), install the returned Entry through cursor._replace_entry, then perform all existing bound-cell writes. General setters never infer a skipped transfer from equal projection values. |
| Raw projection 14654 | cursor.set(name,value) with default no_work=False. Identical-object raw writes still clear certification. No transfer or cell write. |
| Raw pop 14658 | Read current Entry, cursor.delete only if present, return its value/default. No captured-cell delete. Preserve delete/reinsert order. |
| Semantic deletion 14681 | cursor.delete, then the original strong/weak bound-cell deletion sequence. pop/setdefault retain their existing semantic routes. |
| clear 14728 | Replace names with a fresh cursor over NameVersion.empty on the SAME meter. Detach ancestry. Do not merely empty a tail while preserving an unchanged history token; do not delete cells. |
| copy 14732 | Allocate/charge the wrapper; cursor.fork yields an independent cursor while sharing a sealed snapshot. Fork authority and bindings unchanged. No transfers, new lexical cells or cell writes. All 72 state _fork_values callers use this path. |
| Plain Mapping _fork_values 14974 | Keep the fresh constructor, resolver-selected mode and every existing transfer. No incidental adoption of stores or proof from a plain Mapping. |

_transferred_name_entry retains its exact four-fact rule and metering: actual enabled full transfer, returned object is input, no authority refs, helper_provenance is None. _transfer_authority and _write_cells AST bodies are protected. The cursor Entry installation must not allocate/certify another Entry after this helper has already done so.

## Constructor policy: private builds first, one narrow sharing seam

1. Generic resolver entry (14967) has a newly prepared plain dict: aliases, module entries, parent overlay, local/parameter/global adjustments. Use a fresh private cursor and the existing per-entry inheritance/transfer sequence. Do not wholesale share parent order or bypass local cell writes.
2. Plain-Mapping fork (14974) likewise uses a private build with all original transfers, including missing-store refusal for ref-bearing values.
3. Registered helper environment (18476) starts with NO caller names despite inheriting caller authority/bindings. Use an empty private cursor. Subsequent alias/seed/module assignments and filtered caller overlay remain semantic setters; sharing the caller projection would leak locals.
4. Empty merge (21831) creates fresh empty stores/names. Singleton merge retains _fork_values control flow.
5. Exact-parent/no-local entry (25388) is a justified sharing seam: when values IS the ExecutionState parent and the supplied local_names is empty, fork the parent's names directly while still forking authority/bindings. This skips only the already-proven inherited-entry copy loop. Do not infer this condition from equality, a prepared overlay, or an arbitrary iterable's contents. The empty-parent “or {}” case may retain the ordinary empty private build.
6. Filtered-parent local-helper entry (25895) initially keeps its existing ordered comprehension and generic private constructor. Retained entries inherit exact parent Entries; omitted names do not delete bindings/cells. No new filtered-map API or caller-specific root optimization is needed for the first port.

Private builds do not publish after every constructor entry. They retain every original transfer/cell-write in original order, but publish only when a later real fork/adoption/join requires a snapshot. No eager end-of-constructor seal is necessary. _transfer_authority and _write_cells do not inspect the partially constructed name map.

## Update and adoption

For update(supplied_state), capture an immutable supplied name snapshot BEFORE changing destination names or adopted stores. This includes supplied is self. Never read a live supplied cursor while mutating a potentially aliased destination. Charge the actual publication, captured references and any resulting compaction.

Adopt supplied authority and bindings as v20 does. If the destination is empty, create its independent cursor over the captured supplied snapshot; preserve all proof/debt. If nonempty on the same meter, retain the destination cursor/order/leftover names and raw-overlay supplied ordered items. Each incoming Entry is installed as pending, even for equal values. A value-only overwrite preserves destination key position.

For a different meter, read the previous destination through its own meter, create a detached empty cursor on the supplied meter, raw-rebuild previous ordered values, then raw-overlay captured supplied values. Do not import foreign history, add transfers, or mint certificates. The two distinct budgets charge their own actual reads/writes.

Keyword updates remain semantic after state adoption. Iterable/ordinary-Mapping updates remain ordinary semantic loops without adopting authority. The 17267/17281 generator refreshes, 18123 deferred return, and 18488 filtered helper overlay stay on these routes.

The nonempty state adoption at 18561 preserves destination-only lexical entries and existing positions. The nine clear+state-update pairs (16382,19628,19664,23126,23139,23177,23226,23276,23319) can share captured immutable supplied snapshots after clear. Pre-entry BoolOp/IfExp receivers and dict update14905 remain plain dictionaries; do not route them into store adoption.

No prototype cursor update/adopt/clear API is invented. These remain _ExecutionState adapter responsibilities.

## Joins: sparse and full paths remain distinct

Keep empty/singleton handling, first-state _fork_values conversion, authority joins, binding tuple unions and first-state mode behavior. Identical name data never discharges required strong/weak cell writes.

Enabled sparse compatibility still requires ExecutionState inputs, enabled authority, identical name meter and matching authority budget. Preserve the existing participating-cell plan and overlap/missing-cell checks. Capture every input cursor as an immutable version before callbacks or result name mutation. Duplicate source objects may produce repeated references to the same snapshot; no mutable cursor is passed to primitive join.

Call the namespaced prototype join with these frozen versions and the existing merge-name callback. It performs every required changed/pending normalization. Wrap its returned immutable version in a new result cursor. Then perform EVERY existing participating bound-cell write. Distinct existing-cell commutativity is the same prior proof; no new class of inputs enters this path.

For disabled, plain-Mapping, cross-context, overlapping-cell or missing-cell fallback, retain literal built-in set union, original input ordering, _merge_flow_values, full semantic transfer and sequential cell writes for every union name. State inputs may be captured as name snapshots before this loop; plain Mapping inputs stay plain and are never converted into extra ExecutionStates. The original first plain-Mapping conversion remains exactly where it already occurs.

The fallback result uses a new empty private cursor and ordinary setter loop in exact union iteration order. It therefore builds one private dictionary rather than an immutable version after each name. It does not invoke the sparse join or use a projection-only batch. Overlapping cells still observe exactly the old sequential writes. Return the private cursor without an unnecessary terminal publication.

Mode is a semantic property of authority; there is no disabled representation exemption. All modes use the same cursor/layer backend. Disabled transfer remains its original immediate-return behavior, and disabled joins remain full fallbacks.

## Authority-only seams and class finding

Keep captured-cell hydration15010, activation raw pops/argument installs18959–18964, helper-completion authority-only adoption19020 and its raw cell refresh19025–19029, and class authority-only adoption23596 in place. They are caller/child descendants on the same budget lineage; changing name representation neither replaces caller bindings nor imports class-local projections.

The class-body semantic RED reproduced on v19 is not closed by this plan. Preserve the relevant _statements/class-adoption bytes in the storage delta. Any separate semantic repair must be reviewed and combined deliberately; if it changes the intended predecessor, reissue the exact port lease/preservation comparison. Storage checks alone cannot authorize candidate acceptance while that blocker remains.

## Cost, order and failure obligations

- Forward all prototype dictionary/layer/history/pending/order/publication charges through _NameMeter into the same original _AnalysisBudget. No refunds, amortization discounts, raised caps or unmetered fallback.
- Charge adapter wrapper/reference allocations, input snapshot tuples, supplied state capture, cross-meter rebuilds, values tuples and unchanged full-fallback set operations where they actually occur. Remove a former charge only together with the physical work it represented.
- Do not construct a fresh _NameMeter per fork or compatible child. Do not reuse foreign-budget snapshots/history.
- Preserve exact insertion/deletion/reinsertion order, true dict_keys union inputs, first-matching alias behavior and raw-versus-certified entries. Keep the four existing identity-None alias guards unchanged.
- NameCursor snapshot/fork/keys/items keep their whole-operation staging contract. No new whole-_ExecutionState rollback guarantee is inferred: authority forks/adoption and semantic writes already fail closed through the original budget. Reads of names do not themselves publish.
- The immutable reference API publishes per set, but production setters use the owned cursor directly. Conversely, every actual fork can seal a tail; the measured 5415 public24 copies warn that publication may still be frequent. Bounded depth limits lookup attempts, not aggregate compaction or retained-snapshot memory.
- Preserve the prototype category caveat: publication_change_entry_visits is original private-tail size; publication_tail_entry_visits includes all sealed dictionaries, including compacted output. Completion requires successful operation return, not merely a spent publication charge.
- Capture constructor/private write cost, publication frequency/tail size, layer attempts, complete compaction visits/copies, history/pending work, full versus sparse join cost and terminal/repeated ordered reads. Do not infer runtime ratios from units.

## Proposed port and review sequence

1. After root grants a fresh exact-source lease, replace only the name-storage block and adapter/join seams above. Use systematic identifier namespacing; map prototype Meter to existing _NameMeter without changing charge delegation. No new import is needed.
2. Before any payload, issue create-only T/engineer-generator-v21.py (or coordinator-selected next version), full r010-to-candidate diff, exact v20-to-candidate delta, inverse/diff bounds, and static source inventory. A changed predecessor must stop this mechanical recipe, not bypass its guard.
3. Verify AST preservation for _AnalysisBudget including consume, all five analysis caps, _transfer_authority, _write_cells, _FlowValue and all existing authority stores. Canonically compare namespaced storage helpers to the reviewed prototype, enumerate every _names mutation/access, and verify only the generator changed among tracked paths. Keep old tests/generated bytes unchanged.
4. Root independently inspects exact source before dispatch. The permitted next checks require a separate run disposition: unchanged design53/depth contracts, authority matrix, public24 and the existing composition regressions on the real slots, followed by ordinary generation/downstream gates. Do not claim those results from prototype success.
5. Stop at a semantic, primitive-atomicity or supported-workload budget failure. Diagnose the category against this single design rather than adding a mode exemption or another local cost shave. The separate class-body semantic repair remains an explicit integration blocker until resolved.
