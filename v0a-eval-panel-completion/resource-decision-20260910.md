# Resource decision, per phase — adopted 2026-09-10

**Status: ADOPTED by the controller 2026-09-10T14:59:45Z.**

Controller, verbatim: "let's amend the envelope to your suggestion then let's get a
candidate"

The suggestion referred to is the agreement envelope proposed in this document, 2,400
seconds and 3,072 MiB of worker Job memory, together with the per-phase structure and the
derivation rule below. Adoption decides the envelope only. It authorizes no invocation:
the agreement run still needs its own bound plan, its own review and its own one-shot
authorization.

## Why the old decision needs replacing

The decision of 2026-09-09 records one envelope, 600 seconds and 2,048 MiB, derived from the
capacity and preflight prerequisite runs and written for the full-pool solve. It says so
plainly. What has happened since is that it was read as the campaign's envelope rather than
the solve's, and that reading nearly cost a run.

| Phase | Observed | Under 600 s / 2,048 MiB |
|---|---|---|
| Solve, retained | 22.7 s worker, 788.1 MiB peak | ample |
| Export, retained | 12.6 s worker, 788.1 MiB peak | ample |
| Agreement rehearsal | 1,194.4 s worker, 1,625.1 MiB peak | **killed on time; 1.26x memory** |

Had the old figure been carried into the agreement plan, the retained run would have been
terminated at the budget roughly halfway through its 1,084 host sessions, consuming its
one-shot authorization and retaining a failed result. The envelope is not a campaign
constant. It is a per-phase quantity, because the phases do not resemble each other: solve
and export are single-pass computations over 1,081 hands, while agreement runs 1,084 real
host sessions and holds a witness scan of nearly a hundred thousand draws.

## What is decided

**One envelope per phase, each derived from a full-scale rehearsal of that phase.**

| Phase | Seconds | Worker Job MiB | Basis | State |
|---|---:|---:|---|---|
| Solve | 600 | 2,048 | prerequisite preflight | executed, spent |
| Export | 600 | 2,048 | export rehearsal, 15 s / 787.8 MiB | executed, spent |
| Agreement | **2,400** | **3,072** | full-pool rehearsal, 1,199 s / 1,625.1 MiB | **adopted** |

The solve and export figures are recorded as history, not reopened. Both phases have run and
their authorizations are consumed. The solve figure additionally cannot be changed: the
adopted tool hardcodes `600 / 2048` for phase `solve`, so any other value would be refused.

## The rule for deriving an envelope

So that the next phase does not need a fresh judgement call:

1. Rehearse the phase **at full scale**, in a disposable detached snapshot, under a
   deliberately generous envelope chosen so the true peak is observed rather than truncated.
   A smaller-scale rehearsal does not license an envelope; the agreement phase's memory grows
   with both the witness bank and the pool, so a four-hand subset told us nothing usable.
2. Set seconds to **twice the observed wall time**, rounded up to the next 100 seconds.
3. Set worker Job memory to **1.9 times the observed peak**, rounded up to the next 256 MiB.
4. If either number exceeds **3,600 seconds or 4,096 MiB**, stop and return to the controller
   with the measurement instead of applying the rule. A phase that large deserves a fresh
   decision about whether to run it at all.

Applying the rule to the agreement measurement gives 2,400 seconds and 3,072 MiB, which is
what the table proposes.

The margins are deliberate. A budget kill does not merely fail a run: it consumes a one-shot
authorization and leaves a retained failure, so the cost of a wall set too tight is far higher
than the cost of one set generously. The margins are still measured, not invented, which is
what the standing prohibition on unmeasured walls requires.

## What the envelope does and does not bound

It bounds the **worker Job only**. The parent process that supervises the worker and holds
every drained observation before writing is outside the Job limit and is not bounded by any
number here.

For the agreement rehearsal the parent's dominant term was reconstructed at about 286 MiB
over a 16 MiB baseline, by loading, serialising and encoding the retained report. That is a
reconstruction, not a live sample. My attempt to sample it live failed and its number is
void: the venv `python.exe` is a launcher stub, so the sampler measured the stub for the
whole run and reported a constant 4.5 MiB, which I confirmed by pointing the same sampler at
a process that touched 600 MiB and reading 4.5 MiB again. The live parent peak remains
unmeasured for every phase of this campaign, and the correct method is to sample the process
tree rather than the launched process.

Disk is not bounded either. The agreement result is 48.9 MB against the export's 0.19 MB,
because it carries 98,304 draw observations and 1,084 full host session results.

## Relationship to the pinned file

`prerequisite-run-20260909/resource-decision.md` **must not be edited.** Its digest
`037a0de1…` is one of the three `PREREQUISITES` constants compiled into the adopted tool, and
the tool re-reads and re-hashes that exact file before admitting any declared-full phase.
Changing one byte would make every remaining phase refuse with "prerequisite differs from
resource decision", and would invalidate the export packet that pins it.

That pin proves a resource decision existed and was bound to the plans. It does not carry the
decision's content into the tool: the tool never reads the file. So this document supersedes
the earlier decision's **scope** while leaving its **bytes** untouched, and plans continue to
pin the original file exactly as they do now. What governs an invocation is the `resource`
object inside its plan, which the controller approves per phase.

## Suggested adoption wording

"I adopt the per-phase resource decision of 2026-09-10: agreement runs under 2,400 seconds
and 3,072 MiB worker Job memory, envelopes are derived per phase from a full-scale rehearsal
by the stated rule, and prerequisite-run-20260909/resource-decision.md stays byte-identical
because the adopted tool pins it."

Adopting this decides the envelope. It does not authorize the agreement invocation, which
needs its own bound plan, its own review and its own one-shot authorization.
