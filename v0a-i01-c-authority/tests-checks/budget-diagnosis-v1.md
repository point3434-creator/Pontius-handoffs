# Ordinary corpus budget diagnosis

Read-only engineering diagnosis; no production/test/generated edits or cap changes.

Exact failed pair:
- generator cb83045209fd9fcdbc6f4c0afc320ce44235dec9956f33ec1417a92dab8a9fea
- tests 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd
- r010 base 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358

Fresh actual-3.11.15 ordinary --check reproduces the original --write budget RED.
The observing wrapper records each consume caller before invoking the unchanged
original _AnalysisBudget.consume. The original code object and 262144 cap are
asserted unchanged. All tracked snapshot source hashes remain unchanged.

Failure: work 262144 + 1 = 262145, in budget instance index 211 (212 created).
The exact phase is _process_review_rows' per-module
_definition_time_protocol_resolver for tests/test_inventory_and_profiles.py.
The class-body definition path reaches _contains_sensitive_runtime for
test_authority_transfer_issued_witnesses (test source line 31854), then fails in
_metered_ast_walk at generator line 7863. This occurs before per-test capability
review. The stale outer-loop variable naming tests/test_windows_process_memory.py
in an enclosing frame is not the actively failing source path.

Failing-budget work by caller:
- _metered_ast_walk:7863: 99461 units / calls
- _bounded_local_generator_dependencies:9325: 89769 units / calls
- _MeteredHelperBindings.visit:23233: 71547 units / calls
- _SourceOrderedResolver._evaluate_value:18509: 283 units
- _SourceOrderedResolver._statements:22315: 268 units
- _AnalysisBudget.container:9071: 195 units / 40 calls
- _SourceOrderedResolver._flow_statement_value:21524: 56 units

The remaining authority work is 566 units, all observed with authority disabled:
getitem 292; empty-table/binding forks 210; clear 32; join branches 16 + 16.
AuthorityMap.items is also called 48 times but charges zero units for empty maps.
The three AST/body scans total 260777 units. Disabled authority bookkeeping is
real, but removing only 566 units does not address the dominant full-body work.

Source path: _definition_time_protocol_resolver creates a resolver without a
helper registry. Class method definitions nevertheless enter the general function
construction branch. It computes generator dependencies, sensitivity, and
_helper_local_namespace_effects. The latter is evaluated as an argument before
_with_callable_authority can return early for disabled helper authority.

Controlled isolator:
The unchanged original r010 generator
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692 with the SAME v4
test corpus completed ordinary build and design analysis with zero budget
failures across 6685 budget instances. Its exit 2 is solely the expected
"generated governance file differs: tests\\test-inventory.json" stale-output
check. That is not a budget failure. Therefore the added test corpus alone fits
the prior generator; the replacement's helper-disabled construction work is the
distinguishing mechanism. No cb-plus-old-tests or 3.14 run was needed.

Evidence:
- red-budget-cb-v4-311-receipt.json SHA-256
  7e9ae7673e5901982ec1528f23cbf99ca6918f86822331a2146c5689d1222d22
- red-budget-cb-v4-311.txt SHA-256
  45e6b192cc4075b82d42db25ae1903ce5861c8367488833c0d095f897e0f0552
- red-budget-r010-v4-311-receipt.json SHA-256
  dbc1d06d6b68e47b7ed152441b5cd8608e3468cb5d3b59c8c33721e4fd50d672
- red-budget-r010-v4-311.txt SHA-256
  67dc2e459640a44319ac84f8737080ff08ac782d00e0f730e8ccfd39b937a776

Both runs use separate fresh D-local disposable snapshots, exact overlay hashes,
the actual floor executable, -B -P payloads, -I -S -B -P controls, scrubbed
environment, snapshot cwd/src PYTHONPATH, D-local temp and absolute validated Git.
No inspected source fixture or owner was executed. Both wrappers executed ordinary
generator --check, not a test suite or acceptance wall. No infrastructure failure
is counted as product RED in these two budget runs.

B owns any fix. Restoring a bounded helper-disabled construction path must retain
eager definition/decorator/default protocol behavior and helper-enabled ordered
method installation. This diagnosis neither approves a budget increase nor claims
a replacement fix has passed the corpus.

