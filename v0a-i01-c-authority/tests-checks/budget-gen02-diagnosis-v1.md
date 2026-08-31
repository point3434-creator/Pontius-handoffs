# Ordinary generation budget diagnosis, gen02

This is a bounded engineering diagnosis, not a cold review. No production, test, generated-output, or budget-cap bytes were changed. The root's original --write failure remains the ordinary-generation RED; this independent diagnostic reproduces its budget failure through the real --check entry point.

Candidate generator SHA-256: b56551af864fe13c78219dc8392dfaac8b88a0d538a4de1427229e3c0fa8874a
Released v4 test SHA-256: 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd
Frozen base: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358

The fresh disposable snapshot used exact generator and v4 test overlays on r010. CPython 3.11.15 executable, full patch version, safe-path/bytecode flags, and snapshot import identity were asserted before repository imports. The run used a scrubbed environment, snapshot cwd and src PYTHONPATH, D-local temporary directory, and validated absolute Git. All 1761 tracked paths were unchanged after execution. No source fixture bodies or owners were executed.

The wrapper records before delegating to the unchanged original _AnalysisBudget.consume. Its original code object and the 262144 limit were asserted unchanged. The failing budget was index 1525 of 1526 created: work_before 262144, requested_units 1, work_after 262145, exit 2. Counts below concern that one budget and include its throwing unit; they are not totals across the corpus.

The active source is tests/test_documentation_integrity.py, stable ID tests/test_documentation_integrity.py::DocumentationIntegrityTests::test_bootstrap_safe_work_preflight_v2_is_preregistered, definition line 2103. The phase is _review_body -> _source_ordered_review_flow -> resolver normal-flow and exception-successor coalescing. This is a later phase than gen01's module definition-time prepass.

Dominant metered callers in tools/generate_test_inventory.py:

| Caller | Units | Calls |
| --- | ---: | ---: |
| _AuthorityMap.__setitem__:13885, shared-table copy | 144120 | 578 |
| _AuthorityMap.__getitem__:13877 | 40696 | 40696 |
| _AuthorityMap.items:13906 | 26576 | 853 |
| _AuthorityMap.__setitem__:13881, direct write | 24194 | 24194 |
| _transfer_authority:13981 | 14855 | 14855 |
| _AuthorityMap.fork:13870 | 5093 | 5093 |
| _metered_ast_walk:7863 | 1893 | 1893 |
| _ExecutionScopeVisitor.visit:7887 | 1477 | 1477 |
| _SourceOrderedResolver._evaluate_value:18509 | 1283 | 1283 |
| _helper_body_is_deferred:9374 | 21 | 21 |

Of the 144120 shared-table copy units, 137497 come directly from _evaluate:18498 assigning observed[id(node)] = result. Other substantial costs are merging bindings (11544 items plus 11544 writes), joining cells (9953 items), recursive sequence authority transfer (6946), and transferring values assigned to execution states (6717). The deferred-body caller is _apply_helper_call_effects:18297 and contributes only 21 units. It is not the causal high-cost path here.

Authority-disabled bookkeeping is present but totals only 123 positive units in this failing budget: 78 lookups, 21 forks, 12 clears, and 6+6 join checks. Enabled authority work dominates.

The final throwing stack is _AuthorityMap.fork:13870 <- _AuthorityState.fork:13939 <- _ExecutionState.copy:14110 <- _fork_values:14346 <- _merge_states:21197 <- _coalesce_successors.merged_raises:21422/21420 <- _coalesce_successors:21439 <- _flow_statements:21485 <- resolve:15753 <- _source_ordered_review_flow:23188 <- _review_body:24871. The final fork is only the last unit, not the principal accumulated expense.

Source inspection explains the measured cost: _AuthorityState.fork shares the observed map (13941); _snapshot_call forks values and single-state _merge_states forks again (16070-16072, 21195-21197); every enabled _evaluate records every expression node (18498). Single-successor transitions preserve earlier observed IDs. Once a call or successor snapshot marks the map shared, the next changed observation pays for copying its entire accumulated data. AuthorityState.join clears observed/results (13966-13967), but singleton forks do not. The observed map is described as caller evaluation-stack data at 18394-18397, yet it travels through historical execution-state snapshots. This is concrete lifetime/copy overhead, not evidence that the budget cap should increase.

Engineering guidance: keep live object/cell history and branch authority intact while bounding expression scratch to the evaluations that require it. Any change must preserve nested operand lookup, call arguments, caller observation restoration, extraction, and joined captured dependencies; simply deleting observations or dropping historical authority is not justified. This diagnosis does not claim a fix or future corpus pass.

Evidence:

- snapshot-budget-gen02-v4.json SHA-256 b633bee02cbc793637c2ac6d5b2a1b59d570d02384d1fe5503dacea5a2a56d83
- budget-gen02-probe-v1.py SHA-256 41cdc8daf85e8b4a197531ee19d0ec819fa3fb24b6613d3cde873091cfc5c933
- budget-gen02-control-v1.py SHA-256 adb187b86abb35b0e770a0221cc0694f43e2b2fb167e1254ace630d7ff77ba1c
- red-budget-gen02-v4-311.txt SHA-256 98878385fda0b661169f8bdebd12c9c01109bad88905a76f63d9efa523ce1435
- red-budget-gen02-v4-311-receipt.json SHA-256 9b27303eefbe92602937579912e552626356bdfaf08b6d8ac73428a5cf2f598a

Limitations: floor-only diagnostic was explicitly sufficient for attribution; no 3.14 or broad wall was run. The prior original-r010-generator plus v4-tests isolator already completed all 6685 budgets without a budget failure; it was not repeated. Observing instrumentation adds wall-clock overhead but delegates every original work charge unchanged. A stack formatter field called function can be overwritten by a local AST function in _process_review_rows; the active path and stable ID above come from the nearest _review_body frame, not stale outer locals.
