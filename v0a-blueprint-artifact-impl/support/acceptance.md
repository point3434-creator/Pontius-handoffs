# Implementation acceptance inventory

Binding source: ADR-0490 and adopted r002 design; base c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.
This is a planned population, not a passing result.

## Baseline and focused evidence

Unchanged test_immutable_blueprint.py: 8 tests PASS in fresh snapshots on CPython 3.11.15 then 3.14.6. Native 3.14 execution was needed because the sandbox launcher failed with Access denied before importing the source; that failed attempt is retained, not classified as a codec failure. JSON receipts are under run-records/.

Focused pre-review: both new suites and public boundary/generation checks; focused codec additionally at startup int_max_str_digits=640 on each slot. Census expectation changes need attribution and focused existing census checks. All fresh snapshots use -B -P, scrubbed environment and absolute PONTIUS_GIT; no optional/scientific execution.

## Post-CLEAN population

Execute only after two independent CLEAN implementation reviews, floor first then development slot. Union of the adopted design's suites and base CI's direct CPU hard gates, without duplicate suites:

- tests/test_blueprint_artifact.py
- tests/test_blueprint_artifact_boundary.py
- tests/test_immutable_blueprint.py
- tests/test_status_generation.py
- tests/test_evidence_errors_and_model.py
- tests/test_evidence_manifests.py
- tests/test_evidence_manifest_generation.py
- tests/test_test_orchestration_import_boundary.py
- tests/test_test_orchestration_configuration.py
- tests/test_inventory_and_profiles.py
- tests/test_stabilization_boundaries.py
- tests/test_retained_evidence_inventory.py
- tests/test_v0a_hand_replay.py
- tests/test_v0a_trace.py
- tests/test_v0a_replay.py
- tests/test_v0a_contract_faults.py
- -m pontius.status_generation --check
- tools/generate_test_inventory.py --check
- tools/check_stabilization_boundaries.py

The CI native transaction diagnostics is explicitly non-gating instrumentation, and Ruff is explicitly informational; neither is counted as a hard acceptance gate. No dependency sync/install, GPU, scientific profile or owner is in this population.

## Candidate closure

Verify only twelve approved paths differ, all six base pins match, no legacy/runtime/design/ADR bytes changed, initializer inert, source <=300 lines, new tests <=300 lines combined, exactly two fixture files <=8192 bytes combined, manual registration delta <=100 added+removed lines excluding the two generated outputs. Verify generated old IDs/rows retain meaning and all capability-binding hashes remain zero. Hash raw frozen Git blobs, whole-row sort the manifest; review identity is not the mutable authoring directory.

Publication and a source-seal decision are separate from local correctness. No adoption, operating permission or strategy improvement follows from passing codec tests.

## Executed outcome

Both r002 technical reviews CLEAN; post-CLEAN broad acceptance BLOCKED. Completed
floor then native,19commands per slot:18pass/1fail each. Failure is the existing
native handle-reuse test within the88-method inventory suite. All other commands
pass. See packets/r002/acceptance.md, acceptance-results.json and
acceptance-blocker.md. No source seal, gate waiver or further correction authorized.
