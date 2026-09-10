# Review request: retained solve plan, r002 — v0a-eval-panel-completion/solve-run-20260910-r002

One reciprocal cold review under `controller-review-policy-20260909`: Claude drafted,
Codex reviews. Round kind: FIX of `../solve-run-20260910` (two reviews NOT CLEAN: four
Important defects in the invocation wrapper; plan, identities, envelope and rehearsal
census passed). Packet date: 2026-09-10. Packet manifest SHA-256
`8acaaa389fc152e4127e98fe879df758fd819961085c717dd5c2601b9d145f1a`.

**Manifest rule (corrected).** `manifest.sha256` holds one row `<sha256>  <path>` per file
over raw bytes, the rows sorted as whole rows in byte order (`LC_ALL=C sort`), joined with
LF; the packet digest is the SHA-256 of that file. Outside it: this file, `candidate.json`
and the manifest itself. `authorization.md` and `invocations/` do not exist until the
controller authorizes and the run happens.

## What changed since solve-run-20260910

- `plans/solve.json` — byte-identical (`c1a6af60…`); the execution checkout, source,
  prerequisites and envelope are unchanged.
- `invoke.sh` — rewritten: fixed roots with overrides refused in retained mode; rehearsal
  requires an explicit, non-retained, detached root; an atomic exclusive claim
  (`mkdir invocations/claim.d`) after the read-only preconditions and before any record
  or launch; every record write checked (a failed pre-launch record stops without a
  launch; `noclobber` captures; post-launch write or attribution failure exits 99 even
  when the child exited 0); journal row attributed, never assumed.
- `journal_attribution.py` — new helper (digest pinned in the script): BOUND only for
  exactly one new row naming the adopted commit and binding an existing result file by
  digest; ABSENT / EXTRA / MISMATCH otherwise, attaching nothing.
- `checks/` — executed fault-path checks: `wrapper-checks.sh`, `wrapper-checks.jsonl` (14
  cases, 0 failures), per-case refusal captures, both callers' captures of the race.
- `rehearsal/` — a renewed rehearsal produced by the race winner in a fresh disposable
  snapshot (`receipt.json`); the later-phase `chain-receipt.json` carried unchanged.
- `campaign-note.md` — the agreement memory paragraph corrected (one observation; worker
  Job peak vs parent retention; growth with both bank size and H; no numeric forecast).
- `identity.json`, `authorization-request.md` — updated for the above.

## Identity to recompute

- Source: `git rev-parse 1c706744^{tree}` = `3d2fe79d…`; `git ls-remote origin
  refs/heads/codex/eval-panel-completion-adopted`.
- Plan bytes: SHA-256 of `plans/solve.json` and of
  `D:/Pontius-worktrees/eval-panel-solve-20260910/plans/solve.json`, both `c1a6af60…`.
- Prerequisite bytes: the three absolute paths inside the plan hash to the `PREREQUISITES`
  constants in `tools/v0a_eval_panel_completion.py` at the source commit.
- Helper pin: `ATTRIBUTE_SHA` in `invoke.sh` equals SHA-256 of `journal_attribution.py`.
- Manifest under the rule above; execution checkout HEAD and `status --short`.

## Read order and allowed inputs

1. This file, then `identity.json`.
2. `invoke.sh` and `journal_attribution.py`, read as frozen control flow. Do not run them
   against the retained checkout. The predicates and exit codes are listed in
   `identity.json`; each fault-path case in `checks/wrapper-checks.jsonl` names its
   expected and actual exit.
3. `plans/solve.json` against the frozen validator (`validate_plan` in
   `tools/v0a_eval_panel.py`, `validate` in `tools/v0a_eval_panel_completion.py`), if the
   reviewer wishes to re-establish admission; the prior reviews established it.
4. `checks/` (the checks script, its receipt and captures), then `rehearsal/receipt.json`
   and the raw captures, then `rehearsal/chain-receipt.json`.
5. `authorization-request.md`, then `campaign-note.md`.
6. Deferred inputs, after the reviewer's own inventory: `../solve-run-20260910/reviews/`
   (both reviews and the coordination note) and `../solve-run-20260910/disposition.md`.
7. Governing documents at the source commit: `docs/architecture/v0a-eval-panel-impl-r001/
   {brief,design}.md` (design section 1, 3 and step 7; brief acceptance 3 and 9), and
   `../prerequisite-run-20260909/resource-decision.md`. Where a required document carries
   historical verdict language, identity-only reading is enough for this review.

## What the review must establish

1. **Each prior Important is closed by a predicate, not by prose.** Reservation: is the
   claim exclusive and taken before any launch, and does a second caller fail without
   launching or writing captures? Rehearsal/roots: can any environment make retained mode
   run elsewhere, or rehearsal mode run against the retained checkout or without
   authorization on it? Records: is there any path where a launch happens without its
   start record, or where the wrapper exits 0 with a missing capture, digest or retained
   file list? Attribution: can an older journal row ever be attached, and are ABSENT,
   EXTRA and MISMATCH recorded rather than substituted?
2. **The executed checks test what they claim.** Do cases C1–C7 refuse before any launch
   (no `solve-stdout.json` under the case's packet), do C8's six synthetic journals cover
   the helper's outcomes, and does C9's race show exactly one launch and one exit 97 with
   the winner's records equal to `rehearsal/`?
3. **Rehearsal consistency.** Do `rehearsal/receipt.json`'s numbers follow from the log,
   captures and attributed row (exit 0, evidence complete, rows 59 to 60, census 1,081,
   zero ties, both action categories, teacher `c3ffab40…`)? Is anything from a rehearsal
   or a check presented as evidence?
4. **Residual risk the wrapper does not close.** Name any one-shot or evidence property
   still resting on operator behaviour (for example an abandoned claim, or a second
   authorization), so the controller sees it before authorizing.
5. **Manifest and campaign note.** Does the manifest reproduce under the stated rule? Is
   the memory paragraph now within what `chain-receipt.json` and the frozen code support?
6. **Forbidden claims.** Nothing proves teacher strength or host agreement; nothing
   authorizes export or agreement; the controller's envelope is used unchanged.

## Known deviations to weigh

- Lines over 100 columns in shell scripts, JSON and receipts where paths, digests, format
  strings or captured output require them; markdown and the helper are within 100.
- `rehearsal/solve-stdout.json` and `rehearsal/journal-attribution.txt` are raw CRLF
  captures of printed output; `receipt.json` records the raw and LF-normalized stdout
  digests. The evidence of record for a retained run is `result.json` in the checkout,
  bound by its attributed journal row.
- The rehearsal snapshot was removed; the rehearsal is inspectable only through captures.

## Report

Write `reviews/review-01-codex.md` in this packet with a verdict (CLEAN or NOT CLEAN) and
findings graded Critical / Important / Minor, each citing file and line or predicate.
Append one line to `D:/Pontius-handoffs/progress.md`
(`date | v0a-eval-panel-completion/solve-run-20260910-r002 | Codex reviewer | text`).
A material finding returns to the drafter for a further corrected packet; a CLEAN verdict
is followed by the controller's one-shot authorization in the wording
`authorization-request.md` suggests, then the invocation.

## Addendum for cold review 02 (controller ruling 2026-09-10)

The controller ruled: "well run a cold review first if it still clean we will publish";
Codex runs it. This review is a fresh-session cold pass on the same frozen bytes (manifest
`8acaaa38…`). In addition to the read order above:

- Do NOT open `reviews/`, `disposition.md`, `checks/review-01-inventory.md`,
  `checks/review-01-verification.json`, `../solve-run-20260910/reviews/`,
  `../solve-run-20260910/disposition.md`, or any ledger (`progress.md` at either level)
  before your own inventory is written and hashed. After the inventory, the deferred
  inputs remain only those named in step 6 above (the r001 reviews and disposition);
  the r002 follow-up review and its disposition stay closed for the whole pass.
- Read predecessor records (adoption, authorization, prerequisite packet) for identity
  only; their verdict language is not an input.
- Report to `reviews/review-02-codex.md`; inventory to `checks/review-02-inventory.md`;
  one ledger line in `D:/Pontius-handoffs/progress.md`
  (`date | v0a-eval-panel-completion/solve-run-20260910-r002 | Codex reviewer 02 | text`).
  State the coldness probe result and any exposure explicitly.
- If CLEAN, the controller authorizes the retained solve in the wording of
  `authorization-request.md`; if NOT CLEAN, the packet returns to the drafter.
