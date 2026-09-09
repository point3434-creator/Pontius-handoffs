# Coverage claim: v0a-eval-panel-code/r004 (FIX round)

Deferred input. Reviewers: do not open this until your initial invariant and
related-path inventory are recorded, per the cold-review request.

## What changed since r003, and how this file differs

r003's coverage table restated intended properties as if the source implemented
them ("every cleanup step guarded" was false). This file therefore cites, for
each corrected property, the frozen line that implements it and the executed
case that falsifies its absence. Line numbers are in `tools/v0a_eval_panel.py`
at `0bc19bca` unless stated. Only the tool and its test module changed;
`eval_bridge.py`, its tests, the fixtures and `cases.json` are byte-identical to
r003 (same blob digests in `manifest.sha256`).

## Corrected paths (r003 findings)

| r003 finding | Property | Implementing lines | Executed case (`tests/test_eval_panel_tool.py`) |
|---|---|---|---|
| I-01 (R01/R02) — one `try` around all cleanup | Every release is its own bounded attempt: `attempt` (359–368) records success, `Exception`, or `KeyboardInterrupt` per step and continues; order is terminate job (379), kill process, wait, join ×3, close stdin/stdout/stderr, drain, verify (370–377), close job (388, outside the `process is not None` branch so it always runs). `supervise` fills a caller-owned `report` (266, 278–281); `main` passes its own (477) so an unwound `supervise` cannot discard drained observations. | `test_cleanup_faults_do_not_skip_later_releases_or_retained_stages` (221): real launcher, `Job.active` raises `HostRefusal` and `Thread.join` raises `OSError`; asserts `terminate job` and `verify` failed, all three joins failed, kill/wait/three closes/drain/close job `ok`, `cleanup_verified` false, exit code observed, `cleanup verify: HostRefusal` in `errors`, production stage retained. `test_interrupt_during_cleanup_keeps_the_partial_report` (248): `Popen.wait` raises `KeyboardInterrupt`; `supervise` returns (does not raise) with status `interrupted`, `wait` = `interrupted`, later steps `ok`, production stage retained. `test_interrupted_supervisor_still_records_its_drained_observations` (344): `main` through the real `finish_run` with a supervisor that fills the report then raises `KeyboardInterrupt`; one journal row, status `interrupted`, the drained observation in the result. `test_capacity_runs_to_completion_under_containment` (212) now asserts every cleanup step `ok`. |
| I-02 (R01/R02) — count-only `declared-full` | `sample_identity` (140–147): a hand is two card strings, parsed by `parse_cards` (distinct), sorted to the canonical tuple, and must be a member of `hero_hands(board)` (no board overlap). Duplicates across hands and controls refused for any coverage (132). `declared-full` requires the sample to equal `declared_sample` exactly (134; 150–153): board `2c 7d 9h Js Qc`, the four declared hands, the royal `2c 3d` control. `run_plan` builds units through the same `sample_identity`, so record names are canonical. The parent refuses a stage or completion event for an already-complete record (314). `full_pool_estimate` (427–441) estimates only when all four required hands have `complete` records on the declared board; otherwise `not_estimated` naming the missing hands. | `test_validate_refuses_every_wrong_or_missing_member` (75): refused — four copies of `As Ad`, four substituted distinct hands, no control, a non-royal control on the development board, the royal control's hand replaced, malformed card `Zz`, board-overlap `2c Ad`, `As As`, a string hand, and a `test-subset` with a repeated hand; accepted — the fixture, the fixture with `Ad As` reordered, a one-hand `test-subset`. `test_full_pool_estimate_needs_every_declared_hand_complete` (166): four complete records → `estimate` with `sample=4`; one incomplete → `not_estimated` naming it; `test-subset` → `not_estimated`; no coverage → `None`. The repeated-observation guard (314) is defense in depth behind admission and has no executed case (a validated plan cannot schedule a repeat). |
| I-03 (R02) — `pop` before the first write | `retain_boundaries` (400–424): encodings stay on the observation; each artifact is written to `<name>.partial` and renamed into place (414); the binding is recorded and the encoding removed only after the rename (415–417); `boundary_artifacts` is created with `setdefault` so a retry keeps earlier bindings; the `finally` labels retention `incomplete` with the unwritten encodings still in `boundary_base64`, or `complete` (418–424). | `test_retention_failure_keeps_bound_artifacts_and_unwritten_encodings` (137): two encodings, `Path.write_bytes` fails on the second; the first is bound with the byte-exact digest, the second remains as base64, retention `incomplete`, only the first artifact exists on disk (no `.partial`), and a retry completes both. `test_capacity_phase_emits_boundary_bytes` (118) now retains the real capacity observation and reads every artifact back byte-equal to its encoding. |

## Unchanged paths (r003 table, still asserted)

Plan bytes (`parse_plan`), plan schema outside the sample (closed keys, runtime,
stacks, prefix, universe digest and count, seed, full permutation, resource),
declared root, capacity probe, production, reference, lattice rule, request
transport, stage events, nonfinite output, run record: the r003 coverage table
applies unchanged and its cases are re-executed in the receipt (27 cases).

## Exercised cases (executed, receipts in `checks/`)

Bridge suite 11 (unchanged). Tool suite 16: the 11 of r003 (two extended as
noted) plus the five new cases named above. Focused receipt: **27 unittest
cases, 0 skipped, pytest exit 0**, in a disposable detached snapshot of the
candidate with its own `uv sync --group dev` venv, `env -i`, `-B -P -W
error::ResourceWarning`. Scrubbed-environment suites were run before the freeze
this time (r002 lesson).

## Limits

No retained measurement; no export or agreement code. The pipe-fill stall is
corrected by construction and not reproduced by a test. Not covered: a
real-worker `main` invocation end to end, a run-directory write failure, a
cleanup failure at a stream close (the injected faults are the job query, the
joins and `wait`). Budget: see `checks/line-budget-and-hygiene.md`.
