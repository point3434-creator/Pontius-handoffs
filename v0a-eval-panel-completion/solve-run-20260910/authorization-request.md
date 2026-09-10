# Authorization request: retained full-pool solve invocation

Drafter: Claude, 2026-09-10. Status: **not executed; awaiting one cold Codex review under
controller-review-policy-20260909 and then the controller's explicit one-shot
authorization.** This is the first of the three retained phases that design step 7
requires after the adoption of completion/r003 (adoption granted no invocation).

## What is bound

- **Source** — `1c7067448106cfa2aca3d57be879842d72293c61`, the adopted head of
  `codex/eval-panel-completion-adopted`; tree `3d2fe79d` identical to the reviewed
  completion/r003 candidate `7ca82180` (CLEAN/SOUND, broad GREEN, controller: "I approve all.")
- **Execution checkout** — `D:/Pontius-worktrees/eval-panel-solve-20260910`, branch
  `claude/eval-panel-solve`, HEAD = source; source scope clean; permanent, mirrored
- **Interpreter** — `<checkout>/.venv/Scripts/python.exe`, CPython 3.14.6, `uv sync --locked
  --offline --group dev`
- **Plan** — `<checkout>/plans/solve.json` (copy: `plans/solve.json`), SHA-256 `c1a6af60…`,
  12,365 bytes; `pontius-eval-panel-completion-plan-v1`, phase `solve`, `declared-full`,
  pool 1,081 on 2c 7d 9h Js Qc, the retained capacity run's pool seed and permutation
  (digest `344e7eeb…`), envelope 600 s / 2048 MiB exactly as the resource decision records
- **Prerequisites bound inside the plan** — the retained capacity result (`29f532a9…`), the
  retained preflight result (`8a17325e…`) and the controller's resource decision
  (`037a0de1…`), by absolute path and SHA-256; these are the digests the adopted tool
  refuses to run without
- **Command** — `python -B -P -W error::ResourceWarning tools/v0a_eval_panel.py run
  --reviewed-commit 1c706744… --plan plans/solve.json`, cwd = checkout, no `--development`
- **Environment** — scrubbed; `SystemRoot TEMP TMP` retained; `PONTIUS_GIT=C:/Program
  Files/Git/cmd/git.exe`; `PYTHONDONTWRITEBYTECODE=1`; no inherited run context

Full detail in `identity.json`; the invocation script is `invoke.sh`.

## What is requested

**One retained solve invocation** on the binding above. It runs exactly once. The
authorization is recorded in `authorization.md` before the launch (the script refuses to
start without it). An interrupted, failed or ambiguous invocation consumes the
authorization and is never retried as if it had not happened; its result, stdout, stderr,
exit code and journal row are retained regardless of outcome.

Not requested and not implied: the export and agreement phases (each needs its own bound
plan, rehearsal, review and one-shot authorization — see `campaign-note.md`), a second
solve, integration of anything into `master`, or any change to the adopted source.

## Rehearsal (not evidence)

The same script, command, environment and plan bytes were run once with `REHEARSAL=1` in
a disposable detached snapshot at the same commit; the snapshot was then removed. Records
are in `rehearsal/` (`receipt.json`, the invocation log and raw captures); they are
labeled rehearsal and feed nothing.

- **Solve** — completed, exit 0, 19 s wall, worker 16.0 s; stderr empty under
  `-W error::ResourceWarning`; `source_verified` true; `cleanup_verified` true
- **Census** — 1,081 of 1,081 hands; 545 raise-to-2 rows and 536 CHECK rows (both action
  categories present, as design section 3 requires host agreement to observe later)
- **Ties** — zero exact ties, so the tie search reports `absent_in_completed_pool` over the
  completed census; no singleton reference check was triggered
- **Production per hand (untraced)** — 0.013–0.066 s, mean 0.014 s, 15.5 s in total; the
  preflight's estimate was 15.8–71.4 s
- **Peak worker Job memory** — 787 MiB (38% of 2048 MiB)
- **Teacher** — `teacher.json`, 241,587 bytes, SHA-256 `c3ffab40…`, retention complete; the
  retained run should reproduce this digest (a diagnostic comparison only; the retained
  bytes are the identity)

A rehearsal chain then consumed that rehearsal teacher to exercise the later phases'
mechanics: a declared-full export (wire 1,010,990 bytes, membership passed on all 1,081
hands) and a four-hand solve/export/agreement through the real host (four hits, three
controls as designed). Numbers and one memory finding for the agreement plan are in
`campaign-note.md` and `rehearsal/chain-receipt.json`.

Against the plan's limits the rehearsal used about 3% of the 600 s and 38% of the
2048 MiB. The limits are left exactly as the controller decided, so the retained run
binds the reviewed plan bytes unchanged.

## After authorization

`invoke.sh` runs once with stdout/stderr/exit captured; the result, journal row and
teacher artifact are bound by hash in `invocations/`; journal and STATUS.md are committed
on `claude/eval-panel-solve`; a measured report returns here naming completed hands, the
tie census outcome, cost, memory and the teacher identity. The export plan then binds this
run's `teacher.json` and `result.json` by absolute path and SHA-256.

Suggested wording if granted: "I authorize one retained solve invocation on
1c7067448106cfa2aca3d57be879842d72293c61 as bound in identity.json."
