# Task 1 portable blueprint artifact implementation report

Status: **DONE** — the bounded implementation and registration unit is complete
and edit-frozen for independent review. No operating run was performed.

## Frozen candidate identity

The parent froze the stable authoring result as local review packet r001:

- commit: `6fb7f840d31d946e6b5dcb45faf82939dafd46ec`
- tree: `6f8e17c12da42ad901c90bc764fc39958cca5854`
- manifest: `26b8fb178aecaf3dccf038ee2e108dc4ce913f7f07baff10cff5efbe11011aee`
- packet: `packets/r001`

This is a local review freeze, not a publication or decision commit. The source
was not edited after the stable signal.

## Authority and outcome

The implementation follows adopted ADR-0490 and the complete retained r002
design set. Two separately recorded controller approvals also bind this packet:

- `driver-amendment-authorization.md` permits the exact pre-existing rehearsal
  driver origin and its three existing internal imports in the public boundary
  checker, with continued scanning and real public-gate negative coverage.
- `inventory-amendment-authorization.md` permits registration of the exact
  pre-existing rehearsal-driver test file, in addition to ADR-0490's two codec
  test files, with independently attributable census updates and zero grants.

The result adds an inert `pontius.blueprint_artifact` package and only the three
public codec symbols authorized by the design:

- `BlueprintArtifactError(ValueError)`
- `decode_blueprint(raw: bytes)`
- `encode_blueprint(source)`

The codec enforces the closed artifact schema and exact graph types before any
user hook can run. It rejects malformed JSON, duplicate object names, floats,
non-finite values, a UTF-8 BOM, non-scalar Unicode, out-of-range integers, extra
or missing members, wrong container types, and exact-type violations. Integer
parsing remains symmetric at the adopted 640-digit boundary even when CPython's
minimum `int_max_str_digits` setting is active. The encoder emits deterministic
ASCII JSON with sorted keys, compact separators, one final LF, and entries
ordered by full `key.canonical_bytes`. The decoder reconstructs the retained
immutable source/key/entry/action types and returns the decoded document used by
the runtime loading path. There is no artifact-size ceiling.

Focused tests exercise handwritten literal fixtures, exact graph equality,
canonical byte oracles, action/history labels, postflop state, entry-order
normalization, empty input, malformed/corrupt inputs, integer bounds, Unicode
scalar and surrogate behavior, input larger than 1 MiB, exact-type and subclass
rejection before callbacks, temporary bytes, loaded-policy hit/miss/illegal-hit
behavior, and a complete `ReplayHost` hand checked by an independent expected
policy reader. The main suite contains seven grouped test methods; the boundary
suite contains four grouped methods. Assertions and table-driven subtests are
not reported as invented test counts.

## Changed paths

Exactly the twelve approved paths are present in the candidate.

New codec source:

- `src/pontius/blueprint_artifact/__init__.py`
- `src/pontius/blueprint_artifact/codec.py`

New tests and handwritten fixtures:

- `tests/test_blueprint_artifact.py`
- `tests/test_blueprint_artifact_boundary.py`
- `tests/fixtures/blueprint_artifact/raise_control.json`
- `tests/fixtures/blueprint_artifact/history_control.json`

Approved existing registration and policy paths:

- `.github/workflows/ci.yml`
- `tools/check_stabilization_boundaries.py`
- `tools/generate_test_inventory.py`
- `tests/test_inventory_and_profiles.py`
- `tests/test-inventory.json`
- `tests/test-profiles.toml`

No driver, driver behavioral test, immutable runtime, replay/runtime model,
analyzer logic, historical artifact, governance, ADR, or status file changed.

## TDD and focused execution evidence

All test payloads ran through
`D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/run-snapshot.ps1` in fresh
D-local snapshots at fixed base
`c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`. The helper overlaid only the
approved authoring paths, scrubbed the child environment, used absolute Git,
`-B -P`, and snapshot `PYTHONPATH`, and recorded JSON receipts under
`run-records/`. No payload ran in the primary checkout or authoring clone.

### Meaningful RED

The prerequisite boundary RED was run first on CPython 3.11.15:

```powershell
& run-snapshot.ps1 -RunName driver-red-r001 -Slot 311 `
  -PythonArgs @('tests/test_blueprint_artifact_boundary.py')
```

It ran three methods: the wrong-origin negative passed, while the public gate
reported the expected unclassified driver origin and the three forbidden
driver imports. Receipt: `run-records/driver-red-r001-311.json`.

The codec API RED then ran on the floor:

```powershell
& run-snapshot.ps1 -RunName codec-red-r001 -Slot 311 `
  -PythonArgs @('tests/test_blueprint_artifact.py')
```

It failed during import with `ModuleNotFoundError` for the absent codec API.
This establishes the missing API, not execution of the behavioral assertions.
Receipt: `run-records/codec-red-r001-311.json`.

The separate public-boundary RED contained four grouped methods. Three existing
checks passed and the codec policy check failed because the codec origin policy
was absent. Receipt: `run-records/codec-boundary-red-r001-311.json`.

### GREEN

The final seven-method codec suite passed in all four required configurations:

- CPython 3.11.15 normal: 7/7, `codec-focused-floor-r001-311.json`
- CPython 3.11.15 with `-X int_max_str_digits=640`: 7/7,
  `codec-min-digits-floor-r001-311.json`
- exact CPython 3.14.6 normal: 7/7,
  `codec-focused-native-r001-314.json`
- exact CPython 3.14.6 with `-X int_max_str_digits=640`: 7/7,
  `codec-min-digits-native-r001-314.json`

The final four-method public boundary suite passed on both runtimes after the
test-shape correction:

- floor: 4/4, `boundary-shape-fix-floor-r001-311.json`
- exact CPython 3.14.6: 4/4,
  `boundary-shape-final-native-r001-314.json`

The public negatives call `CHECKER.check_repository` on disposable source
mutations. They cover an undeclared sibling, a forbidden import from the driver,
a forbidden import from the codec, and a legacy tool origin importing the codec.
Original bytes are restored exactly in `finally`, and only a test-owned sibling
is unlinked. The standalone driver public gate also exited 0, and its strengthened
three-method public-negative suite passed on both runtimes; see
`driver-public-gate-green-r001-311.json`,
`driver-public-negatives-green-r001-311.json`, and
`driver-public-negatives-native-r001-314.json`. The first sandboxed 3.14 launch
was retained as `driver-public-negatives-green-r001-314.json` after Windows
returned `Access is denied` before import; the required exact native execution
then passed.

## Registration and generated outputs

The unchanged writer registers exactly these three current stabilization paths:

- `tests/test_blueprint_artifact.py`
- `tests/test_blueprint_artifact_boundary.py`
- `tests/test_v0a_rehearsal_driver.py`

The same list is mirrored in `tests/test_inventory_and_profiles.py`. The two
codec suites have direct CPU CI steps; the rehearsal-driver suite does not gain
a CI step. Both capability-binding digests remain the all-zero value.

The writer was run only in fresh floor snapshots and the two generated files
were copied byte-for-byte into authoring. The first final writer attempt was
retained as `registration-final-write-r001-311.json`: it correctly refused an
inherited/aliased unittest class. The single bounded correction replaced the
shared inherited test class with a module-level assertion helper while leaving
both concrete test classes as direct `unittest.TestCase` subclasses. No analyzer
or inference behavior changed. The corrected unchanged writer exited 0 in
`registration-final-write-r002-311.json`.

The final generated delta was audited as follows:

- all 2,828 prior inventory rows are byte-semantically unchanged;
- exactly 23 rows were added: seven codec, four boundary, and twelve existing
  rehearsal-driver test methods;
- discovered test files changed from 404 to 407, stable IDs from 2,828 to 2,851,
  and introduced IDs from 461 to 484;
- all 422 existing TOML payloads are unchanged;
- exactly three current payloads were added;
- every other profile setting is unchanged apart from the exact three path and
  payload registrations; and
- no scientific, process, GPU, network, or other capability binding was added.

Fresh final `tools/generate_test_inventory.py --check` executions both exited 0:

- CPython 3.11.15: `registration-stable-final-floor-r001-311.json`
- exact CPython 3.14.6: `registration-stable-final-native-r001-314.json`

## Census attribution

The registration-only driver amendment exposes one previously unregistered
helper site:

```text
tests/test_v0a_rehearsal_driver.py::DriverTests::cli (line 32)
```

Nine registered driver methods reach that one helper site. The resulting 18 new
fail-closed blocker rows are exactly:

- nine `unsupported subprocess keyword: capture_output` rows, changing that
  reason count from 46 to 55; and
- nine `dynamic helper arguments prevent exact sink derivation` rows, changing
  that reason count from 15 to 24.

The total blocker count therefore changes from 376 to 394. These rows remain
blocked; none was removed, bypassed, or granted a capability. Direct subprocess
sites remain 43; unique helper sites change from five to six; cross-file and
CuPy counts remain 27 and 30.

The final analyzed-site fingerprint is
`31879b63b1de2070ed2886cb104848b136cf5afa59c178c475d71d89fcd96e54`.
The exact nine newly analyzed rows identify the helper above. The string-decoy
count and partitions remain 588 and 17/6/34/531; its new coordinate-sensitive
fingerprint is
`e344991972f24356926fe90e6a329e3c819b9c7208a3691de5893ff8c683bb17`.
An attribution reconstruction that substituted the base
`tests/test_inventory_and_profiles.py` and removed the new tests reproduced the
base fingerprint exactly. The change is therefore confined to the three
registration lines shifting that existing file's source coordinates. The
affected exact coordinate assertions were updated by three lines (for example,
1458 to 1461); they were not weakened.

The two specifically authorized focused census methods passed with real
assertions on both runtimes:

- floor 2/2: `inventory-focused-floor-r002-311.json`
- exact CPython 3.14.6 2/2: `inventory-focused-native-r001-314.json`

The earlier diagnostic receipts remain evidence, not PASS claims:
`inventory-census-diagnostic-r001-311.json`,
`inventory-blocker-diagnostic-r001-311.json`, and
`inventory-fingerprint-attribution-r001-311.json`.

One premature floor execution of the complete 88-method inventory/profile suite
is retained as `inventory-suite-final-floor-r001-311.json`. It exposed the two
attributable expectations subsequently corrected and a separate native-hardlink
`PermissionError` in `AtomicAndGitBoundaryTests`. The latter is a sandbox and
Windows environment failure outside this codec change; no production, test, or
analyzer change was made for it. This report does not claim that complete suite
passed. Per the plan, no further broad population was run before independent
review.

## Budgets and final hygiene

- Codec source: 281/300 lines (`__init__.py` 1, `codec.py` 280).
- Combined new codec/boundary tests: 299/300 lines (225 and 74).
- Handwritten fixtures: 1,699/8,192 bytes (648 and 1,051).
- Manual existing registration/policy delta: 96/100 added-plus-removed lines:
  CI 8, inventory expectation test 41, boundary checker 44, generator 3.
  Mechanically generated bytes are excluded as specified.

Fresh read-only scope checks found exactly the twelve approved changed paths.
`git diff --check` exited 0; its only output was the repository's Windows
autocrlf warning. All six new files are UTF-8 without BOM, use LF, have no
trailing whitespace, and the Python files have a maximum line length of 99.

No source seal, implementation review, broad post-CLEAN acceptance population,
decision commit, publication commit, push, operating run, or reviewer dispatch
was performed by this task. The parent owns the two independent fresh Tier C
reviews, any authorized bounded correction, and the broad reviewed acceptance
union.
