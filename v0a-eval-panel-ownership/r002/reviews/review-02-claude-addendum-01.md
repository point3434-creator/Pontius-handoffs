# Addendum 01 to cold review 02 — Claude — v0a-eval-panel-ownership/r002

Appended 2026-09-09 after reviews 03 and 04 and the completeness critique. The
original review-02-claude.md is unchanged; this is a new record, not an overwrite,
as the workflow requires.

Candidate: `d8d291cc1f813ce798f2d3a990b2a8bf2297e124` (unchanged).

## What this addendum does

It files one finding that my pass missed and that I now judge **Important**, and it
records the standalone measurement that establishes its magnitude. My original verdict
of CLEAN was issued without noticing it; I withdraw that verdict's completeness claim.
Whether the candidate is CLEAN is the finalizer's ruling, not mine to re-issue.

The finding was first raised by the completeness critic (`completeness-critique.md`,
D-01), which had both cold reviewers' inventories and their Minor/Advisory titles and
was asked what both had missed. I verified it independently against the frozen blob and
measured it before recording it here.

## I-01 (new, Important) — timings are measured under `tracemalloc`

Every reported time is measured with allocation tracing running, and the full-pool
estimate multiplies those inflated times by 1,081 without disclosing it.

Location: `tools/v0a_eval_panel.py:200-210` (`measure`), consumed at `226-228`
(`preflight_hand.stage`), `258` and `264` (`run_plan`), and `566-573`
(`full_pool_estimate`). Present unchanged since `v0a-eval-panel-code/r001`; not a
regression introduced by this repair.

Frozen source:

```
200  def measure(function):
202      tracemalloc.start()
203      started, cpu = time.perf_counter(), time.process_time()
204      try:
205          value = function()
206      finally:
207          _, traced_peak = tracemalloc.get_traced_memory()
208          tracemalloc.stop()
209      return value, dict(elapsed_seconds=time.perf_counter() - started,
210                         cpu_seconds=time.process_time() - cpu, ...)
```

Tracing is started before the clock (202-203) and the clock is read after tracing is
torn down (209), so `elapsed_seconds` covers the whole body running under per-allocation
tracing *plus* the `get_traced_memory()`/`stop()` teardown.

Violated requirement: brief criterion 2 at BASE `f647a798` — "Record cold/warm context,
time, work counts and memory where observed; distinguish measurements from estimates."
The tool distinguishes its estimate from its measurements, but the measurements
themselves are inflated by the instrument and nothing in the result says so. The
`assumptions` string at 572-573 names only the cold/warm cache, production-only scope
and the sample-only reference.

Concrete scenario: a `declared-full` preflight. `bridge.hand_totals` enumerates 990
villains per hand, allocating a strengths list and two settlement results per villain —
allocation-dominated work, the worst case for `tracemalloc`. The four inflated
`production` elapsed values are stored by `drain` (390-395), read by
`full_pool_estimate` (566) and multiplied by `hero_count = 1081` (568-571). A controller
sizing the full-pool solve from `production_seconds_min/mean/max` reads a projection
several times larger than the uninstrumented cost, with nothing in the report to warn
them.

Magnitude — reviewer arithmetic, not a test receipt: `checks/tracemalloc-overhead.py`
(standalone, no project code, CPython 3.14.6) times an allocation-shaped loop of 990
iterations with and without tracing, reading the clock exactly as `measure` does. Two
runs: **3.17x** and **3.18x** inflation (0.36 ms → 1.14 ms, best-of-200). Output in
`checks/tracemalloc-overhead.txt`. This is indicative of the magnitude on
allocation-dominated work; it is not a measurement of the tool, which no one is
authorized to run.

Note this also means the r001 development diagnostic figures (0.06-0.35 s/hand, full
H approximately 1-6 min) are instrumented figures and overstate the real cost.

Why Important rather than Minor: the per-hand cost measurement and the full-pool
estimate are the reason design steps 2-3 exist — they are the input to the controller's
full-pool launch decision, and the project's protocol forbids unmeasured walls. A
decision input that is systematically wrong by a factor of about three, undisclosed, is
material even though nothing crashes.

Why a finalizer could reasonably rule it Minor: the bias is conservative. The estimate
overstates cost, so it cannot cause an under-resourced launch; it can only make the
full pool look more expensive than it is. The tool never claims the timings are
uninstrumented. On that reading it is a disclosure defect on a fail-safe number.

Smallest correction (not implemented here): read the clock before tearing down the
tracer and stop tracing before timing the body — or, better, take the two measurements
separately, since the platform memory peak the report certifies comes from the job
object (`423-424`), not from `tracemalloc`, so tracing is not load-bearing for the
stages whose time feeds the estimate. If tracing must stay inside the timed window,
say so in the `assumptions` string and in the stage cost records.

Verification the correction needs: one case asserting that a stage's
`elapsed_seconds` excludes tracer teardown, and one asserting the estimate's
`assumptions` names the instrumentation state of its inputs.

## Effect on my original findings

M-01 (`defer_interrupts` None sentinel) and M-02 (unguarded stderr reader) are
independently confirmed by both cold passes (03 M-01/M-02, 04 M-02). The critique's
S-1 strengthens M-01: with the deferring handler still installed, a SIGINT during the
certificate's `all(...)` iteration at 483-485 inserts a key into `report["cleanup"]`
while it is being iterated, raising `RuntimeError: dictionary changed size during
iteration` outside every `try`. That path requires the C-installed-handler precondition,
which is unreachable from the tool's own entry, so M-01 stays Minor — but its stated
consequence is now a falsified comment-asserted invariant, not only a leaked handler.

My A-01 (interrupt inside the retention reconcile) stands. Reviews 03 and 04 add the
orphan `.partial` file on a failed rename (03 M-04, 04 A-02), which I did not catch.

## Disclosure

I am the author of the rejected r004 and of its root-cause note; reviews 03 and 04 were
run precisely because my pass was not fully independent. This addendum was written after
reading both of their reports and the critique.
