# Disposition: agreement-run-20260910-r001 (drafter and finalizer: Claude)

Verdict of record: **NOT CLEAN**, 1 Important and 3 Minor, from one opposing Codex review.
The label is preserved as issued. All four findings are accepted. The Important one is
corrected here; the three Minors are dispositioned without a further round, which is what the
controller's proportionality rule prescribes: a further round follows a material unresolved
finding or changed executable behaviour, not a documentation advisory.

The reviewer's independent verification was substantial and I record it rather than restate
my own claims: all 42 manifest members, six input and prerequisite bindings and 892
source-scope files verified; all 98,304 candidate draws and the first selected witness for
each of the 1,081 hands reconciled; three rehearsal reports reconciled across 1,084 sessions,
22,225 frames and 4,336 decisions; 545 raises and 536 checks matched with all three controls
behaving as specified.

## I1, Important: a failed enumeration could be recorded as complete evidence

**Accepted, corrected, and reproduced as an executed fault.** The reviewer raised it as a
static control-flow finding. Before correcting it I reproduced it: shadowing `find` so the
enumeration fails after emitting nothing, the old block left `EVIDENCE=complete` with a
zero-line inventory. So the defect was real and demonstrable, not merely traceable.

The cause is that a process substitution's failure status is not collected, even under
`pipefail`, because the pipeline runs inside `<(...)` rather than in the shell whose status
the outer `||` tests. An enumeration that returned nothing, or part of the tree and then
failed, would leave the subshell exiting zero. Anything it did return would be hashed
successfully, so the wrapper could exit zero after a successful child while its inventory was
empty or partial. That is precisely the property this design exists to prevent, and it is
worth noting that the previous version failed loudly on the same input class: the fix for the
`host-inputs/` defect traded a noisy failure for a silent one.

The correction is the smallest one the reviewer named. The enumeration is captured by command
substitution, whose status does propagate and which `pipefail` covers for both `find` and
`sort`; its status is checked before any output is used; and an empty enumeration for a new
run directory is refused rather than accepted as an empty inventory. A filename containing a
newline would split, and that case also fails closed, because the fragment will not hash.

Three focused controls now run in `checks/wrapper-checks.py`, each shadowing `find` against
the exact frozen slice: enumeration fails outright, enumeration returns part of the tree and
then fails, and enumeration returns no names. All three must record incomplete evidence and
must leave no partial inventory. The normal case still walks the subdirectory.

The wrapper changed, so the end-to-end rehearsal was run again against the corrected bytes
rather than inherited. That is the same discipline that found the `host-inputs/` defect in
the first place.

## M1, Minor: the stated derivation rule does not yield the adopted number

**Accepted; the adopted envelope governs and is unchanged.** The rule as written says 1.9
times the observed peak rounded up to the next 256 MiB, which gives 3,328 MiB from the
observed 1,625.1 MiB. The adopted envelope is 3,072 MiB, which is 1.89 times the peak. The
rule was written after the number and I mis-stated the multiplier; the defect is in my
explanation, not in the envelope, and neither the adoption nor any observed run is affected.

I have not edited `resource-decision-20260910.md`, because it is the controller's adopted
artifact and its copy at `inputs/resource-decision-20260910.md` is a manifest member. The
reconciliation is recorded here and in `coverage.md`. If the controller wants the rule's
wording to match its own arithmetic, "at least 1.8 times the observed peak, rounded up to the
next 256 MiB" yields exactly 3,072 MiB, and 2,400 seconds already satisfies the time rule.
That is a one-line amendment for a later decision, not something to change under the
controller's name here.

## M2, Minor: stale descriptions

**Accepted and corrected.** `authorization-request.md` carried the pre-fix wrapper digest,
an out-of-date check count, and attributed atomic contention to the final green rehearsal.
The contention happened in the RED rehearsal, where both callers passed the read-only
preconditions in the same second and the loser lost at the `mkdir`; the green rehearsal's
loser stopped at the pre-claim existence check. Both receipts are retained and now say so.

## M3, Minor: overstated coverage

**Accepted and closed by strengthening the test rather than weakening the claim.**
`coverage.md` claimed the attribution cases assert the copied row bytes; they asserted exit
code, label and file existence. The helper cases now compare the copied bytes: on success the
target must contain the new row verbatim with one trailing newline, and on every refusal it
must contain nothing. The claim is now true because the test does what it said.

## Coldness, as the reviewer disclosed it

The reviewer received no candidate findings or verdicts and sealed its inventory before
opening deferred evidence, but the harness injected general repository-history summaries, so
its report says candidate-blind rather than wholly history-free. It opened no memory files,
ledgers, conversations or other reviewers' material. That disclosure is accurate and is
preserved; whether it satisfies the cold condition is the controller's call, and this packet
does not claim more than the reviewer claimed.

## Status

All four findings are closed or dispositioned. The wrapper, the two check suites and the
affected prose changed; the plan, its bindings, the envelope and the retained export inputs
did not. The packet is re-frozen with a new manifest, and the approval template is regenerated
to name it. No invocation, authorization, commit or push has occurred.

---

# Review 02 (focused correction review): NOT CLEAN, 1 Important, 1 Minor

Verdict preserved as issued. Both findings accepted. The reviewer stayed inside
`review-scope.md`: the plan, the witness census and the host agreement were not re-reviewed,
and it confirmed that the controls would detect reversion of the two corrections it was
asked to check.

## R2-I1, Important: the loop's input redirection failure was unchecked

**Accepted and corrected.** The loop ended `done <<< "$listing"`. If the here-string's input
descriptor or backing storage could not be created, the loop could fail before processing any
file, and because a while loop that executed no body command returns zero, the later
`seen > 0` check would mask it and the block would report a complete inventory it never
wrote. That is the same class as review 01's I1: a silent failure producing complete
evidence.

I verified the mechanism rather than accepting it. Using the same construct with a
redirection that does fail on this build, a missing file, the unguarded block returns zero
and the failure is masked; with `|| exit 1` appended the block returns one. Both are now
permanent controls, the second existing purely to show the guard is load-bearing.

I could not induce a here-string backing-storage failure on this build, bash 5.3.15 on
cygwin, including with `TMPDIR` pointed at a non-existent directory. Review 02 likewise did
not establish that build's behaviour. So the specific trigger remains unreproduced while the
general mechanism is demonstrated and guarded. That is stated here rather than glossed.

The correction is the one the reviewer proposed, unchanged and local: `done <<< "$listing" ||
exit 1`. No broader rewrite.

## R2-M1, Minor: stale identities and counts, again

**Accepted, corrected, and the recurrence closed at its cause.** The authorization request
named an older wrapper digest and out-of-date case counts, and the scope and coverage
miscounted the inventory fixtures.

This is the second review in a row to raise stale prose figures, which makes the cause the
process rather than the instance: the figures were written by hand and drifted whenever the
wrapper or the suites changed. Every derived figure is now generated from its receipt, and
`checks/prose-figures.py` recomputes each one and fails if the prose disagrees. It caught
five stale figures on its first run, including two the review had not named. It is part of
the suite from here on, so the class cannot recur silently.

## Whether this warrants another round

The controller's rule is that a further round follows a material unresolved finding or
changed executable behaviour. Executable behaviour did change, by one operator. My
recommendation, which is the controller's to accept or reject, is that this be the last
correction round on this block.

The reasoning: the finding just closed required an external resource failure that neither the
reviewer nor I could induce on this build; the block now carries 12 controls including one
whose only job is to prove another control is load-bearing; and the last two rounds have
moved from a defect that would silently corrupt evidence, through one requiring a storage
failure, to prose counts. That is a converging sequence, and the remaining risk in this block
is now smaller than the risk of continuing to change it. The consolidation the controller has
already agreed, one tested runner with explicit state transitions, is the right place for
further work on this logic, not another patch to the shell.
