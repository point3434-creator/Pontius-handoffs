# Eval-panel timing correction

Tier C: measurement provenance and the full-pool resource-decision input.
Parent: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
The controller authorized fixing the timing contract on 2026-09-09 after the
finalizer specified untraced primary timing and explicit estimator provenance.
Scope: tools/v0a_eval_panel.py and tests/test_eval_panel_tool.py only.
Budget: 300 changed lines, two source-review rounds before returning to controller.

Acceptance:
1. Primary elapsed and process CPU costs describe a single invocation of the
   callable without allocation tracing; clocks stop before postprocessing.
2. The helper refuses pre-existing tracing before invoking the callable, leaves
   that tracing owned by its caller, and refuses an active tracer found afterward.
3. Cost records explicitly identify the timing mode and mark traced peak memory
   as not collected. The real worker Job peak remains the observed memory metric.
4. Full-pool estimates require compatible timing metadata on every selected
   development-hand production input. Missing, traced or unknown input modes
   produce not_estimated, never an untraced forecast. Estimates name their mode
   and assumptions. Existing role/completeness/comparison checks remain active.
5. Initialization, capacity, all seven per-hand stages, and persisted estimator
   outputs carry this contract through actual production callers and serialization.

Oracle: real tracemalloc.is_tracing inside the callable, its actual return value
and call count, independently controlled body/teardown clock advances, and real
stage/result JSON. No ratio from a synthetic allocation benchmark is a test oracle.
No sleep threshold or claimed performance improvement is required for acceptance.

Design: retain one invocation and the original cold/warm ordering. Check tracer
state at entry, time the body once, stop clocks, then check state before publishing
an explicitly untraced-body-v1 cost. Do not start/stop a tracer owned elsewhere.
Keep traced_peak_bytes with null and traced_peak_status=not_collected so absence
cannot be read as zero memory. Native Job memory remains separate and unchanged.
The estimator admits only the same mode with these unavailable-memory markers;
it does not retrofit provenance onto legacy results.

Rejected: a fixed overhead divisor (not calibrated for the solver), moving only
the end clock (leaves tracing active in the body), and an undisclosed second call
for memory (would alter cache state and side effects). Separately measured traced
allocation data can be designed later if needed; it is not required by this fix.

The helper's callers are known internal functions, not arbitrary plugin code.
Entry/exit checks are not a continuous monitor for arbitrary concurrent toggling
or a callable starting and stopping its own tracer. Inventory all current callers
and tracing operations to verify that this is not a reachable internal behavior.

Tests: valid RED using the new assertions on unchanged production, integrated
GREEN on the corrected candidate, two independent cold Tier C passes, then the
registered broad harness. All executions use fresh locked dev snapshots and
CPython 3.14.6, -B -P, explicit root/src/tests import paths, absolute PONTIUS_GIT
with PATH absent, and strict resource/unraisable warnings. Only correctness tests
are authorized; no retained cost preflight, full-pool solve, source adoption or
public push. Existing arithmetic, ownership, sample policy and history remain.

Dependencies: the accepted measured-resource decision before design steps 4-7
waits on this correction. Unrelated work may proceed. Adopt only after review and
tests plus explicit controller authority. Return for redesign or reauthorization
if a material finding survives the second round. Separate reviewer scratch roots,
create-only inventory files and explicit allowed-input lists protect cold reviews.

The initial timing correction exposed two cutoff-dependent cleanup fixtures:
uninstrumented work could complete before their six-second budget. Preserve their
native cleanup assertions by holding the actual worker at reference entry through
a test-only profile callback. The callback writes a marker and waits at most 30
seconds; the unchanged six-second supervisor budget must terminate the real Job.
Missing entry markers fail the case. No successful resource effect is simulated.
