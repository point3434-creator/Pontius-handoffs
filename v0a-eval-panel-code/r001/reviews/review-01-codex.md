# Codex independent cold review 01: v0a-eval-panel-code/r001

Verdict: **NOT CLEAN**. Design verdict: **STRAINED**.

Reviewer: Codex, independent cold pass 01, 2026-09-09. This review did not execute
project code, tests, tools, owners, hosts, solvers or measurements. Findings below are
frozen-source proofs or explicitly labeled coverage findings, not reproduced runs.

## Identity and review contract

- Candidate C: b1fdacf157649ca92d1aee3e39b7b0471edbcd5d
- Base B: f647a7989394f084875a040b20c41891168163ed
- Candidate tree: 7a450159a8ca30cb0ac176e66f6e2a25235c457d
- Manifest SHA-256:
  376dff405c15301a489ea3fde84abc3a41c2afa4c33c6ee67423477ca9e08b8e

All locations prefixed C or B refer to those immutable Git objects, with one-based
line numbers. Every finding binds to C and the manifest above. Git independently
confirms the parent, tree, seven-path scope, all manifest rows and all 34 supplied
dependency blob pins. No sealed source path changed.

I read the handoff first, then the pinned inputs, governing frozen brief/design and
candidate production source. I wrote my invariant/related-path inventory before opening
checks/. Its SHA-256 is:
6b6c009adc94278607c0cf2e169496ec156c642518fe79f6931704697ba8589e

Authority is the adopted implementation design, steps 1-3, checklist v1 and controller
rulings. The 3.14-only ruling overrides stale 3.11 wording. Export/agreement are deferred.
The budget addendum grants an increase; its proposed exact 800/500 limits remain the
drafter's interpretation, not a second controller quotation.

## Required findings

### I-01 Important: rollback can leak the suspended worker and discard retained observations

Confidence: high, static control-flow proof. Primary location:
C:tools/v0a_eval_panel.py:180 and 202-218; related main boundary at 250-272.

Scenario: Popen succeeds with CREATE_SUSPENDED, then Job.assign refuses. The new process
has never joined the Job. The exception is recorded at 200-201, but finally asks only
job.active(), which is zero, and then waits ten seconds on the still-suspended process.
No process.kill() fallback exists. TimeoutExpired leaves finally before job.close(),
event reconciliation and the return. main retains only that later exception because
the assignment to report never completed. The suspended process remains alive; the
original containment cause and worker exit/cleanup evidence are lost.

A cleanup query, terminate, wait or close failure after a completed hand similarly
escapes before the buffered events are copied into observations. main then retains a
generic failed report without those completed hand records.

This is a regression relative to the actual reusable pattern at
B:tools/v0a_blueprint_workload.py:319-348: it tracks assignment, kills an unassigned
process, records cleanup failure and closes the Job in a nested finally. Its real
assignment-failure test is B:tests/test_blueprint_workload_session.py:198-204.
B:tools/v0a_table_host.py:383-385 confirms that assign only calls the native API; it
does not adopt or clean up the rejected process.

The same incomplete ownership boundary appears in main: mkdir occurs outside the try,
and KeyboardInterrupt during plan reading/validation or runtime-file publication skips
finish_run entirely. This violates the admitted invocation's failure/interruption record
requirement even with healthy storage.

Required correction: make post-admission retention and resource cleanup exception-safe,
track assignment, independently reap the created process, always attempt close-once
cleanup, preserve primary/secondary causes and already-received observations, and report
cleanup truthfully. Verify native assignment refusal, cleanup failure after one observation
and post-admission interruption through the real owner. Do not repair sealed host code.

### I-02 Important: nonfinite input disables limits and breaks the strict result writer

Confidence: high, static writer/consumer proof. Primary locations:
C:tools/v0a_eval_panel.py:53-56, 192, 258-272;
B:src/pontius/execution.py:139-161.

Concrete input: change the capacity fixture's resource.seconds token to 1e309, retaining
its finite integer memory_mib. Python's default JSON loader converts that standard JSON
number to positive infinity. The positive-only predicate admits it. Neither the parent's
elapsed >= seconds test nor a preflight worker's deadline can expire. Once an otherwise
successful phase returns, main includes the infinite value in report.plan. finish_run
uses json.dumps(..., allow_nan=False), so it raises before writing result.json or the
journal row. The invocation both lacks its required finite time limit and loses its record.

The same writer mismatch affects the specified nonfinite-reference failure case:
C:src/pontius/eval_bridge.py:263 retains raw response_value even when validation rejects
NaN/inf. C:tools/v0a_eval_panel.py:102, 143 and 169 pass those nonfinite diagnostics through
permissive JSON. The eventual failed report is rejected by the strict execution writer.
This second scenario is a required negative case, not a claim that the current s=4 kernel
normally produces nonfinite values.

Required correction: strictly admit finite positive resource values with deliberate exact
types and memory bounds before launch; reject nonfinite values anywhere in admitted plan
data; encode nonfinite diagnostic values losslessly in a JSON-safe form. Verify that
invalid plans and rejected nonfinite references still yield one failed retained result
and one journal row. Keep the execution owner's strict JSON rule.

### I-03 Important: the worker request write bypasses the time watchdog

Confidence: high for the blocking path; no runtime duration was measured.
Primary location: C:tools/v0a_eval_panel.py:186-195.

Scenario: an admitted plan is larger than the pipe buffer and the resumed worker stalls
before reading stdin. Plans have no size bound and unknown members are accepted, so even
a capacity plan with a large string member can reach this state. The supervisor blocks
in stdin.write/flush before entering its watchdog loop. Expiration of the declared seconds
does not execute job.terminate; the process and supervisor can remain blocked beyond the
authorized envelope.

The pre-existing workload supervisor sends its initial request on a dedicated writer
thread (B:tools/v0a_blueprint_workload.py:218-223, 289-309), leaving its owner able to enforce
the deadline during startup.

Required correction: bound plan admission and make request transport subject to the
supervisor's deadline, including startup. A bounded sender thread or the existing transport
pattern is advisory; the required outcome is timely termination and retained failure when
the real worker cannot consume a pipe-filling request. Test the trigger with real process,
pipe and Job cleanup rather than a fabricated successful supervisor result.

### I-04 Important: the accepted plan omits mandatory frozen identities

Confidence: high, specification/source comparison. Primary locations:
C:tools/v0a_eval_panel.py:42-68, 116-122;
C:tests/fixtures/eval_panel/plan-capacity.json:1-8.

The shipped capacity fixture is accepted although it has no declared replayed prefix,
complete ordered hand universe, actual ordered permutation or runtime selection. The
permutation is generated only after launch and appears only in the output. Supplying an
inconsistent extra permutation field also has no effect because it is ignored.

B:docs/architecture/v0a-eval-panel-impl-r001/design.md:10-27 requires these inputs before
launch and refusal when mandatory inputs are absent; lines 44-46 explicitly require the
actual ordered permutation in the plan. Binding code and seed alone is reproducible,
but is not the accepted explicit plan contract. The current fixture therefore demonstrates
an accepted missing-input case, not merely an untested possibility.

Required correction: represent and validate the mandatory phase inputs before launch,
including exact universe/permutation membership and order and prefix/runtime identity.
If dealer banks are intentionally inapplicable to capacity/preflight, document that narrow
phase-specific interpretation rather than silently dropping the shared input contract.
A controller amendment could change the contract; no such amendment is in these inputs.

### I-05 Important: a changed s=3 reference domain is accepted as valid

Confidence: high, frozen-kernel derivation. Primary locations:
C:tools/v0a_eval_panel.py:49;
C:src/pontius/eval_bridge.py:87-92, 200-220.

Use an otherwise valid preflight plan with stacks=3 and the royal-spade board/2c 3d hand
(the tool's own test demonstrates that board/sample shape is admitted). Replay leaves
one chip in each live stack. B:src/pontius/no_limit_betting.py:392-421 makes the legal
all-in interval [1,1]. bet_action checks only equality of the bounds and returns raise_to(1).

build_reference compares the hero actions against (CHECK, bet), where bet is that same
derived action, so it does not assert the required raise_to(2). Its terminal-magnitude
check also passes. On the royal board both forced values and production totals are zero,
the denominator remains 990 and the reference comparison accepts the tie. A different
game has passed a rule explicitly restricted to s=4.

The required fixed action and changed-domain refusal are explicit at
B:docs/architecture/v0a-eval-panel-impl-r001/design.md:68-89. For a non-tie at s=3, terminal
values can also be +/-3, outside the cited exact power-of-two scaling derivation.
This finding does not assert that a larger error bound could not be proved for that game.

Required correction: enforce the declared s=4 production/reference domain and assert the
fixed legal action set against CHECK/raise_to(2), independently of the derived bet.
Retain deeper-stack root helpers only where an explicitly labeled negative control needs
them. Verify refusal of s=3 as well as s=6, with real kernel replay.

### I-06 Important: capacity drops the boundary wire artifacts it must retain

Confidence: high, complete producer/consumer inspection. Primary locations:
C:src/pontius/eval_bridge.py:136-162;
C:tools/v0a_eval_panel.py:119-122, 259-272.

For any completed capacity invocation, the helper repeatedly creates boundary encodings,
but returns only counts, lengths and SHA-256 strings. The tool writes runtimes.json and
the final report; neither it nor the execution owner persists either boundary byte string.
Consequently the retained output cannot supply the actual measured boundary artifact for
independent decoding or byte inspection without rerunning its producer.

B:docs/architecture/v0a-eval-panel-impl-r001/design.md:34-35 and 50-54 expressly require
retaining the actual wire bytes and boundary encodings, including the one-row failure.
A digest and deterministic regeneration recipe do not fulfill that retained-byte outcome.

Required correction: retain the already-measured boundary encodings in the single run's
output directory, bind their paths/lengths/digests in its result, and verify independent
read-back/decode. This does not require a per-hand seal, codec change or additional run.

### I-07 Important: focused coverage does not exercise the declared reference sample or owner

Confidence: high; coverage defect, not an inferred arithmetic failure.
Primary locations: C:tests/test_eval_bridge.py:95-155;
C:tests/test_eval_panel_tool.py:58-101.

The only real sealed singleton comparison in test_eval_bridge uses the all-zero royal
board. The tool's preflight test also replaces the development sample with that same
royal control. The development test checks production AsAd/Td8d only. Thus the 14-case
receipt does not execute the independent reference on any of the four required nonzero
development hands. A reference-path regression that returns zero forced values and a
zero CHECK response on every hand would pass the real-reference tests; the independent
arithmetic fixtures would remain green because they supply their own values.

The ownership test replaces begin_run, supervise, finish_run, mkdir and write_text.
No candidate test calls the real supervisor. Real Job containment, worker environment,
cleanup, retained failure and inherited ownership are therefore unexercised by this receipt.
The caller budget test only supplies an already-expired deadline to run_plan; it does not
cover startup, mid-hand termination, disagreement-stop or report publication.

Required correction: exercise the declared singleton development sample on CPython 3.14.6
and the real candidate supervisor/owner in disposable snapshots, including the material
failure schedules above and disagreement stopping before another hand. Complete signed
cancellation/smallest-gap validation coverage through validate_reference, not only the
scalar lattice helper. Keep arithmetic fixtures labeled and native successful effects real.
No broad or retained measurement run is requested by this review.

## Findings that did not survive, and requirement evidence

- Root/key construction is public replay, not hand-filled state. Kernel apply_action
  explicitly terminates a completed river at B:no_limit_betting.py:528-529; _terminal's
  fallback does not add another chance node. BlueprintDecisionKey.from_state checks the
  actual legal decision and copies history/refunds, stacks and contributions.
- The ranker validates seven distinct cards. With a valid board and hero, combinations
  over 47 and 45 remaining cards give 1,081 and 990 unique hands. Production constructs
  two betting terminal states and settles each villain through the kernel; no joint game.
  Settlement uses integer division/payouts/net returns at B:no_limit_betting.py:696-750.
- Wire monotonicity is sound for the real codec: _admit sorts independent rows but does
  not compress or rewrite existing rows; encode_blueprint emits compact JSON plus LF
  (B:blueprint_artifact/codec.py:207-240, 280-285). Positive row bytes and separators
  increase every nonempty prefix. CHECK/null is three bytes longer than raise/2.
  Actual wire lengths, not canonical-source lengths, determine this probe.
- The zero-prefix convention reports largest_fitting=0 even for cap=10, where the empty
  envelope itself cannot fit. one_row_failure identifies the no-nonempty-pool case.
  This diagnostic convention is not a universal capacity theorem; no material finding
  is based on it.
- At the declared s=4 root, source tracing establishes one hero key, one initial chance
  choice and utility values in {0,+/-2,+/-4}. Distinct raw deals are constructed at weight
  1.0 before normalization. B:river.py:203-227 sums those exact units and normalizes once.
  The normalized-weight cardinality assertion is not itself proof of raw unit inputs;
  that proof comes from the construction. Terminal assertions inspect only one deal
  and omit an explicit integrality check; actual frozen kernel structure supplies those
  invariants at s=4. I-05 covers the concrete changed-domain hole.
- Villain policies explicitly assign FOLD=0/CALL=1. Both deterministic forced policies
  call expected_utilities separately; best_response is another call, and its returned
  value uses expected_utilities (B:evaluation.py:267-273). The float accumulation uses
  explicit += at lines 59-65. Under the fixed bound/domain, exact Fraction comparisons,
  integer maximizing, wrong non-tie action rejection and tie-label allowance are sound.
- run_plan stops after its first comparison failure; the parent treats its failed event
  as failure even though worker subsequently emits completed and exits zero. That event
  sequence is confusing but does not itself yield a successful parent report.
- main admits ROOT and begin_run resolves that same path; supervise launches with cwd=ROOT.
  This meets the worker-root rule for this entry path. Future Session.prepare must still
  enforce the inherited root (B:execution.py:37-44; B:tools/v0a_table_session.py:204-209).
- Read-only cache_info() does not modify a sealed source surface. The first production
  observation precedes its reference, and the reference uses the same rank keys already
  evaluated by that production hand. The private-cache dependency is real but not a seal
  violation.
- Capacity and preflight return without export/full-pool work. Deferred bridge mechanisms
  are not missing implementation findings in this first checkpoint.

Specification result: **Fail**, due to I-01 through I-07.
Engineering-quality result: **Fail**, especially lifecycle, bounded transport and retention.
Arithmetic/key/capacity mechanics are statically supported within the fixed s=4 domain;
the executed reference and orchestration evidence remains partial.

## Design verdict and engineering guidance

**STRAINED**, not WRONG SHAPE. Per-hand integer production plus a sealed singleton
reference and exact lattice validation remains a suitable narrow design. The current
orchestrator recreates an existing worker supervisor while dropping its assignment
rollback, asynchronous initial sender and cleanup protection. That duplication is already
producing multiple failures of the same ownership/resource contract.

A bounded rewrite of this small supervisor around the existing ownership pattern is
preferable to unrelated local catches. Preserve one parent/one worker/one record, make
completed observations available throughout cleanup, and use explicit failure-safe report
values. Reusing a suitably small shared helper is advisory; adding a general run framework
or changing sealed modules is not required.

The 575 production/264 test lines are independently confirmed, within the original
checkpoint allowance. Future completion pressure was disclosed, and the controller has
since granted an increase. The budget is a controller decision, not a candidate defect
or permission to compress away verification. Confirm the exact revised limits before
using them at a later freeze.

Additional nonblocking cost-report limitations: only cache-before and cache-after-production
are retained; both forced calls share one cost field; reference work counts and explicit
cold/warm repetitions are absent. The full-pool estimate clearly says production only
and reports spread, but should state cache assumptions and identify initialization/work
counts before it supports a resource decision. No retained measurement is claimed here.

## Receipt audit and limits

The pinned workflow, original controller rulings and dependency JSON match their published
hashes. The addendum SHA-256 is:
d3a15c896463449913fa0852b51f654ac7688b6c6941b57652a745244e040a6c

All five checks/ file hashes match the handoff, using its corrected LF digest for stdout:

- focused-snapshot-3.14.6.txt:
  71852648acf012cac609c144d3c669390e4bcf710e89aed0e50f86f87e7235c2
- focused-snapshot-receipt.txt:
  483826946647e3c39ea7170f9400383d0f80337dcd2c73bbfdcc680f01c2e64f
- focused-snapshot-journal-line.jsonl:
  0b5b24a45f129c767ac5ef2c92cc7af7f34c8cc29e27a10c235e6976aaa7ad86
- line-budget-and-hygiene.md:
  9e2eab5288d43d5b67150cfe1fb33706c1764ae93acf72eb37c569046c335ba2
- development-diagnostic.md:
  dc8a88ac667e107b97ae0cb90b017293e560ae797644b9bf3a386f9a93c3e4b9

The stdout says two parameterized suites passed, 44 deselected. The journal states
14 unittest cases, zero skips, exit zero, candidate source_commit and source_verified=true.
B:tests/test_pontius.py:58-76 explains that accounting; candidate source contains nine
bridge cases and five tool cases. No failed executed receipt was supplied. The development
diagnostic is expressly non-evidence and is not used to certify reference/sample cost.

The disposable snapshot and detailed result JSON are absent, so their actual source/output
byte digests cannot be freshly validated. A read-only hash of all 886 frozen source-scope
blobs gives 62497652efe41328eaff3202e484d2bbfb88a9adeec4ed63abef7bde550cf2d2.
The journal's 94c293... identity hashes actual checkout bytes, not Git blobs
(B:execution.py:89-105); checkout newline conversion is permitted. These are different
objects. I do not treat their differing hashes as proof of source drift or substitute
the Git digest for the receipt's runtime identity.

Frozen README and pyproject still say >=3.11 while .python-version is 3.14.6, contrary to
the ruling's statement that all three repository texts were already updated. The direct
3.14-only controller instruction remains authoritative. This review required no 3.11
execution and does not treat that stale base text as a candidate source-change defect.

## Inspection record and scope limits

Read-only commands completed successfully: Git status, ls-tree, diff, show, rev-parse and
cat-file using -c safe.directory=D:/Pontius; PowerShell/.NET raw-byte SHA-256 and line
checks. The manifest was reconstructed from raw Git blobs, sorted by whole ASCII row,
and joined with LF. All seven changed files have no CR, BOM, trailing whitespace or
lines above 100 columns. An initial culture-sensitive StartsWith BOM check was unsuitable;
the final check compared the first three raw bytes explicitly.

I reviewed all seven candidate blobs and actual base implementations for kernel replay,
raise bounds and settlement; card/range/ranker normalization; continuation and evaluator;
key/codec serialization; execution/status writers; Job/Source/Session admission and the
related workload supervisor and failure tests. I examined applicable frozen governance,
runtime configuration and the pytest harness. Supplied provider/clock/adapter/dealer pins
were verified for identity; deferred host-agreement semantics were not promoted to a
transitive audit or a claimed executed boundary in this checkpoint.

The live status initially showed pre-existing changes to STATUS.md and execution_journal.jsonl.
Neither was read as review evidence or modified. No source/candidate edits, fetch, installs,
test runs or live ownership operations occurred. Only my three temporary reviewer outputs
were written; the parent will publish these bytes and my single attributed ledger line.
