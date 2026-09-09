# Cold code review 02: Codex

Defect verdict: **NOT CLEAN**.
Design verdict: **STRAINED**.

The s=4 mathematical decomposition fits the accepted task. The new orchestration loses
ownership or evidence on concrete failure paths, and its admission checks do not enforce
the fixed reference domain or the adopted plan contract. Five Important findings remain.
No source, candidate, project state, or published packet was changed by this review.

## Attribution and immutable identity

Reviewer: Codex, independent cold pass 02, 2026-09-09.
Task/round: v0a-eval-panel-code/r001; NEW-SURFACE, Tier C.

- Candidate: b1fdacf157649ca92d1aee3e39b7b0471edbcd5d
- Parent/base: f647a7989394f084875a040b20c41891168163ed
- Tree: 7a450159a8ca30cb0ac176e66f6e2a25235c457d
- Manifest: 376dff405c15301a489ea3fde84abc3a41c2afa4c33c6ee67423477ca9e08b8e

All findings below bind to that candidate and manifest. C denotes the candidate; B denotes
its base. File locations are frozen blob line numbers, not working-tree line numbers.
Requirements are B:docs/architecture/v0a-eval-panel-impl-r001/{brief,design}.md and the
parent lane design, with the pinned controller rulings overriding stale runtime wording.
Only CPython 3.14.6 is required here.

The initial invariant inventory was written before opening checks/. Its original digest was
bcc16dde1294af8f85f0f40b7e22973c81f1b9ae89d4a352504fda74a77f3e0b.
Two table cells were subsequently shortened solely to meet the 100-column delivery rule;
no invariant, dependency, or failure category was added after reading checks/.
Final inventory SHA-256:
22fe701f6373fcf0e091cc9f055e2bfc232a744e3e8e77cae28895a3e78500ff.

## Important findings, ordered by consequence

### I-01: A failed Job assignment leaves a suspended worker without cleanup ownership

Severity: Important / High. Confidence: high, from frozen control flow; not executed.

Locations: C:tools/v0a_eval_panel.py:175-180 and 202-211.
Dependencies: B:tools/v0a_table_host.py:383-385, 430-446, and 576-623.
Requirements: design:164-165, 279-282; workflow checklist items 1 and 9.

Concrete scenario: Popen succeeds with CREATE_SUSPENDED, but AssignProcessToJobObject
refuses the process, for example because containment cannot be established in the launch
environment. Job.assign raises. The new finally block checks job.active(), which is zero
because the child was never assigned, and therefore does not terminate anything. It then
waits ten seconds on the still-suspended child. That wait raises TimeoutExpired; job.close
is skipped and no direct process.kill path exists. The child can survive the failed tool
invocation suspended outside its Job. The original containment cause is also replaced by
the timeout in main's report because supervise never returns its accumulated errors.

This is a new caller defect, not a defect attributed to the unchanged Job primitive.
The base host's actual owner already handles precisely this state: finish kills an
unassigned root at lines 591-592 and attempts later cleanup despite earlier failures.
More generally, any query/terminate/wait failure in the new finally block skips subsequent
cleanup and event harvesting. A cleanup query failure after observations were received can
therefore discard those observations and the original failure cause as well.

Required outcome: own the process independently from Job membership immediately after
Popen; terminate and reap an unassigned suspended process; attempt every owned cleanup
operation even if an earlier one fails; retain primary and secondary failures and received
observations. Do not report cleanup verified while owned readers or processes remain.

Smallest correction direction: bounded, exception-isolated cleanup with an explicit
unassigned-process branch and unconditional Job/pipe cleanup in the new supervisor.
Do not modify the sealed host. Verification must drive the actual launcher through an
assignment-failure schedule and independently observe process death, handle cleanup, and
retention of the original containment failure. The current mocked ownership case cannot
supply this evidence.

### I-02: Nonfinite resource values pass admission and can prevent the sole journal record

Severity: Important / High. Confidence: high, from frozen parser and writer contracts.

Locations: C:tools/v0a_eval_panel.py:53-56, 145-148, 192, 258, 265-272.
Dependency: B:src/pontius/execution.py:139-161.
Requirements: design:27, 164-165 and 279-282; workflow checklist item 10.

Concrete scenario: change resource.seconds in the capacity fixture to JSON number 1e999,
leaving memory_mib=2048. json.loads produces positive infinity. The only predicate is >0,
so both parent and worker admit it. The worker deadline and parent deadline comparison
cannot exhaust this budget. Even if capacity completes normally, main embeds the plan
containing infinity in report. finish_run uses json.dumps(..., allow_nan=False), which
raises before result bytes or the journal line are written. This loses the one required
run record after admitted work. No malformed JSON token is necessary for this scenario.

Booleans also satisfy the resource comparisons. Fractional or excessively large memory
values reach the native c_size_t assignment without validating exact type or range.
These are related admission holes, although their precise native outcomes were not run.

Required outcome: before creating a worker, admit only finite positive numeric seconds
with booleans excluded, and an exact positive memory quantity whose byte conversion fits
the native field. Rejected input must yield a serializable failed outcome without retaining
nonfinite objects in the structured result. Preserve a raw-input hash or safe diagnostic.

Smallest correction direction: validate the complete resource value domain at the plan
boundary and reject nonfinite JSON values. Verify through main with the real result/journal
writer in a disposable snapshot; check zero worker starts and one failed record for 1e999,
nonfinite constants, booleans, fractional memory and native-range overflow.

### I-03: The reference accepts s=3 and raise-to 1 as the fixed s=4 domain

Severity: Important / Medium. Confidence: high, from kernel and reference source.

Locations: C:tools/v0a_eval_panel.py:48-49;
C:src/pontius/eval_bridge.py:84-89 and 198-220.
Dependencies: B:src/pontius/no_limit_betting.py:392-422, 519-529 and 696-738;
B:src/pontius/legal_river_continuation.py:110-143 and 288-307.
Requirements: design:68-89 and 99-111; parent design's fixed s=4 ruling.

Concrete scenario: use replay_root(stacks=3), the royal-spade board, and hero 2c 3d.
After the valid prefix, each live seat has one chip left. The kernel's short-all-in rule
sets minimum_raise_to=maximum_raise_to=1. bet_action accepts this and returns raise-to 1.
The hero action assertion then compares the game with (CHECK, bet), where bet was derived
from that same changed root. It does not assert the specified raise_to(2). The singleton
still has 990 deals; all showdown utilities on the royal board are zero, and the fold
line returns magnitude 2. Every current domain predicate passes, and lattice validation
can report a passing tie for a game the contract explicitly requires it to refuse.

On a non-tie board the bet line at this depth has +/-3 returns, outside the stated
power-of-two scaling derivation. This review does not claim the numeric bound actually
fails there; the demonstrated defect is admission of a different game under that rule.
The existing changed-domain test uses s=6, which has multiple bet sizes and misses s=3.

Required outcome: enforce the actual fixed root/domain, including s=4 and exactly
(CHECK, raise_to(2)), independently of the action inferred from the supplied root.
Keep generic root replay available for negative key controls if desired. Validate domain
before production work at the tool boundary and again where the reference claims its bound.

Smallest correction direction: explicit fixed-domain validation shared by the production
entry/reference boundary, with an s=3 refusal control in addition to s=6. Verify the royal
s=3 example fails before a reference can be classified as passing.

### I-04: The plan does not freeze the required ordered pool or enforce preflight coverage

Severity: Important / Medium. Confidence: high for the contract mismatch and source trace.

Locations: C:tools/v0a_eval_panel.py:42-68, 116-127, 265-267;
C:tests/fixtures/eval_panel/plan-capacity.json:1-8;
C:tests/fixtures/eval_panel/plan-preflight.json:1-10.
Requirements: design:10-15, 24-27, 44-45 and 148-150.

Concrete scenario: the supplied capacity fixture has no complete hand universe, ordered
permutation, or declared prefix. It is nevertheless accepted. run_plan creates the hand
order itself and places it only in the result after the probe. If a caller supplies a
permutation field with duplicate, missing, reordered or different hands, validate_plan and
run_plan ignore it and still probe the regenerated order. The run can complete without
checking that the actual measured family equals an explicitly frozen family in the plan.
The implementation's seed-only rule may be deterministic, but the adopted rule explicitly
requires the actual ordered contents in the plan and refusal of missing mandatory inputs.

A separate observable instance of this incomplete plan admission is preflight: replace the
development board/hands with royal-spades/2c 3d and set controls=[] (exactly the in-process
control used at C:tests/test_eval_panel_tool.py:64-74). The plan is accepted and can complete,
although none of the four mandatory development hands and no distinct control run occurred.
main also creates an ordinary full-pool estimate from that substituted development row.
There is no test-only/subset or incomplete-coverage classification at this entry boundary.

Required outcome: reconcile the schema with the adopted phase requirements before launch.
For capacity, require the frozen universe/permutation contents and check exact membership,
order and agreement with the declared seed/rule. Bind the declared prefix to the replay.
For an accepted cost preflight, verify the required development/control schedule; a bounded
subset used by correctness tests must be explicitly identified and cannot satisfy the full
preflight predicate. The design also names runtime and seed/index-bank fields: either
implement their applicable validation or obtain an explicit phase-specific amendment.

Smallest correction direction: expand and validate the two data plans using the existing
narrow schema; no service or generalized planning framework is needed. Test omitted and
mismatched permutation contents and a missing control through the real plan entry point.
A controller decision to use seed-only identity or defer other plan fields is an alternative
specification change, not an assumption this candidate may silently make.

### I-05: A budget kill during reference work discards already completed cost observations

Severity: Important / Medium. Confidence: high for loss of data; trigger timing not measured.

Locations: C:tools/v0a_eval_panel.py:90-106, 133-134 and 192-205.
Requirements: design:148-165; the brief's cost-before-full-pool and failure-retention criteria.

Concrete scenario: the first hand's production enumeration and its measurement finish,
then the finite wall budget expires while build_reference or a later reference stage is
running. Production totals, elapsed/CPU time and cache observations exist only in the
worker's local observation dictionary. Nothing is emitted until all reference and comparison
stages return. The supervisor kills the worker, retains a budget_exhausted status, but has
zero hand observations to retain. The completed production measurement is lost. The same
loss occurs when a later reference stage raises normally: worker emits only an error.

This prevents the failed preflight from reporting the completed cost information needed
to understand why the authorized envelope was infeasible. It is distinct from accepting
an incomplete reference: partial costs should remain partial and must not pass preflight.

Required outcome: publish each completed measured stage to the parent before beginning the
next fallible stage, with enough identity and ordering to reconstruct one partial hand
observation. On kill/refusal retain those completed costs and label the remaining stages
unavailable; keep the phase failed/incomplete. This remains one final result and one journal
line, with no per-stage files or source scans.

Smallest correction direction: stage progress events merged into the single parent report.
Verify a bounded stop after a real production stage and before reference completion; the
result must retain that production measurement, the failure reason and missing-stage labels.

## Design assessment

STRAINED, not WRONG SHAPE. The per-hand library and exact comparison are appropriate.
The orchestration assumes that a whole hand operation and then its cleanup return before
an outcome becomes durable in the parent. That same shape produces I-01's lost causes and
I-05's lost measurements. Validate the fixed plan once, retain stage results as they become
available, and keep cleanup as a bounded owner operation that cannot discard the report.
These are local changes to the new tool, not a new lifecycle framework or sealed rewrite.

The size issue is advisory for this checkpoint. Frozen blobs contain 575 production lines
and 264 test lines, below 600/400. The accepted brief explicitly permits this first source
checkpoint before bridge completion; unfinished steps 4-7 are not defects here. Its remaining
25 production lines make the later bridge budget strained. Return that whole-slice budget
to the controller before further implementation/freeze; this review grants no increase.
There is no evidence-based need to compress the code or change the accepted poker game.

## Requirement and dependency assessment

- Identity/scope: verified the exact parent/tree and all seven changed paths from Git.
  Manifest rows were hashed from raw cat-file blob bytes, sorted whole-row ordinally and
  joined with LF. The result equals both candidate.json and manifest.sha256. All 34 direct
  dependency blob IDs match B. The inventory is correctly described as nontransitive.
- Root/key: the prefix uses public new_hand/apply_action/advance_street, checks actor drift,
  and supplies root.legal_decision() to BlueprintDecisionKey.from_state. That constructor
  independently checks decision equality and copies all complete history atoms, including
  returned chips. OneSeatCardState rejects overlap; board_cards rejects reversed boards.
- Capacity: encode_blueprint is the byte counter. Its uncompressed JSON consists of fixed
  metadata and positive row lengths; canonical sorting only permutes rows. Therefore the
  nested-prefix wire length strictly increases. Duplicate keys are rejected by the source.
  CHECK/null is three bytes longer than raise/2. Boundary sizes/digests and decoded key-set
  equality are implemented. No capacity result was obtained by executing this reviewer.
- Retention limit: capacity_probe returns sizes/hashes, not the boundary wire encodings.
  Design:34-35 and 50-54 say actual boundary bytes are retained. This should be reconciled
  with I-04's frozen family when correcting its plan/artifact record; hashes alone do not
  constitute retained bytes. The packet diagnostic is not retained capacity evidence.
- Production: only one hero is ranked/settled at a time; there is no full joint sealed game.
  Both forced lines settle through the integer kernel. River apply_action already creates
  showdown terminals in B, so _terminal's advance fallback is inactive on these forced
  lines. It does not change the accepted current game's terminal semantics.
- Reference: 990 distinct combination deals are supplied with literal raw weight 1.0.
  B's constructor normalizes those weights once to 1/990; collection traverses all deals.
  Explicit villain CALL and deterministic hero policies avoid uniform defaults. Forced
  values and best_response are separate evaluator calls and do not use production totals.
  B:returns obtains integer kernel net returns and converts them to floats; in s=4 they
  are 0, +/-2 or +/-4. The first-deal terminal assertions are not an exhaustive numeric
  assertion, but the frozen kernel/domain establish the other deals for s=4. I-03 remains.
- Lattice: Fraction(as_integer_ratio()) avoids a second floating tolerance. At n=990 and
  E=2^-40, 2E<1/n; checking nearest and its two neighbors identifies the unique admissible
  integer. The maximum range, reconstructed totals, production CHECK ties, best-response
  value and exact singleton legal map are checked. Wrong non-tie actions fail. NaN/inf
  cannot pass comparison. This conclusion is restricted to the fixed n/E domain.
- Phase behavior: current source contains capacity/preflight only and no full-pool launch.
  run_plan stops after its first failed comparison or pre-hand budget event. worker emits
  completed after such a return, but supervise retains the earlier failed event and turns
  the final status into failure, so that extra event is not a false-success finding here.
- Worker root: main obtains its context from begin_run(ROOT); B resolves that same ROOT.
  cwd=ROOT therefore equals the inherited root on the actual main call path. No Session is
  prepared at this checkpoint. Later Session.prepare must retain the stated equality rule;
  no current mismatch was demonstrated. The worker receives PONTIUS_RUN_CONTEXT.
- Sealed cache: cache_info() is read-only introspection of the unchanged ranker. It changes
  no sealed bytes or cache contents. It is not a sealed modification finding. Cost records
  label traced allocation separately from Job memory; the estimate is labeled an estimate.
- One-run limit: ordinary main success has one begin/finish and an output directory under
  experiments/results/runs. In addition to the concrete failures above, mkdir is outside
  main's guarded region (253), and main has no overall interruption/finalization guard.
  A KeyboardInterrupt during plan read or result preparation skips finish_run. Correct
  admission-to-finish ownership while fixing failure retention; source refusal before
  successful admission is not being counted as an already-admitted run in this review.

## Executed evidence and its limits

The supplied focused receipt reports CPython 3.14.6, the candidate commit/tree, -B -P,
a scrubbed environment and absolute PONTIUS_GIT. pytest reports two parameterized suites
passed, 44 deselected; the harness journal reports 14 unittest cases, zero skipped, exit 0,
source_verified=true. B:tests/test_pontius.py records the underlying case counts and the
per-suite outcomes, while B:pyproject.toml explicitly adds src/tests for module resolution.
The reviewed suites have nine and five test methods, consistent with fourteen.

Verified receipt SHA-256 values:

- focused-snapshot-3.14.6.txt:
  71852648acf012cac609c144d3c669390e4bcf710e89aed0e50f86f87e7235c2
- focused-snapshot-receipt.txt:
  483826946647e3c39ea7170f9400383d0f80337dcd2c73bbfdcc680f01c2e64f
- focused-snapshot-journal-line.jsonl:
  0b5b24a45f129c767ac5ef2c92cc7af7f34c8cc29e27a10c235e6976aaa7ad86
- line-budget-and-hygiene.md:
  9e2eab5288d43d5b67150cfe1fb33706c1764ae93acf72eb37c569046c335ba2
- development-diagnostic.md, expressly not evidence:
  dc8a88ac667e107b97ae0cb90b017293e560ae797644b9bf3a386f9a93c3e4b9

The corrected LF digest of focused stdout matches the handoff correction. The original
CRLF digest in the earlier table is not the current stored identity. The diagnostic's
numbers are not used to establish feasibility, teacher correctness, or retained results.
Its stated four nonzero reference comparisons cannot substitute for focused test evidence.

The real singleton checks in the tests use only the all-zero royal control. Production
checks use As Ad and Td 8d, without the nonzero singleton oracle. No executed receipt here
establishes the required nonzero four-hand singleton sample. Arithmetic fixtures cover
positive/negative residual reconstruction and +/-1/990 at lattice_integer, but the complete
validator is not exercised on both signs of the minimum nonzero gap; that limits the claim.
There is no caller-level reference-disagreement stop test. These gaps should be closed in
the next authorized focused snapshot along with the required correction controls.

The only ownership case mocks begin_run, supervise, finish_run, mkdir and write_text.
It establishes argument plumbing, not actual Job containment, inherited worker imports,
process cleanup, real result serialization or a single real journal append. No Windows
boundary receipt is supplied for the new supervisor. Passing pre-existing host tests would
not establish a new caller's failure handling. Broad suites are correctly still deferred.

The source reference bound is coherent for s=4 under the sole supported runtime; this is
not a fresh independent executable pass. Receipt source_sha256 is of actual snapshot file
bytes, allowing checkout newline conversion. The removed snapshot and retained test-result
body are unavailable in this packet, so that aggregate source hash and output hash were not
recreated from an assumed checkout layout. Candidate blob identity was verified separately.

## Review operations and disposition

Only read-only Git status/show/ls-tree/rev-parse/diff-tree/diff/cat-file, packet/skill reads,
and native PowerShell/.NET byte hashing/text checks were used. No fetch, project imports,
test execution, solver, host, tool invocation, or measurement was performed. The source
review used frozen candidate/base blobs, not uncommitted implementer files. No sibling
review, ledger, prior-round review, implementer transcript or development conversation was
read. Existing STATUS.md and execution_journal.jsonl modifications were observed by status
only and left untouched. No AGENTS.md exists in the frozen base; README identifies archived
root documents as historical rather than current development instructions.

All seven candidate paths independently satisfy LF, no BOM, no trailing whitespace and
at most 100 columns. Production counts are 297+278=575; test counts are 159+105=264.
Pinned workflow, controller-rulings and dependencies file hashes match their handoff values.
The base README/pyproject still contain old runtime wording; the explicit controller ruling
supersedes it. No 3.11 execution is requested, required or inferred from that stale text.

Specification result: Fail on the required domain, plan, ownership and retention behaviors.
Engineering-quality result: Fail on resource/cleanup failure handling; mathematical path
for the accepted s=4 domain is supported by source review and limited focused evidence.
The required next action is a scoped correction and new immutable review round with the
appropriate focused failure evidence. No implementation, integration, launch or budget
increase is authorized by this report.
