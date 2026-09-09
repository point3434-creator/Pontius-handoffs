# Cold review — review-01-codex

Defect verdict: **CLEAN**. Design verdict: **SOUND**.

No required correction was identified in the bounded fixture-launch and workload-pipe correction. This is a source-review verdict supported by the supplied focused receipts, not a broad-suite pass or adoption authorization. Acceptance criterion 4 remains partial until the registered broad harness passes after both Tier C reviews.

Reviewer: Codex, independently dispatched review-01, 2026-09-09.
Candidate: `9fce4bfba3acf1c34938aa47f37f9743e5011cea`.
Base: `d8d291cc1f813ce798f2d3a990b2a8bf2297e124`.
Tree: `6fed83eb5772da271890e1daf950f438684ec701`.
Manifest SHA-256: `d05fd7b821fec534044eeb80acdf23a4fe09767373a67e4cde20bc5ba1bed088`.
Ref: `refs/heads/review/v0a-eval-panel-verification/r001`.

## Independence and identity

Read the packet's handoff, brief and governing inputs, then frozen Git source and its complete diff. Saved `inventory-01-codex.md` before opening `coverage.md` or any checks. No implementer transcripts or sibling reports were read. The current pinned README's archived-document policy and the explicit CPython 3.14.6 ruling govern interpretation of the older frozen parent metadata.

Independently verified the ref, sole parent, tree, complete three-path no-renames diff, each changed raw blob SHA-256, and exact whole-row-sorted LF manifest bytes. Verified all 17 dependency pins against their individually stated commits, every handoff-listed supporting-file hash, and the brief and deferred-coverage hashes. Changed scope is 123 additions plus 27 deletions (150 changed lines), within the 200-line budget. Raw frozen changed files are LF-only, BOM-free, at most 100 columns and have no trailing whitespace. Rechecked the ref at the end; it still resolves to the same candidate.

## Contract findings and evidence

All locations below are in the exact candidate above.

| Requirement | Reviewed behavior and evidence | Assessment |
|---|---|---|
| Three Git fixture launch sites operate without PATH | `tests/test_blueprint_workload_session.py:24,57,92` and `tests/test_legal_river_quotient_fixed_width_device_preflight.py:30,537` bind the explicit environment executable first, require an absolute path and use it at all three sites. The supplied scrubbed receipt includes PONTIUS_GIT and excludes PATH. Existing source and Git-attribute assertions remain. | Satisfied by source plus supplied focused receipt. |
| Real worker pipes close after their users stop | `tools/v0a_blueprint_workload.py:321-354` terminates/waits for the native worker, joins each registered pipe user, then closes stdin, stdout and stderr. `table_host.Job` uses native assignment, termination and active-process accounting. Assignment failure has no started users and kills the suspended worker before closing its streams. | Satisfied on reviewed ordinary terminal paths; exceptional limits below. |
| Pipe error cannot certify success or prevent other releases | Each close has its own catch; an error is retained and keeps `streams_closed` false. The conjunction also checks real closed flags, Job activity and live threads. Final reconciliation at workload lines 371-377 forces failure when cleanup is unverified and retains late errors. | Satisfied. |
| Native observation is independent of cleanup bookkeeping | `tests/test_blueprint_workload_session.py:156-197` delegates construction to real Popen, selects the real suspended worker, and inspects its poll/closed properties before unittest cleanup. The injected stdout close calls the saved real close, then raises; actual release remains real and failure bookkeeping is observed through the returned production report. | Valid scoped oracle. |
| Existing worker, grant, result and source contracts remain | Inspected worker/grant handling, input and HEAD checks, queue draining, final status reconciliation and main retention/exit behavior. The delta changes cleanup and formatting only. Existing wrong-nonce, refusal, expiry, completion/count, late-stderr, inheritance and session-retention assertions remain. | No weakening found. |
| Consumer meaning stays consistent | The sole production caller is workload `main:464`; false cleanup becomes failed status before retention, and main returns nonzero unless completed. `execution.finish_run` retains that report/status without recertifying it. The legacy directory reader uses a separate historical result contract; current JSON reading returns the stored report. | No new consumer mismatch found. |
| Existing device-fixture assertions remain | An independent AST comparison reverses only the authorized Git binding/argv edit and finds the remaining device test module identical to the parent. Final RED and GREEN test blobs are byte-identical; RED production is byte-identical to parent. | Verified statically. |

## Supplied correctness receipts

The focused receipt names the exact candidate and a disposable snapshot. Its launch uses the absolute snapshot interpreter, `-B -P`, strict `ResourceWarning` and pytest unraisable warnings, and a scrubbed environment. The pinned snapshot script creates a fresh detached snapshot and uses `uv sync --locked --offline --group dev` with the required absolute CPython 3.14.6 interpreter, checking actual interpreter version before launch.

Focused result: pytest exit 0, four registered suites passed, 42 deselected; journal/summary report 66 unittest cases, zero skipped. These are the two changed suites plus eval-panel-tool and eval-bridge. RED result: pytest exit 1, seven workload failures specifically observe open real pipes; device suite passes. RED's journal reports 31 unittest cases, zero skipped. Receipt, summary and journal candidate/result identities agree. The supplied lint receipt reports Ruff 0.16.5 exit 0 on all three changed files.

These are inspected supplied receipts, not test executions performed by this reviewer. No project code, project tests, dependency synchronization, benchmark or retained experiment was executed. The full result artifact is referenced by hash in the supplied summary/journal but is not reproduced in the packet; this review does not claim an independent replay of its complete per-case contents.

## Deferred coverage comparison and limits

The deferred inventory matches the independently recorded core category: every supervisor-created Popen pipe and the three bare Git fixture launch sites. Its native exercised cases cover completion, input refusal, startup budget exhaustion, expired input check, assignment failure, late stderr and post-close error. No omitted ordinary cleanup branch was found that could return a successful certificate with a registered live user, open pipe or retained close error.

The initial inventory additionally called out Popen/Job acquisition failures, thread startup/join failure, kill/termination failure and interruption. Source inspection confirms these do not gain a successful cleanup certificate through the new logic. The brief explicitly excludes redesigning those exceptional paths; failures before the close loop can still skip release and remain failures. The live-thread guard itself is only statically assessed: no deterministic stalled-reader test is supplied. The close-error test proves an ambiguous report after actual release; it does not establish recovery from a physically unclosed stream or an actual OS close failure. These are explicit evidence limits, not demonstrated defects and not new required corrections.

The broad harness remains a subsequent acceptance gate under the pinned workflow. Optional dependency skips must remain explicit there. No capacity, retained-run, broad-pass, integration or publication claim follows from this review.

## Design judgment and disposition

**SOUND:** cleanup ownership remains in one supervisor, closure follows user quiescence, every stream close is independently attempted, and the certificate uses actual resource state plus failure memory. This is a proportionate local repair with no new abstraction or result schema. The conservative all-thread guard sacrifices release in an already-failed exceptional path to avoid blocking on a live buffered-I/O owner, as the brief explicitly permits.

Required corrections: none. Advisory implementation changes: none needed for this round. The named exceptional-path coverage limits should accompany downstream interpretation; they do not justify a redesign or another repair round on present evidence.

## Reviewer actions

Fresh read-only evidence used: Git status/diff/show/grep/cat-file/rev-parse; raw-byte hashing and identity validation; AST and RED/GREEN blob comparison; .NET raw-file hygiene checks. Utility execution used only `C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe` 3.14.6 with `-B -P`. Initial sandbox execution was denied; the same read-only utility was then permitted by automatic approval review. No live source edit, commit, push, hook, network publication, or sibling-report read occurred. Existing live modifications to STATUS.md and execution_journal.jsonl were observed and left untouched. Attributed outputs are staged in `D:/Pontius/tmp/review-01-codex-r001/` for exact-byte packet copy because the packet lies outside the writable workspace.
