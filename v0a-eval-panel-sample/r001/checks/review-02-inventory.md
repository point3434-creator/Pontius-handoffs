# Independent inventory — Claude cold pass on v0a-eval-panel-sample/r001 and
# v0a-eval-panel-ownership/r002

Recorded before opening coverage.md, checks/ contents, inputs/*disposition.md
or inputs/repair-plan.md of either packet. Built from frozen blobs only:
tools/v0a_eval_panel.py and tests/test_eval_panel_tool.py at 72954e13 (sample)
and d8d291cc (ownership, the combined source), the diffs 182d14e2..72954e13 and
72954e13..d8d291cc, BASE src/pontius/execution.py (finish_run) and BASE
tools/v0a_table_host.py (Job) at f647a798.

Disclosure: a status check at session start tailed progress.md (ls + tail -3)
before this review began and exposed the ledger lines for ownership/r001,
sample/r001 and ownership/r002 including the sibling verdicts (Codex CLEAN on
both). No review file, disposition, coverage or check content was opened.

Identity (verified from Git objects before this inventory): sample/r001 =
72954e13, parent 182d14e2, tree 73797f3b; ownership/r002 = d8d291cc, parent
72954e13, tree 2b542a78; each changes exactly tools/v0a_eval_panel.py and
tests/test_eval_panel_tool.py; both manifests recomputed from raw blobs match
the packets byte-for-byte; src/, tests/test_eval_bridge.py, fixtures and
cases.json are unchanged since 0bc19bca (r004). authorization.md pinned digest
b88a1621… matches in both packets.

## Sample contract (r001 D → r003 I-02 → r004 C; second residual)

Invariant S1. There is one admitted, role-bearing, canonical schedule; the
worker executes it and the estimator reads it. Nothing rebuilds it from the
raw plan lists.
Invariant S2. declared-full admits exactly {development×4 on 2c7d9hJsQc,
control×1 royal 2c3d} by (role, board, hand); any role movement, substitution,
duplicate, board change, malformed or board-overlapping hand is refused.
Invariant S3. A completed declared-full run has exactly the four development
records complete and agreeing, named as the estimator expects; otherwise no
estimate and no "completed".
Paths: validate_plan → AdmittedPlan(wire, schedule); ScheduledHand.record_key;
run_plan (admitted.schedule); worker re-validation from the wire; drain record
key (label, board names, hand name); complete_sample; full_pool_estimate;
supervise status finalization (sample_complete); main.

Frozen-source reading: S1 holds — AdmittedPlan is returned by validate_plan,
accepted as-is on re-entry, run_plan iterates admitted.schedule, the parent
sends admitted.document and the worker derives the same schedule from the same
wire deterministically; complete_sample keys records by ScheduledHand.
record_key and full_pool_estimate consumes complete_sample. S2 holds — set
equality on role-bearing ScheduledHand tuples plus distinctness on (board,
hand) plus plan.board == DEVELOPMENT_BOARD. S3 holds — complete_sample returns
None on any unexpected, duplicate, incomplete, stage-missing or non-passing
record, and supervise demotes "completed" to "failed" when sample_complete is
false. Record naming: hero is the sorted card tuple, hand_name → "AdAs",
"KdKh", "8dTd", "3c4d"; estimator key uses the same function on the same
tuple. No defect found.

## Ownership contract (r001 A → r003 I-01 → r004 A, B; second residual)

Invariant O1. cleanup_verified is true iff every release attempt succeeded
(including the final job close and any console interrupt) AND the resource
state was observed released; it is decided after the last release and can
only be false once any attempt fails.
Invariant O2. Every drained observation is reachable from the caller-owned
report at the moment it is drained; no local accumulation.
Invariant O3. A console interrupt at any instant between resource acquisition
and the last release never unwinds past a release; it is recorded and the
remaining releases run.
Invariant O4. Every release attempt is bounded (wait, join, stream close).
Invariant O5. main records exactly one result and one journal row for
completed, failed and interrupted, with the owned observations.
Paths: defer_interrupts; supervise acquisition order (Job → Popen → assign →
threads → resume); loop exit conditions; attempt/verify/join/close_stream;
certificate computed after the with-block; status finalization; main.

Frozen-source reading: O1 holds — resource_state_verified is set only by a
successful verify, the certificate is computed after "close job" and after the
handler is restored, and is the conjunction with all(value == "ok"); the
console-interrupt entry is not "ok". O2 holds — drain appends the record to
observations on first receipt and mutates it in place; hands is gone. O3 holds
on the main thread — SIGINT is recorded, not raised, inside the with-block; the
loop and the post-acquisition check observe status. O4 holds — shared 10 s
cleanup deadline for joins and closes, close via an owning daemon thread with
a bounded wait, process.wait(timeout=10). O5 holds — report is main's dict.

Candidate concerns to verify (not yet findings):
C1. defer_interrupts uses None both for "not main thread" and for
signal.getsignal returning None (a handler not installed from Python); in the
latter case the deferring handler is never restored and the process stays
un-interruptible after supervise returns. Reachable only with a C-installed
SIGINT handler; not the tool's own entry.
C2. retain_boundaries runs after supervise with the normal handler restored; an
interrupt inside the reconcile finally (read_bytes/compare/assign) leaves a
published final-name file with publication state "publishing" and no
boundary_artifacts entry. The identity was registered before the rename so
nothing is lost and the state is honest; the retention label still says
"recoverable encodings remain", which is true. Advisory at most.
C3. receive_errors has no exception guard; a non-UTF-8 byte on the worker's
stderr kills the reader thread and loses the remainder of the diagnostic
stream (join still succeeds). Pre-existing since r001; diagnostic, not
observation.
C4. A console interrupt after the with-block exits and before the certificate
store unwinds supervise with cleanup_verified left at its initial False —
intended per the comment; observations are owned. Consistent with O1/O2.

## Retention contract (r003 I-03 → r004 D; first residual)

Invariant R1. A boundary artifact's identity (path, bytes, sha256) is in the
result before the file can become visible under its final name; a completed
final-name file is never unbound or mislabeled as unwritten.
Reading: publications[count] registered with identity before write; state
pending → publishing → bound; finally reconciles by is_file + byte compare.
Holds, modulo C2's narrow window inside the reconcile itself.

## Tests inventory (from the frozen test blob)

Admission: role movement ×2, all-controls rebound board; the r004 negatives
kept. Worker: capacity retention round-trip; second-write failure + retry;
estimator fixture labeled as fixture; stage emission; budget; json_safe.
Real supervisor: completion (all cleanup ok), fault at active+join, interrupt
at wait (now asserts cleanup_verified false), assignment refusal, budget kill.
Ownership (fake supervisor): completed, 1e999, interrupted-with-preloaded.
RealRunOwnershipTests (disposable shared clone, real main/worker/writer):
failed last release (real close then fail) → cert false; declared-full real
worker + estimator roles (end-to-end five hands); interrupt after cleanup
before finalization via settrace → drained production stage retained;
console SIGINT at the certificate STORE_SUBSCR → cert false; SIGINT at Job
acquisition → job released; interrupt after real os.replace → file bound;
bounded close against a real pipe writer holding the lock.
Not seen: a test for C1/C3; a stream-close *failure* (as opposed to timeout).

## Budget (raw lines, frozen blobs)

sample/r001: tool 621, tests 545. ownership/r002: tool 626, tests 601.
Production 333 + 626 = 959; tests 198 + 601 = 799. Working figure 1,200/600;
tests exceed the working figure; controller authorization.md grants up to
3,000 lines. Hygiene from raw bytes: re-measured separately (grep -c $'\r'
on a pipe mis-reported; Python byte count is authoritative).

Prediction recorded before opening deferred inputs: no Important finding on
either contract; Minor/advisory only.

Recorded 2026-09-09T14:40:12Z
