# Cold review: v0a-eval-panel-design/r003

Candidate ref: `refs/heads/review/v0a-eval-panel-design/r003`
Candidate commit: `18b7527a3989f7d38830a7881c976385fe9bc4de`
Manifest SHA-256: `2664aca6f857999a4b45036b5cd3c250fbc3d8210b3132510d0e05a57e821975`
Base commit: `b378104cd2934f248a9545d7d482b0db25db813c`
Tree: `26952b679cde91cc3c975500e2dd15a9270934ca`
Tier: C specification review; no runtime implementation exists in this candidate.
Round kind: FIX (corrects r002, which was NOT CLEAN / STRAINED under two reviews).

The full commit and manifest bind identity; this path and the index only locate
it. The ref is pushed to `origin`. Independently verify the exact candidate,
base, and blob-derived manifest (`git cat-file blob <commit>:<path>`, whole-row
byte sort, LF rows). Read candidate Git blobs, not mutable working files.
Changed bytes or scope require a new round. Never invoke a runtime, solver,
host, historical owner, or test from this packet.

## Scope

- `docs/architecture/v0a-eval-panel-r001/brief.md` — Stage 0 task brief, corrected
- `docs/architecture/v0a-eval-panel-r001/design.md` — Stage 0b design, corrected

Nothing else differs from base. The candidate is parented on base, not on
r002. Prior frozen candidates for comparison: r001 `e1e1e357…`, r002
`61a1ce0c…`.

## FIX deferred input

`coverage.md`, SHA-256
`964369af90b87912ea72ad11e90609551b82f6a0fa60c4c633a849dc152efb23`. Do not
open it until your initial invariant and related-path inventory are recorded.
Following the r002 reviewers' critique, it is organized by **path** — teacher →
export → acquisition → composition → child frames → host validation →
retention → classifier → provider boundary → settlement → pairing →
divergence → exclusion → inference → recording — with the governing frozen
surface, the r003 assertion, and a falsifying observation per stage; finding
IDs are cross-references only. It pins a 21-blob dependency inventory
including `v0a/trace.py` and `legal_decision_spine_v2.py`.

The r002 reviews and the finalizer's disposition are in `../r002/reviews/` and
`../r002/disposition.md`. On a FIX round you may read the disposition after
your independent inventory; you may not read another r003 reviewer's output.

## Pinned inputs

At BASE `b378104c`: `README.md` working rules (blob
`99bc05dcfcbbf1786e1ea2e70bfbb1894b68151f`); `docs/workflow.md` checklist v1,
captured byte-identically in `inputs/workflow.md` at SHA-256
`c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37` (base blob
`503fd1701800710e344905589f3ccadbd002b980`); `docs/workflow-amendment-2026-08-30.md`;
`experiments/research-roadmap.md` (blob `08fb65f04459b9b485287ba9cadca60590de4570`).

Controller rulings of 2026-09-08 are in `inputs/controller-rulings.md` at
SHA-256 `2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6`,
unchanged since r001. No new ruling or refinement was made for r003.

## Review contract

Review the whole candidate, not the diff, against checklist v1 and Stage 0 /
Stage 0b in `inputs/workflow.md`. Then challenge the two r002 corrections and
their consequences, against the frozen sources at BASE:

1. **Outcome classifier (mechanism 5; brief criteria 1–2).** Is failure
   precedence over the real envelopes — session hand entry, host
   `hand_result`, per-event `event_result` with nullable `decision`/`failure`
   — complete? Does every failure shape the frozen runtime and host can
   produce (pre-publication rejection with no decision, ambiguous delivery,
   timing failure after accepted delivery, incomplete hand, protocol or
   cleanup failure, truncated capture) land in **excluded** without needing a
   decision record? Is reading the river `DecisionRecord` from the retained
   `child_stdout_base64` frame stream sound, given `read_stream`'s cap and
   `capture_truncated`? Is the independent `action_for` cross-check of
   `selection_reason` correctly motivated by the v1 host performing no lookup,
   and does it separate hit from default on check-hands as claimed?
2. **Missingness (mechanisms 7 and 9; brief criteria 5 and 7).** Is
   retaining prefix-diverged units in chip comparisons — while excluding them
   from agreement only — the right resolution of card-dependent divergence?
   Is the withhold-on-any-exclusion rule, with survivors reported as
   conditional and Manski bounds over the planned denominator, a valid
   inferential statement, and is anything still silently substituting a
   survivor estimand? Are the normalization equations and the Hoeffding floor
   on planned units internally consistent?
3. Whether the r001 corrections survived the r002 edits intact: per-hero-hand
   T1 with the singleton sealed game as ground truth; collision-only
   acquisition with off-pool defaults; fixed strata; static `s = 4`.
4. Whether the coverage claim's path organization actually enumerates the
   design's category, and whether the 21-blob inventory now covers every
   surface the key identity and the oracle depend on.

No implementer transcript or other r003 reviewer's output is a cold input.
No tests, owners, or candidate edits are requested.

CLEAN requires that no material finding survive verification. Every Critical
or Important finding binds to this commit and manifest, cites exact frozen
locations, states a concrete failing scenario (inputs/state → wrong outcome),
and names the smallest correction without implementing it. Separate required
outcomes from advisory design choices. State one required design verdict —
SOUND, STRAINED, or WRONG SHAPE — with a short justification, even if the
defect verdict is CLEAN. On this FIX round, compare your recorded inventory
with `coverage.md` after opening it; missing coverage is not automatically a
product defect.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md`, one file per
reviewer, severity-ordered, one entry per finding, design verdict stated
separately. Reviewer assignment is the controller's. A corrected finding is a
new record, never an overwrite.

## Coordinator notes

Branch `codex/v0a-eval-panel` remains at BASE; worktree
`D:/Pontius-worktrees/v0a-eval-panel` holds the two corrected files untracked.
Both candidate files are LF, BOM-free, and at most 100 columns. This is the
third specification round; the r002 disposition asks the controller whether
the brief's two-review-round budget, written for implementation slices, also
bounds specification rounds. Implementation, any solver or host run,
ceremonial commit, and changes to sealed surfaces remain ungranted gates.
