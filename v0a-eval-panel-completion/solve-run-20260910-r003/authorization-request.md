# Authorization request: retained full-pool solve invocation (r003)

Drafter: Claude, 2026-09-10. Status: **not executed; awaiting one cold Codex review under
controller-review-policy-20260909 and then the controller's explicit one-shot
authorization.** This packet corrects `solve-run-20260910-r002`, whose cold review found
one Minor: the prose promised exit 99 for all incomplete evidence while the executable
returns a nonzero child status first. The plan bytes are unchanged through all three
packets. It is the first of the three retained phases that design step 7 requires
after the adoption of completion/r003 (adoption granted no invocation).

## What is bound

- **Source** — `1c7067448106cfa2aca3d57be879842d72293c61`, the adopted head of
  `codex/eval-panel-completion-adopted`; tree `3d2fe79d` identical to the reviewed
  completion/r003 candidate `7ca82180` (controller: "I approve all.")
- **Execution checkout** — `D:/Pontius-worktrees/eval-panel-solve-20260910`, branch
  `claude/eval-panel-solve`, HEAD = source; source scope clean; permanent, mirrored
- **Interpreter** — `<checkout>/.venv/Scripts/python.exe`, CPython 3.14.6, `uv sync --locked
  --offline --group dev`
- **Plan** — `<checkout>/plans/solve.json` (copy: `plans/solve.json`), SHA-256 `c1a6af60…`,
  12,365 bytes, unchanged from the reviewed packet; `pontius-eval-panel-completion-plan-v1`,
  phase `solve`, `declared-full`, pool 1,081 on 2c 7d 9h Js Qc, the retained capacity run's
  pool seed and permutation (digest `344e7eeb…`), envelope 600 s / 2048 MiB exactly as the
  resource decision records
- **Prerequisites bound inside the plan** — the retained capacity result (`29f532a9…`), the
  retained preflight result (`8a17325e…`) and the controller's resource decision
  (`037a0de1…`), by absolute path and SHA-256
- **Wrapper** — `invoke.sh` (SHA-256 `162cc5aa…`) with
  `journal_attribution.py` (digest pinned in the script): fixed checkout and packet,
  overrides refused, `REHEARSAL` restricted to 0 or 1, `authorization.md` required, an
  atomic claim (`mkdir invocations/claim.d`) before any record or launch, checked record
  writes, exactly one launch, and a journal row attached only when exactly one new row
  binds this checkout's result file
- **Exit status** — a nonzero child status is returned unchanged, whether or not the
  evidence is complete; a child that exited 0 with incomplete evidence yields 99; otherwise
  0. No path reports success with incomplete evidence, and every failing path leaves the
  claim consumed
- **Command** — `python -B -P -W error::ResourceWarning tools/v0a_eval_panel.py run
  --reviewed-commit 1c706744… --plan plans/solve.json`, cwd = checkout, no `--development`
- **Environment** — scrubbed; `SystemRoot TEMP TMP` retained; `PONTIUS_GIT=C:/Program
  Files/Git/cmd/git.exe`; `PYTHONDONTWRITEBYTECODE=1`; no inherited run context

Full detail in `identity.json`.

## What is requested

**One retained solve invocation** on the binding above. It runs exactly once: the wrapper
refuses to start without `authorization.md`, refuses a second caller at the claim, and
never retries. An interrupted, failed or ambiguous invocation consumes the authorization;
its claim, captures, exit code and attributed (or explicitly absent) journal row are
retained regardless of outcome, and what an abandoned claim means is the controller's call.

Not requested and not implied: the export and agreement phases (each needs its own bound
plan, rehearsal, review and one-shot authorization — `campaign-note.md`), a second solve,
integration of anything into `master`, or any change to the adopted source.

## Rehearsal and fault-path checks (not evidence)

The wrapper was exercised in two fresh disposable detached snapshots at the same commit,
which were then removed. `checks/wrapper-checks.sh` asserts every observable and exits
nonzero on any failure; it ran 18 cases with 0 failures (`checks/wrapper-checks.jsonl`):
ten refusals before any launch (override in retained mode, missing authorization, rehearsal
without a root, rehearsal root equal to the retained checkout, rehearsal root on a branch,
a prior claim, an unwritable record directory, two rejected `REHEARSAL` values, and a
failed start record on a labeled one-line mutant), six journal-attribution outcomes on
isolated synthetic journals, one child-failure precedence case, and one race of two
concurrent callers in which exactly one claimed and launched while the other exited 97.

The child-failure case is the path cold review 02 traced: with the second snapshot's venv
deliberately broken, the tool failed during import before any journal row was appended, the
helper reported ABSENT, the evidence was recorded incomplete, and the wrapper returned the
child's status 1 rather than 99, printing EVIDENCE INCOMPLETE. The corrected contract is
therefore verified by execution, not only by reading.

The race winner's run is the packet's rehearsal (`rehearsal/receipt.json`):

- **Solve** — completed, exit 0, 16 s wall, worker 16 s; stderr empty; evidence complete;
  journal row BOUND (rows 59 to 60) to the run's `result.json`; `source_verified` true
- **Census** — 1,081 of 1,081 hands; 545 raise-to-2 and 536 CHECK rows; zero exact ties, so
  the tie search reports `absent_in_completed_pool`
- **Production per hand (untraced)** — 0.013–0.067 s, mean 0.014 s, 15.1 s in total
- **Peak worker Job memory** — 787 MiB (38% of 2048 MiB)
- **Teacher** — `teacher.json`, 241,587 bytes, SHA-256 `c3ffab40…`, identical to the r001
  and r002 rehearsal digests (deterministic); the retained run should reproduce it, as a
  diagnostic comparison only

The later-phase chain measured in the first packet is carried unchanged in
`rehearsal/chain-receipt.json`; its memory reading is restated in `campaign-note.md`.

## After authorization

`authorization.md` is written verbatim with a UTC timestamp; `invoke.sh` runs once; the
claim, captures, attributed journal row and retained-file digests sit in `invocations/`;
journal and STATUS.md are committed on `claude/eval-panel-solve`; a measured report returns
here. The export plan then binds this run's `teacher.json` and `result.json`.

Suggested wording if granted: "I authorize one retained solve invocation on
1c7067448106cfa2aca3d57be879842d72293c61 as bound in solve-run-20260910-r003/identity.json."
