# Cold design review: v0a-i01-freeze-tools-design/r002

Adversarial design review request.

Round kind: FIX. Tier C. Design/specification only.
Finalizer: `codex/finalizer` for this authority-tool checkpoint only.
Required independent reviewers: 2 (`codex-a`, `codex-b`).
Candidate ref: `refs/heads/review/v0a-i01-freeze-tools-design/r002`
Candidate commit: `48e590327c0a4bfd7ea5019e6770e1d582182b08`
Manifest SHA-256: `010e96031f60afd8badc07ebb4dd97ab8db4102527be0eb42ee56c2d65e7c984`
Base commit: `d1ed3cbda6107d61ea8e77133871720af04970cd`
Tree: `27e0503a7f6f4efd44122078aeab62f3151420d5`

The commit plus manifest is the candidate identity. Independently verify the
pushed ref, single parent, exact six-path add-only diff, modes, and manifest
from frozen Git blobs. Do not use checked-out candidate files as byte authority.
Changed bytes or changed scope require a new round.

## Candidate scope

- `docs/briefs/v0a-i01-freeze-tools-r002-brief.md`
- `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v5.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md`
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-schemas.md`

The separate packet file `coverage.md` is frozen handoff material, not a
candidate path. `coverage-plan.md` is excluded from both candidate and packet.

This is a documentation-only design checkpoint. It contains no authority
utility implementation or tests and authorizes none. The workflow amendment and
schemas are proposals under review; they are not adopted authority and grant no
execution.

## FIX predecessor

Rejected predecessor: `v0a-i01-freeze-tools-design/r001`, candidate commit
`ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e`, manifest SHA-256
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

The r001 disposition requires this FIX round to close eleven binding classes:
role capability closure; complete reviewed-source identity; pre-execution
runtime closure; deterministic commit bytes; credential monotonicity; canonical
review provenance; real HTTPS mutation rehearsal; complete main graph/state;
retirement replay closure; fresh-repository adoption ownership; and complete
local atomic-tuple classification. Its consolidation also retains the advisory
graph, replay, and atomicity findings and their verification criteria.

## Complete cold-input set and deferred coverage order

Before opening `coverage.md`, record your own governing invariants and
systematic related-path/seam inventory from the frozen requirements and sources.
Include the inventory and an explicit statement that it preceded the coverage
claim in your report. Then open and challenge:

- `coverage.md`, SHA-256
  `72fff2541772140f558bc40ef3e137a165c240f29feabd9faac139467a030e46`;
  it maps formal and advisory correction classes, discovery method, affected
  members, mechanisms, limits, and falsifying observations;
- this `handoff.md`, `candidate.json`, and `manifest.sha256`;
- the six frozen r002 candidate blobs and their exact base blobs;
- the five frozen r001 candidate blobs and r001 manifest identified above;
- `inputs/r001-disposition.md`, SHA-256
  `e36d27f08ab4cf650542e6effce65c4fae6585c25c73ecd24a47be5a5e76545e`,
  4,190 bytes;
- `inputs/r001-consolidation.md`, SHA-256
  `2905924143ef610e0a4299ec879204d798c7a756991dea8f37c780db4b5191fa`,
  18,301 bytes;
- `inputs/workflow.md`, adopted-workflow capture, SHA-256
  `ab5202b170a5fd9c2cf1540aa198d4a82c742cb336134b0f9a8db944fd64f91a`,
  30,942 bytes; and
- `inputs/runtime-closure.json`, direct CPython closure, SHA-256
  `3390ab3d041d432f06754ca94aed348774c421de1c14553a25395c2cab112a3a`,
  413,522 bytes, 2,614 governed files, 63,499,244 governed bytes.

The pinned workflow capture governs this review over the older workflow blob
inherited from the candidate base. Verify all input hashes before assessment.
Parse the runtime closure read-only; do not start that runtime. Primary
Microsoft, Git, and CPython documentation needed to verify frozen API semantics
may be consulted and cited.

No chat transcript, mutable P or H file, design discussion, implementation
self-report, unlisted check, current advisory audit, r001 formal-review report,
peer report, `progress.md`, candidate artifact, runtime, C candidate, harness,
Model, sensitive case, analyzer, controller artifact, or retained evidence is a
cold input. Both reviewers receive the same immutable initial packet commit.
Mutable handoff `main` is never review authority.

## Review contract

Assess the complete six-document design, not only the r001 correction matrix or
the sections named by `coverage.md`. Challenge whether the structured claim
misses a related member, uses an unsound discovery method, or substitutes a
structural assertion for a falsifying public-boundary observation.

At minimum, determine whether:

- the bootstrap and authority DAG are acyclic, self-free where required, and
  incapable of allowing unreviewed tools to issue their own authority;
- the four role boundaries, complete source projections, child runtime,
  filesystem, Git/GCM, credential, and process capabilities are closed before
  execution and remain closed through cleanup and final revalidation;
- every schema, union branch, digest preimage, byte count, equality, carrier,
  receipt, and publication edge is typed, reachable, unambiguous, and acyclic;
- local tuple, remote pair, main graph, retirement, replay, lost-ack, partial,
  descendant, ambiguity, cancellation, host-failure, and recovery states remain
  monotonic and cannot be cross-substituted;
- raw blob/tree/commit/manifest construction is byte-deterministic and avoids
  checkout, index, filter, attribute, identity, time, and normalization drift;
- reviewer/output cardinality, provenance, issuer attribution, peer blindness,
  and convergence through terminal r005 are exact without self-bootstrap;
- rehearsals exercise the actual Windows, CPython, Git, credential, HTTPS,
  process, storage, retention, and publication boundaries claimed; and
- the frozen brief, central design, schemas, runtime appendix, Git appendix,
  amendment, and deferred coverage claim agree without a stronger requirement
  being weakened elsewhere.

Resolve any conflicting or looping requirement by naming the stronger
invariant, the weaker frozen text, and the smallest coherent correction. Do not
silently choose an interpretation or enlarge authority, scope, or trusted code.

Every Critical or Important finding must bind to this candidate pair, cite
exact frozen locations, state a concrete state/inputs-to-wrong-outcome scenario,
name the violated invariant, and give the required outcome and verification
criteria. Separate required corrections from advisory engineering techniques.

Each report states each of these fields exactly once:

- `Reviewer ID`
- `Candidate commit`
- `Manifest SHA-256`
- `Defect verdict`
- `Design verdict`

The defect verdict is `CLEAN` only when no Critical or Important correction
remains. The design verdict is exactly `SOUND`, `STRAINED`, or `WRONG SHAPE`,
with the adopted-workflow justification. Issue both even if no defect survives.

Routine read-only Git inspection, frozen-blob manifest calculation, source
inspection, and documentation lookup are permitted. Do not implement, edit
candidate or packet bytes, execute the pinned CPython runtime or candidate
artifact, run implementation tests, mutate a network ref, publish a C candidate
or packet ref, mutate retained evidence, or spend an experiment authority.

## Output contract

`codex-a` authors `reviews/review-01-codex-a.md`; `codex-b` authors
`reviews/review-02-codex-b.md`. Neither report is an input to the other review.
Each reviewer must record its initial invariant/seam inventory before opening
`coverage.md`, then compare that inventory to the claim in the same report.

After fixing its report bytes, each issuer supplies exactly one append-only
ledger line for `../progress.md` containing date, round, reviewer, both verdicts,
candidate commit, manifest, report path, and report SHA-256. The coordinator
publishes each issuer-authored output through ordinary handoff packet rule 6.
