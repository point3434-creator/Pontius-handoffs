# Measured report: retained full-pool solve

The authorized retained solve ran once on 2026-09-10 and completed. This report states what
was measured; it establishes no teacher-strength, host-agreement or transfer claim, and it
authorizes nothing further.

## What ran

- **Authorization** — `authorization.md`, recorded verbatim at 2026-09-10T05:50:00Z before
  the launch. Controller: "lets go with what we have thanks for saying that", in reply to
  the choice between one more cold pass on r004 and authorizing as-is with the r003 Minors
  disclosed and corrected.
- **Source** — `1c7067448106cfa2aca3d57be879842d72293c61`, the adopted bridge; the run
  reports `source_verified` true against it.
- **Checkout** — `D:/Pontius-worktrees/eval-panel-solve-20260910` on
  `claude/eval-panel-solve`, CPython 3.14.6, NumPy 2.5.2.
- **Plan** — `plans/solve.json`, SHA-256 `c1a6af60…`, unchanged since the first packet; the
  result echoes the same `plan_sha256` and permutation digest `344e7eeb…`.
- **Wrapper** — `invoke.sh`, SHA-256 `160cfcec…`; claim taken at 2026-09-10T05:49:36Z,
  preconditions passed with 59 journal rows before the run.
- **Envelope** — 600 s / 2048 MiB, exactly as the recorded resource decision states.

## Result

| Measure | Value |
|---|---|
| Outcome | completed, exit 0, evidence complete |
| Wall time | 24 s wrapper, 23.3 s journal duration, 22.7 s worker |
| Peak worker Job memory | 788.1 MiB, 38% of the 2,048 MiB limit |
| Hands solved | 1,081 of 1,081 |
| Action rows | 545 raise-to-2, 536 CHECK |
| Exact ties | none |
| Production per hand, untraced | 0.014 to 0.118 s, mean 0.020 s, 21.9 s in total |

`cleanup_verified`, `resource_state_verified` and `phase_complete` are all true, the worker
exited 0 and the error list is empty.

**Tie census.** No hand produced equal CHECK and bet totals, so the summary records
`absent_in_completed_pool`: absence over the completed census of H, and nothing beyond it.
No singleton reference check was triggered, because the design triggers one only at the
first exact tie with nonzero per-deal returns.

**Retained artifacts**, bound in `invocations/retained-files.txt` and by the journal row:

- `teacher.json`, 241,587 bytes, SHA-256
  `c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3`
- `result.json`, 527,220 bytes, SHA-256 `e6db93c0…`, named by the journal row
- `runtimes.json`, 338 bytes, SHA-256 `12af22dd…`

The teacher digest equals the digest all four rehearsals produced from the same source and
plan bytes, which is what the deterministic export contract predicts. That agreement is a
diagnostic; the retained bytes are the identity.

**Evidence path.** Exactly one new journal row appeared, rows 59 to 60. The attribution
helper reported BOUND and copied that row only after checking that it names the adopted
commit and binds an existing result file by digest. The end record states
`evidence: complete`. Journal and STATUS.md are committed at `0872ba8` on
`claude/eval-panel-solve` and pushed; the run directory
`experiments/results/runs/ded0fe697fbe424aa40ffd5320940d4b/` stays on disk under the
retention convention and should be mirrored with the other retained runs.

## Scope and what remains

The claim in `invocations/claim.d/` is consumed. This authorization is spent; a second
solve would need its own.

Not established here: any teacher-strength, equilibrium or transfer claim; any host
agreement result; any statement about hands, boards or budgets outside this plan. The tie
absence is over the completed census of this H on this board only.

Next, each with its own bound plan, rehearsal, review and one-shot authorization
(`campaign-note.md`): the export phase, which binds this run's `teacher.json` and
`result.json` by absolute path and SHA-256 and needs its own envelope; then the agreement
phase, whose envelope must be measured on a full-pool rehearsal because memory and result
size grow with both the witness bank and the pool. The r004 wrapper's carried follow-ups
apply to the export wrapper: the r002 review's M-01 producer-trust assumption stays
disclosed, and the r003 review's operator duties remain with the operator.
