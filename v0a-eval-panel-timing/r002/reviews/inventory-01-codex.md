# Independent cold-review inventory 01

Candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968
Base: 9fce4bfba3acf1c34938aa47f37f9743e5011cea
Tree: d26c3fb14959562a03b10e09fd746e317009d91b
Manifest SHA-256: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2

Recorded before reading coverage.md or any checks/ contents. No verdict is supplied here.
The dispatch and environment were automatically visible; no prior review or verdict was exposed.
System skill instructions were read in addition to the packet's permitted review inputs.

## Identity and allowed scope

The named ref resolves to the candidate. Its sole parent and tree equal the pinned identities.
Git diff reports only tests/test_eval_panel_tool.py (153 added, 4 removed) and
 tools/v0a_eval_panel.py (19 added, 12 removed): 188 changed lines, below 300.
The whole-row ordinal-sorted LF manifest was regenerated from raw Git blob bytes and matches
both manifest.sha256 bytes and its pinned digest. All 16 dependency Git blob pins match.
The six initial supporting-input hashes match the handoff pins, including the current brief.
The current README and brief require Python 3.14.6 despite the archived dual-runtime labels.

## Requirements and independent falsifiers

1. One callable invocation, original return identity, untraced elapsed and process CPU body cost.
   Falsifiers: real is_tracing() true inside body; duplicate invocation; replaced return;
   deterministic clock advances in postcheck/teardown included in the published body cost.
2. Existing tracing is rejected before invocation and remains owned by the external caller.
   A tracer active after a successful body prevents publishing an untraced record.
   Falsifiers: external tracer stopped, body entered while tracing, or mislabeled cost emitted.
   Body exceptions must propagate without retry or a success cost; no cleanup owns a tracer.
3. Every cost carries timing_mode=untraced-body-v1, traced_peak_bytes=null and
   traced_peak_status=not_collected. Job memory stays a separate actual observed metric.
   Falsifiers: omitted metadata, zero substituted for unknown memory, or a fabricated Job peak.
4. Forecasts select each admitted development production cost only after role, completeness,
   stage and comparison checks. Missing/unknown/traced timing or contradictory memory metadata
   refuses estimation. A valid forecast names its mode and cold/cache/sample assumptions.
   Falsifiers: one incompatible row admitted; legacy metadata relabeled; control/warm cost used;
   incomplete or failed comparison forecast; changed min/mean/max arithmetic.
5. Initialization, capacity and all seven per-hand stages retain the contract in real JSON and
   persisted result output. Falsifiers: a caller bypasses measure; payload building is timed;
   JSON drops null/status/mode; final result loses stages or changes estimator provenance.
6. Correctness controls preserve real worker, native Job limits and cleanup effects. The two
   budget-dependent fixtures must prove reference entry and retain completed production.
   Falsifiers: fake worker/Job success, no entry marker, successful completion accepted as kill,
   indefinite test hold, altered supervisor deadline, or weakened native cleanup assertions.

## Producer, caller and consumer inventory

Frozen tools/v0a_eval_panel.py:
- measure, lines 201-210: sole timing producer; clock endpoints precede exit tracer check.
- preflight_hand.stage, lines 224-230: captures cache outside measurement and emits payload
  only after measure returns. Seven stages: production, production_warm,
  reference_construction, forced_check, forced_bet, best_response and comparison.
- run_plan, lines 252-280: initialization replay_root and capacity_probe use measure;
  preflight preserves production-before-warm-before-reference order and original sample order.
- worker, lines 287-303: json_safe and JSON line serialization preserve null/mode/status;
  exceptions emit failed and exit nonzero. No tracing controller is installed here.
- supervise receive/drain, lines 363-418: transfers ready and nested stage/capacity costs;
  report owns observations; Job peak comes from the host rather than traced allocations.
- complete_sample, lines 536-553: same admitted role/board/hand schedule; exact stage set,
  unique records, complete=True and comparison.passed=True required.
- full_pool_estimate, lines 556-582: development-role production costs only; timing admission
  follows completeness; min/mean/max scale by hero count; capacity and test-subset remain gated.
- main, lines 585-633: passes estimator output and collected observations through json_safe to
  finish_run. No automatic full-pool execution is present.

Frozen src/pontius/eval_bridge.py provides replay_root, capacity_probe, hand_totals,
build_reference, forced_value, reference_best_response and validate_reference. These are
internal synchronous callables. Their source contains no tracing start/stop operations.
Their evaluator, kernel, codec and ranker dependencies are unchanged. A raw Git grep over
src and tools finds tracing operations only in the panel and unrelated
v0a_blueprint_workload_measure.py; the panel does not import that workload tool.
The worker's threading is supervisor transport in another process, not a tracer controller.
Concurrent external toggling or a plugin body starting and stopping tracing is expressly
outside this helper's promised detection model. No reachable internal toggler was found.

Frozen src/pontius/execution.py:122-169 writes the full report as strict JSON, then binds its
actual SHA-256 in the one journal row. status_generation append/render consume journal
metadata, not stage costs; they do not reinterpret the timing mode.
Frozen tools/v0a_table_host.py supplies the Job's native peak_memory interface, unchanged.

## Independent planned evidence assessment

Inspect TimingTests for real tracing state, return identity, invocation count, exception
identity and controlled clock changes with independent expected 3 elapsed / 2 CPU seconds.
Inspect WorkerTests for real initialization/capacity and seven-stage costs, and mutate each
provenance field in one otherwise complete development input. Preserve legacy sample checks.
Inspect RealRunOwnershipTests for real worker -> supervisor -> result.json -> json.loads,
all declared development hands plus control, exact stages, estimator metadata and native peak.
Inspect the profile-trigger fixture for real subprocess containment and positive entry marker.
Then read deferred coverage and pinned RED/GREEN receipts, binding test/source identities,
runtime, command, import roots, scrubbed environment, outcome and limitation to this inventory.
No fresh project execution is permitted, so receipts can only establish supplied execution.

## Actions and limitations before deferred reads

Read only initial allowed packet files and frozen Git source, plus system skill documentation.
No reviews/, progress.md, INDEX.md, disposition/readiness file, sibling scratch, other packet,
transcript or conversation history was opened. No shared scratch directory was crawled.
An attempted absolute Python 3.14.6 utility process was denied by the local execution layer.
It ran no project code. Raw-byte verification instead succeeded using PowerShell/.NET and Git.
No tests, project imports, dependency installs, hooks, measurements or source writes occurred.
Only this assigned create-only output file has been written.
