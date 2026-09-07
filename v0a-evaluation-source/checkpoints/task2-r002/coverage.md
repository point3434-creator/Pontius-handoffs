# Task 2 FIX02 final coverage for deferred independent review

This record describes the implemented correction and actual finite controls. It does
not confer CLEAN or source acceptance. Source/test writes are frozen.

## Binding and discovery

Rejected candidate 674f82da9e044705fdaa6df46ad0a3d43b681ca9; whole-row manifest
036e0830134303e5240911216062ea588dba99893d4d5e1913a420530badcf0b.
Issued task2-r001/reviews/task-review.md SHA256
 a3788610d9cedcc4cca16ea4db9f62124084ce1df59c5b9a4220b82169be431c.
Pre-edit coverage SHA256 016e3c376edc3b8848235c500cb9fc54c2d90743eeba53549fa43937f11c265a.
The coordinator accepted T2-01/T2-02 and released RED then minimal correction.
This is global source correction 2/3; one remains.

The native finding was discovered by source-order tracing: check called command
before reading the captured native identities. The retention finding was discovered
by data-flow tracing: a completed summary was copied before fallible retained reads,
and the catch changed only state/cause. Tests reproduced both on rejected production.

## Related-site census and correction

T2-01: every wrapper Git call goes through SourceBinding.command. Initial calls are
HEAD, BASE ls-tree, current ls-tree, cat-file batch, pre-load check and post-load check.
Subsequent check calls occur through revalidate before trial admission, immediately
before Popen, after capture/cleanup and before publication. The shared command now
requires the captured Git bytes/file identity/ancestor identities to match before
subprocess.run. Later source/input checks remain. The sole Python Popen still follows
revalidate and retains its unchanged suspended Job/resource/cleanup protocol. Searches
found no alternate wrapper Git launcher. No inherited host implementation changed.

T2-02: execute's shared catch covers retained intent.json, launch.json, stdout.bin,
stderr.bin and result.json existence/read failures. It now sets both completeness
flags false and net_chips null while retaining cause/state and genuine prefix fields.
Earlier execute failures start from an incomplete null-score observation; run_trial's
own cause handler already normalizes flags/score; returned failed rows are normalized.
No other downgrade site was found. Publication guard failures do not reclassify trial
summaries or permit rewriting final artifacts; their dynamic coverage remains Task 3.

## Actual exercised cases and independent oracles

NativeIdentityTests.test_unchanged_disposable_native_admits_and_rechecks executes an
unchanged disposable native Git plus copied dependencies, completes real source
admission and subsequent check. It passed RED, GREEN and full. No system file changed.

NativeIdentityTests.test_admitted_native_drift_refuses_before_execution has three
actual persistent post-admission schedules: appended executable bytes, preserved-and-
replaced file identity with identical bytes, and preserved-and-replaced ancestor with
hard-linked unchanged files. Each begins with real successful source admission.

NativeIdentityTests.test_each_initial_native_command_revalidates_captured_identity
injects byte drift after capture just before each of the six initial command boundaries.
Each case asserts its target boundary was reached. A subprocess.run recorder delegates
to the real native subprocess; there are no synthetic Git return values. The independent
oracle is refusal with zero changed-native launch entries. On RED every drift schedule
recorded changed-native launches (three post-admission + six initial-boundary failures).
On GREEN and full every schedule refused with zero changed launches.

RetentionTests.test_completed_trial_retention_fault_clears_score injects a one-shot
OSError at the execute retention read of u001/stdout.bin after a real completed
run_trial. RetentionTests.test_completed_trial_retention_interrupt_clears_score injects
KeyboardInterrupt at u001/result.json in the same after-return window. A transparent
run_trial wrapper only arms the trigger after checking actual completion; it calls the
real public runner and never fabricates observer/trial results. Both controls reuse
only the explicitly allowed zero-seed vector and exercise one real session per case.

Actual retained unit results in both schedules are completed with net 0 and observed
applied_actions_by_kind {"fold":1}. RED root diagnostics correctly stopped later units
but retained true report/observation flags and net 0. GREEN/full root rows retain every
other genuine summary field, including capture hashes/counters, while both flags are
false and net null. Fault gives failed/trial_failed/exit1; interrupt gives interrupted/
interrupted/exit130. Both assert one trigger, one completed real unit, eleven unstarted
later rows, no later unit directory/intent/launch, incomplete pairs, null aggregate,
pending guard present and completion.json absent. The original unit result remains
completed and is not rewritten. A child failing to complete cannot pass this control.

Falsifiers were observed on unchanged rejected production: bypassing the required
pre-command guard reaches the real native launch recorder; omitting normalization
fails the retained root flag assertion. The independent checks also reject an unchanged
score, unchanged second flag, erased prefix counters or any later unit/aggregate.
No additional post-fix mutation run was needed to reproduce the old defects.

## Fresh receipts and retained evidence

All receipts below are under D:/Pontius/tmp/v0a-evaluation-source-r001/run-records;
snapshots and process-temp roots with matching run names remain retained. Harness was
run-source-snapshot-v2.ps1, actual CPython 3.11.15 at D:/Pontius-tools/py311/Scripts/python.exe,
-B -P; each receipt contains the successful exact-version/cwd/flags probe.

- t2-f2-red01-311.json, snapshot 771b11789543f90cb4aa2e20feffd2aa1ea131db:
  five focused tests, eleven failures, 59.099s, expected exit1; native unchanged control
  passes. Production SHA d797cd32d0ed03419c6aa931ef60e13270a7b9b585a9fe89dedd12c7a67e41af
  exactly equals rejected production. Receipt SHA256
  0f8a2fadb7d78be256c54753171a95d7a6b875fc20fb3105712513eca2947cac.
- t2-f2-green01-311.json, snapshot 27ad8686af6c382d9653a6cdb6912b05596c604b:
  identical five focused tests PASS, 55.357s, exit0. Receipt SHA256
  d977e488986bc1a26ab4f0cdf2ef44fa4cfe0053bcfb2836c3f62ad5e17455f1.
- t2-f2-full01-311.json, snapshot f30eb99d86bf67b1052583aefb5a338b05115b16:
  all28 runner tests PASS, 246.522s, exit0. Receipt SHA256
  a05538120a902eccc508f290d96fa0a3012f286be671b1f8a15923148ce5b67b.

Focused invocation: tests/test_v0a_evaluation_runner.py -v NativeIdentityTests RetentionTests.
Full invocation: tests/test_v0a_evaluation_runner.py -v. Final source/test hashes match
that full snapshot byte-for-byte. The expected root-collision REFUSED output is its
negative control. No other payload attempt occurred in FIX02.

Coordination artifacts alongside this record:
- task2-fix02-focused-evidence.json SHA256
  15ee254bcb12f03bc81e75ead7544798ad16062f1926f4fbd0904bc48dd8b695.
- task2-fix02-final-evidence.json SHA256
  63fb899903cf6e43aa555e74a21d587b72287dc4036fbcb99788fdfcb98bc4b6.
- task2-fix02-self-review.md SHA256
  2ba66ea60be8e696234e04705da66527ee05bb11eb53079044f4d1c3465aa7dc.

Evidence inventories include exact retained root paths, real trial summaries and raw
lifecycle file hashes/lengths. Final independent launch counts: ev-matrix-e8bxid1e/out
12, ev-retention-19o88m29/out 1 interrupted, ev-retention-4aazw0bm/out 1 failed, all under
process-temp/t2-f2-full01-311. Focused runs had two real sessions each, zero matrices;
full had fourteen (one twelve-trial matrix plus two prefixes). FIX02 total18 starts;
Task2 cumulative development78. No invocation exceeded the accepted24 suite maximum.

## Scope, limits and remaining gates

Final wrapper SHA256 3a041143fb1ef7e0ac84cfb5306d619873fec3f7d8ac0079c791637e113389f5:
624 lines /32531 bytes, two net lines added. Runner tests SHA256
9fa3adcd5b350bdcfccfaba251999579e8a37d9d2d63bc7d8789c982ffd3774a:577 lines/29624 bytes.
Whole production1232/1250; test subtotal1023/1800 leaves777 for Task3. Python LF-only,
BOM-free, maxwidth100. Helper608 lines, helper tests446 and20335-byte one-deal fixture
remain unchanged. No old source, fixture, registration, Task3 or public schema edits.

Coverage concerns persistent native drift, not adversarial simultaneous replacement,
DLL admission expansion, OS crash/power loss, or new non-D child admission promises.
No fabricated successful poker/cleanup/publication oracle, entropy, extra seed/deal
selection, actual evaluation, deletion, commit, push or subagent occurred. No required
FIX02 RED is unresolved, but this is implementer evidence. Independent FIX review,
Task3 boundary/registration, whole-source reviews, actual3.14.6 and integrated acceptance
remain pending; no source seal or operating/playing-strength authority is asserted.
