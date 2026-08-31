# Gen04 ordinary-generation budget attribution

Bounded engineering diagnostic only. Exact v17 source SHA-256 99cf67ff483244f1540f8d4959f1a84ba010a651de7ec51c228e207636815f84 and released v4 tests SHA-256 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd were overlaid on a fresh disposable r010 clone, base29c02f6fbd5eb0b7ddc9e816ef28f570b9839358. One actual CPython3.11.15 ordinary --check trace ran. No source/test/generated/cap edits, owners, sensitive fixture execution, second interpreter, or broad wall.

Original unchanged _AnalysisBudget.consume raises at262144 +1 =262145. All5 caps remain unchanged. Counter totals equal the entire failing budget. The observer counts immediate callers/parents, captures the full stack only at failure, and retains no budget objects or AST caches. Observed epoch2204 is an instrumentation epoch, not a stable production identifier.

Active source: tests/test_fresh_action_width_transfer_structures.py
Active item: tests/test_fresh_action_width_transfer_structures.py::FreshActionWidthTransferStructureTests::test_complete_finite_inventories_have_no_transfer_counterpart
Definition line:386
Reached helper at failure: _historical_inventory_sha256, definition line127 in the same source file.
Phase: _review_body -> _source_ordered_review_flow -> ordinary source-ordered helper effects -> helper-body exception-successor coalescing.

The dominant category has changed. Ordinary authority-map lookups cost87844, including62441 generic Mapping.__contains__ calls. _transfer_authority costs58803, of which54890 come directly from _ExecutionState.__setitem__. Ordinary COW copies21533, map items21003 and forks16151 also contribute. The observation specialization costs29453 total across all its operations; compaction is only232 traversal units plus8 dictionary and8 tuple units. Do not attribute this failure to observation compaction merely because gen03 had that cause.

Full immediate-caller costs for this failing budget (including the throwing unit):

| Caller | Units | Calls |
| --- | ---: | ---: |
| _AuthorityMap.__getitem__:13877 | 87844 | 87844 |
| _transfer_authority:14036 | 58803 | 58803 |
| _AuthorityMap.__setitem__:13885 | 21533 | 1017 |
| _AuthorityMap.items:13906 | 21003 | 1105 |
| _AuthorityMap.fork:13870 | 16151 | 16151 |
| _ObservedAuthorityMap.__init__:13926 | 12327 | 4109 |
| _AuthorityMap.__setitem__:13881 | 9312 | 9312 |
| _helper_provenance_seeds:23439 | 6727 | 6727 |
| _ObservedAuthorityMap.get:13941 | 5569 | 5569 |
| _ObservedAuthorityMap.fork:13932 | 4104 | 4104 |
| _SourceOrderedResolver._evaluate_value:18575 | 3296 | 3296 |
| _ObservedAuthorityMap.__setitem__:13965 | 2900 | 2900 |
| _ObservedAuthorityMap.__setitem__:13962 | 2361 | 624 |
| _ObservedAuthorityMap.clear:13969 | 1944 | 972 |
| _metered_ast_walk:7863 | 1694 | 1694 |
| _SourceOrderedResolver._reachable_helper_authorities:17648 | 1346 | 1346 |
| _ExecutionScopeVisitor.visit:7887 | 1005 | 1005 |
| _AnalysisBudget.container:9071 | 554 | 141 |
| _helper_provenance_seeds:23428 | 529 | 529 |
| _AuthorityMap.clear:13914 | 494 | 494 |
| _SourceOrderedResolver._flow_statement_value:21590 | 481 | 481 |
| _AuthorityState.identity:13986 | 422 | 422 |
| _helper_body_is_deferred:9374 | 391 | 391 |
| _AuthorityState.join:14015 | 315 | 315 |
| _SourceOrderedResolver._statements:22381 | 249 | 249 |
| _ObservedAuthorityMap.__setitem__:13956 | 232 | 64 |
| _AuthorityState.join:14003 | 207 | 207 |
| _SensitivePreclassifier._expression:11027 | 135 | 135 |
| _AuthorityMap.__delitem__:13892 | 89 | 89 |
| _AuthorityMap.__delitem__:13895 | 89 | 89 |
| _SensitivePreclassifier._statements:11559 | 17 | 17 |
| _ObservedAuthorityMap.__setitem__:13953 | 8 | 8 |
| _ObservedAuthorityMap.__setitem__:13958 | 8 | 8 |
| _AnalysisBudget.cardinality:9075 | 3 | 3 |
| _SourceOrderedResolver._invalidate_helper_identities:17817 | 2 | 2 |
| _review_body:24750 | 1 | 1 |

All observation-map operation parent costs:

| Observed-map caller | Immediate parent | Units |
| --- | --- | ---: |
| _ObservedAuthorityMap.__init__:13926 | _AuthorityState.__init__:13983 | 12327 |
| _ObservedAuthorityMap.get:13941 | _ObservedAuthorityMap.__setitem__:13948 | 4942 |
| _ObservedAuthorityMap.fork:13932 | _AuthorityState.fork:13996 | 4015 |
| _ObservedAuthorityMap.__setitem__:13965 | _SourceOrderedResolver._evaluate:18563 | 2900 |
| _ObservedAuthorityMap.__setitem__:13962 | _SourceOrderedResolver._evaluate:18563 | 2361 |
| _ObservedAuthorityMap.clear:13969 | _AuthorityState.join:14021 | 988 |
| _ObservedAuthorityMap.clear:13969 | _SourceOrderedResolver._evaluate:18527 | 956 |
| _ObservedAuthorityMap.get:13941 | _SourceOrderedResolver._evaluate:18549 | 531 |
| _ObservedAuthorityMap.__setitem__:13956 | _SourceOrderedResolver._evaluate:18563 | 232 |
| _ObservedAuthorityMap.fork:13932 | _SourceOrderedResolver._apply_helper_call_effects:18452 | 89 |
| _ObservedAuthorityMap.get:13941 | _SourceOrderedResolver._retain_native_list_call:18221 | 48 |
| _ObservedAuthorityMap.get:13941 | _SourceOrderedResolver._apply_helper_call_effects:18301 | 48 |
| _ObservedAuthorityMap.__setitem__:13953 | _SourceOrderedResolver._evaluate:18563 | 8 |
| _ObservedAuthorityMap.__setitem__:13958 | _SourceOrderedResolver._evaluate:18563 | 8 |

The observation initializer costs12327 across4109 calls. The4015 observed forks directly from _AuthorityState.fork correspond to at least12045 initializer units constructing an empty observation map that the same fork then overwrites. That is measured avoidable construction, but eliminating it alone is not evidence of a full corpus pass.

Source-level mechanism boundaries, using exact v17 line numbers: registered-helper environment construction at17905-17920 repeatedly fills module aliases, seeds, assignments and unshadowed globals into an execution state. Multi-state merge at21270-21274 clears/reinstalls every projected name. Both feed _ExecutionState.__setitem__ at14110-14115, which performs transfer and binding membership; _transfer_authority additionally checks supplied object references at14038. This trace proves the immediate assignment/transfer/membership costs, but it does NOT partition54890 assignment transfers across these third-level producer paths. No extra run was used to guess that partition. Preserve actual capture, mutation, branch alternatives and unresolved-reference refusal when evaluating improvements.

The test source at386-440 builds several prior context collections, computes semantic keys, and calls _historical_inventory_sha256(prior). That helper's source at127-134 contains nested hashing/JSON/sorted-generator expressions. These bytes were analyzed statically only; no context builders or experiment owners were executed by this diagnostic.

Final throwing stack: _AuthorityMap.__getitem__:13877 <- Mapping.get <- _AuthorityState.join:14005 <- _merge_states:21266 <- _coalesce_successors.merged_raises:21488/21486 <- _coalesce_successors:21505 <- _flow_statements:21551 <- _apply_helper_call_effects:18442 (helper _historical_inventory_sha256) <- outer expression/source flow <- _review_body:24937. The final lookup is only the last unit, not the full causal expense. The full stack and complete caller-parent distribution remain in the raw log.

The run asserted full executable/patch identity before repository imports; payload -B -P, snapshot cwd and src PYTHONPATH, scrubbed environment, D-local temp and validated absolute Git. Controller -I -S -B -P. All1761 tracked-file hashes match before/after. Payload exit2 is a valid reproduced work-budget refusal, not infrastructure failure. Owned exec97767/PID30296 completed; no diagnostic remains active. Prior reports, logs and receipts remain unchanged.

Artifacts under tests-checks:

- snapshot-budget-gen04-v4.json SHA-256 9e3f879957ce8fc5ba57724d07f6f935b126b2f2c6cb07ede5552c927277f217
- budget-gen04-probe-v1.py SHA-256 1aefd7450aa54722828222dc4b04dd9b012035e94b58d825262ee3c5e66e48ef
- budget-gen04-control-v1.py SHA-256 ece60924c1df73649a446024a0470dcf352a748b8a261ec70865be4d1e39bc91
- red-budget-gen04-v4-311.txt SHA-256 90e27396cd6f5a52745d94c3459a10634220a2314497604d05e7a842ec3d93ed
- red-budget-gen04-v4-311-receipt.json SHA-256 4b753726b3165bc5bf7b33df081329530f71a75c0f711a758ac253990b79e300

This diagnosis asserts neither a fix nor corpus readiness. Root's ordinary --write04 RED remains separate evidence.
