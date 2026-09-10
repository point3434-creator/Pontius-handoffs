# Disposition: solve-run-20260910 (drafter and checkpoint finalizer: Claude)

Verdict of record: **NOT CLEAN**. Two Codex cold reviews (`reviews/review-01-codex.md`,
`reviews/review-02-codex.md`; coordination in `reviews/coordinator-note-codex.md`) agree on
four Important defects in `invoke.sh`; the concrete plan, its prerequisites, the source and
checkout identities, the envelope and the rehearsal census passed both reviews. The
controller had requested two reviews for this round; that count applies to this round only.

## Findings and rulings

| Finding | 01 | 02 | Ruling | Correction (packet `../solve-run-20260910-r002`) |
|---|---|---|---|---|
| One-shot reservation not atomic | I-01 | I-01 | Accepted, Important | `mkdir invocations/claim.d` is the exclusive claim, taken after the read-only preconditions and before any record or launch; it survives interruption; a second caller exits 97. Executed race check C9: two concurrent callers, one launch, one 97. |
| Rehearsal can reach the retained checkout; roots overridable | I-02 | I-03 | Accepted, Important | Retained mode refuses `SOLVE_ROOT`/`REHEARSAL_PK` (exit 88); rehearsal requires an explicit root that is not the retained checkout (86) and is a detached worktree (85); refusal checks C1, C3, C4, C5 executed. |
| Required record writes unchecked | I-03 | I-02 | Accepted, Important | `set -o pipefail`; every record write is checked; a failed claim/start record stops before launch (98); `noclobber` on captures; post-launch capture, hash or retained-file failures end in exit 99 EVIDENCE INCOMPLETE even when the child exited 0; checks C6, C7. |
| Old journal row attached after no new row | I-04 | I-04 | Accepted, Important | `journal_attribution.py` (digest pinned in the script) reports BOUND only when exactly one new row appeared, names the adopted commit and binds an existing result file by digest; ABSENT/EXTRA/MISMATCH are recorded and nothing is attached; six executed cases C8. |
| Manifest ordering vs handoff rule | I-05 | M-01 | Accepted, **Minor** (coordinator ruling stands; both grades retained in the reports) | r002 manifest is whole-row byte-sorted (`LC_ALL=C`) and its handoff states that rule; the r001 aggregate `a2833969…` stays as published, with the whole-row digest `d82f8671…` acknowledged. |
| Agreement memory forecast overstated | M-01 | M-02 | Accepted, Minor | Campaign note rewritten: one observation, worker Job peak distinguished from parent retention, growth in both bank size and H (retained host outcomes), no numeric exceedance claim. |

Root cause, in the drafter's words: the r001 wrapper was written for the ordinary path and
rehearsed only on it. Its "one-shot" and "every record kept" promises were prose, not
predicates: no exclusive claim, no checked writes, no attribution of the journal row, and a
rehearsal switch that weakened the retained gate instead of adding a separate one. The r002
wrapper turns each promise into a predicate with its own exit code and an executed
fault-path check (`checks/wrapper-checks.sh`, 14 cases, 0 failures), so the successful path
is no longer the only exercised path.

## Cold-input disclosure

Both reviewers reported CONTEXT_PROBE_NONE and sealed inventories before rehearsal evidence,
then encountered historical verdict labels in documents this handoff required them to read
(adoption, authorization and prerequisite records). They opened no prior reviews or
dispositions. Next packets should point reviewers at identity-only predecessor receipts
where a document's verdict language is not needed.

## Status

The r001 packet is closed as NOT CLEAN; its plan bytes (`c1a6af60…`) are unchanged in
r002. No retained invocation, authorization or source change occurred. The reviews' exact
bytes, inventories and dispatch receipts are committed with this disposition.
