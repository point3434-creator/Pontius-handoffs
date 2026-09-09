# Cold review 01: eval-panel timing correction

Defect verdict: CLEAN.
Design verdict: SOUND.
No required correction or material coverage finding survives this bounded review.

Candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968
Base: 9fce4bfba3acf1c34938aa47f37f9743e5011cea
Tree: d26c3fb14959562a03b10e09fd746e317009d91b
Manifest SHA-256: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2
Inventory: inventory-01-codex.md
Inventory SHA-256: 90fb8d0a82b36c261a997c6fc86d3f456c7e9b6c450154c7afe05d62ff4338ae

This is a cold, read-only source review supported by authenticated supplied correctness
receipts. It is not a fresh reviewer test execution, broad-suite pass, measurement,
resource-decision approval, source adoption or authorization to solve the full pool.

## Findings and design assessment

No Important, Critical or required Minor finding was established against the scoped timing
contract. No redesign is recommended. The bounded helper and explicit producer/consumer
metadata make the contract readable at its existing boundaries without adding a second
invocation, tracer ownership machinery or a new measurement framework.

The design's stated limitation is appropriate for the inspected internal call graph: entry
and exit checks cannot observe an external tracer that starts and stops wholly inside the
body interval. The current source contains no reachable internal tracer toggler. Arbitrary
plugin callbacks or concurrent external tracer interference are outside the accepted contract.
A callable that raises publishes no cost and propagates its original exception; the helper
has no reason to stop an external tracer or retry work on that path.

## Identity and scope verification

The review ref resolves to the exact candidate. Raw commit inspection, repeated with
--no-replace-objects, confirms the sole parent and tree above. The diff contains only the two
authorized files: tests/test_eval_panel_tool.py +153/-4 and tools/v0a_eval_panel.py +19/-12.
The cumulative 188 changed lines are below the 300-line correction budget.

Using raw Git stdout bytes through PowerShell/.NET, I independently regenerated SHA-256
blob rows, sorted complete rows ordinally, appended LF and compared the entire manifest
byte-for-byte. Both its bytes and pinned digest match. All 16 dependency blob pins and all
six initially pinned supporting-input hashes match. Deferred coverage and all 18 checks
file hashes match the handoff pins. Frozen changed files pass LF-only, no-BOM, <=100-column
and no-trailing-whitespace checks. git diff --check also passes.

## Requirement-to-evidence assessment

1. Single untraced body and endpoints: tools/v0a_eval_panel.py:201-210 checks entry state,
   samples both clocks, invokes once, samples endpoints, then checks exit state. Payload
   construction and tracer postcheck occur after the endpoint samples. TimingTests checks
   real tracing state, unchanged return identity, one invocation and original exception.
   The independent controlled-clock oracle expects 3 elapsed and 2 CPU seconds. RED instead
   observed 1003/502 because old tracer teardown was included; GREEN covers the correction.
2. External tracing ownership: the two explicit refusal tests start a real tracer outside
   the helper or as its body. They require refusal, no entry when already tracing, and
   retained tracer state. Production neither starts nor stops tracing. Tests restore the
   tracer they own in finally blocks.
3. Memory and timing metadata: the producer sets untraced-body-v1, null traced_peak_bytes
   and not_collected. WorkerTests checks initialization, capacity and each emitted stage.
   The unchanged host Job query remains the source of peak_job_memory_bytes; native
   integration requires that observed peak to be positive.
4. Forecast admission: tools/v0a_eval_panel.py:556-582 retains coverage and complete_sample
   gates, then checks every selected development-role production cost's timing mode and
   both unavailable-memory markers. The test mutates a later development row, removing
   mode or memory metadata or supplying traced/unknown/incompatible values, and requires
   not_estimated with no production forecast. The independent 0.5 * 1081 = 540.5 oracle
   preserves arithmetic. Completeness, comparison, role and test-subset gates remain.
5. Production and persistence: measure has three current call sites: initialization,
   capacity and preflight_hand.stage. That stage helper serves all seven declared stages.
   Cache reads, output payloads and event serialization follow measurement; the original
   production/warm/reference order remains. Worker JSON, supervise.drain, main.json_safe
   and execution.finish_run preserve nested costs and estimator fields. The real five-hand
   integration at tests/test_eval_panel_tool.py:582-608 reads result.json, checks actual
   roles and completed stage sets, all stage metadata, forecast metadata/arithmetic and
   real Job memory. Its run_and_read helper also checks the journal's result-byte digest.
6. Cutoff controls: tests/test_eval_panel_tool.py:347-380 wraps the actual worker entry with
   runpy and a profile callback. It observes the exact build_reference entry, disables
   itself, writes an entry marker and waits at most 30 seconds. Native Popen and the same
   suspended Job assignment remain active. The two callers retain the six-second budget,
   require the marker and retain their native cleanup/partial-production assertions.
   The wrapper controls the failure trigger; it supplies no successful resource outcome.

The independent inventory and deferred coverage describe the same relevant population and
failure mechanisms. Source searches covered measure/tracemalloc/estimator fields across the
frozen panel, its library and tools surfaces. Tracing mutation occurs in an unrelated
blueprint workload tool, which is not imported by this worker. The unchanged execution and
status-generation writer/consumer paths were inspected; status rendering does not interpret
stage costs. No overlooked current timing caller or contradictory estimator consumer was
found. Existing mathematical, ownership and sample-policy behavior remains outside the
production delta and is supported only to the extent exercised by the focused suites.

## Supplied execution evidence

The RED commit is 370cab05902cd2c79745f68c3be4a609bee31cd4. Its only delta from the parent is
the test file. Its test Git blob equals the candidate test blob exactly:
d55cb4fdb8bb177774be968731328be86fc72121.
Its production tool blob equals the parent's exactly:
378ea931f3adb144f1c3f32bee0f38f7e7ceb39c.
RED stdout reports five timing failures and four missing-metadata errors, 29 cases, no skips,
pytest exit 1. These failures are the intended contract defects, not dependency refusal.

The candidate focused receipt selects eval_panel_tool or eval_bridge through the registered
pytest harness. It reports 2 parameterized suites passed, 44 deselected, 40 unittest cases,
zero skipped and exit 0. Its journal source_commit equals this candidate and source_verified
is true. Journal and summary agree on output digest:
82f7d27443b1424d201625416c3e599c9a48ace33799868f610eb809256ff2a0.
The pinned lint receipt records ruff 0.16.5, both changed paths and exit 0.

The preliminary failed receipt remains a failure. Its timing cases and metadata integration
passed; the two old budget fixtures did not reach their assumed budget-exhaustion state.
The final fixture change targets that observed trigger failure and retains cleanup checks.
I did not infer a speedup or representative cost from any correctness-test duration.

The inspected snapshot script creates a fresh detached snapshot, syncs the locked dev group,
checks CPython 3.14.6, clears the child environment, sets absolute PONTIUS_GIT with PATH absent,
and uses -B -P, explicit root/src/tests import paths and strict resource/unraisable warnings.
Receipts identify separate RED and candidate snapshot roots and matching commands. I did not
open those snapshots, rerun the script, or independently reopen retained result artifacts;
the permitted summaries/journals bind those artifacts but are supplied evidence.

## Review actions, limitations and exposure

Executed only read-only Git inspection, packet reads, PowerShell/.NET raw-byte hashes and
text-format checks, plus create-only writes in the assigned reviewer root. A utility launch
of the prescribed absolute Python 3.14.6 interpreter was denied by the execution layer;
it ran no code, and .NET verification succeeded instead. No other interpreter was used.
No project code, tests, uv/pip, hooks, retained measurement, commit, push or ref mutation ran.
No source, packet, ledger or sibling scratch path was written or crawled.

The independent inventory was created and hashed before opening coverage.md or checks/.
No reviews/ directory, progress.md, INDEX.md, disposition/readiness document, prior verdict,
other packet, implementer transcript or conversation history was opened. Automatic context
contained only the dispatch/environment and tool/skill instructions. The permitted deferred
coverage text includes a nonspecific sentence about unchanged prior Minor findings; it
exposes no finding or verdict details. I did not follow that reference or use it as evidence.
System code-verification skill documentation was also read to structure the review.

CLEAN applies only to the frozen commit and manifest pair above. The broad harness, measured
resource decision and explicit controller adoption authority remain separate later gates.
