# Cold review 02 — Claude — v0a-eval-panel-sample/r001

Verdict: **CLEAN**. Design verdict: **SOUND**.
No Critical or Important finding survives frozen-source verification. One advisory.
Specification: PASS on the admitted-sample contract. Engineering quality: PASS.

Reviewer: Claude, independent cold pass 02, 2026-09-09.
Candidate: `72954e1331c9b191d927c1c4b82f277bcd322a4c`
Manifest SHA-256: `d79035495a278fa8ee3fb1a6adc6fc1838938900ab7c19bbdd434264faf63510`
Base / sole parent: `182d14e213c6f0b7d7578e429f81d051a9e59707` (ownership/r001)
Tree: `73797f3b554f68c3ced59cc295b0e41f1507b8bb`
Ref: `refs/heads/review/v0a-eval-panel-sample/r001` (local; not on origin at review time)
All locations are frozen blob line numbers at the candidate commit.

## Disclosure

Before this review began, a session-start status check listed the handoffs tree and
tailed `progress.md` (three lines), which exposed the ledger lines for ownership/r001,
sample/r001 and ownership/r002 including the sibling Codex verdicts. No review file,
disposition, coverage or check content was opened before the inventory below was
recorded and hashed. The controller decides whether the pass still counts as cold; the
inventory and every finding here were derived from the frozen blobs, and the verdict
did not change after the deferred inputs were opened.

The reviewer is the author of the rejected r004 and of its disposition's root-cause
note; the candidate implements the shape that note endorsed. That is disclosed as a
possible bias toward acceptance. The counter-measure was an adversarial re-read of the
combined source after the inventory, listed under "Adversarial checks".

## Contract under review and its residual status

The admitted-sample contract: r001 D → r003 I-02 → r004 C (second residual). Under the
workflow's "count residuals" rule this candidate is the contract's own separate
candidate. The root-cause note it answers is `inputs/prior-disposition.md`.

## Independent inventory (recorded and hashed before deferred inputs)

Scratchpad file `eval-panel-sample-ownership-inventory-claude.md`, SHA-256
`52b87992a333ae0b5278ba7c0b82c4baed5c5ad5881333f520a4a966ecf9bc92`, recorded
2026-09-09T14:40:12Z; copied to `checks/review-02-inventory.md`.

Invariants stated before reading coverage:
- S1. One admitted, role-bearing, canonical schedule; the worker executes it and the
  estimator reads it; nothing rebuilds it from the raw plan lists.
- S2. `declared-full` admits exactly {development×4 on 2c 7d 9h Js Qc, control×1 royal
  2c 3d} by (role, board, hand); role movement, substitution, duplicates, board change,
  malformed or board-overlapping hands are refused.
- S3. A completed declared-full run has exactly the four development records complete
  and agreeing, named as the estimator expects; otherwise no estimate and no "completed".

## Verification against frozen source (`tools/v0a_eval_panel.py` @ 72954e13)

- S1 holds. `validate_plan` returns `AdmittedPlan(wire, schedule)` and returns an
  `AdmittedPlan` unchanged on re-entry; `run_plan` iterates `admitted.schedule`
  (`for label, unit_board, hero in admitted.schedule`); the parent sends
  `admitted.document` and the worker re-admits the same wire, so both sides derive the
  schedule by the same deterministic function; `complete_sample` keys records by
  `ScheduledHand.record_key` and `full_pool_estimate` consumes `complete_sample`.
  No consumer reads `development_hands`/`controls` after admission.
- S2 holds. Distinctness on `(board, hand)` over the role-bearing tuple, then
  `plan["board"] == DEVELOPMENT_BOARD and set(sample) == set(expected)` where `expected`
  carries roles. Moving one or all development hands into `controls` changes the role
  and fails set equality; all-controls with a rebound main board fails the board test;
  the r004 negatives (duplicate, substituted, malformed, overlap, string hand, wrong
  control) are inherited unchanged.
- S3 holds. `complete_sample` returns `None` on any record outside the schedule, any
  duplicate key, `complete is not True`, a stage set different from `STAGES`, or a
  non-`True` comparison; it requires the key set to equal the schedule. `supervise`
  sets `sample_complete` for preflight and demotes `completed` to `failed` when it is
  false; `full_pool_estimate` refuses without a complete sample and sums only
  development-role costs. Record naming: the hero is the sorted card tuple on both
  sides, so worker names and estimator keys agree (`AdAs`, `KdKh`, `8dTd`, `3c4d`).

Tests (`tests/test_eval_panel_tool.py` @ 72954e13): role movement ×2 and the
all-controls rebound board refused; the r004 admission negatives retained; the
estimator fixture now carries roles and challenges an omitted control, a failed
comparison, test-subset and capacity; `RealRunOwnershipTests.test_declared_full_real_
worker_and_estimator_use_the_same_roles` runs the real five-hand worker through `main`
in a disposable shared clone and asserts the four literal development identities, the
royal control and a four-hand estimate from the retained result. This is the
end-to-end case the r004 disposition said would have exposed both earlier misses.

## Adversarial checks (after the inventory; none produced a finding)

- A plan whose `development_hands` is an empty list under `declared-full` → set
  inequality → refused. Under `test-subset` with no controls → admitted, schedule empty,
  worker emits nothing, `complete_sample` returns `{}` (equal to the empty required set)
  → `sample_complete` true, status completed with zero observations. This is a
  degenerate but honest result: coverage is labeled `test-subset`, no estimate is
  produced (`not_estimated`). Not a defect; noted for the controller.
- `AdmittedPlan.document` re-parses the wire on every access; the parent calls it once
  per send and once in `main`; cost negligible.
- A worker that somehow emitted a record outside the schedule would make
  `complete_sample` return `None` → failed. Correct direction.

## Advisory (not material)

- A-01. Type errors in the sample (e.g. an integer where a board list is expected)
  surface as `TypeError` rather than the tool's `ValueError` refusal. `main` records a
  failed run either way before any worker exists. Pre-existing since r001; cosmetic.

## Comparison with deferred coverage (opened after the inventory)

`coverage.md` (SHA-256 `9b481d76…`, matches the handoff) states four invariants that
correspond to S1–S3 plus the end-to-end literal-identity case. The category matches my
inventory; the executed cases it lists are the ones in the frozen test blob. Its
statement that the packet does not claim the combined source ready for adoption is
correct and is respected here: this pass covers the sample contract; the combined
source is reviewed in ownership/r002.

## Identity, receipts, budget

Read-only Git: ref → commit, sole parent 182d14e2, tree 73797f3b; exactly two changed
paths; manifest recomputed from raw blobs with whole-row `LC_ALL=C` sort and LF rows
is byte-identical to `manifest.sha256`; its digest equals the handoff value. All 34
`dependencies.json` pins reproduce at the stated base f647a798 (the file states its own
base; it is a direct inventory, not a closure). All 17 pinned inputs/receipts and
`coverage.md` match their handoff digests. `src/`, `tests/test_eval_bridge.py`, the
fixtures and `cases.json` are unchanged since 0bc19bca; the numerical bridge was not
re-reviewed and retains its three prior static confirmations.

Receipts (supplied, identity-checked, not re-run): GREEN 33 cases, 0 skipped, exit 0 on
this candidate under CPython 3.14.6, `-B -P -W error::ResourceWarning`, `env -i` with
`SystemRoot TEMP TMP PONTIUS_GIT PYTHONDONTWRITEBYTECODE`, `source_verified: true`;
RED beb06945 (tests only on the rejected bytes) 33 cases exit 1. Utility checks here
used CPython 3.14.6 (`D:/Pontius/.venv`) for raw-byte hygiene and pin verification, and
coreutils `sha256sum`/Git for digests; no project code was imported or executed.

Raw frozen lines: tool 621, tests 545 (bridge 333 / 198 unchanged). Both changed blobs
are LF-only, no BOM, no trailing whitespace, no line over 100 columns. Budget is a
controller decision; the pinned `authorization.md` grants up to 3,000 lines.

## Verdict

CLEAN / SOUND. The contract is now one owned object (`AdmittedPlan.schedule`) consumed
by admission, execution and reconciliation alike, which is the shape change the
second-residual rule asked for rather than a further guard. No source change is
requested. This review authorizes nothing beyond itself; the combined source's
adoption depends on the ownership/r002 review and the controller's gates.
