# Independent Task 2 FIX review

Reviewer: Codex evaluation_runner_fix_review, 2026-09-07. Finalizer: Codex coordinator.
Round: task2-r002, substantive FIX review of issued T2-01 and T2-02.

Verdict: CLEAN for this scoped Task 2 FIX checkpoint. No required finding remains.
Specification: PASS for the correction scope. Engineering quality: PASS for the
correction scope and inspected changed-path regressions. Design verdict: SOUND.
The shared native command boundary is the right place for executable revalidation;
the outer retained-row downgrade correctly has responsibility for invalidating its
own completion claims while preserving the already-written unit record. These small
corrections fit the existing architecture without a new source surface or framework.

This verdict binds only to candidate
07fc312e46d2def87a0016cc2c2e2e5c5b48034c and whole-row manifest SHA256
4dd5397c4606c07f61042a0fcc5325612b93a1c2d36f10fac348b43d04429c4f.
Rejected anchor: 674f82da9e044705fdaa6df46ad0a3d43b681ca9, manifest
036e0830134303e5240911216062ea588dba99893d4d5e1913a420530badcf0b.
The earlier NOT CLEAN report remains an unchanged historical finding against that
anchor. This report establishes closure on the new identity, not a revised old verdict.

## Cold-input sequence and independently recorded inventory

Read handoff first, then CLAUDE/workflow, adopted brief/design/source contract,
ADR-0508 and the Task 2 implementation brief, the explicitly issued prior review,
immutable packet source and fix.diff. Before opening coverage.md, created this
packet's attributed progress.md with the native-admission and late-downgrade
invariants, related paths, required observable controls and explicit limits.
That preserved initial inventory has SHA256
c9e81844f5a2436534da22b82545b3d97ab50f7ad2900ff7a15836f4c3a9f32e.
Only then opened and challenged coverage.md. Its recomputed SHA256 is
8dfa2eb6ecfcb6d2bfbf3b1a693d35854f7b30eb9743df6d531535bd120ca0a8.

The initial inventory is preserved unchanged. Its line ranges were approximate;
these are the precise authoritative sites in the reviewed wrapper:

- Native path admission/read identity: checked_path 43, identity 54,
  directory_ids 58, read_stable 62; SourceBinding.command 88, inventory 96,
  check 108; admit_source 128 through its pre/post-helper checks. Every wrapper
  Git subprocess.run is at line 90 and goes through command. revalidate is at
  194; trial checks are at 234, 247 and 322; publication revalidation is at 515.
- Retained downgrade: run_trial 208, inner normalization 331-337; execute 520,
  initial unstarted row 564-566, real outcome and summary copy 576-578,
  non-success cause propagation 579-580, five retained-file reads 581-584,
  exception downgrade 585-589, and reduction/result preparation 591-600.
  Observer completion/score assignment is in the unchanged helper at 549-572;
  reduce_trials is at 576-608. verify_completed/read_completed and publish's
  incomplete-result guard path are downstream consumers, not extra downgrade sites.

No implementer self-report, transcript, coordinator rationale document, or other
current reviewer findings were read. The deferred structured claim and its named
raw receipts are permitted inputs; its linked self-review/evidence-summary documents
were not opened. Two explicitly named full-run retained root/unit summaries were
also read directly to check the actual stored outcome independently of that prose.
No source/test/poker/generator/census payload was executed by this reviewer.

## Finding closure and category challenge

### T2-01 closed: native identity precedes every wrapper Git launch

The protected invariant is temporal: the saved executable bytes, file identity and
ancestor identities must still match before submitting that executable to process
creation. The guard at tools/v0a_evaluation.py:89 now calls read_stable(self.git)
and compares the complete saved tuple before line 90 can run subprocess.run.
read_stable rejects nonregular/reparse paths and checks raw bytes, file identity and
ancestor identities around the read. Initial capture is already established before
command is first called. Thus the guard covers the first HEAD query, both inventories,
cat-file, pre-helper check, post-helper check, and every subsequent check caller.
The old later checks remain; Python Popen retains its separate preceding revalidation.

The deferred census agrees with the independently traced sites. It does not confuse
initial GetBinaryTypeW admission with continued admission and does not omit Git calls
inside validation itself. I found no alternate wrapper Git launcher.

The actual tests at tests/test_v0a_evaluation_runner.py:343-424 exercise an unchanged
copied native Git with real dependencies, real admission and a subsequent check.
Three persistent post-admission schedules then change executable bytes, replace the
file with identical bytes, or replace its ancestor while hard-linking unchanged files.
Six initial-admission schedules inject byte drift immediately before each successive
command. Every schedule must reach its boundary. The recorder observes calls at
subprocess.run and delegates to the real native operation; it does not substitute
Git stdout, status, source admission or the check result. The independent requirement
is refusal and zero changed-native launches. The retained rejected-source RED records
all nine schedules violating that requirement; the unchanged control passes. Both
focused GREEN and the full suite pass all these cases on the corrected bytes.

This is finite evidence for persistent drift, not a claim of race-free executable
handles. The tests do not enumerate every possible filesystem error, initial boundary
with every drift kind, or every revalidate caller dynamically. Shared control flow
and the real drift controls justify those related sites in this bounded correction.
They do not certify DLL admission, hostile simultaneous replacement after validation,
or inherited native helpers beyond their unchanged accepted contract.

### T2-02 closed: late retention failures invalidate completion metrics

The invariant is that failed/interrupted summaries have unknown net chips and false
report/observation completeness, while preserving legitimate observed prefix data,
causes, retained lifecycle artifacts and the stop-before-later-units rule.
The catch at tools/v0a_evaluation.py:585-589 now changes precisely state, cause and the
three completion-dependent fields. Counter/capture fields remain copied from the real
outcome. add_cause retains earlier causes; an already failed returned outcome supplies
its primary/secondary causes before a later retention error is appended. Earlier
execute exceptions start from a null-score incomplete row. The unchanged run_trial
handler separately normalizes its own causes. No additional downgrade site was found.

The common catch covers exceptions from existence/read checks for intent.json,
launch.json, stdout.bin, stderr.bin and result.json. The new retained controls at
runner-test lines 427-482 trigger one OSError at stdout.bin and one KeyboardInterrupt
at result.json only after original run_trial has actually completed. They do not
fabricate an observer result. Assertions require one real completed trial and one
trigger, the appropriate root status/cause/exit code, a still-completed original unit
record, null root-row score, both root-row completeness flags false, every other
summary field preserved, eleven unstarted rows, no later unit directory, no aggregate,
incomplete pairs, guard present and completion absent.

Both RED failures are the real retained root report_complete assertion against
unchanged rejected production; GREEN reaches and passes the remaining assertions.
I separately read the two named full-run roots beneath process-temp/t2-f2-full01-311:
ev-retention-19o88m29/out and ev-retention-4aazw0bm/out. Each unit result is completed,
net 0, with applied_actions_by_kind={"fold":1}; each root row has null net and false
completeness flags, the expected interrupted/interrupted or failed/trial_failed state
and cause, zero completed trials, eleven unstarted rows, only u001, aggregate null,
a pending guard and no completion file. The final root diagnosis therefore does not
rewrite or erase the completed unit lifecycle evidence.

The two schedules are representatives, not every retained-file/error combination.
In particular, no new dynamic compound schedule combines an already failed returned
row with a later retention error, and intent/launch/stderr positions are covered by
inspection of the same loop/catch rather than separate new runs. The unchanged inner
failure controls pass in the full suite. No unmet required scenario or surviving
product defect was established by these finite limits. Final publication failures
remain their distinct Task 3 transition contract.

## Identity, scope and dependency verification

Every Git inspection used native C:/Program Files/Git/cmd/git.exe, the global
--no-replace-objects option, and exactly command-local -c safe.directory for the
repository being inspected. Verified the native file and every parent are non-reparse.
No PATH-resolved Git, source execution, external diff driver or mutation was used.

The ref refs/heads/review/v0a-evaluation-source/task2-r002 resolves to the candidate
above, with parent 34616938c708b1ca306b9d8a17b9d98e2f9e451f and tree
71d3cbb5705dffc3940c5f86f3b7ba136e2b25a7. Recomputed both candidate and rejected-anchor
manifests from binary cat-file blob output, whole-row ordinal sorting and LF encoding.
The new digest also exactly matches manifest.sha256 raw bytes. Each of the five
immutable packet files matches its candidate blob hash. diff-tree --no-renames gives
exactly the five new files relative to the candidate parent, and exactly two modified
paths relative to the rejected anchor: tools/v0a_evaluation.py and its runner test.
The production FIX is one native guard plus the two-line completion invalidation;
the test FIX adds five test methods and their finite fixture/control support.

Recomputed git diff --no-ext-diff --no-renames --unified=10 matches both review.diff
and source.diff byte for byte (SHA256
169515308521106d509a9d1d6ad75742eb16b560a534c7f8d5040d3d34623de2).
The exact anchor-to-candidate fix.diff also matches (SHA256
db326d56ec5d1b45631db020087bc4f1e8137bb2e3bbf7b03d57808df2ae08b0).
Task 1 helper/test/fixture are byte-identical to their checkpoint
b10363549ce6538574ffe34a6db691733ae2c20b. No old source, fixture, registration,
public schema or Task 3 boundary suite changes are present in this FIX.

Raw packet census: wrapper 624 lines plus helper 608 = 1232 production lines, within
the explicitly supplied controller ceiling 1250. Runner tests 577 plus contract tests
446 = 1023, leaving 777 of 1800 for Task 3. Fixture remains 20335 bytes and unchanged.
All four Python files are LF-only, BOM-free, without trailing whitespace or lines
over 100 columns. This was direct byte/text inspection, not a census payload run.

## Receipt binding, regression evidence and limits

Independently hashed and read all three permitted complete receipts:

| Receipt | Snapshot | Actual result |
| --- | --- | --- |
| t2-f2-red01-311.json | 771b11789543f90cb4aa2e20feffd2aa1ea131db | 5 tests, 11 expected failures, 59.099s, exit 1 |
| t2-f2-green01-311.json | 27ad8686af6c382d9653a6cdb6912b05596c604b | Same 5 tests, 55.357s, exit 0 |
| t2-f2-full01-311.json | f30eb99d86bf67b1052583aefb5a338b05115b16 | All 28 runner tests, 246.522s, exit 0 |

Receipt SHA256s respectively:
0f8a2fadb7d78be256c54753171a95d7a6b875fc20fb3105712513eca2947cac,
d977e488986bc1a26ab4f0cdf2ef44fa4cfe0053bcfb2836c3f62ad5e17455f1,
a05538120a902eccc508f290d96fa0a3012f286be671b1f8a15923148ce5b67b.
The issued prior review digest independently matches
a3788610d9cedcc4cca16ea4db9f62124084ce1df59c5b9a4220b82169be431c.

Verified each actual snapshot HEAD against its receipt. Focused five-file differences
from both GREEN snapshots to this candidate are empty. The RED snapshot has the same
new runner tests as this candidate and all other focused files equal the rejected
anchor; its unchanged wrapper SHA256 is
d797cd32d0ed03419c6aa931ef60e13270a7b9b585a9fe89dedd12c7a67e41af.
This binds the failures to rejected production and the passing regressions to the
exact reviewed source/test bytes rather than only to a reported commit label.

All receipts include a successful actual CPython 3.11.15/version/executable/cwd and
-B -P probe at D:/Pontius-tools/py311/Scripts/python.exe. The full receipt has the
complete 28-test output and expected root-collision refusal. Existing unchanged
controls cover real Job assignment/cleanup, descendants, overflow, timeout, interrupt,
partial capture, retained unknown launch and the public 12-trial matrix plus reader
mutants. Inspected assertions derive arithmetic from actual host stacks and verify
real retained artifacts; no profitability or substitute poker oracle is counted.

The new controls add two real sessions to the existing 12-session matrix per full
runner invocation, so this suite consumes 14 of the allowed 24. Task 3 must account
for its own starts in the integrated suite total. The receipts do not serialize the
complete parent environment, so they alone do not prove every parent scrubbed-env
variable; runner child-environment assertions remain useful but narrower evidence.
No actual 3.14.6 or whole-source integrated acceptance is claimed here.

Read-only commands completed identity/diff/hash/source/test/receipt and raw retained
summary verification. An initial irrelevant nonexistent skill-path read failed and
was followed by the correct skill read; no payload ran. Initial sandbox reads of the
two retained summaries were denied; a read-only escalation succeeded without changing
the files. Only create-new progress.md and this review report are written by this
reviewer. No source edits, test executions, subagents, commits, pushes or remote work.

Task 3 boundary/publication faults and registrations, both fresh whole-source Tier C
reviews, exact full acceptance on 3.11.15 then 3.14.6, and any source-seal/evaluation
authorization remain separate pending gates. This CLEAN checkpoint neither discharges
those gates nor authorizes a population run.
