# V25 carrier review successor plan v1

> For any later authorized source work, use the executing-plans skill. This document authorizes no source authoring or payload.

Goal: close the five source blockers and two conformance gaps in the frozen v25 carrier implementation, using shared result boundaries and the existing authority/obligation channels.

Architecture: retain deferred objects independently of sensitivity; preserve immediate alternatives and container depth; consult current authority before reading collection contents; emit existing typed refusal causes at actual consuming boundaries. No new class heap, witness family, general interpreter model or storage optimization is proposed.

Tech stack: existing Python analyzer, immutable FlowValue/AuthorityRecord data, existing operation budget. No dependencies.

Spec: tests-checks/v25-authority-carrier-engineering-review-codex-a-v1.md, SHA256 7b0b322d2c91c6db51b1c9c7549b59413b89c2d02edb4fce6865d5eaede1627c; v25 plan v2 e2ed7f88a6c081be3ec54556e47a327ce1ea2d336e55200e788857cfec099bb8 and accepted owner/origin/projection/inheritance addenda remain binding.

All paths are under D:/Pontius-handoffs/v0a-i01-c-authority. Base is engineer-generator-v25-semantic.py, SHA256 481098d0be86d27f1664d0705a44a91d50b3a1361280a4e28c82bc366a541853. V25 remains immutable and unexecuted. Anchors below refer to those bytes. Root chooses the eventual successor filename and separately authorizes authoring and dispatch.

## Disposition of every finding

| Finding | Independent source assessment | Bounded disposition |
| --- | --- | --- |
| M1 ordinary deferred members disappear | Accept. The retention query fixes both flags false at15601; generator/local-generator branches15560–15567 then omit ordinary roots. Member installation15850 and escaped-member discovery20185 use that query for admission. | Retention discovers all supported deferred kinds and explicit issue roots. Sensitivity and class-origin policy are applied only at the appropriate consuming/escape boundary. Audit every existing admission use of this query, not just member installation. |
| M2 partial owner-ref union masks unresolved alternative | Accept. Merge strips per-operand proof13597, unions refs13611 and retains only selected operands13625. Owner traversal15733 follows live records and continues before raw mixed alternatives. | Retain each original recognized immediate class alternative before proof stripping; live tagged IDs never certify the whole merged receiver. Preserve unresolved alternatives through the explicit result-alternative channel and inspect them even when a ref union is nonempty. |
| M3 current invalidation loses to old projected read | Accept. Subscript20982/20994 and view22361 read the old projection. The added read gate20463 does nothing on failure, and unknown-only fallback20391 cannot correct a stale scalar/helper result. | A common current collection read view must dominate affected legacy selection/materialization; invalid current shape yields opaque current roots, never the old exact contents. |
| M4 typed issues do not reach syntax consumption | Accept. The immediate query18764 only yields generator roots; helper_deferred_refusal never reaches this blocker. Existing descriptor checks do not cover opaque issue carriers. | One reached-result issue path feeds calls and syntax iteration. It follows immediate alternatives only and exports the original helper-namespace cause. Mere lookup/storage/containment stays dormant. |
| M5 new allocation/reference work is undercharged | Accept. The8-unit singleton union is below the review's9-event allocation/reference floor even before visits/lookup; eager setdefault lists and carrier/record replacements add other omitted work. | Replace informal aggregate estimates with a source-level operation ledger, then charge every new visited/copy/allocation/dedup event through the existing budget. No cap increase or global equality audit. |
| Pair wrappers for items/popitem | Accept as a conformance defect, not a newly executed RED. Unknown popitem20402 exposes raw elements as the returned pair itself; items20407 lacks the pair layer. | Preserve the mandatory containment layer using existing opaque element carriers. No new positive key/value or general native precision is required. |
| LIFO sibling reversal | Accept as a conformance defect. Ordered inputs pushed with extend and removed with pop reverse the sibling order before ordered dedup. | Preserve the already-approved operand/edge order; do not narrow that contract after implementation. Use ordered depth-first expansion with reverse pushes, explicitly charging staging/reversal work. Never sort by private IDs. |

There is no rejected finding. These are source-proved omissions or design-conformance gaps. Neither the reviewer nor this author executed v25, so this plan asserts no public v25 wrong-clean, false refusal, cap failure or passing population. Earlier v23 RED remains evidence for the unchanged cases, not execution evidence for these newly inspected paths.

## Task 1 — one result-evidence traversal, with separate retention and consumption

- [ ] Refactor the existing role-aware traversal into a shared _result_boundary_evidence(value, values, *, immediate) result containing ordered deferred roots and ordered typed issue roots. It remains iterative, read-only, operation-local and budget-owned.
- [ ] Keep _retained_deferred_values as the all-deferred retention view, not a marker-only query. Keep _immediate_deferred_values as the immediate-iterator view. Add a small _has_result_obligations admission predicate covering deferred and typed issue evidence for existing carrier-creation sites.
- [ ] Add _record_reached_result_issues(value, values, site) as the single issue export boundary. It appends the existing helper-namespace refusal cause through the existing completion channel and returns whether it blocked. Only result-associated typed issue evidence participates; ordinary callable/capture/global projections do not become generic deferred refusals. It does not execute a generator, invent a throw/normal successor, or scan unread members.
- [ ] Make _record_deferred_generator_consumption invoke that boundary, while preserving its old direct-generator/local-generator execution paths and mode/default behavior. Calls' new opaque-consumer shortcut must use the same reached boundary rather than its separate marker-specific boolean gate.

Traversal rules are fixed: retain ordinary and marked generator/local-generator alternatives regardless of current sensitivity or remaining count; consult sensitivity/epoch policy only where consumption or existing unknown escape requires it. Immediate traversal stops at element edges and unopened named class tables. Ordinary callable captures/defaults are not immediate results. A typed issue inside a contained element is retained, not emitted by iteration of its outer container. Known __iter__/iter acquisition forwards its owner without treating acquisition as body execution. Unstarted close, invalid arity, default/one/full modes and existing explicit call-shape refusals remain unchanged.

The carrier-admission audit is bounded to existing v25 sites: class installation15850, member escape20183, reached helper shortcut20259, result adapters20391–20452, comprehension element binding20656, builtin adapter21912, existing unknown escape22573–22599, starred/destructuring22754/22868 and loop element binding23912/24341/24886. These sites use a common admission view; none gains a private marker test. Existing syntax consumers (starred literal/args, eager comprehensions, destructuring, For/AsyncFor, YieldFrom and membership where already consuming) receive the same issue boundary through their existing shared consumer call. Preserve roots and cause through helper/merge/consumption completion.

This fixes retention without claiming precise execution for ordinary generators newly transported through an opaque class member. Existing admitted direct precision stays intact; an already allowed reached refusal remains sufficient where exact consumption is unavailable. No blanket ordinary global-read or dormant-construction refusal is introduced.

## Task 2 — preserve every receiver alternative before joining refs

- [ ] At _merge_flow_values, after the unchanged identical-input early return, retain original recognized immediate class operands under explicit alternative carriers before _flow_without_helper_proof strips them. Include explicit implicit_class and helper_provenance.kind=="class" origins; arbitrary qnames stay ordinary.
- [ ] At _class_member_owner_ids, traverse these explicit immediate alternatives even when the merged wrapper has live refs. Read tagged owners through their current records; retain missing/unregistered alternatives as unresolved evidence. Do not reopen stale embedded record.value merely because it exists.
- [ ] Keep current owner IDs and unresolved/issue evidence as separate outputs. _retain_class_member_write emits the existing approved unresolved-origin store refusal when any relevant alternative remains unresolved and the incoming value carries callable/deferred obligations, even if other alternatives have live owners.

No identity is invented for the unresolved alternative and no alias-name rewrite is used. Scalar/non-obligation stores keep their approved behavior. Element/capture edges never become receiver alternatives, and the read-only named base edge remains selection-only. Retaining the original operand preserves actual proof/negative evidence; it does not promote an opaque wrapper to a callable, lexical cell or exact class member.

## Task 3 — current collection reads dominate old shape

- [ ] Add _current_collection_read_value(owner, values) -> _FlowValue, a transient read view. For an unmanaged/disabled-origin collection it returns the original object unchanged. A collection is managed here by its existing native mutable-collection identity/projection or current native collection record, not by authority_refs alone; a class owner is not a collection. For a managed collection whose every applicable current record proves compatible exact contents, it returns that current view. If an applicable current record is missing, opaque, retained/shape-invalid or incompatible, it returns an opaque view carrying current may-elements and relevant missing-store issues.
- [ ] Use it before the original Subscript selection and dict-view materialization, after evaluation of indices/arguments that may mutate the owner. Remove the unknown-result-only prerequisite for carrying an invalidated collection result.
- [ ] Apply the same read view at existing affected collection content/shape consumers: collection native results, list/tuple conversion and element extraction, loop/comprehension bound and target selection, and destructuring. Normalize managed collection results before _evaluate publishes its observation so ordinary Name and nested alias reads cannot expose an invalidated old sequence.
- [ ] Inventory direct .value content/length reads in these affected routes and record which current-state boundary dominates each. Any direct read used after intervening operand effects must refresh there, not trust an earlier observed owner. Existing current-shape mutation/token gates remain separate and cannot become true from admission alone.

This is no general projection rewrite: reads neither mutate a historical FlowValue nor reseed a record. No alias search is needed. Exact current contents may be used only if all alternatives justify them; invalidation failure cannot leave the earlier scalar/helper selection in place. Preserve independent explicit alternative evidence while excluding stale positive contents. The named class heap/descriptor/metaclass/global model does not expand. Existing unmanaged scalar/native behavior stays unchanged. The shared-list pair's exact native append path remains required, not replaced by conservative refusal.

## Task 4 — preserve pair depth and graph order

- [ ] Separate native result adapters: get/pop/setdefault/__getitem__ export selected/may elements as alternatives; copy/list/tuple retain element edges; popitem returns an opaque pair with element roots; items returns an outer element edge to that pair.
- [ ] A pair needs no invented exact key, member value, order or length proof. Represent it with existing opaque element carriers. Extracting from it exports may-elements; iterating the pair does not execute a contained generator. Existing exact native pair/view construction remains authoritative when supported.
- [ ] Known exact keys/values selection retains its existing distinction. An opaque map may retain conservative may-roots, but it cannot erase the pair layer or pretend those roots are the immediate iterator.
- [ ] Make every new graph expansion preserve ordered operand/edge traversal before dedup: FlowValue alternatives, authority-ref alternatives, current-record roots, carrier roots, selected named/base roots. Use reverse pushes for left-to-right depth-first traversal, with metered staging only where the source is not already reversible. Track role+FlowValue and role+authority-ID visits; first occurrence means first in that traversal.

This disposition fixes both concerns rather than weakening the approved role/order contracts. It adds no exact private allocation-ID assertion or new clean-support label.

## Task 5 — explicit new-work accounting and static handoff

- [ ] Retain a per-helper source accounting table before any successor payload: event, source operation, count/units expression, duplicate/hit/miss behavior and charged budget owner. Apply it to the two union helpers, all new result/owner walks, carriers/member bundles/current-shape invalidation, and newly added branches in transfer, record joins, helper reachability and callable detection.
- [ ] Count source-visible visits, set/dict attempts, pending/result/member/reference copies, tuple/list/set/dict and dataclass allocations, keys, output copies and ordered staging. Replace eager setdefault(name, []) with explicit lookup/new-bucket creation so charges follow real hit/miss allocation. Do not treat one append charge as covering a newly allocated pair plus all its references.
- [ ] Include new record/FlowValue replacement work and all explicit intermediate containers. The frozen field inventories are FlowValue18, AuthorityRecord6, DeferredResultCarrier2 and NativeCollectionEffect3. Allocation plus retained-field writes is a lower bound for each new object, not a complete formula for a compound expression; its surrounding tuple/key/copy operations must also be charged.
- [ ] Verify singleton, duplicate, existing-bucket, multi-root, shared-authority, missing-authority and cycle-shortcut paths against the source ledger. This is static accounting inspection, not new runtime tests or a new witness population.
- [ ] Use only the existing operation budget and propagate it on every new walk/copy. Keep nonrecord equality behavior and unchanged baseline equality outside this bounded audit. Disclose hidden Python implementation internals rather than claiming every interpreter allocation is metered. No discounts, epoch reset, limit increase or cap change.

The identical-input law remains mandatory: _merge_flow_values(name, (same exact FlowValue, ...), budget=existing) returns that same object through the existing first branch, before new carrier walks or semantic effects, including generators/opaque carriers. Do not move normalization ahead of this branch. This preserves the specific cross-lane storage composition premise; it is not a proof of any broader join-ownership optimization.

## Frozen limits and release sequence

All52 sensitive sources, harmless Models, traces, unreachable events and labels remain unchanged across the seven packs bound by engineer-checks/generator-v25-semantic-static-v1.json (a048320ff76815ab84a56987a86c11cbd6365c22698c5cc450dbe16a924e2cc1): composition4, scalar6, class12, name8, comprehension6, extensionR8 and ownerL8. No new fixture or oracle is authorized. The review gaps are not claimed covered merely by retaining that population.

- [ ] Root reviews this plan and separately decides source authorization.
- [ ] A future author creates one immutable T-only semantic successor from exact v25, with exact diff, touched-category/read-boundary inventory, new-work ledger and static preservation proof. W, main, tests and storage candidates remain untouched.
- [ ] Preserve the storage27 algorithm/AST boundary, existing two mechanical ExecutionState budget keywords, _AnalysisBudget/caps, other protected path bytes and all accepted lexical/class/global/prepass/exception limits. No storage composition is implicit.
- [ ] Root inspects issued source before dispatch, then uses the existing fixed52 controls and original gates: fresh D-local r010 snapshot, exact pinned overlay, actual floor interpreter first, scrubbed environment/Git/PYTHONPATH, -B -P, manifests and before/after hashes, W watch,60-second direct watchdog, partial failure custody, matching successful floor evidence before dev as required by each existing control.
- [ ] No result-driven expectation changes. If an existing required-clean contract cannot survive this bounded repair, report the conflict; do not widen the analyzer, weaken a label or add a witness family silently.

Only this plan is issued now. No source authoring, candidate import, analyzer/Model/oracle execution, config, snapshot, test mutation or commit occurred.

