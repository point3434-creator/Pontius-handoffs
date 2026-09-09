# Disposition: v0a-eval-panel-code/r004

Finalizer: the round's drafter (Claude). Date: 2026-09-09. Both Codex cold
reviews returned **NOT CLEAN / STRAINED** (R01: three Important; R02: four
Important; no Critical). Every finding was verified against the frozen blobs
at `0bc19bca` (manifest `70ca4c76…`) before acceptance. All are accepted.
Neither review found a defect in `eval_bridge.py`; the replay, per-hand
settlement, singleton reference and lattice rule are confirmed statically for
the third consecutive round and have not changed since r003.

Outcome: **r004 is not adopted, and in-place fixing stops.** Both reviewers
independently invoke the workflow's second-residual rule (`workflow.md`, "count
residuals, not rounds") on two contracts. The finalizer concurs. The controller
has decided that Codex drafts the next candidate(s); per checkpoint alternation
Claude then reviews. This document supplies the root-cause note the rule
requires before any further fix on those contracts.

The coordinator's provenance note (`reviews/coordinator-provenance.md`)
discloses that both reviewers ran standalone utility hashing on Python 3.11 /
3.12 rather than 3.14. No project code was imported or executed under those
interpreters; identity and digests were re-verified with .NET. Accepted as a
disclosed process deviation with no effect on the findings.

## Findings, de-duplicated across the two reports

| # | Finding (R01 / R02) | Verified at (`tools/v0a_eval_panel.py` @ `0bc19bca`) | Disposition | Residual status |
|---|---|---|---|---|
| A | R01 I-01 (A) / R02 I-01 — `verify` sets `cleanup_verified=True` at 372–375, then `close job` runs at 388; a failed `Job.close` (`HostRefusal`) is recorded but the certificate stays true. `verify` never consults recorded cleanup outcomes, so a failed join or interrupted `wait` followed by an independently dead process also yields a true certificate. | 359–388 | **Accepted.** The certificate must be the last thing computed and must be a conjunction of observed resource state and *all* release outcomes including the final job release. | **Second residual** on the cleanup contract (r001 A → r003 I-01 → here). Separate candidate + root-cause note required. |
| B | R01 I-01 (B) / R02 I-02 — drained preflight records accumulate in the local `hands` dict (309–321) and reach `observations` only at 389–391, after the `finally`. A `KeyboardInterrupt` there, or between cleanup attempts (outside any `attempt`), unwinds `supervise` and `main` records its report without those records. The r004 ownership test pre-loaded the report through a fake supervisor and so proved the writer, not the producer-to-report seam. | 277–281, 309–321, 389–391 | **Accepted.** Each record must be attached to caller-owned storage when first created and mutated in place thereafter; `missing_stages` annotation must be separate from ownership. | Same contract as A (observation preservation under interruption). Second residual. |
| C | R01 I-02 / R02 I-03 — `declared-full` compares the *unlabeled union* of `(board, hand)` identities against `declared_sample` (129–134). Moving any development hand into `controls` — or all of them, leaving `development_hands=[]` — passes admission; `run_plan` labels by input list (236–239); `full_pool_estimate` requires `label == "development"` (436–441) and reports the hand missing; `main` still records `status=completed, coverage=declared-full`. With all five identities as controls the plan board is unconstrained by any development sample. | 124–136, 236–239, 436–441 | **Accepted.** Admission must bind the development board, the four development identities and the royal control *per role*, and one role-bearing admitted schedule must be what the worker executes and the estimator reads. A `declared-full` run whose role-specific sample is unmet must not complete. | **Second residual** on the sample contract (r001 D → r003 I-02 → here). Separate candidate + root-cause note required. |
| D | R01 I-03 / R02 I-04 — `retain_boundaries`: `os.replace` publishes the final-name artifact (414); an interrupt before `retained[count] = …` (415–417) leaves a complete file unbound and the `finally` labels its encoding "unwritten". Bytes remain recoverable in `boundary_base64`; the defect is artifact-to-result identity and a false label, not loss. | 406–424 | **Accepted.** Register the publication (intended path, state) before the fallible rename and reconcile after; distinguish pending publication from completed binding. | First residual on the retention contract (r003 I-03 → here). In-place fix permitted; both reviewers say so. |

Also accepted from R01's inventory, not as a finding: `stream.close()` has no
timeout and a join timeout does not bound a later close against a live I/O
thread, so "every attempt is bounded" is unverified under compound failure.
Carry this into the cleanup candidate's invariants.

## Not accepted

Nothing.

## Root-cause note (required by the second-residual rule)

Two contracts, two fixes each, all four missed. The misses share one cause, so
one note covers both.

**Cleanup / observation preservation (r001 A → r003 I-01 → r004 A, B).**
r001 copied the workload supervisor's shape and inherited its single `try`.
r003 guarded each step and passed `report` by reference. Both fixes were
*sequences of actions* designed against the schedules I had imagined, and
each test replayed one of those schedules. The contract is not a sequence; it
is two invariants that must hold at every instant of the cleanup, whatever
order events arrive in:

1. `cleanup_verified` is true **iff** every release succeeded *and* the
   resources are observed released — so it can only be decided after the last
   release, and any recorded failure or interrupt makes it false monotonically.
2. Every observation that has been drained is reachable from the caller's
   report **at the moment it is drained** — so `hands` cannot be a local, and
   `main` must see records the instant `supervise` creates them.

r003 violated (1) by having no per-step outcomes at all; r004 violated (1) by
computing the certificate before the last release, and (2) by owning the dict
but not its contents. A test of the *invariant* — inject a fault at every step
in turn and assert (1) and (2) after each — would have caught both rounds. I
tested the paths I designed instead.

**Sample identity (r001 D → r003 I-02 → r004 C).** r001 checked a count.
r003 checked a set of identities. Each fix validated a *projection* of the
schedule (its size; its membership) and left the worker and the estimator to
reconstruct the schedule's meaning from the raw plan lists again, with roles.
The contract is that there is **one admitted schedule** — role-bearing,
canonical, exactly the declared sample under `declared-full` — and that this
single object is what the worker executes and the estimator consumes. Three
consumers each rebuilding it from the plan is three chances to disagree, and
they did. A test that runs a valid `declared-full` plan through the real
worker and checks that the estimator finds exactly the four development
records it expects — the end-to-end case the packet declared uncovered — would
have exposed both r003 and r004.

**Why the pattern repeated.** Both contracts are *state* contracts and I kept
treating them as *control-flow* contracts. The reviewers' STRAINED verdicts
say the same thing in design terms: the protected state is reconstructed in
several places (admission, worker labels, local accumulation, certificate,
publish-then-bind) rather than owned in one. The fix is a shape change within
the tool, not another guard: a role-bearing admitted schedule; records
attached to the run on first receipt; a certificate finalized from monotonic
outcomes after the last release; a publication record that spans
staging → rename → binding. R02's advisory shape is the right one and this
note endorses it rather than proposing an alternative.

## Guidance for the next candidate(s)

- One candidate per contract is what the rule says. A single candidate is
  acceptable only if its disposition explains why the two contracts were
  taken together; R02 asks for that explanation explicitly.
- Finding D (retention) may ride with the cleanup/ownership candidate as an
  in-place fix.
- The scrubbed-environment receipt procedure in `checks/` is sound; keep it,
  and run it before freezing.
- Coverage should state each invariant and the fault schedule that falsifies
  it, not the functions touched. r004's coverage cited implementing lines and
  still missed four members because it described paths, not state.
- The bridge is not to be touched; it has three CLEAN static confirmations.

## Design verdict and budget

STRAINED accepted with its stated cause (above). Reviewers reproduced 834 /
556 and the 1,050–1,150 whole-slice projection against the pinned 3,000
ceiling and 1,200 / 600 working figure; no budget action. A shape change to
the tool's orchestration may move the tool's count in either direction; the
next freeze reports it.

## Calibration

The drafter predicted 65% CLEAN for r004 after predicting 60% NOT CLEAN for
the r003 spec (which was CLEAN) — wrong in opposite directions, both times on
orchestration. Recorded so the next prediction is discounted accordingly.
