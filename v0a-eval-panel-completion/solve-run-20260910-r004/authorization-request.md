# Authorization request: retained full-pool solve invocation (r004)

Drafter: Claude, 2026-09-10. Status: **not executed; awaiting one cold Codex review under
controller-review-policy-20260909 and then the controller's explicit one-shot
authorization.** This packet corrects `solve-run-20260910-r003`, whose cold review returned
NOT CLEAN over three Minors: the race check did not assert the caller-status pair it
printed, an explicitly empty `REHEARSAL` was normalised to retained mode, and the
claim-consumption promise also covered precondition refusals that consume nothing. The plan
bytes are unchanged through all four packets. It is the first of the three retained phases
that design step 7 requires
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
- **Wrapper** — `invoke.sh` (SHA-256 `160cfcec…`) with
  `journal_attribution.py` (digest pinned in the script): fixed checkout and packet,
  overrides refused, `REHEARSAL` defaulting to 0 only when unset and any other set value
  refused including an empty string, `authorization.md` required, an
  atomic claim (`mkdir invocations/claim.d`) before any record or launch, checked record
  writes, exactly one launch, and a journal row attached only when exactly one new row
  binds this checkout's result file
- **Exit status** — a nonzero child status is returned unchanged, whether or not the
  evidence is complete; a child that exited 0 with incomplete evidence yields 99; otherwise
  0. No path reports success with incomplete evidence
- **Claim scope** — a precondition refusal happens before the claim exists, consumes
  nothing, and leaves the packet callable again once the refused condition is corrected.
  Every failure from the successful claim onward leaves the claim consumed and is never
  retried
- **Command** — `python -B -P -W error::ResourceWarning tools/v0a_eval_panel.py run
  --reviewed-commit 1c706744… --plan plans/solve.json`, cwd = checkout, no `--development`
- **Environment** — scrubbed; `SystemRoot TEMP TMP` retained; `PONTIUS_GIT=C:/Program
  Files/Git/cmd/git.exe`; `PYTHONDONTWRITEBYTECODE=1`; no inherited run context

Full detail in `identity.json`.

## What is requested

**One retained solve invocation** on the binding above. It runs exactly once: the wrapper
refuses to start without `authorization.md`, refuses a second caller at the claim, and
never retries. An interrupted, failed or ambiguous invocation that reached the claim consumes the
authorization; its claim, captures, exit code and attributed (or explicitly absent) journal
row are retained regardless of outcome, and what an abandoned claim means is the
controller's call. A precondition refusal never reaches the claim: nothing is consumed and
the corrected call may proceed.

Not requested and not implied: the export and agreement phases (each needs its own bound
plan, rehearsal, review and one-shot authorization — `campaign-note.md`), a second solve,
integration of anything into `master`, or any change to the adopted source.

## Rehearsal and fault-path checks (not evidence)

The wrapper was exercised in two fresh disposable detached snapshots at the same commit,
which were then removed. `checks/wrapper-checks.sh` asserts every observable and exits
nonzero on any failure; it ran 20 cases with 0 failures (`checks/wrapper-checks.jsonl`).
It opens with a negative control that feeds the gate a deliberate mismatch and confirms it
records a failing row (`checks/gate-negative-control.jsonl`), so the suite is known to
depend on its comparisons rather than merely on reaching the end. Then: eleven refusals
before any launch (override in retained mode, missing authorization, rehearsal without a
root, rehearsal root equal to the retained checkout, rehearsal root on a branch, a prior
claim, an unwritable record directory, three rejected `REHEARSAL` values including an empty
one, and a failed start record on a labeled one-line mutant), six journal-attribution
outcomes on isolated synthetic journals, one child-failure precedence case, and one race of
two concurrent callers that asserts both the caller-status pair and the single launch.

The child-failure case is the path cold review 02 traced: with the second snapshot's venv
deliberately broken, the tool failed during import before any journal row was appended, the
helper reported ABSENT, the evidence was recorded incomplete, and the wrapper returned the
child's status 1 rather than 99, printing EVIDENCE INCOMPLETE. The corrected contract is
therefore verified by execution, not only by reading.

The race winner's run is the packet's rehearsal (`rehearsal/receipt.json`):

- **Solve** — completed, exit 0, 17 s wall, worker 16 s; stderr empty; evidence complete;
  journal row BOUND (rows 59 to 60) to the run's `result.json`; `source_verified` true
- **Census** — 1,081 of 1,081 hands; 545 raise-to-2 and 536 CHECK rows; zero exact ties, so
  the tie search reports `absent_in_completed_pool`
- **Production per hand (untraced)** — 0.014–0.071 s, mean 0.015 s, 15.7 s in total
- **Peak worker Job memory** — 786 MiB (38% of 2048 MiB)
- **Teacher** — `teacher.json`, 241,587 bytes, SHA-256 `c3ffab40…`, identical to the r001
  through r003 rehearsal digests (deterministic); the retained run should reproduce it, as
  a diagnostic comparison only

The later-phase chain measured in the first packet is carried unchanged in
`rehearsal/chain-receipt.json`; its memory reading is restated in `campaign-note.md`.

## After authorization

`authorization.md` is written verbatim with a UTC timestamp; `invoke.sh` runs once; the
claim, captures, attributed journal row and retained-file digests sit in `invocations/`;
journal and STATUS.md are committed on `claude/eval-panel-solve`; a measured report returns
here. The export plan then binds this run's `teacher.json` and `result.json`.

Suggested wording if granted: "I authorize one retained solve invocation on
1c7067448106cfa2aca3d57be879842d72293c61 as bound in solve-run-20260910-r004/identity.json."
