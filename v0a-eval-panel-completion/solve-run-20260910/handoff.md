# Review request: retained solve plan — v0a-eval-panel-completion/solve-run-20260910

One reciprocal cold review under `controller-review-policy-20260909`: Claude drafted,
Codex reviews. Round kind: NEW-SURFACE (the first retained-run plan of the completion
campaign; it changes no source). Packet date: 2026-09-10. Packet manifest SHA-256
`a283396997e87cde60ffe00ae5c1e5413fe27a77eca559a360a20570ffe5abfe` over the twelve files
listed in `manifest.sha256` (this file, `candidate.json` and the manifest itself are
outside it; `authorization.md` and `invocations/` do not exist until the controller
authorizes and the run happens).

## What is under review

A bound execution plan and a one-shot invocation script for **one retained full-pool T1
solve** on the adopted source, plus the rehearsal records and a campaign note that
sequences the two later phases. There is no source candidate and no review ref: the
source is the adopted commit `1c7067448106cfa2aca3d57be879842d72293c61` (tree
`3d2fe79d2af20125e322dd4a668335e789810863`, branch `codex/eval-panel-completion-adopted`,
controller: "I approve all."). The plan is `plans/solve.json`, SHA-256
`c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982`, and the same bytes
sit at `D:/Pontius-worktrees/eval-panel-solve-20260910/plans/solve.json`, the checkout the
invocation will use. Adoption granted no invocation; this review precedes the controller's
one-shot authorization (design step 7; brief acceptance 3).

## Identity to recompute

- Source: `git rev-parse 1c706744^{tree}`; `git ls-remote origin
  refs/heads/codex/eval-panel-completion-adopted`; the r003 adoption receipt.
- Plan bytes: SHA-256 of `plans/solve.json` and of the checkout copy; both equal the digest
  above. The plan's `pool_seed`, `prefix`, `hand_universe_sha256` and permutation equal the
  retained capacity run's plan and result (`prerequisite-run-20260909`, run `a89932e7`).
- Prerequisite bytes: the three absolute paths inside the plan hash to the three
  `PREREQUISITES` constants in `tools/v0a_eval_panel_completion.py` at the source commit
  (`git cat-file blob 1c706744:tools/v0a_eval_panel_completion.py`); the two run results
  are bound by the journal rows at `642858d` on `claude/eval-panel-prerequisite`.
- Manifest: whole-row byte sort (`LC_ALL=C`), LF rows, raw file bytes.
- Execution checkout: `git -C D:/Pontius-worktrees/eval-panel-solve-20260910 rev-parse
  HEAD` and `status --short` (only the untracked `plans/` directory); `.venv` is CPython
  3.14.6 from `uv sync --locked --offline --group dev`.

## Read order and allowed inputs

1. This file, then `identity.json`.
2. `plans/solve.json`, read against the frozen validator: `validate_plan` in
   `tools/v0a_eval_panel.py` and `validate` in `tools/v0a_eval_panel_completion.py` at the
   source commit. Read the frozen control flow; do not run the tool against the repository
   to learn its behaviour. The receipts in `rehearsal/` are the executed record.
3. `invoke.sh`.
4. `rehearsal/receipt.json`, then the raw captures and `invocation-log.jsonl`, then
   `rehearsal/chain-receipt.json`.
5. `authorization-request.md`, then `campaign-note.md`.
6. Governing documents at the source commit: `docs/architecture/v0a-eval-panel-impl-r001/
   {brief,design}.md` (design sections 1, 3 and step 7; brief acceptance 3), the resource
   decision `../prerequisite-run-20260909/resource-decision.md`, and that packet's
   `identity.json` and `measured-report.md`.

## What the review must establish

1. **Admission.** From the frozen predicates, not from the rehearsal: does the plan
   satisfy every check for a declared-full solve — exact key set, runtime, board, stacks,
   prefix, universe digest and count, `pool_seed` with the full permutation, resource
   exactly 600 s / 2048 MiB, `pool_count` 1,081, prerequisites with absolute paths and the
   constant digests, the capacity result's permutation digest equal to the re-derived
   order, preflight `sample_complete`, empty `inputs`?
2. **Binding.** Do the bound prerequisite bytes carry the identities the journal rows and
   the resource decision record? Is the execution checkout what `identity.json` states?
3. **One-shot semantics.** Are `invoke.sh`'s preconditions minimal predicates (review
   checklist item 8) and sufficient: authorization present and log empty, HEAD, plan
   digest, prerequisite digests, interpreter, no untracked run directory, clean source
   scope? Does any failure keep every record and stop? Is there any path by which the
   invocation could run twice, retry, or write outside the checkout and this packet?
4. **Rehearsal consistency.** Do `receipt.json`'s numbers follow from the raw captures and
   the log (digests, exit 0, wall, census 1,081, zero ties, both action categories,
   teacher digest, `cleanup_verified`, `source_verified`)? Is anything from the rehearsal
   presented as evidence anywhere in the packet?
5. **Campaign note.** Is the phase sequencing consistent with the frozen tool (input
   binding, coverage rules, `teacher_input`) and design step 7? Are the two agreement
   findings (bank sizing arithmetic; memory and result growth with the bank) stated
   correctly from `chain-receipt.json` and the frozen `witnesses`/`agreement` code?
6. **Forbidden claims.** Nothing here proves teacher strength or host agreement, and
   nothing authorizes the export or agreement phases; the controller's envelope is used
   unchanged.

## Known deviations to weigh

- Lines longer than 100 columns occur in `invoke.sh` (shell format strings and the
  precondition pipelines), `identity.json`, `plans/solve.json` and the receipts, where
  absolute paths, digests or commands require them. Markdown files are within 100.
- `rehearsal/solve-stdout.json` is the raw CRLF capture of the tool's printed report; its
  raw and LF-normalized digests are both in `receipt.json`. The evidence of record for a
  retained run is `result.json` in the checkout, bound by its journal row.
- The snapshot used for the rehearsal was removed after the records were copied; the
  rehearsal cannot be re-inspected on disk, only through its captures.

## Report

Write `reviews/review-01-codex.md` in this packet with a verdict (CLEAN or NOT CLEAN) and
findings graded Critical / Important / Minor, each citing the file and line or predicate.
Append one line to `D:/Pontius-handoffs/progress.md` in the ledger format
(`date | v0a-eval-panel-completion/solve-run-20260910 | Codex reviewer | text`). A material
finding on the plan or the script returns to the drafter for a corrected packet with new
plan bytes, a repeated rehearsal and a new manifest; the corrected packet returns to the
same reviewer under the ordinary scope and residual rules. A CLEAN verdict is followed by
the controller's one-shot authorization in the wording `authorization-request.md`
suggests, then the invocation.
