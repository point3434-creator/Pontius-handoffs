# Verification correction r001: disposition and broad gate

Decision: CLEAN / SOUND for the bounded correction. Both independent cold
reviews found no required correction. The post-review broad gate now passes.
This is technical readiness; ceremonial adoption and public push are pending.

Candidate: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
Base: d8d291cc1f813ce798f2d3a990b2a8bf2297e124.
Manifest: d05fd7b821fec534044eeb80acdf23a4fe09767373a67e4cde20bc5ba1bed088.
Ref: refs/heads/review/v0a-eval-panel-verification/r001.

## Change and reason

The three Git fixture calls use an absolute resolved executable, including the
PONTIUS_GIT supplied by scrubbed verification. Existing assertions remain.
The older workload controller joins its registered pipe users before closing
stdin, stdout and stderr. It retains each close failure, continues other close
attempts, and requires observed closure for its cleanup certificate.

Existing real native-worker cases now inspect the actual process and streams
before test cleanup. One added case closes the real stdout and then injects an
error; the production report must retain that error and withhold certification.
The delta is 123 additions and 27 deletions across three authorized files;
production accounts for 17 additions and 3 deletions. Reflow keeps changed
source files within 100 columns. No eval-panel source or arithmetic changed.

## Verification

- Final RED: 31 cases, zero skips, exit 1; seven native cases detect open pipes.
  Production matches the parent; test bytes match the final candidate.
- Focused GREEN: 66 cases, zero skips, exit 0; both affected suites and both
  eval-panel suites pass. Ruff passes for all three changed files.
- Cold review 01: CLEAN / SOUND. Cold review 02: CLEAN / SOUND.
  Original reports and initial inventories are retained unchanged in reviews/.
- Post-review broad: 588 unittest cases, 10 explicit skips, exit 0;
  46 registered suites processed. No warning summary and empty stderr.
  Duration: 356.75 seconds.
- All execution used fresh locked dev snapshots, CPython 3.14.6, -B -P,
  PATH absent, absolute PONTIUS_GIT, explicit root/src/tests import paths,
  ResourceWarning-as-error and pytest unraisable-exception warnings as errors.
  Source verification is true for the actual final result and its journal.
- Independent blob verification matched the manifest and all 17 dependency pins.

Explicit optional skips:

- test_sparse_open_mode_factor_tt: 2 skipped.
- test_leaf_adjoint_cfr: 5 skipped.
- test_leaf_adjoint_evaluation: 3 skipped.

All ten skipped cases explicitly declare the optional SciPy screen. They are
not counted as executed passing cases: 578 passed, 10 skipped.

Broad result remains in its original snapshot:
D:/Pontius-worktrees/eval-verification-check-r001-broad/
experiments/results/20260909T154804-79784074.json
Result SHA-256: e3a898e86eb9339b6495282e202a6b00cc2ddceee20b90f0b98a9948cbc5de45.
checks/broad-result-summary.json and the receipt/journal bind its exact identity.
The earlier failed broad run and import-diagnostic records remain unchanged in
the completion preparation packet; their failures are not relabeled as passes.

## Scope limits and next decision

The tests establish the exercised native cleanup paths. They do not establish
recovery after arbitrary OS termination/join failure, an indefinitely stalled
reader, or every asynchronous interruption. Both reviews accept those explicit
limits for this bounded correction; no live-resource success is simulated.
Optional dependency skips are not GPU/SciPy coverage. No performance, capacity,
full-pool solve, teacher export or host agreement claim follows from this gate.

The correction worktree remains parented on d8d291cc, and this candidate exists
only as an immutable local review ref. Master and the earlier repair worktree
are untouched; existing STATUS.md and execution_journal.jsonl edits are preserved.
No ceremonial commit or public push was performed by this correction task.

The accepted design's next gate is a retained capacity/preflight decision before
steps 4-7. next-gate-request.md prepares exact source, plan hashes, budgets and
conditional execution. It is a proposal, not an invocation or authorization.
Claude's previously assigned commit turn remains available to the controller.
