# v25 carrier and current-authority engineering review v1

Author: codex/r010_cold_a. Independent bounded engineering inspection by a prior test author; not a cold review.
No candidate, Model, analyzer, oracle or test was executed. No new witness was authored. No candidate/source/test bytes changed.

## Subject and scope

- Source: engineer-generator-v25-semantic.py, SHA-256 481098d0be86d27f1664d0705a44a91d50b3a1361280a4e28c82bc366a541853.
- Exact v23 delta: engineer-generator-v25-semantic-from-v23.diff, SHA-256 6f1499e085f9b3bb85d8cbd93e63a1d27810b511c4d0a332b25da4a59e0e4a02.
- Category inventory: engineer-generator-v25-semantic-category-inventory-v1.md, SHA-256 455f8ff35988f3d359577e13da78ae3cd44ae2c4d11ce861da208c44124c61f8.
- Author's static proof: engineer-checks/generator-v25-semantic-static-v1.json, SHA-256 a048320ff76815ab84a56987a86c11cbd6365c22698c5cc450dbe16a924e2cc1.

Normative design inputs: v25 plan v2 e2ed7f88a6c081be3ec54556e47a327ce1ea2d336e55200e788857cfec099bb8, v3 1d661231a472fc689af06ea993234f27ab88a65da950d83f1811c1f941d94723, origin clarification v2 458e182d3bfc8e715e1f9f2be0762fe1237088570a98c81f1958b1f766b22e70, projection companion 96bbf47d1251b5249e7796c6f3f9482f6a2a6e2b257c26207f0b5e7e6c9ae21e and inheritance clarification 6f1aeb1b68593ac5f3c863d4137b5008700eb5cf5b5f88a72d8252a043cc7582. The older plan v1 remains context where those successors do not replace it.

Focus: current record dominance, carrier roles, named/base owner transport, scalar-projection origin, collection shape gates, reached refusal causes and newly introduced accounting. Root independently covers other semantic integration. All anchors below refer to the frozen v25 source.

Disposition: no static clearance. The five issues below need correction or a concrete source proof that excludes the path before treating v25 as ready. They are source-proven omissions/contract gaps; no public v25 wrong-clean output, budget failure or new runtime RED is claimed.

## Must-fix source issues

### M1 — ordinary deferred roots disappear at member installation

_deferred_result_values at15560–15567 returns an ordinary generator only for immediate=True, all_deferred=True, or class_scope_unresolved. It similarly omits ordinary deferred_local_generator in the default retention mode. _retained_deferred_values at15601 fixes both flags false.

_with_class_member_authority at15847–15853 selects a member only if callable authority, that filtered retention query, or class-owner obligations succeed. A plain generator produced in an enclosing function and assigned into a class namespace has no callable_definition/helper_provenance merely because its delayed body calls a helper. With no other metadata it fails all three predicates and is absent from the named member table. The later named read has no root to export. The escaped-member scan at20181–20193 repeats the same filtered query. This is the same loss category as Q05/member transport, not a request for general generator precision.

The direct generator consumer already has a sensitivity/refusal path at18078/18949; losing the object at the member boundary prevents that path from receiving it. The class-origin marker controls a particular refusal policy, not whether other deferred objects retain their existence. Keep retention/discovery separate from current sensitivity and origin. A permitted unsupported refusal is sufficient; silently deleting the ordinary root is not. No new safe-case precision promise is demanded.

Related callers of the filtered predicate at20391–20451,20657,21916,22754/22868 and23912 also use it to decide whether to create result/element carriers. A correction should audit this predicate's admission role across those existing sites rather than changing only the member's if statement.

### M2 — a live ref union hides an unresolved immediate class alternative

_merge_flow_values at13595–13622 constructs the legacy merged value from operands stripped of helper proof/refs, then attaches the union of refs. Its helper_obligations retention condition does not preserve every provenance-only class operand. A mixed implicit_protocol_merged class result can therefore contain both a live tagged class alternative and a structurally unregistered alternative while exposing a nonempty ref union.

_class_member_owner_ids at15731–15761 follows the union's live records and then continues. It does not traverse current.value immediate alternatives on that branch. Thus the tagged alternative suppresses the unregistered alternative's unresolved-class evidence. The fallback in _retain_class_member_write at15873 then does not run, although the origin-v2 contract explicitly requires every unresolved/missing alternative to survive a join.

Retaining the stored root only on the live class record does not repair access through a preexisting alias of the unregistered alternative. This is an unsound completeness inference from a partial ref union. Preserve per-alternative unresolved evidence before/through merge, or reject that mixed owner at the reached store. Do not infer completeness from any tagged ID, and do not allocate a fake alias identity. No additional public program was executed.

### M3 — current-shape failure does not suppress legacy projected reads

The new _current_exact_collection_value at15895 correctly rejects missing, retained/opaque or incompatible records. _invalidate_collection_result_shape at15915 replaces current record.value with unknown and retains current may-elements. However, the gate is not dominant over the original read:

- _evaluate_value(Subscript) at20979–20993 still returns _flow_mapping_value(base, key) or base.value[index] directly from the projected value.
- _evaluate at20391 adds the new alternative carrier only when that result is unknown.
- The later current-record gate at20458–20469 only overwrites a result when exact current shape succeeds. A rejected current shape leaves the earlier projected result untouched.
- The dict items/keys/values path at22357–22390 likewise materializes direct_owner.value before _collection_authority_result's current-shape check.

A contained/captured/other historical alias can retain that old projection: _ExecutionState.__getitem__/get at14959/14978 return the stored projection, while _poison_mutable_collection at18732 scans only current name projections with the mutable identity. It does not rewrite nested aliases. Reading such an alias can select an old scalar/helper instead of exporting the current opaque may-roots. A direct scalar/helper result then misses the unknown-result fallback. This source path defeats the plan's no-stale-recovery guarantee even though both newly named gates exist.

Make current authority determine whether every affected legacy read is admissible; otherwise return an opaque result carrying the proper current roots or an allowed refusal. Do not repair this by reconstructing current records from a stale projection or by broad alias-name rewrites. The unchanged shared-list pair checks exact append transport, not this invalidation/captured-alias route.

### M4 — typed missing-member/base obligations do not reach syntax consumers

_class_member_owner_ids/_class_member_obligations at15724–15775/15813 create helper_deferred_refusal roots for missing/unresolved ownership, and named selection wraps them as alternatives. Ordinary calls can find them through _reachable_helper_authorities at19426 and export a helper-namespace refusal.

The syntax path differs. _record_deferred_generator_consumption at18760–18772 asks only for immediate generator roots. _deferred_result_values does not return helper_deferred_refusal or helper_refusal evidence as such, so a pure typed refusal carrier produces no immediate generator and returns unblocked. _record_implicit_protocol_blocker at17079 does not close this gap: its helper/protocol paths inspect descriptors, and _implicit_protocol_descriptors at16241 ignores opaque carrier/refusal values.

For/async-for at23881–23900 uses these two checks before continuing. Destructuring at22845–22855 and the other syntax iteration paths have the same boundary. The typed issue therefore does not satisfy the promised reached-consumption refusal contract on these routes, even though it remains in the object graph. Class-header handling at24486 does not establish a universal earlier refusal for a provenance-only qname base.

Use a reached-only issue path that is distinct from “consume all retained generators”; it must not turn mere storage, lookup or containment into execution. This is a cause-propagation omission, not a claim that an actual public v25 failure was measured.

### M5 — new metadata operations exceed their stated aggregate charges

The approved contract counts new visits, allocation, dedup and copied references. Passing the existing budget to a walk establishes its owner, not enough units.

A minimal source count for _ordered_flow_roots at9055 is decisive: one group with one distinct root and empty refs charges3+1+2+2=8. Even excluding traversal and lookup costs, the declared model has at least9 allocation/reference events: result list and seen set allocations(2); key tuple allocation and two reference writes(3); inserting the key ref and appending the value ref(2); output tuple allocation and one reference copy(2). The seen lookup, group/root visits and other work increase that lower bound.

_join_member_obligations at9080 eagerly evaluates [] for every grouped.setdefault(name, []) call, including existing-name hits; its two-unit charge does not account for all list allocation, dictionary/bucket activity and appended group refs. Result (name, roots) pair allocation/copies are also not matched by the result-loop charge.

_carrier_result at15617 charges3+len(old obligations), but creates at least four new objects before reference-copy accounting: payload, carrier FlowValue, obligation tuple and replaced result FlowValue.

The sibling new walks need the same audit:
- _deferred_result_values15513: pending edge tuples, role/id and role/ref keys, seen insertions, result/pending copies.
- _element_result_values15624: pending/result/seen storage and output-copy costs.
- _class_member_owner_ids15695: role-aware keys/sets, appended IDs/issues, carrier/base edge pushes.
- _with_class_member_authority15826 and _retain_class_member_write15862: member pair/root tuples and record replacements.
- _invalidate_collection_result_shape15915: new current/carrier/opaque/replacement metadata and roots.
- The new carrier branches of _reachable_helper_authorities19434 and _has_callable_authority19884 need their new reference work checked alongside the existing traversal charges.

This finding concerns newly introduced operations, not a demand to retroactively meter every old analyzer allocation or to count hidden Python dictionary internals. No cap increase, discount, or relabeling of cost units is justified. Establish an explicit accounting map/lower-bound argument before runtime fitness claims.

## Other source-conformance concerns to resolve explicitly

**Containment adapters.** At20402 unknown popitem is grouped with get/pop and forwards raw may-elements as immediate alternatives. A native popitem result is a pair container, not the contained deferred value. Unknown items at20407 similarly preserves only one element layer where each yielded item is a pair. Flattening those wrappers can turn later iteration of the pair into apparent consumption of a contained generator. This needs an API/scope disposition; it is not a new demanded clean assertion for unsupported native precision, nor a reported runtime failure.

**Ordered graph traversal.** _ordered_flow_roots preserves the order it receives, but the new graph walkers use pending.extend(ordered_roots) followed by pop(), reversing sibling traversal before their final ordered union. _class_member_owner_ids similarly reverses owner alternatives. The approved plan requires operand/edge order and first occurrence preservation. If the order contract was intended only for direct unions, state that narrower boundary explicitly; otherwise fix traversal without sorting by private IDs. No public private-ID/order assertion is proposed.

## Supported design pieces and category inventory

| Category | Source support | Remaining limit |
| --- | --- | --- |
| Current object/record ownership | _AuthorityMap no-op record checks use identity; COW records remain immutable; joins explicitly preserve tag and named/wildcard unions. | Accounting M5; union completeness M2. |
| Enabled class construction | _finish_class_definition24621 creates the bundle only on normal class completion; _with_class_member_authority reserves owner identity before _bind_name, including empty bundles. | M1 selection; no blanket construction refusal is needed. |
| Scalar projection origin | _assign23061 attaches an explicit alternative to the previous recognized class owner while preserving the legacy mapping result. | Source route supports the approved companion; arbitrary mappings do not mint class provenance. |
| Read-only bases | Only member_lookup follows class_member_base; requested name remains fixed per operation; current tagged record edges are read instead of copied member snapshots. Instance writes exit before following class read edges. | M4 missing-base consumption; no positive MRO/shadow precision established. |
| Marker copies/joins | Same-identity generator merge OR-retains class_scope_unresolved; mixed direct/merged generators preserve explicit alternatives; empty-and-unchanged check is shared with epoch comparison. | Retention filter M1; this is source inspection, not R8/Q05 passing evidence. |
| Immediate versus element | _DeferredResultCarrier is immutable/identity-equal; immediate walk stops on element edges; class member tables are not globally opened as iterators. | Adapter wrapper issue above and refusal issue M4. |
| Native mutation | _NativeCollectionEffect is call-local; admission-only tokens have shape_exact=False; matching exact update checks owner refs and mutable identity. Invalidation reads current records. | M3 legacy read dominance; no new reverse/sort/index precision. |
| Transfer/copy channels | Carrier roots, starred/base values, helper obligations/defaults/receivers and merged payloads are transferred; named/wildcard roots initialize before the ordinary live-ref shortcut. | New accounting M5; no proof of entire analyzer recursion/cap behavior. |
| Refusal export | New opaque active consumption/store reasons use helper namespace; helper completion forwards that channel. | Typed graph issues need every consuming syntax boundary, M4. |

## Fixed 52-case custody and coverage limits

All seven packs were independently rehashed against the retained static proof. No source/Model/trace/label changed:
- class-semantic-extension12: 925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268.
- class-name-boundary8: 31c50af8fda3cebc65e44d655db600dd1029a3e110b711a82d475750ece05a1c.
- class-comprehension-boundary6: 9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71.
- class-comprehension-extension8: eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd.
- class-owner-late-store8: 08fce0e37eaeb24192c4f227677d7625097748ccb2cbc79470df4699718a9b47.
- storage-composition4: faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709.
- scalar-class-composition6: 50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac.

Q05 challenges the class-created member carrier; R05/R07 challenge joined marked alternatives and changed empty iterators; L01/L03/L05 challenge direct/contained/captured late-store aliases; L07/L08 distinguish unresolved-origin deferred store from scalar storage; shared-list-consumed/dormant challenge exact native append. They remain necessary, but none is claimed to cover every omission above. Do not relabel the fixed52 from future results.

Review was read-only source/text inspection with hashes. No new source fixture or runtime oracle exists for these observations. Root owns any bounded diagnostic decision, correction and later dispatch.
