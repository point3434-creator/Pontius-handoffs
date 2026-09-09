# Cold review 01: v0a-eval-panel-code/r004

Reviewer: Codex (independent cold pass 01). Date: 2026-09-09.
Verdict: NOT CLEAN. Design verdict: STRAINED.
Three Important findings; no Critical findings. Findings are source-derived counterexamples,
not newly executed reproductions. The packet's executed evidence is assessed separately.

Candidate: 0bc19bcaad5c6660468094772216cac2dc27a651
Manifest SHA-256: 70ca4c76bc8bdefe8ffaab72fa8de5b7d24d49697157436d78a3e1c025a370c3
Base: f647a7989394f084875a040b20c41891168163ed
Tree: 45c76c9c8f2d7fbfa4b00e4e5b8b8cffc538b4fc
Ref: refs/heads/review/v0a-eval-panel-code/r004

Every finding below binds to this complete candidate/manifest pair. Locations refer to
frozen Git blobs, never to mutable worktree files. Administrative review reauthorization
was supplied with this assignment. No additional work or execution gate is implied.

## Important findings

### I-01: Cleanup can certify a failed release, and drained stages remain local until return

Confidence: high for the frozen control flow; the counterexamples were not executed.
Locations: tools/v0a_eval_panel.py:303-321, 359-395, 477-495;
BASE tools/v0a_table_host.py:441-445 (Job.close);
tests/test_eval_panel_tool.py:221-258, 306-321, 344-354.
Requirement: implementation brief criterion 3 and design section 3 require interrupted
work to retain completed observations; the r004 contract explicitly forbids verified
cleanup after a recorded cleanup failure and requires retention if supervise unwinds.

Counterexample A: let an ordinary worker exit, all threads finish and all pipes close.
verify sets cleanup_verified to true at lines 370-375. Then Job.close raises HostRefusal
because the real CloseHandle returns failure. attempt records that failure and an error,
but nothing clears cleanup_verified. The final result is failed with cleanup_verified=true.
A cleanup interrupt after successful verification has the same stale certificate. An
isolated earlier join failure also need not prevent the verification predicate becoming
true once its thread dies: the predicate does not consult cleanup outcomes at all.

This does not incorrectly turn the overall status into completed: the errors/status checks
still stop that. It does publish a false resource-cleanup assertion in the retained result,
including when the last native release was not verified. Job.close removes its stored
handle before calling CloseHandle, so this is precisely a release whose success matters.

Counterexample B: a production stage has been received and drained into hands. A Ctrl-C
arrives after cleanup finishes but before observations.append at lines 389-391 (or between
cleanup attempts, outside an attempt's try). The unwind skips the local-to-report merge.
main catches the interrupt and finishes its caller-owned report, whose observations still
exclude that drained preflight record. Passing report by reference did not make hands or
its new records caller-owned. The lost stage is distinct from an event never received.

The fault case checks process.poll-derived worker_exit_code independently of its injector,
which is a valid observation of the direct process's death. However its always-failing
Job.active also prevents verify from succeeding, masking the stale-certificate case.
The interrupt case checks wait interruption but never asserts cleanup_verified is false.
The main ownership case substitutes supervise and directly inserts observations into the
report; it bypasses the real supervisor's local hands accumulation and delayed merge.
These executed cases establish their schedules, not the two counterexamples above.

Smallest correction: make each drained record reachable from the caller-owned report when
it is first registered; retain finalization diagnostics without relying on a normal return.
Make cleanup verification a final conjunction of actual resource observations and all
required cleanup outcomes, including the last job release, with failure monotonicity.
Keep the existing independent release attempts. Add real-supervisor schedules that isolate
one failing release while the remaining checks succeed, and interruption after a real
stage drain before the ordinary return merge. Preserve native operations and independent
process-death checks; do not certify resource effects through injected bookkeeping.

Residual ruling: this is a second residual on r001 A / r003 I-01's cleanup and interruption
retention contract. Per the pinned workflow, stop in-place fixing of that contract; it
requires its own candidate and a written root-cause note explaining both earlier misses.
The caller-owned report and per-step wrappers improve the mechanism but do not close it.

### I-02: declared-full admission erases the roles required by its worker and estimator

Confidence: high, static counterexample.
Locations: tools/v0a_eval_panel.py:124-136, 150-153, 236-245, 436-441, 481-486;
tests/test_eval_panel_tool.py:75-114, 166-181.
Requirement: brief criterion 2 and design section 3 require four declared development
hands and a separate royal control, with the full-pool estimate based on that development
sample. The plan's declared board/universe also identifies the pool being preflighted.

Concrete accepted plan: start with the frozen preflight fixture, keep its board, resource,
universe and permutation, move As/Ad out of development_hands, and append the control
object {board: [2c,7d,9h,Js,Qc], hand: [As,Ad]} to controls. All JSON card values remain
strings. The combined canonical sample is exactly the same five unique identities, so
lines 129-134 admit coverage=declared-full. No expensive execution is needed to establish
that admission path from the frozen predicates.

run_plan labels the moved hand control at lines 238-239. If all five comparisons complete,
the supervisor reports completed, but full_pool_estimate discards the moved hand because
it requires label=development. It returns not_estimated, declaring that required hand
missing. main still retains status=completed with coverage=declared-full. Thus an admitted
full preflight need not produce the complete required development sample or its estimate.
This is a disclosed missing estimate, not a fabricated one-hand numerical estimate.

The same loophole permits development_hands=[] and all five identities in controls. Then
plan.board is not constrained by any development sample: it can be another valid board
with that board's matching universe/permutation, although the five controls use the two
fixed sample boards. The admitted pool identity can consequently differ from the declared
development board while the combined-set check still passes.

The existing negative cases reject substituted identities, duplicates, malformed hands
and invalid controls, and canonical naming is now consistent. They do not move valid
identities across the two roles. The estimate case creates the desired development rows
directly, so it does not exercise the admission-to-worker-to-estimator mismatch.

Smallest correction: validate the development board and the canonical development-hand
membership separately from the exact royal-control membership, or carry one role-bearing
canonical admitted schedule through both execution and estimation. A full preflight must
not report completed when its required role-specific sample is missing. Add admission
controls for moved roles, all-controls/empty-development, and a changed pool board with
otherwise exact control identities; retain the accepted reversed-card-order control.

Residual ruling: this is a second residual on r001 D / r003 I-02's declared-sample contract.
It requires a separate candidate and the workflow's root-cause note before another fix.
The original duplicate/count-only defect is corrected; the protected admission contract
still fails because identity includes a semantic role used downstream.

### I-03: An interrupted rename can publish an artifact before its report binding exists

Confidence: high for the interruption window; no fault schedule was executed here.
Locations: tools/v0a_eval_panel.py:406-424, 479, 487-495;
tests/test_eval_panel_tool.py:137-164.
Requirement: the r004 retention contract requires failed/interrupted publication not to
leave a completed boundary artifact unbound; completed bindings and remaining encodings
must be retained together in the invocation's result.

Concrete schedule: staging.write_bytes succeeds; os.replace moves the complete encoding
to capacity-boundary-<count>.blueprint.json; KeyboardInterrupt is delivered at the return
from replace, before retained[count] is assigned. The finally block sees the still-pending
encoding, labels it unwritten/incomplete, and does not reconcile the successful rename.
main retains an interrupted result with no boundary_artifacts entry for the now-complete
canonical artifact. An interrupt during binding construction at lines 415-416 has the
same effect. This needs only the already-supported interruption category, not malformed
worker output or a second invocation.

The encoding is still recoverable from boundary_base64, and the result is not marked
completed. The material remaining defect is incomplete artifact-to-result identity and
an inaccurate unwritten label, not irreversible loss of the measured bytes. A consumer
following boundary_artifacts cannot discover the completed file through that binding.

Smallest correction: register the intended artifact identity and publication state before
the fallible rename, and reconcile whether the final file was published when rename or
binding is interrupted. Preserve the pending encoding until an unambiguous binding is
retained. A deterministic schedule should perform the real rename and then trigger the
interrupt, observing the final file and retained report independently of the injector.
Do not satisfy this with a fake successful filesystem operation.

The current second-write test raises before any write on its failing branch. It proves
that an earlier completed binding and the next pending encoding survive an ordinary
write refusal; it does not cover the publication-to-binding interval. Retrying after a
fully completed row is safe statically: the absent boundary_base64 becomes {}, existing
bindings survive setdefault, and finally retains complete. A partial physical write uses
the distinguishable .partial suffix. Those improvements are acknowledged.

Residual ruling: the original r003 I-03 write-loss mechanism is corrected, but the same
publication/retention contract has this first residual. It has not independently reached
the second-residual threshold. Do not count it as another residual on I-01 or I-02.

## Independent inventory, coverage comparison, and design assessment

The initial inventory was written before coverage, checks, or prior disposition were
opened, and was checked for LF, BOM, trailing whitespace and column length before writing.
Its SHA-256 is 3b4c09fd97db9b2114ccc7ab92805e14a8ea19bb0b461dddc4d9634479fe4b0d.
It covers plan roles, native release/finalization, caller retention, and publication
intervals independently of the drafter's corrected-path table.

The deferred table maps the same main functions and correctly describes the added normal
write-failure, wait-interrupt, duplicate-input and partial-estimate cases. Its discovery
stops too early at wrapper/combined-set/staging patterns: the final close occurs after the
certificate, real records become report-owned after cleanup, roles disappear at admission,
and rename commits the file before binding. These are concrete missed members of the
recorded categories, not automatic defects inferred merely from absent tests.

The repeated-observation guard, stream-close fault, pipe-fill stall, real-worker main
invocation and run-directory write failure remain unexercised, as the packet states.
Their absence is not a separate product finding. In particular, stream.close has no
explicit timeout, and sequential join timeouts do not bound a later close against a live
I/O thread. The claim that every attempt is bounded therefore remains unverified under
compound termination/wait failure; I did not execute or claim a native hang reproduction.

SOUND would overstate orchestration correctness. STRAINED is warranted because the same
protected state is reconstructed across admission, worker labels, local accumulation,
cleanup verification and file publication. The bridge's narrow replay/enumeration/reference
shape remains appropriate. A bounded revision of the affected orchestration contracts is
preferable to a whole-slice rewrite: make admitted roles authoritative, attach records to
the run immediately, and finalize resource/publication state from the actual completed
operations. Costs are focused fault schedules and a small migration of internal report
construction; preserve schemas, native containment, measured stage data and immutable
source boundaries. A new framework or rewrite of sealed modules is not justified.

## Specification and engineering evidence

Specification result: FAIL on I-01 through I-03. Engineering-quality result: FAIL for the
same protected ownership/identity boundaries; the numerical helper has no material finding.
No runtime feasibility, poker-strength, export, host-agreement or Slice B claim is made.

- Replay/ranges/capacity: inspected real betting replay, card/key construction, complete
  hero universe, seeded permutation, real codec sizes and nested-prefix boundary search.
  Executed cases cover root invariants, changed stacks, board order, membership, conservative
  three-byte action difference, exact boundary, all-fit and one-row failure behavior.
- Teacher/reference: inspected per-hand real settlement, singleton continuation, explicit
  CALL villain, separate forced values and best response, and exact rational lattice rule.
  Inspected the frozen parser, continuation and evaluator consumers. Real singleton cases
  cover royal tie and As/Ad nonzero action; arithmetic fixtures cover signed residuals,
  false ties, wrong totals/actions/maps, smallest signed gaps and nonfinite values.
  The entire four-hand preflight sample was not executed end to end by these tests.
- Plan/worker: closed phase keys, runtime, finite resources, prefix/universe/permutation
  checks and canonical compatible hands are present. Separate stage costs/cache labels,
  budget exit and production-only estimate limitations are explicit. I-02 limits admission.
- Ownership: real worker/Job completion, assignment refusal and budget-kill cases exist;
  substituted-supervisor ownership tests use real result/journal writers in disposable
  repositories. This distinguishes actual native coverage from the main integration seam.
- Registration and isolation: cases.json adds exactly the two suites. The frozen harness
  imports the named modules, counts unittest cases/skips and emits one harness journal row.
  The supported runtime ruling is 3.14.6 only; no stale 3.11 acceptance gate was applied.

## Identity, receipt verification, and review actions

Read-only Git resolved the ref to the stated commit, sole BASE parent and tree. Exactly
seven paths differ from BASE. Each manifest SHA-256 was independently computed from raw
cat-file blob bytes; complete rows were sorted bytewise and joined with LF. The rows equal
the packet manifest exactly and its digest equals the bound manifest above. All 34 BASE
dependency pins reproduce using raw blob bytes and Git's blob-length framing. No replace
refs exist. Pinned workflow/rulings/dependencies and all deferred input/receipt digests
match their handoff values; no sibling or prior-round review was opened.

The receipt reports Python 3.14.6 in a disposable detached candidate snapshot with its own
uv dev environment; -B -P -W error::ResourceWarning; env -i with SystemRoot, TEMP, TMP,
PONTIUS_GIT and PYTHONDONTWRITEBYTECODE. Git is an absolute executable path. It reports
2 pytest entries passed, 44 deselected, and the harness journal reports 27 unittest cases,
0 skipped, exit 0, source_verified=true, and this candidate commit. Those are supplied
executed receipts, not a new review run. The removed snapshot and its result artifact
were not independently re-executed or fetched.

As an additional read-only identity check, 886 frozen source-scope blobs produce raw census
SHA-256 e04d1487948a2c44e1aa580e88262e8ad89d47fb5c01cf605203787118288dba. Applying the
normal Windows CRLF checkout transform while preserving the frozen eol=lf attributes
reproduces the receipt's raw-source census:
e0ab0696981eef0aa7ffac5f514dc536795d229ef6af2ea4451479abb0ff3bfb.
This explains the raw-Git versus checkout digest distinction without executing the owner.

Raw candidate census independently reproduces 834 production / 556 test lines and
731 / 481 nonblank lines. All seven changed blobs are LF-only, BOM-free, <=100 columns,
with no trailing whitespace. The projected 1,050-1,150 whole-slice production lines are
an estimate, not a measured final size. They are below the pinned 3,000 hard ceiling;
1,200/600 remains the working figure. The anticipated test-budget overrun is disclosed
and is not a new gate under the controller's clarification.

Review commands were read-only Git show/ls-tree/diff-tree/diff/cat-file/for-each-ref and
packet reads, with standalone Python standard-library hashing/text validation. An initial
bare python lookup failed because it was absent from PATH; subsequent byte-audit scripts
used an explicit installed interpreter. No project module was imported or executed, no
test or owner ran, no dependencies were installed, and no source or Git state was changed.
Only the three assigned append-only review staging artifacts were created. Their format
was validated in memory before exclusive creation and checked again after writing.
