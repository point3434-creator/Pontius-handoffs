# v20 chain32 diagnostic plan v1

Status: prepared, syntax parsed only; coordinator inspection and explicit dispatch remain required. No production edits or payload execution are authorized by this note.

The floor-only release20-design-311 check on exact v20 produced 2 failures and 1 error. This diagnostic isolates its first error: the existing review_evidence(chained_source(32)) in _fix15_frozen_review_boundary_contracts. It does not invoke the encompassing 53-test campaign, any preceding contract case, chain70, matrix cases, ordinary generation, or fixture runtime bodies.

Pins:
- r010 baseline: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
- v20 generator: e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
- Original r010 tests: c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf. The later matrix overlay is intentionally absent.
- Probe: engineer-chain32-budget-probe-v1.py, SHA256 c37f214c65462565290e3f6eae1dce16d7e2c4adc7f343d81f5a82b087c3dbc9.
- Controller: engineer-chain32-budget-control-v1.py. The coordinator supplies its inspected SHA256 as the second argument, independently of the file being executed.

The controller creates a fresh D-local shared clone, detaches r010 with hooks/global Git configuration disabled, and overlays only the exact v20 generator. It pins every tracked file plus probe/controller/wrapper before import, checks all bytes afterward, and retains the snapshot and raw stdout/stderr hashes. The child uses actual D:\Pontius-tools\py311\Scripts\python.exe 3.11.15 with -B -P, PYTHONPATH set to snapshot/src, validated absolute PONTIUS_GIT, and scrubbed environment. Hash seed remains unspecified as in the failed design controller, and a hash probe is recorded. Controller invocation uses the same executable with -I -S -B -P. Child timeout is 60 seconds.

The probe uses original DesignReviewTests.setUp and _review and constructs byte-equivalent existing chain32 source. It imports no changed test module, executes no fixture body, and records the generated fixture hash. Observers delegate original _AnalysisBudget.__init__ and consume. Initializer delegation creates scalar-only epochs, so reused Python object IDs cannot merge distinct original budgets. The observer retains only integer identities, strings, numeric counters and derived JSON structures; it retains no budget, state, flow value, AST, frame or cache.

For each original budget, requested consume units and exclusive constructor/join/ordering/lookup/assignment-or-overlay/fork/other phase totals are recorded. Immediate caller, parent and third-frame origins remain available so the phase heuristic can be audited. Calls through unchanged _NameMeter.charge additionally record exact kind, parent origin and kind/phase totals. At the first original cap refusal, the full failing budget record and scalar summaries of all budgets are printed; their counted and phase units must reconcile exactly to original work_units. All five limits and original consume/initializer/name-meter code objects are checked, and methods are restored on exit. No cap, refund, alternate cache, budget retention, production code-body modification, or accounting suppression is introduced.

Expected outcome is exit 2 with the original analysis work units exceed 262144 refusal. Exit 0 is an unexpected pass to inspect; any other exception or timeout is diagnostic failure, not acceptance evidence. The controller preserves the raw child status in its receipt and itself exits nonzero for a nonzero child. The result will assess whole-representation fitness and deferred order costs; no source fix, local budget shave, or extra run follows without coordinator disposition.
