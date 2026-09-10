# Retained full-pool host agreement: completed

The authorized retained agreement ran once on 2026-09-10 and completed. This states what was
measured. It establishes no teacher strength, equilibrium quality or transfer, and authorizes
nothing further.

This file sits outside the reviewed manifest `8485039b…`, which is unchanged by the run, as
do `authorization.md` and `invocations/`. The packet's own `measured-report.md` remains the
pre-run envelope measurement it always was; this is the record of the run itself.

**Slice A's bridge is complete.** A teacher solved for the full pool, exported to a blueprint
artifact, and now reproduced through the unchanged host for every hand in that pool.

## What ran

- **Authorization** — `authorization.md`, recorded verbatim as a single line at
  2026-09-10T20:06:00Z, before the wrapper ran and before any claim was acquired. Every
  identity it names was recomputed from the bytes and matched first: the source commit, the
  reviewed manifest over all 65 members, the wrapper digest, and the envelope.
- **Source** — `1c7067448106cfa2aca3d57be879842d72293c61`; `source_verified` true.
- **Checkout** — `D:/Pontius-worktrees/eval-panel-agreement-20260910` on
  `claude/eval-panel-agreement`, CPython 3.14.6 with NumPy 2.5.2.
- **Plan** — `plans/agreement.json`, SHA-256 `525944ae…`, byte-identical through all four
  packet revisions; the result echoes the same digest.
- **Wrapper** — `invoke.sh`, SHA-256 `d030bcba…`, run once in retained mode with no rehearsal
  flag and no root overrides. Claim taken at 20:06:10Z with 59 journal rows before the run.
- **Producer inputs** — the retained export run `cf3bcdda`: teacher `c3ffab40…`, blueprint
  `666021c4…`, result `00d9b9a0…`, each verified against the plan before the claim.
- **Envelope** — 2,400 s / 3,072 MiB, the per-phase decision adopted on 2026-09-10.

## Result

| Measure | Value |
|---|---|
| Outcome | completed, exit 0, evidence complete |
| Wall time | 1,150 s wrapper, 1,146.0 s worker |
| Peak worker Job memory | 1,623.8 MiB, 53% of the limit |
| Hands played | 1,081 of 1,081, one real host session each |
| Hits | 1,081 |
| Disagreements | none |
| Exclusions | none |
| Missing outcomes | none |

`phase_complete`, `cleanup_verified` and `resource_state_verified` are true, the worker
exited 0, and the error list is empty. Time used 48% of its envelope, memory 53%.

**Witness census complete.** 98,304 draws produced 73,226 collisions, 23,997 unused draws and
exactly 1,081 witnesses, one per required hand, none missing. The bank of 6,144 seeds by 16
indices did in practice what its union bound predicted.

**All three controls behaved as designed.** The off-pool artifact classified unsupported
while staying chip-eligible, the CHECK-hit artifact hit, and the changed-stack replay recorded
zero table hits.

**Schedule reconciled.** 1,084 attempts scheduled, 1,084 observed, no missing outcomes and no
missing pool hands. Per-attempt cost ran 0.506 to 1.599 seconds, mean 1.053.

**Both action categories were observed** in the host-played pool, check and raise-to-2, which
the design requires to be observed rather than presumed.

## Retained artifacts

In `experiments/results/runs/44b6dd6a3fc84760933b0a2e65a18be2/` under the agreement checkout,
bound in `invocations/retained-files.txt`:

- `result.json`, 48,932,851 bytes, SHA-256 `55111052…`, named by the journal row
- `control-off-pool.json`, 1,010,010 bytes, and `control-check-hit.json`, 1,034 bytes, both
  retained complete
- `host-inputs/host-blueprint.json` and `host-inputs/host-input.json`, the last session's
  inputs, which the corrected inventory walks rather than choking on
- `runtimes.json`, 342 bytes

**Evidence path.** Exactly one new journal row appeared, rows 59 to 60. The attribution helper
reported BOUND only after checking that the row names the adopted commit and binds an existing
result file by digest. The end record states `evidence: complete`. Journal and STATUS.md are
committed at `3df2ee2` on `claude/eval-panel-agreement` and pushed. The run directory stays on
disk under the retention convention and should be mirrored with the other retained runs.

## Scope, and what this does not establish

The claim in `invocations/claim.d/` is consumed and this authorization is spent.

Agreement establishes that the exported artifact reproduces the teacher's action through the
unchanged host, for this pool, on this board, at this stack depth, with this replayed prefix.
It says nothing about whether the teacher plays well.

The limits recorded before the run stand unchanged. The full pool has no off-pool complement,
so the default path rests on one synthetic control rather than a population. No genuine host
disagreement has ever been observed, because teacher and host agree by construction; the
classifier's disagreement path is exercised by relabelling a real capture. The worker Job
limit bounds neither the parent process nor disk, and the parent's live peak remains
unmeasured for every phase of this campaign.

## What follows

Slice B is unblocked. It must draw its population from the reserved holdout seed range and
never from the witness draws selected here.

The carried findings for the Slice B interface are in `next-phase.md`, along with the
consolidation the controller has agreed: one small tested runner with phase-specific data,
now that three phases have been worked, with fewer duplicated rules, explicit state
transitions, and independence from the code it launches.
