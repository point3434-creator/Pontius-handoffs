# Completeness critique — v0a-eval-panel-ownership/r002 (not a cold pass)

Author: Opus 5 agent, spawned by the coordinator after reviews 03 and 04 returned.
Candidate: d8d291cc1f813ce798f2d3a990b2a8bf2297e124.

**This is not an independent cold review and must not be counted as a Tier C pass.**
It was given both cold reviewers' invariant inventories and the titles of their
Minor/Advisory items (no reports, no verdicts, no severities beyond those titles),
and asked one question: what did both of them miss? It then checked its own
suspicions against the frozen blobs. It ran no project code and made no writes.

---

I read both frozen blobs plus the four related-path files that carry the untraced consumers
(`eval_bridge.py`, `execution.py`, `status_generation.py`, `v0a_table_host.py`) at the same commit,
all via `git cat-file blob`. Nothing was run.

---

# Completeness critique — d8d291cc

## A. What neither inventory mentions at all

Functions/branches absent from both lists: `refuse` (74-76), `finite` (101-108), **`json_safe`
(189-197)**, **`measure` (200-210)**, `main`'s run-directory/`runtimes.json` block (592-597) and
finalization block (616-622), and three report fields — `peak_job_memory_bytes` (350, 423-424),
**`worker_seconds` (494)**, **`permutation_sha256` (608-609)**. R03's twenty invariants and R04's
thirteen obligations both stop at the boundary of *what is measured*; neither asks **how** it is
measured or **who reads the number afterwards**.

---

## B. Actual defect neither reviewer found

### D-01 [Minor] Every reported time is measured with `tracemalloc` running, and the full-pool
estimate multiplies that instrumented time by 1081 without disclosing it —
`tools/v0a_eval_panel.py:200-210`, propagated at `226-228`, `264-266`, `566-573`

`measure` starts allocation tracing *before* it starts the clock and stops it *before* it computes
the elapsed figure:

```
202  tracemalloc.start()
203  started, cpu = time.perf_counter(), time.process_time()
205      value = function()
207      _, traced_peak = tracemalloc.get_traced_memory()
208      tracemalloc.stop()
209  return value, dict(elapsed_seconds=time.perf_counter() - started,
210      cpu_seconds=time.process_time() - cpu, traced_peak_bytes=traced_peak)
```

So `elapsed_seconds`/`cpu_seconds` cover (a) the whole body running under per-allocation tracing and
(b) the `get_traced_memory()` + `tracemalloc.stop()` teardown at 207-208, which is inside the timed
window because the clock is only read at 209-210.

Every timing in the report comes through this one function: each of the seven per-hand stages
(`preflight_hand:226`), the capacity probe (`run_plan:264`), and the initialization cost
(`run_plan:258`).

**Concrete scenario.** A `declared-full` preflight run. `bridge.hand_totals`
(eval_bridge.py:207-233) loops 990 villains, allocating a `strengths` list, two `settle()` results
and their `net_returns` per villain — roughly 4×990 short-lived objects per hand, the worst case for
`tracemalloc`, which on CPython typically costs ~2× on allocation-dominated code. Those four
inflated `production` elapsed values are stored by `drain` (390-395), read back by
`full_pool_estimate:566`, and multiplied by `hero_count = 1081` at 568-571 to produce
`production_seconds_min / _mean / _max`. The `assumptions` string at 572-573 discloses only
cold/warm caching, production-only, and the sample-only reference — **it does not say the sample was
timed under instrumentation**, and no other report field does either. A reader sizing the slice from
`full_pool_estimate` gets a projection that can be roughly double the uninstrumented cost, with
nothing in the report to warn them.

This is not covered by "estimate-not-proof" (R04 O7) or by R04 A-01 (omitted initialization cost):
those concern what the estimate *leaves out*. This concerns the *sample values themselves* being
systematically wrong in a stated direction. It is also independently avoidable — the platform memory
peak the report actually certifies comes from the job object (`423-424`,
`v0a_table_host.py:377-381`), not from `tracemalloc`, so the tracer is not load-bearing for the
stages whose time feeds the estimate. The docstring at 201 ("the platform peak is the job's") shows
the author knew the two memory sources coexist but did not draw the timing consequence.

### D-02 [Advisory] `worker_seconds` is not the worker's seconds and can exceed the declared budget
on a report that certifies clean cleanup — `tools/v0a_eval_panel.py:352`, `432-434`, `459`, `471`,
`494`

`started` is taken at 352, *before* `host.Job(...)` (405), `Popen` (409-413) and `job.resume` (421);
`report["worker_seconds"]` is computed at 494, *after* the entire `finally` block. That block can
legitimately consume `process.wait(timeout=10)` (471) plus the shared 10-second join/close deadline
(459, 462, 476). A `budget_exhausted` run with `resource.seconds = 600` and a slow-exiting worker
therefore reports `worker_seconds ≈ 620` — about 20 s over its own declared budget — on a report
whose `cleanup` entries are all `"ok"`.

The report also mixes two clocks with no field saying so: `worker_seconds` and
`peak_job_memory_bytes` are the **parent's** measurements, while `ready.initialization_cost` (260)
and every stage `cost` (227) are the **child's** `time.perf_counter()`. A consumer summing stage
costs and comparing against `worker_seconds` is comparing across processes.

Fail-closed check: this cannot corrupt a certificate — the demotion at 490-493 keys on
`status`/`errors`/`cleanup_verified`, never on `worker_seconds`. It is a labelling defect in a
reported number, not a soundness hole.

---

## C. Interactions between the two repaired contracts — checked, and they hold

These are the admission→cleanup/reporting seams the question asks about. I traced each and they are
correct; here is the evidence.

**C-1. `role` is produced by admission and consumed in four unrelated places; all four agree.**
`validate_plan` stamps `"development"` (157) and `"control"` (159) into `ScheduledHand.role`. It is
then read by (i) `run_plan:271`'s positional unpack `for label, unit_board, hero in
admitted.schedule` — position 0 of the NamedTuple, so `label` *is* `role`; (ii) `preflight_hand:221`
`label=label`, emitted on every stage and on `hand_completed`; (iii) `complete_sample:541,546`,
where `required` comes from `ScheduledHand.record_key` (58-61, position 0 = `self.role`) and the
observed key from `row["label"]`; (iv) `full_pool_estimate:567`'s `if unit.role == "development"`
filter. The board/hand halves also match exactly: admission stores `board_cards(...)` and
`tuple(sorted(parse_cards(*names)))` (173-180), `record_key` formats them with
`format_card`/`hand_name`, and `preflight_hand:221-223` formats the *same tuples* with the same two
functions. No divergence.

The `role` filter at 567 is load-bearing and correct: the royal control (46) sits on a *different
board*, so its `production` stage re-misses the entire `lru_cache(maxsize=200_000)` on
`river._evaluate_seven_cached` (river.py:164-165) and is a cold outlier; excluding controls from
`costs` is right.

**C-2. Off-schedule observations are fail-closed.** `drain` (379-397) creates a preflight record for
*any* stage event without consulting the schedule — but `complete_sample:548` returns `None` on `key
not in required`, which sets `sample_complete = False` (487), appends the error at 489, and demotes
at 490-493. An event for a hand admission never admitted cannot produce a `completed` status.

**C-3. The two independent admissions produce the same schedule.** The parent admits at `main:600`,
`supervise:344` early-returns on `isinstance(plan, AdmittedPlan)` (114-115), and `send:368` ships
`admitted.document`; the **child re-derives its own schedule** at `worker:288` and `run_plan:255`.
So `complete_sample`'s `required` and the worker's execution order come from two separate
`validate_plan` calls. They agree because `sample_identity` (173-180) is deterministic and the
ordering (development in plan order, then controls in plan order) is fixed — but note R03's I-14,
"the single admitted schedule shared by all consumers," is literally false: it is two derivations
from one wire snapshot, equal by determinism rather than by sharing.

**C-4. The child's plan ingestion is weaker than the parent's, and it does not matter.**
`worker:287` uses bare `json.loads(sys.stdin.readline())` — no `PLAN_LIMIT`, no `parse_constant`, no
`finite()` (all of which live only in `parse_plan`, 89-98, which the child never calls), and
`request["seconds"]` at 289 is used unchecked. I checked whether a nonfinite value could survive: it
cannot. `validate_plan` type-checks or equality-checks every admitted key (116-169), and each of the
two escape hatches is independently caught — a non-finite `resource.seconds` by `math.isfinite` at
145, and a non-finite deadline by the parent's own budget kill at 432. Unexamined, correct.

**C-5. The report's two `permutation_sha256` fields are consistent.** `main:608-609` hashes
`json.dumps(plan["permutation"])`; the capacity observation at `run_plan:267` carries
`bridge.permutation_digest(permutation)`, which is `sha256(json.dumps([hand_name(h) for h in
permutation]))` (eval_bridge.py:157-158). Same function, same default separators, and
`validate_plan:137-140` refuses unless `plan["permutation"]` is exactly `[hand_name(h) for h in
order]` for the same seed and universe that 263 recomputes. The digests are equal. Neither reviewer
traced this; it turns out fine.

**C-6. The un-`require_declared_root`'d second replay is safe.** `run_plan:259` checks the primary
root; the control-board re-replay at 275 is never passed through `require_declared_root`. That is
covered downstream: `hand_totals:209` and `build_reference:238` both call `bet_action`, which calls
`require_declared_root` (eval_bridge.py:117-120), exactly as the `replay_root` docstring claims at
79-80. Every hand re-checks. Not a defect.

**C-7. The stderr thread is deliberately excluded from the completion condition, and the demotion
covers it.** Line 428 tests only `threads[0]` (stdout), so the loop can set `status = "completed"`
at 429-430 while `receive_errors` (362-364) is still appending. The `finally` joins **all** threads
(472-473) before line 490 re-reads `errors`, and any join that times out is recorded as a cleanup
failure, which falsifies `cleanup_verified` (485) and demotes anyway. A late stderr line cannot
survive into a `completed` report. Unexamined, correct.

**C-8. `cleanup_verified` cannot be certified vacuously.** `all(...)` over an empty
`report["cleanup"]` is `True` (485), but `resource_state_verified` (351) is only ever set by
`verify()` (452-457), which is attempted at 478 — inside the `if process is not None` block, after
every release. When `process is None` the certificate is `False and True` = `False`. Also `process
is not None ⟹ job is not None` (405 precedes 409), so `verify`'s `job.active()` cannot hit a `None`
handle, and `Job.close` (v0a_table_host.py:443-446) always runs after `verify`.

---

## D. Strengthenings of items they did file

**S-1. R03 M-01 / R04 M-02 are worse than "the handler leaks."** Both filed the 300-302/312-313
guard: if `signal.getsignal(SIGINT)` returns `None` (a handler installed from C), `previous is None`
and the deferring handler is never removed. Neither connected that to the invariant the code
*asserts in a comment* at 481-482 — "The normal handler must be restored before finalizing this
certificate. A late console interrupt then unwinds instead of silently changing its inputs
mid-store." With the handler still installed, a Ctrl+C during line 485 runs `interrupted()`
(304-306), which **inserts a key into `report["cleanup"]` while line 485 is iterating
`report["cleanup"].values()`** → `RuntimeError: dictionary changed size during iteration`. Lines
483-495 sit outside every `try`, so that escapes `supervise` with `report["status"]` still
`"completed"` from 429-430, and it escapes *before* `retain_boundaries` (604), so capacity artifacts
are never written. In the frozen tool `main:614` corrects the status to `failed`, and the boundary
bytes survive in `boundary_base64` — but the docstring at 341-342 explicitly invites external
callers to own `report`, and such a caller is handed a `completed` report with no reconciliation
performed. The named consequence is a demonstrable falsification of a comment-asserted invariant,
not just a leaked handler.

**S-2. R03 M-02's silent-drop shape applies to `send` too.** `receive_errors` (362-364) has no
handler at all; `send` (366-371) catches only `(BrokenPipeError, OSError)`. A `TypeError` from
`json.dumps` at 368 kills the send thread silently, the child blocks forever on `stdin.readline()`
(287), and the run ends as `budget_exhausted` at 432-434. Less severe than M-02 (it is recorded, not
silent), but the same missing-guard pattern in a third thread.

**S-3. R03 A-05 / R04 M-03 (vacuous empty sample) reach the ledger.** I confirmed the path is
reachable: `coverage: "test-subset"` with `development_hands: []` and `controls: []` passes 153-156,
yields `sample = ()` at 149, passes the distinctness check at 161 (`0 == 0`), skips 163-169, and
`complete_sample` returns `{}` — which is `is not None`, so `sample_complete = True` at 487. What
neither traced is where that lands: `main:618-620` writes `summary = "preflight completed; 0
observations"` into `execution_journal.jsonl` via `finish_run` (execution.py:142-161) with `status:
"completed"` and `source_verified: true`, and it renders into `STATUS.md`
(status_generation.py:68-78). The mitigation is that "0 observations" is literally in the rendered
summary text, so the row is visually distinguishable — worth stating, since it bounds how bad
A-05/M-03 actually are.

---

## E. Out-of-slice, for the record

`finish_run` (execution.py:162) calls `render_status`, which re-parses and re-validates **every**
historical journal line (`read_runs`, 38-50) and raises on the first invalid one — *after* this
run's line has already been appended at 161. A single corrupt legacy row therefore makes every
future `main()` crash out of its `finally` (620) before printing its report (621), with the run
recorded. Not in the frozen changed files, but it is a consumer of `main`'s finalization that
neither inventory's related-path set traced through.

---

## Bottom line

One new defect worth filing (**D-01**, Minor: instrumented timings propagated into the full-pool
estimate undisclosed), one new advisory (**D-02**, `worker_seconds` scope/label and the two mixed
time bases), and three strengthenings (**S-1** is the most consequential — it converts M-01/M-02
from a hygiene leak into a falsified invariant with an escape path through unprotected code at
483-495). The two repaired contracts do **not** have a hole between them: the
role→record_key→estimator chain (C-1), the off-schedule fail-closed path (C-2), the dual-admission
determinism (C-3), and the two `permutation_sha256` fields (C-5) all check out against the frozen
bytes. The reviewers' combined coverage of the *state* is genuinely complete; what fell between them
is the *measurement apparatus* and the *report fields nobody consumes inside the tool*.
