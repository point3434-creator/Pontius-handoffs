# Gate A R1 harness engineering review — codex A v1

Reviewer: codex/r010_cold_a. This is a bounded engineering review of the harness, not a cold implementation review or an implementation CLEAN verdict.

Disposition: no material static blocker to root dispatch of the first actual CPython 3.11.15 Gate A run. Runtime behavior remains unverified by this reviewer. The existing successful, matching floor receipt requirement still governs any 3.14.6 run; a completed semantic RED does not unlock development-slot replication.

## Frozen input and custody

H commit: f6d9d79e5b9820bffa946193983e193d896575d4.

- Preparation manifest: ee8e0c23a53ed9aee251d9551b8319d248523585b7010ca628543df2d765d4d3.
- Design manifest v2: 18fdd632f5eeb3f414ac9e5160b9b276ef9dca0830f60ae13ca1f774b78dd55f.
- Early population: 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce.
- Probe: c0672ac61fa19b5dd3d46fc6c0dbbdaae4565c610e7e658619c738559fb27395.
- Controller: 9310da3cecabaae0127fb6562a15b388355f722c35dcd5abbd2b039fd0f4d48c.
- Harness plan: 8cec0f3af002f04b20c82dee62d29f0601a87047249ab2dfcde5a164ca73826d.
- Observer map: af8df00ceb6b02bb5730eee56754ce78badcab6102ce861d726eed704522bfbd.
- Author static record: 49414e161aca661bc6c3c302564b5982759ca5ec23618b71dd0cba19568ada97.
- Handoff: cdea6c9dcd3cb91755223178e9114b026edc5625849d641a2d58dbcedd5756d6.
- Probe predecessor diff: a9078e6be36c468a321b2484e4ddcb6ed1986a54e290466dd3ff0778cbba88a2.
- Controller predecessor diff: 4763694e0430cd0abd84c7a946b343236419e8dc2184ee00f569d959b7847b5c.
- Coordinator plan disposition: 64fbb4b0690d5555c6eebd7b96d0e8129115df01d44c4441e95cb8d98dd177a8.

Independent read-only Git cat-file verification matched both manifests and their listed local bytes against this commit: 45 distinct files, including both manifests. Absolute validated Git was used in owner context with global/system configuration disabled per process; no safe.directory or other configuration was changed.

## Requirement-to-evidence review

| Requirement | Independent static result |
| --- | --- |
| Fixed Gate A population | All six complete case-record hashes, source hashes, Model hashes and classifications match the frozen population. Exactly eight separate Model projections are selected: 2 required-clean, 3 required-refuse, 1 permitted-refusal case. No Gate B or new source schedule is dispatched. |
| Real unchanged public boundaries | Storage public function body/signature equals the original storage envelope AST after only its definition-name rename. Name-environment public envelope is unchanged by AST. Both independent Model runners match their predecessors. Sensitive source is passed to derive_design_review; only the separately authored harmless Models are compiled/executed. Each projection gets a fresh namespace. |
| Expectations independent of candidate | Clean argv, blocker requirements, traces, exception-class results and unreachable-event checks remain case-bound. Probe/controller load_cases, public_verdict and budget validator ASTs agree. The exact raw predecessor diffs regenerate byte-for-byte. |
| Original budget and refusal behavior | Probe lines 278–442 wrap original _AnalysisBudget.__init__/consume, not production semantics. Original calls delegate exactly once; throwing requests are recorded and reraised. The exact consume source segment is pinned at d910a8af42711e5130b93af9e55b8917dbd8b48433e29e1ab3cd51df63b7af5c. All five caps are checked before/after, with no refund/reset/split/cap edit. Scalar epochs distinguish reused object IDs; request, origin, phase and throwing totals reconcile. Wrapper method/code identity restoration is checked. |
| Exact source and environment | Controller lines 384 onward require retained T candidate path/hash, separate explicit core-worktree watch and fixed old-worktree watch. It creates a fresh D-local r010 detached clone, overlays only the pinned generator and harness files, verifies all 1761 tracked files, and binds complete before/after manifests and original input watches. Actual patch-level CPython, executable, flags, seed0, cwd, snapshot/src PYTHONPATH, scrubbed environment and Git identity are checked before candidate import. |
| Floor-first custody | Controller lines 435–521 require a successful exact-int-zero, complete, intact, matching 3.11 receipt before 3.14. It rehashes the floor's source/configuration pins, raw stdout/stderr/log/setup, identity, six results/eight projections, accounting and snapshot. A new development snapshot is required. |
| No false success on interruption/infrastructure error | Controller lines 274–381 independently reconstruct the complete result and exact exit status. The 60-second direct-child watchdog kills a timed-out child; timeout/negative exit, missing or malformed records, oracle/analyzer/accounting errors, incomplete restoration or changed files cannot produce success. Raw outputs and error receipts are retained. An intact semantic RED is distinct from infrastructure failure and is not a passing receipt. |

## Provenance clarification and limits

The observer-map field observer_class_source_sha256 hashes the author's literal OBSERVER fragment, including three helper definitions plus BudgetObserver and surrounding LF, rather than the class AST source segment alone. Its exact hash is a686ac14f297a228b9357a75215f6320697995d85ec3cf25f2ab70e8e13fa585. The reconciliation hash 2e8bc49b2aecf7696c6ad829dcd18cee1a985c10b39d0d03bb6b951aaf86636f likewise includes the literal's surrounding LF. I independently extracted these literals with ast.literal_eval, reproduced both hashes and verified both fragments occur verbatim in the pinned probe. My initial class-segment-only comparison therefore used a different boundary; it was not a stale-input or product failure. The map's field name is imprecise, but this does not require changed runtime inputs.

The observer counts original charged units, not all physical work. Candidate import precedes observation; it must remain free of unauthorized analysis side effects. Its source accounting remains a separate review obligation. Observer stack traversal/bookkeeping is extra runtime overhead, and no timing result follows from these counters. last_observed_work is the initial value or last observed consume value, not a retained budget's end-of-life read.

Phase labels are descriptive. In particular, budget_phase recognizes the exact name review_flow, while r010 uses _source_ordered_review_flow; otherwise-unrecognized work remains other with caller/parent and creation/throw context. This does not remove its charges from totals, but other must not be interpreted as absence of body analysis.

The controller bounds the direct child, not the entire controller plus Git/cleanup or arbitrary descendant processes. The reviewed probe/Models do not spawn payload descendants. Gate A success would characterize these six cases only and does not certify accounting completeness, Gate B headroom, the whole canonical rewrite, broad acceptance or final release.

Verification performed: full source/diff/plan/map review; own isolated stdlib AST, canonical-data and SHA-256 comparisons; read-only Git blob comparison. No generator, probe, controller, sensitive fixture or Model payload was imported or executed; no runtime checks were launched. No source, tests, candidate, existing evidence or worktree files were edited. Only this create-only review was retained.
