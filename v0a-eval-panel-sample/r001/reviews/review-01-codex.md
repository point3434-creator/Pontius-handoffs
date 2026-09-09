# Codex cold review 01 - v0a-eval-panel-sample/r001

Verdict: CLEAN. Design verdict: SOUND.
Reviewer: Codex, independent cold subagent. Issued: 2026-09-09.
Scope: role-bearing admission, worker execution, complete-sample reconciliation and estimation.
No Critical, Important or other required correction survives this scoped review.

Candidate: 72954e1331c9b191d927c1c4b82f277bcd322a4c
Manifest SHA-256:
d79035495a278fa8ee3fb1a6adc6fc1838938900ab7c19bbdd434264faf63510
Base: 182d14e213c6f0b7d7578e429f81d051a9e59707
Tree: 73797f3b554f68c3ced59cc295b0e41f1507b8bb
Ref: refs/heads/review/v0a-eval-panel-sample/r001

This verdict binds the full candidate and manifest pair above. It is a local review result,
not an adoption verdict for the combined implementation or the separate cleanup follow-up.

## Findings and design assessment

No material product defect was established in the affected sample contract or its consumers.
Specification result: no demonstrated violation in scope, supported by fresh static inspection
and the supplied focused executable receipts. Engineering-quality result: SOUND in scope.
The independent reviewer did not execute the candidate; the GREEN is supplied evidence.

The replacement shape addresses the prior projection problem: admission records each role,
board and hand in one immutable schedule, execution iterates that schedule, and both success
classification and estimation call the same complete_sample reconciliation. JSON transport
revalidates the immutable wire snapshot at the worker boundary. This is a bounded change to
one tool, with no extra service or lifecycle layer and no numerical bridge changes.

## Independent discovery and substantive checks

Initial inventory was issued before opening coverage.md, checks/, prior-disposition.md or
repair-plan.md. Its create-only file is eval-sample-r001-review-01-inventory.md, SHA-256:
a4502df3e3a6eec7f67647b192cd298e304e5dd9f8100e80ce0fd7f82cdbe00d

Locations below are frozen at the candidate above; line numbers refer to Git object text.

- Admission: tools/v0a_eval_panel.py:111-180 checks phase/runtime/root/universe/permutation
  and limits before freezing the document. Lines 157-169 bind roles and canonical identities,
  reject duplicates across roles, and require the explicit development board plus the exact
  four development hands and royal control. Moving any development identity to controls,
  omitting or adding identities, and all-controls main-board rebinding cannot pass.
  Private-card reversal canonicalizes to the same hand; nonascending boards are refused.
- Stable admitted value: tool:52-71 and 170 use strings and tuples of immutable card values.
  document returns a new JSON tree. Mutation of the caller's original dict or a returned
  document does not alter the admitted wire or schedule. The AdmittedPlan fast path is a
  trusted internal representation; searched callers do not construct arbitrary instances.
- Execution: tool:219-290 carries one role/board/hand identity through production, warm
  repeat, singleton construction, both forced actions, best response and comparison.
  run_plan consumes admitted.schedule. supervise serializes admitted.document at 367-370;
  worker validates it again at 287-289. Budget exhaustion and disagreement emit a failure
  that the parent retains even when worker also emits its final completed event.
- Aggregation and completion: tool:374-402 owns preflight rows in report observations on
  first receipt. Rows are keyed by role, board and hand. Repeated events after completion
  add errors. At 481-488 an otherwise completed worker becomes failed when its admitted
  sample is incomplete or disagrees. At 534-548 exact membership, unique records, exact
  True completion, the complete stage set and exact True comparison are required.
  Wrong role/board/hand, extra/duplicate rows, omitted control, absent stage, unfinished
  hand and failed comparison cannot satisfy that predicate.
- Estimate: tool:551-568 invokes the same reconciliation before selecting only development
  production elapsed times. The four costs, not the control or reference times, enter the
  min/mean/max extrapolation. Every admitted control must nevertheless pass. Capacity has
  no estimate; test-subset explicitly returns not_estimated. The value is labeled an
  estimate with cold/warm and production-only assumptions, not a measured full-pool cost.
- Retention consumer: tool:595-615 passes one admitted object to supervision and estimation,
  retains the plan identity and observations, and uses the existing finish_run boundary.
  Exceptions retain a failed report. src/pontius/execution.py owns result and journal output.
  Cleanup source was inspected only where its outcome feeds sample success; its separate
  follow-up is not certified here.
- Direct numerical dependencies: src/pontius/eval_bridge.py supplies canonical card names,
  replayed s=4 root, compatible hands and the independent singleton comparison consumed
  by each stage. Static tracing confirms the same scheduled board/hero reaches production
  and reference. The bridge blob is unchanged from this candidate's parent. Neither the
  sealed evaluator nor future export/agreement/paired-inference mechanisms changed.
- Consumer discovery: git grep for the affected names and v0a_eval_panel found the tool,
  tests and specification references, with no additional production caller in the frozen
  tree. tests/cases.json and tests/test_pontius.py register/run the two focused suites.

## Deferred coverage comparison and evidence limits

The independent inventory's admission, stable schedule, stage identity, completion,
correct cost population, failure classification, provenance and test-oracle categories
are addressed by coverage.md invariants 1-4 and the inspected implementation.
The deferred prior disposition's sample finding is closed by the role-bearing equality
at admission and shared complete_sample consumers, not merely by a renamed label.

The focused tests provide these useful observations:

- tests/test_eval_panel_tool.py:69-83 tests one moved development hand, all four moved,
  and all identities under controls with the main board rebound. Existing admission cases
  at 94-133 cover missing/substituted/duplicate/colliding hands and canonical reversal.
- The estimator fixture at 185-208 covers a valid full sample, incomplete development,
  omitted royal control, failed royal comparison, subset exclusion and capacity exclusion.
- The real five-hand test at 441-456 checks the literal AdAs, KdKh, 8dTd and 3c4d identities
  on the development board, the royal-board 2c3d control and a four-hand estimate. Its
  helper at 388-421 uses a disposable clone, real source admission and main/worker path,
  then independently reads the published result and verifies its journal output hash.
- Existing stage and budget tests at 210-224 exercise real per-hand emission and refusal
  to begin a hand once the deadline is exhausted. The focused population also includes
  the unchanged bridge suite and real containment/ownership controls.

Nonblocking evidence observations, not product findings or new acceptance gates:

1. Coverage describes the estimator fixtures as literal. In fact, lines 188-195 construct
   their identities from admitted.schedule and stages from STAGES. Their standalone
   identity oracle is therefore coupled to implementation. The separate real-worker test
   does supply literal independent expected identities, so the whole evidence set avoids
   relying exclusively on that coupled fixture.
2. The three role-movement examples represent classes; they do not enumerate every subset
   of moved hands. Admission's exact role-bearing equality statically covers the category.
3. Supplied executable cases do not individually demonstrate each duplicate/extra row,
   missing-stage and post-admission mutation challenge in the independent inventory.
   The relevant predicates and immutable values establish those properties statically.
   Missing coverage alone is not treated as a product defect.
4. The full-worker positive control passed on RED too; it establishes the valid path, while
   the new role-movement negatives demonstrate the original admission defect. It is not
   claimed that the positive control alone discriminates the fix.

## Supplied executable receipts

These were read after the independent inventory and hash-verified, not rerun by this reviewer.
Both identify CPython 3.14.6, -B -P, ResourceWarning-as-error, locked snapshot environments,
absolute PONTIUS_GIT via the stated scrubbed environment, and source_verified true.

Command represented by both receipts:
pytest -p no:cacheprovider -q tests/test_pontius.py -k 'eval_bridge or eval_panel_tool'

GREEN: candidate 72954e1331c9b191d927c1c4b82f277bcd322a4c, exit 0.
stdout: 2 pytest entries passed, 44 deselected, 249.78 seconds.
journal: 33 unittest cases exercised, zero skipped, passed.
RED: candidate beb069455a6d3ce20f202c0b4398683548631a33, exit 1.
stdout: one pytest entry failed, one passed, 44 deselected, 253.43 seconds.
The failing tool suite has exactly three ValueError-not-raised assertion failures for
role movement/rebinding and zero unittest errors. Journal: 33 cases, zero skipped.

Read-only Git independently confirms RED changes only tests/test_eval_panel_tool.py from
this BASE; its tool blob equals BASE's 3637c4dc6e62fd6da9390d28fa322f9295f3702b.
The records establish focused correctness evidence. They do not authorize or constitute
retained capacity/preflight measurements, broad acceptance, poker strength or pool cost.
This review did not inspect snapshot working files or independently recreate run output
hashes referenced inside journal receipts; the supplied journal assertion remains attributed.

## Identity, provenance and hygiene verification

Fresh read-only git rev-parse, show --format=raw, diff --name-status and cat-file blob checks:
ref, parent, tree and exactly two changed paths match candidate.json and the handoff.
Diff size is 127 insertions and 39 deletions across the two files.

Git-object SHA-256 values:
- tools/v0a_eval_panel.py, 29481 bytes:
  793c83c37cd36e268115bf413476564ec46d7daa5e07ed7702dfb6e0771d09d5
- tests/test_eval_panel_tool.py, 27763 bytes:
  ccef961bed883ab79985cd620fe584885753e0571cdde8106b5d641a4860d7e3

PowerShell/.NET streamed raw Git blob bytes, formed digest-first whole rows, sorted with
ordinal comparison, and joined with LF. The generated manifest bytes equal manifest.sha256
exactly and hash to the bound manifest above. Both changed files are LF-only, BOM-free,
without trailing spaces and at most 100 columns. All 16 handoff input/receipt pins match.
coverage.md SHA-256 matches:
9b481d761c8eaa73bfe9e26447e9cc54ddbe046a6fe99727d994a9685958129d

All 34 dependencies.json blob pins match its explicitly stated original base:
f647a7989394f084875a040b20c41891168163ed.
This is not the immediate parent. Relative to that original base only tests/cases.json
among the pinned paths differs in this candidate: it adds test_eval_bridge and
 test_eval_panel_tool. Both registrations already exist in the immediate parent.
The bridge's candidate/parent blob is e4826810d4af13957c944b89134ab9ae5f466dd9.
No source file outside the two declared paths differs from the immediate parent.

## Review procedure and disposition

Sole substantive entry was the frozen handoff. Governing documents were read from their
pinned Git identities, with controller rulings overriding stale Python 3.11 language.
No implementer transcript, sibling review or other task was inspected. The permitted
prior-disposition and repair-plan inputs were opened only after inventory issuance.
No Python execution, project execution/tests, source changes, network writes, commits,
pushes or packet publication occurred. Existing STATUS.md and execution_journal.jsonl
working modifications were observed and left untouched.

This is one independent Tier C pass. CLEAN / SOUND applies to the frozen sample scope.
Separate ownership cleanup, final combined review and later workflow gates remain owned
elsewhere; this report does not grant their completion. No required sample correction.
