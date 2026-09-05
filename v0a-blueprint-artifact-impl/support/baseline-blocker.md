# Pre-implementation blocker: the accepted driver is outside the boundary inventory

Base: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.
No codec, test, registration or tracked documentation edits have been made. No implementation candidate was frozen. Primary master and isolated authoring HEAD remain at the base.

## Direct evidence

Fresh no-hardlink D-local snapshots of the unchanged base, CPython 3.11.15 first then 3.14.6, -B -P, scrubbed child environment, absolute PONTIUS_GIT, snapshot cwd and PYTHONPATH:

- tools/check_stabilization_boundaries.py exits 2 on both slots: `unclassified stabilization origin: tools/v0a_rehearsal_driver.py`.
- A separate read-only invocation of the unchanged checker import-policy function on that driver's unchanged source also refuses its three existing direct internal imports: pontius.immutable_blueprint, pontius.v0a.replay and pontius.v0a.trace. This is diagnostic evidence, not a public-gate PASS or execution of the driver.
- The unchanged immutable blueprint suite passes all 8 tests on each slot. A sandbox 3.14 launcher Access denied attempt is retained separately from the successful native baseline.

Receipts: run-records/baseline-boundary-311.json, baseline-boundary-native-314.json, baseline-driver-imports-311.json; immutable baseline receipts in the same directory.

## Cause and scope

ADR-0488 added and source-sealed the driver at dab424a4f49b09adb7b85bdb9bb8c44e809e9afe. Its accepted delta did not change the boundary checker. The checker classifies every tools/ Python origin through ORCHESTRATION_ORIGIN_PATHS, which omits this path, and its existing import policy forbids those three internal edges. ADR-0488 explicitly used a bounded driver/v0a verification population, not repository-wide or CI acceptance.

ADR-0490 now requires the public boundary gate as codec acceptance, but opens the checker only for the two codec origins and requires unrelated checks to remain unchanged. None of its six base pins drifted: all match. The problem is an unclosed integration requirement in the base, not drift or a codec regression. Adding only the driver's filename would reveal the additional import refusals and would not resolve the gate.

## Recommended next action, not implemented

Obtain a narrow prospective amendment for the exact already-sealed driver path and its three direct internal imports in tools/check_stabilization_boundaries.py, retaining scanning and unrelated rejection rules. Require positive public-gate coverage plus negatives for an undeclared sibling and an extra forbidden driver import. Keep driver, runtime, old tests, analyzer and all historical artifacts unchanged. Confirm this baseline gate before resuming the bounded codec round. Do not waive the gate or present existing driver acceptance as proof it passes.

The current implementation round is paused before source edits. No commit, push, source seal, operating run, new review verdict or adoption disposition has occurred.
