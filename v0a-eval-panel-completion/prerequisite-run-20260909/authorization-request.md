# Authorization request: retained capacity and preflight invocations

Drafter: Claude, 2026-09-09. Status: **not executed; awaiting the controller's
explicit one-shot authorization.** This supersedes the source binding in
`preparation-20260909/prerequisite-run-plan.md` (bound to `d8d291cc`, which the
timing disposition says is not authority to run). The run plan's execution
boundary, phase order and retention rules are otherwise followed as written.

## What is bound

- **Source** — `beb84be566aa28029284bd35c526d33cd27af369` — adopted head of
  `codex/eval-panel-timing`; tree `d26c3fb1` identical to the reviewed candidate `a40e29ca`
  (timing/r002: two CLEAN/SOUND cold reviews, broad 583 passed / 10 optional skips)
- **Execution checkout** — `D:/Pontius-worktrees/eval-panel-prerequisite-20260909`, branch
  `claude/eval-panel-prerequisite`, HEAD = source; source scope clean; permanent, mirrored
- **Interpreter** — `<checkout>/.venv/Scripts/python.exe`, CPython 3.14.6, `uv sync --locked
  --offline --group dev`
- **Capacity plan** — `<checkout>/plans/capacity.json`, bytes of blob `5040350e`, SHA-256
  `6ad3e205…`, 600 s / 2048 MiB
- **Preflight plan** — `<checkout>/plans/preflight.json`, bytes of blob `6f8d92d2`, SHA-256
  `d2e5c04c…`, 3600 s / 2048 MiB, `declared-full`: As Ad, Kh Kd, Td 8d, 3c 4d on 2c 7d 9h Js Qc;
  control 2c 3d on Ts Js Qs Ks As
- **Command** — `python -B -P -W error::ResourceWarning tools/v0a_eval_panel.py run
  --reviewed-commit beb84be5… --plan plans/<phase>.json`, cwd = checkout, no `--development`
- **Environment** — scrubbed; `SystemRoot TEMP TMP` retained; `PONTIUS_GIT=C:/Program
  Files/Git/cmd/git.exe`; `PYTHONDONTWRITEBYTECODE=1`; no inherited run context

Full detail in `identity.json`.

## What is requested

1. **One retained capacity invocation** on the binding above.
2. **One retained preflight invocation**, conditional on the capacity invocation
   completing with a nonempty fitting pool. If capacity fails, interrupts, or fits
   nothing, the sequence stops and its result is retained; the preflight is not run.

Each phase runs exactly once. Authorization and invocation start are recorded
before each launch. An interrupted or ambiguous invocation consumes its
authorization and is never retried as if it had not happened; its result, stdout,
stderr and exit code are retained regardless of outcome.

Not requested and not implied: the full-pool solve, export, agreement, ceremonial
integration of anything, or design steps 4–7. After both phases, the measured
report returns to the controller for the resource decision that step 4 requires.

## Rehearsal (not evidence)

Before this request, the same command, environment and plan bytes were run once in
a disposable detached snapshot at the same commit, then the snapshot was removed.
Records are in `rehearsal/`; they are labeled rehearsal and feed nothing. Their
purpose is the amendment's "separate rehearsal, measured operating bounds, then
one-shot authorization" order — so the limits below are authorized against
observed behaviour, not guesses.

- **Capacity** — completed, exit 0, 6 s wall; all 1,081 hands fit at 1,012,625 bytes (3.4% headroom
  under the 1,048,576 cap); boundary artifact bound; cleanup verified
- **Preflight** — completed, exit 0, 31 s wall; 5/5 units complete; four development hands `agree`,
  royal control exact `tie`; cleanup verified
- **Production per hand (untraced)** — cold 0.065 s (first hand), then 0.014–0.019 s; warm 0.014 s
- **Reference per hand** — ≈ 1.6 s construction + 0.8 s forced CHECK + 0.9 s forced BET + 2.4 s best
  response ≈ 5.7 s
- **Full-pool production estimate (tool's own, labeled estimate)** — 15–70 s over 1,081 hands, mean
  31 s, `timing_mode: untraced-body-v1`
- **Peak worker Job memory** — ≈ 780–800 MiB (whole worker process including NumPy)
- **Stderr** — empty for both phases under `-W error::ResourceWarning`

Against the plan's limits: capacity used ~1% of its 600 s; preflight ~1% of its
3600 s; memory ~39% of 2048 MiB. The limits are ample and are left unchanged so
the retained run binds the reviewed plan bytes exactly.

For calibration only: the r001 development diagnostic projected full-H production
at 1.1–5.9 minutes under allocation tracing; the untraced rehearsal projects
15–70 s. That is the I-01 inflation observed on the real workload, roughly 4–5×.

## After authorization

Capacity, then preflight, each with stdout/stderr/exit captured; results,
journal rows and the boundary artifact bound by hash; journal and STATUS.md
committed on `claude/eval-panel-prerequisite`; a measured report returned here
naming capacity-selected H, boundary size, per-hand cost spread, memory, stage
and comparison outcomes, and the estimate labeled as such.

Suggested wording if granted: "I authorize one retained capacity invocation and,
on nonempty capacity success, one retained preflight invocation on
beb84be566aa28029284bd35c526d33cd27af369 as bound in identity.json."
