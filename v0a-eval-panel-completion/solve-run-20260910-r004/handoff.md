# Cold review request: retained solve plan r004

Packet: v0a-eval-panel-completion/solve-run-20260910-r004.

One cold review under `controller-review-policy-20260909` and the controller's ruling of
2026-09-10 ("well run a cold review first if it still clean we will publish"; Codex runs
it). Claude drafted. Round kind: FIX of `../solve-run-20260910-r003`, whose cold review
returned NOT CLEAN over three Minors while judging the bound invocation operationally
sound. Packet date: 2026-09-10.

**Manifest.** `manifest.sha256` holds one row `<sha256>  <path>` per file over raw bytes,
the rows sorted as whole rows in byte order (`LC_ALL=C sort`), joined with LF; the packet
digest is the SHA-256 of that file. Outside it: this file, `candidate.json` and the
manifest itself. `authorization.md` and `invocations/` do not exist until the controller
authorizes and the run happens.

## What changed since r003

Each change closes one finding of the r003 cold review; nothing else in the invocation
path was touched.

- **M-01, the race check did not assert its advertised outcome.**
  `checks/wrapper-checks.sh` now passes the caller-status pair as the compared value
  (`assert C9-race-status-pair one-winner-one-refusal "$RACE" launches 1 "$LAUNCHES"`), so a
  winner whose child failed, or a regression that kept one capture pathname, fails the
  suite. The receipt's status fields are quoted, since a case may now compare a pair rather
  than a numeric code. A new negative control (S0) opens the run: it feeds the gate a
  deliberate mismatch and asserts that it records a failing row, so the suite is known to
  depend on its comparisons rather than on reaching the end.
- **M-02, an explicitly empty `REHEARSAL` bypassed the guard.** `invoke.sh` uses
  `${REHEARSAL-0}`, so only an unset variable takes the default; any other set value,
  including an empty string, is refused with exit 84. New case C14 covers the empty value.
- **M-03, the claim-consumption promise overreached.** The header, `identity.json` and
  `authorization-request.md` now separate a precondition refusal, which happens before
  `claim.d` exists, consumes nothing and leaves the packet callable again once corrected,
  from a failure after a successful claim, which consumes it and is never retried.
- The carried campaign note's Phase 1 figures are this packet's rehearsal, not r001's.

`plans/solve.json`, `journal_attribution.py` and `rehearsal/chain-receipt.json` are
byte-identical to r003. The exit precedence, the atomic claim, the fixed roots, the checked
record writes and the journal attribution are unchanged.

The r002 review's M-01 remains a disclosed assumption: the helper trusts that the adopted
tool is the sole journal producer in a checkout only this wrapper drives. The r003 review's
residual-risk row records the operator duties no wrapper can discharge; they are restated
in `identity.json` and are not claimed to be closed.

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
4. `checks/` (the runner, `wrapper-checks.jsonl`, `gate-negative-control.jsonl`, the
   per-case captures, the mutant diff and identity), then `rehearsal/receipt.json` and its
   raw captures, then `rehearsal/chain-receipt.json`.
5. `authorization-request.md`, then `campaign-note.md`.
6. Deferred, only after your own inventory is written and hashed: the `reviews/` and
   disposition files of `../solve-run-20260910-r003`, `../solve-run-20260910-r002` and
   `../solve-run-20260910`.
7. Governing documents at the source commit: `docs/architecture/v0a-eval-panel-impl-r001/
   {brief,design}.md` (design sections 1 and 3, step 7; brief acceptance 3 and 9), and
   `../prerequisite-run-20260909/resource-decision.md`. Read predecessor records for
   identity only; their verdict language is not an input.

Do not open any ledger (`progress.md` at either level) at any point in this pass.

## What the review must establish

1. **Each of the three findings is closed by the artifact that carries it.** Does the race
   case now compare the pair, and would a failed winner fail the suite? Can any set
   `REHEARSAL` value other than 0 or 1 reach a launch? Do the header, identity and
   authorization request now describe claim consumption accurately for both scopes?
2. **The gate is real.** Does S0 demonstrate that a mismatch is recorded and counted, and
   does the runner's exit status depend on the accumulator?
3. **The previously closed properties still hold** after these edits: exit precedence,
   exclusive claim before any launch, fixed roots with overrides refused, checked record
   writes, and journal attribution that never substitutes an older row.
4. **The checks remain honest.** Does each case assert what its name claims? Is the C12
   mutant labeled, bound by diff and digest, and used only for the property the host
   filesystem cannot exercise directly? Does C13 still show the traced compound path?
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
- The suite does not exercise every filesystem failure, a zero-child-with-incomplete-
  evidence 99 case, or interrupted cleanup; the r003 review's coverage-limits paragraph
  still applies and is not claimed to be closed.

## Report

Write `reviews/review-01-codex.md` in this packet with a verdict (CLEAN or NOT CLEAN) and
findings graded Critical / Important / Minor, each citing file and line or predicate, and
state the coldness probe result and any exposure. Inventory to
`checks/review-01-inventory.md`. Append one line to `D:/Pontius-handoffs/progress.md`
(`date | v0a-eval-panel-completion/solve-run-20260910-r004 | Codex reviewer | text`).
If CLEAN, the controller authorizes the retained solve in the wording
`authorization-request.md` suggests; if NOT CLEAN, the packet returns to the drafter.
