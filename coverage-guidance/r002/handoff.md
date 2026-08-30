# Coverage-guidance r002

Round kind: FIX, r001 I1 only (coverage-only closure can require a fabricated RED).
Tier A. Finalizer: Claude. No ceremonial source commit is authorized.

Candidate: 81fb6cf6491b7ae87ca2a2a3ccd0a7103c4cfed3
Ref: refs/heads/review/coverage-guidance/r002
Base: d1ed3cbda6107d61ea8e77133871720af04970cd
Tree: 33dc90fc78bb8ec62f07c7afed82f6b4b2a4851e
Manifest SHA-256: 2c9903843b765143f2f2a33c4c3e0233ff0ca9c907faae9462f12b2577e56fdc
Prior candidate: d07b11e874955121487351a20104dec5176f9cb3
Prior manifest: dd4dcf342e86556db151871fb1e5292ff0cd0f68e8160f969c9ff5f90bdd5c6b

Scope: frozen docs/workflow.md only; relative to r001, just the Stage 1 and
Stage 4 finding-closure rules. Other source files and the separate pending
mandatory design-verdict block are excluded. Mutable working and before/after
captures are not cold inputs.

Acceptance: retain genuine behavioral RED/GREEN, allow independent evidence
closure when no behavioral defect is shown, and avoid conflicting obligations
elsewhere. Preserve existing immutable-ref, severity, scope and authorization
rules. No additional approval stage or claim of acceptance is introduced.

Allowed prior finding: ../r001/reviews/review-01-codex.md I1. Before reading
the structured coverage claim, independently inventory finding-closure paths
from the frozen requirements and source, and record it in checks/.
Then read coverage.md (SHA-256 b293a9260ff3556f1384fe943414332e46ddc40d55db6d6a5f019c43e190da4a).
The claim is supporting review input, not the authority for the verdict.

Verify the pair from Git blobs using absolute Git. No Python production imports,
test runs, or code edits needed. One independent light documentation pass.
Write reviews/review-01-codex.md, bound to the full pair. You have the exclusive
append slot for ../progress.md for your own verdict; preserve prior bytes.
Do not edit issued packet inputs or other records and do not commit.
