# Task 1 independent source review

Reviewer: Codex /root/evaluation_contract_review, independent of implementation.
Date: 2026-09-07. Round: NEW-SURFACE, task1-r001.
Scope: pure contract checkpoint before native implementation. This is not an integrated
Tier C acceptance pass or a source seal.

Verdict: **NOT CLEAN**. Specification: **FAIL**. Engineering quality: **FAIL** on
one bounded observation-accounting defect. Design: **STRAINED** in the event observer;
the overall pure-helper/public-subprocess split remains appropriate.

## Binding and independently verified identities

- Repository: D:/Pontius/tmp/v0a-evaluation-source-r001/authoring.
- Ref: refs/heads/review/v0a-evaluation-source/task1-r001.
- Candidate: 55b1f5f75f7bcdf8061a2a02906a86769345715d.
- Parent/base: 34616938c708b1ca306b9d8a17b9d98e2f9e451f.
- Candidate tree: 1dabb73de6d0ff69a509b750789dcd21b8251776.
- Manifest SHA256: c15299d1d6cbf53e0660fcd24e91f488e228735135b97a0ce467882eee089cb6.
- Final floor-test snapshot: 1f0f4c1e619eaa5a7137139be0b96293e9b235e1.
  Its actual HEAD and tree were resolved independently in the snapshot repository;
  its tree equals the candidate tree above. All three snapshot files also equal the
  packet raw files byte for byte.

Raw candidate blobs were read through native Git cat-file, compared byte for byte
with packet files, and hashed independently. Reconstructed sorted whole digest/path/LF
rows equal manifest.sha256 exactly, including the manifest hash. Git diff-tree shows
exactly the three additions. A fresh binary Git diff equals review.diff byte for byte.

| Path | SHA256 | Bytes / lines |
| --- | --- | --- |
| tools/v0a_evaluation_contract.py | 4197281f2cd8780a106fabd26abf55c320fd19ae4417d25fc1f1db8b8d9eacf7 | 35158 / 603 |
| tests/test_v0a_evaluation_contract.py | 725dd62407e0dc69c4252303001b9335d6b801fe7c05abe70273fa5be9b98b21 | 22828 / 389 |
| tests/fixtures/evaluation/controls.json | 9204a8aec4a4d6558381b246385495201d64c33e67732e2d3ab21feed31c7eea | 20335 / 634 |

## Required finding I-01: rejected event rows can change retained observations

Severity: **Important** (bounded incorrect diagnostic accounting). Confidence: **high
from direct source-path tracing**, not an executed reproduction. Location:
tools/v0a_evaluation_contract.py:437-455 and 476-488; public observe_trial output.

The accepted source contract requires schema/identity-valid event observations only,
retention of the valid prefix preceding a malformed row, and refusal of conflicting
copies without counting them as two incidents. The observer appends to failures and
seen at lines 444-449 before checking same-action timing conflicts at 453-454. The
exception handler breaks parsing but does not undo these mutations. The result then
publishes the mutated failures list at lines 521-523. Consequently refusal of a row
does not prevent that row from contributing an action failure.

Concrete finite scenario using the existing literal fixture, without any new deal:

1. Use the failed blueprint-v1 fixture, ready plus failed_event_v1, with outer/hand
   child_failed and exit 1 as in the existing failure tests. The valid first failure
   has event_index=0, action_index=1, delivery_rejected, interrupted timing with
   last_valid_observation_ns=1.
2. Append a copy of that event. Set both its outer event_index and its failure's
   event_index to 1. Keep hand_id/action_index/code/delivery unchanged. Change only
   the copied timing's last_valid_observation_ns to 2. This remains individually
   valid interrupted timing, but conflicts with the earlier timing for this action.
3. The second row passes the local schema and identity checks. Its new event index
   creates a different seen key, so a second action_failures entry is appended.
   The timing key is still the same (hand_id, action_index); conflicting_timing then
   raises. The final result is refused with that deficiency, but action_failures
   contains two entries, including one originating in the refused conflicting row.

Required outcome: preserve the first valid unverified failure only; report the conflict,
leave observation_complete false and net_chips null, and do not admit the second row's
failure, source labels, selection counts, timing or attribution effects. Refusing the
trial already prevents a paired score, but does not repair its published diagnostic
prefix. Honest failed-trial observations are an explicit deliverable of this task.

Related locations share the same cause: seen source labels change at 442 before later
checks, and selected/legacy/decisions change at 480-484 before the timing check at
486-487. A later conflicting row can therefore affect additional observation fields.
For example, a failure-only v1 row may establish timing for action 1; a following action
frame and decided event for action 1 can pass local checks with different timing,
insert the decision/legacy count, then fail the timing comparison. That rejected
decision remains available to the final host-action attribution loop. The row-local
validation/commit boundary needs to cover these related updates, not just list append.

Required correction: make all output-visible observation changes conditional on the
whole row passing relevant local and cross-row conflict checks. Preserve prior accepted
observations on rejection. A small staged row delta or validation-before-mutation
reordering is suitable; a new framework or engine reimplementation is unnecessary.
The choice of technique is advisory; the stated output invariant is required.

Required verification: before changing production bytes, run a deterministic RED in a
fresh authorized floor snapshot against this frozen candidate using the above exact
finite scenario. Assert the entire retained action-failure prefix is the single first
entry, the conflict is retained, and no score is produced. Also exercise one late
conflict on the decision/selection/attribution path, asserting that all those metrics
remain those of the preceding valid prefix. GREEN the corrected pure suite in its
fresh snapshot, retaining existing matching-copy/source-label/null-identity controls.
These checks require no poker, generator or additional full deal. Freeze corrected
bytes in the next round; this issued finding and rejected candidate remain immutable.

## Requirement and evidence assessment

| Requirement / risk | Inspection and finite evidence | Result |
| --- | --- | --- |
| Strict request and bounded input | Exact keys/types, canonical re-encode, duplicate/depth/size/digit rejection, lineup and reserve checks; literal refusal tests | No material issue found |
| Matrix and matched population | d/l/r order, fixed physical cards, six seats, per-deal button, ordered opponents, paired bytes/hash, alternating arm IDs; literal 6/12 and bounded 24/48, 96/192 cases | No material issue found |
| Full denominator and integer sums | Every planned pair and both strategies required; literal [4,-2] vs [1,3], deltas [3,-5], aggregate -2/2; missing/duplicate/failed/incomplete/cleanup cases | No material issue found |
| Versioned wire and identity | Full v1/v2 field lists inspected against unchanged host/session, v0a model, provider model/codec; wrapper and child manifest distinction preserved | Substantial checks present; I-01 limits accepted observation claims |
| Host-applied actions and fallback | Bot/seat equivalence, action ordinals, nth decision/action match, separate baseline/legacy counters and unknown attribution | I-01 affects rejected-row metrics |
| Failures and timing | Failure schema/null identities, same-frame source coalescing, complete/failure copies, timing deduplication and outer timeout distinction | FAIL: I-01 |
| Completion and settlement | Exit/status/capture/cleanup, close ordering, chip conservation, nested equality and next button; no score on incomplete/refused trial | No material issue found within helper scope |
| Finite tests | One manually specified full deal, synthetic versioned frames/reports, six named in-memory mutants | Appropriate bounded controls, but existing conflict tests miss the late-mutation case |
| Native ownership/publication | Not implemented or claimed at Task 1 | Deferred, not passed |

The v1/v2 fixture schemas and provider relationships were checked against the accepted
B source rather than treating the synthetic success fixture as an engine oracle.
The copied timing/failure and provider field/domain checks substantially match those
sources. No solver, game legality reconstruction or generic additional population is
requested. No separate coverage-only finding is added: the targeted missing conflict
check belongs to I-01 and its required verification.

## Engineering and design judgment

**STRAINED**, locally. observe_trial mixes admission, sequence validation, duplicate
comparison, mutable metrics and summary publication inside one loop. The concrete
mutation-before-final-check sites above demonstrate the failure mode that shape invites.
A bounded per-row validate-then-commit boundary would make prefix preservation explicit
at small local cost. Preserve the existing pure-helper boundary, immutable B schemas,
finite fixture population and production budget. There is no basis here for replacing
the whole helper, expanding scope or reopening the accepted architecture.

Opposing evidence: the implementation already fails the whole trial closed, retains
many valid incomplete prefixes, and its six source mutants exercise independent
matrix/denominator/action-cause assertions. The finding concerns correctness of the
retained refused-trial observations; it does not establish false completed-pair scoring.
Largest unknown: the later native wrapper and full integrated acceptance are not in
this packet. Cheapest falsifying check for I-01 is the exact fixture-only RED above.
If that frozen public output retains only the first valid row with unchanged metrics,
reassess this static finding before implementing a correction.

## Review method, commands and limits

Read handoff first; then governing CLAUDE/workflow, accepted source contract in full,
brief/design, Task 1 requirements, ADR-0508 and relevant project boundary/evidence
sections. Inspected all three raw files and review.diff. Did not read author reports,
coordinator/implementer transcripts, other reviewer conclusions or rationale packets.
No source edits, tests, poker/generator/census execution, subagents, commits or pushes.
Only create-new attributed review/ledger records were written.

All Git commands used C:/Program Files/Git/cmd/git.exe with --no-replace-objects and
command-local safe.directory equal to the exact repository being inspected. Operations:
rev-parse for candidate/ref/parent/tree and snapshot HEAD/tree; diff-tree for scope;
cat-file blob plus binary-stream SHA256 and byte comparison for raw files; binary diff
comparison for review.diff. Get-Content/rg supplied source inspection; .NET SHA256 and
byte comparisons supplied independent identity checks. The read-only identity checks
above passed. An initial equality check against unchanged working source bytes stopped
on checkout EOL differences; follow-up verified B/candidate blob equality and inspected
text equality after checkout CRLF normalization, without modifying any file. The new
three-file candidate and snapshot comparisons were raw byte comparisons, not normalized.

Unchanged B/candidate blob identities independently resolved:

- tools/v0a_table_host.py: 6ec8a162b053158203663c48e82314b10750f962.
- tools/v0a_table_session.py: a5e058260fa56e29f06e38074d59dc55f420c5ee.
- src/pontius/v0a/model.py: 3602989e3a3d5f36c9a0bd5d102797b8e349191d.
- src/pontius/decision_provider/model.py: 6cce376e73594a6836d146cd53022fdb250a04f5.
- src/pontius/decision_provider/codec.py: f5795bc1d7f723a569b76732cf195b2ef9d69eaf.
- src/pontius/legal_decision_spine_v2.py: 824f4938788769be4165dcad04926bf9f2ec22e8.

Read the permitted raw receipts task1-red-contract-311, task1-red-prefix-311 and
 task1-green-final-311. They retain respectively 16 missing-helper failures, two
behavioral prefix/ordinal failures among 18 tests, and 21 passing tests on actual
3.11.15 with -B -P and the named final snapshot. The final run's tree and raw three-file
snapshot binding were independently verified. This review did not rerun that suite;
its recorded 21 passes do not cover I-01 or replace later integrated acceptance.
Full source acceptance still requires two fresh Tier C CLEAN reviews and all sixteen
specified commands on actual 3.11.15 then 3.14.6 under the accepted snapshot procedure.
