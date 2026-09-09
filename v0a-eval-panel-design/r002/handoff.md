# Cold review: v0a-eval-panel-design/r002

Candidate ref: `refs/heads/review/v0a-eval-panel-design/r002`
Candidate commit: `61a1ce0ce964dc56b67636ff71a613e5525ab0ae`
Manifest SHA-256: `8e5b22c22e4f7a7d4a0eff603ed256cc18a66351a329f27b011e6c52c8bbd9e2`
Base commit: `b378104cd2934f248a9545d7d482b0db25db813c`
Tree: `cf5c090f80ceeaf5118214e08e4362a0062b5f3c`
Tier: C specification review; no runtime implementation exists in this candidate.
Round kind: FIX (corrects r001, which was NOT CLEAN / STRAINED under two reviews).

The full commit and manifest bind identity; this path and the index only locate
it. The ref is pushed to `origin`. Independently verify the exact candidate,
base, and blob-derived manifest (`git cat-file blob <commit>:<path>`, whole-row
byte sort, LF rows). Read candidate Git blobs, not mutable working files.
Changed bytes or scope require a new round. Never invoke a runtime, solver,
host, historical owner, or test from this packet.

## Scope

- `docs/architecture/v0a-eval-panel-r001/brief.md` — Stage 0 task brief, corrected
- `docs/architecture/v0a-eval-panel-r001/design.md` — Stage 0b design, corrected

Nothing else differs from base. The candidate is parented on base, not on r001;
r001's frozen candidate `e1e1e357e71cce632aee2a9b50c62705595bf86a` remains for
comparison.

## FIX deferred input

`coverage.md`, SHA-256
`da5487bc8e2144f8ec7d4514353ddbfa6d4be3d7ce19c67818c6d083bb17408e`. Do not
open it until your initial invariant and related-path inventory are recorded.
Its claim maps each r001 finding to the correction and a falsifying
observation, lists the exercised derivations, states limits, and pins the
dependency inventory the r001 reviewers asked for.

The r001 reviews and the finalizer's disposition are in `../r001/reviews/` and
`../r001/disposition.md`. On a FIX round you may read the disposition after
your independent inventory; you may not read another r002 reviewer's output.

## Pinned inputs

At BASE `b378104c`: `README.md` working rules (blob
`99bc05dcfcbbf1786e1ea2e70bfbb1894b68151f`); `docs/workflow.md` checklist v1,
captured byte-identically in `inputs/workflow.md` at SHA-256
`c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37` (base blob
`503fd1701800710e344905589f3ccadbd002b980`); `docs/workflow-amendment-2026-08-30.md`;
`experiments/research-roadmap.md` (blob `08fb65f04459b9b485287ba9cadca60590de4570`).

Controller rulings of 2026-09-08 are in `inputs/controller-rulings.md` at
SHA-256 `2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6`,
unchanged from r001. Two refinements to their wording — ruling 3's "clusters"
stated as fixed strata, and the rulings 1–2 inclusion law made explicit — are
recorded in the candidate design and in `../r001/disposition.md` as flagged for
the controller; they are not new rulings.

## Review contract

Review the whole candidate, not the diff, against checklist v1 and Stage 0 /
Stage 0b in `inputs/workflow.md`. Then challenge the corrections in particular,
against the frozen library sources at BASE:

1. **Host oracle.** Does the v1 `DecisionRecord` mapping in mechanism 5 cover
   every record shape the `blueprint-v1` path can emit, with no shape falling
   outside hit / disagreement / unsupported / excluded? Is the separate direct
   `BlueprintProvider` check well-defined, and does the design avoid inferring
   runtime behavior from it?
2. **Population and calibration.** Is the single inclusion law (collision-only
   rejection, both orientations always played, off-pool hero as
   `passive_default` cell) consistent with the deployed-policy calibration over
   hero uniform on 1,081 × villain uniform on 990? Does whole-unit exclusion
   preserve pairing? Does anything reintroduce a membership filter?
3. **Per-hero-hand T1.** Is the partition argument sound — that villain-policy
   fixity makes hero information sets independent at `s = 4` — and correctly
   confined to T1 and calibration, not T2? Is the sealed singleton-hero game
   `{h} × 990` the right ground truth for the per-hand result, and is a cost
   preflight with a stop condition sufficient discipline before a full pool?
4. **Estimand.** Are the equal-weight four-board strata, the matched-unit
   observation in `[−4s, 4s]`, the Hoeffding-type floor, and the
   tighten-only-before-holdout rule internally consistent and honest about
   what more deals can and cannot reduce?
5. **Static `s = 4` derivation** from `_raise_bounds`, now asserted rather than
   deferred.
6. Whether the r001 advisory items were adopted without introducing new
   errors: `s = 6` three histories, weak-dominance direction control with zero
   allowed, board-order invariant, conservative placeholder, marginalization
   qualifier, softened random-boards claim, dependency inventory.

No implementer transcript or other r002 reviewer's output is a cold input.
No tests, owners, or candidate edits are requested.

CLEAN requires that no material finding survive verification. Every Critical
or Important finding binds to this commit and manifest, cites exact frozen
locations, states a concrete failing scenario (inputs/state → wrong outcome),
and names the smallest correction without implementing it. Separate required
outcomes from advisory design choices. State one required design verdict —
SOUND, STRAINED, or WRONG SHAPE — with a short justification, even if the
defect verdict is CLEAN. On this FIX round, compare your recorded inventory
with `coverage.md` after opening it: challenge the category, the falsifying
observations, and the limits; missing coverage is not automatically a product
defect.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md`, one file per
reviewer, severity-ordered, one entry per finding, design verdict stated
separately. Reviewer assignment is the controller's. A corrected finding is a
new record, never an overwrite.

## Coordinator notes

Branch `codex/v0a-eval-panel` remains at BASE; worktree
`D:/Pontius-worktrees/v0a-eval-panel` holds the two corrected files untracked.
Both candidate files are LF, BOM-free, and at most 100 columns. Implementation,
any solver or host run, ceremonial commit, and changes to sealed surfaces remain
ungranted gates.
