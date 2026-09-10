# Cold review 03 - Codex

Verdict: NOT CLEAN
Design verdict: STRAINED

Candidate: 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13
Parent: beb84be566aa28029284bd35c526d33cd27af369
Tree: 09d78e4ede52a9093fc7941270d497a7362706dc
Ref: refs/heads/review/v0a-eval-panel-completion/r001
Manifest SHA-256: f58d6ed822787f0766c23ee63540ddc999784ad11d03dc103a1cbf80f68c0194
Inventory SHA-256: 361920169a9c7e092b67fcc4618a83367a7ae54a3354ac585199da40c6a7db97

## Material finding

### R03-01 - Important: malformed retained protocol values can receive successful credit

Frozen primary locations:

- src/pontius/eval_agreement.py:101-115, ready and frame validation.
- src/pontius/eval_agreement.py:152-155, the admitted v2 decision branch.
- src/pontius/eval_agreement.py:163-165, terminal interruption count.
- src/pontius/eval_agreement.py:242-245, outer counts and ordinal.
- src/pontius/eval_agreement.py:259-268, chip credit and early baseline return.

All locations refer to the candidate above, not worktree lines.

Governing requirement: accepted design section 5 makes malformed capture an unsuccessful
outcome before either chip or agreement credit. The current brief mechanism 7 similarly
excludes malformed frames. Workflow checklist 10 requires exact int/bool discipline in
evidence paths. Complete field-name equality does not establish valid field values.

Concrete v1 scenario: take the completed CHECK report constructed by the frozen
tests/test_eval_agreement.py fixture, or the completed CHECK Session report produced by the
real host test. Decode its retained child stream and change only ready.evidentiary from false
to true, null or a string; re-encode the frame stream. Leave the nested completed envelope,
source/artifact identities, actions, settlement, timing and all other frames intact.
frames_for checks that the ready field exists but never reads its value. The only evidentiary
value checks are on the final hand and closure frames. Therefore every classifier predicate
has the same result as before, and this malformed retained capture still receives chip credit
and classification='hit'. No speculative poker outcome or timing assumption is needed.

An independent authority falsifies that acceptance: the unchanged real host's
WireConsumer.ready at tools/v0a_table_host.py:729-736 requires ready.evidentiary is False.
The altered stream is not one that the actual host could accept as a completed observation.

A second member of the same boundary gap is terminal.interrupted_response_count. Replacing
its integer 0 with JSON false or 0.0 still passes line 163 because both compare equal to zero.
The frozen host instead requires an exact integer at tools/v0a_table_host.py:890, using its
integer predicate at line 43. Similar equality coercions accept true/1.0 for requested_hands,
completed_hands and ordinal at classifier lines 242-245. These are accepted malformed evidence,
not tests of different chip arithmetic.

The v2 path has a larger related omission. Starting with an otherwise successful retained v2
baseline report, remove schema_version or provider from each decision while leaving transport
pairing, timing and delivery fields intact. The classifier's v2 branch validates only delivery
agreement, so these required decision fields are never accessed. The completed baseline still
receives chip credit and exits before agreement checks. The unchanged public validator at
src/pontius/decision_provider/codec.py:44-48 requires exact fields and these identities, and the
real host calls that validator at tools/v0a_table_host.py:760. Valid baseline divergence must
retain chips; missing mandatory protocol fields must not acquire that exemption.

These are static, path-complete counterexamples from frozen source. I did not execute them:
reviewer project execution is prohibited. The retained GREEN does not contradict them; the
changed tests cover missing v1 fields, nonfinite JSON, failure types and settlement types,
but do not mutate these ready/count values or validate an actual v2 decision schema.

Required correction: validate the complete supported retained protocol before awarding outcome
credit. Preserve the intended agreement-only treatment of an unknown/relabelled reason, and
preserve chip eligibility for a valid completed baseline outside the declared root. Require
exact scalar types and required values for ready/terminal/envelope counters. For accepted v2
records, apply the actual public schema validator or enforce its full relevant contract; do not
admit v2 solely by its protocol suffix and three delivery fields.

Required verification: deterministic RED against this frozen candidate, followed by integrated
GREEN, for the ready flag and interruption-count mutations above. Include related outer/action
counter types and missing required v2 members. Mutate a retained successful real host stream
where the test claims host provenance, and keep valid CHECK-hit and valid baseline controls.
Observe the classifier result independently: malformed records must be excluded with chips null,
not successful hits or baseline chip credit. No change to the unchanged host is required.

## Design assessment

STRAINED. The teacher/export side fits the accepted shape: immutable canonical teacher bytes,
a fixed narrow game, existing codec/provider calls and explicit phases. The retention classifier
implements another partial protocol reader using a mix of exact models, untyped equality and a
special v2 branch. The finding above demonstrates multiple omitted members of one contract.
The branch for baseline preservation makes the omissions more consequential because it returns
before the later agreement reconciliation can inspect them.

Advisory engineering direction: make one explicit validated retained-outcome boundary that
separates protocol/schema validity from agreement semantics. Reuse existing public v2 validation
and typed v1 records, with a small explicit validator for the host envelope fields. Keep reason
relabeling in the agreement layer where required. This is a bounded classifier refactor and
contract-test expansion, not a reason to replace the bridge or modify host/session code.

## Independent inventory reconciliation and advisories

The inventory was exclusively written and hashed before coverage.md, operating-boundary.md or
any checks/ content was opened. Deferred claims 1-8 broadly match the independent map of plan,
teacher, codec/provider and witness paths. The admission-only receipt addresses the initially
uncertain full-prerequisite branch, including refusal of changed H, seed and resource envelope.

Deferred claims 10-13 overstate complete strict retained-frame validation to the extent named
in R03-01. Field sets and typed v1 decision construction cover many cases but do not close the
ready values, exact counters or admitted v2 decision schema. The real CHECK control and reason
relabeling are useful independent controls; they do not falsify these omitted-value cases.

A separate nonblocking retention advisory remains: completion.play holds Session.run's report
locally, then classifies it before returning; host_attempt is emitted afterward. The parent has
an attempt_scheduled observation if a worker dies during an active Session, but no incremental
child capture from that attempt. Session copies capture bytes in its finalization at
tools/v0a_table_session.py:294; completion publishes only at
tools/v0a_eval_panel_completion.py:307-311 and 338-342. The current missing-outcome accounting
avoids inventing agreement, so this review does not classify loss of an active attempt's partial
capture as a demonstrated acceptance defect. A real supervised kill during Session is a useful
future correctness control to establish the exact retained-data limit; the existing send-then-
fail test returns through Session cleanup and does not exercise that schedule.

The tie-reference path uses the existing singleton evaluator, both forced values and the exact
lattice comparison. No full-H cancellation census was run, and absence of such a tie is not
claimed by these subset checks. This limitation is correctly disclosed in deferred coverage.
The source control tests cover real CHECK/default/changed stack, transport failure, reason
relabeling and a two-hand three-phase chain; these establish their named populations only.

## Verified identity, evidence and size

- Ref, sole parent, tree and all eight changed paths independently match candidate.json.
- Manifest recomputed from raw cat-file blob bytes, sorted as whole digest/path byte rows with
  LF endings, is byte-identical to manifest.sha256 and hashes to the identity above.
- Every named inputs/ hash and D:/Pontius frozen semantic dependency hash matches its pin.
- All supporting-files.json entries, including deferred receipt files, match their SHA-256s.
- coverage.md hash:
  95578e84dc9e4d8830e9ad4bdf0744be3b46eca9c27b507b1ced756a2121899e
- operating-boundary.md hash:
  cfb1a43f88923938f3a8460b89a6db14c36539aefa65f77297c5f0bcf04267fd
- Focused receipt and journal identify this exact candidate, CPython 3.14.6 and
  source_verified=true. The journal output digest matches focused-result.json. That result
  records 78 unittest cases, zero skipped, across five registered suites; pytest reports
  5 passed, 44 deselected, exit 0. ResourceWarning and unraisable warnings are errors.
- Inspected the frozen snapshot script's scrubbed environment, explicit imports and absolute
  PONTIUS_GIT. The focused run is implementer evidence; I did not rerun it or certify broad gates.
- Initial RED receipts are explicitly incomplete in the provenance note. Existing dirty RED
  diagnostics cannot establish a frozen source identity; no missing receipt is inferred.
- Fresh raw-blob census: 2,008 production lines and 1,781 test lines for the whole Slice A surface.
  Both exceed working figures 1,200/600; production remains below the adopted 3,000 hard ceiling.
  The clarification does not require controller return for the working-figure excess alone.
- Fresh delta: 1,883 additions and 5 deletions across the eight paths. Existing game, codec,
  provider, host, session, dealer, execution and status source blobs are unchanged by this delta.
- All counted source/test blobs pass LF-only, BOM-free, <=100 columns and trailing-space checks.
  The packet's separate lint receipt reports success; I did not run a linter.

## Exposure, execution and authority limits

Inherited context contained general tool, skill, environment and workflow instructions plus
this assignment. It contained no candidate implementation, prior finding or prior verdict.
Permitted packet inputs contain historical references and the deferred implementer provenance;
no linked histories, implementation conversations, other reviews, verdicts, dispositions,
readiness files, indexes, ledgers, other packets, sibling scratch or memory sources were opened.
No unsolicited prohibited substantive exposure occurred during this pass.

Only packet reads, raw frozen Git reads and utility operations were performed. The mandated
absolute Python reports CPython 3.14.6; its first sandbox launch was denied by the OS, then
read-only utility escalation succeeded. No approval-review rejection remained unresolved.
No project code was imported or executed, no tests/host/solve/export/agreement were run, and no
source, packet, Git-ref or ledger writes occurred. The only authored files are this report and
its prior inventory in the assigned exclusive scratch directory.

This verdict does not grant broad testing, adoption, publication, retained execution or a retry.
The required malformed-observation correction remains open on this candidate. Any changed
candidate needs its own frozen identity and the applicable controller/review procedure.
