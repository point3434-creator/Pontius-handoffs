# Remaining baseline prerequisite: driver test registration

Read-only diagnosis after the controller approved the driver source-boundary amendment. This document does not amend that authorization or claim a codec result.

The untouched c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98 base fails tools/generate_test_inventory.py --check on CPython 3.11.15 in a fresh scrubbed snapshot:

`unreviewed stabilization test file: tests/test_v0a_rehearsal_driver.py::DriverTests::test_authorized_mode_is_not_an_option`

A separate read-only discovery census over all baseline and current test sources found exactly one unregistered file, tests/test_v0a_rehearsal_driver.py, containing 12 introduced methods. No registration data or analyzer function was modified for this census. Receipts: run-records/baseline-inventory-311.json and baseline-unregistered-census-311.json.

ADR-0488 explicitly left this driver suite direct-run only and left inventory files sealed. ADR-0490 permits registering exactly the two codec test files. The later controller approval concerns the driver source-boundary path and its three imports, not changing the driver's direct-run-only test disposition. Consequently driver test registration needs separate prospective authority.

Recommended scope if approved: add this exact third test path to STABILIZATION_TEST_FILES and its mirrored expectation, use the unchanged writer for derived inventory/profile rows and identities, and adjust only independently attributable census expectations. Preserve the 12 driver test methods and source bytes, every existing stable ID and historical assignment, zero capability grants and the analyzer's parked status. Registration would not authorize a driver or rehearsal invocation. Do not add a CI step for the driver or waive the generator check. Stop if the unchanged generator requires analyzer repair, capability grants or an unrelated expectation change.

No claim is made that registration alone resolves every later generator check; that remains to be verified if authorized. No implementation candidate is frozen and no correction round is consumed.
