# Measured basis for the agreement envelope

Full-pool agreement rehearsal, 2026-09-10, in a disposable detached snapshot at the adopted
source commit. **Not evidence.** Its purpose is to measure what no earlier run determines,
and it feeds nothing. The retained agreement phase must bind the retained export's outputs;
this rehearsal consumed the export rehearsal's snapshot copies, which is why none of it can
stand in for a retained result.

## The headline: the inherited envelope would have failed on both axes

The solve and the export both ran inside 600 seconds and 2,048 MiB, and both peaked near
790 MiB. Agreement does not resemble them.

| | Observed | Solve/export envelope | Verdict |
|---|---:|---:|---|
| Wall time | 1,199 s | 600 s | **would be killed** |
| Worker Job peak | 1,625.1 MiB | 2,048 MiB | 1.26x headroom, uncomfortably tight |

Had the recorded resource decision simply been carried forward, the retained agreement run
would have been terminated at the budget roughly halfway through its host sessions, consuming
its one-shot authorization and retaining a failed result. That is the single most useful thing
this rehearsal establishes.

## Proposed envelope

**2,400 seconds and 3,072 MiB worker Job memory.** These require the controller's own
decision; nothing here adopts them.

- Time: 2,400 s is 2.0x the observed 1,199 s. The workload is 1,084 real host sessions plus
  a 98,304-draw scan, so wall time moves with machine load, and a budget kill costs the
  authorization rather than merely the run.
- Memory: 3,072 MiB is 1.89x the observed 1,625.1 MiB peak, against 1.26x at 2,048 MiB. The
  workload is deterministic, so run-to-run variance should be small, but the margin at
  2,048 MiB leaves little room for an interpreter or allocator difference.

## What the rehearsal did

Plan digest `80b5c45d…`, bank of 6,144 seeds by 16 indices, admitted by the frozen validator
before launch. It ran under a deliberately generous 5,400 s / 12,288 MiB so the true peak
would be observed rather than truncated by the Job limit; that generous envelope is a
measuring instrument and is not what is proposed.

**Outcome: completed, exit 0, empty stderr.** `phase_complete`, `cleanup_verified` and
`resource_state_verified` all true, worker exit 0, no errors.

- **Witness census complete.** 98,304 draws produced 73,226 collisions (74.5%, matching the
  predicted 1 - 0.2532), 23,997 unused and exactly 1,081 witnesses, one per required hand.
  Nothing was missing, so the bank sizing holds in practice as well as in the bound.
  The scan itself took 2.40 s.
- **Every primary attempt hit.** 1,081 scheduled, 1,081 observed, 1,081 hits, zero
  disagreements, zero excluded, zero missing, complete true.
- **All three controls behaved as designed.** The off-pool control classified unsupported,
  the CHECK-hit control hit, and the changed-stack control classified unsupported with zero
  table hits.
- **Schedule reconciled.** 1,084 scheduled attempts, 1,084 observed, no missing outcomes and
  no missing pool hands.
- **Both action categories present** in the host-observed pool, check and raise-to-2, which
  design section 4 requires to be observed rather than presumed.

Per-attempt cost was 0.518 s minimum, 1.098 s mean, 1.677 s maximum, 1,190 s in total, so
the host sessions dominate the run. Each attempt rewrites the 1,010,990-byte blueprint into
the host input directory, which is part of that cost.

Retained by the run: `result.json` at 48,934,237 bytes, `control-off-pool.json` at 1,010,010
bytes, `control-check-hit.json` at 1,034 bytes, and `runtimes.json`. The result is roughly
fifty times the size of the export's, because it carries 98,304 draw observations and 1,084
full host session results.

## Parent memory, and a failed measurement I am reporting rather than hiding

Every review of this campaign has recorded that the Job limit bounds the worker and that the
parent, which holds every drained observation before writing, has never been measured. I set
out to close that gap by sampling the launched process from outside during the rehearsal.

**That measurement failed, and its number is void.** It reported a constant 4.5 MiB. The venv
`python.exe` is a launcher stub that runs the real interpreter as its own child, so the
sampler measured the stub for the whole twenty minutes. I confirmed the failure rather than
inferring it: the same sampler, pointed at a process that allocated and touched 600 MiB,
also reported 4.5 MiB. Adding correct `ctypes` signatures changed nothing, which rules out
handle truncation as the cause.

What I can state instead is a **reconstruction, not a live sample.** Loading the retained
report, serialising it and encoding it, exactly what the parent does at the end of a run,
measured by self-measurement, which no launcher stub can distort:

| Stage | Peak working set |
|---|---:|
| Baseline | 16.2 MiB |
| Report read | 62.8 MiB |
| Report parsed | 239.4 MiB |
| Serialised and encoded | 286.4 MiB |

So the parent's dominant term is roughly 270 MiB above baseline for a run of this shape. The
live parent additionally held its event queue, its reader threads and the worker's pipe
buffers, which are small beside the report, and it built the observations incrementally
rather than parsing them in one pass. Treat 286 MiB as an estimate of the same order, not as
the observed live peak. The live peak remains unmeasured, and the correct fix, sampling the
whole process tree rather than the launched PID, belongs to whoever next needs the number.

None of this affects the proposed envelope, which bounds the worker Job only.

## Limits

This is one observation of a deterministic workload on one machine. It establishes no host
agreement result, no teacher strength, no equilibrium quality and no transfer to other
boards or budgets: the retained agreement run is the only thing that can establish agreement,
and it is neither requested nor authorized here. The rehearsal consumed snapshot copies of the
export rehearsal's outputs, so its own artifacts must never substitute for retained ones. The
per-attempt and total costs would change if the pool, the board or the bank changed.
