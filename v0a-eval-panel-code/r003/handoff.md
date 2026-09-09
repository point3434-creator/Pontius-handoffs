# Cold review: v0a-eval-panel-code/r003

Candidate ref: `refs/heads/review/v0a-eval-panel-code/r003`
Candidate commit: `7004285d883995de98161dafd766b18d7862cd46`
Manifest SHA-256: `12e9ceddd6e366f2a5f4e9ebd1d6de2a8327a7ddbb732cf082f0906d544eab73`
Base commit: `f647a7989394f084875a040b20c41891168163ed` (adoption of the Slice A
implementation design; unchanged since r001)
Tree: `850b111d83aa2755363eca1db25de454b8a0b4b4`
Tier: C — the first source checkpoint of Slice A, implementing design steps 1–3.
Round kind: FIX (corrects r001, NOT CLEAN / STRAINED under two Codex reviews).
Drafter and checkpoint finalizer: Claude. Codex reviews independently; Tier C
requires two independent cold passes.

r002 (`e398f833`) froze the same production code and was withdrawn by the
drafter before any review because its focused receipt failed on a test-fixture
defect (`git` invoked by bare name under the scrubbed environment). r003 differs
from r002 in that fixture and two imports only; see `inputs/r002-withdrawal.md`.

The full commit and manifest bind identity; this path and the index only locate
it. The ref is on `origin`. Recompute parent, tree, scope and the blob-derived
manifest (whole-row byte sort, LF rows) from Git objects; read candidate blobs,
not working files. Changed bytes or scope require a new round. Do not run the
candidate's tool against the repository to learn its behavior — read its frozen
control flow; the receipts in `checks/` are the executed evidence for this round.

## Scope — the same seven paths as r001, nothing sealed touched

- `src/pontius/eval_bridge.py` — adds `require_declared_root`, `prefix_document`,
  `hand_universe_digest`, work counts, per-action `forced_value`, and boundary
  encodings returned as bytes from `capacity_probe`.
- `tools/v0a_eval_panel.py` — plan schema v2 with closed per-phase key sets and
  the full ordered permutation; `parse_plan` with size bound, constant refusal
  and finiteness walk; the supervisor rebuilt on the workload ownership pattern
  (assignment tracked, unassigned process killed, sender thread, guarded
  cleanup, pipes closed, nested `job.close()`); per-stage events assembled by the
  parent; boundary artifacts retained in the run directory; `json_safe`;
  `main` records once on success, failure and interruption.
- `tests/test_eval_bridge.py` (11), `tests/test_eval_panel_tool.py` (11).
- `tests/fixtures/eval_panel/plan-capacity.json`, `plan-preflight.json` —
  schema v2, carrying the 1,081-hand permutation.
- `tests/cases.json` — the two suites registered.

## FIX deferred input

`coverage.md`, SHA-256
`4eaf77871518f84043010f998ed62257991c84b5bdb7f7ceebd0ae8c43d048ff`. Do not
open it until your initial invariant and related-path inventory are recorded.
It is organized by data path (plan bytes → schema → declared root → capacity →
production → reference → lattice → request transport → ownership → stage
events → nonfinite output → run record), with the r001 finding letters as
cross-references, and lists the executed cases.

The r001 reviews and the finalizer's disposition are in `../r001/reviews/` and
`inputs/prior-disposition.md`. On a FIX round you may read the disposition after
your independent inventory; you may not read another r003 reviewer's output.

## Pinned inputs

- `inputs/workflow.md`, SHA-256
  `c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37`.
- `inputs/controller-rulings.md`, SHA-256
  `9652b870dfb214af764addb3de276c776d51015d7e55b75b98d0bb519711f3bc`, and
  `inputs/controller-rulings-addendum.md`, SHA-256
  `d3a15c896463449913fa0852b51f654ac7688b6c6941b57652a745244e040a6c` (the
  raised slice budget; the exact figure remains the drafter's reading).
- `inputs/dependencies.json`, SHA-256
  `ab0933726111415870200d4b14358012826da35fd2f083890cf7d8b0165f50b2` (34
  direct pins at BASE; not a transitive closure).
- `inputs/prior-disposition.md` (r001), SHA-256
  `31b5d5ea90942b45466906d7b4bc72ddc9454fbad604453a47836caa4b1cbab5`;
  `inputs/r002-withdrawal.md`, SHA-256
  `1c50a633a7bcc65dc356a26a2b3751a7093d40a9047f02e8ee43237f5f67afbf`.
- The governing documents at BASE: `docs/architecture/v0a-eval-panel-impl-r001/
  {brief,design}.md` and the parent lane design.

## Receipts in `checks/`

| File | SHA-256 | What it is |
|---|---|---|
| `focused-snapshot-3.14.6.txt` | `9cbd626f1a8590a222e2f7cca39db4b55c2274acc1c7141fcd194d36945b95a6` | both suites through `tests/test_pontius.py` in a disposable detached snapshot of the candidate with its own `uv sync --group dev` venv; `-B -P -W error::ResourceWarning`, `env -i` with `SystemRoot TEMP TMP PONTIUS_GIT`; **22 cases, 0 skipped, exit 0** |
| `focused-snapshot-receipt.txt` | `d6259f2d44bc3c05f1de1c7e678f6e4b3e3775fbf55fcd9faf861c23bf8a29db` | snapshot commit, interpreter, invocation, environment |
| `focused-snapshot-journal-line.jsonl` | `dd774ae2c1e1ba5f4416b353b4db75d6dedea1dac8b3befbef1fca3800505033` | the harness's one journal row **inside the snapshot**; `source_verified: true`, `source_commit` = candidate |
| `line-budget-and-hygiene.md` | `09dd0998f06a9bb016723d27171485431630d8bd8cdbe4080655d4f0714a9bd8` | 792 production / 428 test raw lines; 0 over-100-column lines, 0 CR, 0 trailing whitespace; the budget projection for the whole slice |

Digests are of the LF bytes as stored. The snapshot was removed after the
receipts were copied; no journal row was written in a live worktree.

## Review contract

Review the whole candidate, not the diff, against checklist v1 and design
steps 1–3. Then challenge each r001 correction against frozen source at BASE:

1. **Ownership (r001 A).** In `supervise`: is the unassigned-process branch
   reachable and correct when `Job.assign` raises after a suspended `Popen`?
   Can any exception in the cleanup block still skip `job.close()` or lose
   drained events? Are the three pipes closed on every path? In `main`: does
   every failure after `begin_run`, including `KeyboardInterrupt`, reach
   `finish_run` exactly once with `output_directory` set whenever the directory
   was created?
2. **Admission (r001 B, C, D).** Does `parse_plan` refuse `1e999`, `NaN`,
   `Infinity` and oversize input before any worker exists? Does `validate_plan`
   bind the prefix, universe digest, count, seed **and** the full ordered
   permutation, refuse unknown members including bank fields, reject bool and
   nonfinite seconds and non-exact memory, and prevent a `test-subset` from
   passing as `declared-full`? Is the sender thread sufficient for the
   pipe-fill stall, given no test reproduces it?
3. **Declared domain (r001 E).** Does `require_declared_root` refuse `s = 3`
   and `s = 6` at every production and reference entry, and is the returned
   bet the constant `raise_to(2)` rather than anything derived from the root?
4. **Retention (r001 F, G).** Are the boundary artifacts written from the
   worker's base64 into the single run directory and bound by path, length and
   digest? Do stage events let a kill after production retain that stage with
   the rest labeled missing, and does an incomplete hand still fail the phase?
5. **Coverage (r001 H).** Do the executed cases in `coverage.md` exercise the
   real launcher for assignment refusal, budget kill and completion, the real
   `finish_run` for a completed run and a `1e999` refusal, and the sealed
   reference on `As Ad`? Compare with your inventory after opening it.
6. **Budget.** 792 / 428 for this checkpoint; the slice projection is
   1,000–1,100 production lines. Assess as before: candidate defect, brief
   defect, or controller decision.

No implementer transcript, prior-round review, or other reviewer's output is a
cold input. Record your own inventory before opening `checks/` or `coverage.md`.
No tests, owners, or candidate edits are requested; the receipts are the
executed evidence.

CLEAN requires that no material finding survive verification. Every Critical or
Important finding binds to this commit and manifest, cites exact frozen
locations, states a concrete failing scenario, and names the smallest correction
without implementing it. State one required design verdict — SOUND, STRAINED,
or WRONG SHAPE — with a short justification. On this FIX round, compare your
recorded inventory with `coverage.md` after opening it; missing coverage is not
automatically a product defect.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md`, one file per
reviewer, severity-ordered. Reviewer assignment is the controller's. A corrected
finding is a new record, never an overwrite.

## Coordinator notes

Branch `claude/v0a-eval-panel-code` remains at BASE; the worktree holds the
seven paths uncommitted. Implementation beyond steps 1–3, retained measurement,
ceremonial commit, and integration remain ungranted gates.
