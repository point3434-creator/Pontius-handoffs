# Independent cold review

Verdicts: **NOT CLEAN** (specification); **NOT SOUND** (engineering quality for adoption in its current form).
One material finding: **Medium / P2, high confidence**, a recorded SIGINT can be lost during finalization, causing a false complete success. No other material finding was confirmed. This is a bounded recorder defect; it does not invalidate poker arithmetic or establish any strategy-strength change.

## Exposure, identity and independence

Initial context contained no candidate-specific history, verdict or candidate-specific memory summary. It did contain general Pontius workspace guidance. No memory files/indexes, author conversation, prior reviews, unrelated packets or mutable checkout source were opened. The mandatory source document includes author acceptance/evidence claims; those were encountered before checks as required by the handoff, and are not independent evidence. Packet checks were first opened after my independent inventory was written and hashed.

I used the code-verification skill, reviewed alone, and did not spawn agents. The user-authorized substitution of Codex for Claude changes the reviewer name only. This is exactly one independent review pass.

Authority: D:/Pontius/tmp/eval-runner-consolidation-review/r001/identity.json, base commit 1c7067448106cfa2aca3d57be879842d72293c61, tree 3d2fe79d2af20125e322dd4a668335e789810863, plus its seven raw source overrides. All 18 manifest entries and all seven override lengths and SHA-256 hashes matched. Read-only Git objects and a Git archive supplied unchanged dependencies. Snapshot source was never taken from the dirty author checkout.

Independent inventory: inventory.md, SHA-256 04bae11678559b7a4b4e9ad76df8d5d48bb91aad454f28e8d675c1434be4c00f. It was not revised after reading author evidence.

## Finding F1: deferred late signal can produce verified success

Severity: Medium / P2. Confidence: high, directly reproduced on Windows CPython 3.14.6.

Frozen location: source/tools/retained_eval_run.py:342-357 in r001, especially signals snapshot at 342, final signal check at 343, completion calculation at 345, and final outcome publication at 352. The deferred handler is installed at 250-263 and remains active across that publication because the surrounding context begins at 297.

Violated obligation: source/docs/eval-runner.md:133-135 says an observed recorder interruption withholds complete status. Lines 35 and 40-41 also require interrupted records not be upgraded to success and faults not yield a false-complete outcome. This is inventory I10 and the handoff's claim/start/capture/evidence failure question.

Reachable path: an otherwise successful child exits; attribution and inventory finish; the recorder copies `interrupted` to `report['signals']` and checks the list; a console SIGINT then arrives before outcome.json publication. Its still-installed handler appends to the live list. The report has already captured signals and completion, and no later code revisits the list, so the recorder writes and returns verified success. The same window includes outcome encoding/write/fsync and the final print. This finding concerns a signal before publication/return, not a signal after a completed invocation.

Reproduction: reused the existing RunnerTests disposable controlled-child fixture and patched only its runner write_new seam to call `signal.raise_signal(signal.SIGINT)` immediately before forwarding the outcome.json write to the original function. The real handler, file writer, child launch, attribution, inventory and outcome read all ran. No candidate bytes were changed. Exact source is late-signal-reproduction.py; the originally executed code was this same code supplied via stdin. The receipt is late-signal-reproduction.log.

Observed result: return 0; child_exit 0; state verified; evidence_complete true; recorded_signals []; errors []; exactly one launch. The injected signal was delivered while the runner's defer_interrupts context remained active and before original write_new opened outcome.json.

Handling elsewhere: the child has already exited at this stage and cannot repair its parent's outcome. The recorder has no postpublication signal reconciliation. Unchanged base tools/v0a_eval_panel.py explicitly restores its own normal handler before finalizing its cleanup certificate; that separate child mechanism does not protect this parent window. The existing prelaunch signal test covers a different boundary and passes.

Consequence: an operator interrupt during recorder finalization can be silently omitted from the record and reported as a complete, successful invocation, contrary to its operational contract. The claim remains consumed and underlying phase evidence is not shown corrupted; impact is the false recorder completion/interruption attestation.

Smallest remediation direction: establish a deliberate finalization boundary that does not continue silently deferring newly observed signals while publishing a precomputed success certificate. Preserve child nonzero status precedence and one-shot claim behavior. Include a deterministic regression at the prepublication boundary. No fix was made.

Falsifying observation: with the same SIGINT delivered before outcome publication, the invocation must not return successful complete status; it must report interruption/incomplete evidence or unwind without a successful completion result. A signal delivered after the invocation has completed would not substantiate this finding.

## Requirement-to-evidence results

| Inventory | Result and evidence |
|---|---|
| I01-I03 identity/authorization/ownership | Pass within documented operator ownership. Recorder 175-247 binds document, launcher, plan, source HEAD, input digests, baseline and modes; retained authorization precedes claim. Child begin_run in frozen base execution.py independently hashes source. Focused negative cases passed. No authentication or hostile-writer isolation is inferred. |
| I04-I05 exclusive claim/start | Pass. mkdir of claim.d is exclusive after both callers may preflight, retained on failure, no retry/removal branch. Two-callers barrier and start/capture failure cases passed. |
| I06-I09 exit/evidence/attribution/inventory | Pass for reviewed paths. launch records child exit before capture flush; nonzero precedes evidence failure. Exact raw appended row, source/result/runtime hashes and exactly its new run directory are required. Recursive scandir/context-managed file reads propagate failures; links/reparse entries/nonregular files refuse. Focused checks passed. Late signal defect is separately I10. |
| I10 interruption | Fail, F1. Existing prelaunch test passes; newly reproduced prepublication interval does not satisfy the contract. |
| I11-I12 admission/phase chain | Pass for changed surface. Exact diff only replaces fixed prerequisite digests with prerequisite names and removes fixed solve envelope. Full count/board/names/status/cleanup/phase/capacity permutation/preflight sample checks remain. Raw bound bytes still checked. Producer phase/scope/prerequisites/permutation/artifact checks and completion arithmetic are unchanged. Alternate prerequisite/resource and changed-byte rejection test passed. |
| I13 runtime/environment | Pass for executed scope. CPython 3.14.6, sanitized child environment and real temp creation. Standard-library runner, no independent parent Job/watchdog or memory bound asserted. |
| I14 compatibility scope | Supporting author evidence only. Inspected test before receipts: one/two hands, fixed teacher totals, export teacher identity/membership, host primary hits and controls/accounting. Test intentionally uses base child source plus new runner; it does not exercise changed full-plan admission in a real campaign. Full-plan admission is separately tested. Claims fairly limit conclusions to these hands, not full-pool equivalence/playing strength. |
| I15 findings discipline | F1 traced to reachable parent path, explicit obligation, absent protection elsewhere and direct reproduction. No speculative adjacent issue promoted to finding. |

## Executed checks and receipts

1. PowerShell Get-FileHash manifest/override verification: 18 manifest entries, seven lengths/hashes, no mismatch. Git rev-parse of base tree matched identity.
2. Read-only Git archive created base-source.zip from the exact base for src, tools, tests, pyproject.toml, .gitattributes and README. Applied the seven raw overrides under this private scratch snapshot. Git no-index comparison confirmed the narrow completion, completion-test and README deltas. No candidate or base repository commit was created or changed.
3. Existing focused suites on Python 3.14.6: EvidenceTests, RunnerTests, CompletionAdmissionTests. **34 tests passed, zero skips, 9.468 seconds; process exit 0.** Receipt focused-checks.log. Existing RunnerTests create temporary fixture Git commits as part of their pre-existing setup, entirely inside test-temp and cleaned by the fixture; no candidate/base/history commit or push occurred.
4. One bounded finalization-signal diagnostic using that existing fixture: command exit 0, reproduced F1's return-zero/verified behavior. Receipt late-signal-reproduction.log and exact reproduction code retained.

Execution environment: C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe; `-B -P -W error::ResourceWarning`; cwd private snapshot; TEMP and TMP set to scratch/test-temp; PONTIUS_GIT C:/Program Files/Git/cmd/git.exe; PYTHONPATH snapshot, snapshot/src, snapshot/tests, and existing D:/Pontius/.venv/Lib/site-packages. The focused command loaded the three named classes through unittest.defaultTestLoader and used TextTestRunner(verbosity=2). Exact repeat commands are in commands.ps1. No package installation occurred.

Initial sandbox probes of both venv launchers and base Python returned access denied. These were environment failures, not candidate failures. The authorized isolated Python runs then succeeded with sandbox escalation. No automatic approval rejection occurred.

Author receipts, inspected after inventory: pytest-final.log reports 49 passed/2 skipped in 257.11 seconds; pytest-result.json reports 665 unittest cases/10 skips; compatibility-green.log reports its single two-campaign test passed; low-memory receipt preserves child exit 1 and failed state with complete evidence, including OpenBLAS allocation stderr. These are supporting author receipts, not independently rerun results. Claimed development RED history is not independently retained proof.

## Limits and disposition

No full CPU manifest or real-host campaigns were rerun solely to reproduce author receipts. No full-pool run, strength improvement, hostile-writer isolation, global lock across distinct bindings, power-loss durability guarantee, or independent parent resource bound is established. Filesystem fault tests use controlled seams; they do not exhaust every Windows kernel/filesystem failure. The late-signal diagnostic is deterministic injection at an actual asynchronous boundary rather than a physical Ctrl+C stress campaign.

All review outputs are under D:/Pontius/tmp/eval-runner-cold01-20260910/. No candidate, packet, historical packet, retained authorization, retained claim/run, or controller ledger was edited. No retained invocation, adoption, commit/push of repository work, fix, publication or authorization was performed. The report does not grant retained-run authority. F1 is an executable-behavior finding requiring remediation and focused verification before an affirmative adoption verdict.
