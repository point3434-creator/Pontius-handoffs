# Task 3 independent expected cases and registration preparation

Prepared 2026-09-07 by evaluation_boundary_impl. READ-ONLY/PREPARATION standing.
This document precedes boundary-suite implementation. No payload, generator, poker,
native control, census, or acceptance command was executed to prepare it. No source,
test, fixture, registration, review, commit, or retained artifact was changed.
Only this new coordination document is written. Implementation awaits coordinator release.

## Authority, source identity, and limits

Read task-3-brief.md first, then task-3-context.md, registration-map.md,
acceptance-map-preparation.md, controller-budget-ruling-2026-09-07.md, full adopted
source-contract.md and brief.md, ADR-0508, CLAUDE.md, applicable workflow sections,
project evidence protocol, roadmap evaluation scope and architecture boundaries.
Read full census-comparison-procedure-v1.md and compare-census-v1.py; no cold Task 2
review was opened. Source inspection includes the complete runner and existing test
IDs plus the exact registration sections. Expected behavior below comes from the
adopted contract, not a passing observation of candidate behavior.

Authoring HEAD is adopted opening 34616938c708b1ca306b9d8a17b9d98e2f9e451f.
The five working raw blobs match immutable Task 2 checkpoint
674f82da9e044705fdaa6df46ad0a3d43b681ca9 by ls-tree/hash-object comparison:

| Path | Git blob |
| --- | --- |
| tools/v0a_evaluation.py | ca6cf6edb659cf1d95c75ebca0060c1005aee550 |
| tools/v0a_evaluation_contract.py | a254cdb58fe3340dde215bb729b8071e4cca75b7 |
| tests/test_v0a_evaluation_runner.py | d08c0514c22a40a0ded6852a33e6517ccdf2a56e |
| tests/test_v0a_evaluation_contract.py | f25111f0ae908152885d46a83e8079058e71c9a4 |
| tests/fixtures/evaluation/controls.json | 1cdda907ada17655d3812a4ce7af83eaa1ce5297 |

The first read-only Git rev-parse/ls-tree attempt refused dubious ownership under
the sandbox account. Repeating with a command-local exact safe.directory succeeded;
no Git configuration was modified. No execution evidence is inferred from raw reads.

Semantic B remains e043f81ecec3ac16128720b42c3312bb41a4ed67. Production cap is 1250
by the appended user ruling; 1200 in historical adopted documents is superseded.
Reported current sizes are helper 608, wrapper 622, contract tests 446, runner tests
438, fixture 20335 bytes/one literal deal. Remaining test room is 916 lines out of
1800. Boundary target is at most 850 lines, leaving integration room. Manual six-file
registration cap remains 160 added+removed lines excluding generated inventory/profile
bytes; measure actual census-literal edits before treating the budget as satisfied.
Task 3 owns the new boundary suite and six exceptions only. Route production findings
and a required larger adjustment to coordinator; do not alter helper/wrapper/fixture.

## Execution and independent observation rules for later release

Every later named finite run uses run-source-snapshot-v2.ps1, a fresh short unique
D-local exact-candidate snapshot, actual 3.11.15 first then 3.14.6, -B -P, snapshot cwd
and src, scrubbed environment, absolute verified native Git, and retained receipts.
No authoring execution, wildcard discovery, baseline analyzer rerun, or old owner run.
Retain all roots, faults, captures, command failures, and original source variants.
Destructive source-negative fixtures must be separate disposable snapshot copies;
preserve pre-fault bytes in a retained sibling, never modify the parent run snapshot.

Boundary controls add zero poker session starts. Native workers are finite Python
processes writing a marker/partial bytes and then exiting or awaiting cleanup. They
cannot emit a synthetic successful session report. Do not replace run_trial with a
successful record. The runner suite's existing MatrixTests.test_one_zero_seed_twelve_public_sessions
remains the sole complete generator/public-session vector (12 starts per suite set).
Use the existing literal deal for direct trial inputs and no additional fixture deal.
If execute-level stop controls need card preparation, bind the same existing literal
at an explicitly documented planner-input seam and obtain coordinator routing for that
seam before implementation; this asserts orchestration only, not dealer correctness.

Publication-only controls may independently build six synthetic complete pair rows,
12 trial summary rows, and canonical request/plan records. Label them publication
records, never actual engine outcomes. Suggested literal net vectors are baseline
[3,5,7,11,13,17] and blueprint [1,2,3,5,8,13]: sums 56 and 32, delta 24, denominator
6; per-seat and lineup groups must match those literal values. Use no production
reducer to create the expected aggregate. Real publish, verify_completed,
read_completed, create_file, read_stable, revalidate, source.check and filesystem
operations execute. Admit the frozen source normally; no fake successful source check.
A synthetic request/plan for this seam creates no additional cards or poker trial.

File faults wrap the actual opened stream: perform real requested partial/full writes,
real flush/fsync/close where the schedule reaches them, then raise or advance the
controlled clock at the named boundary. Record whether the trigger actually fired.
Do not replace create_file with a success token, read_completed with an oracle, or
rmdir with a fabricated success. A precommit outcome requires public-consumer refusal
and independently inspected retained bytes, guard presence, and no release attempt.
Restore monkeypatches in finally; never remove a consumed test root during cleanup.

## Proposed finite boundary IDs and expected outcomes

Final stable IDs use tests/test_v0a_evaluation_boundary.py::CLASS::METHOD. The names
below are planned, not discovered or passing IDs. Subtest schedules are finite and
must be named in receipts/report. Unknown higher-order combinations remain unclaimed.

| Class.method | Controlled case and independent expected observation |
| --- | --- |
| AdmissionBoundaryTests.test_raw_source_and_extra_population_refuse_before_load | Separately change one old raw source byte, one new tool byte, add an extra src file/directory, and preserve-away a required source/helper in isolated source copies. Real admit_source refuses before helper load; no output root/native child; old raw copies retained. |
| AdmissionBoundaryTests.test_preloaded_modules_refuse_before_helper_execution | Independently preload pontius, pontius.child, and each of the three fixed aliases. No admitted loader or downstream native work runs; preserve and restore original module entries. |
| AdmissionBoundaryTests.test_interpreter_git_and_origin_refuse | Real CLI invocation without -B and without -P; relative/missing/non-native PONTIUS_GIT; wrong wrapper __file__/cwd and changed loaded-helper __file__/module identity. Admission refuses; invalid Git is never executed. Interpreter claim is actual flags/origin, not a fabricated sys.version tuple. |
| AdmissionBoundaryTests.test_child_environment_discards_poison | Supply finite GIT_CONFIG_COUNT/GIT_DIR, PYTHONPATH/PYTHONSTARTUP and PONTIUS_ decoys after module startup; real admitted Git sees scrubbed env and native non-poker child reports only exact keep/set keys. Poison does not reach children. Wrong configured Git still refuses. |
| AdmissionBoundaryTests.test_existing_root_and_file_collision_preserve_bytes | Existing root with sentinel reservation and existing target final file each refuse; byte identity and directory population survive, no retry/overwrite/native child. Include a guard-name collision as any object. |
| DriftBoundaryTests.test_saved_request_plan_and_pair_drift_before_trial | For each original request, saved request, plan, pair input: actually alter bytes or identity in retained scratch files after saving. Real run_trial refuses before intent/process; result remains unscored and no marker executes. |
| DriftBoundaryTests.test_drift_after_real_child_retains_prefix_and_stops | A real resumed non-poker worker emits known prefix and mutates the selected saved request/plan/input or source fixture. Real post-child revalidate refuses; raw prefix, intent, launch and trial result remain; all later units unstarted/no directories and aggregate null in execute-level case. |
| DriftBoundaryTests.test_final_source_and_file_revalidation_refuse | During publication, actually change a saved input/source or replace a final-file identity after close/readback. Real revalidation rejects even when marker bytes parse; guard remains and public consumer refuses. |
| DeadlineBoundaryTests.test_full_trial_budget_exact_edges | Clock values leave budget+5000ms reserve exactly, then one ns short. Exact fit reaches real non-poker process marker; one ns short launches none and records budget_insufficient. Exercise both initial admission and time lost during real prelaunch revalidation. |
| DeadlineBoundaryTests.test_total_deadline_covers_reduction | Run real reduce_trials on synthetic publication records and advance clock after actual reduction; then real publication must remain unconsumable when deadline has passed. Separate from trial-timeout existing runner control; no synthetic native success. |
| PublicationBoundaryTests.test_final_clock_equal_and_one_ns_late | Identical independent records; final commit clock exactly deadline accepts, deadline+1 refuses despite parseable complete marker. Record actual clock phases so marker-preparation time is not substituted for final check. |
| PublicationBoundaryTests.test_result_write_flush_close_and_readback_faults | Separate short real write, flush error, fsync error, real close followed by close error, and actual post-close byte corruption before readback. Each preserves actual bytes/guard, refuses consumer, releases zero times. |
| PublicationBoundaryTests.test_completion_write_flush_close_and_readback_faults | Same named schedules on completion after a verified real result. Full-byte close failure must retain a complete parseable marker and still refuse. Include creation failure with real collision separately. |
| PublicationBoundaryTests.test_completion_real_write_and_close_delayed | Write full completion bytes then advance clock; separately actually close completion stream then advance clock. Both complete their real operation and fail final verification deadline, retaining full marker and guard. |
| PublicationBoundaryTests.test_partial_marker_and_interrupt_keep_guard | Real prefix write followed by OSError, and by KeyboardInterrupt; full completion after close followed by KeyboardInterrupt. Exact actual prefix/full bytes remain; consumer refuses and release is never attempted. CLI mapping tested where the public main path can be used without synthetic engine success. |
| PublicationBoundaryTests.test_normal_publication_round_trip | Real create/write/flush/close/readback/revalidate and one actual empty-directory release. Public reader yields independently specified aggregate; final file bytes match prepared canonical records. |
| PublicationBoundaryTests.test_delayed_release_exposes_verified_commit | Invoke actual rmdir once after advancing clock beyond deadline, observe absent guard and public acceptance; prefix timestamps stay unchanged. No visibility deadline is asserted. |
| PublicationBoundaryTests.test_failed_release_keeps_commit_hidden | Inject OSError or KeyboardInterrupt before actual removal: exactly one attempted release, guard stays, real public consumer refuses. Do not retry or recreate guard. |
| PublicationBoundaryTests.test_ambiguous_release_preserves_visible_commit | Invoke actual rmdir once, then raise OSError or KeyboardInterrupt. Guard absent; public consumer accepts previously verified files despite publication exception. No retroactive invalidation. |
| PublicationBoundaryTests.test_reader_rechecks_guard_and_file_identity | Start from separate valid synthetic roots. Introduce actual guard object or file-identity drift during real reading; final reader check refuses. Preserve both identities/artifacts; no mutable shared valid root. |
| PublicationBoundaryTests.test_missing_final_deadline_check_breaks_independent_oracle | New isolated mutant of the production publish function omits final deadline require only. Delayed real completion now releases and becomes consumable; unchanged independent requirement that late precommit publication is unconsumable must raise AssertionError. Retain mutant bytes/outcome. This is test sensitivity, not an accepted publication. |
| RegistrationBoundaryTests.test_exact_loader_and_import_controls | Accepted raw tools pass new policy; new raw-string mutants add forbidden import/dynamic route, change alias/path/captured-byte exec source, add second exec, or access host.Source/Table/Session. Policy raises; old host pin and seeded restrictions remain unchanged. No mutated source is executed. |

Independent evidence must include process marker/PID observation rather than only a
Popen call counter, actual raw contents rather than injector flags, and real public
consumer outcome rather than publication return/exception alone. Existing runner
unknown-launch, cleanup-failure, assignment/overflow/timeout/interrupt/descendant
controls remain the native ownership integration evidence; do not duplicate them
with fabricated cleanup booleans. Compound cases claim only their named schedules.

## Exact six-path registration approach

Before FIRST edit, copy each exact raw B Git blob to its authoring exception path,
then independently hash-object and compare the six pins below. Use raw byte APIs;
PowerShell text redirection is not a raw Git-blob copy. Four current checkout paths
are CRLF; the accepted B blob is the edit baseline, not checkout normalization.
All other old bytes, especially old table-session HOST_BLOB, are untouched.

| Exception | B blob | Planned delta |
| --- | --- | --- |
| tools/check_stabilization_boundaries.py | 9cc2ae8d8e82ccc77648ade4eb79ae9c34c88a9f | Add two exact origins, one closed evaluation policy, one dispatch call. |
| tools/generate_test_inventory.py | 2ac1413b0f89fa848f1ee5df0814b58dcbfa15b8 | Add exactly three suite string literals in STABILIZATION_TEST_FILES only. |
| tests/test-inventory.json | c28445aa4b77a98cfd706672d955be4570b98a15 | Raw output of unchanged --write in authorized fresh snapshot only. |
| tests/test-profiles.toml | 4469bf813b2e97116667c206784a7bc212f6eef5 | Same mechanical generation; preserve old payload order/grants. |
| tests/test_inventory_and_profiles.py | e71a24322878361fb2feb44437d9210cff79c89e | Matching three registration literals and explained census literals only. |
| .github/workflows/ci.yml | 3d873a2f75ff1b155bf3533583eddf971eb7790a | Three explicit CPU steps after seeded boundary, before v0a trace. |

Origins are tools/v0a_evaluation.py and tools/v0a_evaluation_contract.py. Contract
imports are exactly __future__, base64, hashlib, json, math, re. Wrapper imports are
exactly __future__, argparse, ctypes, hashlib, json, os, pathlib, re, stat, subprocess,
sys, threading, time, types. Use ordinary existing import-edge extraction plus bounded
AST structural checks. Do not broaden orchestration/import/SCC/classification logic.

Bind current frozen loader in admit_source: ALIASES is exactly
('_pontius_evaluation_contract','_pontius_evaluation_dealer','_pontius_evaluation_host').
NEW is exactly ('tools/v0a_evaluation.py','tools/v0a_evaluation_contract.py'). OLD[5]
is tools/v0a_seeded_deals.py and OLD[3] tools/v0a_table_host.py. The sole raw route is
for alias,path in zip(ALIASES,(NEW[1],OLD[5],OLD[3])) with types.ModuleType(alias),
module.__file__=str(repo/path), exact sys.modules/s.modules registration and
exec(compile(s.raw[path],module.__file__,'exec'),module.__dict__). Structural guard
must bind enclosing function, fixed source indices/constants and raw-buffer expression,
not merely count an exec token. Reject alternate exec/compile/import routes and direct
host.Source/Table/Session/game-loader calls; allowed host use is Job/native ownership,
dealer use deal_for_hand, contract use schema/planner/reducer. This is a bounded
structural control only, not a general dynamic-language safety proof. Fit within
manual budget; a need for generalized analyzer repair is a separate blocked issue.

Insert suite literals boundary/contract/runner in lexical order near existing v0a
entries while preserving every old literal's relative order. Generator source uses
frozenset({...}); independent test uses a tuple. Do not rewrite surrounding forms.
CI names v0a evaluation contract suite, v0a evaluation runner suite, v0a evaluation
boundary suite, each if: ${{ !cancelled() }} and existing .venv command convention.
No fixture registration, support/probe module, new grant or approval token.

## Full census and provenance strategy

Preserve existing four B captures; do not rerun baseline analyzer. Before census
literal refresh, obtain four same-candidate captures (test and production populations,
3.11 first then 3.14) using byte-identical capture-census.py. Compare entire cross-version
documents removing only interpreter, separately per population. Record commit/tree,
raw source/input/observer hashes, actual interpreter/origins, argv/env, exit, elapsed
and output hashes. A candidate is not inferred from a prior capture.

Create source-bound line-map JSON from raw accepted/candidate Git blobs of
 tests/test_inventory_and_profiles.py: only equal logical-line matching blocks from
SequenceMatcher(autojunk=False), one-based increasing/injective ranges and both raw
SHA256 values. Inspect all unmatched hunks and enclosing constructs; repeated text
alone does not establish semantic correspondence. Never remap IDs/strings by heuristic.

First comparison uses a new empty explanation object and retains its expected nonzero
unexplained-additions diagnostic. Then a new per-occurrence explanation object keys
expanded/blockers/analyzed/helpers/decoys/universe/deny_all by candidate row index.
Bind exact row SHA256, owning new-suite raw-source SHA256, source line number/text,
construct and reason including multiplicity. Shared-helper traversal cites new initiating
callsite and complete closure path. Decoys cite literal/f-string parent/anchor/tokens
and prior_stabilization_synthetic provenance. Review complete ordered rows and Counter
multiplicities; old IDs must retain full records/order, including every old blocker.

Retain entire census test: discovery/introduced digests, full universe, expanded rows,
spec digest, all census scalars, analyzed/decoy hashes, coverage/disjointness/sorting,
historical exclusions, CuPy bounds, named refusal controls, complete blocker reason
Counter and all three ordered location lists. Change only mechanically derived literals.
Keep 3041 old inventory records and 440 old payload records byte-equivalent in their
semantics/order, both capability digests zero, sections absent and refusal checks intact.
After constant refresh freeze another identity, obtain four fresh captures, and repeat
full comparisons because literals can shift AST lines. Coordinator source audit and
independent full diff review supplement comparator; a mechanical pass is not acceptance.

Preparation issue routed to coordinator: compare-census-v1.py registered_tree assumes
ast.Tuple/List and accesses .elts, but actual generator uses frozenset({...}). The
coordinator confirmed it and will preserve v1 and prepare strict compare-census-v2.py
for the exact literal form/three additions. Await that retained v2 context before
later comparison; no production analyzer edit is needed. No v1 comparator was run.

## Acceptance criterion mapping and final handoff

| Brief criterion | Existing named evidence plus planned completion | Finite limit / falsifier |
| --- | --- | --- |
| 1 strict ordered matrix | ContractTests.test_request_* and test_literal_matrix_seats_buttons_order_cards_and_hashes; boundary saved-request/plan drift and reader identity controls. | Existing literal requests/deal only; wrong order/hash must refuse or fail literal oracle. |
| 2 unchanged recipe/opponents | Runner AdmissionTests.test_admit_exact_source_without_poker_imports and MatrixTests.test_one_zero_seed_twelve_public_sessions; raw-source/population and closed-loader controls. | Raw B closure, no new cards/opponents; added source or alternate loader must refuse. |
| 3 paired inputs/seats/reset | ContractTests.test_matrix_lineup_placement_and_deal_blocks; runner real matrix stack/input/order assertions; boundary pair drift. | Six seats, one 12-start matrix; wrong reset/button/cards must fail independent expectations. |
| 4 public authority | Runner exact argv/env/namespace/source checks plus boundary interpreter/Git/modules/registration controls. | Parent cannot import poker/select actions; poison/alternate origin fails or is excluded from child env. |
| 5 retention/no retry | Existing runner intent/unknown-launch/collision/cleanup controls; boundary post-child drift, later-unit stop and all publication fault roots. | Every consumed root retained; later launch or overwrite fails marker/raw-byte observations. |
| 6 honest reports | Contract complete/failed schema, action-scope and reducer tests including six sensitivity mutants; real matrix independently summed stacks; synthetic publication aggregate checks. | Null incomplete aggregate, literal sum 56/32/24 only at publication seam; no engine claim from synthetic rows. |
| 7 ownership/deadline/publication | Existing runner native Job/overflow/descendant/interrupt controls; all boundary clock and real writer/reader/release controls. | Exact final <= deadline, late precommit refuses, actual ambiguous release accepts iff guard absent; no OS hard wall/durability claim. |
| 8 finite/versioned acceptance | Final stable-ID/fixture/session enumeration, full two-population census comparison, source audit, two fresh Tier C CLEAN reviews, sixteen exact gates per interpreter. | One literal deal, boundary zero poker, total twelve existing matrix starts; no profitability criterion. |

This is an implementation-ready expectation map, not a coverage or source-acceptance
verdict. Final task-3-report.md must bind actual discovered IDs/schedules, raw diff/limits,
all exercised and missing controls, RED/GREEN receipts, source manifests/census comparison
outputs, review dispositions, residual counts, and exact candidate. Coordinator owns
freeze/review dispatch and sixteen-command acceptance ordering; do not self-dispatch
reviews or broad gates. A later separately reviewed source seal and exact user commit
authorization remain required; no successful source control authorizes evaluation.
