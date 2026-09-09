# Cold review 02 - Codex - v0a-eval-panel-code/r003

Defect verdict: NOT CLEAN. Design verdict: STRAINED.
Specification: Fail. Engineering quality: Fail at ownership and evidence-retention boundaries.
Three Important findings survive frozen-source verification. No Critical finding.

Reviewer: Codex, independent cold pass 02, 2026-09-09.
Candidate ref: refs/heads/review/v0a-eval-panel-code/r003.
Candidate commit: 7004285d883995de98161dafd766b18d7862cd46.
Manifest SHA-256: 12e9ceddd6e366f2a5f4e9ebd1d6de2a8327a7ddbb732cf082f0906d544eab73.
BASE/sole parent: f647a7989394f084875a040b20c41891168163ed.
Candidate tree: 850b111d83aa2755363eca1db25de454b8a0b4b4.
All finding locations below refer to these frozen Git objects, never working files.

## I-01 - Important: cleanup faults still bypass remaining releases and retained events

Confidence: high, from control flow and the frozen native Job failure contracts.
Primary location: tools/v0a_eval_panel.py:335-363, especially 338-347 and 354-358.
Related locations: tools/v0a_eval_panel.py:434-446; BASE tools/v0a_table_host.py:430-446.
Requirement: handoff ownership item 1; implementation design sections 3 and 6; checklist item 9.

Concrete failing schedule: an assigned worker has emitted completed stages and the supervisor
enters cleanup after its deadline. The first cleanup job.active() query raises HostRefusal,
which is an explicit outcome of the real QueryInformationJobObject wrapper at BASE. Control
jumps from line 338 to line 354. The fallback may kill the process, and the nested finally
still attempts job.close(), but process.wait, all thread joins, all three stream closes and
the final drain are skipped. A wait timeout or an exception closing stdin similarly skips
all subsequent releases and the final drain. The cleanup_verified flag correctly becomes
false; it does not close the leaked handles or recover queued completed observations.

An ordinary user interrupt during process.wait or thread.join is a related stronger loss
path: the cleanup handler catches Exception, not KeyboardInterrupt. After job.close() the
interrupt escapes supervise. main has not assigned supervise's report yet, so its interruption
record uses the original empty observations list and discards even previously drained stages.
This is a first interrupt during normal cleanup; a second interrupt is not required.

The assignment-refusal branch itself is now reachable and kills the unassigned suspended
process on its normal path. The remaining defect is that every cleanup operation shares one
try block. Both the docstring and deferred claim say each step is individually guarded;
the actual source does not implement that property. Copying the BASE workload pattern also
copies its single-block weakness and does not satisfy the stronger accepted correction.

Required correction: guarantee that each remaining release and final event drain is attempted
after any earlier cleanup failure. Preserve the partial report across cleanup interruption.
Keep close-once job ownership and retain the primary cause plus secondary cleanup failures.
Do not implement this correction by turning cleanup_verified true after an incomplete cleanup.

Required verification: through the real launcher and resource owner, control failure at the
first cleanup query, wait and one stream close; separately interrupt cleanup after a completed
stage. Observe process death, each pipe's closure, job-close attempt, retained stages and the
single real result/journal record independently of the injector. The existing assignment and
budget-kill cases must still pass. These schedules are not new measured OS failure-rate claims.

## I-02 - Important: declared-full accepts repeated or substituted sample identities

Confidence: high, from admission, scheduling, parent assembly and estimate control flow.
Primary location: tools/v0a_eval_panel.py:120-134.
Related locations: tools/v0a_eval_panel.py:216-228, 288-298, 390-406 and 439-444.
Requirement: implementation brief criterion 2 and fixed semantics; design section 3;
handoff admission item 2 and accepted r001 D correction.

Concrete failing plan: keep the valid preflight fixture's board, identities, permutation and
royal control, but replace development_hands with four copies of ["As", "Ad"]. Keep coverage
as declared-full and provide enough finite resources for completion. All admission predicates
pass, because the only full-sample predicate checks list lengths. The worker runs the same
known-valid singleton four times. No predicate requires Kh Kd, Td 8d or 3c 4d to be present.

The parent groups by (label, board, hand), so these four scheduled observations collapse into
one record and overwrite that record's stage costs. Its complete flag remains true. A clean
worker exit therefore produces status completed, coverage declared-full and a full-pool
estimate with sample=1. The retained production cost is from the last repeated, warmed hand,
yet the estimate says the first sampled hand is cold. The three omitted development cases
have no missing observation or failed-coverage classification.

Controls are likewise checked only for object keys and board shape. Replacing the royal
control with a valid development-board As Ad control meets the full predicate while removing
the required exact-zero control. Substituting other distinct hands also passes; detecting
only duplicate count inflation would not close the required sample-identity contract.

Required correction: bind declared-full to the specified development board, canonical required
hand membership and required royal board/hand control before launch. Validate every scheduled
hand's card count, distinctness and board compatibility at the same admission boundary.
Reject duplicate occurrences or give permitted repetitions separate occurrence identities and
reconcile them against the schedule. Emit full coverage/estimates only after required completed
membership is established; a label and list length cannot establish it.

Required verification: negative admission cases for repeated As Ad, four substituted distinct
hands, absent/replaced royal control, malformed private cards and board overlaps. A valid full
plan must retain all required distinct identities; test-subset must remain explicitly partial
and produce no full-pool estimate. If repetitions remain supported, a later partial repetition
must not inherit a prior occurrence's complete flag or stage costs.

## I-03 - Important: interrupted boundary retention discards recoverable measured bytes

Confidence: high, from mutation order and main's interruption handler.
Primary location: tools/v0a_eval_panel.py:375-387, especially 381 and 384-387.
Related locations: tools/v0a_eval_panel.py:437 and 445-453.
Requirement: implementation brief criteria 1 and 3; design sections 2 and 6;
handoff retention item 4 and the declared failure/interruption coverage category.

Concrete failing schedule: a completed capacity worker returns two boundary encodings.
retain_boundaries pops boundary_base64 from the observation before attempting either write.
The first artifact is written; the user interrupts the second write, or that write raises
OSError. main catches the failure and writes its single failed/interrupted result, but the
observation no longer contains the original base64 data and boundary_artifacts was never
assigned. The first completed artifact is left without its path/length/digest binding in the
result; the second measured encoding is unrecoverable from the result. Partial writes may
also leave an artifact file whose completeness the result cannot establish.

The worker completed the measurement before this failure. This is a loss introduced by the
parent's retention order, not missing computation caused by the budget kill, and not a request
to guarantee successful writes on a permanently failed storage device.

Required correction: preserve the source encodings until their retention is committed, and
record each successful path/length/digest before beginning the next fallible write. On failure
retain the completed bindings and a recoverable representation or explicit retention status
for remaining encodings in the single result. A bounded temporary-file/rename strategy is
advisory; the required outcome is no destruction of completed evidence before replacement.

Required verification: exercise the real retention writer with two encodings and a controlled
failure/interruption at the second write. The real final result must bind the first complete
artifact and preserve/account for the second encoding; no unbound partial file can masquerade
as a completed boundary. Ordinary capacity completion must retain both byte-exact bindings.

## Design verdict and budget disposition

STRAINED: the per-hand decomposition, real codec use and exact rational reference comparison
fit the intended small checkpoint. The orchestration repeatedly substitutes local flags and
container shape for whole-path invariants: cleanup has one broad guard, full coverage is a
length check, and boundary evidence is removed before replacement is established. The r001
disposition already accepts ownership, sample admission and retention corrections; the
residuals above show that the mechanism was not closed across related paths.

A bounded rework of the tool's admission and ownership/retention boundaries is preferable to
another isolated condition per example. Advisory technique: one validated schedule with
explicit occurrence identity, one partial report owned across cleanup, and monotonic retention
of measured data. This is confined to the tool and its affected tests; no sealed evaluator,
new general framework or whole-slice rewrite is indicated. The controller/finalizer should
apply the workflow's repeated-contract rule and document any decision to patch instead.

Budget is a controller decision, not a proven candidate algorithm defect or a reason to invent
an 800-line hard gate. Raw frozen totals independently reproduce 792 production / 428 test
lines. The original brief says 600/400; the controller explicitly raised the budget, while the
addendum labels 800/500 as the drafter's unconfirmed reading. The stated 1,000-1,100 production
projection for the whole slice is an estimate, not an independently measured final size.
An explicit whole-slice number should be settled before proceeding to bridge completion.

## Independent inventory compared with deferred coverage

The initial inventory was recorded before coverage.md, checks/ and prior-disposition.md were
opened. Its SHA-256 is bea7702af654c8534f6109f917f2a7608bc3ac5aa5502bdbd059a456b722a642.
Its original file is eval-code-r003-review-02-inventory.md. It has not been revised to match
these conclusions. No sibling review, prior-round review or implementer transcript was read.

- Frozen identity: verified ref, sole parent, tree and exactly seven changed paths. Recomputed
  each changed blob SHA-256 and sorted whole LF rows with ordinal byte-equivalent ordering.
  Result matches both the pinned manifest digest and manifest.sha256's exact bytes. All 34
  direct BASE dependency blob IDs match. This is a direct inventory, not transitive closure.
- Plan bytes/schema: source and focused cases cover oversize rejection, NaN/Infinity, 1e999,
  finite non-bool seconds, exact bounded memory, closed phase members, prefix, seed, universe
  digest/count and ordered permutation. Both fixtures independently have 1,081 unique names
  and their sorted-name universe digests match. Full sample identity remains I-02. Seed/index
  banks are explicitly refused for these two phases; later agreement banks remain outside scope.
- Declared domain/teacher/reference: s=3 and s=6 are refused by bet_action, hand_totals and
  build_reference, and by tool stack admission. The bet is constant raise_to(2). Source uses
  two real kernel settlements per villain and a single hero reference with explicit CALL.
  Forced values and BR remain separate calls. The frozen evaluator accumulates expected values
  with += and returns BR's value through expected_utilities; exact dyadic lattice checks precede
  action comparison. The focused receipt exercises royal ties and the real nonzero As Ad game.
- Numeric coverage: signed cancellation, both smallest lattice gaps, false production tie,
  changed total, wrong action, extra map key and nonfinite controls are present. Arithmetic
  fixtures are correctly labeled. No full-pool census or nonzero-cancellation poker tie census
  is claimed by this checkpoint.
- Capacity: real key/codec search and returned boundary encodings are covered, including an
  all-fit and one-row-failure control. Happy-path retention binds path/length/digest in source.
  No existing test calls retain_boundaries with a real boundary row; I-03 identifies the
  corresponding interrupted-retention defect, not merely a coverage percentage gap.
- Transport/ownership: the sender thread prevents initial pipe-fill from blocking the watchdog
  on its write. That stall is explicitly untested. Real completion, assignment refusal and
  budget-kill cases cover ordinary containment; none exercises the cleanup exceptions or
  cleanup-time interrupt in I-01. A nested job.close is present but is not an individual guard
  around every earlier release. The deferred ownership assertion overstates the source.
- Stage events: successful completed stages survive the ordinary tested budget kill and absent
  stages are labeled. I-01 covers cleanup-time data loss; I-02 covers schedule coalescing.
- Run record: the focused tests use real finish_run in a disposable repository on success and
  1e999 refusal, with exactly one journal row. They replace supervise, so they do not establish
  the interrupted supervisor-to-writer composition. main now invokes finish_run from finally
  for ordinary admitted work failures and KeyboardInterrupt, and json_safe handles nonfinite
  floats. Source records output_directory before runtimes/plan work on the normal creation path.
- Tests/registration: both suites are added once to tests/cases.json. The actual pytest harness
  discovers each unittest suite and journals total counts; two pytest items mean 22 unittest
  cases here. The fixture Git-resolution correction aligns with the scrubbed environment.

The deferred category matches the independent inventory's data flow, but its cleanup and full
sample assertions are falsified by source. Missing tests alone are not treated as product
findings. The three findings state concrete control-flow counterexamples and bounded outcomes.

## Evidence, commands and limits

Executed read-only Git queries with -c safe.directory=D:/Pontius: rev-parse, show, cat-file,
diff-tree, diff, ls-tree and status --short. Used PowerShell/.NET raw stdout byte reads and
SHA-256 for identity, pins, fixtures and hygiene; no candidate imports or owners were invoked.
The attempted .venv Python launch for a standalone hashing script was denied before execution;
all hashing was completed using .NET instead. One Select-String regex was corrected by reading
the complete evaluator; it is not an unresolved verification failure.

All pinned workflow/ruling/dependency/deferred-file hashes and the four checks/ receipt hashes
match the handoff. The receipt identifies this exact candidate/tree, Python 3.14.6, a disposable
snapshot, scrubbed environment, -B -P -W error::ResourceWarning and pytest exit 0. Its retained
journal states 22 unittest cases exercised, zero skipped, source_verified true. It is supplied
executed evidence, not a fresh test execution by this reviewer. The removed snapshot/result
cannot be re-inspected; no claim is made that its raw-worktree source digest was reconstructed
from Git blobs, because the owner's raw-byte digest also depends on checkout line endings.

Seven frozen changed paths independently pass LF/no BOM/no trailing whitespace/100-column
checks. Production files have 333 and 459 lines; test files have 198 and 230. The manifest
also confirms sealed dependencies were not changed. Existing working STATUS.md and journal
changes were observed by status only and left untouched.

No project tests, solver, capacity/preflight measurement, host, execution owner, source edits,
Git mutation, publication, ceremonial commit or integration was performed. This report is
review evidence only; it neither authorizes a retained run nor completes the Tier C gates.
