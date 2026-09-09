# Cold review: reviewer 02

Defect verdict: CLEAN
Design verdict: SOUND

Candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968
Base and sole parent: 9fce4bfba3acf1c34938aa47f37f9743e5011cea
Tree: d26c3fb14959562a03b10e09fd746e317009d91b
Manifest: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2
Ref: refs/heads/review/v0a-eval-panel-timing/r002
Inventory SHA-256: 2ad786b3d0c8e00e12e9e373eddaf4b01fd0433d45a5ca66a2a49975582c114a
Coverage SHA-256: b3170f0dca6c43a713830d75545f5c93ccd62838bc7146fc6ff074b1fdf894e0

## Findings and design assessment

No Critical, Important or Minor required correction identified in the bounded timing fix.
No advisory change is needed for this candidate. CLEAN is a source-review conclusion;
it is not a broad test pass, retained resource measurement, source adoption or authority
for a full-pool invocation.

SOUND: one helper enforces the timing contract at all three production call sites, and
one estimator admission check protects the changed meaning at its actual consumer.
The implementation retains one invocation and the original stage/cache ordering. Explicit
unavailable-memory markers prevent the absence of traced allocation from claiming zero
memory. Native Job memory remains independently observed. This fits the internal-callable
contract without introducing an unnecessary second execution or lifecycle framework.

## Acceptance evidence

All source locations below bind to the candidate identified above.

1. tools/v0a_eval_panel.py:201-210 checks the real tracer state before reading start
   clocks or invoking the callable, executes the body once, captures elapsed and CPU
   ends, and only then checks exit tracer state and constructs the cost record. It never
   starts or stops tracemalloc. A pre-existing tracer stays owned by its caller; a body
   leaving tracing active cannot return an untraced cost. Exceptions propagate directly,
   without another invocation or a successful cost. TimingTests at tests/
   test_eval_panel_tool.py:140-217 observes real tracing, object identity, call count,
   original exception identity and independent body/check/teardown clock advances.
2. tools/v0a_eval_panel.py:208-210 emits timing_mode=untraced-body-v1,
   traced_peak_bytes=null and traced_peak_status=not_collected. Its stage wrapper at
   :221-249 packages payload/cache observations only after measurement. Initialization
   and capacity use the same helper at :258 and :264. The seven stages retain their
   existing production, warm, reference, forced-action, response and comparison order.
3. tools/v0a_eval_panel.py:556-582 preserves coverage and complete_sample gates, then
   selects every admitted development production cost. Each must have exactly the
   compatible mode and unavailable-memory markers before min/mean/max arithmetic runs.
   One incompatible selected input refuses the estimate. Unknown/legacy provenance is
   not retrofitted. The output names its mode and production/cache assumptions. Existing
   role, duplicate, completeness and reference-comparison checks at :536-553 remain.
   The fixture at tests/test_eval_panel_tool.py:274-313 independently expects 540.5
   seconds for 0.5 * 1081 and invalidates a non-first input across seven metadata cases.
4. The production path preserves costs through worker JSON, supervise.receive/drain,
   report assembly, json_safe and execution.finish_run's strict result.json writer.
   Initialization remains in ready, capacity in observations and each hand's seven
   costs in stages. Job.peak_memory uses the existing native query; the report keeps
   peak_job_memory_bytes separately. RealRunOwnershipTests at :580-608 reads the real
   worker's persisted result and checks stage metadata, selected arithmetic and positive
   Job memory. WorkerTests additionally checks initialization/capacity emitted costs.
5. The test-only reference hold at tests/test_eval_panel_tool.py:347-378 delegates to
   real Popen with the actual worker target and native containment flags. Its profile
   callback matches the real build_reference source/function, disables itself, writes
   an entry marker and waits at most 30 seconds. The existing six-second supervisor
   budget causes the real termination; launch count and marker must be observed.
   The two callers retain actual worker exit, partial production-stage and native
   cleanup/failure assertions. No successful resource effect is substituted. The
   separate full-sample integration remains free of this controlled hold.

The frozen source search across src, tools and tests found no tracing mutation in any
current eval-panel measured body. The other production tracer owner is the unrelated
blueprint workload measuring tool, which the eval-panel worker does not invoke. The
accepted entry/exit design does not establish continuous monitoring of arbitrary plugin
code or concurrent on/off toggling; such behavior is absent from the internal callers.

## Deferred coverage comparison

The inventory was exclusively created and hashed before coverage.md or checks/ was read.
Deferred coverage agrees with the independently identified helper, ownership, timing,
initialization, capacity, seven-stage, estimator, role/completion, JSON and native-memory
surfaces. The subsequent cutoff-fixture explanation matches the inspected test code and
retained preliminary failure output. No additional uncovered required category emerged.

## Identity and supplied receipt verification

- Verified ref, sole parent and tree using frozen Git objects. The complete two-file
  diff has 172 insertions and 16 deletions, within the 300 changed-line budget.
  Recomputed blob SHA-256 rows, sorted complete rows ordinally, joined them with LF and
  compared the exact bytes and digest to manifest.sha256. git diff --check passed.
- Verified all 16 pinned dependency blobs, the six supporting input file hashes,
  coverage.md and all 18 individually pinned checks files. All match the handoff.
- RED candidate 370cab05902cd2c79745f68c3be4a609bee31cd4 differs from the parent only
  in tests/test_eval_panel_tool.py. Its test blob is exactly the GREEN candidate's
  d55cb4fdb8bb177774be968731328be86fc72121; its production blob is exactly the parent's
  378ea931f3adb144f1c3f32bee0f38f7e7ceb39c. The receipt records exit 1, 29 unittest
  cases and zero skips. Output shows five timing failures and four missing-metadata
  errors, including actual traced bodies, missing refusal and the falsifying clock
  result (1003, 502) instead of (3, 2). This is a valid behavioral RED.
- Preliminary candidate cedc41f76d63fa50040334cb363c227168c6474e remains failed.
  Its output records the timing tests passing, with two cleanup-trigger expectations
  failing when the real worker reached completion before the cutoff. It is not counted
  as GREEN. The bounded reference-entry hold directly addresses those trigger cases.
- GREEN focused receipt binds to a40e29ca432fa6024a29033efebdaa5b8a31f968, exit 0:
  two pytest suite parameters passed, 44 deselected, 40 unittest cases, zero skips.
  The selection is eval_panel_tool or eval_bridge, not the registered broad harness.
  Its journal source identity, result-summary digest and receipt agree. The three
  supplied stderr files are empty. r002-lint.json records ruff 0.16.5 exit 0 for the
  changed files; I did not rerun lint.
- snapshot.ps1 uses a fresh detached snapshot, locked offline dev sync, the absolute
  CPython 3.14.6 base interpreter and an explicit actual runtime assertion. Execution
  uses -B -P, root/src/tests imports, ResourceWarning and unraisable warnings as errors,
  and a cleared environment with absolute PONTIUS_GIT and no PATH. The receipts record
  those arguments and version. I inspected this supplied procedure and its receipts;
  I did not execute it or independently inspect the external snapshot environments.

## Limits and exposure disclosure

This was read-only frozen-source inspection, byte verification and review of supplied
focused evidence. No project code, tests, uv/pip, hooks, retained measurements, commits,
Git ref mutations or source edits were executed. The allowed absolute utility Python
failed to launch with Access is denied; it ran no utility code. PowerShell/.NET completed
all raw-byte verification without an interpreter workaround or escalation.

Only the assigned output directory was written, with exclusive create semantics. No
sibling scratch root, reviews directory, progress.md, INDEX.md, disposition/readiness
file, prior verdict, other packet or implementer transcript was opened. No automatic
prohibited exposure occurred. Allowed deferred coverage contains a generic mention of
unchanged prior Minor findings; no prior finding details or verdict were sought or read.

I did not reopen the full mathematical/library correctness review, execute a broad
harness, inspect retained resource measurements, or claim measured speed improvement.
Raw integration result files referenced by summaries were not opened outside the allowed
packet. The supplied focused receipts support the inspected integration assertions;
they do not independently establish the later registered broad gate or adoption authority.
