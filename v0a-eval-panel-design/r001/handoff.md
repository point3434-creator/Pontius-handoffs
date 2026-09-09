# Cold review: v0a-eval-panel-design/r001

Candidate ref: `refs/heads/review/v0a-eval-panel-design/r001`
Candidate commit: `e1e1e357e71cce632aee2a9b50c62705595bf86a`
Manifest SHA-256: `8798e05557bff9436ca3a057dc40a169f1b61c5e7d51379a288b5918b6d5ac5a`
Base commit: `b378104cd2934f248a9545d7d482b0db25db813c`
Tree: `bf0079d6f05da01df13108c347d840d429bc1d44`
Tier: C specification review; no runtime implementation exists in this candidate.
Round kind: NEW-SURFACE.

The full commit and manifest bind identity; this path and the index only locate
it. The ref is pushed to `origin`. Independently verify the exact candidate,
base, and blob-derived manifest (`git cat-file blob <commit>:<path>`, whole-row
byte sort, LF rows). Read candidate Git blobs, not mutable working files.
Changed bytes or scope require a new round. Never invoke a runtime, solver,
host, historical owner, or test from this packet.

## Scope

- `docs/architecture/v0a-eval-panel-r001/brief.md` — Stage 0 task brief
- `docs/architecture/v0a-eval-panel-r001/design.md` — Stage 0b design

Nothing else differs from base. The frozen tree is base plus these two files.

## Pinned inputs

At BASE `b378104c`: `README.md` working rules (blob
`99bc05dcfcbbf1786e1ea2e70bfbb1894b68151f`); `docs/workflow.md` checklist v1,
captured byte-identically in `inputs/workflow.md` at SHA-256
`c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37` (base blob
`503fd1701800710e344905589f3ccadbd002b980`); `docs/workflow-amendment-2026-08-30.md`;
`experiments/research-roadmap.md` (blob `08fb65f04459b9b485287ba9cadca60590de4570`),
which the brief and design position this lane against.

Controller rulings that settled six design decisions on 2026-09-08 are in
`inputs/controller-rulings.md` at SHA-256
`2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6`. They are
direct user instructions and are review input, not review outcome.

Source surfaces the design declares frozen, with their base blobs, are listed
in the design's own "Base blobs" table. Verify that table against BASE; a wrong
blob there is a Critical finding.

## Review contract

Review the whole candidate against checklist v1 and the Stage 0 / Stage 0b
requirements in `inputs/workflow.md`: every template field present and
decided rather than defaulted; each design element names its mechanism, the
invariant it maintains, and every place that invariant must hold; alternatives
rejected with reasons; a coverage claim stated before building; rulings
recorded, not left implicit.

Challenge these technical claims in particular, against the frozen library
sources at BASE:

1. The reachability claim: opponents `fold_to_bet` in seats 0, 3, 4, 5 and
   `passive` in seat 1 with controlled seat 2 and button 0 reach the
   `LegalHeadsUpRiverContinuation` entry condition on **every** deal, with the
   four omitted seats at zero committed chips.
2. The `s = 4` claim: exactly one legal bet size and one hero decision node per
   hand. The design marks this "to be confirmed against the kernel"; say
   whether the kernel's raise-to rules support it.
3. Villain's marginal hand distribution given board and hero hand is uniform
   over the 990 compatible hands regardless of the folders' cards.
4. Capacity arithmetic, and the wire-bytes-versus-canonical-bytes distinction.
5. Soundness of the three amended criteria, and whether any amendment weakens
   the brief's protected invariant.
6. T1 purity and lossless export; whether the agreement enumeration's
   reachability definition is well-founded for a pure policy.
7. Validity of the calibration control: `expected_utilities` over the declared
   joint range against a panel whose hero distribution is conditional on a
   table hit.
8. Whether the hand-swap duplicate is well-defined when the pool `H` is smaller
   than the full 1,081 hands.
9. Whether the four "must be byte-identical" surfaces are sufficient, or
   whether the runtime, provider, or host code paths the key identity depends
   on should also be pinned.

No implementer transcript, prior findings, disposition, or other reviewer's
output is a cold input. Do not read those before issuing your independent
verdict. No tests, owners, or candidate edits are requested.

CLEAN requires that no material finding survive verification. Every Critical
or Important finding binds to this commit and manifest, cites exact frozen
locations, states a concrete failing scenario (inputs/state → wrong outcome),
and names the smallest correction without implementing it. Separate required
outcomes from advisory design choices. State one required design verdict —
SOUND, STRAINED, or WRONG SHAPE — with a short justification, even if the
defect verdict is CLEAN.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md`, one file per
reviewer, severity-ordered, one entry per finding, design verdict stated
separately. Reviewer assignment is the controller's. A corrected finding is a
new record, never an overwrite.

## Coordinator notes

The controller's instruction was to create the worktree and branch, place the
documents, and freeze. The documents were placed **uncommitted** in the
worktree and frozen from there, because the workflow's order is freeze →
review → tests → authorize → commit → push, and a prior commit would have left
this candidate's manifest empty. Branch `codex/v0a-eval-panel` remains at BASE;
worktree `D:/Pontius-worktrees/v0a-eval-panel` holds the two files untracked.

The rulings settle design questions only. Implementation, any solver or host
run, ceremonial commit, and changes to sealed surfaces remain ungranted gates.
