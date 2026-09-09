# Disposition: v0a-eval-panel-code/r003

Finalizer: the round's drafter (Claude). Date: 2026-09-09. Both Codex cold
reviews returned **NOT CLEAN / STRAINED** (R01: two Important; R02: three
Important; no Critical). Every finding was verified against the frozen blobs
at `7004285d` (manifest `12e9cedd…`) before acceptance. All are accepted. All
three sit in the tool's orchestration (`tools/v0a_eval_panel.py`); neither
review found a defect in `eval_bridge.py` — the replay, per-hand settlement,
singleton reference and lattice rule are confirmed statically by both.

Outcome: **r003 is not adopted.** Corrections go to `v0a-eval-panel-code/r004`
(FIX round). Per the brief (BASE lines 166–169) any later candidate review needs
explicit controller reauthorization; the freeze is the drafter's, the review
assignment is the controller's.

## Findings, de-duplicated across the two reports

| # | Finding (R01 / R02) | Verified at | Disposition | Correction in r004 |
|---|---|---|---|---|
| I-01 | R01 I-01 / R02 I-01 — every cleanup action shares one `try`; `Job.active()` (BASE `v0a_table_host.py:430–438`) raises `HostRefusal('cleanup_failed')` on a failed query, so a failure there skips `wait`, thread joins, all three pipe closes and the final `drain`; a `KeyboardInterrupt` during cleanup escapes `supervise` and `main` records its original empty report | `tools/v0a_eval_panel.py:335–363`; `main` 434–446 | **Accepted.** Residual of r001 A (first residual on that contract). The coverage claim "every cleanup step guarded" was false; the docstring said it and the source did not do it. | Cleanup rewritten as independent bounded attempts (terminate, kill, wait, join, each pipe close, drain, verify, job close), each recording its own failure and never preventing the next; `KeyboardInterrupt` inside an attempt is recorded and cleanup continues; `supervise` fills a report dict owned by `main`, so an escape cannot discard drained observations; the per-step outcomes are retained in the report. |
| I-02 | R01 I-02 / R02 I-02 — `declared-full` is a length check; four copies of `As Ad` (or four substituted hands, or a non-royal control) pass admission, collapse to one record under `(label, board, hand)`, and yield `status=completed` with a full-pool estimate from `sample=1` | `tools/v0a_eval_panel.py:120–134`, `288–298`, `390–406` | **Accepted.** Residual of r001 D (first residual on that contract). | Admission parses every hand and control with `parse_cards`, requires each hand to be in the compatible universe of its board (distinct cards, no board overlap), refuses duplicate identities in any coverage, and binds `declared-full` to the exact declared sample: board `2c 7d 9h Js Qc`, the four named hands as a set, and the royal-spade `2c 3d` control. The parent refuses a stage event for an already-complete record. `full_pool_estimate` issues an estimate only when all four required hands have complete records. |
| I-03 | R02 I-03 — `retain_boundaries` pops `boundary_base64` before the first write; a failure at the second write leaves the first artifact unbound and the second encoding unrecoverable | `tools/v0a_eval_panel.py:375–387` | **Accepted.** New finding (not a residual). | Encodings stay on the observation until each is committed; each artifact is written to a staging path and renamed into place; the binding is recorded after each successful rename and the encoding removed only then; on failure the completed bindings and the unwritten encodings both remain in the single result with an explicit retention status. |

## Root-cause note (workflow "count residuals")

I-01 and I-02 are each the first residual on their contract, so in-place
fixing is permitted; a second residual on either would require a separate
candidate. Why r003 missed them: the r001 corrections were written against the
*pattern* (the workload supervisor's shape; the plan's key set) rather than
against the *property* each finding stated (every release attempted; the
declared sample is a set of identities). The coverage table then restated the
intended property as if the source implemented it. r004's coverage will cite
the line implementing each claimed property, and each property has a test that
injects the failure the reviewers described.

## Not accepted

Nothing. R01's related observation that control/hand strings were parsed in
the worker rather than at admission is folded into I-02. Both reviews' residual
coverage gaps that are not product findings (an actual pipe-fill schedule, a
real-worker `main` invocation, directory-write failure) are recorded here and
not claimed closed by r004 unless its coverage lists a case.

## Design verdict

STRAINED is accepted with its stated cause. The correction is bounded to the
tool's admission, cleanup and retention boundaries and its tests; no sealed
module, no new framework, no whole-slice rewrite.

## Budget

Reviewers reproduced 792 / 428. The controller's ruling (addendum-2) sets a
hard ceiling of 3,000 production lines for the slice; the working figure
1,200 / 600 remains the drafter's reading. r004 reports its totals against it.
