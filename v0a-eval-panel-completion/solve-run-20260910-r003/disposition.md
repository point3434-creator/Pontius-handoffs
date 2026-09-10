# Disposition: solve-run-20260910-r003 (drafter and checkpoint finalizer: Claude)

Verdict of record: **NOT CLEAN**, 0 Critical, 0 Important, 3 Minor (Codex cold review 01,
`reviews/review-01-codex.md`, `743ab75a…`; coordination `reviews/coordinator-note-codex.md`;
inventory `276514b4…` sealed after step 3). The label is preserved without reinterpretation.
The reviewer's separate engineering assessment, operationally SOUND for the bound retained
solve under exclusive operator ownership with no material reachable launch-safety failure,
does not replace it. Probe `CONTEXT_PROBE_NONE`; one reviewer; no agent fan-out.

All three findings are accepted. I verified each from the frozen bytes before ruling.

- **M-01, the race check does not assert its advertised outcome.**
  `checks/wrapper-checks.sh:131` passes the caller-status pair only inside the condition
  label, so `assert` compares 0 with 0 and the launch count with 1, and never compares the
  observed pair with `one-winner-one-refusal`. A winner whose child failed, or any
  regression that kept one capture pathname, would still record a pass. This is my own
  defect and it is exactly the hole review 01 M-02 asked me to close in the runner; I
  generalised the runner but left this call site incomplete.
- **M-02, an explicitly empty `REHEARSAL` bypasses the 0/1 guard.** `invoke.sh:43` uses
  `${REHEARSAL:-0}`, which substitutes the default for an empty string as well as for an
  unset variable, so `REHEARSAL=""` reaches retained mode instead of exit 84. Narrow, since
  authorization, fixed roots and the claim all still apply, and an empty value with a root
  override is still refused; it is nonetheless an input-contract defect against the claim
  the packet makes.
- **M-03, the claim-consumption promise overreaches.** The prose in `invoke.sh:24`,
  `identity.json` and `authorization-request.md` says every failing path leaves the claim
  consumed. Precondition refusals occur before `claim.d` exists, so no claim is consumed
  and a corrected call may legitimately proceed. Only failures after a successful claim
  consume it.

The reviewer also noted that the carried campaign note still cites the r001 rehearsal's
19 seconds while this packet's receipt records 16; that figure is corrected too.

## Correction

`solve-run-20260910-r004` closes all three: the race case asserts the status pair as its
compared condition, `REHEARSAL` distinguishes unset from empty, and both the header and the
binding documents separate precondition refusal from a claimed attempt. A new check covers
the empty value. The exit precedence, the atomic claim, the fixed roots, the checked record
writes and the journal attribution are unchanged; the plan bytes are unchanged for the
fourth packet running.

Nothing here reopens the closed properties. Review 01 M-01 of r002 remains a disclosed
assumption: the helper trusts that the adopted tool is the sole journal producer in a
checkout only this wrapper drives, and the reviewer's residual-risk row records the operator
duties that no wrapper can discharge.

r003 is closed, not withdrawn. Its plan, identities and rehearsal stand, and the controller
may still authorize it as-is with these three Minors disclosed, since none of them touches
the launch-safety properties and the only behavioural one requires deliberately setting the
mode variable to an empty string.
