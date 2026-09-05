# Cold design review: v0a-blueprint-artifact-design/r001

Tier C, NEW-SURFACE design review. Finalizer/coordinator: Codex.
Candidate: 336b8660f2f0b33fbeaa40d02cfc97c041ae6e1a
Base: 7ee314b443e10896e87a2e194f24eddda31ff77d
Ref: refs/heads/review/v0a-blueprint-artifact-design/r001
Manifest SHA-256: 404d81333837358c2c4d5d60e1702039a13c276dbe14979684033aa23b82024a

The review object is exactly two frozen Git blobs:
- docs/architecture/v0a-blueprint-artifact-r001/design.md
- docs/architecture/v0a-blueprint-artifact-r001/source-opening-draft.md

Local repository containing the immutable ref:
D:/Pontius/tmp/v0a-blueprint-artifact-design-r001/freeze-snapshot
Permanent packet home:
D:/Pontius-handoffs/v0a-blueprint-artifact-design/r001/

The controller approved this written proposal for freezing and independent
review. The proposal includes a closed JSON codec, a proposed format ceiling,
bounded registration exceptions and correction budgets. It does not authorize
implementation, adoption, a source seal, a ceremonial commit or a runtime run.

Read CLAUDE.md and docs/workflow.md at the base, especially Stage 0b, Stage 3 and
the checklist. Requirements are docs/briefs/v0a-blueprint-artifact-brief.md and
ADR-0489 at the base. Read relevant ADR-0485/0486/0487 scope and immutability
boundaries as needed. The six proposed registration exceptions are reviewable
changes, not permissions already in force; assess their precision and scope.

Independently recompute the manifest from raw frozen Git blobs using whole-row
digest-first sorting, not checkout hashes. Verify the supplied base/ref/tree
and the exact two-file population. Then assess the design against the real
key/action API, runtime admission and replay reader, existing registration/CI
mechanisms, and the applicable requirements. Distinguish a missing requirement
from an advisory preference. Assess the claimed acceptance oracles, field
coverage, rejection and identity contracts, source-opening sequence, bounded
scope and implementability. Do not relitigate parked lanes outside this scope.

This is a design-only review: no feature exists to test yet. A missing test
execution is not itself a design defect. Read source; do not import project
payloads, run tests/owners/prototypes, install anything, move Git state, mutate
source, or create an implementation. Read-only hashing and source inspection
are permitted. Do not spawn agents or read another reviewer's findings, this
thread, implementer transcripts, or non-required coordination material.

Return a severity-ordered report bound to candidate and manifest, with Spec and
Quality PASS/FAIL, Critical/Important/Minor counts, and a mandatory design verdict
SOUND/STRAINED/WRONG SHAPE. Each required correction names an exact file/line,
unmet contract, concrete consequence and verification criterion. Distinguish
required corrections from advisory implementation choices. CLEAN means no
required correction remains. State source-inspection limits and independence.
The dispatch supplies your sole permitted report path. Write only that report;
do not write the other reviewer's path, the ledgers, or an adoption record.
