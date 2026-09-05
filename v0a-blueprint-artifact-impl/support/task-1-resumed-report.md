# Task 1 resumed implementation report

Status: **BLOCKED** — prerequisite boundary amendment complete; codec not started.

## Outcome

The controller-authorized prerequisite amendment in
`driver-amendment-authorization.md` is implemented and verified. The public
stabilization boundary now classifies exactly
`tools/v0a_rehearsal_driver.py`, continues scanning it, and admits exactly its
three existing direct internal imports:

- `pontius.immutable_blueprint`
- `pontius.v0a.replay`
- `pontius.v0a.trace`

The allowance is origin-specific. Undeclared siblings, additional driver
imports, and the same internal imports from other tool origins remain rejected.
The new negative tests exercise `CHECKER.check_repository` against real
temporary source mutations in disposable snapshots and restore the original
bytes, or unlink only the test-owned new sibling, in `finally` blocks.

Codec work remains blocked before its first test or source edit. A pristine-base
generator check independently fails because the pre-existing
`tests/test_v0a_rehearsal_driver.py` is absent from the governed stabilization
test registration. Neither ADR-0490 nor the prerequisite amendment authorizes
registering that additional existing test file. No workaround or wider inventory
change was made.

The earlier baseline-blocker report `task-1-report.md` remains unchanged as the
historical first disposition.

## TDD evidence

### RED — CPython 3.11.15 floor

```powershell
& D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/run-snapshot.ps1 `
  -RunName driver-red-r001 -Slot 311 `
  -PythonArgs @('tests/test_blueprint_artifact_boundary.py')
```

Interpreter/source identity passed. The three-test suite ran with one passing
negative and two expected errors:

- `unclassified stabilization origin: tools/v0a_rehearsal_driver.py`
- forbidden driver imports to `pontius.immutable_blueprint`,
  `pontius.v0a.replay`, and `pontius.v0a.trace`

Receipt: `run-records/driver-red-r001-311.json`.

### Initial GREEN and standalone public gate — CPython 3.11.15

- `driver-green-r001-311`: 3/3 tests passed.
- `driver-public-gate-green-r001-311`: the standalone unchanged public command
  `tools/check_stabilization_boundaries.py` exited 0.

### Strengthened real-public-gate negatives

The tests were tightened within the same initial TDD iteration to exercise the
public repository gate for an undeclared driver sibling, an extra driver import,
and the same privileged import from the wrong tool origin.

- `driver-public-negatives-green-r001-311`: CPython 3.11.15 identity passed;
  3/3 tests passed in 22.244 seconds.
- The first sandboxed 3.14 launch,
  `driver-public-negatives-green-r001-314`, was retained after exiting 101 before
  import with `Access is denied`.
- `driver-public-negatives-native-r001-314`: the same suite through the exact
  CPython 3.14.6 interpreter passed 3/3 in 24.152 seconds after the required
  native launch approval.

All executions used fresh D-local snapshots, the fixed base, exact approved
overlay, scrubbed child environment, absolute `PONTIUS_GIT`, `-B -P`, and
snapshot `PYTHONPATH` through the task-local helper.

## Separate blocking evidence

Controller pristine-base preflight ran floor-first:

```text
python -B -P tools/generate_test_inventory.py --check
exit 2
test inventory generation failed: unreviewed stabilization test file:
tests/test_v0a_rehearsal_driver.py::DriverTests::test_authorized_mode_is_not_an_option
```

Receipt: `run-records/baseline-inventory-311.json`.

The failure predates and is independent of the new boundary test. Registering
that existing twelve-test file requires a separate exact authorization before
the codec's two newly opened test paths can be registered or generated.

## Changed paths and budgets

- `tools/check_stabilization_boundaries.py`: 7 added, 1 removed manual line.
- `tests/test_blueprint_artifact_boundary.py`: 65 new test lines.

Budget use at this stop:

- Manual existing-registration delta: 8 of 100 added-plus-removed lines.
- Combined new-test budget: 65 of 300 lines.
- Codec source budget: 0 of 300 lines; neither approved codec source path exists.
- Fixture budget: 0 of 8 KiB; neither approved fixture exists.
- Generator/inventory/profile/CI census delta: none.

No other source, test, registration, driver, runtime, analyzer, fixture,
governance, ADR, STATUS, artifact, or historical path changed. No codec RED or
GREEN exists. No broad acceptance, implementation review, source seal, commit,
push, publication, operating run, scientific profile, or capability grant
occurred.

## Required next authority

Resume only after an exact registration-only disposition covers the one
pre-existing `tests/test_v0a_rehearsal_driver.py` population and its derived
inventory/profile effects. Do not infer that permission from ADR-0490 or the
driver boundary amendment.
