# Task 1 FIX01 final coverage

Finding I-01 only; rejected candidate 55b1f5f75f7bcdf8061a2a02906a86769345715d,
manifest c15299d1d6cbf53e0660fcd24e91f488e228735135b97a0ce467882eee089cb6.
Issued finding SHA256 31774fe43923e0a9260dff18563e6e8976f81d7a6db391d38db0651e22d4e364.
Immutable pre-edit plan SHA256
7106cdb246768f89fae9a672ac0aa98af5bf2af9d6f3fc32db100f6e25df067c.

Invariant: a rejected event row cannot change retained observations of its prior
valid prefix. Refusal/coverage diagnostics change; net score stays null.

## Discovery before production edit

Read the complete issued finding, immutable coverage plan and systematic-debugging
skill. Verified original helper/fixture hashes before test overlay. Traced every
event_result mutation, subsequent require and final summary/attribution consumer.
The inventory was sent to the coordinator before production editing:

- failures.append and seen insertion publish a new failure before late timing checks.
- seen aliases failure objects; changing seen[identity][1].sources changes prior output.
- failed timed assignment follows its own timing check but precedes later decision checks.
- selected/legacy increments and decisions insertion precede decision timing checks.
- final attribution consumes decisions, so a rejected insertion changes attribution too.
- decision timed assignment occurs after its cross-row check.
- pending/event sequence updates already occur after all checks in this branch.
- ready publishes ready/wire_seen only after all row checks.
- action assigns pending only after row checks.
- hand_result assigns terminal after all row checks.
- session_result assigns closed/finished after all row checks.

The last four branches do not contain the demonstrated partial-row accounting
pattern and were left byte-identical. No new schema, matrix, reducer, decoder,
native or publication surface was opened by this fix.

## Correction

Reordered decision identity/timing conflict checks immediately after local decision
validation and before failure/selection updates. Moved failure timing comparison
before failure append/seen/source-label mutation. Removed the now-redundant late
decision/timing checks. Every event branch now finishes relevant row validation
before its first output-visible mutation. Valid duplicate merging, prefix
observation semantics and public interfaces remain unchanged; no rollback or
state-copy framework was introduced.

## Exercised category cases

Three new named tests / four finite version scenarios:

1. Exact reviewer v1 reproduction: first event0/action1 delivery_rejected interrupted
   timing last_valid=1, then event1/action1 with last_valid=2. Literal expected
   failure list is exactly the first entry. Conflict, refusal and null score persist.
2. Late decided row after failure-only prefix, separately v1 and v2. New row is
   locally valid, but its action1 completed timing conflicts with prior interrupted
   timing. Existing host check remains unattributed. Legacy or baseline selection/
   applied counts remain empty. This exercises selection, decisions and attribution.
3. V2 source-label alias: prefix contains one decision/failure event0/action1 and a
   matching-timing failure-only event1/action1. A repeated event1 carrying its
   decision conflicts with the earlier action1 decision. It cannot add decision
   to the second prior failure's sources.

The common oracle compares all observation metrics before/after: complete
action_failures list, applied_actions_by_kind, baseline_fallback_selections,
baseline_fallback_applied, legacy_choices, unattributed_applied_actions, both
timing counts, hand_failure_codes and session_failure_codes. It independently
requires refusal, named conflict, observation_complete=false and net_chips=null.
Literal expected first failure/source labels and empty selection/unattributed
expectations supplement the before/after comparison.

Existing matching-copy, source-label merging, null-identity, malformed-tail,
complete-version, arithmetic and six named negative-source mutation tests remain
unchanged and GREEN. No fixture edit, full deal addition, poker start or generator call.

## Fresh floor RED and GREEN

Both commands used:
C:/Users/point/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe
-NoProfile -Command "& 'D:/Pontius/tmp/v0a-evaluation-source-r001/run-source-snapshot-v2.ps1'
-RunName NAME -Slot 311 -PythonArgs @('tests/test_v0a_evaluation_contract.py','-v') FLAGS"

RED NAME task1-fix01-red-late-row; FLAGS -ExpectFailure.
Snapshot HEAD f44fcd825d02388c5b4c9b4b7729d40e569dc5a5.
24 tests, exit1, 8 assertion failures across the three new tests:
extra failure twice checked; changed source alias; v1 legacy and attribution;
v2 selections, applied selections and attribution. All pre-existing tests passed.
Snapshot helper SHA256 4197281f2cd8780a106fabd26abf55c320fd19ae4417d25fc1f1db8b8d9eacf7;
fixture SHA256 9204a8aec4a4d6558381b246385495201d64c33e67732e2d3ab21feed31c7eea.
These equal the rejected raw candidate. Only new test bytes were overlaid.

GREEN NAME task1-fix01-green; no FLAGS.
Snapshot HEAD 2fe913fe95096cf9647fb2998ba856385ed0c99b.
24 tests, exit0, 0.045s test time; all six old negative mutants remain detected.
Both runs were actual CPython3.11.15, -B -P, fresh D-local snapshots,
scrubbed environment, correct snapshot cwd/src and absolute native Git.
RED was reported to the coordinator before production editing.

Receipts under D:/Pontius/tmp/v0a-evaluation-source-r001/run-records/:
task1-fix01-red-late-row-311.json SHA256
2b76e882dacdbfc076c7c1b4df4d28413a9e89aea4f4ea1a2e7cd49562f9c6d0
task1-fix01-green-311.json SHA256
9a35a50a866e7d45fcef66cb3c59ec3825cd34b9d76279393da35a5a543f809b

## Corrected raw identities and budget

Authoring files equal GREEN snapshot bytes:
- tools/v0a_evaluation_contract.py: 608 lines / 35588 bytes,
  b62170553c20acce17bead44391904c53be43cf0cc59c0fd2fb9b47743e988ad.
- tests/test_v0a_evaluation_contract.py: 446 lines / 26456 bytes,
  6a3b8be9cd071738df37599b8f24c0de0698e5e4dd5622b527f227e0d48af45b.
- tests/fixtures/evaluation/controls.json: unchanged 634 lines / 20335 bytes,
  9204a8aec4a4d6558381b246385495201d64c33e67732e2d3ab21feed31c7eea.

Python lines <=100 columns; all assigned files LF/no BOM. Production increases
603 to608 (+5 net); tests389 to446 (+57). Remaining whole-asset allowances:
592 production lines, 1354 test lines. No scope or budget expansion.

## Limits and falsifier

This establishes the finite I-01 paths, not exhaustive schema correctness, native
ownership, operating authority or integrated acceptance. Any rejected event that
changes a prior observation metric, or any valid matching copy that loses its
intended observation, falsifies the category claim. Failure causes/deficiencies
remain separate and observed failed prefixes remain unverified. New Tier C review,
3.14/integrated acceptance and source freeze/commit remain coordinator/controller
responsibilities. The rejected candidate and issued review remain immutable.
