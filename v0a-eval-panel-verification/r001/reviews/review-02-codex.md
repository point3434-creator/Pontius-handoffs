# Review 02 — Codex — v0a-eval-panel-verification/r001

Defect verdict: **CLEAN**.
Design verdict: **SOUND** for the bounded cleanup/fixture correction.

Candidate: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
Base: d8d291cc1f813ce798f2d3a990b2a8bf2297e124.
Manifest SHA-256: d05fd7b821fec534044eeb80acdf23a4fe09767373a67e4cde20bc5ba1bed088.
Reviewer: independently dispatched Codex review 02, 2026-09-09.

No demonstrated Important or Critical defect remains in the reviewed correction. No required source correction is identified. This is a cold source/evidence review, not a broad-test pass or adoption authorization.

## Independence and review boundary

Read handoff, pinned current README (including its archived-document policy), brief, authorization, workflow and dependency inventory. Reviewed raw candidate/base Git objects. Recorded inventory-02-codex.md before opening coverage.md or any checks/ file. Did not read implementer transcripts or sibling reviews. No project code or tests were executed; no live source, test, dependency, ref or lifecycle file was modified. Existing STATUS.md and execution_journal.jsonl worktree changes were preserved and excluded from review.

The full supervise allocation-to-return path, worker protocol, main/status/output consumer, execution source boundary, native Job methods and relevant session/report callers were traced. The review scope remains the three authorized changed files and their affected contract, not a new audit of every historical research component.

## Findings and design assessment

The correction has one clear owner: supervise creates the pipes, terminates/waits for the native worker, joins the registered users and then releases its streams. At frozen tools/v0a_blueprint_workload.py:329-353, a live registered thread prevents stream closure and certification. Otherwise each stream gets its own close attempt, and each Exception leaves streams_closed false while preserving its diagnostic and allowing subsequent streams to be attempted. Both observed closure and native Job/thread checks are required for certification. Final status processing at :371 rejects a false certificate and rejects completed status when errors remain.

This is a SOUND local repair: the lifecycle and authority remain in the existing supervisor, with no new ownership abstraction or parallel success bookkeeping. The all-thread guard is conservative and readable. Termination/wait/join exceptions retain the existing failure behavior; the change does not claim successful cleanup for them. Broader restructuring of exceptional acquisition or asynchronous signal handling is not warranted by a demonstrated defect in this packet.

The Git fixture change is bounded and consistent: tests/test_blueprint_workload_session.py:24-26 resolves and validates the absolute executable before its setup/add launches at :57 and :92; tests/test_legal_river_quotient_fixed_width_device_preflight.py:30-32 does the same for check-attr at :538. A supplied nonempty PONTIUS_GIT takes precedence, so the required no-PATH environment never invokes shutil.which. Existing fixture assertions remain intact.

## Requirement-to-evidence assessment

| Requirement | Evidence and result |
| --- | --- |
| All three fixture Git launches work without PATH | Three candidate call sites use validated GIT. Pinned snapshot runner clears the environment and supplies absolute C:/Program Files/Git/cmd/git.exe. Focused receipt and verified result show both affected fixture suites pass. |
| All three real worker pipes close after their users stop | Source lifecycle trace plus seven supervisor observations using actual Popen objects; process.poll and each stream.closed are asserted before unittest cleanup. Completion, input refusal, startup budget, expired check, assignment failure, late-error handling and close-error paths pass. |
| A close failure is retained and cannot certify success | Native close-error case saves and calls the real stdout.close, then raises OSError; real process and all stream closure assertions remain active. The test requires failed status, false certificate, retained error and two completed cells. Source catches each close error independently. |
| Existing statuses, grants, source and result checks persist | Controller nonce/order, HEAD/input checks and budget handling are unchanged; source-boundary and worker cases pass. Eval bridge and eval-panel suites also pass in the supplied focused selection. Final main/finish_run consumers preserve failure status. |
| Strict locked supported-runtime verification | Snapshot runner uses uv sync --locked --offline --group dev with the pinned absolute interpreter, asserts 3.14.6, runs -B -P, clears PATH, sets ResourceWarning and pytest unraisable warnings to error and disables cache output. Receipts and result hashes are consistent. The broad registered harness is still an outstanding downstream gate. |

The native observer at tests/test_blueprint_workload_session.py:156-190 delegates construction to saved real Popen and observes returned streams directly. Its cleanup callbacks execute after the assertions. The injected failure represents an ambiguous release report after a real close; it is an independent check of certificate failure, not evidence that an ordinary OS close failure has been reproduced. The inherited late-stderr test supplies its trigger through a scheduled thread wrapper and synthetic error stream; it establishes late-error bookkeeping, not arbitrary OS stderr timing.

## Independent frozen identity checks

Executed the review utility using C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe -B -P; its asserted and printed interpreter is CPython 3.14.6. The initial sandbox launch could not start that executable; the same read-only utility succeeded with approved escalation, exit 0. It imports standard-library modules only, reads raw Git objects and packet/snapshot result files, and does not import or execute the project.

Verified:

- Ref resolves to the stated candidate; candidate has exactly the stated parent and tree 6fed83eb5772da271890e1daf950f438684ec701.
- Exactly the three scoped paths changed, with 123 insertions and 27 deletions: 150 changed lines, within the 200-line budget.
- Manifest bytes equal freshly computed SHA-256 blob rows sorted by whole row with LF; manifest digest exactly matches the bound identity.
- All 17 dependency pins match raw blobs at their own stated commits, including current README/workflow from b6f8b08 rather than treating the frozen parent's older runtime configuration as governing.
- All 18 pinned supporting files, brief and deferred coverage match their published SHA-256 values.
- All changed blobs are LF-only, BOM-free, at most 100 columns, with no trailing whitespace.
- Final RED production workload blob is byte-identical to base. Both RED test blobs are byte-identical to GREEN. Device test AST is identical to base after reversing only the authorized Git-resolution edit.
- Pinned focused/red result summary identities match their journals, and the actual snapshot result bytes match their recorded output SHA-256 values.

## Supplied execution evidence and limits

GREEN: candidate 9fce4bf..., exit 0; 4 registered pytest suites, 66 unittest cases, zero skips: device fixture 15, workload session 16, eval bridge 11, eval panel 24. Focused stdout reports 4 passed and 42 deselected. Stderr is empty. Supplied Ruff receipt records exit 0 for the three changed files; lint was not rerun by this reviewer.

RED: 5815bfaefdb74de85a0d9aa78a2af4013d78fde9, exit 1; 31 unittest cases, zero skips. The seven affected native supervision cases fail on the independent open-real-pipe assertion; no unittest teardown errors occur. The device fixture suite passes. This is a useful regression comparison for the leak correction. Because the fixture Git correction is present in both final RED and GREEN, this RED is not a pre-fix regression demonstration of the Git executable issue; GREEN under the required scrubbed environment supplies its direct evidence.

Compared the saved inventory against deferred coverage. They agree on all three pipes, fixture launches, native ownership, status/certificate consumers and seven exercised cleanup paths. Coverage explicitly acknowledges that no deterministic live-reader stall case was added. A failure before real close, partial startup failure, join/termination failure and asynchronous interruption are not independently exercised by these new observations. Source inspection supports the registered-live-user and close-error failure predicates, but these tests do not prove OS cleanup for every exceptional path. Those are transparent coverage limits, not demonstrated defects or a reason to invent a redesign requirement.

The full registered broad harness remains required after both independent Tier C verdicts. No broad pass, retained experiment, performance/capacity conclusion, integration, commit or publication is established by this review.
