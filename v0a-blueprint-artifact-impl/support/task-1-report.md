# Task 1 implementation report

Status: **BLOCKED**

## Outcome

Implementation stopped before the first edit and before a RED candidate. The
unchanged public stabilization boundary gate fails on pristine base
`c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98` because
`tools/v0a_rehearsal_driver.py` is an unclassified stabilization origin. A
separate read-only policy diagnostic proves that merely classifying the origin
would still be insufficient: the current orchestration policy rejects the
driver's direct imports of `pontius.immutable_blueprint`, `pontius.v0a.replay`,
and `pontius.v0a.trace`.

ADR-0490 authorizes only the portable-artifact family and its exact direct
imports. It does not authorize registering or changing the rehearsal driver or
widening the orchestration import policy. The task therefore stops rather than
hiding the baseline failure or transferring the exception to a different
registration design.

## Requirements and preflight completed

- Read `CLAUDE.md`, ADR-0490, and all three adopted r002 specification files.
- Read the relevant immutable blueprint, betting, v0a runtime/replay, boundary
  checker, generator, inventory expectation, and CI registration surfaces.
- Confirmed the authoring branch and base:
  `codex/blueprint-artifact-impl-r001` at
  `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`.
- Independently recomputed all six authorized existing-file Git blob IDs. They
  exactly match ADR-0490's pins:
  `c3f739f...`, `da0fb1e...`, `45c65de...`, `d655d20...`,
  `ada2c73...`, and `0585dcd...` in the specification's listed order.
- Inspected the task-local snapshot helper and observed that it binds the fixed
  base, the exact twelve approved overlay paths, scrubbed child environments,
  absolute `PONTIUS_GIT`, `-B -P`, snapshot `PYTHONPATH`, and exact interpreter
  versions.

## Retained fresh-snapshot evidence

Controller baseline preflight invoked the task-local helper, floor first:

```powershell
& D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/run-snapshot.ps1 `
  -RunName baseline-boundary -Slot 311 `
  -PythonArgs @('tools/check_stabilization_boundaries.py')
```

The identity preamble passed on CPython 3.11.15. The unchanged gate then exited
2 with:

```text
stabilization boundary check failed: unclassified stabilization origin: tools/v0a_rehearsal_driver.py
```

Receipt:
`run-records/baseline-boundary-311.json`.

The same pristine-base command was repeated on CPython 3.14.6 with fresh run
name `baseline-boundary-native`; its identity preamble passed and the unchanged
gate exited 2 with the identical violation. Receipt:
`run-records/baseline-boundary-native-314.json`.

A fresh CPython 3.11.15 snapshot then loaded the unchanged checker and applied
its public `enforce_orchestration_import_policy` directly to the unchanged
driver bytes. It exited 1 with all three independently enumerated violations:

```text
forbidden orchestration import: tools.v0a_rehearsal_driver -> pontius.immutable_blueprint
forbidden orchestration import: tools.v0a_rehearsal_driver -> pontius.v0a.replay
forbidden orchestration import: tools.v0a_rehearsal_driver -> pontius.v0a.trace
```

Receipt:
`run-records/baseline-driver-imports-311.json`.

The controller also recorded 8/8 passing unchanged immutable-blueprint tests on
both supported slots. Those checks establish that this blocker is in the
baseline registration gate, not the existing immutable source behavior; they do
not constitute codec RED or GREEN evidence.

## RED/GREEN and changed paths

- RED: not started. No test or fixture bytes were written.
- GREEN: not started. No codec or registration bytes were written.
- Authoring changed paths: none. `git status --short`, `git diff --stat`, and
  `git diff --name-only` were empty at stop.
- Report-only path added outside the authoring clone:
  `D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/task-1-report.md`.
- No payload ran in the authoring checkout. No operating run, analyzer repair,
  commit, push, reviewer dispatch, ADR edit, or STATUS edit occurred.

## Budgets and census attribution

- Codec lines used: 0 of 300.
- New test lines used: 0 of 300.
- Fixture bytes used: 0 of 8 KiB.
- Manual registration additions/removals used: 0 of 100.
- Inventory/profile census delta: none; generation was not run.
- Implementation rounds consumed: none. The stop occurred on an external
  baseline dependency before a candidate existed.

## Required controller disposition

A separately authorized prospective amendment must disposition the existing
rehearsal driver's origin classification and its three direct imports. After
that amended base is adopted and the task/base pins are refreshed as needed,
the bounded codec work can begin with handwritten fixtures and a meaningful
floor-first RED. ADR-0490 alone cannot resolve this blocker.
