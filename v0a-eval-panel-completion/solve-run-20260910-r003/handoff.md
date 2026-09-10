# Cold review request: retained solve plan r003

Packet: v0a-eval-panel-completion/solve-run-20260910-r003.

One cold review under `controller-review-policy-20260909` and the controller's ruling of
2026-09-10 ("well run a cold review first if it still clean we will publish"; Codex runs
it). Claude drafted. Round kind: FIX of `../solve-run-20260910-r002`, whose cold review
returned NOT CLEAN over a single Minor: the packet's prose promised exit 99 for all
incomplete evidence while the executable returns a nonzero child status first. Packet date:
2026-09-10.

**Manifest.** `manifest.sha256` holds one row `<sha256>  <path>` per file over raw bytes,
the rows sorted as whole rows in byte order (`LC_ALL=C sort`), joined with LF; the packet
digest is the SHA-256 of that file. Outside it: this file, `candidate.json` and the
manifest itself. `authorization.md` and `invocations/` do not exist until the controller
authorizes and the run happens.

## What changed since r002

- `invoke.sh` — the exit-status contract is stated in the header exactly as the code
  behaves: a nonzero child status is returned unchanged whether or not the evidence is
  complete, 99 is reserved for a zero-status child with incomplete evidence, otherwise 0.
  The failing branch now also prints `EVIDENCE INCOMPLETE` before returning the child's
  status, so an incomplete-evidence outcome is visible on both paths. `REHEARSAL` is
  restricted to exactly 0 or 1 (exit 84). The claim refusal message no longer asserts a
  cause it cannot distinguish. No other behaviour changed.
- `checks/wrapper-checks.sh` — rewritten to assert each case's exit code and a stated
  condition, and to exit nonzero if any case fails; 18 cases, up from 14.
- `identity.json`, `authorization-request.md` — the exit contract and the check summary.
- `plans/solve.json`, `journal_attribution.py`, `campaign-note.md`,
  `rehearsal/chain-receipt.json` — byte-identical to r002.
- `rehearsal/` — renewed on the corrected script in a fresh disposable snapshot.

These close cold review 02 M-01 (equally review 01 M-03), review 01 M-02 and review 01
M-04. Review 01 M-01 remains a disclosed assumption: the helper trusts that the adopted
tool is the sole journal producer in a checkout only this wrapper drives.

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
   against the retained checkout.
3. `plans/solve.json` against the frozen validator (`validate_plan` in
   `tools/v0a_eval_panel.py`, `validate` in `tools/v0a_eval_panel_completion.py`).
4. `checks/` (the runner, `wrapper-checks.jsonl`, the per-case captures, the mutant diff
   and identity), then `rehearsal/receipt.json` and its raw captures, then
   `rehearsal/chain-receipt.json`.
5. `authorization-request.md`, then `campaign-note.md`.
6. Deferred, only after your own inventory is written and hashed:
   `../solve-run-20260910-r002/reviews/` and its `disposition.md` and
   `disposition-addendum-01.md`, and `../solve-run-20260910/reviews/` and `disposition.md`.
7. Governing documents at the source commit: `docs/architecture/v0a-eval-panel-impl-r001/
   {brief,design}.md` (design sections 1 and 3, step 7; brief acceptance 3 and 9), and
   `../prerequisite-run-20260909/resource-decision.md`. Read predecessor records for
   identity only; their verdict language is not an input.

Do not open any ledger (`progress.md` at either level) at any point in this pass.

## What the review must establish

1. **The exit contract is now exactly what the code does.** Compare the header, the
   `identity.json` exit-status list and `authorization-request.md` against lines 140-142.
   Is there any remaining path where prose and behaviour differ, or where success is
   reported with incomplete evidence?
2. **The `REHEARSAL` guard is complete.** Can any value other than 0 or 1 reach a launch,
   and does the guard run before the mode branch uses the value?
3. **The four earlier Important properties still hold** after these edits: exclusive claim
   before any launch, fixed roots with overrides refused, checked record writes, and
   journal attribution that never substitutes an older row.
4. **The checks are honest evidence.** Does the runner actually fail the suite when a case
   fails? Does each case assert what its name claims? Is the C12 mutant labeled, bound by
   diff and digest, and used only for the one property the host filesystem cannot exercise
   directly? Does C13 demonstrate the traced compound path rather than a rehearsed one?
5. **Rehearsal consistency.** Do `rehearsal/receipt.json`'s numbers follow from its log,
   captures and attributed row? Is anything from a rehearsal or a check presented as
   evidence?
6. **Residual risk.** Name any one-shot or evidence property still resting on operator
   behaviour, so the controller sees it before authorizing.
7. **Forbidden claims.** Nothing proves teacher strength or host agreement; nothing
   authorizes export or agreement; the controller's envelope is used unchanged.

## Known deviations to weigh

- Lines over 100 columns in shell scripts, JSON and receipts where paths, digests, format
  strings or captured output require them; markdown and the helper are within 100.
- `rehearsal/solve-stdout.json` and `rehearsal/journal-attribution.txt` are raw CRLF
  captures; `receipt.json` records the raw and LF-normalized stdout digests. The evidence
  of record for a retained run is `result.json` in the checkout, bound by its attributed
  journal row.
- Case C12 runs a labeled one-line mutant, not the frozen script; C13 uses a second
  snapshot whose venv was deliberately broken. Both snapshots were removed after their
  records were copied, so the rehearsal is inspectable only through its captures.

## Report

Write `reviews/review-01-codex.md` in this packet with a verdict (CLEAN or NOT CLEAN) and
findings graded Critical / Important / Minor, each citing file and line or predicate, and
state the coldness probe result and any exposure. Inventory to
`checks/review-01-inventory.md`. Append one line to `D:/Pontius-handoffs/progress.md`
(`date | v0a-eval-panel-completion/solve-run-20260910-r003 | Codex reviewer | text`).
If CLEAN, the controller authorizes the retained solve in the wording
`authorization-request.md` suggests; if NOT CLEAN, the packet returns to the drafter.
