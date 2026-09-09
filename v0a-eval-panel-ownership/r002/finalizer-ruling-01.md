# Finalizer ruling 01: I-01 timing instrumentation

Date: 2026-09-09. Finalizer: Codex. This is an attributed ruling, not a cold review.
Ownership candidate: d8d291cc1f813ce798f2d3a990b2a8bf2297e124.
Ownership manifest:
86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926.
Descendant candidate: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
Descendant manifest:
d05fd7b821fec534044eeb80acdf23a4fe09767373a67e4cde20bc5ba1bed088.

## Ruling

I-01 is CONFIRMED and IMPORTANT. Overall readiness for the intended cost
preflight is NOT CLEAN until the measurement contract is corrected. The design
remains SOUND; a bounded measurement correction is appropriate. No finding in
this ruling changes the poker arithmetic or reopens the ownership/sample repair.

This record supersedes aggregate readiness claims to the extent that they imply
no material unresolved cost-measurement defect. Earlier reports and receipts
remain unchanged. The independent reviews of the three-file workload/Git
correction at 9fce4bf retain their bounded conclusions. That candidate inherits
the unchanged eval-panel timing defect, so its passing broad gate does not make
the combined source ready for the intended preflight decision.

## Verified mechanism and requirement

Read the Claude review-02 addendum, its standalone script/output, the frozen
measure() and its stage/capacity/initialization callers, full_pool_estimate(),
the accepted implementation brief and design, and the contamination disclosures.
Git confirms tools/v0a_eval_panel.py is unchanged between d8d291cc and 9fce4bf.

At frozen tools/v0a_eval_panel.py:200-210, allocation tracing starts before the
start clocks. The body runs while tracing is active. The end clocks are read
after get_traced_memory() and stop(). Reported elapsed and CPU times therefore
include the traced workload and tracer teardown. This statement applies to the
measure()-produced costs, not every separately recorded wall-clock metric.

At lines 566-573 the declared-full estimate takes development-hand production
elapsed values and scales their min/mean/max by hero_count. Its assumptions name
cache reuse and production/reference scope but omit instrumentation. The cost
record's traced_peak_bytes shows that tracing occurred; it does not explicitly
define the timing window or the target execution mode of the estimate.

The accepted brief criterion 2 requires recorded costs and a distinction between
measurements and estimates. Design section 3 requires separate cost attribution,
cache/runtime context and an estimate supporting a later resource decision. It
expressly says the estimate is not a feasibility proof or an elapsed-time upper
bound. The undisclosed measurement/target mismatch is material to that decision.

The observed durations are valid observations of instrumented execution. They
are not established observations or calibrated estimates of an untraced solve.
Calling them simply wrong obscures the actual correction: define and preserve
the measurement conditions through the estimator and its consumer.

## Magnitude and its limits

The retained reviewer output reports 3.18x on a synthetic allocation-shaped loop.
I reran the exact standalone script with the absolute CPython 3.14.6 interpreter,
-I -B, no project imports, exit 0. Output was:

    plain best-of-200: 0.352 ms
    traced best-of-200: 1.132 ms
    inflation factor: 3.21x
    overhead per call: 0.780 ms

This corroborates substantial overhead for that diagnostic only. It does not
measure the actual solver, establish its slowdown factor, or prove that a real
full-pool run is three times faster. No retained preflight or project benchmark
was executed for this ruling. Do not divide old timings by 3.18 or 3.21.
The historical diagnostic must be labeled instrumented; its untraced cost is
unknown until measured under the intended conditions. Preserve original bytes.

## Why Important, despite a plausible conservative direction

The cost projection exists to support the controller's resource decision.
Undisclosed overhead can cause a feasible campaign to be declined, delayed or
needlessly reduced. Avoiding an under-resourced launch does not make that decision
input immaterial. Also, the sample projection is explicitly not an upper bound;
one synthetic overhead ratio cannot establish a conservative bound for a future
full-pool run with different cache, allocation and instrumentation conditions.
Severity rests on that contract and use, not on treating 3.21x as a solver fact.

## Required correction and verification outcomes

1. Define the timed execution mode and clock boundaries explicitly. A body-only
   metric must stop both clocks before instrumentation teardown or reporting.
2. Make each cost record and derived estimate state their instrumentation mode.
   An untraced production forecast requires matching untraced timing inputs.
   Alternatively, explicitly target traced execution and exclude any claim that
   the result forecasts an untraced production run.
3. Prefer untraced primary cost timing and the existing native Job memory peak.
   Traced allocation metrics may be unavailable or collected separately with
   explicit provenance. A second invocation is not harmless: preserve labeled
   cold/warm conditions and do not secretly warm the primary timing sample.
4. Add a behavioral check of the real tracer state inside the measured callable,
   and a controlled clock-order check excluding teardown from body-only timing.
   Verify serialized cost metadata reaches the actual estimate/assumptions, and
   that incompatible or legacy inputs cannot silently acquire an untraced claim.
5. Freeze a new candidate and obtain the applicable reviews and focused/broad
   verification. Preserve old source, results and verdicts as historical records.

These are required outcomes; separate timing/memory passes are an option, not a
mandated implementation. Moving only the end clock before stop() is insufficient
to remove tracing overhead from the body. A fixed empirical divisor is not a fix.
No production source was changed or additional source/run authority inferred here.

## Review independence and publication

Reviews 03 and 04 are useful disclosed-exposure reviews. Do not describe them as
two perfectly cold independent passes: 03 saw a sibling inventory; 04 saw sibling
verdicts after fixing its initial findings. Their pre-exposure inventories remain
useful evidence, but their existence cannot prove that exposure had no influence.
The completeness critic is synthesis, not an additional cold reviewer.

For the next source candidate, use unique per-reviewer scratch roots and filenames,
create-only inventory writes, and an explicit allowed-input list. Exclude all
verdict-bearing dispositions/readiness notes regardless of filename. Give each
reviewer only its own output location; hash its inventory before deferred reads.
These are coordination corrections, not proof that the underlying harness changed.
No new review is needed merely to increase the pass count on superseded bytes.

The controller alone authorizes publication. This ruling supports publishing the
review record with I-01 retained as Important and readiness NOT CLEAN; it does not
authorize a commit, public push, source adoption or retained measurement.
