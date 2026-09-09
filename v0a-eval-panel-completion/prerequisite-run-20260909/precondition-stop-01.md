# Precondition stop 01 — before any launch

At the first attempt to run `invoke.sh` (2026-09-09, after `authorization.md` was
written), the precondition "experiments/results/runs is empty" failed with exit 95.
No phase was launched: `invocation-log.jsonl` has no start event, `invocations/` is
empty, and the checkout's `execution_journal.jsonl` is unchanged (59 rows, equal to
the adopted blob). The authorization is therefore not consumed.

Cause: the predicate was over-specified (review checklist item 8). The adopted tree
`beb84be5` itself tracks run directories under `experiments/results/runs/` despite the
`.gitignore` rule, so a clean checkout is not empty there. The predicate is replaced by
its minimal form: no run directory beyond those tracked at HEAD. The binding step after
the run likewise lists only new directories. The identification of the tracked runs is
recorded in the invocation log's first entry on the next attempt.
