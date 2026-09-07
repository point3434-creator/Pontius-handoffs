# Task 2 independent NEW-SURFACE review

Reviewer: Codex evaluation_runner_review, 2026-09-07. Finalizer: Codex coordinator.

Verdict: NOT CLEAN. Specification: FAIL. Engineering quality: FAIL for the two bounded
correctness findings below. Design verdict: SOUND. The split between pure observation
and a retained native runner fits the contract; these findings concern ordering and
failure-state normalization, not a need to replace that architecture.

This verdict binds only to candidate 674f82da9e044705fdaa6df46ad0a3d43b681ca9 and
whole-row manifest SHA256
036e0830134303e5240911216062ea588dba99893d4d5e1913a420530badcf0b.

## Required findings

### T2-01 — P2 / Important: revalidate the native Git identity before invoking it

Location: tools/v0a_evaluation.py:107-121, especially 108-109; related command boundary
at 88-93 and initial capture/admission at 135-149. Confidence: high from source order;
no runtime reproduction was performed in this read-only review.

A successfully admitted binding captures the Git executable bytes and path identity.
If that executable or an ancestor changes between trials, the next source.check()
first executes self.command('rev-parse', ...). That launches the current executable
at the saved pathname before the captured identity comparison at lines 120-121.
A replacement native executable can therefore run before the wrapper refuses its
changed identity. A non-native or invalid replacement is also submitted to process
creation before rejection. This is a temporal admission failure, even when the later
check prevents poker launch or final publication. It does not require a concurrent
race during a read: a persistent replacement made before check() is sufficient.

The source contract requires native regular/non-reparse paths and stable identities,
with identity checks before and after children. A revalidation operation must not first
execute the native input whose continued admission it is about to establish.

Required correction: validate the captured native executable/path/ancestor identity
before every wrapper Git invocation, including revalidation calls and the multiple
commands during initial admission after capture. Retain the subsequent source and
input checks. Verification must exercise a real admitted disposable binding, introduce
native executable/path identity drift at the allowed boundary, and independently
establish refusal before the changed Git is launched; an unchanged native control
must still admit. No stronger adversarial race-proof guarantee is requested.

Related-path inspection: all wrapper Git calls pass through SourceBinding.command;
check() is reached at admission before/after helper loading, through revalidate()
before and after each trial, and during publication. The actual poker subprocess is
preceded by revalidate(), so this finding is about Git execution inside that validation,
not a claim that the poker child necessarily starts. The accepted host Source/Job
paths were inspected as dependency context; their bytes are outside this correction
scope. test_non_native_git_refuses_before_first_git_command covers initial non-native
admission only and does not cover a previously admitted executable changing.

### T2-02 — P2 / Important: clear completed metrics when late trial retention fails

Location: tools/v0a_evaluation.py:577-587, specifically 586-587. Related outcome
normalization at 330-336, summary production at 589-600, and dependency reducer at
tools/v0a_evaluation_contract.py:549-572 and 576-608. Confidence: high from explicit
state assignments; no runtime reproduction was performed.

Concrete schedule: let u001 run to a real completed outcome. Line 577 copies its
completed summary, including report_complete=true, observation_complete=true and an
integer net_chips. Raise a one-shot KeyboardInterrupt or read failure while the loop
at 580-583 takes the retained intent/launch/capture/result snapshots. The exception
handler changes only state and failure_reason. The final root diagnostic result can
therefore contain state='interrupted' (or 'failed') alongside both completeness flags
true and an integer net_chips. publish() writes that incomplete diagnostic result
under the pending guard. Later units remain unstarted, and the reducer correctly
withholds the pair and aggregate, but the failed trial's own score and completion
claims survive.

The source contract explicitly requires net chips only for a complete trial, unknown
score for failed/stopped/incomplete cases, and observation_complete=false for
incomplete rows. The runner already implements those invalidations for failures inside
run_trial at 330-333; the outer retention exception bypasses that rule.

Required correction: normalize all downgrade paths consistently so any failed or
interrupted trial clears its score and complete-observation claims while preserving
valid observed counters as a prefix, its original causes, and retained lifecycle
artifacts. Keep later units unstarted and aggregate null. Verify with a controlled
one-shot fault/interrupt after a real completed run_trial returns, through execute()
and the actual retained root result; the oracle must assert null net_chips, both
completeness flags false, accurate state/cause, no later launch and no aggregate.
Do not replace the real observer with a fabricated successful result.

Related-path inspection: exceptions before run_trial returns start from the unstarted
null-metric row; failures inside run_trial explicitly clear the fields; a non-success
returned by run_trial carries its own normalized row. Only the exception window after
the completed row is copied leaves this contradiction. Publication failures leave
the guard and do not themselves reclassify completed trials, so they are a separate
contract. The supplied runner suite has no after-return retained-file failure control.

## Identity and scope verification

Read handoff.md, candidate.json, manifest.sha256, immutable packet source/diff,
repository CLAUDE.md and docs/workflow.md, adopted evaluation brief/design and full
source-contract.md, Task 2 brief, and the named controller ruling. No implementer
report, transcript, correction proposal, coordinator rationale or other review was
read. The three Task 1 files were dependency inputs, not reopened Task 1 review scope.

Used C:/Program Files/Git/cmd/git.exe, --no-replace-objects, and exactly command-local
-c safe.directory=D:/Pontius/tmp/v0a-evaluation-source-r001/authoring for every Git
inspection. The ref resolves to the candidate above, its parent is
34616938c708b1ca306b9d8a17b9d98e2f9e451f, and its tree is
fdd2b1293ad38ed8b68f8b643cdc32b6a23c4fa4. diff-tree --no-renames lists exactly the five
manifest additions. No old production source changed in this candidate.

Recomputed SHA256 rows from binary cat-file blob output, sorted entire row strings
ordinally and encoded with LF; the resulting manifest exactly matches both the named
digest and manifest.sha256 bytes. Every immutable packet file hash matches its raw
candidate blob. Recomputed git diff matches review.diff byte for byte. A focused diff
from receipt snapshot 91461e6e53be4e422fe6253900a97491001ada04 to this candidate is empty
for all five files. The helper/test/fixture diff from Task 1 checkpoint
b10363549ce6538574ffe34a6db691733ae2c20b is also empty.

Controller ruling SHA256 independently matches
82c997a7b7702adc5d35389b27234107177caf49c3ebf6e794597b52ea32e0d9.
It raises the production ceiling to 1250. Packet tools total 1230 lines (622 + 608);
tests total 884 lines so far; literal fixture is 20335 bytes. The four Python files
are LF-only, BOM-free, have no trailing whitespace and no lines over 100 columns.
Task 3 tests/registration remain to be counted in integrated acceptance.

## Requirement-to-evidence assessment

| Requirement/risk | Evidence and result |
| --- | --- |
| Exact old/new source and fixed loader origins | Candidate admission inventories B/current blobs, checks exact src path population and captured identities, and compiles only three captured fixed helper files. Preload/origin admission controls pass in the receipt. Required T2-01 concerns native revalidation ordering. |
| Public matrix and no parent poker imports | Source inspection plus the real 12-session zero-seed receipt control; all-seat stack resets, common physical deal, parity arm order, argv and environment, host settlement arithmetic are asserted. No profitability claim. |
| Native containment/capture | Suspended creation, Job assignment before resume, concurrent bounded raw drains and native cleanup traced against accepted Job methods. Tests retain raw partial JSON, cap each stream and observe descendant exit through real native process handles. |
| Deadline and stop behavior | Full budget plus reserve is checked before creation; trial deadline is checked during capture, after revalidation and after observation. Failure stops later units. Receipt covers expiry, timeout, late observer and interrupt. Exact-edge/final-publication faults remain Task 3. |
| Retained failure semantics | Intent precedes creation; launched remains null when launch status is unknown; failed creation and cleanup causes are retained. T2-02 violates the late downgrade schema. |
| Public reader/schema | Canonical raw records, exact field/type/count/identity checks, request/plan/result/completion hash bindings and independent aggregate recomputation inspected. Missing-arm/capture/unknown-key/identity/type mutants are rejected by the real reader. |
| Publication transition | Guard before final files, create-only fsync/close/readback, complete verification and source check before final deadline check, single postcommit guard removal. Static inspection supports the intended ordering; Task 3 must provide the named failure/ambiguous-release controls. |
| Independent negative controls | Assignment bypass actually runs an uncontained finite child and the independent marker assertion fails; partial JSON is genuinely captured/refused; missing arm and incomplete capture are mutated in fresh roots and rejected by read_completed. No replacement poker oracle is counted. |

## Receipt and verification limits

Independently hashed and read the entire permitted t2-green10-311.json receipt:
SHA256 aaf078cc2a52f6977eef4ecd005833caea6cd78ad6f166019d3127850ccc1a1f.
It records actual interpreter D:/Pontius-tools/py311/Scripts/python.exe, CPython
3.11.15, safe_path and dont_write_bytecode assertions, and the exact D-local snapshot
cwd. Its -B -P tests/test_v0a_evaluation_runner.py -v invocation exits 0: 23 tests,
185.769 seconds, full per-test output and OK. The expected root-collision refusal is
present. The receipt's version probe also exits 0. Its two records do not serialize
the complete parent environment, so that aspect of snapshot isolation is not
independently proven by this receipt alone; child environment assertions are in the
runner test. It is focused floor evidence, not fresh integrated acceptance.

No source or test payload was executed for this review. Read-only native Git identity
commands, PowerShell/.NET binary hashing, source reads and a raw line census were run.
One initial PowerShell census expression had a parse error and was corrected; it
executed no payload or mutation. An overbroad filename search encountered denied
process-temp directories; it read no reports or retained payload outputs there.

Remaining gates are explicitly outside this Task 2 checkpoint: Task 3 boundary suite
and registration work, both fresh whole-source Tier C reviews, and the complete named
acceptance population on 3.11.15 then 3.14.6. Their absence is not reported as a Task 2
omission. The two production findings above remain required regardless of those
pending gates. No source edits, payload runs, subagents, commits, pushes or remote
operations were performed. Only this create-new report and its attributed one-line
packet ledger are written.
