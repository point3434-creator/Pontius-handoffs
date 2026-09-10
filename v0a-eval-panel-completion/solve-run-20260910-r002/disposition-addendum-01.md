# Disposition addendum 01 — cold review 02 (finalizer: Claude)

The controller ruled on 2026-09-10 that a cold review must precede authorization and that
publication follows only "if it still clean". Codex ran one fresh ephemeral session,
probe `CONTEXT_PROBE_NONE`, inventory sealed at `90180d2d…` before the check and rehearsal
inputs, with the r002 follow-up review and `disposition.md` closed throughout.

## The two labels, unreconciled and both preserved

- **Cold review 02 (`reviews/review-02-codex.md`, `66c9e55d…`): NOT CLEAN**, 0 Critical,
  0 Important, 1 Minor; engineering verdict SOUND for the bound retained solve; all four
  prior Important findings independently closed.
- **Follow-up review 01: CLEAN / SOUND**, same substance, the same issue graded M-03.

Neither label is rewritten. The difference is whether a known documentation discrepancy
blocks a CLEAN label; there is no disagreement about executable launch safety.

## The finding, verified by the finalizer from the frozen bytes

Cold M-01 is the accepted M-03. I read `invoke.sh` at its frozen digest `f311ea90…`:
line 140 is `[ "$rc" -eq 0 ] || exit "$rc"` and line 141 is the evidence test returning 99.
A nonzero child status therefore takes precedence, and 99 is reserved for a zero-status
child whose evidence is incomplete. The prose in `invoke.sh:15-18`,
`authorization-request.md:31`, `identity.json` and `handoff.md` states the 99 contract
without that precedence. Both paths exit nonzero, keep the claim consumed and record the
incomplete evidence, so no successful retained solve can be manufactured; the defect is
that an operator classifying outcomes by exit 99 alone could misread a failed child with
incomplete evidence. The reviewer's reachability trace (a `begin_run` failure before the
entry's try/finally, helper ABSENT, child status returned) is correct.

## Ruling

The controller's condition was not met on its face: the cold verdict reads NOT CLEAN.
Rather than authorize a one-shot retained run on a packet whose cold review carries that
label, or argue the label away, the finalizer corrects the discrepancy at its source.
`solve-run-20260910-r003` aligns the prose to the executable in all four files, and also
closes the two remaining wrapper-side Minors from review 01 (M-02 assert-and-fail check
runner with injected record failures; M-04 `REHEARSAL` value validation), each with its own
executed check. The exit policy itself is not changed: both branches already fail closed,
and changing precedence would be a behaviour change needing fresh validation for no gain.
Review 01's M-01 remains a stated assumption: the adopted tool is the sole journal producer
in a checkout only the wrapper drives.

r002 is closed. It is not withdrawn: its plan bytes, identities and rehearsal stand, and the
controller may still authorize it as-is with this Minor disclosed, since r003 changes no
executable behaviour except the new `REHEARSAL` guard.
