# Author coverage and limitations (deferred review input)

New phase packet. No project source changed. The wrapper derives from the export wrapper with
two deliberate changes, each answering a finding the export round recorded, and the plan binds
the retained export's outputs rather than any rehearsal copy.

**Bind the completed retained export.** The plan's three inputs are the retained export run's
`teacher.json`, `blueprint.json` and `result.json`, by absolute path and SHA-256. The frozen
`teacher_input` was executed against them during preparation and accepted: producer phase
`export`, status completed, `phase_complete` and `cleanup_verified` true, coverage, pool count
and prerequisite dict equality, permutation digest re-derivation, and both produced artifacts
bound with `retention == "complete"`. *Falsifier: a wrong digest, phase, coverage, artifact
binding or hand order.*

**Check inputs before spending the claim.** `verify_plan_inputs.py` verifies every member of
the plan's `inputs` object before the claim is taken, exit 80. Ten executed helper cases plus
two wrapper-level slice cases. *Falsifier: a missing, relative, malformed or changed input
passing the guard.*

**Check the launch environment before spending the claim.** `SystemRoot` or `SYSTEMROOT`,
`TEMP` and `TMP` are checked at the top of the wrapper, exit 79, because the launch line
expands them under `set -u`. Three executed cases. *Falsifier: a missing variable reaching
the claim.*

**Preserve the mode boundary.** Nine mode values, two empty-override refusals, missing
authorization, and both rehearsal-root separations. *Falsifier: any invalid set mode or any
retained override passing.*

**Claim at most once, on both refusal paths.** Two concurrent callers of the frozen wrapper
were raced more than once, and the two receipts cover different windows. In the RED rehearsal
both callers passed the read-only preconditions in the same second and the loser lost at the
atomic `mkdir` with "File exists": that is the concurrent-acquisition window itself, which the
export round recorded as having no receipt. In the green rehearsals the loser stopped earlier,
at the pre-claim existence check. Each race produced exactly one launch and one new journal
row. *Falsifier: another status pair, two launches, or more than one new journal row.*

**Attribution binds exact new bytes.** Twelve executed helper cases asserting exit code,
label and the copied row bytes, including the four refusal families the export round's cold
review named as unexercised: an unparsable row, an absent or non-string `output`, a missing
output file, and a `runtimes_sha256` disagreeing with the sibling file. On success the target
must hold the new row verbatim with one trailing newline; on every refusal it must hold
nothing. *Falsifier: a missing, extra or mismatching row attaching, or copied bytes
differing.*

**The retained-file inventory is complete or the evidence is not.** The enumeration's status
is checked before its output is used, and 12 executed controls cover the normal walk into a
subdirectory, an absent run directory, a failed, partial or empty enumeration, and a failed loop
redirection. *Falsifier: a run recorded
as complete evidence with a missing or partial inventory.*

**Child and evidence precedence.** Eight executed combinations of child status and evidence
state against the exact frozen tail. *Falsifier: a wrong exit or a missing
incomplete-evidence message.*

**Full-pool agreement completes.** Every full-pool rehearsal, including those driven by the
frozen wrapper, produced the same phase outcome: 1,081 primary hits, no disagreement, no
exclusion, a complete witness census, and the three controls as designed. *Falsifier: any
non-hit primary, an incomplete census, or a control classifying wrongly.*

**Resource.** The envelope comes from the controller's adopted per-phase decision of
2026-09-10, itself derived from a full-scale rehearsal. *Falsifier: a budget kill or a peak
above the declared limit.*

## Limits, stated plainly

The full pool has no off-pool complement, so `validate_membership` produced no `unsupported`
rows in the export and the default path is exercised here only by the single synthetic
off-pool control. Zero unsupported is a property of an empty complement, not a passed control.

No genuine host disagreement has ever been observed, because teacher and host agree by
construction. The classifier's disagreement path is exercised by relabelling a real capture's
selection reason, which is reasonable coverage but is not the same as having seen one.

Retaining all 98,304 witness draws dominates memory and result size. The bank and the
deterministic dealer already reproduce witness selection, so the retention is redundant. It
is recorded as a carried finding for the Slice B interface and deliberately not changed here,
because changing it means changing adopted source and reopening its review.

The parent process is outside the worker Job limit and its live peak remains unmeasured for
every phase of this campaign. A reconstruction of its dominant term for a run of this shape
gave about 286 MiB over a 16 MiB baseline. An attempt to sample it live failed and its number
is void; `measured-report.md` records why.

The wrapper checks execute refusals and exact source slices with local fixtures. They do not
prove every filesystem error, interrupted cleanup, or a race with an unrelated journal writer.

The adopted resource decision states a derivation rule of 1.9 times the observed peak rounded
up to the next 256 MiB, which would give 3,328 MiB from the observed 1,625.1 MiB, while the
envelope the controller adopted and this plan carries is 3,072 MiB, or 1.89 times the peak.
The adopted number governs; the discrepancy is in the rule's stated multiplier, and
`disposition.md` records the reconciliation. Neither the adoption nor any observed run is
affected.

The wrapper-level suite ran while the rehearsal's winner was still executing, which is
disclosed in the rehearsal receipt; the suite launches nothing and touches no checkout.

Nothing here establishes teacher strength, equilibrium quality or transfer to other boards or
budgets. Agreement establishes that the exported artifact reproduces the teacher's action
through the unchanged host for this pool, on this board, at this stack depth.
