# Agreement phase preparation

Drafter: Claude, 2026-09-10. This is a **preparation packet, not a frozen candidate.** It
carries the decisions, the wrapper, the helpers and their executed checks, and the measured
basis for an envelope. It is not frozen, and it requests nothing.

## Status: the bindings now exist

When this packet was started the retained export had not run, so the plan could not be
bound. That changed while the packet was being drafted: the controller approved one retained
export and it completed on 2026-09-10, run cf3bcdda, exit 0, evidence complete. Its outputs
are now real files with real digests:

| Input | SHA-256 | Bytes |
|---|---|---:|
| teacher.json | c3ffab40... | 241,587 |
| blueprint.json | 666021c4... | 1,010,990 |
| result.json | 00d9b9a0... | 194,697 |

They live under the permanent export checkout, in
experiments/results/runs/cf3bcdda9eed4031938c214959b1e10c/. So this packet can graduate from
preparation to a candidate as soon as the envelope is decided: the three input bindings, the
plan digest and the wrapper constants can all be filled from those files. Nothing in this
packet is frozen yet, and nothing requests authorization.

The blueprint digest equals the one both rehearsals produced, which is what the
deterministic export contract predicts. The rehearsal copies in this packet remain rehearsal
copies and must never substitute for the retained files above.

## What the agreement phase does, from the frozen source

At the source commit, `agreement` reads the exported teacher and wire, re-derives the wire
from the teacher and requires byte equality, scans the whole declared witness bank, and then
requires a witness for every hand in the pool. It plays one real host session per hand and
then three controls: an off-pool artifact with the first hand's key removed, a CHECK-hit
artifact carrying only that key, and a changed-stack replay. For the full pool that is 1,084
host sessions. Acceptance requires every primary attempt to classify as a hit, the off-pool
control to be chip-eligible and unsupported, the CHECK-hit control to hit, and the
changed-stack control to be chip-eligible with zero table hits. The schedule is reconciled
attempt by attempt against the admitted order.

## The witness bank

The bank is the one substantive new decision this phase needs, and the frozen validator
requires it to carry its own sizing rationale.

Per draw, the collision-free fraction is C(47,12)/C(52,12) = 0.253181, and conditional on a
collision-free draw the controlled hand is uniform over the 1,081 compatible hands. So the
probability that one draw supplies one specific required hand is 2.342102e-4.

| Seeds | Draws | Expected witnesses per hand | Union bound on any hand missing |
|---:|---:|---:|---:|
| 2,048 | 32,768 | 7.7 | 5.0e-01 |
| 4,096 | 65,536 | 15.3 | 2.3e-04 |
| **6,144** | **98,304** | **23.0** | **1.1e-07** |
| 8,192 | 131,072 | 30.7 | 5.0e-11 |

**Proposed: 6,144 seeds by all 16 indices, 98,304 draws.** The union bound is a planning
estimate only. The draws come from one deterministic dealer and may be dependent, so
acceptance rests on the actual complete census and not on the bound. An incomplete census
fails the run and consumes its authorization; the pool is never shrunk and no seed is added
after seeing the outcome. Larger banks buy little: the bound is already far below any other
risk in this phase, and both memory and result size grow with the draw count.

**Holdout reservation.** The bank declares a disjoint holdout seed range that this lane never
opens. Slice B's analysis population must come from that range, and the validator refuses a
bank whose development and holdout ranges overlap. The witness draws selected here answer a
finite correctness question and must never become Slice B's sample.

## The wrapper

Derived from the export wrapper, with two deliberate changes, each answering a finding the
export round produced. Everything else is unchanged: mode guard, override refusal including a
set-but-empty value, atomic claim before any record or launch, checked record writes,
`noclobber` captures, journal attribution that never substitutes an older row, and the exit
precedence that returns a nonzero child status before the incomplete-evidence code.

1. **The required launch environment is checked before the claim, exit 79.** The export
   wrapper expands `SystemRoot`/`SYSTEMROOT`, `TEMP` and `TMP` under `set -u` below the
   claim, so a shell lacking any of them consumes the one-shot claim and starts no child.
   That was graded Advisory there, correctly, because reopening a frozen wrapper for a hazard
   that has never occurred was not worth the cost. This is a new wrapper, so the check costs
   nothing and the hazard is removed rather than documented.
2. **Input digests are verified against the plan, exit 80, not against duplicate constants.**
   The export wrapper pinned each producer input digest twice, in the plan and again in the
   wrapper. That is a drift hazard with no benefit, since the wrapper already pins the plan's
   own digest. `verify_plan_inputs.py` checks every member of the plan's `inputs` object:
   absolute path, regular file, digest match. The plan becomes the single source of truth,
   and the check still runs before the claim.

## Checks executed now

`checks/helper-checks.py`, receipt `checks/helper-checks.json`: 23 cases, 0 failures, opening
with a negative control that proves the gate records a mismatch. It covers both helpers,
which do not depend on any binding filled at freeze.

For `journal_attribution.py`, carried unchanged, it adds the four refusal families the export
round's cold review named as unexercised: an unparsable row, an absent or non-string
`output`, a missing output file, and a `runtimes_sha256` that disagrees with the sibling
`runtimes.json`. That last one matters most, because the run owner always writes
`runtimes_sha256` when an output directory is set, so a real retained row carries it while
only the passing side had ever been exercised. Both the mismatching and the matching case now
run.

For `verify_plan_inputs.py`, it covers a fully bound plan, a wrong digest, a missing file, a
relative path, three malformed member shapes, an empty inputs object, an unreadable plan and
a missing argument.

The wrapper-level suite, the modes, the environment guard, the claim, the two-caller race and
the exit tail, runs against the filled wrapper at freeze. It is not claimed here.

## What the rehearsal measures

No earlier measurement determines this phase's envelope. The solve and export both peaked
near 790 MiB, but agreement's memory and result size grow with the witness bank and with the
pool at once: every draw is emitted as an observation and also retained inside the scan
report, and every one of the 1,084 attempts retains a full host session result. A four-hand
subset with a 65,536-draw bank already produced a 20 MB result and a 1,560 MiB worker peak.

The rehearsal therefore runs the full pool with the proposed bank, in a disposable detached
snapshot, under a deliberately generous envelope so the true peak is observed rather than
truncated by the Job limit. It also attempted to sample the parent process's peak working set,
to close a gap every review so far has recorded: the Job limit bounds the worker, and the
parent that holds every drained observation before writing has never been measured. That
attempt failed and its number is void; `measured-report.md` records why, and reports a
reconstruction in its place. The results and the envelope proposal are in that report.

## What must still be filled, and by whom

At freeze, now that the retained export has completed: the three input bindings and their digests,
the plan digest, the wrapper's retained root, packet path and helper digests, and the
executed wrapper-level suite. Then one review, then the controller's own one-shot
authorization for the agreement invocation, which nothing here requests or implies.

Nothing in this packet establishes host agreement, teacher strength, equilibrium quality or
transfer to other boards or budgets.
