# Cold review: v0a-eval-panel-code/r004

Candidate ref: `refs/heads/review/v0a-eval-panel-code/r004`
Candidate commit: `0bc19bcaad5c6660468094772216cac2dc27a651`
Manifest SHA-256: `70ca4c76bc8bdefe8ffaab72fa8de5b7d24d49697157436d78a3e1c025a370c3`
Base commit: `f647a7989394f084875a040b20c41891168163ed` (adoption of the Slice A
implementation design; unchanged since r001)
Tree: `45c76c9c8f2d7fbfa4b00e4e5b8b8cffc538b4fc`
Tier: C — the first source checkpoint of Slice A, implementing design steps 1–3.
Round kind: FIX (corrects r003, NOT CLEAN / STRAINED under two Codex reviews).
Drafter and checkpoint finalizer: Claude. Codex reviews independently; Tier C
requires two independent cold passes.

**Authorization.** The implementation brief at BASE (lines 166–169) says a
later candidate review requires explicit controller reauthorization. This
packet is frozen and receipted; the review assignment waits on the controller.

The full commit and manifest bind identity; this path and the index only locate
it. The ref is on `origin`. Recompute parent, tree, scope and the blob-derived
manifest (whole-row byte sort, LF rows) from Git objects; read candidate blobs,
not working files. Changed bytes or scope require a new round. Do not run the
candidate's tool against the repository to learn its behavior — read its frozen
control flow; the receipts in `checks/` are the executed evidence for this round.

## Scope — the same seven paths; two blobs changed since r003

- `tools/v0a_eval_panel.py` (changed) — `sample_identity` and `declared_sample`
  bind every scheduled hand and control to a canonical card identity in its
  board's compatible universe, refuse duplicates, and require `declared-full`
  to equal the declared sample exactly; `supervise` takes a caller-owned report
  and runs each cleanup release as an independent bounded attempt recorded
  under `report["cleanup"]`, closing the job last; the parent refuses events
  for an already-complete record; `retain_boundaries` writes to a staging name,
  renames, binds, and only then drops the encoding; `full_pool_estimate`
  estimates only from the complete required membership.
- `tests/test_eval_panel_tool.py` (changed) — 16 cases: five new, two extended.
- `src/pontius/eval_bridge.py`, `tests/test_eval_bridge.py`, the two plan
  fixtures and `tests/cases.json` — byte-identical to r003 (same blob digests).

## FIX deferred input

`coverage.md`, SHA-256
`cc8dca8ea97959e93f31fee5ba92b97fd7ca1a5cfa95739534c83126c16edbc0`. Do not
open it until your initial invariant and related-path inventory are recorded.
It cites, for each corrected property, the frozen line that implements it and
the executed case that falsifies its absence — the r003 disposition's
root-cause note explains why.

The r003 reviews are in `../r003/reviews/`; the finalizer's disposition is
`inputs/prior-disposition.md`. On a FIX round you may read the disposition
after your independent inventory; you may not read another r004 reviewer's
output.

## Pinned inputs

- `inputs/workflow.md`, SHA-256
  `c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37`.
- `inputs/controller-rulings.md`, SHA-256
  `9652b870dfb214af764addb3de276c776d51015d7e55b75b98d0bb519711f3bc`;
  `inputs/controller-rulings-addendum.md`, SHA-256
  `d3a15c896463449913fa0852b51f654ac7688b6c6941b57652a745244e040a6c`;
  `inputs/controller-rulings-addendum-2.md`, SHA-256
  `0b708f7619c25167a51d55f8af00baa3cedc3e8a85e0a80511c18bd178e93dfa` (the
  3,000-line ceiling and the drafter's 1,200 / 600 working figure — now pinned).
- `inputs/dependencies.json`, SHA-256
  `ab0933726111415870200d4b14358012826da35fd2f083890cf7d8b0165f50b2` (34
  direct pins at BASE; not a transitive closure).
- `inputs/prior-disposition.md` (r003), SHA-256
  `0b642f5a3883a3a77081c46cb1cfaea5c9d0dff22dd6c5bf7d143770644bbd9b`;
  `inputs/r002-withdrawal.md`, SHA-256
  `1c50a633a7bcc65dc356a26a2b3751a7093d40a9047f02e8ee43237f5f67afbf`.
- The governing documents at BASE: `docs/architecture/v0a-eval-panel-impl-r001/
  {brief,design}.md` and the parent lane design.

## Receipts in `checks/`

| File | SHA-256 | What it is |
|---|---|---|
| `focused-snapshot-3.14.6.txt` | `80f0bb1d4632ae9bccb82b35e67955af40b744c78eb323f697194e168812114a` | both suites through `tests/test_pontius.py` in a disposable detached snapshot of the candidate with its own `uv sync --group dev` venv; `-B -P -W error::ResourceWarning`, `env -i` with `SystemRoot TEMP TMP PONTIUS_GIT PYTHONDONTWRITEBYTECODE`; **27 cases, 0 skipped, exit 0** |
| `focused-snapshot-receipt.txt` | `88f7bc346566f37429bf18851484be7aa1dc0710fb52b7f9d378738ca86b52aa` | snapshot commit, interpreter, invocation, environment |
| `focused-snapshot-journal-line.jsonl` | `682320ce51d74eb08f3bc0589ee2a1d5005842f40e4136268e977e50a3592331` | the harness's one journal row **inside the snapshot**; `source_verified: true`, `source_commit` = candidate |
| `line-budget-and-hygiene.md` | `98b6f10a2207587c640efb274454e91b087cd480c73957c1d1ea51bd862043bf` | 834 production / 556 test raw lines; 0 over-100-column lines, 0 CR, 0 trailing whitespace; the whole-slice projection against the ruling |

Digests are of the LF bytes as stored. The snapshot was removed after the
receipts were copied; no journal row was written in a live worktree.

## Review contract

Review the whole candidate, not the diff, against checklist v1 and design
steps 1–3. Then challenge each r003 correction against frozen source at BASE:

1. **Cleanup (r003 I-01).** Is every release attempted after any earlier
   attempt fails or is interrupted — including `job.close()` when `Popen`
   itself raised? Can any path leave `supervise` without returning, and if so,
   does `main` still record the drained observations? Does the injected-fault
   case observe process death independently of the injector? Is a cleanup that
   recorded a failure ever reported `cleanup_verified: true`?
2. **Sample identity (r003 I-02).** Can any plan with `coverage: declared-full`
   pass admission without exactly the declared board, the four declared hands
   and the royal control? Can a repeated, malformed, board-overlapping or
   string hand reach the worker under either coverage? Can the estimate be
   issued from fewer than four complete required records? Is the record name
   the worker emits the same canonical name the estimate looks up?
3. **Retention (r003 I-03).** Can a failed or interrupted write leave a
   completed artifact unbound, an encoding unrecoverable from the result, or a
   partial file that could be mistaken for a boundary artifact? Is the
   `finally` correct when `boundary_base64` is absent (retry after completion)?
4. **Residual rule.** I-01 and I-02 were each the first residual on their
   contract (r001 A and D). If either survives here, the workflow's separate
   candidate/root-cause rule applies; say so explicitly.
5. **Coverage.** Compare your inventory with `coverage.md` after opening it.
   The repeated-observation guard, a stream-close fault, and a real-worker
   `main` invocation are declared uncovered; missing coverage is not
   automatically a product defect.
6. **Budget.** 834 / 556 for this checkpoint; the slice projection is
   1,050–1,150 production lines against the pinned ruling. Assess as before.

No implementer transcript, prior-round review, or other reviewer's output is a
cold input. Record your own inventory before opening `checks/` or `coverage.md`.
No tests, owners, or candidate edits are requested; the receipts are the
executed evidence.

CLEAN requires that no material finding survive verification. Every Critical or
Important finding binds to this commit and manifest, cites exact frozen
locations, states a concrete failing scenario, and names the smallest correction
without implementing it. State one required design verdict — SOUND, STRAINED,
or WRONG SHAPE — with a short justification.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md`, one file per
reviewer, severity-ordered. Reviewer assignment is the controller's. A corrected
finding is a new record, never an overwrite.

## Coordinator notes

Branch `claude/v0a-eval-panel-code` remains at BASE; the worktree holds the
seven paths uncommitted and byte-identical to the candidate. Implementation
beyond steps 1–3, retained measurement, ceremonial commit, and integration
remain ungranted gates.
