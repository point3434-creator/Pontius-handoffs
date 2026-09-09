# Cold review: v0a-eval-panel-code/r001

Candidate ref: `refs/heads/review/v0a-eval-panel-code/r001`
Candidate commit: `b1fdacf157649ca92d1aee3e39b7b0471edbcd5d`
Manifest SHA-256: `376dff405c15301a489ea3fde84abc3a41c2afa4c33c6ee67423477ca9e08b8e`
Base commit: `f647a7989394f084875a040b20c41891168163ed` (adoption of the Slice A
implementation design, `v0a-eval-panel-impl/r002`, on `codex/v0a-eval-panel-impl`)
Tree: `7a450159a8ca30cb0ac176e66f6e2a25235c457d`
Tier: C — the first source checkpoint of Slice A, implementing design steps 1–3.
Round kind: NEW-SURFACE. Drafter and checkpoint finalizer: Claude. Codex reviews
independently; Tier C requires two independent cold passes.

The full commit and manifest bind identity; this path and the index only locate
it. The ref is on `origin`. Recompute parent, tree, scope and the blob-derived
manifest (whole-row byte sort, LF rows) from Git objects; read candidate blobs,
not working files. Changed bytes or scope require a new round. Do not run the
candidate's tool against the repository to learn its behavior — read its frozen
control flow; the receipts in `checks/` are the executed evidence for this round.

## Scope — seven paths, all added or modified, nothing sealed touched

- `src/pontius/eval_bridge.py` — replayed root, hand universes, root keys,
  strength-blind permutation, capacity probe, per-hand integer totals, and the
  singleton sealed reference split into construction, forced values,
  `best_response`, and pure lattice validation.
- `tools/v0a_eval_panel.py` — plan validation, `Job`-supervised worker,
  capacity and preflight phases, one `begin_run`/`finish_run` per invocation
  with `output_directory` under `experiments/results/runs`.
- `tests/test_eval_bridge.py`, `tests/test_eval_panel_tool.py` — 14 cases.
- `tests/fixtures/eval_panel/plan-capacity.json`, `plan-preflight.json`.
- `tests/cases.json` — the two suites registered.

Design steps 4–7 (export, membership, provider check, outcome/agreement
classifier, export/agreement phases) are **not** in this candidate, by design:
capacity and cost are measured before bridge code exists.

## Pinned inputs

- `inputs/workflow.md` checklist v1, byte-identical to BASE `docs/workflow.md`,
  SHA-256 `c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37`.
- `inputs/controller-rulings.md`, SHA-256
  `9652b870dfb214af764addb3de276c776d51015d7e55b75b98d0bb519711f3bc` — carries
  the 3.14-only ruling (absent from the impl packets), the acceptance of the
  implementation design, and the authorization to implement this checkpoint.
- `inputs/dependencies.json`, SHA-256
  `ab0933726111415870200d4b14358012826da35fd2f083890cf7d8b0165f50b2` — the
  direct semantic inventory (34 blobs), re-verified at BASE; not a transitive
  closure.
- The governing documents at BASE: `docs/architecture/v0a-eval-panel-impl-r001/
  {brief,design}.md` (the adopted r002 text) and the parent lane design
  `docs/architecture/v0a-eval-panel-r001/design.md`.

## Receipts in `checks/`

| File | SHA-256 | What it is |
|---|---|---|
| `focused-snapshot-3.14.6.txt` | `a62c2780924cce4344c592daf26738e75847c185dfb38491256a3c8d103517a7` | pytest output: both suites through `tests/test_pontius.py` in a disposable detached snapshot of the candidate with its own `uv sync --group dev` venv; `-B -P`, `env -i` with `SystemRoot TEMP TMP PONTIUS_GIT`, absolute Git; **14 cases, 0 skipped, exit 0** |
| `focused-snapshot-receipt.txt` | `483826946647e3c39ea7170f9400383d0f80337dcd2c73bbfdcc680f01c2e64f` | snapshot commit, interpreter, invocation, environment |
| `focused-snapshot-journal-line.jsonl` | `0b5b24a45f129c767ac5ef2c92cc7af7f34c8cc29e27a10c235e6976aaa7ad86` | the one journal row the harness wrote **inside the snapshot**; `source_verified: true`, `source_commit` = candidate |
| `line-budget-and-hygiene.md` | `9e2eab5288d43d5b67150cfe1fb33706c1764ae93acf72eb37c569046c335ba2` | line counts against the slice budget; 0 over-100-column lines, 0 CR, 0 trailing whitespace |
| `development-diagnostic.md` | `dc8a88ac667e107b97ae0cb90b017293e560ae797644b9bf3a386f9a93c3e4b9` | **NOT EVIDENCE**: in-process, unjournaled run of both phases by the drafter before the freeze, so the numbers' shape is visible |

The snapshot was removed after the receipts were copied; no journal row was
written in `D:/Pontius` or any live worktree.

## Review contract

Apply checklist v1 and the adopted design's steps 1–3 to the whole candidate.
Challenge in particular, against frozen source at BASE:

1. **Root and keys (design §2).** `replay_root` replays the declared prefix via
   `new_hand`/`apply_action`/`advance_street` and refuses drift; `root_key` uses
   `BlueprintDecisionKey.from_state` with the root's own `legal_decision()`;
   `board_cards` refuses non-ascending boards. Is anything hand-filled?
2. **Capacity (§2).** `placeholder_artifact` uses `check`/`null` rows and the
   fixed-width `t1:` + 64 zeros `source_id`; `capacity_probe` binary-searches
   the nested prefix family on **wire** bytes from `encode_blueprint`, retains
   boundary sizes and digests, and decodes the boundary artifact to check key-set
   equality. Is the monotonicity assumption sound for this codec? Is any
   canonical-bytes size used anywhere?
3. **Per-hand totals (§3).** `hand_totals` settles both forced lines through the
   kernel (`_terminal` advances a completed river round only if the kernel left
   it non-terminal); integer totals; CHECK on exact equality; no private payoff
   formula. Does it ever construct more than one hero hand's game?
4. **Singleton reference (§3).** `build_reference` supplies exactly 990 deals at
   raw weight 1.0, asserts one hero root with `(CHECK, raise_to(2))`, `CALL` at
   every villain key, terminal utility ≤ 4 and no extra chance node on the
   forced lines, and an explicit `{FOLD: 0.0, CALL: 1.0}` villain policy;
   `forced_values` uses `expected_utilities` with explicit deterministic hero
   policies; `reference_best_response` is a separate call. Are the domain
   assertions the design demands all present and are any of them tautological?
5. **Lattice rule (§3).** `lattice_integer` treats each float as its exact
   dyadic rational, admits exactly one `J` with `|R − J/n| ≤ 2⁻⁴⁰` in
   `[−4n, 4n]`, and `validate_reference` requires `J == production`, production
   maximizing, `best_response` value within the bound of `max(J)/n`, a map with
   exactly the hero key and a legal action, exact action equality on non-ties,
   production CHECK on ties with either reference label accepted and recorded.
   Check the arithmetic fixtures in `test_eval_bridge.py` against the design's
   list: cancellation both signs, false production tie, changed total, wrong
   non-tie action, smallest lattice gap both signs, NaN/inf.
6. **Tool (§1, §3, §6).** `validate_plan` refuses every missing mandatory input
   with no defaults; `run_plan` stops at the first reference disagreement and at
   an exhausted budget, and a preflight never starts a full-pool solve;
   `supervise` launches one suspended worker into a memory-limited `Job`, sets
   `PONTIUS_RUN_CONTEXT` in its environment, terminates the job on budget,
   verifies cleanup; `main` calls `begin_run` once, sets `output_directory`,
   calls `finish_run` once including on failure. Does the worker's `cwd=ROOT`
   satisfy the design's worker-root rule? Does `cache_state()`'s read of the
   ranker's private cache count as touching a sealed surface?
7. **Budget.** `checks/line-budget-and-hygiene.md` states that this checkpoint
   alone uses 575 of the slice's 600 production lines and that bridge
   completion cannot fit. Assess whether that is a candidate defect, a brief
   defect, or a controller decision; the drafter's view is the third.

No implementer transcript, prior-round review, or other reviewer's output is a
cold input. Record your own invariant and related-path inventory before opening
`checks/`. No tests, owners, or candidate edits are requested; the receipts are
the executed evidence, and re-running the harness from this packet is outside
the review.

CLEAN requires that no material finding survive verification. Every Critical or
Important finding binds to this commit and manifest, cites exact frozen
locations, states a concrete failing scenario (inputs/state → wrong outcome),
and names the smallest correction without implementing it. Separate required
outcomes from advisory design choices. State one required design verdict —
SOUND, STRAINED, or WRONG SHAPE — with a short justification.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md`, one file per
reviewer, severity-ordered. Reviewer assignment is the controller's and is the
reauthorization the brief requires for a review beyond the two specification
rounds. A corrected finding is a new record, never an overwrite.

## Coordinator notes

Branch `claude/v0a-eval-panel-code` remains at BASE; the worktree
`D:/Pontius-worktrees/v0a-eval-panel-code` holds the seven paths uncommitted.
Tests during development used `D:/Pontius/.venv` (3.14.6 + numpy) via
`unittest discover -s tests`, because `-P` drops the working directory and the
bare 3.14 interpreter lacks numpy; the receipt run used a venv synced inside the
disposable snapshot instead of touching the main one. Implementation, retained
measurement, ceremonial commit, and integration remain ungranted gates.

## Correction (2026-09-09)

`checks/focused-snapshot-3.14.6.txt` was captured with CRLF line endings and
normalized to LF when stored; the digest in the receipts table above is of the
working file. The authoritative stored-blob SHA-256 is
`71852648acf012cac609c144d3c669390e4bcf710e89aed0e50f86f87e7235c2`. Content identical modulo line endings; the file in the
packet is now LF.
