# r002 coordinator review: host accounting and trace storage

Reviewer: Codex coordinator (/root), 2026-08-30. This is an additional
coordinator pass, not one of the two independent cold reviews.

Candidate: `18c965d1f3445c253a6333c4d10899c1dcac0cc6`
Ref: `refs/heads/review/v0a-i01-impl/r002`
Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Manifest SHA-256: `4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18`
Tree: `35f00349a7538cffc02f8e81f71913251be200be`

Verdict: **NOT CLEAN**. Three Important findings below are directly reproduced
on actual CPython 3.11.15 and 3.14.6. No implementation or test bytes changed.
All source locations refer to this frozen commit, not mutable worktree files.

## C-01: Decision serialization disappears from complete accounting

Severity: Important. Confidence: high, directly reproduced.
Location: `src/pontius/v0a/replay.py:404-408`, `:424-428`, `:505-516`;
`src/pontius/v0a/runtime.py:228-252`.

ADR-0485's authoritative clock/emission contract requires post-delivery trace
serialization and writing to be measured as uncredited preparation or
post-terminal bookkeeping, outside the next action wall. Terminal totals must
cover every preceding trace-row write through the pre-publication cut.

The host calls `builder.add_event`, `add_decision`, and `add_failure` outside
`runtime.bookkeeping()`. The existing bookkeeping interval covers settlement
and its oracle only. Consequently the next response starts later, but no
preparation interval reports the work that delayed it.

Diagnostic: run real fixture A with the real runtime, immutable empty policy,
mailbox, TraceBuilder, and deterministic monotonic witness. Wrap the real
`TraceBuilder.add_decision` to advance that same clock by two seconds before
calling the unchanged serializer. Four decisions add exactly 8,000,000,000 ns.
Baseline and delayed runs both report:

- preparation_compute_seconds: `0.000061`;
- post_terminal_compute_seconds: `0.000002`;
- receipt passed: `true`; accounting_complete: `true`.

The delayed clock ends exactly eight seconds later. The work is neither in
response durations nor either complete non-response total. This is not a
latency benchmark; deterministic injected time proves omitted accounting.

Correction direction: enclose each actual post-delivery serialization/write
interval in the public bookkeeping API, classify it once by terminal state at
entry, and include all such intervals before the terminal cut. Preserve fresh
next-action walls. Also measure pre-cut semantic computation and other host
verification work rather than assuming those costs are zero. A clock failure
while closing such work must prevent further input and successful accounting.

## C-02: No decision trace is written before the next event is dispatched

Severity: Important. Confidence: high, directly reproduced and source traced.
Location: `src/pontius/v0a/replay.py:389-429`, `:520-554`;
`src/pontius/v0a/trace.py:298-323`.

ADR-0485 expressly requires serializing and writing a decision after delivery
and clock closure, before dispatching the next event. A write failure after a
delivered action must stop further input while retaining that action and its
in-memory record. This is distinct from final terminal publication.

Diagnostic: run real fixture A with an explicit existing run directory and a
new destination. Immediately after each real `add_decision` returns, inspect
the actual destination. It is absent after action indices 1, 2, 3, and 4. It
exists only after `ReplayHost.run()` completes. The receipt reports success.

Source confirms that `TraceBuilder` accumulates bytes in a list, and the only
`write_trace` call occurs inside final terminal publication. Thus a storage
failure cannot be detected between actions; the host has already processed
all later events and emitted all four actions before attempting any trace
write. The existing occupied-destination test likewise checks four retained
decisions after the eventual failure and does not exercise the required first
post-delivery write boundary.

Correction direction: open the create-new destination under the run root and
publish the appropriate row prefix at each event/decision boundary; do not
accept the next input until required writes succeed. Keep the final terminal
row and its publication receipt separate, retain incomplete files as
unaccepted on failure, and preserve the first primary failure and delivery
facts. Do not emulate this by repeatedly invoking a whole-file create-new
writer or by moving write cost inside the next action's response wall.

## C-03: Parent replacement can redirect a create-new write outside its run root

Severity: Important. Confidence: high, real Windows filesystem reproduction.
Location: `src/pontius/v0a/trace.py:377-396`.

ADR-0485 requires create-new trace destinations under an explicit run root,
with unsafe links and path escape refused without overwrite. `write_trace`
resolves the path and checks its parent, then performs an unbound path-based
`os.open`. There is no binding between the checked parent and the parent used
by the open.

Diagnostic, entirely under a unique disposable D:-local fixture directory:

1. Create `race-root/slot` as a real directory and a sibling `outside` directory.
2. Call real `write_trace` for `race-root/slot/escaped.jsonl` under `race-root`.
3. At its `os.open` boundary, after the writer's path checks, rename `slot` to
   `parked` and create a real Windows junction named `slot` pointing to
   `outside`. Then invoke the original `os.open` unchanged.
4. The writer returns digest
   `6afee7a409bf24d19d788248bbe15f83cbc96211d240f378bf4e79e58afbc727`
   without exception, and `outside/escaped.jsonl` contains `review-only\n`.

Both interpreters reproduce this. The diagnostic hook only schedules an actual
filesystem replacement; it does not fake the open, file contents, or path
resolution. No path outside the disposable fixture area is touched, and no
pre-existing file is overwritten. `O_EXCL` protects the leaf from replacement
of an existing file; it does not bind ancestor directories.

Correction direction: make directory validation and file creation refer to
the same stable directory authority, refusing replacement/reparse paths before
writing. Use an appropriate directory-handle/identity-bound primitive or an
equivalent explicitly verified protocol. Keep this narrowly scoped to the
trace writer; this does not call for a general governance transaction engine.

## Evidence and limits

`checks/codex_verify_r002.py` independently checked the ref, parent, tree,
changed-path set, every frozen blob, the whole-row-sorted LF manifest, and the
manifest file's own SHA-256. It created independent no-hardlink detached clones
with LF checkout bytes and no alternates. Both unchanged-from-r001 paths also
have an empty Git diff. The primary checkout still has only its pre-existing
untracked `.tmp.driveupload/` directory.

Each interpreter identity was recorded and asserted before payload imports;
all runs used `-B -P`, snapshot cwd, exact snapshot `PYTHONPATH`, a scrubbed
environment, and absolute `PONTIUS_GIT`. Required NumPy imported through the
existing package baseline; CuPy and Torch did not. All four focused suites
pass on each interpreter: hand_replay 36, trace 25, replay 20, contract_faults
18, total 99. Those successes do not exercise the failures above.

Diagnostics and invocation evidence:

- `checks/codex_host_storage_probes.py`;
- `checks/codex_run_host_storage.py`;
- `checks/codex-py311-host-storage.txt`;
- `checks/codex-py314-host-storage.txt`;
- `checks/codex-py311-verification.json`;
- `checks/codex-py314-verification.json`.

Both diagnostic processes exited zero because their observations completed;
that is not a correctness pass. Source snapshots remained clean. Junctions
and diagnostic files are retained only in unique disposable fixture areas.

This pass does not establish source-seal closure, measured limits, broad-suite
acceptance, lifecycle authority, CI admission, or any poker/latency result.
Slice C remains outside this packet's scope. The independent cold reviewers
supply their own whole-candidate findings; this report does not speak for them.
Claude remains the checkpoint finalizer. No fixes, evidence-repository commits,
or review-ref retirement were performed.
