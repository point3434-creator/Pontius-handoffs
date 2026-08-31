# Gen05 ordinary-generation budget attribution

One bounded floor-only engineering trace, exact v18 source SHA-256 d97ea66ef606144bb635f522856af3a5cd08819368af981a0a408c84c1e6cc99 with released v4 tests SHA-256 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd, on a fresh disposable r010 clone at29c02f6fbd5eb0b7ddc9e816ef28f570b9839358. No production/test/generated/cap edits, owners, sensitive fixture-body execution, second interpreter or broad wall.

Original unchanged _AnalysisBudget.consume raises at262144 +1 =262145. Every counted unit equals the entire failing budget; all5 caps and original method code object remain unchanged. Minimal caller/immediate-parent instrumentation adds a third frame only for authority transfer through ExecutionState assignment and ordinary-map lookup through Mapping.get/contains. It retains no budget objects or AST caches. Observed epoch2204 is diagnostic bookkeeping, not a stable production identifier.

Active source: tests/test_fresh_action_width_transfer_structures.py
Active item: tests/test_fresh_action_width_transfer_structures.py::FreshActionWidthTransferStructureTests::test_complete_finite_inventories_have_no_transfer_counterpart
Definition line386. Same top-level item as gen04, but a later/deeper point: _historical_inventory_sha256(line127) -> _historical_semantic_key(line106) -> _fraction_pair(line96), through deferred generator sensitivity projection and reached helper effect analysis. The final failure is a transfer during _fraction_pair completed-state merge.

The new attribution resolves the previous uncertainty: repeated merge name reinstallation is the largest remaining assignment family, not constructor normalization. Selected transfer counts are40027 from _merge_states:21285,8561 from _ExecutionState.update:14165,8095 from registered-helper alias assignment17918,128 from registered-helper seed assignment17921,466 from ordinary _assign:20787,305 from constructor fallback14110,16 from mutable-collection poisoning, and1 from _review_body. Their sum57599 includes the throwing transfer. Constructor exact-copy work is separately8486 units.

Ordinary-map binding lookups inside _ExecutionState.__setitem__:14127 cost57598 units, one less than the assignment transfer count because the final transfer raises before lookup. Remaining major get parents are object joins9060 and cell joins6748; supplied-reference membership inside _transfer_authority accounts for only355. This distinguishes binding checks from object-reference validation.

Full immediate-caller totals (this failing budget only, including the throwing unit):

| Caller | Units | Calls |
| --- | ---: | ---: |
| _AuthorityMap.__getitem__:13877 | 78555 | 78555 |
| _transfer_authority:14045 | 62205 | 62205 |
| _AuthorityMap.__setitem__:13885 | 26334 | 1210 |
| _AuthorityMap.fork:13870 | 19323 | 19323 |
| _AuthorityMap.items:13906 | 17132 | 709 |
| _ExecutionState.__init__:14107 | 8486 | 8486 |
| _helper_provenance_seeds:23451 | 8171 | 8171 |
| _ObservedAuthorityMap.get:13941 | 6632 | 6632 |
| _ObservedAuthorityMap.fork:13932 | 4914 | 4914 |
| _AuthorityState.fork:13991 | 4899 | 4899 |
| _SourceOrderedResolver._evaluate_value:18586 | 3899 | 3899 |
| _ObservedAuthorityMap.__setitem__:13965 | 3452 | 3452 |
| _AuthorityMap.__setitem__:13881 | 3004 | 3004 |
| _ObservedAuthorityMap.__setitem__:13962 | 2799 | 740 |
| _ObservedAuthorityMap.clear:13969 | 2318 | 1159 |
| _metered_ast_walk:7863 | 1694 | 1694 |
| _SourceOrderedResolver._reachable_helper_authorities:17659 | 1616 | 1616 |
| _ExecutionScopeVisitor.visit:7887 | 1005 | 1005 |
| _AnalysisBudget.container:9071 | 635 | 163 |
| _helper_provenance_seeds:23440 | 631 | 631 |
| _AuthorityMap.clear:13914 | 585 | 585 |
| _SourceOrderedResolver._flow_statement_value:21602 | 577 | 577 |
| _AuthorityState.fork:14001 | 546 | 91 |
| _AuthorityState.identity:13986 | 497 | 497 |
| _helper_body_is_deferred:9374 | 391 | 391 |
| _AuthorityState.join:14024 | 366 | 366 |
| _SourceOrderedResolver._statements:22393 | 297 | 297 |
| _ObservedAuthorityMap.__init__:13926 | 282 | 94 |
| _ObservedAuthorityMap.__setitem__:13956 | 275 | 72 |
| _AuthorityState.join:14012 | 237 | 237 |
| _SensitivePreclassifier._expression:11027 | 135 | 135 |
| _AuthorityMap.__delitem__:13892 | 106 | 106 |
| _AuthorityMap.__delitem__:13895 | 106 | 106 |
| _SensitivePreclassifier._statements:11559 | 17 | 17 |
| _ObservedAuthorityMap.__setitem__:13953 | 9 | 9 |
| _ObservedAuthorityMap.__setitem__:13958 | 9 | 9 |
| _AnalysisBudget.cardinality:9075 | 3 | 3 |
| _SourceOrderedResolver._invalidate_helper_identities:17828 | 2 | 2 |
| _review_body:24762 | 1 | 1 |

Selected third-level attribution, exactly as recorded:

| Consume caller | Immediate parent | Selected third-level caller | Units |
| --- | --- | --- | ---: |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _ExecutionState.__setitem__:14127 | 57598 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._merge_states:21285 | 40027 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _AuthorityState.join:14014 | 9060 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _ExecutionState.update:14165 | 8561 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._registered_helper_environment:17918 | 8095 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _AuthorityState.join:14026 | 6748 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._assign:20787 | 466 |
| _AuthorityMap.__getitem__:13877 | Mapping.__contains__:780 | _transfer_authority.<locals>.<genexpr>:14047 | 355 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _ExecutionState.__init__:14110 | 305 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _SourceOrderedResolver._apply_helper_call_effects.<locals>.<genexpr>:18467 | 250 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._registered_helper_environment:17921 | 128 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _SourceOrderedResolver._reachable_helper_authorities:17668 | 72 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._poison_mutable_collection:17009 | 16 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _review_body:24785 | 1 |

Relevant exact-v18 source paths: _merge_states21282-21286 clears and reinstalls every projected name after joining authority/bindings. Each assignment enters _ExecutionState.__setitem__14121-14131, paying transfer plus binding lookup and retaining the existing strong/weak cell write behavior. The constructor exact-parent path14104-14108 has largely removed its repeated transfer cost; only305 fallback constructor transfers remain in this budget. _registered_helper_environment17918 and17921 are the measured alias and seed writes. The8561 update transfers are measured at the update method; the requested three-level trace does not partition that method's callers further.

Final throwing edge: _transfer_authority:14045 <- _ExecutionState.__setitem__:14121 <- _merge_states:21285 <- _apply_helper_call_effects:18457 for _fraction_pair. The larger stack passes through nested deferred-generator projections for _historical_semantic_key and _historical_inventory_sha256, then source flow and _review_body:24949. The complete stack and all immediate parent distributions are retained in the raw log.

These are precise overhead attributions, not authorization to skip semantic joins or change admitted behavior. Any optimization of merge reinstallation must preserve already-joined live authority, changed values, new binding alternatives, one-cell strong updates, multi-cell weak writes/deletes, and unresolved-reference refusal. No particular fix or corpus pass is asserted here.

The payload used actual CPython3.11.15 with full executable/patch identity asserted before repository imports, -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment, D-local temp and validated absolute Git. Controller used -I -S -B -P. All1761 tracked-file hashes match before/after; exit2 is a reproduced product work-budget refusal, not infrastructure failure. Exec65256/PID17136 completed; no diagnostic remains active. Logs streamed create-only and all previous versions remain immutable.

Evidence under tests-checks:

- snapshot-budget-gen05-v4.json SHA-256 af9717bc15d91ffd6d7b5c50dee819ff41c22e6700f23a0594f156112ef335d7
- budget-gen05-probe-v1.py SHA-256 c3baf610f6456b4538db9d89ef00a1eda8a696988e9760e5ee3cd437423bd450
- budget-gen05-control-v1.py SHA-256 440081fa8809538eb8290786211de9ac73dce915b0c1db88b176c5487dc4b1c1
- red-budget-gen05-v4-311.txt SHA-256 399d728b559440ca9af1bc2147a03a8b6ed80ea183ae3f7fd95f02e092789b22
- red-budget-gen05-v4-311-receipt.json SHA-256 0a9a8fc7f457e0e3f4ce128027058ef3afc2712302b1b2e2d3fc24b6bbc24a23

Limitation: these totals end at the current refusal point. Gen04 ended earlier in the same item, so their raw totals do not measure cost changes at identical progress. No additional diagnostic was run. Root's ordinary --write05 RED remains separate evidence.
