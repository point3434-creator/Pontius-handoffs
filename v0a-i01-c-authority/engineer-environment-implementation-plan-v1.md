# Environment implementation design v1

2026-08-31. Pre-edit engineering design; no source edit or payload execution.
Bound to generator v19 SHA-256
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.
This refines engineer-environment-reassessment-v1.md; it does not authorize implementation.

## Decision and evidence

Select an immutable path-copied AVL name index plus a lazy legacy-order recipe, not a flat COW dictionary or a two-index insertion-order map. This is a concrete conditional design, not a claim that ordinary generation will pass. Gen06 still refuses the same historical-inventory helper item at work262149 against262144. Its492 selected v19 plans saved15780 measured units, while transfers/gets/copies/items/forks account for184711 units. Further local binding heuristics do not remove repeated full environments.

The proposed boundary is ExecutionState names, their projection/adoption seams and merge materialization. Object/cell/result/observation stores, helper language support, exception partitions and all five caps remain unchanged. A structural prototype must earn continuation before production integration. Exact-order demand can defeat the benefit; that is an explicit no-go, not a reason to weaken order or metering.

## Selected representation

A NameVersion holds: immutable AVL root; immutable order recipe; parent version plus the names changed relative to that parent; and a coupled normalization context. A NameEntry holds the immutable FlowValue and its registered/pending status. AVL nodes hold one name/entry, left/right children, height, subtree size and pending-entry count. Exact string comparison determines the index only, never exposed iteration order.

Lookup follows one balanced path. Assignment/deletion path-copy and rebalance only visited nodes; overwriting an existing name preserves its order; deletion followed by insertion appends it. No first-write full dictionary copy occurs. Fork shares the version and forks existing authority/binding stores. Pending counts permit enumeration of only pending subtrees. Rotations, comparisons, visits, copied references/nodes and allocations are charged; do not hide tuple copies behind a one-unit allocation.

A version records changed names, including deletion and raw projection. Common-base discovery walks parent-version links with a charged identity set; it is O(H), not free. Join unions changed names from the common base to every input, adds pending names, and computes each candidate with the existing ordered input-state tuple. Unchanged certified entries may share state0's nodes. A merge version records actual resulting changes relative to state0; a metadata-only order change still has its own version. Empty/reset or unrelated histories fall back to a complete name join. No semantic history or authority is pruned.

This design deliberately does not add a second persistent insertion-ordinal index: that index would still need N ordinal rewrites to express the current set-union reorder. The AVL has no tombstones and no compaction phase. Version history can retain O(total edits) metadata; discovery costs are explicitly charged and measured. If history traversal rather than changed names becomes quadratic, stop and redesign rather than adding an unmeasured ancestry cache.

## Exact order policy

Order remains a safety obligation. First-match alias consumers use values.values() at16703/16717,17510,17572. Two same-identity projections are not proven interchangeable. Do not change these non-None searches to tree order, insertion-order union, arbitrary alias selection or canonical authority lookup.

Order recipes are Empty, Materialized(keys), Edit(parent, insert-or-delete, name), and LegacyUnion(parent-order-roots in input-state order). Overwrite creates no order edit. A merge attaches LegacyUnion without immediately enumerating all names. On an order demand, realize the same operation as current21285: set().union(*(state.keys() for state in states)), using ordinary dictionaries reconstructed with the parents' exact key order. Verify this compatibility on both interpreters and multiple hash seeds; do not assume sorted keys or an ordered union is equivalent.

Realization is iterative postorder, not recursive Python stack growth. Collapse a consecutive Edit run into one temporary ordered dictionary, apply edits in chronological order, and freeze its keys once. Never materialize every prefix of that run. For LegacyUnion, realize parents, perform the actual built-in union, then freeze its iteration order. Charge every recipe visit, input/output key visit, temporary allocation, dictionary/set operation and copied reference. Publish a memo only after successful completion; budget failure cannot publish a partial answer. A completed memo may release its now-unneeded recipe-parent references; retained snapshots keep their own values and authority roots.

Ordered items/values must not pay N separate AVL lookups invisibly. For a previously uncached version, visit the AVL into a temporary name-to-entry index and assemble pairs in the realized order, charging both traversals and the temporary copy. Repeated reads of that immutable version can share the cached pairs but still charge their actual visits. The adapter must preserve the observed Mapping/view behavior at existing consumers; mutating-while-iterating calls require an explicit compatibility check, not an assumed snapshot view.

Worst case is deliberately admitted: the first ordered read after S uncached merge ancestors can cost O(N*S), and overlapping/missing-cell fallbacks can force that cost at every merge. Lazy recipes defer that work; they do not abolish it. Terminal ordered reads belong in RED/GREEN so deferred work cannot masquerade as a structural improvement. Sharing/caching is useful only when actual consumers avoid or share those demands.

Four small demand guards are semantically justified within this design: when the bound mutable_collection_identity is None, return the already-bound default without constructing/scanning values.values(). Exact sites are16700-16708,16714-16722,17507-17515,17569-17578. Every candidate fails the existing predicate in that case. Non-None behavior stays exact. Other scans, including16852 shared-identity collection and17873 reflective invalidation, remain real work.

## Normalization and store ownership

A normalized flag is not a guess based on current value identity. An entry can be certified only by the full existing transfer path in this state's object-store context, or inherited from an already-certified entry through a proved record-preserving fork/join/adoption. Raw projected values are pending. Missing-reference refusal/obligation behavior remains exactly in transfer. External mappings and uncertain provenance take the existing full path.

For enabled state, transfer of a certified entry is idempotent: registered authority refs remain present, or the immutable value contains no remaining registration work at this entry boundary. This must be proved for all FlowValue forms, including nested maybe_unbound/starred forms and retained helper edges. If a form cannot carry that proof, leave it pending and transfer it normally. Disabled state does not create an enabled-state certificate.

A fork preserves the coupled context. A same-budget monotonic object join retains all input keys, even when their records merge; that supports input certificates. Authority-only adoption is permitted without invalidation only when a proved descendant/join context covers the previous name context. Otherwise mark the old projection pending through a charged traversal. Do not infer ancestry from matching integer IDs or the same budget alone. No cached state-dependent helper effects are introduced.

Audit both authority-only replacements: helper completion18463 and class completion23026. The class body starts from a fork at23000, but continuation must preserve that ancestry. ExecutionState.update currently overlays names while replacing authority/bindings; leftover old names cannot borrow supplied certificates. An empty-destination replacement may share the whole coupled version. A nonempty overlay preserves old key positions and performs a charged full compatibility path for leftover entries. Constructor from an ordinary mapping retains full traversal; this proposal does not hide that remaining cost.

Fresh/raw projections do not eagerly normalize on lookup: captured-cell hydration14453, raw argument binding18407 and post-helper projection18471 preserve their existing timing. They become pending for the next existing transfer boundary. Projection-only removal18404 differs from semantic deletion and must not write an unbound cell.

## Merge and cell-write proof obligations

First join object/cell stores and binding alternatives exactly as now. Resolve changed and pending names through the full existing merge/transfer operations. Keep input-state ordering in merge_flow_values and preserve all refusal reasons, retained edges, activation identities and source points. No generic setter optimization is authorized by this design.

Then perform every old participating bound-name write, even when name roots are identical. The existing _write_cells helper retains strong versus weak behavior. If all participating cell IDs are distinct and already exist, delayed writes commute: transfer reads objects, not cells, and updates do not alter cell insertion order. Meter discovery, identity overlap checks and accesses.

If any participating IDs overlap, or a cell is missing, realize the exact legacy merged-name order and perform cell writes in that order. Do not omit even apparently redundant strong or weak writes. Allocation numbers are opaque and may be alpha-renamed, but alias graph, shared/distinct identities, source points, activation ownership and ordered alternatives must remain equivalent. This is narrower than claiming literal old IDs/allocation order. If any semantic consumer observes numeric ID order, stop; no such consumer has been established by this audit.

## Cost contract and compatibility surface

With N names, D candidate changed names, P pending names, H examined history links and B participating bound cells: lookup/update/delete cost O(log N), fork O(1) for names, and the optimistic name-join path costs O(H+(D+P)*S*log N+B*log N) plus actual transfer graph/cell work. Here S is the input-state count. Existing object/cell joins are additional. Ordered realization adds the explicitly measured recipe cost, potentially O(N*S) across accumulated merge history. There is no claim that every merge is O(D).

All physical node/reference copies, comparisons, lookup visits, history/delta enumeration, joined entry reads, pending discovery, order materialization, cache construction and cell planning are charged at their actual multiplicities. A slower fallback keeps the planning charges already spent. All five admission caps and fail-closed budget behavior remain unchanged.

Replace only the audited dictionary seams: ExecutionState14086-14181; fork_values14415; projection14453; projection drop/set18404/18407; authority adoption/projection18463/18471; merge21269-21332; class adoption23026. Preserve semantic scope-exit pops21588/21590 and all current clear/update pairs. Search all dictionary bypasses, Mapping assumptions and iteration/mutation consumers again before freezing. Plain pre-entry dictionaries remain valid inputs. Do not silently change a dict-only consumer or Mapping.update overlay semantics.

## Implementation sequence and falsifiers

1. Root accepts or rejects this bounded design and the Stage0 interpretation. No production changes before that decision. Keep exact v19 as predecessor and measurement control.
2. Build the structural RED family through the public analyzer: vary ambient N, normal/exception successors S and changed D; include D=0, small fixed D, terminal ordered read, repeated ordered reads, raw entries, deletion/reinsertion, alias divergence, overlapping/missing cells, unrelated adoption and enabled/disabled transition. Use harmless independent runtime oracles; do not execute sensitive inspected bodies.
3. Measure predecessor real copies/transfers/reads, not only its existing charged total. Implement the isolated map/adapter and route the listed seams; preserve the full transfer and shared cell helper. Remove v19's sparse planner when the new merge supersedes it. Keep v15/v16/v17 corrections and v18 fork allocation/single-get behavior.
4. Run focused state/ordering/normalization checks and design53 plus matrix192/212 on actual3.11.15 then3.14.6, source/receipt bound. Compare public rows/blockers and the canonical census. Differential order checks use the actual legacy algorithm, adversarial equal-hash keys where the harness permits, and several fixed hash seeds. This is supplementary evidence, not the public behavioral oracle alone.
5. Run ordinary corpus generation under unchanged caps. Only demonstrated structural savings including final materialization, preserved outputs and corpus GREEN justify freezing for independent review. No broad suite before the existing frozen-snapshot workflow permits it.

No-go if exact ordered reads or ancestry traversal merely move N*S cost, persistent lookup charges erase savings, normalization needs guessing, alpha-renaming changes behavior, authority history is lost, a full interpreter rewrite is needed, or multiple independent maps must be redesigned to make this work. The current design is coherent as a conditional storage replacement; its performance adequacy is unproved and it is not a release-ready repair.
