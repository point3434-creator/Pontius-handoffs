# Cold design review: v0a-hand-adapter-design/r003

Round kind: FIX. Tier C. Two fresh independent substantive design reviews.
Ref: refs/heads/review/v0a-hand-adapter-design/r003.
Commit: 02e24f143b8df4b2f03e8a94c58ab57905a8b2b6.
Manifest SHA-256: f730799182d3f3eda2d9efa273048b2eaf28ceeb4274ea7525df95426ca679b1.
Base: 7a387e995e3b37232d2379332927247a4d49c64e.
Tree: bd1cd2f83612aacac9d1de1c8e0afd673a86579c.
Object repository: D:/Pontius/tmp/v0a-hand-adapter-design-r001/authoring.
Finalizer: Codex; separate controller authorization is required for adoption.

## Requirements and complete scope

The approved brief/design task is a one-hand file adapter: an existing saved
blueprint and scripted-hand JSON file go through the existing ReplayHost,
independent persisted-trace verification, and a concise actions/settlement
summary. Selecting inputs requires no Python edits. Existing runtime, codec,
driver and historical evidence stay unchanged. No implementation or invocation
is authorized. The candidate has exactly three proposed document additions:

- docs/architecture/v0a-hand-adapter-r002/brief.md
- docs/architecture/v0a-hand-adapter-r002/design.md
- docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md

The r002 document edition labels/paths are intentionally retained. r003 names
the new frozen snapshot, whose only delta from r002 is one removed terminal LF
per document. The controller explicitly approved this one-time third-candidate
formatting replacement and two fresh reviews; authorization.md records that
narrow scope. The brief's original budget is otherwise unchanged. No fourth
candidate, design expansion or source implementation is authorized.

Read frozen raw blobs, not mutable working files. Recompute commit/parent/tree,
exact changed-path scope, raw file digests, whole-row-sorted LF manifest and the
source-opening proposal's six base blob pins. Verify the exact three-byte delta
from r002 as well as the complete substantive design. Use raw Git object mode.

Base governing inputs: CLAUDE.md; docs/workflow.md and its 2026-08-30 amendment;
PROJECT.md's charter/evidence protocol; ROADMAP.md's blueprint section;
ADR-0485, ADR-0486 and ADR-0489 through ADR-0492. Read directly referenced base
contracts as needed, not retained scientific results or implementer discussions.

Assess feasibility against actual base source: src/pontius/v0a/{model,runtime,
replay,trace}.py, src/pontius/blueprint_artifact/codec.py,
src/pontius/immutable_blueprint.py, src/pontius/holdem_cards.py,
tools/v0a_rehearsal_driver.py, the six proposed registration files and directly
relevant tests. Proposed documents are not authority to run or modify these.

## FIX inputs and deferred coverage

Prior substantive candidate: 21474e3d5b105c1709205df1eb5543417abb5a0a; manifest
ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9.
Required input is Reviewer B/C1 at ../../review-b/review.md, SHA-256
19e85c4e99a2928de87d9b01f7d4bafaa6a90b6cd9ee9614d2496ab225e141ab.
That original finding report and the prior three raw blobs are permitted FIX
inputs. No current sibling review or prior Reviewer A report is input.

Unreviewed r002 candidate: 1c2fde7bdb9359436f9c2ff260e324a08439752b; manifest
f2c8c9f8c292585623b06a7f623e6b31f6202199f66c82afd78d765bfcab1b1a.
Its raw blobs are permitted for independent formatting comparison. r002 never
received substantive reviews, so this is not qualified mechanical verification
under Stage 4 and no earlier verdict transfers to r003.

Before opening coverage.md, record your own invariant and affected-path inventory
from the contracts, original finding and frozen design. Then read coverage.md,
SHA-256 051adc62d56fd25a3795a0b76b257abfd2ba1f11a5031fd25025d7d78a356e3d,
verify that digest and compare its discovery, boundaries, limits and falsifier
with your independent inventory. Future CLI controls are prescribed, not run.

Challenge all three documents: raw source/input and import bindings, literal-card
adaptation and host-only full-deal separation, independent acceptance/output
conjunction, failure retention, ground truth, finite coverage and proportionality,
actual registration dependencies and scope. Required findings need a concrete
contradiction or failure scenario and a verifiable correction criterion. Distinguish
coverage gaps from executed product failures. Optional preferences are observations.

## Output and authority limits

Return your original attributed review as the final answer. Its first line is
your one-line task verdict bound to this commit and manifest. The host retains
your original report and verbatim first line without rewriting. Include
Spec/Quality PASS or FAIL, C/I/M counts, CLEAN only with no unresolved required
correction, Design SOUND/STRAINED/WRONG SHAPE with reasons, evidence and limits.
Record your initial inventory and subsequent deferred comparison in the report.
Review all permitted scope; roughly two pages is a target, not a limit on findings.

Do not read controller transcripts/progress or other reports. Do not edit files,
index, HEAD or refs; import project code; run tests, hands or owners; install
dependencies; call the network; or spawn agents. Read-only Git/stdlib metadata
calculations are permitted. Git is C:/Program Files/Git/cmd/git.exe; command-local
safe.directory for this exact clone is allowed if needed, never global edits.
No runtime acceptance, source seal, adoption or invocation is claimed here.
