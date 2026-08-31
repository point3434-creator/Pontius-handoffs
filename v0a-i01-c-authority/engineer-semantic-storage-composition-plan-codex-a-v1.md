# Semantic and storage composition preparation plan

> **For agentic workers:** Use superpowers:executing-plans only after a separate root authorization to author a composition. This document authorizes no composition, installation, candidate import, payload, test, or commit.

**Goal:** prepare a bounded, reviewable composition of an independently frozen semantic successor and the storage lane without dropping either lane's behavior or evidence obligations.

**Architecture:** use the approved semantic source as the future composition baseline, transplant only the pinned storage primitive and three adapter intersections, and preserve semantic class projection at every merge boundary. The new disabled shortcut is eligible only where its complete semantic callback is proved identity/no-effect; a low-level merge identity law alone is insufficient.

**Tech stack:** the existing Python analyzer, immutable FlowValue/authority records, NameVersion/NameCursor, original AnalysisBudget, and standard-library AST/source comparisons.

**Spec:** the root's bounded preparation request; `coordinator-disabled-join-operation-disposition-v1.md` (320df60041e12736d19f40b7f7bdfdc39b064cd6d42f2c1696fd36c8fa42295e); `engineer-generator-v25-review-successor-plan-v1.md` (56c1b494349ea3b70af3eee2f26d9bf99fab72db1725b5b833b4af187be4ac34); the accepted semantic plans/addenda named by that plan. All relative artifact paths below are under D:/Pontius-handoffs/v0a-i01-c-authority.

## Scope and current standing

This is engineering preparation, not implementation or review approval. V31 is being authored and was not inspected. Its future source, diff, inventories and proofs are required inputs before this plan can be executed; the v25 map below cannot be assumed to describe its final changes.

V25 remains a frozen predecessor with known source findings. V30 is not runtime-ready: root's `coordinator-v30-design-verification-v1.json` (ed57b0fa44fda469f2291268682774bda02e82f5bc13dc9bbfca9d807c2acbf1) records 53 tests, 52 passing, no errors/skips, and the generator70 exact-depth method still receiving the work-cap refusal. Receipt ae46f1f92f9f7de5e554f5cc1f51694a4bd69d6856acce12e099389319a6391d. Neither combining files nor a semantic fix relabels that failure. No dev/matrix/corpus expansion or acceptance follows from this plan.

The only work performed for this preparation was read-only source/document/hash inspection and standard-library AST parsing/diffing of the four named frozen sources. No source, test, Model, oracle or analyzer was imported or executed. No composed source was created.

## Global constraints

- Keep all issued source, test, case, expectation, output and evidence bytes immutable; any authorized work receives a new T-only version.
- Preserve the original budget object and caps: work262144; container4096; cardinality2147483647; helper depth64; child depth4. No new budget, discount, reset, cap/message relaxation or unmetered new traversal.
- W/main, generated outputs, inventory census, old119 inventory tests, prior141 rows, existing matrix expectations and the fixed52 semantic cases remain outside this authoring plan. Root owns any separately authorized publication/census work.
- Payloads remain root-dispatched, one explicit slot at a time, in fresh D-local exact-candidate snapshots with actual3.11.15 first, then3.14.6 only after its required matching floor gate. Preserve -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment, D-local temp, validated absolute Git, full identity before imports, exact manifests, watchdog and incomplete/failure custody.
- No owners, protected fixture bodies, GPU, broad wall, source seal/rehearsal or install capability is implied. Final Tier C cold reviews and any subsequent broad gate remain separate requirements.
- Current instruction copies read: W/CLAUDE.md fe8e8ec5d06f8d7f225dfe836d096dd098b2179de0d3fa35e42ed044e495702d; W/docs/workflow.md 81022af7449f0a107787987a15bcd2ac6b53641806a7620671bedf1d1b0b0635; amendment3b43c3c21426e9d0ebb26ec0bfb9215373740877c77b28de0e06fb0a4eadad0a. Root's task-specific restrictions govern this preparation.

## Frozen comparison inputs

| Role | Source | SHA-256 |
| --- | --- | --- |
| Common full-lane baseline | engineer-generator-v22.py | 61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3 |
| Semantic prerequisite baseline | engineer-generator-v23-semantic.py | 53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499 |
| Frozen semantic predecessor | engineer-generator-v25-semantic.py | 481098d0be86d27f1664d0705a44a91d50b3a1361280a4e28c82bc366a541853 |
| Frozen storage lane | engineer-generator-v30-storage.py | 1a28fce14cfdd2ee30d9892b7d2719aba8ec152d99d1e3c915660648cf9756fd |

The semantic delta v23→v25 is6f1499e085f9b3bb85d8cbd93e63a1d27810b511c4d0a332b25da4a59e0e4a02. The prerequisite v22→v23 delta isa6a69bfa10ad120f423c025d76112391320a71bb5222319a4e339351851eaec8. Both matter: restricting the comparison to v23→v25 alone hides two adapter conflicts already introduced by v23.

The complete storage lane is compared with v22. Its immediate v29→v30 delta isd50c98213038bbedd0060c5136b8150b7e33832a64d406af8f33801863517fff; it adds only the two enumeration accounting calls. Earlier storage-specific stages are retainedv26 (1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951), v28 (4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e), andv29 (b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466).

Required frozen proof inputs already available:
- semantic v23 static64439a89ea77835aabf68f29290ad6d491ca1602a4e6ee5bdfed1034c3e709e0 and v25 statica048320ff76815ab84a56987a86c11cbd6365c22698c5cc450dbe16a924e2cc1 under engineer-checks/;
- storage v30 static14506755969039902f8c951d111991b806f814e185face0372367579a4ff3f29, preservation5bd766b888984b8ddc81073e10d8bf1ff7c595c4e37d6fe5872336e1ca7505b8, accounting8d89ca2da1d66b5e52ee1eb6d12925b3972e7f96762869d185b098dd7581a094;
- root v30 source inspection169bfc18b9943d10f2433729e1f2c37cc6684f1146be0aa4ededb135dfefed9f;
- v28 binding proofd786b9a609a37bf88ea18d6d6585d2ffb6cafd6ced908d23c1e086291ed8650c and qualified v29 engineering reviewtests-checks/v29-disabled-join-engineering-review-codex-a-v1.md f397975e37f00ea9512563e91dea9bc89ae7f9dda2ce96ab2f5ed5ba1dc610ad.

These proofs are input evidence to recheck, not substitutes for a combined-source proof.

## Exact overlap map established from the frozen sources

Independent AST comparison, excluding location attributes, finds only `_SourceOrderedResolver.__init__` overlapping between the direct v23→v25 delta and the complete v22→v30 storage delta. Including the required v23 semantics produces the following three real method intersections.

| Region/method | Semantic obligation | Storage change and composition rule |
| --- | --- | --- |
| Name primitive: v25 lines14317–14912; v30 lines14086–14982 | V25 preserves the v23 layered primitive exactly; it does not authorize changing ownership fields outside this region. | Replace the primitive with the pinned v30 **47 nodes:41 definitions+6 constants**. Keep NameMeter separately exact and budget-owned. Preserve every attribute name, slot string, local binding and literal; no tokenize/name-wide renaming. Remove only the replaced layered definitions/constants. |
| _ExecutionState.__init__: v25 line14916; v30 line14986 | V23 allocates real local cells as _LexicalCellId(serial), with the2-unit token charge, before the existing parent/name shortcut. | V30 adds exact dict/ExecutionState unique-entry bulk construction at15014. Apply that producer after the semantic allocation/setup; do not replace the whole class with v30 and lose lexical ownership. Preserve parent forks, inherited Entry identity/proof OR pending debt, raw projection behavior, conditional cell writes, detached order and publication timing. |
| _SourceOrderedResolver.__init__: v25 line15287; v30 line15248 | Keep _class_frame, three-component _helper_effect_shapes, and especially the metered _class_module_values snapshot at15425–15429 **before** entry overlay. | V30's borrow window replaces only the old entry update (15389–15432). Put it after that semantic module snapshot, preserving the exact empty-prepared-map/scope/registry guards, entry truthiness and final existing ExecutionState fork. Capturing module values after borrowing entry would import caller/class projections into the module fallback. |
| _SourceOrderedResolver._merge_states: v25 line23261; v30 line22351 | Keep _CellIdentity annotations and class-aware projection in both old full and sparse callbacks. | V30 adds disabled sparse retention and full unique-entry bulk publication. All three merge-value sites must remain class-aware; the new disabled omission additionally needs the wrapper identity guard described below. Preserve ordered authority/binding joins, cells and transaction boundaries. |

The two approved semantic ExecutionState budget changes are additional preservation touchpoints even though storage leaves those methods unchanged: `_write_cells`15044 and `__delitem__`15050 use `budget=self.authority.budget`. Do not revert them by wholesale class replacement.

The remaining v25 semantic changes—authority records/maps/join/transfer, captured-call environment, semantic merge helpers, carrier helpers, class/consumer/read paths and source-ordered helper return—are semantic-lane-owned and source/AST-exact except any explicitly enumerated future composition call-site changes. Current module-level nondefinition differences are disjoint: v25 adds typing.Literal; storage replaces the sealed-layer threshold with four radix constants and retains its two sentinels. Storage does not require replacing semantic imports or definitions outside its proven region.

## The wrapper law is not universal

V25 `_class_merge_local_projection`16057–16092 delegates directly to budgeted `_merge_flow_values` only when no class frame is active or the name is outside both local/free-name sets. For an active affected name, identical `unbound` operands take the new-unbound path16078–16079. Identical `maybe_unbound` operands are flattened and rebuilt at16084–16092. Thus the wrapper does **not** universally preserve the exact input object's identity. This is source proof, not a newly executed witness.

The future composition must:
- retain the semantic helper at every changed/unproved merge site;
- require a charged `self._class_frame is None` guard before the new disabled unchanged-entry optimization, taking the original class-aware full fallback otherwise;
- retain all other v30 exact-type, same-budget/meter, all-pending, common-history, candidate and per-entry guards;
- make no assertion that disabled authority implies the semantic callback is identity;
- require a separate reviewed proof before any later per-name refinement of the class-frame exclusion.

This narrow exclusion is the proposed composition correction, not an edit to v30. The low-level identical-object law remains necessary and must still be re-established on the final semantic source; it is not sufficient by itself.

## Operation-budget and callback closure

V30 has three direct calls lacking the semantic successor's required operation budget:
-22533: changed/unproved name inside the disabled staged branch;
-22563: full bulk producer;
-22584: enabled NameVersion join callback.

A naked retained call must be `_merge_flow_values(name, supplied, budget=self.budget)` (or `values` at the third site). But adding these keywords alone is **not** a correct composition: it drops class projection. The preferred class-preserving form at each site is `self._class_merge_local_projection(name, supplied)` / `(..., values)`; the existing helper's signature has no budget keyword and its low-level calls use `budget=self.budget`. Keep its frame-None delegation unchanged. Do not invent a new default budget or pass an unsupported keyword to the wrapper.

After the semantic lane freezes, enumerate every Name reference to both `_merge_flow_values` and `_merge_legacy_flow_values`, including nested functions and recursive callbacks. Each actual call must have exactly the correct existing operation budget: `budget` in free functions, `self.budget` in resolver/authority operations, and `self.authority.budget` in ExecutionState. Reject indirect aliases/unexplained references rather than treating a count as proof. The old v25 inventory had35 calls; that is historical evidence, not a target count for v31 or the composition. Recheck the join callback and full/disabled producers themselves, which can change without changing the top-level function inventory.

The primitive join callback remains `merge(name, supplied)`; it does not receive a fresh budget. Its closure owns the resolver's existing operation budget. All new guards, callback plumbing and allocations need explicit ledger entries under the same budget, including the class-frame exclusion.

## Gated preparation-to-composition sequence

### Task1 — close and freeze both lane inputs

- [ ] Root identifies the exact independently issued semantic successor source, its from-v25 diff, source-region/method inventory, accounting ledger, preservation/static proof and source-review disposition. V31 authoring is not an input.
- [ ] Rehash both frozen lane sources and every referenced proof; verify the storage proof chain and explicit remaining v30 fitness failure. Root may choose a later independently frozen storage successor, but then this storage map must be recomputed before composition.
- [ ] Recompute the semantic/common-base/storage AST and raw-source overlap map. Any new overlap, changed merge law, storage node or adapter boundary requires an amended plan before authoring. Do not infer compatibility from version names or the current v25 table.

Deliverable: a root-reviewed exact input and overlap record. No composed source exists at this gate.

### Task2 — author only the separately authorized composition

- [ ] Root separately authorizes one new immutable T-only candidate path and the exact two lane pins. Start from the semantic source; apply only the primitive and three adapter intersections above.
- [ ] Preserve the semantic constructor setup and module snapshot order, lexical tokens, cell APIs and existing call-budget keywords.
- [ ] Preserve class-aware projection at all three merge sites and restrict the new disabled shortcut to the proved frame-None context. Keep raw entries pending and all full fallback behavior.
- [ ] Produce exact diffs against **both** lane sources, with an ownership table assigning every changed span to storage, semantics or the narrowly reviewed intersection. No unrelated cleanup or source normalization.

Deliverable: candidate bytes and reviewable diffs, not an installation or a passing verdict.

### Task3 — re-establish the composition invariants statically

- [ ] Verify all47 primitive nodes against the pinned v30 source as raw source and AST; separately verify NameMeter, all attributes/slots/literals/global bindings, complete node census and no unresolved helper/name capture. If extraction is used, prove it is the actual combined-source primitive, not the retained prototype.
- [ ] Prove exact FlowValue repeated-input merge returns that same object before new carrier work/effects. Separately prove every skipped callback context satisfies the whole class-wrapper law; active frames are excluded.
- [ ] Prove retained Entry.no_work remains False in the disabled path; raw projections remain pending; no positive certificate is minted; enabled/recursive/retained transfers keep their full existing boundaries.
- [ ] Re-establish all-parent eager set-union order, exact input/snapshot order, original authority/binding joins, ordered conditional strong/weak cell writes and class-projection placement. Mere equal root sizes or shared IDs are not substitute proofs.
- [ ] Re-establish local publication staging and failure behavior, distinguishing pre-existing snapshot/key-cache publication from the new staged result. No partial result install, budget refund, reseeding stale authority or changed exception successor is permitted.
- [ ] Produce the complete caller-budget closure and source-level new-work ledger; verify the five caps and original consume implementation remain exact.
- [ ] Check semantic-lane preservation outside the enumerated storage/intersection spans; storage primitive preservation; unchanged fixed52 sources/Models/traces/labels; unchanged tests except any root-approved, separately pinned existing test revision; unchanged W/main and all protected/generated paths. Retain exact hashes and failures.

Deliverable: complete combined-source static proof and independent source review. This gate cannot convert v30's52/53 into fitness.

### Task4 — obtain evidence for the actual combined bytes

- [ ] Root reviews candidate, static proof, actual test revisions and hash-bound controllers before any payload. Controllers must read a retained candidate path/SHA, never mutable W.
- [ ] The actual combined design53 must satisfy all current approved assertions, including generator70's substantive exact-depth gate; preserve the v30 failure record. A failed floor gate does not authorize automatic dev/matrix/corpus expansion.
- [ ] Root chooses the next bounded serial dispatch only after each applicable gate: existing fixed52 semantic cases, existing matrix192/212 projections, unchanged public24/58, and existing93 primitive order/collision/retention/atomicity checks through actual combined-source extraction. Do not add cases or change expectations through this plan.
- [ ] Rehash all inputs/outputs and verify exact populations, actual runtime/exit, floor matching, failures and incomplete custody. Prior primitive558, separate lane passes and diagnostic-only results are supporting history, not combined-source acceptance.
- [ ] Ordinary inventory generation/check and required preservation checks must run on the actual final combined snapshot before readiness. Root handles generated artifacts/census separately; preserved old119 tests/prior141 rows are required behavior, not permission to rewrite expectations.
- [ ] Any remaining substantive semantic, budget, preservation or infrastructure failure is classified and retained. It is not excused as a composition artifact. Only after the actual combined source is ready may root pursue its immutable review ref/blob manifest, the required independent Tier C cold passes, and later authorized gates/publication.

Deliverable: new combined-source evidence tied to exact bytes and authorized gates. There is no acceptance, composition, install or runtime authorization in the present preparation.
