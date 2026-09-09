# Disposition: v0a-eval-panel-code/r001

Finalizer: the round's drafter (Claude). Date: 2026-09-09. Both Codex cold
reviews returned **NOT CLEAN / STRAINED**. Their Important findings overlap
heavily and are accepted in full; every one was verified against the frozen
candidate blobs before acceptance, and every one is in the new orchestration or
admission code — none in the per-hand arithmetic, the lattice rule, the key
construction, or the capacity probe, which both reviews confirm statically.

Outcome: **r001 is not adopted.** Corrections are frozen as
`v0a-eval-panel-code/r002` (FIX round). Design verdict STRAINED is accepted
with its stated cause: I re-implemented a supervisor that already existed in
`tools/v0a_blueprint_workload.py` and dropped its assignment rollback, its
asynchronous initial sender, and its nested cleanup. r002 rebuilds the
supervisor on that pattern rather than patching the copy.

## Findings, de-duplicated across the two reports

| # | Finding (R01 / R02) | Disposition | Correction in r002 |
|---|---|---|---|
| A | R01 I-01 / R02 I-01 — failed `Job.assign` leaves a suspended worker unowned; `finally` is not exception-safe; `main` skips `finish_run` on `KeyboardInterrupt` and on failures before its `try` | **Accepted.** | Supervisor rewritten on the workload pattern: assignment tracked; unassigned process killed; every cleanup step attempted under its own guard; `job.close()` in a nested `finally`; events drained during the loop and again in cleanup so completed observations survive; `main` records one result and one journal row on success, failure, and interruption. |
| B | R01 I-02 / R02 I-02 — nonfinite resource values pass admission (`1e999` → `inf`), defeating limits and breaking the strict writer; booleans and non-exact memory pass; nonfinite reference diagnostics reach the writer | **Accepted.** | Plan JSON parsed with a `parse_constant` refuser; a recursive finiteness check over the whole plan; `seconds` must be a finite positive `int`/`float` that is not `bool`; `memory_mib` an exact `int` in a declared range; plan size bounded; every retained report passes through a JSON-safe pass that encodes nonfinite floats as tagged strings. |
| C | R01 I-03 — the initial request write blocks before the watchdog | **Accepted.** | Request sent on a daemon sender thread, as the workload supervisor does; plan raw size bounded at admission. |
| D | R01 I-04 / R02 I-04 — the plan omits the adopted mandatory identities (prefix, hand universe, ordered permutation, runtime); a substituted test sample can pass as a full preflight and feed the estimate | **Accepted.** | Plan schema v2 with closed per-phase key sets: `runtime.python`, `prefix` (checked equal to the replayed prefix), `hand_universe_sha256` and `hand_count`, `pool_seed` **and** the full ordered `permutation` (checked for exact membership and order against the seed rule), `coverage` = `declared-full` or `test-subset` for preflight; a `test-subset` result is labeled and produces no full-pool estimate; `declared-full` requires at least four development hands and one control. Seed/index bank fields are stated as inapplicable to these two phases in the tool's contract text, not silently dropped. |
| E | R01 I-05 / R02 I-03 — `s = 3` accepted as the fixed domain (`raise_to(1)`) | **Accepted.** | `require_declared_root` asserts the exact declared root — river, acting seat 2, live seats (1, 2), pot 4, live stacks 2, legal `(CHECK, RAISE)` with bounds exactly `[2, 2]` — and `bet_action` returns the constant `raise_to(2)` only after that check; `hand_totals`, `build_reference` and the tool's plan admission (`stacks == 4`) all enforce it. `replay_root(stacks=…)` remains only for the labeled negative key control. Tests refuse `s = 3` and `s = 6`. |
| F | R01 I-06 — boundary wire artifacts not retained | **Accepted.** | `capacity_probe` returns the boundary encodings; the worker ships them base64; the parent writes them into the single run directory and binds path, length and digest in the result. |
| G | R02 I-05 — a budget kill during reference work discards the completed production measurement | **Accepted.** | The worker emits one `stage` event per completed measured stage; the parent assembles hand observations from stages, so a kill retains what completed and labels the rest unavailable; the phase stays failed. |
| H | R01 I-07 — focused coverage never runs the real reference on a nonzero hand or the real supervisor | **Accepted.** | New tests: the sealed singleton reference on `As Ad` (nonzero totals) through `validate_reference`; the real supervisor on a real capacity worker; an assignment-refusal schedule through the real launcher observing process death and the retained containment cause; a real budget kill after production and during reference retaining the partial hand; `main` through the real `finish_run` in a disposable git repository for both a completed run and a nonfinite-plan refusal, each yielding exactly one journal row; signed cancellation and smallest-gap cases through `validate_reference`, not only the scalar helper. |

Advisory items adopted: cache state recorded after every stage; the two forced
evaluations costed separately; work counts (villain hands, settlements,
ranker calls) recorded where the caller performs them and marked
`not_instrumented` for the sealed evaluator's internals; one explicit warm
repetition of production per hand; the estimate states its cache assumption.
R01's note that BASE `README.md`/`pyproject.toml` still read `>=3.11` is about
the base, not the candidate; the controller has since updated the working tree.

## Not accepted

Nothing. The reviews' claim that the arithmetic, keys and probe are statically
sound is also accepted as scoping, not as evidence.

## Budget

Both reviews confirm 575 production / 264 test lines and defer the slice budget
to the controller. The controller raised it on 2026-09-09
(`inputs/controller-rulings-addendum.md`); the exact figure remains the
drafter's reading of 800/500 until confirmed. r002 will exceed the original
600 on its own and reports its counts in its receipts.

## What r002 is not

No retained measurement, no full-pool solve, no export or agreement code, no
sealed change, no ceremonial commit. It returns for a second Tier C cold review.
