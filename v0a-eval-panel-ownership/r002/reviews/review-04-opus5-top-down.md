# Cold review: v0a-eval-panel-ownership/r002 (final combined source)

Reviewer: Claude, independent Tier C pass under checkpoint alternation.

Candidate: `d8d291cc1f813ce798f2d3a990b2a8bf2297e124`
Manifest: `86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926`
Parent / sample candidate: `72954e1331c9b191d927c1c4b82f277bcd322a4c`
Manifest: `d79035495a278fa8ee3fb1a6adc6fc1838938900ab7c19bbdd434264faf63510`
Governing brief and design base: `f647a7989394f084875a040b20c41891168163ed`

**Verdict: CLEAN. Design verdict: SOUND.**
Critical 0 / Important 0 / Minor 4 / Advisory 5. No required correction remains.

---

## 1. Identity and digest verification

Resolved independently with read-only `git rev-parse`, `cat-file`, `diff-tree`.

| Item | Verified value | Matches packet |
|---|---|---|
| ownership r002 ref | `d8d291cc...e124` | yes |
| candidate tree | `2b542a78b5a96963a154ed1da6408834eea3e3e8` | yes |
| candidate parent | `72954e13...22a4c`, one parent only | yes |
| sample r001 ref | `72954e13...22a4c` | yes |
| sample tree | `73797f3b554f68c3ced59cc295b0e41f1507b8bb` | yes |
| sample parent | `182d14e2...9707` (ownership/r001) | yes |
| chain | `f647a79 > 0bc19bc > 182d14e > 72954e1 > d8d291c` | yes |

Changed paths at each step: every commit in the repair chain touches exactly
`tools/v0a_eval_panel.py` and `tests/test_eval_panel_tool.py`, and nothing else.

Out-of-scope files confirmed byte-identical to the rejected round `0bc19bc` by
blob id, and not audited:

- `src/pontius/eval_bridge.py` `e4826810d4af13957c944b89134ab9ae5f466dd9`
- `tests/test_eval_bridge.py` `0e55a0ae8ee6baccebaa038f6cd9084b3db4f06e`
- `tests/fixtures/eval_panel/plan-capacity.json` `5040350e1332a360d5737a667749832a6817b8d7`
- `tests/fixtures/eval_panel/plan-preflight.json` `6f8d92d2171ad7145000d0c2bdbfb76a5bf87523`
- `tests/cases.json` `8d81dd6ccf74afce50b3743055119bbb4f3ffd99`

**Manifest recomputation.** SHA-256 over the raw blob bytes of each changed path:

```
2b7cebc8dbf18abc816d5e714f9d737db0320089f2bd809787fedc94e4427ead  tests/test_eval_panel_tool.py
4bc3bae53f78d747d69d5c4cca4cc39c7ac58d309fc4a3d4a9c453d39f3e1763  tools/v0a_eval_panel.py
```

Reconstructed with two-space separation, whole-row `LC_ALL=C` order and LF after
every row, the result is byte-identical to `manifest.sha256` and hashes to
`86a583d2...6926`, equal to the digest in `handoff.md` and `candidate.json`. The
sample packet reproduces identically to `d7903549...3510`; note its rows sort by
digest rather than by path, which is correct for whole-row sorting.

**Pinned bytes.** All 22 pinned inputs and receipts of the ownership packet and
all 16 of the sample packet hash to their stated digests, as do both deferred
`coverage.md` digests (`5d0c4c73...e4f5`, `9b481d76...129d`). Both
`focused-stderr.txt` and both `red-stderr.txt` are 0 bytes, and `e3b0c442...b855`
is the empty-input digest.

**Dependency provenance.** `inputs/dependencies.json` states
`"base": "f647a7989394f084875a040b20c41891168163ed"` and
`"scope": "direct semantic inventory, not transitive closure"`. All 34 pinned
blob ids resolve at that stated base and **not** at the candidate's immediate
parent: `tests/cases.json`, for example, is pinned at `53497f56` (the base)
whereas the candidate carries `8d81dd6c`. The file is therefore a direct
inventory at the original design base, exactly as it and the handoff declare. It
is explicitly not a closure and I did not treat it as one.

No mismatch of any kind was found. Utility arithmetic used
`D:/Pontius/.venv/Scripts/python.exe` (CPython 3.14) with `-B -P`, plus coreutils
`sha256sum` and read-only `git`. Reviewer arithmetic, not a test receipt.

---

## 2. Independent inventory, recorded before any deferred input

Written and hashed **before** opening `coverage.md`, `checks/`,
`inputs/prior-disposition.md`, `inputs/ownership-disposition.md`,
`inputs/repair-plan.md`, `inputs/authorization.md`, `inputs/workflow.md` or
`inputs/controller-rulings*.md`:

`inventory.md` sha256
`7b91277554f06b4c08acaeb595c98ec0a01750ea00d58f0e90a10fb48b9d096e`

It derives thirteen obligations (O1-O13) from brief criteria 1-3 and 9 and design
sections 1-3 and 6, maps them to eleven invariants (I1-I11) against exact frozen
line ranges, lists the related-path set, and records eight candidate observations
(C1-C8) plus hygiene measured from raw bytes. Findings M-02, M-03, M-04, A-01,
A-02 and A-03 below are C1, C3, C5, C4, C6 and C7 of that inventory; M-01 and
A-04 come from the same frozen-source pass.

Method: every source line was read via `git cat-file blob <commit>:<path>`. The
working tree is dirty (`STATUS.md`, `execution_journal.jsonl`) and was never used
as the candidate. No project code was imported, no test run, no tool invoked.

---

## 3. Obligation-by-obligation assessment of the frozen source

Line numbers are lines of the frozen blobs at `d8d291cc`.

**Admission (design 1; brief criteria 1-3).** `parse_plan` 89-98 bounds the plan
to 1..262144 bytes and refuses `NaN`, `Infinity` and `-Infinity` both as JSON
constants via `parse_constant` and as non-finite floats via `finite` 101-108.
`validate_plan` 111-170 enforces exact key-set equality per phase (119-120),
re-derives board, stacks, prefix, hand count, universe digest and the full seeded
permutation from the bridge (125-140), requires `runtime.python` to name the
executing interpreter (121-124), and uses `type(x) is int` so `True` cannot pass
as `stacks`, `hand_count` or `memory_mib`. Later-phase members such as a
seed/index bank are refused by the key-set rule, and the module docstring 3-8
states that as a deliberate phase-specific reading rather than a dropped field.
No default is supplied anywhere. **Satisfied.**

**Role-bearing admission and one schedule (sample contract).** `AdmittedPlan`
64-71 carries an immutable canonical wire string plus a tuple of
`ScheduledHand(role, board, hand)` (52-61). `validate_plan` returns it (170) and
short-circuits when handed one (114-115). The identical object is what
`supervise` serialises to the worker (368), what the worker iterates (271), what
`complete_sample` reconciles against (541), and what `full_pool_estimate` filters
by role (567). Declared-full admission compares role-bearing sets (163-169), so
relabelling a development hand as a control, emptying `development_hands`, or
rebinding the main board are all refused. `ScheduledHand.record_key` (57-61),
`drain`'s key (380) and `complete_sample`'s key (546) are the same triple of
role, formatted board tuple and hand name: I checked the three producers and
consumers agree on meaning, not merely on shape. **Satisfied. This is the shape
change the r004 root-cause note asked for, not another guard.**

**Cleanup lifetime and certification (ownership contract).** The native `Job` is
now acquired inside both the interrupt-deferred region and the cleanup `try`
(405), with an immediate `if report["status"] == "interrupted": raise
KeyboardInterrupt` (406-407), so an interrupted acquisition never proceeds to
launch a worker and still reaches `attempt("close job", job.close)` (479-480).
Every release is its own bounded `attempt` (441-450); the order is terminate,
kill, wait, join, close streams, drain, verify, close job (466-480);
`close_stream` (316-333) gives each stream one daemon closer and a bounded wait,
closing the gap carried from r004 where a synchronous `close()` could block the
record owner behind a live I/O thread. The certificate (483-485) is computed
outside and after `defer_interrupts`, and is the conjunction of
`resource_state_verified` (set by `verify` 452-457, before the job is closed) and
every cleanup outcome being `"ok"`. Since the deferring handler writes
`report["cleanup"]["console interrupt"] = "interrupted"` (306) and `attempt`
writes a non-`"ok"` value on any failure or interrupt, the certificate is
monotonic: nothing can restore it to true. I could not construct a schedule in
which a resource leaked, a release failed, or an interrupt was recorded, and
`cleanup_verified` was nevertheless true. **Satisfied.**

**Observation ownership under interruption.** `drain` 373-401 appends each
preflight record to `report["observations"]` at first receipt (384-386) and
mutates that same object thereafter; `missing_stages` (394-395) is a derived
annotation, not the ownership mechanism. There is no end-of-function merge, so an
unwind at any point after a stage arrives cannot lose it. `main` (590) owns the
dict it hands to `supervise` and writes it through `json_safe` (617), so a
non-finite float cannot make `finish_run`'s `allow_nan=False` writer refuse the
whole record. **Satisfied.**

**Boundary-artifact publication.** `retain_boundaries` 498-536 computes the
intended identity and registers a `publications[count]` entry in state
`"pending"` before the fallible write (513-514), moves it to `"publishing"`
between write and rename (517), and reconciles in a `finally` (519-529): if the
final path exists, its bytes are re-read and compared with the measured bytes
(`refuse`, 524) before the artifact is bound and only then removed from the
recoverable `boundary_base64`. If the loop raises, `boundary_retention` is set to
`"incomplete; recoverable encodings remain in boundary_base64"` (531-533). There
is no normal path on which the loop finishes with entries still pending, so
`"complete"` cannot be claimed while an encoding is unbound, and the function is
idempotent on retry. **Satisfied.**

**Worker execution, phase termination and estimate reconciliation.** `run_plan`
252-279 returns after the single capacity observation (270) and after the
preflight loop; there is no phase chaining. The deadline is checked between hands
(272-274) and the first failed comparison stops the phase (277-279).
`preflight_hand` 219-249 emits exactly the seven declared `STAGES` in the
declared order with per-stage elapsed, process CPU and traced peak (`measure`
200-210) and `cache_before`/`cache_after` from the unchanged ranker (213-216).
Production and its warm repeat both precede reference construction, so the
reference cannot secretly warm the production measurement, and the royal control
is scheduled last so it cannot pollute the development sample's cache.
`complete_sample` 539-553 requires each admitted unit exactly once, all seven
stages, observed completion and `comparison.passed is True`, including the royal
control, and `supervise` refuses to leave a preflight run `"completed"` when that
reconciliation fails (486-493). `full_pool_estimate` 556-573 estimates only under
`coverage == "declared-full"` after that same reconciliation, uses
development-role costs only, labels itself `kind="estimate"` and carries an
explicit assumptions string. **Satisfied.**

**One-run ownership.** `main` 576-622 calls `begin_run` once (588), creates the
run directory and `runtimes.json` and sets `context["output_directory"]` before
finishing (592-597), and calls `finish_run` exactly once in a `finally` (620), so
a failure, an interrupt and a success each yield exactly one result and one
journal line. The worker branch (583-584) never touches the journal, and
`execution.finish_run` independently returns early for an inherited context. No
per-hand admission, verification file or journal row is produced.
`report["plan_sha256"]` (599) binds the operator's raw plan bytes, and
`permutation_sha256` has two producers, `bridge.permutation_digest` in the worker
(267) and `hashlib.sha256(json.dumps(...))` in the parent (608-609). I confirmed
these are the same function of the same validated list of hand names, so the two
consumers of that value agree. **Satisfied.**

---

## 4. Findings

No Critical and no Important finding survived verification. The four Minor
findings carry recommended, not required, corrections; none defeats a stated
invariant of either contract, and none produces a false success, a lost
observation or an unbound artifact.

### M-01 (Minor) A console interrupt in the supervision loop can be relabelled failed

*Location:* `tools/v0a_eval_panel.py` 422-434 (check 426-427; stores 429-430 and
432-434), with 483-493.

*Invariant:* the terminal status of a run reports the actual terminating cause;
an operator interrupt recorded by the deferring handler is reported as an
interrupt.

*Counterexample:* the operator presses Ctrl-C while the loop is between line 426
and line 429. The comparison at 426 has already evaluated `False`; the handler
(304-307) then runs at one of the eval-loop checkpoints inside `process.poll()`,
`threads[0].is_alive()` or `events.empty()` and sets
`report["status"] = "interrupted"` and `cleanup["console interrupt"]`. Line 429
immediately overwrites the status with `"completed"`. Cleanup records the
interrupt, so `cleanup_verified` is `False` (485) and 490-493 flips the status to
`"failed"`. The retained result and the journal line read `status: "failed"` for
what was an operator interrupt, and the only trace of the cause is
`cleanup["console interrupt"]`. The same window exists against the budget store
at 432-434, where the status then stays `"budget_exhausted"`.

*Why Minor:* no false success is possible, the certificate is still false and the
exit code is still 1, and brief criterion 3 only requires that interruption stop
the phase and retain a failed or incomplete result, which it does. The defect is
in the label, not the outcome.

*Smallest correction:* make the terminal status monotonic the way the certificate
already is: after the deferral ends and before 490, set the status to
`"interrupted"` whenever `report["cleanup"].get("console interrupt")` is present.
Verify by injecting SIGINT between the 426 check and the 429 store through the
existing opcode-trace technique and asserting `status == "interrupted"`.

### M-02 (Minor) defer_interrupts can leave its non-raising handler installed

*Location:* `tools/v0a_eval_panel.py` 297-313 (guard at 300-302 and 312-313),
against the comment at 481-482.

*Invariant:* stated by the code's own comment at 481-482, the normal handler is
restored before the cleanup certificate is finalized, so a late console interrupt
unwinds instead of silently mutating the certificate's inputs. This is exactly
the ownership/r001 I-01 lifetime boundary.

*Counterexample:* `previous` is initialised to `None` and only assigned from
`signal.getsignal(SIGINT)`. `signal.getsignal` returns `None` when the current
handler was not installed from Python, for instance under an embedding host or a
C extension that called `signal()` for `SIGINT`. In that case `previous` stays
`None`, the deferring handler is installed at 308, and the `finally` at 312-313
skips restoration. From then on the process has no unwinding SIGINT handler: line
483's certificate is computed with deferral still active, and every later Ctrl-C
through `retain_boundaries`, `full_pool_estimate` and `finish_run` mutates a
stale `report` dict instead of unwinding. The guard conflates "not the main
thread" with "no Python-level handler to restore".

*Why Minor:* unreachable in the frozen supported invocation. Under CPython 3.14
running this file as `__main__` (625-626) or under pytest, `getsignal(SIGINT)`
returns `signal.default_int_handler`, so `previous` is never `None`. There is no
other caller of `defer_interrupts`.

*Smallest correction:* track installation with an explicit flag rather than
inferring it from `previous`, and decline to defer at all when `getsignal`
returns `None`, since restoration is then impossible through the Python API,
recording that deferral was not installed. Verify with a unit case that patches
`signal.getsignal` to return `None` and asserts the handler after the context
manager is the one that was there before.

### M-03 (Minor) An empty preflight schedule certifies sample_complete vacuously

*Location:* `tools/v0a_eval_panel.py` 149-169, 539-553, 486-489.

*Invariant:* `sample_complete` certifies that the admitted role-bearing sample
was actually executed and agreed; a preflight that measured nothing has not
completed a sample.

*Counterexample:* a plan with `"phase": "preflight"`, `"coverage":
"test-subset"`, `"development_hands": []` and `"controls": []`. Admission accepts
it: 153-156 checks only types, 161 checks distinctness over an empty set, and the
declared-full block at 163 is skipped, producing an empty `schedule`. `run_plan`
iterates nothing and the worker emits `ready` then `completed`. In the parent
`required` is `set()`, no preflight row is seen, and `complete_sample` returns
`{}`, which `is not None`, so `report["sample_complete"]` is `True` (487). The
run exits 0 with `status: "completed"`, `sample_complete: true` and zero
observations.

*Why Minor:* the record is not otherwise dishonest. `coverage` is
`"test-subset"`, `observations` is `[]`, the journal summary reads `preflight
completed; 0 observations`, and `full_pool_estimate` returns `not_estimated`, so
no measurement or authorization can be derived from it. But `sample_complete`
belongs to the same certificate family as `cleanup_verified`, and a vacuously
true certificate is the shape the r004 root-cause note set out to remove.

*Smallest correction:* refuse an empty schedule in preflight admission, or return
`None` from `complete_sample` when `required` is empty. Verify with an admission
case asserting `ValueError` for the empty-lists test-subset plan.

### M-04 (Minor) The dynamically loaded host module is keyed globally

*Location:* `tools/v0a_eval_panel.py` 79-86, exercised by
`tests/test_eval_panel_tool.py` 388-407.

*Invariant:* a tool instance rooted at a given tree executes that tree's host
module; the disposable-clone integration exercises the clone's code.

*Counterexample:* `load_host` caches the host under the constant `sys.modules`
key `"pontius_eval_panel_host"` and loads it from that tool instance's `ROOT`
only on the first call. `RealSupervisorTests` (235-314) drives the repository's
`TOOL` instance and populates that key with the repository's
`tools/v0a_table_host.py`. `RealRunOwnershipTests` (388-407) then loads a second
tool instance from a disposable clone under a different module name, but its
`self.tool.load_host()` returns the already-cached repository module. Both
classes run in one pytest process, so
`test_failed_last_release_cannot_certify_cleanup` and
`test_interrupt_at_native_job_acquisition_still_releases_the_job` patch and
exercise the repository's `Job`, not the snapshot's.

*Why Minor:* under the disposable-snapshot procedure the clone is a fresh
checkout of the same commit, so the two files are byte-identical and no receipt
is invalidated. The worker subprocess is still launched from the clone, since
`str(Path(__file__))` at 410 resolves to the clone's tool. Only the host module's
provenance is weaker than the test's docstring claims.

*Smallest correction:* derive the `sys.modules` key from `ROOT`, or bind the
loaded module to the tool instance rather than to a process-global name. Verify
by asserting `load_host().__file__` lies under that tool instance's `ROOT`.

### Advisory notes, no correction requested

- **A-01.** `full_pool_estimate` (556-573) reports production-only min, mean and
  max with its cache assumptions, but not the initialization cost that design
  section 3 asks the estimate to show. The number exists in the same result at
  `report["ready"]["initialization_cost"]` (260-261), so a reader must join two
  fields. Worth carrying into the estimate object when steps 4-7 land.
- **A-02.** If a boundary write succeeds and the rename does not (516-518), the
  `.partial` staging file is left in the run directory. Retention is correctly
  labelled incomplete and the bytes stay recoverable, but the orphan is never
  swept.
- **A-03.** `run_plan` 275 replays a fresh root whenever the unit board differs
  from the plan board, although `replay_root` depends only on `stacks`; the
  branch is a no-op that reads as if the root were board-dependent.
- **A-04.** `worker()` (282-294) emits `completed` and returns 0 even after
  `run_plan` has emitted a `failed` event for budget exhaustion (272-274) or a
  reference disagreement (277-279), so a retained result can show
  `worker_exit_code: 0` beside `status: "failed"`. The parent's classification is
  nonetheless correct, because the `failed` event is drained into `errors` before
  the completion branch at 428-430 can fire, that branch requiring
  `events.empty()`, and a non-empty `errors` forces `"failed"`. Having `run_plan`
  return its success to `worker()` would remove the contradiction.
- **G-01 (governance).** Measured from raw frozen bytes: 959 production lines
  (`eval_bridge.py` 333 plus `v0a_eval_panel.py` 626) and 799 test lines
  (`test_eval_bridge.py` 198 plus `test_eval_panel_tool.py` 601). Against the
  working figure in `inputs/controller-rulings-addendum-2.md` of 1,200 production
  and 600 test lines, with a hard ceiling of 3,000 production lines, production
  is within the figure and test is 199 lines over it. The brief's rule that an
  over-budget implementation returns to the controller before freeze is
  explicitly unchanged by both addenda. `coverage.md` discloses the overrun
  honestly and does not redefine the number, but justifies it as "within the
  controller's up-to-3,000-line correction authorization". That authorization is
  permission to spend up to 3,000 lines on the correction, and addendum 2 records
  the 3,000 as a ceiling on *production* lines for the whole slice; neither
  raises the 600-line *test* working figure. The overrun needs a controller
  number, not a reviewer's. It is reported as an open governance item and is not
  counted against the defect verdict, consistent with addendum 2's instruction
  that reviewers treat the budget as a controller decision.

---

## 5. Design verdict: SOUND

The r004 disposition's root-cause note identified two *state* contracts that had
been repaired as *control-flow* contracts, and named four shape changes. All four
are present in the frozen source, and each is an owning object rather than
another guard:

1. one role-bearing admitted schedule (`AdmittedPlan`, `ScheduledHand`) consumed
   unmodified by the worker, the reconciler and the estimator;
2. observation records attached to caller-owned storage at first receipt and
   mutated in place;
3. a cleanup certificate that is a conjunction of monotonic per-release outcomes,
   computed after the last release and after the interrupt-deferral lifetime
   ends;
4. a publication record spanning staging, rename and binding, reconciled against
   the actual file.

The two prior verdicts were STRAINED because the protected state was
reconstructed in several places. That is no longer true for any of these
contracts, which is why I do not carry STRAINED forward.

Residual strain, offered as advice and not as a finding: `supervise` (335-495)
still carries launch, supervision, cleanup, certification, sample reconciliation
and status arbitration in one 160-line function, and the certificate's
correctness is still *positional*, correct because line 483 is textually after
the `with` block. What keeps that acceptable is that
`test_console_interrupt_cannot_race_a_true_cleanup_certificate` (492-519) is a
real structural regression: it locates the assignment by source line and by every
compiler copy of the `STORE_SUBSCR`, so moving the certificate back inside the
deferral fails loudly rather than silently. If a further checkpoint extends this
function for design steps 4-7, extracting a `finalize_cleanup(report)` whose
precondition is "deferral ended" would convert that positional guarantee into a
structural one.

---

## 6. Comparison with the deferred coverage claims

| My inventory | Ownership coverage.md | Assessment |
|---|---|---|
| O9 / I7 acquisition inside protection | Invariant 1 | agrees, verified |
| O9 / I7 certificate after all inputs final | Invariant 2 | agrees, verified |
| O10 / I8 drained record owned at receipt | Invariant 3 | agrees, verified |
| carried r004 item: bounded stream close | Invariant 4 | agrees, verified |
| O11 / I9 identity registered before rename | Invariant 5 | agrees, verified |
| O12 / I2, I3 role-bearing admission | inherited sample | agrees, verified |
| O13 line budget | Size paragraph | disclosed, see G-01 |

The sample packet's four invariants match my I2, I3 and I11, and its Invariant 4,
a real declared-full execution producing the literal identities the estimator
needs, is exactly the end-to-end case the r004 root-cause note said was missing.
Both coverage documents state invariants and their falsifiers rather than listing
touched functions, which is what the disposition asked for.

Items I found that coverage does not claim: M-01, M-02, M-03, M-04 and A-01
through A-04. None is a coverage defect in the workflow's sense; each is either
unreachable in the supported runtime, an honest label question, or advice. Missing
coverage alone does not prove a product defect, and it does not here.

Coverage claims verified independently: "only two files change against rejected
r004, 486 additions and 118 deletions" is exact, since
`git diff --numstat 0bc19bc d8d291c` gives 255/12 and 231/106 over exactly those
two paths; the 959/799 line figures are exact; the 35-case and 33-case counts
reconcile as 24 plus 11 and 22 plus 11 module and bridge cases. Coverage's limits
paragraph is accurate: deterministic schedules establish correctness, not
external failure rates, and no performance or poker-strength claim is made.

---

## 7. Assessment of the supplied RED/GREEN receipts

**The ownership r002 RED is unusually strong.**
`b6ede27a2c737f2a77344908fb3ebe8a88088f54` has the sample candidate `72954e1` as
its sole parent, changes `tests/test_eval_panel_tool.py` only, and its test blob
`3c04043` is byte-identical to the GREEN candidate's test file, while its
`tools/v0a_eval_panel.py` blob `46eb71e` is the un-repaired parent's. The same
test bytes therefore run against pre-fix and post-fix production.
`red-stdout.txt` shows `run=24 errors=0 failures=2` and exactly the two intended
failures:

- `AssertionError: True is not false` carrying the cleanup map with
  `'console interrupt': 'interrupted'` and every other release `ok`, which is the
  false certificate;
- `AssertionError: Lists differ: [False] != [True]` for
  `"acquired native Job escaped cleanup protection"`.

Both are observed through the real result file written by the real journal
writer, not through the injector's bookkeeping, which satisfies the workflow's
controlled-failure-schedule rules; the injectors change timing and failure only,
never successful native or filesystem effects. The remaining 22 module cases plus
11 bridge cases pass, matching the journal's 35.

GREEN `focused-journal.jsonl` records the same command at
`source_commit: d8d291cc`, `status: passed`, `35 unittest cases exercised; 0
skipped; pytest exit 0`, `source_verified: true`, and `output_sha256 ab111704`
matching `checks/coordinator-verification.json`. Receipt arguments are
`-B -P -W error::ResourceWarning -p no:cacheprovider` on CPython 3.14.6 with a
scrubbed five-variable environment including absolute `PONTIUS_GIT`, as the
handoff requires. `lint.json` records `ruff check --no-cache` on both changed
files, exit 0.

**The sample r001 RED is a near-pair rather than an exact one, and the packet
does not hide it.** `beb069455a6d3ce20f202c0b4398683548631a33` also changes tests
only, on parent `182d14e`, but its test blob `23708fa` differs from the sample
GREEN's `db882cc`. The diff is mechanical: the two tests that touch the new
`AdmittedPlan` API, the estimator fixture case and the `fake_supervise` closure,
keep the old positional-coverage and raw-dict forms because the new API does not
exist in the RED production. Neither is a role-movement discriminator, so the
three discriminating subcases are unaffected. `red-stdout.txt` shows
`run=22 errors=0 failures=3`, all three `AssertionError: ValueError not raised`
from `test_declared_full_refuses_role_movement`, and coverage states plainly that
the real full-worker integration passes on RED, that is, that it is a positive
control and not the discriminator. That is an honest characterisation.

**What the receipts correctly do not establish.** The focused runs are
correctness evidence only. They are not a capacity, cost or preflight
measurement, not authorization for a full-pool solve, and not evidence of poker
strength; the roughly 258-second elapsed figures are test wall time, not per-hand
cost. The disclosed `ee98f51f` locator diagnostic is retained with its own
receipt and explicitly not counted as a product RED, and I agree: its stdout
shows a test-side instruction-locator failure, not a production defect.

---

## 8. Line counts and hygiene, measured from raw frozen bytes

| File | Lines | Non-blank | Bytes | Longest |
|---|---|---|---|---|
| `tools/v0a_eval_panel.py` | 626 | 555 | 29,775 | 100 |
| `tests/test_eval_panel_tool.py` | 601 | 528 | 30,352 | 100 |
| `src/pontius/eval_bridge.py` (unchanged) | 333 | 283 | 14,500 | 99 |
| `tests/test_eval_bridge.py` (unchanged) | 198 | 171 | 10,782 | 100 |

Both manifest files: LF only, zero CRLF sequences, final newline present, no
trailing whitespace on any line, no tab characters, no non-ASCII bytes, and no
line over 100 columns. Ruff clean per `checks/lint.json`. Slice totals and the
budget position are in G-01.

---

## 9. Prohibited sources, and one disclosure

I did not open, list the contents of, grep or tail any of the following:

- any `reviews/` directory in any packet, including
  `v0a-eval-panel-ownership/r002/reviews/`,
  `v0a-eval-panel-sample/r001/reviews/`,
  `v0a-eval-panel-ownership/r001/reviews/`, and any under
  `v0a-eval-panel-code/`, `v0a-eval-panel-design/` or `v0a-eval-panel-impl/`;
- `D:/Pontius-handoffs/progress.md` or `D:/Pontius-handoffs/INDEX.md`;
- `checks/review-01-inventory.md` or `checks/review-02-inventory.md` in either
  packet. A plain directory listing showed their file names and sizes; no byte of
  their contents was read;
- any implementer transcript or session log.

I ran no project code: no pytest, no import of any `pontius` module, no
invocation of the tool or the owners, no `uv` or `pip`. All git use was read-only
(`rev-parse`, `cat-file`, `ls-tree`, `diff-tree`, `diff`). Nothing under
`D:/Pontius` or `D:/Pontius-handoffs` was modified.

**Disclosure.** After my inventory was written and hashed, and after my own
findings list was fixed, I read `disposition.md` and `ready-for-claude.md` at both
packet roots. Those two files are not on the prohibition list, but they do state
the sibling Codex passes' verdicts, both CLEAN / SOUND, and the sibling review and
inventory digests. I record this so the controller can weigh it. Every finding
above was derived from the frozen source before those files were opened, and M-01
through M-04 are not claims either sibling disposition makes. If the coordinator
judges that this compromises independence, the correct remedy is a fresh reviewer
context, and I say so rather than leaving it unstated.

---

## 10. Verdict

**CLEAN.** No required correction remains unresolved. Zero Critical, zero
Important. Four Minor findings and five Advisory notes are recorded above with
recommended corrections; the test-line overrun against the 600-line working
figure is an open governance item for the controller, not a defect in this
candidate.

**SOUND.** The shape now matches the state contracts it has to hold, for the
reasons in section 5.

This pass is one Tier C cold review of
`d8d291cc1f813ce798f2d3a990b2a8bf2297e124` and its parent
`72954e1331c9b191d927c1c4b82f277bcd322a4c`. It is not adoption, and not
authorization for broad suites, a retained measurement, a full-pool solve, an
integration commit or any public publication.
