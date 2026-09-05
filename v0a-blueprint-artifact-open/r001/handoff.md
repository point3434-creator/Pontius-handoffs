# v0a-blueprint-artifact-open/r001: adoption metadata review

Tier A; NEW-SURFACE; finalizer and ledger owner: Codex controller.

## Candidate and inputs

- Candidate: `964ae18a64eccc595526525536d0e53e02293b83`.
- Manifest SHA-256: `a6daf28c7bba5d7c531b39d31ea4f2e09c292339996a73baec0edb5bd523da1b`.
- Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`.
- Ref: `refs/heads/review/v0a-blueprint-artifact-open/r001`.
- Local object repository:
  `D:/Pontius/tmp/v0a-blueprint-artifact-open-r001/build-snapshot`.

The candidate changes exactly five documents: new ADR-0490, generated STATUS,
and the three exact reviewed r002 files. There are no implementation changes.

Binding source input is the reviewed design candidate
`a552f6f34efe10155a702fd09a03bcc70802a369`, manifest
`67abe320f73b8edfab60a93511f31eac62d0fac0279cdef712acda91fcf7aced`.
Its three blobs are copied unchanged into the adoption candidate. Original
object repository: `D:/Pontius/tmp/v0a-blueprint-artifact-design-r002/freeze-snapshot`.
Permanent design packet: `D:/Pontius-handoffs/v0a-blueprint-artifact-design/r002/`,
at handoff commit `07d3cf2bea65d6532cfd8d08d7195714a17eefdd`.
The issued Tier C reviews and report-format clarification are prior inputs,
not reviews of this new metadata candidate.

## Independent check

Check raw frozen blobs and independently recompute the five-row digest-first
manifest. Read CLAUDE.md, relevant workflow Tier A/Stage 5 rules, ADR-0489,
the exact reviewed design and source-opening proposal, and ADR-0490/STATUS.

Review faithful incorporation only: the source opening adopts the exact reviewed
r002 contract and six pinned registration exceptions, without broadening runtime,
scientific, invocation or historical authority. Confirm the copied draft wording
is explicitly dispositioned, bounds and stop rules remain, old briefs and source
are untouched, and STATUS is the unchanged generator's output. Do not redesign
the accepted codec, implement it, or re-run Tier C design review as this light
metadata pass. Report any actual inconsistency; do not accept an implementer
claim as its own verification.

The focused metadata scope is the status generator check and
`tests/test_status_generation.py` (12 tests), floor 3.11.15 then 3.14.6.
See focused-checks.md for receipts. If executing checks, use only a fresh
D-local snapshot, documented exact interpreters, -B -P, snapshot/src PYTHONPATH
and a scrubbed environment; never execute from the primary checkout.

## Output and authority boundary

Write one new issued report at
`D:/Pontius/tmp/v0a-blueprint-artifact-open-r001/review.md`, using apply_patch.
Bind the exact candidate/manifest pair; state CLEAN or NOT READY, Spec/Quality
PASS or FAIL, Critical/Important/Minor counts, and SOUND/STRAINED/WRONG SHAPE.
Name concrete required corrections and their verification if any.
LF-only, no BOM, no trailing whitespace, one final LF; keep prose at 100 columns.
Do not alter source, candidate, primary checkout/index/HEAD, prior reports,
handoff repository, or ledger. Do not delegate. Review does not grant commit
authorization. The controller will run post-CLEAN acceptance and obtain
per-candidate authorization before any decision commit.
