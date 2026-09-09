# Cold review: v0a-eval-panel-ownership/r002 (final combined source)

Reviewer: Claude (Opus 5), independent Tier C cold pass, 2026-09-09.
Candidate: `d8d291cc1f813ce798f2d3a990b2a8bf2297e124`.
Verdict: **CLEAN**. Design verdict: **SOUND**.

No Critical or Important finding survived verification. Four Minor and six Advisory
items are recorded below; none of them blocks adoption of this candidate.

A contamination event occurred during the pass and is disclosed in full in section 9.
It did not change this verdict.

## 1. Identity, verified from Git objects

All of the following were resolved from the object database, never from the packets'
claims and never from the working tree (which is dirty and is not the candidate).

| Check | Result |
|---|---|
| `refs/heads/review/v0a-eval-panel-ownership/r002` | `d8d291cc1f813ce798f2d3a990b2a8bf2297e124` |
| Its sole parent | `72954e1331c9b191d927c1c4b82f277bcd322a4c` |
| Its tree | `2b542a78b5a96963a154ed1da6408834eea3e3e8` |
| `refs/heads/review/v0a-eval-panel-sample/r001` | `72954e1331c9b191d927c1c4b82f277bcd322a4c` |
| Sample parent / tree | `182d14e2...` / `73797f3b554f68c3ced59cc295b0e41f1507b8bb` |
| Chain | `0bc19bca` -> `182d14e2` -> `72954e13` -> `d8d291cc`, each a single parent |
| Base of the chain | `0bc19bca`'s parent is `f647a798...`, the governing BASE |

Changed paths at each step (`git diff-tree -r --name-status`) are exactly
`tools/v0a_eval_panel.py` and `tests/test_eval_panel_tool.py`, for all three steps and
for the combined `0bc19bca -> d8d291cc` diff. No other path differs from the rejected
round.

Files declared out of scope are byte-identical to the rejected round `0bc19bca`,
confirmed by blob id, and their contents were not audited:

- `src/pontius/eval_bridge.py` = `e4826810d4af13957c944b89134ab9ae5f466dd9`
- `tests/test_eval_bridge.py` = `0e55a0ae8ee6baccebaa038f6cd9084b3db4f06e`
- `tests/cases.json` = `8d81dd6ccf74afce50b3743055119bbb4f3ffd99`
- `tests/fixtures/eval_panel/plan-capacity.json` = `5040350e1332a360d5737a667749832a6817b8d7`
- `tests/fixtures/eval_panel/plan-preflight.json` = `6f8d92d2171ad7145000d0c2bdbfb76a5bf87523`

### Manifest recomputation

Recomputed from raw blob bytes, rows `"<sha256>  <path>"`, sorted as whole rows under
`LC_ALL=C`, LF after every row:

```
2b7cebc8dbf18abc816d5e714f9d737db0320089f2bd809787fedc94e4427ead  tests/test_eval_panel_tool.py
4bc3bae53f78d747d69d5c4cca4cc39c7ac58d309fc4a3d4a9c453d39f3e1763  tools/v0a_eval_panel.py
```

SHA-256 of those bytes = `86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926`,
which equals both the packet's `manifest.sha256` file (byte-for-byte) and the digest
stated in `handoff.md` and `candidate.json`.

The sample packet reproduces identically: recomputed manifest digest
`d79035495a278fa8ee3fb1a6adc6fc1838938900ab7c19bbdd434264faf63510`, matching its
`manifest.sha256` file and its stated digest.

### Pinned inputs and check receipts

All 22 pinned digests in the ownership `handoff.md` and all 16 in the sample
`handoff.md` were recomputed with `sha256sum` and match exactly, with no exception.
Both deferred coverage digests match: ownership
`5d0c4c730b7fd65f0276d63d78a845d8002442a037c363f415542db5dde9e4f5`, sample
`9b481d761c8eaa73bfe9e26447e9cc54ddbe046a6fe99727d994a9685958129d`. Both packets'
`checks/*-stderr.txt` are the empty-file digest `e3b0c442...`, i.e. genuinely empty.

`checks/coordinator-verification.json` in the ownership packet is not itself pinned in
`handoff.md`. Its contents agree with everything I independently recomputed, so this is
noted, not charged as a defect.

### dependencies.json provenance

`inputs/dependencies.json` is byte-identical in both packets
(`ab0933726111415870200d4b14358012826da35fd2f083890cf7d8b0165f50b2`). It states its own
base as `f647a7989394f084875a040b20c41891168163ed` - the governing BASE, **not** this
candidate's immediate parent - and declares its scope as
`"direct semantic inventory, not transitive closure"`. I resolved all 34 pinned paths at
that stated base with `git rev-parse <base>:<path>`: 34 of 34 blob ids match, zero
mismatches. It is therefore a **direct inventory, not a closure**, and it is pinned at
the base it names, exactly as `handoff.md` requires the reviewer to confirm.

## 2. Independent inventory (recorded before the deferred inputs)

My invariant and related-path inventory was written from the frozen blobs and the BASE
brief/design alone, before `coverage.md`, `checks/`, or any `inputs/*disposition.md`,
`inputs/repair-plan.md`, `inputs/authorization.md`, `inputs/workflow.md` or
`inputs/controller-rulings*.md` was opened.

Path (preserved copy):
`C:/Users/point/AppData/Local/Temp/claude/D--Pontius/b254894f-7ba4-4380-a35a-9701c4422d3f/`
`scratchpad/rvw-opus5-independent-inventory-d8d291cc.md`
SHA-256 `4496f661f1906f91a4a32245dd73df57fae8abca0b7835956c018dd2390b8cb8`.

It records twenty invariants I-1..I-20 over the five protected pieces of state named in
the review prompt (cleanup certificate, observation records, signal-deferral window,
boundary publication registry, admitted schedule), the eight adversarial questions I set
out to answer, and seven residual concerns R-1..R-7 that became the findings below.

## 3. What the frozen source actually establishes

Working bottom-up from `tools/v0a_eval_panel.py` at the candidate, each protected state
holds on every path I could construct, including exceptions, interrupts immediately
before/during/after each write, threads that outlive cleanup, and native failure at each
release.

**Cleanup certificate.** `job` and `process` are pre-bound to `None` (353). The native
Job is constructed *inside* both the interrupt-deferral context and the cleanup `try`
(405), and an interrupt that arrived during construction is converted to a real
`KeyboardInterrupt` immediately afterwards (406-407), so a returned Job is always closed
by `attempt("close job", ...)` (479-480) and an interrupted acquisition never launches a
worker. Every release is its own `attempt` (441-450) that records `ok`, `interrupted` or
the exception text and never prevents the next; the job is closed last. `verify` (452-457)
observes `job.active() == 0`, a non-`None` exit code, no live I/O thread and all three
streams closed, and it runs *before* `close job`, so a failed final release still
falsifies the certificate. The certificate itself (483-485) is computed outside and after
the deferral context, is the conjunction of `resource_state_verified` with *all* recorded
outcomes, and is monotone: no path rewrites a recorded non-`ok` outcome to `ok`.

I could not construct any schedule in which `cleanup_verified` is true while a job
handle, a process, an I/O thread or a pipe survives. That closes accepted finding A of
the r004 disposition and I-01 of the ownership/r001 disposition.

**Signal-deferral window.** Inside the window a console SIGINT does not unwind; it stamps
`report["status"]="interrupted"` and `report["cleanup"]["console interrupt"]="interrupted"`
(304-306), and `"interrupted" != "ok"` makes the certificate false for the rest of the
run. Outside the window the original handler is back, so an interrupt landing on the
certificate store unwinds with the pre-initialised `False` (350) rather than storing a
stale `True`. The comment at 481-482 states this reasoning correctly and the code matches
it. This closes the residual window the ownership/r001 review identified.

**Observation ownership.** `observations` and `errors` are the caller's lists from line
347-349; `drain` appends each record to `report["observations"]` at first receipt
(384-386) and mutates it in place thereafter; `missing_stages` is a derived annotation
(394-395), not an ownership transfer. Every `drain` call site (425, 477) is inside the
deferral window, so the interval between `events.get_nowait()` and the store cannot be
unwound by a console interrupt. That closes accepted finding B.

**Boundary publication.** `retain_boundaries` (498-536) registers the intended identity
(`path`, `bytes`, `sha256`) and a `pending` state *before* the fallible write, moves to
`publishing` after the staged write, and reconciles the actual final file inside a
`finally` - reading it back and refusing on a byte mismatch - before `retained[count]` is
bound and the encoding is deleted from `boundary_base64`. An interrupt delivered after a
successful `os.replace` therefore still binds the artifact, and any failure leaves the
encoding recoverable with `boundary_retention` marked incomplete. That closes accepted
finding D.

**Admitted schedule.** `validate_plan` returns a single `AdmittedPlan(wire, schedule)`
(64-71, 170) whose `wire` is an immutable canonical snapshot and whose `schedule` is a
tuple of role-bearing `ScheduledHand` units. The supervisor's `send` (368), the worker's
execution (255-256, 271), the reconciliation (541) and the estimator (566-567) all read
that one object; the worker re-admits the serialized snapshot across the process boundary
with the same deterministic function, so the two sides cannot disagree. `declared-full`
compares role-bearing sets and the literal board (163-169), so relabelling a development
hand as a control - including the all-controls/empty-development case - is refused. That
closes accepted finding C.

I also checked the two identity claims that could silently disagree.
`bridge.permutation_digest` (`sha256(json.dumps([hand_name(h) ...]))`, default separators)
and `main`'s top-level `permutation_sha256` (599-609, `sha256(json.dumps(plan["permutation"]))`)
are provably the same value, because admission pins `plan["permutation"]` equal to that
exact list (137-140). `full_pool_estimate`'s `hands=HERO_COUNT` (1081) equals
`len(hero_hands(board))` for any five-card board, so it cannot disagree with the admitted
`hand_count`. The `values` keys the panel builds (`str(CHECK)`, `str(reference["bet"])`)
are the same strings `validate_reference` looks up (`str(CHECK)`, `production["bet"]`),
because both derive from `bet_action(root)`.

## 4. Findings

Severity-ordered. No Critical. No Important.

### Minor

**M-01 - `defer_interrupts` never restores a SIGINT handler that was installed from C.**
Location: `tools/v0a_eval_panel.py` 297-313 (specifically 301-302 and 312-313).
Invariant: I-2 - the deferring handler must be uninstalled before the certificate is
finalised; the code's own comment at 481-482 asserts that "the normal handler must be
restored".
Counterexample: embed this tool in a host whose SIGINT handler was set by C code rather
than by Python. `signal.getsignal(signal.SIGINT)` then returns `None`, so `previous` is
`None`, but line 308 still installs `interrupted`. The `finally` at 312-313 is guarded by
`previous is not None`, so it does nothing, and the non-raising handler survives for the
remaining life of the process, bound to a `report` dict that is no longer live. A later
Ctrl-C is silently swallowed and mutates a dead report.
Correction: track installation with a separate boolean (or a sentinel distinct from
`None`) and restore on that, so "not the main thread" and "getsignal returned None" stop
sharing one flag.
Confidence: medium - the defect is certain, its reachability under
`python tools/v0a_eval_panel.py run` on CPython 3.14.6 is not, since the interpreter's
own `default_int_handler` is a Python callable.

**M-02 - a stderr read or decode failure is dropped without a record and cannot falsify
the certificate.**
Location: `tools/v0a_eval_panel.py` 362-364 (`receive_errors`), contrast 355-360
(`receive`), consumed at 456 and 490.
Invariant: I-1 and I-16 - an error the parent could observe must reach `report["errors"]`
so the completion demotion can see it; a released-but-failed reader must not read as a
clean release.
Counterexample: the worker (or a native library loaded in it) writes a byte sequence that
is not valid UTF-8 to fd 2 - for example a localised Windows CRT message on a non-UTF-8
code page - and then exits 0. `for line in stream` in `receive_errors` raises
`UnicodeDecodeError`. Unlike `receive`, there is no `except`, so the thread dies, the
exception is printed by `threading.excepthook` to the parent's own stderr and nothing is
appended to `errors`. `verify` at 456 only asks whether threads are *alive*, and a dead
thread satisfies it, so `resource_state_verified` is true, every cleanup entry is `ok`,
`cleanup_verified` is true and the run reports `status: "completed"` while its entire
stderr stream was discarded. The same asymmetry produces an unhandled thread traceback
whenever a failed join is followed by `close_stream(process.stderr, ...)` closing the pipe
under a live reader.
Correction: wrap `receive_errors`' loop in the same `try/except Exception` as `receive`
and append `f"worker stderr: {type(error).__name__}: {error}"`.
Confidence: medium.

**M-03 - one release can consume the whole shared cleanup deadline, collapsing every
later bound to zero.**
Location: `tools/v0a_eval_panel.py` 459 (`cleanup_deadline`), 461-464 (`join`), 471
(`attempt("wait", ... timeout=10)`), 474-476 (`close_stream(... max(0, deadline - now))`).
Invariant: I-6 - "every cleanup release is its own bounded attempt", as the docstring at
336-343 and the repair plan both state.
Counterexample: `process.kill()` succeeds but the child is stuck in an uninterruptible
kernel call, so `process.wait(timeout=10)` blocks for its own full, independent ten
seconds and raises `TimeoutExpired`. `cleanup_deadline` - set ten seconds earlier - has
now expired, so `join(thread)` calls `thread.join(timeout=0)` for all three threads and
`close_stream(stream, 0)` for all three streams. `done.wait(0)` returns before the closer
thread is even scheduled, so all six attempts record `TimeoutError` regardless of whether
they would have completed, and three daemon closer threads are left racing a still-live
reader thread on the same pipes. No false certificate results (`cleanup_verified` is
false on either reading), but the recorded outcomes no longer distinguish "this release
hung" from "the deadline was already gone", which is the diagnostic the per-attempt
design exists to produce.
Correction: give `attempt("wait", ...)` the same `max(0, cleanup_deadline - now())` bound
the joins and closes use, so a single deadline governs the whole sequence.
Confidence: high on the mechanism, medium on operational impact.

**M-04 - an orphan `.partial` staging file survives a failed or interrupted rename.**
Location: `tools/v0a_eval_panel.py` 516-529.
Invariant: I-11/I-20 - every file in a retained run directory has a recorded identity in
the result. The candidate's own test asserts this shape at
`tests/test_eval_panel_tool.py` 180-181, which enumerates the directory and requires it
to contain exactly the bound artifact.
Counterexample: `staging.write_bytes(raw)` at 516 succeeds and `os.replace(staging, path)`
at 518 fails (cross-device, a virus scanner holding the destination, or `ERROR_ACCESS_DENIED`).
The `finally` finds `path.is_file()` false, sets the publication back to `pending` and
keeps the encoding - correct - but nothing removes
`capacity-boundary-<k>.blueprint.json.partial`, so the retained run directory keeps an
unbound file that appears in no `boundary_artifacts` entry and in no result digest. The
existing test only exercises the write-fails path, where no partial exists, so this is
uncovered rather than contradicted.
Correction: in the `else` branch at 528-529, `staging.unlink(missing_ok=True)` before
setting the state back to `pending`.
Confidence: high.

### Advisory

**A-01 - the sample round's RED receipt was produced from a test file that is not the
frozen candidate's, and coverage does not disclose it.**
Location: `beb069455a6d3ce20f202c0b4398683548631a33:tests/test_eval_panel_tool.py`
(`23708fa4...`) versus `72954e1331...:tests/test_eval_panel_tool.py` (`db882cc2...`), against
`D:/Pontius-handoffs/v0a-eval-panel-sample/r001/coverage.md`.
The delta is two cases that had to track the production API change
(`full_pool_estimate(rows, 1081, "declared-full")` -> `(rows, 1081, admitted)` and
`plan["phase"]` -> `plan.document["phase"]`), so it is a necessary consequence of a
signature-changing repair, not a weakened RED. The three role-movement subcases that
actually fail on RED are byte-identical between RED and GREEN, so the claimed defect *is*
reproduced with the exact frozen assertions. What is missing is the disclosure: the
sample `coverage.md` says only "33 cases ... exactly three assertion failures", implying a
byte-identical pair. The ownership round has no such gap - its RED `b6ede27a` carries the
candidate's exact test blob `3c040439...` and the parent's exact tool blob `46eb71ea...`, so
the only difference between RED and GREEN there is the production file.
Correction: state the two adapted cases and their reason in the sample coverage record.

**A-02 - whole-slice line budget.** The brief at BASE sets 600 production and 400 test
lines for the whole of Slice A. Measured from raw frozen bytes: production
`src/pontius/eval_bridge.py` 333 + `tools/v0a_eval_panel.py` 626 = **959**; tests
`tests/test_eval_bridge.py` 198 + `tests/test_eval_panel_tool.py` 601 = **799**. The
dated experiments script of design step 3 does not exist yet, so both figures will grow.
`coverage.md` discloses this and cites the controller's up-to-3,000-line correction
authorization; the 600/400 brief figure is nevertheless still the written budget and only
the controller can restate it. This needs a controller number, not a reviewer's.

**A-03 - a repeated stage event before `hand_completed` silently overwrites.**
`tools/v0a_eval_panel.py` 390-395 replaces `record["stages"][event["stage"]]` without
comment; only a stage or completion arriving *after* `complete` is true is recorded as
`repeated observation` (388-389). A worker that emitted `production` twice would leave a
record that still satisfies `set(stages) == set(STAGES)` in `complete_sample`. The worker
in this candidate emits each stage exactly once per hand, so this is unreachable from the
frozen source; it is recorded because the two consumers of `stages` treat presence, not
arrival count, as the evidence.

**A-04 - `supervise` can unwind before the report's cleanup keys exist.** Lines 344-351:
`validate_plan` and `load_host` run before `report.update(... cleanup={} ...)`. If either
raises, `main` records a `failed` result that has no `cleanup`, `cleanup_verified` or
`resource_state_verified` member, unlike every other failure path. Nothing in this
candidate reads those keys, so this is a shape note for future consumers.

**A-05 - an empty `test-subset` preflight reports `sample_complete: true` with zero
observations.** Lines 149-170 impose no minimum on `development_hands`/`controls`, so
`coverage: "test-subset"` with both lists empty is admitted, the schedule is empty,
`complete_sample` returns `{}` - which `is not None` (487, 553) - and the run reports
`completed` with `sample_complete: true` and no observations. The report is not false
(coverage, the empty observation list and `full_pool_estimate.kind == "not_estimated"`
are all recorded), and the brief's rule that "host test subsets establish only their
named subset" is satisfied vacuously, so this is a labelling note rather than a defect.
First noticed in the contaminating file described in section 9, then verified
independently against the frozen source; recorded here for completeness, not adopted as
a finding.

**A-06 - the worker exits 0 after emitting a `failed` event.** `worker()` at 282-294
emits `completed` and returns 0 even when `run_plan` already emitted `failed` for budget
exhaustion (272-274) or a reference disagreement (277-279). The parent still classifies
the run correctly, because the `failed` event is always drained before the loop can
declare completion (the exit test at 428 requires the reader thread dead *and* the queue
empty) and a non-empty `errors` forces `status: "failed"` at 429-430 and again at
490-493. The only artefact is `worker_exit_code: 0` beside `status: "failed"` in the
retained result. Same provenance note as A-05.

### Considered and dismissed

- The control hand's freshly replayed root (275) is not passed to
  `require_declared_root` the way the primary root is (259). Not a defect:
  `hand_totals` and `build_reference` both call `bet_action(root)`, which calls
  `require_declared_root` itself, and `replay_root` depends only on `stacks`, so the
  branch produces an equal root.
- `validate_plan`'s short-circuit on an `AdmittedPlan` (114-115) is an in-process trust
  boundary. Not reachable from untrusted input: the worker's plan always arrives as JSON
  (287-288), so it can never be an `AdmittedPlan`, and the cross-process path re-admits
  the serialized snapshot in full.
- `AdmittedPlan.document` re-parses the wire on each access. A performance nit
  (a ~100 KB permutation, parsed a handful of times per run), not a correctness issue;
  it is what makes the snapshot immutable for all consumers, which is the point.
- `drain`'s `events.empty()` / `get_nowait()` pair. Safe: there is exactly one consumer.

## 5. Design verdict: SOUND

The two prior rounds were STRAINED for one stated reason - the protected state was
reconstructed independently in several places (a local `hands` map, a cached cleanup
boolean, three separate rebuilds of the schedule, published files with no binding). This
candidate replaces each of those projections with a single owner:

- one role-bearing `AdmittedPlan` that the sender, the worker, the reconciler and the
  estimator all read, so there is nothing left to disagree;
- observation records attached to caller-owned storage at first receipt, with
  `missing_stages` demoted to a derived annotation;
- a monotone certificate computed once, last, from recorded outcomes plus observed
  resource state, outside the interrupt-deferral lifetime;
- a publication registry that spans staging -> rename -> binding, with reconciliation in
  a `finally`.

Each of the four accepted r004 findings and both ownership/r001 findings are answered by
a structural change rather than another guard, which is what the second-residual root-cause
note asked for. The costs are legibility ones and I weighed them before settling on SOUND:
`supervise` is roughly 160 lines with five nested closures and a large `finally`, and the
`AdmittedPlan` short-circuit is an implicit trust boundary that a reader must reconstruct.
Neither is a shape defect, and neither reintroduces a second copy of protected state.

## 6. Comparison against `coverage.md`

`coverage.md` (ownership) enumerates five invariants. Mapping to my independent inventory:

| Coverage invariant | My inventory | Agreement |
|---|---|---|
| 1 release owner before another fallible operation | I-4, I-5, I-6 | agrees |
| 2 certificate only after all inputs are final | I-1, I-2, I-3 | agrees |
| 3 drained record reachable through the caller's report | I-8, I-9 | agrees |
| 4 stream close cannot block the report owner | I-7 | agrees, with M-03 |
| 5 identity before rename, reconcile after | I-11, I-12 | agrees |
| inherited sample contract | I-13, I-14, I-15, I-17 | agrees |

Coverage explicitly claims the ownership/r001 reviewer's
"after-certification/before-handler-restoration window is eliminated by ordering". I
verified that independently and concur.

Items in my inventory that coverage does not address, all of which are Minor or Advisory
above and none of which is a product defect on its own:

- I-2's failure mode when `signal.getsignal` returns `None` (M-01). Coverage's invariant 2
  reasons about handler *restoration* but not about the case where restoration is skipped.
- The asymmetry between the two reader threads (M-02). Coverage's invariant 3 tracks
  `queue -> drain -> stage -> main -> result/journal` for stdout observations and does not
  reach the stderr channel.
- The shared-deadline coupling (M-03). Coverage's invariant 4 asserts "a bounded wait" and
  the frozen `close_stream` does implement one; what is unaddressed is the bound's value
  after an earlier attempt consumed it.
- Staging-file hygiene on the rename-failure branch (M-04). Coverage's invariant 5
  enumerates "before write, partial write, before rename, after rename and before binding"
  for the *encoding*, not for the staging file.
- I-18's admission totality for the degenerate empty subset (A-05) and I-16's exit-code
  labelling (A-06).

Per `handoff.md` and the workflow, **missing coverage alone is not a product defect**, and
I do not treat any of the above as one. Conversely, coverage claims nothing I could not
verify from the frozen source.

The sample packet's `coverage.md` maps equally cleanly to I-13, I-14, I-15 and I-17. Its
one gap is A-01, the undisclosed RED test-file delta.

## 7. Receipts assessment

**Ownership round.** RED `b6ede27a2c737f2a77344908fb3ebe8a88088f54` has the sample
candidate as its sole parent. I verified from Git that its
`tests/test_eval_panel_tool.py` blob is `3c040439...`, byte-identical to the frozen
candidate's, and its `tools/v0a_eval_panel.py` blob is `46eb71ea...`, byte-identical to the
parent's. That is a textbook RED/GREEN pair: the *only* difference between the failing and
passing runs is the production file. `red-stdout.txt` shows `Ran 24 tests ... failures=2`,
`errors=0`, and the two failures are exactly
`test_console_interrupt_cannot_race_a_true_cleanup_certificate` (recording
`cleanup_verified` true beside `'console interrupt': 'interrupted'` - precisely the
accepted I-01 defect) and `test_interrupt_at_native_job_acquisition_still_releases_the_job`
(`[False] != [True]`, the accepted M-01 leak). GREEN `focused-stdout.txt` is
`2 passed, 44 deselected`; the journal line records 35 cases, 0 skipped, exit 0,
`source_commit` `d8d291cc...` and `source_verified: true`.

**Sample round.** RED `beb0694...` changes tests only against its parent (`tools/...` blob
`3637c4dc...` equals the parent's); `Ran 22 tests ... failures=3, errors=0`, the three
role-movement subcases. GREEN journal: 33 cases, 0 skipped, exit 0, `source_commit`
`72954e13...`, `source_verified: true`. See A-01 for the one disclosure gap.

**Environment.** Every receipt records CPython 3.14.6, `-B -P -W error::ResourceWarning`,
`-p no:cacheprovider`, and a scrubbed environment of exactly
`SystemRoot, TEMP, TMP, PONTIUS_GIT, PYTHONDONTWRITEBYTECODE`, each in its own disposable
worktree with its own locked venv. All four `*-stderr.txt` files are provably empty
(`e3b0c442...`). The 3.14-only rule is honoured throughout, including by the lint receipt.

**Lint.** `checks/lint.json` records `ruff check --no-cache` over exactly the two manifest
files at the candidate, exit 0, `All checks passed!`. `pyproject.toml` at the candidate
sets `line-length = 100` with `E501` selected, which is consistent with my own
measurement.

**Diagnostic.** `ee98f51f...` is a tests-only change on the same parent whose receipt exits
1. Coverage and the ownership disposition both state explicitly that it is an
over-strict instruction-locator diagnostic and **not** counted as a product RED. I
verified its tool blob equals the parent's, so it cannot have demonstrated a production
defect; the exclusion is correct and correctly disclosed.

**Limits I hold the receipts to.** These are correctness receipts only. They are not
authorized capacity or preflight measurement, not a retained run, and not evidence of
poker strength; both `handoff.md` files and both coverage records say so, and nothing in
the receipts overreaches. I executed nothing.

## 8. Line counts and hygiene, measured from raw frozen bytes

Reviewer arithmetic, not a test receipt. Measured with CPython 3.14.6 at
`D:/Pontius/.venv/Scripts/python.exe` over bytes from `git cat-file blob`.

| File | Lines | Bytes | CRLF | Final NL | Trailing WS | Longest | Tabs | Non-ASCII |
|---|---|---|---|---|---|---|---|---|
| `tools/v0a_eval_panel.py` | 626 | 29,775 | 0 | yes | none | 100 (L263) | none | none |
| `tests/test_eval_panel_tool.py` | 601 | 30,352 | 0 | yes | none | 100 (x3) | none | none |

Both files are within the project's configured 100-column limit; no line exceeds it.
Hygiene is clean.

Diff sizes: against the rejected round `0bc19bca`, `git diff --numstat` gives
`231/106` for the tool and `255/12` for the tests - **486 additions, 118 deletions**,
matching `coverage.md` exactly. Whole-slice against BASE `f647a798`: 959 production and
799 test lines (see A-02).

## 9. Disclosure: contamination event

I am disclosing this because the review contract requires it, even though I did not open
any prohibited path.

While this pass was running, a **concurrent process overwrote my scratch inventory file**
at
`.../b254894f-7ba4-4380-a35a-9701c4422d3f/scratchpad/inventory.md` (mtime 12:03:23), and the
harness surfaced the replacing content to me automatically in a file-change notice. I did
not request, open or search for that file's new content. What I saw was another agent's
*inventory* of this same candidate: an obligations list, an invariant list, and eight
lettered "candidate observations" C1-C8. It contained **no findings, no severities and no
verdict**.

The same scratch directory also contains
`eval-panel-sample-ownership-inventory-claude.md` (8,341 bytes, mtime 10:40,
SHA-256 `52b87992a333ae0b5278ba7c0b82c4baed5c5ad5881333f520a4a966ecf9bc92`), which differs
from the 12:03 file. **I did not open it and its contents are unknown to me.** The
scratch directory is evidently shared across concurrent sessions rather than
session-isolated; it also holds `r004_patch.py`, `verify_pins.py`, `verify_deps.py`,
`hygiene.py` and an `mf/` directory that are not mine. This is a harness-isolation defect
worth fixing before the next concurrent review, independent of this candidate.

Effect on this report, stated precisely:

- My own inventory was written and hashed **before** the overwrite and before any deferred
  input was opened. Its exact bytes are preserved at
  `rvw-opus5-independent-inventory-d8d291cc.md`, SHA-256
  `4496f661f1906f91a4a32245dd73df57fae8abca0b7835956c018dd2390b8cb8` - the identical
  digest I recorded at the time of writing, which demonstrates it is unaltered.
- Every Minor finding (M-01..M-04) appears in that pre-exposure inventory as R-1, R-2,
  R-3 and R-4. A-02, A-03 and A-04 likewise (R-5, R-6, and my own line-count arithmetic).
- Two Advisory items, **A-05 and A-06**, were first noticed in the exposed file and are
  labelled as such at the point of use. I verified both independently against the frozen
  source before recording them, and both are labelling notes rather than defects.
- The exposed file's remaining unique observations concerned `load_host`'s fixed
  `sys.modules` key and the no-op control-board replay; I evaluated both against the
  frozen source and dismissed them (see "Considered and dismissed"). Its line-budget
  observation duplicates arithmetic I had already performed.
- The exposure could not have changed my verdict: it contained no verdict, no severity and
  no Critical or Important claim, and nothing in it caused me to withdraw a finding.

## 10. Prohibited sources not opened

I did not open, list the contents of, grep, or tail any of the following:

- Any `reviews/` directory in any packet, including
  `D:/Pontius-handoffs/v0a-eval-panel-ownership/r002/reviews/`,
  `.../v0a-eval-panel-sample/r001/reviews/`, `.../v0a-eval-panel-ownership/r001/reviews/`, and
  any `reviews/` under `.../v0a-eval-panel-code/`, `.../v0a-eval-panel-design/` or
  `.../v0a-eval-panel-impl/`. I listed the top level of the two packet directories, which
  printed the *name* `reviews` and nothing from inside it. The coordinator-provenance and
  review-report files referenced by the dispositions were not opened.
- `D:/Pontius-handoffs/progress.md` and `D:/Pontius-handoffs/INDEX.md`.
- `checks/review-01-inventory.md` and `checks/review-02-inventory.md` in either packet.
  These names appeared in a directory listing; neither file was read.
- Any implementer transcript or session log.

I ran no project code: no pytest, no import of any `pontius` module, no invocation of the
tool, the owners, `uv` or `pip`. Git was used read-only (`rev-parse`, `cat-file`,
`ls-tree`, `diff-tree`, `diff --numstat`, `log -1`). Standalone utility scripting used
CPython 3.14.6 at `D:/Pontius/.venv/Scripts/python.exe` for raw-byte hashing, pin
resolution and hygiene arithmetic only, plus coreutils `sha256sum`; that work is reviewer
arithmetic, not a test receipt. I made no commit, push, ref write, worktree change or
network write, and edited no file in `D:/Pontius` or `D:/Pontius-handoffs`. I wrote no
file outside my scratch directory: both my inventory and this report live there, and this
report is returned as text rather than written into either packet.

## 11. Verdict

**CLEAN.** No material finding survives verification. The four accepted r004 findings and
both ownership/r001 findings are closed by structural change, the identity and digest
chain verifies exactly, the RED/GREEN evidence is sound (with the single disclosure gap
A-01, which is a record-keeping item and not a product defect), and hygiene is clean.

**SOUND**, for the reasons in section 5.

Adoption remains subject to the gates this review does not speak to: the second
independent Tier C pass, the applicable broad snapshot suites, the whole-slice line-budget
number in A-02, and explicit controller authorization for any commit, push or measurement.
