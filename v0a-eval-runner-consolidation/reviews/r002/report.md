# Independent r002 focused repair review

Verdicts: **CLEAN** (specification) and **SOUND** (engineering quality), within the focused F1 repair and neighboring interruption/claim/exit behavior. No material finding confirmed. The original r001 NOT CLEAN / NOT SOUND report remains historical and unchanged. These verdicts are review evidence, not adoption, retained-run, commit, push or publication authorization.

## Exposure and authority

Before opening the packet I disclosed no candidate-specific history or prior verdict. General Pontius memory guidance was present in session context; no memory files or indexes were opened or used. The handoff then explicitly disclosed F1, and the required guide disclosed its historical verdict. This was a fresh-context opposing review, **not finding-blind**. No author conversation, controller ledger, unrelated packet or mutable author checkout source was inspected. One reviewer performed the pass without agents, using the code-verification skill.

The independent inventory was written and hashed before opening disposition.md, prior-review/report.md, or check contents. Hash-only verification of the packet preceded it as required. Inventory remained unchanged thereafter:

- inventory.md: d1cf1d349b82448f309c641420179d171e87e9a18fa1ed22878d8f859b18c8a5
- Packet manifest: f8a63b7e64bbc017d539d94c916cea5a606e10fe48f5b55ef3ca6c3aa222cf93
- Base commit: 1c7067448106cfa2aca3d57be879842d72293c61
- Base tree, verified from Git: 3d2fe79d2af20125e322dd4a668335e789810863
- Repaired launcher: 0997c186fd9441d281a14f60fb7ce1fec953048237d8bdd55ed67bf4e0b4faf7
- Retained RED launcher: 6a8a0ca080866f3441a3ff64ad13e7529a64c30ef1a8f7bb53f432388a5e1538
- Exact RED and GREEN test file: 1a0a5e9aa43b05714b592fb0f74c0d39a5562db1441a3ce6324908a1e2b958b8

All 19 manifest entries and all seven override byte sizes and hashes matched. The source snapshot came from a read-only archive of the exact base Git objects plus the seven packet overrides. No AGENTS.md was listed in the archived base tree; supplied user instructions remained applicable. The retained RED bytes were verified against this packet's manifest; I did not reopen r001 to independently reestablish that historical packet's byte provenance.

## Repair assessment and falsifier

Launcher lines 251-273 install two-phase handlers. Every observed signal enters the list; once stop_deferring changes the flag, a new signal raises KeyboardInterrupt. The finalization try starts at line 352, stop_deferring executes at 354, and the signal snapshot follows at 355. That same try covers error classification, encoding, outcome write, summary and return, with interruption caught at 369. This ordering closes F1: a signal before the transition is included in the final snapshot; a signal after the transition unwinds publication instead of silently appending after a stale successful snapshot.

The child has already exited before this window. No child-side mechanism is needed to repair the parent outcome. exit_status at lines 119-120 preserves an already nonzero child status and returns 99 for incomplete recording after child success. The interruption catch uses it and performs no outcome rewrite. Handler restoration remains in the context manager's finally block. The launcher has no claim release or retry branch; an existing record directory refuses another invocation.

The original F1 falsifier is now observed: deliver SIGINT before the outcome is opened after an otherwise successful child; the same regression that returned zero on retained RED now returns 99, reports finalization interruption, leaves no outcome file, restores the previous handler, retains the consumed claim, refuses a second invocation and launches the child exactly once. Equivalent SIGBREAK behavior and child failure precedence are covered.

No severity is assigned because no material finding remains. A counterexample returning zero for a delivered signal in the reviewed publication interval, losing an established nonzero child status there, releasing/retrying the claim, or failing to restore either prior handler under the tested single-interruption paths would falsify the affirmative verdict.

## Requirement-to-evidence matrix

| Requirement / risk | Independent evidence | Result |
| --- | --- | --- |
| Transition precedes snapshot inside catch | Frozen lines 352-369; exact regression; injection immediately after actual stop_deferring changes flag | Pass |
| Earlier deferred signals recorded as incomplete | Both signal types injected after real inventory traversal, child exits 0 and 7; outcome signals contains delivered signal, state incomplete and evidence_complete false | Pass |
| Publication interrupt cannot return zero or replace child failure | Eight exact regression subcases plus after-real-fsync and final-summary injection; statuses 99 or 7 | Pass |
| Previous handlers restored | Both SIGINT and SIGBREAK handlers checked after every additional probe; exact regression checks injected handler | Pass |
| Claim remains consumed; invocation never retried | Existing controlled-child tests and all additional probes check claim, refusal 97, one launch | Pass |
| Regression detects original F1 | Same exact test bytes run against retained RED: eight failures; repaired focused suite includes the test and passes | Pass |
| Real file publication and residual bytes correctly described | Original writer performs exclusive open/write/flush/fsync; additional probe interrupts after actual fsync and reads same unchanged JSON after return | Pass within documented process/file limitation |
| Neighboring launch/evidence/admission behavior | 35 existing launcher evidence/runner/admission cases passed | Pass on selected cases |

The regression's four child-success RED failures are return 0 versus expected 99. Its four child-failure RED failures are the missing finalization-interrupted diagnostic; child exit 7 was already preserved on RED. Therefore eight failing subcases must not be misdescribed as eight return-zero failures.

## Fresh execution

The exact repeat commands and environment are retained in commands.ps1. Runtime was C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe, CPython 3.14.6 Windows AMD64. TEMP/TMP and all fixture writes were directed below this unique scratch. Python ran with -B and ResourceWarning promoted to error. RED additionally used -I; focused and probes used -P with explicit snapshot root/src/tests PYTHONPATH plus existing D:/Pontius/.venv/Lib/site-packages for dependencies. No package installation occurred.

1. Exact RED regression: Python -I -B -W error::ResourceWarning red-source/tests/test_retained_eval_run.py RunnerTests.test_finalization_interrupt_cannot_return_success_or_replace_child_failure. **One test, eight expected subcase failures, 6.064 seconds, exit 1.** Receipt: red-independent.log.
2. Existing focused GREEN: Python -B -P -W error::ResourceWarning -m unittest -v test_retained_eval_run.EvidenceTests test_retained_eval_run.RunnerTests test_eval_completion_tool.CompletionAdmissionTests. **35 tests passed, zero skips, 18.581 seconds, exit 0.** Receipt: focused-green.log. This includes the exact eight-subcase repaired regression, prelaunch interrupt, competing callers, write/capture/evidence failures, consumed claims and bound prerequisite admission.
3. Bounded independent probes: Python -B -P -W error::ResourceWarning boundary-probes.py. **16 combinations passed, exit 0.** SIGINT/SIGBREAK x child 0/7 x deferred-evidence, stop-transition, fsync-written, summary-print. Receipt: boundary-probes.log; source retained unchanged. The signal and file writer/fixture child are real; stable seams schedule the signal deterministically.
4. Post-execution SHA256 checks: all seven snapshot overrides still match identity and all 19 packet entries remain unchanged.

The existing RunnerTests initialize and commit private disposable Git fixtures, entirely below test-temp, and clean them afterward. These are pre-existing test mechanics, not candidate/base repository-work commits. Execution used ordinary sandbox escalation for the authorized isolated check command; no denied-access retry loop or automatic review rejection occurred. check-results.json records exit statuses and environment; receipts.sha256 binds repeat commands, logs, probe source, archive and source identities.

## Outcome-file limitation

The fsync-written probe observed a successful child's already-written document still declaring verified, evidence_complete true and exit 0, while the actual launcher returned 99 and emitted FINALIZATION INTERRUPTED. For the failed child, the same probe retained file exit 7 and invocation exit 7. This directly supports guide lines 132-140: publication interruption may leave absent, partial or complete precomputed bytes; that file cannot override nonzero invocation status. The file is not upgraded or rewritten and the claim remains spent. Consumers must use both outcome and process status as the guide requires. No atomic file-plus-process-return transaction is established.

## Scope and limits

No full CPU manifest, actual console Ctrl+C/Ctrl+Break stress test, real-host compatibility campaigns or retained solve/export/agreement campaign was run in this review. The packet's affected-suite receipt reports 44 cases, zero skips, pytest exit zero and two disposable real-host campaigns; I inspected it as supporting author evidence after inventory, not independent coverage. The full prior manifest belongs to r001. The unchanged completion/protocol suites and poker arithmetic are not recertified by this focused verdict.

The probes test installed handlers via signal.raise_signal at deterministic boundaries. They do not exhaust Windows console scheduling, repeated forced interruptions, machine failures or hard kills. Signal arrival after publication during interpreter shutdown is outside the repaired publication interval. Threaded library invocation lacks main-thread-installed signal handlers by existing design; the public CLI executes in the main thread. No hostile-writer isolation, parent watchdog, parent memory bound, full-pool equivalence or playing-strength claim is made.

All review artifacts remain under D:/Pontius/tmp/eval-runner-r002-cold01-20260910/. No packet/candidate/source edit, fix, retained authorization/claim/run, repository-work commit, push, publication or controller-ledger update was performed. The repair is CLEAN / SOUND for the requested focused review; any adoption or retained invocation remains a separate controller action.