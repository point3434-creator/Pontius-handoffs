# Gen03 ordinary-generation budget attribution

Bounded engineering diagnosis only. Exact v16 source SHA-256 3b9046fc9928bc17378ab57ab4d920bd57ae99994233bd503528670b362f8ab4 and released v4 tests SHA-256 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd were overlaid on a fresh disposable r010 clone (29c02f6fbd5eb0b7ddc9e816ef28f570b9839358). One actual CPython 3.11.15 --check trace was run. No production/test/generated/cap edits, second interpreter, broad wall, fixture-body execution, or owners.

The unchanged original _AnalysisBudget.consume raises at work_before 262144, requested 1, work_after 262145. All five caps and the original method code object remained unchanged. Counter totals equal the entire failing budget exactly. The wrapper records immediate caller and parent only, collecting the full stack only on failure. It retains no budget objects or their AST caches. The observed budget epoch is 1726; this is an instrumentation epoch, not a claim of a stable production budget identifier.

Active source: tests/test_evidence_manifests.py
Active item: tests/test_evidence_manifests.py::EvidenceManifestTests::test_each_schema_rejects_its_applicable_malformed_scalar_path_count_and_digest_fields
Definition line: 218
Phase: _review_body -> _source_ordered_review_flow -> resolver normal/exception-successor coalescing.

Full immediate-caller costs for this budget (including the throwing unit):

| Caller in tools/generate_test_inventory.py | Units | Calls |
| --- | ---: | ---: |
| _AuthorityMap.__setitem__:13885, shared-table copy | 187349 | 896 |
| _AuthorityMap.__getitem__:13877 | 23628 | 23628 |
| _AuthorityMap.items:13906 | 15318 | 1105 |
| _transfer_authority:13981 | 8362 | 8362 |
| _AuthorityMap.__setitem__:13881, direct write | 6552 | 6552 |
| _AuthorityMap.fork:13870 | 5797 | 5797 |
| _SourceOrderedResolver._evaluate_value:18520 | 4232 | 4232 |
| _metered_ast_walk:7863 | 3088 | 3088 |
| _ExecutionScopeVisitor.visit:7887 | 2482 | 2482 |
| _AuthorityMap.clear:13914 | 1017 | 1017 |
| _helper_provenance_seeds:23384 | 800 | 800 |
| _SensitivePreclassifier._expression:11027 | 630 | 630 |
| _helper_provenance_seeds:23373 | 608 | 608 |
| _helper_body_is_deferred:9374 | 540 | 540 |
| _AuthorityState.join:13948 | 498 | 498 |
| _AnalysisBudget.container:9071 | 392 | 92 |
| _SourceOrderedResolver._has_callable_authority:18047 | 231 | 231 |
| _SourceOrderedResolver._reachable_helper_authorities:17593 | 158 | 158 |
| _SourceOrderedResolver._invalidate_helper_identities:17762 | 132 | 132 |
| _AuthorityState.join:13960 | 99 | 99 |
| _AuthorityState.identity:13931 | 88 | 88 |
| _SensitivePreclassifier._statements:11559 | 87 | 87 |
| _SourceOrderedResolver._flow_statement_value:21535 | 32 | 32 |
| _SourceOrderedResolver._statements:22326 | 24 | 24 |
| _review_body:24695 | 1 | 1 |

The dominant parent edge is _evaluate:18508 -> _AuthorityMap.__setitem__:13885: 184860 copy units (70.52% of the entire budget). The same observed assignment incurs 3491 direct-write units. Other major parent edges include object join items12455, generic Mapping.get15708, MutableMapping.pop4943, merge binding items2863 plus writes2863, and authority registration copy2474. The full caller-parent distribution is retained in the log. Deferred-body checks contribute540 through _apply_helper_call_effects:18298, not the dominant cost. This lightweight trace deliberately does not classify every charge by enabled/disabled mode.

The new v16 outer-expression observed.clear at18472 incurs exactly ONE unit in this budget. The other1016 clear units are508 joins clearing observed and508 clearing results. Source inspection explains the remaining lifetime problem: the method begins with a single large cases tuple at tests/test_evidence_manifests.py223-266. It contains many tuple elements and nested manifest helper calls. Sequence evaluation at18743-18746 saves each completed element in supplied_items, while its evaluated descendants remain in the observed cache until the entire outer tuple finishes. Call/exception snapshots fork that cache, so later sibling evaluation repeatedly copies accumulated observation history. V16 bounds history across outer expressions, but not dead sibling-subtree observations within one large expression. This is the same copy/lifetime category at a different scope, not evidence for increasing the cap.

The final throwing unit is an object lookup during exception-state merge: _AuthorityMap.__getitem__:13877 <- Mapping.get <- _AuthorityState.join:13950 <- _merge_states:21211 <- _coalesce_successors.merged_raises:21433/21431 <- _coalesce_successors:21450 <- _flow_statements:21496 <- resolve:15754 <- _source_ordered_review_flow:23199 <- _review_body:24882. This final location is not the dominant accumulated cost.

Advisory direction: distinguish values still needed by active parent operands from completed subtree scratch, and avoid copying scratch into historical successor tables where no consumer needs it. Preserve selected callees, evaluated argument values, member/subscript receiver dependencies, pending return results, live object/cell authority, and historical source-point state. No specific representation change or fix is asserted by this diagnosis.

The payload used full executable/patch-version checks before repository imports, -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment, D-local temp and validated absolute Git; controller used -I -S -B -P. Before/after all1761 tracked-file hashes match. Payload exit2 is the reproduced work-budget failure, not an infrastructure error. Owned exec session30067 and payload PID35336 completed; no diagnostic remains active. Logs were streamed create-only during execution and retained unchanged.

Artifacts under tests-checks:

- snapshot-budget-gen03-v4.json SHA-256 448c384b3baebb974f51e0c9416f9d473ced2447b71718526bf36e5a08f7ce3a
- budget-gen03-probe-v1.py SHA-256 80ad0d2bc95588f50510fdfe5c7503280e4edd66e066e3bca43467bee168f64a
- budget-gen03-control-v1.py SHA-256 58d043c0de744ab50283e7e7a7cefdc80aa983961aa1c4b5c5980625eead89d6
- red-budget-gen03-v4-311.txt SHA-256 7e2066d07a7a271e5d787b4557b70516eb7c5a251859d85baa744169b4797c64
- red-budget-gen03-v4-311-receipt.json SHA-256 622cf3853869e0dadad1fab79f24113fd8950a680fde996f5594a0775f0acc9e

The root's ordinary --write03 RED and prior gen01/gen02 evidence remain distinct and unchanged. No performance pass or candidate readiness is claimed.
