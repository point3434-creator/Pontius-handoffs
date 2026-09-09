# Timing r002: finalizer disposition

Candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968.
Parent: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
Manifest: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2.
Ref: refs/heads/review/v0a-eval-panel-timing/r002.

Decision: CLEAN / SOUND for the timing correction. I-01 is resolved in this new
candidate. Both independent cold source reviews and the post-review broad gate
support the corrected measurement/provenance contract. Source adoption and public
publication remain separate controller decisions.

## What changed

measure() times one invocation without allocation tracing. Entry/exit checks
refuse active tracing rather than silently stopping a tracer owned by the caller.
End clocks precede the postcheck and result construction. Every produced cost
states untraced-body-v1; traced_peak_bytes is null with not_collected status.
The native worker Job memory peak remains unchanged and separately observable.

full_pool_estimate requires matching timing and unavailable-memory metadata on
every development production cost, emits the timing mode, and names the absence
of allocation tracing in its assumptions. Legacy or incompatible metadata cannot
silently receive an untraced production forecast. Existing role, completeness,
comparison, arithmetic and cache-order behavior remains.

The source delta is 19 additions and 12 deletions. Tests add five timing cases,
extend stage/result and negative-estimator checks, and control two old deadline
triggers at actual reference entry. Total delta: 188 lines across two files,
within the declared 300-line budget.

## Evidence

- Final RED: 29 cases, zero skips, exit 1. Five timing behavior failures and four
  missing timing-mode errors occur on unchanged parent production. The controlled
  native deadline fixtures pass. RED and final test blobs are byte-identical.
- Focused GREEN: 40 cases, zero skips, exit 0. Both eval-panel registered suites
  pass. Real five-hand worker/result tests verify the serialized timing contract,
  estimate arithmetic and native Job memory. Ruff passes for both changed files.
- Cold reviews 01 and 02: CLEAN / SOUND. Their own inventories were recorded
  before deferred inputs, in distinct assigned scratch roots. Original reports
  and disclosures remain in reviews/; this disposition does not rewrite them.
- Post-review broad: 593 cases accounted for; 583 passed and 10 skipped;
  exit 0, source_verified true. Skips are the explicitly optional SciPy cases.
  Stderr is empty and there is no warning summary. Full per-suite counts are in
  checks/broad-result-summary.json and the original referenced result.
- All execution uses CPython 3.14.6, fresh locked dev snapshots, -B -P, root/src/
  tests import paths, absolute PONTIUS_GIT with PATH absent, and resource and
  pytest unraisable warnings as errors. No main-checkout environment was synced.
- Independent raw-blob verification matched the source manifest and all 16 pins.

Actual broad result:
D:/Pontius-worktrees/eval-timing-check-r002-broad/
experiments/results/20260909T182400-cc21db36.json
SHA-256: a243d39b48729d4adf76064b2e16920db782f22417072d24371855d85e8e0a41.

The r001 candidate/failed receipt remain withdrawn-before-review records. Its
two cutoff fixtures failed because the workload completed before the assumed
deadline. The r002 test-only schedule holds the real worker at reference entry;
the real Job budget must terminate it. It changes the trigger, not native
cleanup, recorded production results, or their existing assertions.

## Limits and next gate

Timing mode describes allocation tracing, not the absence of every possible
external profiler. Entry/exit checks are not a continuous monitor of arbitrary
concurrent tracer toggles; the known internal call graph contains no such code.
Controlled-failure fixtures are correctness evidence, not representative timing
samples. No performance ratio or corrected full-pool duration is inferred from
these tests or the old synthetic allocation diagnostic. Historical figures and
their instrumentation addenda retain their original meaning and bytes.

The earlier d8d291cc and 9fce4bf candidates still contain I-01. Their immutable
readiness rulings remain. This new candidate includes both the workload/Git
correction and this timing fix; it does not retroactively repair old source.
No source adoption, public push or retained capacity/preflight invocation occurred.

The next accepted checkpoint remains the separately authorized retained capacity
and preflight, followed by the controller's measured resource decision before
steps 4-7. Any proposed invocation must bind this new full candidate identity;
previous plans naming d8d291cc or 9fce4bf are not authority to run it implicitly.
