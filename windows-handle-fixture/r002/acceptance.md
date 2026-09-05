# Windows handle fixture r002: final local acceptance

Date: 2026-09-05. Outcome: both independent correction reviews CLEAN;
all 38 broad acceptance commands passed; frozen-source post-run audit passed.
This is local candidate acceptance evidence, not source adoption or integration.

## Bound candidate

- Ref: `refs/heads/review/windows-handle-fixture/r002`
- Commit: `c7de23de276c50463d831f3983fede82a5400ce8`
- Tree: `014ee05a5014181bd63471247e5ee09607bb2346`
- Sole parent, preserved codec r002: `5e56e4454f7b8ccb360d3e36245abc33318349bb`
- Changed-source manifest SHA-256:
  `f5e06a5fa9d0fdf37888d29f8bfe6b395b6fc40a4c6f87258f66c95aa17421ed`

Only `tests/test_inventory_and_profiles.py` and `tests/test-inventory.json`
differ from the parent. Exactly three Windows control registrations are added;
all 2,851 previous inventory entries are unchanged. Production code, codec r002,
analyzer implementation, and profiles remain unchanged.

The user-authorized rule-8 exception controls numeric reuse at the Windows API
boundary only. The real writer, native resources, ownership/cleanup behavior,
and independent raw-native resource checks remain in the fixtures. All 14
existing reuse schedules remain. The added controls verify native-resource
preservation, sensitivity to erroneous production replay, and cleanup after
publication/teardown failures.

## Independent reviews

Both final correction reviewers reported Spec PASS, Quality PASS, CLEAN,
Critical/Important/Minor 0/0/0, Design SOUND. Each recorded its independent
inventory before reading the deferred correction coverage claim.

| Review | Report, relative to task root | SHA-256 |
| --- | --- | --- |
| A | `reviews/r002-a/review-a.md` | `ce809df1de640e493a0ac88981e5463938be7cd0a2829b935d670d30e3243700` |
| B | `reviews/r002-b/review-b.md` | `d5f3cbffaff07f8f17bee0a0bc77954372033582b71aceeb498caebf163ef15e` |

The r001 reports and rejected candidate remain unchanged. Their only required
correction was five added lines exceeding 100 columns. The one permitted
correction round wrapped those lines and updated the mechanically consequent
analyzer census string. Complete normalized AST comparison confirms no other
parsed behavior change. The unchanged analyzer independently verified the new
census value on both interpreter slots. No second correction was made.

## Full acceptance population

CPython 3.11.15 ran first, through completion, followed by CPython 3.14.6.
Each command used a unique fresh D:-local no-hardlinks snapshot of the frozen
codec parent, overlaid only with the frozen r002 packet files. Every Python
process ran with `-B -P`, a scrubbed child environment, snapshot-root cwd and
snapshot `PYTHONPATH`, and absolute `PONTIUS_GIT`. Interpreter and module-path
preflights passed for every payload. Native Windows execution was used for the
exact development launcher and real executable-hardlink checks. Command-local
Git trust settings were limited to the task clone; no global setting changed.

| # | Payload | Test methods per slot | 3.11 | 3.14 |
| --- | --- | ---: | --- | --- |
| 1 | `tests/test_blueprint_artifact.py` | 7 | PASS | PASS |
| 2 | `tests/test_blueprint_artifact_boundary.py` | 4 | PASS | PASS |
| 3 | `tests/test_immutable_blueprint.py` | 8 | PASS | PASS |
| 4 | `tests/test_status_generation.py` | 12 | PASS | PASS |
| 5 | `tests/test_evidence_errors_and_model.py` | 7 | PASS | PASS |
| 6 | `tests/test_evidence_manifests.py` | 11 | PASS | PASS |
| 7 | `tests/test_evidence_manifest_generation.py` | 61 | PASS | PASS |
| 8 | `tests/test_test_orchestration_import_boundary.py` | 3 | PASS | PASS |
| 9 | `tests/test_test_orchestration_configuration.py` | 53 | PASS | PASS |
| 10 | `tests/test_inventory_and_profiles.py` | 91 | PASS | PASS |
| 11 | `tests/test_stabilization_boundaries.py` | 52 (1 skipped) | PASS | PASS |
| 12 | `tests/test_retained_evidence_inventory.py` | 4 | PASS | PASS |
| 13 | `tests/test_v0a_hand_replay.py` | 45 | PASS | PASS |
| 14 | `tests/test_v0a_trace.py` | 53 | PASS | PASS |
| 15 | `tests/test_v0a_replay.py` | 62 | PASS | PASS |
| 16 | `tests/test_v0a_contract_faults.py` | 22 | PASS | PASS |
| 17 | `-m pontius.status_generation --check` | - | PASS | PASS |
| 18 | `tools/generate_test_inventory.py --check` | - | PASS | PASS |
| 19 | `tools/check_stabilization_boundaries.py` | - | PASS | PASS |

Per slot: 19/19 command exits zero; 495 unittest methods reported, comprising
494 passing methods and one existing platform skip; zero failures/errors.
The skip is `test_posix_write_rejects_staged_entry_substitution_before_replace`,
explicitly POSIX-only. No Windows reuse test was skipped. The full inventory
suite ran 91 tests in 143.368 seconds on 3.11 and 134.625 seconds on 3.14.
Expected refusal output from negative tests is retained, not suppressed or
misrepresented as empty stderr.

No broad command was retried and no source byte changed between slots.

## Retained evidence and post-run checks

Raw receipts are `run-records/broad-r002-NN-SLOT.json` under the task root:
NN 01 through 19; SLOT 311 or 314. Each contains both preflight and payload
argv, interpreter, snapshot, stdout, stderr, and exit code. Summaries are:

- `broad-r002-311.json`, SHA-256
  `15de49b10d74a11033f6405ac856e7232d86fd85d14cd8503c2087baa024ec66`
- `broad-r002-314.json`, SHA-256
  `43984d5f3839ad4528bf1fc2cd93491466fb16abdc8e193438f3a6244061e340`

`acceptance-evidence.sha256` binds all 38 receipts, both summaries, and the
three runner/audit scripts. Its relative paths resolve from the task root,
not from this packet directory.

The read-only `audit.py r002 --acceptance` completed with exit zero. It checked
raw Git parent/tree/ref identity, packet bytes and manifest, original inventory
preservation, authorized new IDs, correction AST equivalence, added-line
hygiene, all 38 receipt exits and flags, and post-run frozen-file equality in
every snapshot. No other tracked path was modified in the snapshots.

Earlier RED runs, development failures, baseline diagnostics, r001 reports,
and environment-limited attempts remain retained. They are not erased by this
acceptance result. Ruff was unavailable in both slots; no Ruff pass is claimed.
The configured added-line width requirement was checked directly and passed.

## Boundary and next decision

Primary checkout HEAD remains
`c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`, with no tracked modifications.
All work remains under the task-local clone and evidence directory. The local
immutable review commit/ref is not a commit on primary and is not an adoption.
No integration, primary commit, push, source-adoption/seal, operating run,
research run, or parked-lane change was performed.

The previous Windows fixture blocker is closed on the combined frozen codec
r002 plus fixture r002 candidate. The next decision is authorization to
integrate those exact reviewed bytes, not another codec or fixture fix round.
