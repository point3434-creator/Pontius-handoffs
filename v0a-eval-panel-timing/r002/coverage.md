# Deferred timing FIX coverage

Category: every measure()-produced cost and every production cost consumed by
full_pool_estimate. Discovery: raw source search for measure, tracemalloc,
traced_peak_bytes and production_seconds; trace the three call sites through
worker events, parent drain, estimator selection and result JSON retention.

| Surface | Required observation | Falsifier |
| --- | --- | --- |
| Helper body | Real tracer off, one call, unchanged return/exception | Tracing active or repeat |
| Existing tracer | Refusal before body; tracer remains caller-owned | Body runs or tracer stopped |
| Body starts tracer | No untraced cost returned; tracer remains owned | Mislabeled accepted cost |
| Clock boundaries | Body advances 3 wall/2 CPU; postchecks excluded | Postcheck/teardown counted |
| Initialization | ready.initialization_cost declares mode and null memory | Missing mode or zero |
| Capacity | Observation cost declares the same mode | Inconsistent wire record |
| Seven stages | Every emitted stage declares mode and null traced peak | One hidden traced stage |
| Estimator | Every development production cost has matching provenance | Legacy input estimated |
| Role/completion | Existing sample/comparison rules still apply | Control substituted or partial |
| Persisted result | Real worker JSON preserves cost and estimate metadata | Labels lost on drain |
| Memory | Actual worker Job peak positive, traced allocation unavailable | Null mistaken for zero |

The clock schedule controls time readings and assigns large costs to a real
tracer stop and real tracer-state checks. It does not invent a measured speedup.
The saved native tracemalloc functions remain the implementation of state/stop;
the helper under test executes normally. A clock read after a postcheck or tracer
teardown produces a larger duration and fails the independent 3/2 expectation.
Separate real-state tests prevent a correctly timed but still traced body from
passing. No millisecond threshold or diagnostic overhead multiplier is a gate.

Existing estimator fixtures acquire explicit new metadata rather than silently
changing their claimed meaning. Negative cases remove mode/memory fields or mark
them incompatible; those results must not expose a production forecast. Their
arithmetic remains the independent 0.5 seconds * 1081 = 540.5 seconds example.
The actual five-hand native integration checks the serialized production costs,
all stage metadata, Job memory and the derived forecast from the completed roles.
It is disposable correctness evidence, not an authorized retained measurement.

Every known helper caller is an internal function: root replay, capacity probe,
or the seven stage operations. A repository scan finds no tracemalloc state
mutation in their library call graph. The unrelated blueprint workload measuring
tool owns its own tracer and is not invoked by the eval-panel worker. Entry/exit
checks do not claim to detect arbitrary concurrent on/off toggles or a plugin
body restoring state before return; this worker exposes no such callback API.

No traced-memory replay is added, so call counts, cache order and production/
reference separation remain. The change intentionally makes traced_peak_bytes
null with an explicit not_collected status. Native Job peak reporting remains.
Historical costs/results retain their original bytes and labels. This patch
does not derive untraced solver costs from the synthetic overhead diagnostic.

RED and GREEN test blobs must be identical. RED production must equal the parent.
The passing focused receipt covers the eval bridge and the changed tool suite;
post-review broad execution is a separate later gate. The helper's exception
behavior still propagates the actual original exception and retains completed
stages through the existing owner. Unrelated prior Minor findings are unchanged.

## Cutoff fixture correction and preliminary evidence

The first corrected candidate cedc41f passed the five timing-contract cases and
metadata integration checks, but two old cleanup tests assumed a worker could
not finish within six seconds. Its actual worker completed, so the asserted
budget-exhaustion trigger did not occur. Keep that failed receipt as preliminary
evidence; do not relabel it GREEN or treat it as a new cleanup defect.

Those two cases now launch the frozen production worker via a test-only runpy
wrapper. A profile callback recognizes entry to the real build_reference function,
disables itself, writes an independently read marker and waits at most 30 seconds.
The real supervisor's unchanged six-second deadline kills the actual worker Job.
Before this hold, real initialization and production stages run and emit their
normal records. The launch observer delegates native Popen and containment; it
does not fabricate cleanup, worker exit, stage data or comparison outcomes. Tests
require exactly one controlled launch, the entry marker, the existing native
release outcomes and the actual retained completed production stage. The marker
proves the requested reference-entry schedule occurred; a missing marker fails.
These are controlled-failure correctness records, not representative cost samples.
The original pause-free five-hand integration remains the timing/estimate control.
