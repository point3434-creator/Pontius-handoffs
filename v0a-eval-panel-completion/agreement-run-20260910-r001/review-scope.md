# Correction-round scope: the wrapper's retained-file inventory

This describes the diff from the wrapper review 01 saw to the current one. It is kept
current rather than written per review, so a reviewer can always see exactly what has moved
since the last full pass. Review 02 answered an earlier version of it; its findings are
disposed of in `disposition.md`.

## What has not changed, and should not be reviewed again

Review 01 verified the plan, the six input and prerequisite bindings, all manifest members
at that time, 892 source-scope files, all 98,304 candidate draws with the first selected
witness for each of the 1,081 hands, three rehearsal reports across 1,084 sessions, 22,225
frames and 4,336 decisions, and the 545 raises and 536 checks with all three controls.
**None of that has changed.** The plan is byte-identical at `525944ae…`, its bindings are
untouched, the envelope is unchanged, and the retained export inputs are the same files.

Every change since has been inside one post-launch block of the wrapper, its controls, one
strengthened test assertion, and prose.

## The diff

`reviews/reviewed-invoke-6581341a.sh` is the exact wrapper review 01 saw, reconstructed by
reversing the edits and verified by digest against the value that review recorded.
`reviews/wrapper-since-review-01.diff` is the diff from it to the current `invoke.sh`. Every
changed line lies between the `# --- retained file inventory` markers.

Three corrections are in it.

1. **Review 01's I1.** The block fed its loop from a process substitution, whose failure
   status is not collected even under `pipefail`, so an enumeration that returned nothing, or
   part of the tree and then failed, would leave the subshell exiting zero with the evidence
   recorded as complete. Reproduced as an executed fault before correcting, by shadowing
   `find` to fail. The enumeration is now captured by command substitution, whose status does
   propagate and which `pipefail` covers for both `find` and `sort`, its status is checked
   before any output is used, and an empty enumeration for a new run directory is refused.

2. **A residual found by re-reading that fix, confirmed by execution.** With no new run
   directory the loop skipped every tracked directory, wrote nothing, and left the evidence
   complete. A counter now requires at least one new run directory.

3. **Review 02's R2-I1.** The loop's own input redirection can fail before the body runs, and
   a while loop that executed no body command returns zero, so the counter above would have
   masked it. The redirection is now guarded with `|| exit 1`. The here-string's backing
   storage could not be made to fail on this build, bash 5.3.15 on cygwin, and review 02 did
   not establish that behaviour either; the guard is therefore exercised against the same
   construct with a redirection that does fail, and a companion control confirms the guard is
   load-bearing by showing the same block returning zero without it.

## What to attack, if another pass is run

**Is there any remaining path through this block that records complete evidence without a
complete inventory?** Consider at least a filename containing a newline or leading
whitespace, a `find` that succeeds while `sort` fails, a run directory that is unreadable
rather than absent, a symbolic link, and the interaction between `set -u`, `pipefail`, the
here-string and the subshell's exit status.

**Do the controls falsify?** `checks/wrapper-checks.py` runs 12 inventory cases against the
exact frozen slice. Verify they would fail if any correction were reverted, rather than
passing vacuously. One case exists purely to demonstrate that the redirection guard is
load-bearing.

## The rest of the diff

- `checks/helper-checks.py`: the attribution cases compare the copied row bytes, closing
  review 01's M3. On success the target must hold the new row verbatim with one trailing
  newline; on every refusal it must hold nothing.
- `checks/prose-figures.py`: new. Stale digests and counts in prose were raised as findings
  by both reviews, because the figures were hand-written and drifted. Every derived figure is
  now recomputed from its receipt and the check fails if the prose disagrees, so that class
  of defect cannot recur silently.
- `coverage.md`, `authorization-request.md`: the stale descriptions both reviews raised, now
  generated from the receipts rather than typed.
- `disposition.md`: dispositions for both reviews.
- `identity.json`, `manifest.sha256`, `candidate.json`, `authorization-template.txt`:
  regenerated for the current digests.
- `rehearsal/`: re-run end to end through the current wrapper as a two-caller race, rather
  than inherited. `rehearsal-red/` and `rehearsal-prev/` are retained and labelled; neither
  is the packet rehearsal.

## On review 01's M1, which was not silently fixed

The adopted resource decision states a derivation rule of 1.9 times the observed peak rounded
up to the next 256 MiB, which gives 3,328 MiB, while the adopted envelope is 3,072 MiB, or
1.89 times. The adopted number governs and the plan carries it. The controller's adopted
document was not edited to make its arithmetic match, because it is theirs; the reconciliation
is in `disposition.md` and `coverage.md`. A reviewer who thinks that disposition is wrong
should say so.

## Read contract and report

The read contract in `handoff.md` applies. Go straight to the diff and the block; re-deriving
the plan and its bindings would repeat review 01. Open no ledger, no `INDEX.md`, no memory
file, and no other reviewer's material. Execute nothing: no wrapper, no check script, no
phase. Read-only Git and independent CPython 3.14.6 stdlib calculations are allowed.

Write the report as the next free `reviews/review-NN-codex.md` with CLEAN or NOT CLEAN and
findings graded Critical / Important / Minor, each citing file and line with a concrete
reachable scenario. Save the sealed inventory as `checks/review-NN-inventory.md`. Reviewer
publication is not authorized; return the report for the drafter's disposition.
