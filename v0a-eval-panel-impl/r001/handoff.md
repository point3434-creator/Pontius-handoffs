# Cold review: v0a-eval-panel-impl/r001

Candidate ref: refs/heads/review/v0a-eval-panel-impl/r001
Candidate commit: e39d3b93695bfc601d051e8e71f334eef4d10d19
Manifest SHA-256:
4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405
Base: 46f45298a405b967976413a4b8e45e7837602316
Tree: 353e9626ee00ecf1c45b17b04d748d4990d99b8e
Tier C, Stage 0 / Stage 0b specification review. Round kind: NEW-SURFACE.
Drafter and checkpoint finalizer: Codex. Claude reviews independently; Tier C
requires a second independent pass. No review verdict is asserted by this packet.

## Target and authority

Review the complete frozen documents:
- docs/architecture/v0a-eval-panel-impl-r001/brief.md
- docs/architecture/v0a-eval-panel-impl-r001/design.md

The controller requested Codex to design the next checkpoint under the workflow.
The parent specification was accepted at v0a-eval-panel-design/r003 and adopted
as the stated base. Its specification blobs match candidate
18b7527a3989f7d38830a7881c976385fe9bc4de.
Existing implementation/source bytes are unchanged. Integration to master and
execution authority are separate; this packet does not assert either happened.

The proposed first source checkpoint measures wire capacity and per-hand T1 cost.
Bridge completion follows the measured decision within the same Slice A budget.
This packet itself contains no source implementation and no measurements.

## Cold inputs and identity

Read this handoff first. Recompute the candidate parent/tree/scope and manifest
from Git blobs using whole-row byte sort and LF rows. Read candidate Git blobs,
not mutable files. Record an independent invariant and related-path inventory
before reading author checks or prior-round commentary. Do not read another
reviewer's output, task ledger or implementer conversation. There is no deferred
FIX coverage claim in this NEW-SURFACE round.

Pinned inputs under inputs/:
- workflow.md (byte-identical to BASE docs/workflow.md), SHA-256:
  c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37
- controller-rulings.md, SHA-256:
  2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6
- parent-disposition.md (accepted r003 implementation constraints), SHA-256:
  218fdf7b80470d862084a9523022bc15de5dfd49ba91694191fee659f900e0bd
- dependencies.json (direct semantic inventory at BASE), SHA-256:
  ce6c5a918a4c57c35de70c7e986e4a0f8f9c681221ff1a09f8fa7a122f17be3f

Also read BASE README.md, docs/workflow-amendment-2026-08-30.md and the parent
specification at docs/architecture/v0a-eval-panel-r001/{brief,design}.md.
The dependency inventory is a navigation aid, not a transitive-closure claim.
Discover related paths independently and challenge omissions by concrete impact.

## Review contract

Apply workflow checklist v1 and Stage 0/0b to the entire candidate. Challenge:

1. Whether the first source checkpoint really obtains capacity/cost before bridge
   completion without changing Slice A scope or resetting its budgets.
2. Whether the conservative wire-prefix boundary, fixed source_id width and final
   remeasurement establish the stated capacity claim without strength selection.
3. Whether per-hand kernel enumeration and the explicitly fixed-CALL singleton
   reference agree, including tie arithmetic, cost accounting and interruption.
4. Whether finite seeded host witnesses cover the required keys without forcing
   dealt cards or becoming a filtered population for later chip inference.
5. Whether outcome eligibility, agreement eligibility and complete accounting
   remain separate across real session/result/frame and provider boundaries.
6. Whether inherited source admission, per-session preparation, one run record,
   scope limits, executable negative controls and the line budget are credible.

No runtime, solver, host, historical owner, test, source edit or candidate edit
is requested. Use static source inspection and arithmetic. Do not fetch: the
required frozen objects are local. Running a source tool to learn its output is
outside this review; read its frozen control flow instead.

CLEAN requires no material finding survive verification. Each Critical/Important
finding must bind to the candidate+manifest, cite frozen locations, state a
concrete failing scenario and the smallest correction. Separate advisory choices
from required outcomes. State SOUND, STRAINED or WRONG SHAPE separately from
the defect verdict, with the reason and the review's evidence limits.

Return one attributed, append-only report at reviews/review-<NN>-<reviewer>.md.
Assignment is the controller's. Record each reviewer's own task-ledger line;
do not overwrite issued findings. The author may not supply a cold review of
this candidate. New bytes or scope require a new round and fresh identity.
