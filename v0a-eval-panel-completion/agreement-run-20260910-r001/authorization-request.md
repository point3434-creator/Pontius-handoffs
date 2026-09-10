# Authorization request: retained full-pool host agreement

Drafter: Claude, 2026-09-10. **Not executed; awaiting one Codex review and then the
controller's explicit one-shot authorization.** This document requests authority and grants
none. It is the third and last of the three retained phases design step 7 requires.

## What is bound

- **Source** — `1c7067448106cfa2aca3d57be879842d72293c61`, the adopted head of
  `codex/eval-panel-completion-adopted`, tree `3d2fe79d`. No project source changed.
- **Execution checkout** — `D:/Pontius-worktrees/eval-panel-agreement-20260910`, branch
  `claude/eval-panel-agreement`, HEAD at the adopted commit, source scope clean, seven
  on-disk run directories equal to the seven tracked, CPython 3.14.6 with NumPy 2.5.2.
  Separate from the solve and export checkouts.
- **Plan** — `<checkout>/plans/agreement.json`, copy at `plans/agreement.json`, SHA-256
  `525944ae…`, 14,462 bytes. Phase `agreement`, `declared-full`, pool 1,081 on the
  development board, the retained pool seed and full permutation.
- **Producer inputs, from the retained export run `cf3bcdda`** — `teacher.json`
  `c3ffab40…`, `blueprint.json` `666021c4…`, `result.json` `00d9b9a0…`, each by absolute
  path and SHA-256. The frozen `teacher_input` was executed against them and accepted.
- **Prerequisites** — the retained capacity and preflight results and the 2026-09-09
  resource decision, at the three digests the adopted tool compiles in.
- **Witness bank** — 6,144 seeds by all 16 indices, 98,304 draws, with its sizing rationale
  and a disjoint holdout range reserved for Slice B and never opened by this lane.
- **Wrapper** — `invoke.sh`, SHA-256 `d030bcba…`, with `journal_attribution.py` and
  `verify_plan_inputs.py`, both digests pinned inside it.

Full detail in `identity.json`.

## Envelope

**2,400 seconds and 3,072 MiB of worker Job memory**, from the per-phase resource decision
of 2026-09-10 that the controller adopted, copied here at
`inputs/resource-decision-20260910.md`. Its basis is a full-scale rehearsal at 1,199 seconds
and 1,625.1 MiB, giving 2.0x and 1.89x.

This is the one number that could not be inherited. The 2026-09-09 decision covered the
solve; carrying it forward would have killed this run at 600 seconds, roughly halfway
through its host sessions, consuming the authorization and retaining a failure.

## What is requested

**One retained agreement invocation** on the binding above. It runs exactly once. The
wrapper refuses to start without `authorization.md`, refuses a second caller at the atomic
claim, and never retries. A refusal before the claim consumes nothing. Every failure after
the claim leaves it consumed, and what an abandoned claim means is the controller's call.

Not requested and not implied: a second agreement run, any change to the adopted source, any
integration into `master`, or anything in Slice B.

## Rehearsal and checks, neither of which is evidence

Full-pool rehearsals in disposable detached snapshots, the last of them driven by this exact
frozen wrapper as a two-caller race. Each completed the phase: 1,081 primary hits, no
disagreement, no exclusion, a complete witness census, and the three controls as designed.

Both claim refusal paths have receipts, which no earlier phase obtained. In the RED rehearsal
retained at `rehearsal-red/`, both callers passed the read-only preconditions in the same
second and the loser lost at the atomic `mkdir`, which is the concurrent-acquisition window
itself. In the green rehearsal the loser stopped earlier, at the pre-claim existence check.
The RED rehearsal is retained because it also found a real wrapper defect, described there
and in `disposition.md`.

Executed checks, 63 cases with 0 failures across two suites, each opening with a negative
control that proves the gate records failures: 23 helper cases covering both helpers,
including the four attribution refusal families the export round named as unexercised and a
byte comparison of every copied journal row, and 40 wrapper cases covering the environment
guard, the mode boundary, the override refusals, the rehearsal-root separations, the
plan-input guard as a source slice, the retained-file inventory including three controls for
a failed, partial or empty enumeration, and all eight combinations of child status and
evidence state.

## After authorization

`authorization.md` is written verbatim with a UTC timestamp before the launch, the wrapper
runs once in retained mode, and the claim, captures, attributed journal row and retained-file
digests are recorded under `invocations/`. Journal and status are committed on
`claude/eval-panel-agreement`, and a measured report returns here.

The exact approval wording is one physical line in `authorization-template.txt`, which sits
outside the frozen manifest so that it can name that manifest's own digest.
