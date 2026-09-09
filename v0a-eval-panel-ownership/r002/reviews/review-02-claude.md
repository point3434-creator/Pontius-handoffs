# Cold review 02 — Claude — v0a-eval-panel-ownership/r002

Verdict: **CLEAN**. Design verdict: **SOUND**.
No Critical or Important finding survives frozen-source verification.
Two Minor findings and two advisories; none blocks adoption.
Specification: PASS on the cleanup/observation/publication contract and its combined
sample consumers. Engineering quality: PASS.

Reviewer: Claude, independent cold pass 02, 2026-09-09.
Candidate: `d8d291cc1f813ce798f2d3a990b2a8bf2297e124` (final combined source)
Manifest SHA-256: `86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926`
Base / sole parent: `72954e1331c9b191d927c1c4b82f277bcd322a4c` (sample/r001)
Tree: `2b542a78b5a96963a154ed1da6408834eea3e3e8`
Ref: `refs/heads/review/v0a-eval-panel-ownership/r002` (local; not on origin)
All locations are frozen blob line numbers at the candidate commit.

## Disclosure

A session-start status check tailed `progress.md` (three lines) before this review
began and exposed the sibling Codex verdicts for this and the sample packet. No review,
disposition, coverage or check content was opened before the inventory was recorded
and hashed. The reviewer authored the rejected r004 and the root-cause note this
candidate answers; bias toward acceptance is possible and was countered by the
adversarial checks listed below, performed after the inventory.

Per the handoff, this reviewer did not commit, push, run hooks or perform any network
write; the review, inventory copy and ledger line are on disk only, pending the
controller's publication approval.

## Contracts under review and residual status

Ownership: r001 A → r003 I-01 → r004 A/B (second residual); this is the contract's
separate candidate, continued from ownership/r001 (one Important, one Minor, both
accepted by its finalizer in `inputs/ownership-disposition.md`). Retention: r003 I-03
→ r004 D (first residual). Combined sample consumers inherited from sample/r001.

## Independent inventory (recorded and hashed before deferred inputs)

Scratchpad file SHA-256
`52b87992a333ae0b5278ba7c0b82c4baed5c5ad5881333f520a4a966ecf9bc92`, recorded
2026-09-09T14:40:12Z; copied to `checks/review-02-inventory.md`. Invariants:
- O1. `cleanup_verified` is true iff every release attempt succeeded (including the
  final job close and any console interrupt) and the resource state was observed
  released; decided after the last release; monotonically false after any failure.
- O2. Every drained observation is reachable from the caller-owned report the moment
  it is drained; no local accumulation.
- O3. A console interrupt between acquisition and the last release never unwinds past
  a release; it is recorded and the remaining releases run.
- O4. Every release attempt is bounded.
- O5. `main` records one result and one journal row for completed, failed and
  interrupted, carrying the owned observations.
- R1. An artifact's identity is in the result before its file can become visible under
  its final name; a completed final-name file is never unbound or labeled unwritten.

## Verification against frozen source (`tools/v0a_eval_panel.py` @ d8d291cc)

- O1 holds. `resource_state_verified` (350–351, 452–457) is set only by a successful
  `verify`; `cleanup_verified` (483–485) is computed after the `with defer_interrupts`
  block — i.e. after `close job` (479–480) and after the handler is restored — as the
  conjunction with `all(value == "ok")`; a console interrupt writes a non-"ok" entry
  (304–306); a failed `close job` is recorded by `attempt` (448–450). No path stores a
  true certificate before the last release. A console interrupt between the block exit
  and the store unwinds with the initial `False` (comment at 481–482).
- O2 holds. `drain` (373–401) appends a new record to `observations` — the caller's
  list (349) — on first receipt and mutates it in place; `missing_stages` is
  recomputed on the record; the local `hands` map is gone.
- O3 holds on the main thread. `defer_interrupts` (297–313) replaces SIGINT with a
  recording handler for the whole acquisition-to-release span; the loop observes
  `status` (426–427); `Job` is acquired inside the protected `try` and an interrupt
  recorded during acquisition raises before a worker is launched (405–407); the
  `finally` runs each release as an independent `attempt`, the job last (441–480).
- O4 holds. Shared ten-second cleanup deadline for joins (459–464); `close_stream`
  (316–332) closes through an owning daemon thread with a bounded wait and reports a
  pending close as `TimeoutError`, which `verify` then sees as an unclosed stream;
  `process.wait(timeout=10)`.
- O5 holds. `main` owns `report` (590), passes it to `supervise` (602–603), and
  `finish_run` runs in `finally` with `json_safe` (616–620); `KeyboardInterrupt` and
  `Exception` both recorded once.
- R1 holds. `retain_boundaries` (498–536) registers `publications[count]` with path,
  bytes and sha256 in state `pending` before the staging write (512–514), moves to
  `publishing` before `os.replace` (517–518), and the inner `finally` reconciles the
  actual final file by presence and byte equality before binding and dropping the
  encoding (519–529). Retry after completion is safe (`row.get(..., {})`, `setdefault`).

Tests (`tests/test_eval_panel_tool.py` @ d8d291cc) exercise each invariant through the
real launcher, job, worker and result/journal writer in a disposable shared clone:
real native close followed by a reported failure → certificate false (426–442);
console SIGINT at the certificate's `STORE_SUBSCR` opcode → false (492–519); SIGINT
during native `Job` acquisition → job released, close ok, certificate false (521–543);
interrupt after the last release before finalization via `settrace` → the real drained
production stage survives in the retained result (461–490); interrupt after the real
`os.replace` → the final file is bound with byte-exact digest (545–567); a real OS pipe
with 1 MiB backpressure → bounded close timeout, then full drain (569–597). The
inherited fault (active + join), interrupted `wait` (now asserting a false
certificate), assignment refusal, budget kill and completion cases remain.

## Adversarial checks (after the inventory; none produced a material finding)

- Interrupt recorded before `Job` acquisition, then the raise at 406–407: `process`
  is `None`, the job is closed in `finally`, status `interrupted`. Correct.
- `Popen` raising after `Job` creation: job closed, certificate false (no verify), status
  failed with the cause. Correct.
- Assignment refusal: not terminated (unassigned), killed, waited, no threads, streams
  closed, `verify` true (job never had a member), close ok → certificate true with a
  failed status and the `containment_failed` cause. Correct and tested.
- Worker killed before it reads stdin: the sender's blocked write fails on the broken
  pipe when the child dies; no hang. Correct.
- A console interrupt after the worker completes but before the loop observes it:
  status `interrupted`, conservative. Acceptable.
- Sample consumers in the combined source: `complete_sample` and the demotion of
  `completed` (486–493) behave as reviewed in sample/r001; the `document` property and
  `record_key` are unchanged.

## Minor findings

### M-01 — `defer_interrupts` cannot distinguish "not main thread" from a `None` handler

Location: 300–313. `signal.getsignal(SIGINT)` returns `None` when the current handler
was not installed from Python (a C extension or embedding host). In that case
`previous is None` and the `finally` skips restoration, leaving the recording handler
installed after `supervise` returns; later Ctrl-C would mutate a stale report and never
interrupt the process. Not reachable from the tool's own entry (`python … run` installs
`default_int_handler`) or from the test harness. Smallest correction: use a private
sentinel for "no handler installed" and restore whatever `getsignal` returned,
including `None`, when on the main thread. No test needed beyond a unit case on the
context manager.

### M-02 — `receive_errors` is unguarded

Location: 362–364. A non-UTF-8 byte on the worker's stderr raises
`UnicodeDecodeError` in the reader thread (text mode, strict errors); the thread ends,
the remainder of the diagnostic stream is lost, and nothing is recorded in `errors`.
Joins still succeed and no observation is affected. Pre-existing since r001; outside
the two residual contracts. Smallest correction: mirror `receive`'s guard, appending
`worker stderr: …` to `errors`, or open stderr with `errors="replace"`.

## Advisories

- A-01. `retain_boundaries` runs after the deferral context has ended, so a console
  interrupt inside the reconcile `finally` (523–527) — after the rename, during
  `read_bytes`/compare/assignment — leaves the final file present with publication
  state `publishing` and no `boundary_artifacts` entry. Nothing is lost: the intended
  identity is already in `boundary_publications` and the encoding remains in
  `boundary_base64`; the `incomplete; recoverable encodings remain` label is true. A
  consumer wanting a completed binding must reconcile state `publishing` against the
  file. Wrapping the retention loop in `defer_interrupts` would close the window at
  no cost; optional.
- A-02. Any console interrupt during the protected span makes `cleanup_verified` false
  even when every release succeeded. This is conservative and consistent with O1 as
  stated; the report carries `cleanup["console interrupt"]` so the reason is visible.

## Comparison with deferred coverage (opened after the inventory)

`coverage.md` (SHA-256 `5d0c4c73…`, matches the handoff) states five invariants that
map onto O1–O4 and R1, plus the inherited sample contract; its executed cases are the
ones in the frozen test blob and its RED/GREEN identities match the receipts. It
correctly excludes the ee98f51 locator diagnostic from the product RED. It does not
mention M-01/M-02; neither is a missing-coverage claim, both are source observations.
The inventory and coverage agree on category and members.

## Identity, receipts, budget

Read-only Git: ref → commit, sole parent 72954e13 (sample/r001), tree 2b542a78; exactly
two changed paths; manifest recomputed from raw blobs (whole-row `LC_ALL=C` sort, LF
rows) is byte-identical to `manifest.sha256` and its digest equals the handoff value.
All 34 `dependencies.json` pins reproduce at the file's stated base f647a798 (direct
inventory, not a closure). All 23 pinned inputs/receipts and `coverage.md` match their
handoff digests, including `authorization.md` (`b88a1621…`). `src/`,
`tests/test_eval_bridge.py`, the fixtures and `cases.json` are unchanged since
0bc19bca. Chain verified: 0bc19bca → 182d14e2 (ownership/r001) → 72954e13 (sample/r001)
→ d8d291cc.

Receipts (supplied, identity-checked, not re-run): GREEN 35 cases, 0 skipped, exit 0
on this candidate, CPython 3.14.6, `-B -P -W error::ResourceWarning`, `env -i` with
`SystemRoot TEMP TMP PONTIUS_GIT PYTHONDONTWRITEBYTECODE`, `source_verified: true`;
RED b6ede27a (tests only on the sample/r001 bytes) 35 cases exit 1; Ruff exit 0 on the
two changed files; the coordinator verification records the same manifests. Utility
checks here used CPython 3.14.6 (`D:/Pontius/.venv`) for raw-byte hygiene and pin
verification and coreutils `sha256sum`/Git for digests; no project code was imported
or executed. One measurement slip is recorded for honesty: an initial `grep -c $'\r'`
over a `git cat-file` pipe reported every line as CR-terminated; the Python raw-byte
count (0 CR in all four blobs) is the authoritative figure.

Raw frozen lines: tool 626, tests 601; production 959, tests 799 including the
unchanged bridge. Both changed blobs are LF-only, no BOM, no trailing whitespace, no
line over 100 columns. The 600-line test working figure is exceeded and disclosed; the
pinned `authorization.md` grants up to 3,000 lines. Whole-slice projection with design
steps 4–7 still to come: roughly 1,150–1,300 production lines. Budget is a controller
decision.

## Verdict

CLEAN / SOUND. The protected state is now owned in one place each — records on the
caller's report from first receipt, the certificate as a final conjunction after the
last release and after handler restoration, publication as a registered identity
reconciled against the real file — and each invariant has a real-boundary falsifier.
That is the shape change the second-residual rule required, and the two prior misses
described in the root-cause note are closed rather than patched around. No source
change is requested for adoption; M-01/M-02 may ride with the next checkpoint. This
review authorizes nothing beyond itself; ceremonial commit, integration, retained
measurement and the full-pool solve remain the controller's gates.
