# Task 1 bounded post-review correction report

Status: **DONE** — the single permitted post-r001 correction is implemented,
verified, and edit-stable for the parent's r002 freeze and scoped re-review.

The parent subsequently froze that stable result as r002 commit
`5e56e4454f7b8ccb360d3e36245abc33318349bb`, with manifest SHA-256
`6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5`.
This is a local review identity, not publication authority.

## Review disposition and correction scope

Both independent r001 Tier C reports were read completely before any correction
work:

- `packets/r001/reviews/a/review.md`: SOUND design, two Important findings,
  REQUIRED CORRECTIONS.
- `packets/r001/reviews/b/review.md`: SOUND design, two Important findings,
  REQUIRED CORRECTIONS.

The findings were technically verified and consolidated into three obligations:

1. Review A Important 1 and Review B B02 identified the same public-boundary
   defect: `src/pontius/blueprint_artifact.py` was not covered by the exact path
   classifier even though its module name was treated as part of the family.
2. Review B B01 identified missing common typed refusal for exact source, entry,
   key, and action records whose slots are absent.
3. Review A Important 2 identified durable acceptance-map gaps: the full history
   fixture graph/action, all four artifact action labels, action-object membership,
   and nested numeric families were not independently covered by registered tests.

The r001 frozen packet remains untouched. This is the only formal post-r001
correction. The earlier inherited-unittest test-shape adjustment occurred during
initial development before r001 was frozen and is not this correction.

## Finding-to-change mapping

### Exact source-family path rejection

`tools/check_stabilization_boundaries.py` now classifies both the colliding flat
path and paths below the package directory against the same exact two-path
allowlist. The final public test calls `CHECKER.check_repository` after creating
the exact flat file in a disposable snapshot. It retains every existing positive
and negative codec/driver control: the accepted package, undeclared package and
driver descendants, forbidden codec and driver imports, legacy-to-codec import,
the exact driver origin, and its three permitted internal edges.

No graph rule, scanner, analyzer, capability, driver, or other origin was
changed.

### Typed missing-slot refusal

`src/pontius/blueprint_artifact/codec.py` adds one narrow exact-record slot
reader. It is reached only after the existing exact-type checks and translates
only `AttributeError` from a required slot access into a path-specific
`BlueprintArtifactError`. Source, entry, key, and action accesses use it.

The correction does not traverse foreign objects, catch `BaseException`, catch
resource errors, or wrap the entire admission pipeline. Existing subclass hook
traps, numeric-before-formatting controls, and all populated malformed-graph
controls remain registered. The exact entry test deliberately places a valid
entry before the incomplete entry.

### Durable independent acceptance map

The seven-method codec suite remains seven grouped methods, but its tables and
helpers now durably assert:

- the complete handwritten history fixture as a separately constructed exact
  source, including every one of the 17 key fields, all four complete eight-field
  history rows, Unicode source ID, and the entry's `check` action;
- independently expected `fold`, `check`, `call`, and `raise` artifact entry
  actions;
- missing and unknown action members in addition to the retained root, entry,
  and key membership cases; and
- maximum `10**640 - 1` and rejected `10**640`/641-digit values in the key scalar,
  key vector, history-record chip, and action raise-to families through decoding
  and exact-source encoding.

For every numeric family, the accepted wire graph is compared with an
independently constructed exact graph. The accepted exact graph is encoded and
decoded for full equality, and its lazy source digest is explicitly traversed
and compared under the minimum-digit runs. The over-limit exact graph is refused
by the public encoder, and both retained over-limit wire-token forms are refused
by the public decoder.

## RED evidence against frozen r001

A retained test-only overlay was built at
`red-overlays/r001-current-tests`: all production, registration, checker, and
fixture bytes came from frozen `packets/r001/files`; only the final registered
codec and boundary test bytes came from authoring. Hash checks confirmed the
overlay codec exactly matched the frozen r001 codec and the overlay tests exactly
matched the registered correction tests. The public helper then cloned the fixed
base and overlaid that staging tree into fresh snapshots.

### All four malformed exact records

```powershell
& run-snapshot.ps1 -RunName correction-registered-red-final-r001 -Slot 311 `
  -Overlay red-overlays/r001-current-tests `
  -PythonArgs @('tests/test_blueprint_artifact.py')
```

Identity passed on CPython 3.11.15. The seven-method suite ran with four recorded
subtest errors, each demonstrating the wrong frozen-r001 exception contract:

- exact source missing `source_id` escaped `AttributeError`;
- a valid first entry followed by an exact entry missing `key` escaped
  `AttributeError`;
- an exact key missing `street` escaped `AttributeError`; and
- an exact action missing `kind` escaped `AttributeError`.

The other six grouped methods passed. In particular, the new history/action/
numeric controls are positive acceptance evidence on r001, not behavioral RED.
Receipt: `run-records/correction-registered-red-final-r001-311.json`.

An earlier registered RED is also retained at
`run-records/correction-codec-red-r001-311.json`; it stopped at the first missing
source slot and is not used to claim all four reproductions.

### Colliding flat module

```powershell
& run-snapshot.ps1 -RunName correction-registered-boundary-red-final-r001 `
  -Slot 311 -Overlay red-overlays/r001-current-tests `
  -PythonArgs @('tests/test_blueprint_artifact_boundary.py')
```

Identity passed on CPython 3.11.15. The four-method suite ran with three passing
methods and one failure because the real public gate did not raise for
`src/pontius/blueprint_artifact.py`. Receipt:
`run-records/correction-registered-boundary-red-final-r001-311.json`.

The earlier semantically equivalent real-gate RED remains at
`run-records/correction-boundary-red-r001-311.json`.

## Corrected GREEN evidence

Every payload ran only through `run-snapshot.ps1` in a fresh D-local snapshot,
with fixed base `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`, the exact approved overlay,
scrubbed child environment, absolute Git, `-B -P`, and snapshot `PYTHONPATH`.
No payload ran in the primary checkout or authoring clone.

The final registered codec bytes passed 7/7 in all four configurations:

- CPython 3.11.15 normal:
  `run-records/correction-final2-codec-floor-r001-311.json`
- CPython 3.11.15 with `-X int_max_str_digits=640`:
  `run-records/correction-final2-codec-min-floor-r001-311.json`
- exact CPython 3.14.6 normal:
  `run-records/correction-final2-codec-native-r001-314.json`
- exact CPython 3.14.6 with `-X int_max_str_digits=640`:
  `run-records/correction-final2-codec-min-native-r001-314.json`

The final checker and boundary-test bytes passed 4/4 on both runtimes:

- floor: `run-records/correction-boundary-green-floor-r001-311.json`
- exact CPython 3.14.6:
  `run-records/correction-boundary-green-native-r001-314.json`

Only the main codec test file was subsequently reformatted to retain the explicit
digest assertion and the complete r001 subtest RED; checker, codec source, and
boundary-test bytes did not change after those boundary GREEN receipts.

## Registration, generator, and census

No test method was added, removed, renamed, aliased, or inherited. The unchanged
writer was run in a fresh floor snapshot after the final method shape and exited
0: `run-records/correction-registration-write-final-r001-311.json`. Its two
generated files were mechanically copied into authoring. They are hash-identical
to the preceding corrected-writer output because the registered seven/four/
twelve method identities are unchanged.

Fresh final `tools/generate_test_inventory.py --check` executions both exited 0:

- `run-records/correction-final-registration-check-floor-r001-311.json`
- `run-records/correction-final-registration-check-native-r001-314.json`

The structural inventory audit remains exactly the adopted registered delta:

- all 2,828 old rows preserved;
- exactly 23 new rows: seven codec, four boundary, twelve unchanged driver;
- test files 404 to 407, stable IDs 2,828 to 2,851, introduced IDs 461 to 484;
- historical baseline unchanged; and
- capability bindings remain all zeroes.

There is no new census population from r001: the correction retains the same
seven and four registered methods and adds no subprocess/helper site. The two
focused inventory/census assertions passed 2/2 on both runtimes after the
corrected source and registration were present:

- `run-records/correction-inventory-focused-floor-r001-311.json`
- `run-records/correction-inventory-focused-native-r001-314.json`

No analyzer behavior or expectation was changed, and no blocker was removed or
capability granted.

## Coverage-discovery update

The three categories in `correction-coverage-draft.md` were confirmed; none was
excluded and implementation discovery added no new source family, schema member,
or exception category. One refinement was made explicit during test review:
`ImmutableBlueprintActionSource.digest` is a lazy property and exact dataclass
equality does not traverse it, so every accepted numeric family retains an
explicit digest evaluation under the minimum-digit configurations. The final
coverage artifact remains parent-owned and must cite the RED/GREEN receipts
above rather than treating the pre-correction draft as a verdict.

## Final scope, budgets, and hygiene

Correction content changes relative to frozen r001 are confined to four paths:

- `src/pontius/blueprint_artifact/codec.py`
- `tests/test_blueprint_artifact.py`
- `tests/test_blueprint_artifact_boundary.py`
- `tools/check_stabilization_boundaries.py`

The unchanged writer touched `tests/test-inventory.json` and
`tests/test-profiles.toml` mechanically, but their final bytes remain unchanged
from r001. The complete base-to-candidate population is still exactly the same
twelve authorized paths documented in the initial implementation report.

Final budgets:

- codec source: 290/300 lines (`__init__.py` 1, `codec.py` 289);
- combined codec/boundary tests: 300/300 lines (241 and 59);
- handwritten fixture pair: 1,699/8,192 bytes, unchanged;
- manual existing registration/policy delta: 97/100 added-plus-removed lines:
  CI 8, inventory expectation test 41, boundary checker 45, generator 3.

Fresh `git diff --check` exited 0; its only output was the repository's Windows
autocrlf warning. All six new source/test/fixture files remain UTF-8 without BOM,
use LF, and have no trailing whitespace. New Python maximum line length is 99.

No primary-checkout change, broad acceptance population, source seal, review
dispatch, commit, push, publication, operating run, dependency, analyzer repair,
or capability grant was performed by this implementation agent. The parent owns
the recorded r002 frozen identity, final coverage artifact, two scoped fresh FIX
reviews, and any broad post-CLEAN acceptance execution. A third correction is
not authorized.
