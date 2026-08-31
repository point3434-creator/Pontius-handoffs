# Gen06 v19 ordinary-generation budget diagnosis

One authorized floor-only engineering trace on exact v19 source SHA-256 3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1 plus immutable v4 tests SHA-256 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd. The baseline is r010 commit29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 in a fresh D-local disposable clone. This is engineering inspection and diagnosis, not a cold review or release approval.

Result: ordinary --check exits2 with the original analysis work cap failure. The original unchanged _AnalysisBudget.consume raises at262142 +7 =262149 against262144. Instrumentation accounts for all262149 units in the failing budget, including the throwing charge. This is a valid product budget failure, not a stale-generated-output exit or infrastructure error. All5 caps and the original consume code object remain unchanged, and every charge delegates the original method. All1761 tracked snapshot paths are unchanged after the run.

The active source is tests/test_fresh_action_width_transfer_structures.py. The active item is tests/test_fresh_action_width_transfer_structures.py::FreshActionWidthTransferStructureTests::test_complete_finite_inventories_have_no_transfer_counterpart, definition line386. This is the same top-level item as gen04 and gen05, at a different failure point. The current stack is _review_body24994 -> source ordered flow -> _historical_inventory_sha256(def127) -> deferred-generator sensitivity projection -> node.elt evaluation17342 -> _evaluate18577 -> _ObservedAuthorityMap.__setitem__13956. The last operation requests7 units while copying one layer during observation compaction. The fixture's sorted generator at line130 calls _historical_semantic_key(def106); the source contains nested tuple projections at109-112. These bodies were analyzed as ASTs, never executed as runtime oracles.

The throwing charge is not the dominant cost. Observation compaction accounts for301 units total here (282 layer/entry units,10 fresh dictionaries,9 completed replacement tuples), whereas authority transfer, ordinary-map get/copy/items/fork together consume184711 units,70.46% of the budget. The active epoch is2204, an instrumentation counter rather than a stable production identity.

## v19 merge planner: exercised and measurably useful, insufficient for corpus acceptance

N is the number of projected names. K is the number of binding names. B is the number of projected binding names visited by the planner; E is the number of cell entries in those visited bindings. B/E are exact full eligible counts for selected plans, but only visited prefixes for rejected plans. They are unknown for plans skipped by the initial cost check. The observer visits no extra binding collection and retains integers only.

| Active-budget outcome | Count | N range / sum | K range / sum | B range / sum | E range / sum | Planned-cost range / sum |
| --- | ---: | --- | --- | --- | --- | --- |
| Optimized selected | 492 | 79-82 /40200 | 11-15 /7230 | 1-2 /978 | 1-2 /978 | 32-47 /22782 |
| Estimated-cost fallback | 24 | 88-89 /2128 | 10 /240 | 10 /240 | 10 /240 | 93 /2232 |
| Initial fixed-cost fallback | 6 | 18-19 /110 | 14-16 /88 | unknown | unknown | 31-35 /194 |

No overlapping-cell, missing-cell, or incomplete-plan outcome was observed in this run. Selection alone is not a completion sentinel. Separately, all40200 direct optimized transfer-entry charges succeeded, and the492 plan-iteration charges account for978 entries. The failure occurs outside merge planning.

For an accepted plan, the charged overhead is3+2K+3B+4E; the replaced binding lookup cost isN. The accepted-plan modeled reduction is17418 units (range34-47 per plan). The table's rejected planned costs are estimates, not actual charged overhead.

Actual additional planner charges in this failing budget are:

| Operation | Units |
| --- | ---: |
| Initial decision21288 | 522 |
| Temporary plan/set allocations21291 | 1032 |
| Binding items traversal21294 | 7470 |
| Projected-name membership21295 | 7470 |
| Cell visits and overlap lookup21304 | 2388 |
| Cell existence lookup21305 | 1194 |
| Seen-cell registration21308 | 1194 |
| Candidate plan writes21312 | 1194 |
| Final plan traversal21328 | 978 |
| Projected-value lookup21330 | 978 |
| Total | 24420 |

Thus the measured40200 removed binding lookups exceed actual planner overhead24420 by15780 units for these traced merge operations. The difference between selected-plan overhead22782 and total overhead24420 is1638 units spent on the30 fallback plans. This validates that the v19 optimization was exercised and saved work; it does not show that every merge is cheaper or that whole-budget totals can be subtracted across revisions. Different revisions stop at different points; no identical-progress wall-clock or full-budget comparison was performed.

The sparse global summary through the first failing budget records1821 optimized selections (N8-82,sum99624; K0-15,sum11709; B/E0-7,sum4643 each; planned cost3-66,sum61382; modeled reduction1-67,sum38242),7722 estimated-cost fallbacks (N6-93,sum266543; K1-24,sum65123; B/E1-10,sum19545 each; planned cost12-94,sum290227), and2919 fixed-cost fallbacks (N4-58,sum82232; K1-45,sum51188; planned cost5-93,sum111133). These are aggregate integer observations across budget epochs; planned estimates are not a global actual-cost or completed-merge counter. The high fallback count is a concrete engineering limitation of the planner, not evidence of a semantic defect.

## Remaining cost attribution

All65875 authority-transfer entry charges divide into40200 optimized merge transfers,20795 ExecutionState assignment transfers,4085 explicit resolver transfers, and795 recursive transfers (sequence519,obligations132,mapping126,starred18). The20795 assignment transfers divide into9044 ExecutionState.update,8551 registered helper alias installation,2238 fallback merges,491 ordinary assignments,317 constructor fallback,135 registered seed installation,18 mutable-collection poison propagation, and1 review-body assignment. The instrumentation does not look one frame above ExecutionState.update, so it does not claim that all9044 came from a particular update caller.

The44275 ordinary-map lookups include37981 Mapping.get,4723 pop,1571 contains. Selected third-level data separates20795 binding checks from9648 object-join reads,7198 cell-join reads,1194 planner cell-existence checks,377 retained-reference validation checks,264 completed-helper cell reads, and76 reachable-authority reads.

Ordinary map copying costs28414:10980 from authority object registration,8318 from projected cell writes,6555 from cell joins,1434 from constructor local bindings,1127 from object joins. Items traversal costs25740:9648 object joins,7470 planner bindings,7198 cell joins,1424 completed-helper cell publication. The20407 ordinary forks are separate. Constructor inherited-value copies cost8964, and helper stable-import seed traversal costs8627. These are repeated authority projection and state bookkeeping costs along helper/deferred consumption. They are not a recurrence of gen01's disabled class-body prepass scans.

A bounded remedy should preserve transfer/cell meaning and historical-state isolation while reducing repeated work in these actual families. This trace does not justify deleting transfers or seeds, changing caps, weakening dormant/reached behavior, or adding broad semantic caching. It does not contain per-phase inclusive timings or deep helper-call totals; source anchors and the immediate/selected-third-level counters are the supported attribution.

Full immediate-caller totals for the failing budget, including the throwing charge:

| Caller | Units | Calls |
| --- | ---: | ---: |
| _transfer_authority:14045 | 65875 | 65875 |
| _AuthorityMap.__getitem__:13877 | 44275 | 44275 |
| _AuthorityMap.__setitem__:13885 | 28414 | 1288 |
| _AuthorityMap.items:13906 | 25740 | 1265 |
| _AuthorityMap.fork:13870 | 20407 | 20407 |
| _ExecutionState.__init__:14107 | 8964 | 8964 |
| _helper_provenance_seeds:23496 | 8627 | 8627 |
| _SourceOrderedResolver._merge_states:21295 | 7470 | 7470 |
| _ObservedAuthorityMap.get:13941 | 7056 | 7056 |
| _ObservedAuthorityMap.fork:13932 | 5193 | 5193 |
| _AuthorityState.fork:13991 | 5170 | 5170 |
| _SourceOrderedResolver._evaluate_value:18589 | 4117 | 4117 |
| _ObservedAuthorityMap.__setitem__:13965 | 3652 | 3652 |
| _AuthorityMap.__setitem__:13881 | 3157 | 3157 |
| _ObservedAuthorityMap.__setitem__:13962 | 2954 | 780 |
| _ObservedAuthorityMap.clear:13969 | 2446 | 1223 |
| _SourceOrderedResolver._merge_states:21304 | 2388 | 1194 |
| _SourceOrderedResolver._reachable_helper_authorities:17662 | 1710 | 1710 |
| _metered_ast_walk:7863 | 1694 | 1694 |
| _SourceOrderedResolver._merge_states:21308 | 1194 | 1194 |
| _SourceOrderedResolver._merge_states:21312 | 1194 | 1194 |
| _SourceOrderedResolver._merge_states:21291 | 1032 | 516 |
| _ExecutionScopeVisitor.visit:7887 | 1005 | 1005 |
| _SourceOrderedResolver._merge_states:21328 | 978 | 492 |
| _SourceOrderedResolver._merge_states:21330 | 978 | 978 |
| _AnalysisBudget.container:9071 | 667 | 172 |
| _helper_provenance_seeds:23485 | 663 | 663 |
| _AuthorityMap.clear:13914 | 616 | 616 |
| _SourceOrderedResolver._flow_statement_value:21647 | 610 | 610 |
| _AuthorityState.fork:14001 | 546 | 91 |
| _AuthorityState.identity:13986 | 527 | 527 |
| _SourceOrderedResolver._merge_states:21288 | 522 | 522 |
| _helper_body_is_deferred:9374 | 391 | 391 |
| _AuthorityState.join:14024 | 387 | 387 |
| _SourceOrderedResolver._statements:22438 | 313 | 313 |
| _ObservedAuthorityMap.__init__:13926 | 282 | 94 |
| _ObservedAuthorityMap.__setitem__:13956 | 282 | 73 |
| _AuthorityState.join:14012 | 248 | 248 |
| _SensitivePreclassifier._expression:11027 | 135 | 135 |
| _AuthorityMap.__delitem__:13892 | 114 | 114 |
| _AuthorityMap.__delitem__:13895 | 114 | 114 |
| _SensitivePreclassifier._statements:11559 | 17 | 17 |
| _ObservedAuthorityMap.__setitem__:13953 | 10 | 10 |
| _ObservedAuthorityMap.__setitem__:13958 | 9 | 9 |
| _AnalysisBudget.cardinality:9075 | 3 | 3 |
| _SourceOrderedResolver._invalidate_helper_identities:17831 | 2 | 2 |
| _review_body:24807 | 1 | 1 |

Selected third-level totals:

| Caller | Parent | Third | Units |
| --- | --- | --- | ---: |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _ExecutionState.__setitem__:14127 | 20795 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _AuthorityState.join:14014 | 9648 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _ExecutionState.update:14168 | 9044 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._registered_helper_environment:17921 | 8551 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _AuthorityState.join:14026 | 7198 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._merge_states:21319 | 2238 |
| _AuthorityMap.__getitem__:13877 | Mapping.__contains__:780 | _SourceOrderedResolver._merge_states:21305 | 1194 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._assign:20790 | 491 |
| _AuthorityMap.__getitem__:13877 | Mapping.__contains__:780 | _transfer_authority.<locals>.<genexpr>:14047 | 377 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _ExecutionState.__init__:14110 | 317 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _SourceOrderedResolver._apply_helper_call_effects.<locals>.<genexpr>:18470 | 264 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._registered_helper_environment:17924 | 135 |
| _AuthorityMap.__getitem__:13877 | Mapping.get:774 | _SourceOrderedResolver._reachable_helper_authorities:17671 | 76 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _SourceOrderedResolver._poison_mutable_collection:17012 | 18 |
| _transfer_authority:14045 | _ExecutionState.__setitem__:14121 | _review_body:24830 | 1 |

## Read-only v19-v18 semantic inspection

The exact delta extracts the old cell-write loop into _ExecutionState._write_cells14130-14134 and adds the sparse planner/merge branch21286-21331. Original name-set iteration and authority transfer order are preserved at21323-21326. The new branch delays cell writes until every projected value has transferred. _transfer_authority14034-14083 reads/writes object records and may allocate object identities, but does not read/write lexical cells or projected names. _write_cells allocates no identity; _merge_flow_values is a pure value merge. The planner accepts only cells already in the joined store and disjoint across projected names. Existing disjoint cell updates therefore commute; singleton strong writes and multi-cell weak writes keep their old per-cell logic and tuple order. Overlap/missing cells fall back to the original assignment loop. Existing cell keys mean the delayed writes do not change cell-map insertion order. Authority/binding joins before planning remain unchanged.

No concrete semantic defect was found in that bounded source inspection. This is supporting invariant reasoning, not fresh public-boundary semantic test evidence. Parent owns focused semantic validation and corpus acceptance. Rejected plans pay work before fallback, and even selected plans retain every transfer, so v19 can still exhaust the unchanged cap, as this fresh check demonstrates.

## Reproduction and immutable evidence

Controller command: D:/Pontius-tools/py311/Scripts/python.exe -I -S -B -P D:/Pontius-handoffs/v0a-i01-c-authority/tests-checks/budget-gen06-control-v2.py run budget-gen06-v4 311. The payload is generator.main(["--check"]), under actual CPython3.11.15 with -B -P. Full executable/version identity was asserted before repository imports. Cwd and PYTHONPATH point only to the fresh snapshot and its src; environment was scrubbed; temp is D-local; Git is absolute validated C:/Program Files/Git/cmd/git.exe. No primary/worktree acceptance execution, source/test/generated edit, sensitive fixture runtime, owner, GPU, install, broad wall, or second interpreter was used.

Fresh snapshot: D:/pontius-snapshots/c-authority-tests-budget-gen06-v4-df936ccc398e4cafaad19af179b03f47/snapshot.

Artifact SHA-256 values, all under D:/Pontius-handoffs/v0a-i01-c-authority:

- engineer-generator-v19.py:3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1
- engineer-generator-v19-from-v18.diff:2b4a6db7b2969f328d541d4fd6ea39779afe3f721bce31ff3f0a9c0331c91016
- c-authority-gen06-snapshot-v2.json:3803d03944cb0f18844b0ebaccb4e2032922bec4521f2b863e23d84b17e40602
- tests-checks/budget-gen06-probe-v2.py:072177a0322115c3aab9eb2c4e5623a2f827780d67c3fbb6d9760b44d7cf3c4e
- tests-checks/budget-gen06-control-v2.py:d484e10f16e7f38623399219ae84a82b5af530dbfe31462a08193e3219bcad0b
- tests-checks/snapshot-budget-gen06-v4.json:6a9a21a5eea1ed21ec63a85a4f0c3b7ee2f9c2db5d90cc511c3e5df5ffa8e2a4
- tests-checks/red-budget-gen06-v4-311.txt:f4a4090b0ccffabed401dd5bf59e952585f5b3d56b3784d2b2a0c782949a5c74
- tests-checks/red-budget-gen06-v4-311-receipt.json:4ba3c1efac6960d2450428488c540de55be4273c2aae21921f43e7d8912026cc

The unused v1 probe/control were preserved; v2 only clarified the transfer-entry-success counter label before any payload execution. The minimal observer counts caller/immediate parent per charge, selected third-level paths, sparse planner events, and the final stack only. It holds no production budget objects, frames, values, states, or AST caches after a tracked call. Original consume and caps remain authoritative. No process remains active: exec98575 completed, payload PID21060 exited2. No further check was run.
