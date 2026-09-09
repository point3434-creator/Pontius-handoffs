# Independent inventory: reviewer 02

Candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968
Base and sole parent: 9fce4bfba3acf1c34938aa47f37f9743e5011cea
Tree: d26c3fb14959562a03b10e09fd746e317009d91b
Manifest: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2

This inventory was written before opening coverage.md or checks/. Inputs were the
handoff, candidate, manifest, brief, six permitted supporting inputs and frozen Git source.
No prohibited exposure occurred. No other reviewer output or prior verdict was read.

## Identity and scope

The review ref resolves to the candidate, whose sole parent and tree match candidate.json.
Raw Git blob hashes reproduce the whole-row ordinal-sorted LF-only manifest exactly.
All 16 dependencies match their declared frozen blob hashes. The six supporting file
hashes match the handoff. Scope is exactly tools/v0a_eval_panel.py and
 tests/test_eval_panel_tool.py (172 insertions, 16 deletions; 188 changed lines <= 300).
Current README and workflow make CPython 3.14.6 controlling over older runtime labels.

## Requirements and independent falsifiers

1. Single invocation, body without allocation tracing, exact returned object preserved.
   Refuse tracing already active before invocation; never stop caller-owned tracing.
   Stop both clocks before the exit tracing check, dictionary creation and event emission.
   Fail if tracing remains active after the callable; no mislabeled cost may escape.
   A body exception must propagate without replay or a published success cost.
2. Every cost carries timing_mode=untraced-body-v1, traced_peak_bytes=null and
   traced_peak_status=not_collected. Null cannot silently become zero observed memory.
   Native Job peak remains separate from unavailable traced allocation memory.
3. All selected development production costs require compatible provenance before any
   estimate is emitted. Missing mode, traced mode, unknown mode and inconsistent memory
   markers must return not_estimated. Reject one bad input even when others are valid.
   Existing exact role membership, completion, seven-stage and comparison checks stay.
   Test-subset cannot obtain a full-pool forecast; control costs are not selected inputs.
   Retain production-only min/mean/max arithmetic and explicit cache/order assumptions.
4. Exercise actual initialization, capacity, seven per-hand stages and final JSON paths.
   No hidden second call, cache reordering, changed teacher or arithmetic oracle.
5. Deterministic cleanup triggers hold actual build_reference entry, prove entry with
   a marker, then let the unchanged six-second supervisor stop the actual native Job.
   The 30-second hold is bounded. Neither successful cleanup nor memory is simulated.
   Missing markers or a live worker/failed cleanup must fail the independent assertions.

## Producer, caller and consumer paths

Frozen locations below refer to the candidate. These are direct semantic dependencies,
not a claim of complete transitive source review.

- tools/v0a_eval_panel.py:201-210: measure owns entry/body/end-clock/exit-check ordering.
- :221-249: preflight_hand.stage measures and then packages the result. Seven stages are
  production, production_warm, reference_construction, forced_check, forced_bet,
  best_response and comparison. Cache reads and payload conversion are outside timing.
- :251-279: run_plan measures replay_root initialization and capacity_probe; production
  runs before its warm repetition and reference. Controls remain separate role records.
- src/pontius/eval_bridge.py: replay_root, capacity_probe, hand_totals, build_reference,
  forced_value, reference_best_response and validate_reference implement measured bodies.
  Their dependencies include river, evaluation, betting, continuation and blueprint codec.
- Frozen git grep over src, tools and tests finds allocation-tracing mutations only in
  the unrelated tools/v0a_blueprint_workload_measure.py and explicit timing tests.
  No eval-panel production caller starts/stops tracemalloc or imports that workload tool.
  Entry/exit checks are sufficient for these internal paths, not continuous monitoring
  of arbitrary plugin functions or concurrent external toggling (explicitly out of scope).
- tools/v0a_eval_panel.py:282-296 serializes JSON-safe stage events to worker stdout.
  supervise.receive/drain at :357-411 reads JSON and preserves costs in stages and ready.
  Native peak comes from host.Job.peak_memory and remains peak_job_memory_bytes.
- :536-553 complete_sample checks exact admitted keys, duplicates, completion, stage set
  and reference comparison; :556-582 selects development production costs and estimates.
- :585-634 main invokes the estimator, applies json_safe and sends the entire report to
  execution.finish_run. src/pontius/execution.py:122-162 writes result.json, binds its
  digest in one journal row and renders status. status_generation.py displays that row's
  summary/duration, without interpreting or replacing stage timing provenance.
- tools/v0a_table_host.py:377-381 reads the native Job peak through its existing API.

## Oracle inspection and remaining verification

TimingTests uses actual tracemalloc state, actual object identity and invocation counts.
Controlled clocks advance independently for body, checks and teardown, allowing the old
implementation's traced body and included teardown to be falsified deterministically.
WorkerTests examines actual worker function events; RealRunOwnershipTests reads real
result JSON from a real supervised worker and checks all persisted per-hand cost markers,
selected estimate arithmetic, and positive Job peak. Cost compatibility fixtures also
check a non-first selected input. Existing partial/role/comparison controls remain.
The profile wrapper is only in the two cleanup fixtures and matches actual frozen source
filename/function before holding; it does not fabricate the supervisor's outcome.

Next compare this inventory with the deferred coverage and hash-verified receipts. Need
establish valid RED on unchanged production, GREEN bound to corrected frozen source,
CPython 3.14.6 identity, isolated locked imports and strict warnings, plus limited claims.
No project code, tests, measurements, installers, hooks or source/ref changes were run.
The permitted absolute utility Python failed to launch with Access is denied; no code
ran. PowerShell/.NET raw-byte hashing completed the utility verification instead.
