# Cold review: v0a-blueprint-preparation-design/r001

Candidate `ddf652d00e68a84e1eef03d5bd4df37c5a022b79`; base `363c9fb669e19a30375537ee5e92ea338a840a2d`.
Manifest SHA-256 `e68bf5eb2bf2338c9217717a960d79a5624abdb62b09c0914609fa6a3fc35aa4`.
Read candidate.json and verify all six changed raw blobs and the sorted manifest.
Read CLAUDE.md, docs/workflow.md, ADR-0512 and the candidate's ADR-0513, brief,
design, source contract and implementation plan. Inspect base source as needed.

This is a Tier C documentation-only source-opening proposal. Review whether its
ownership, canonical digest, complete-key lookup, real runtime accounting,
independent host oracle, exact source opening and old/current test routing form a
coherent implementable contract. Confirm exact exception pins and preservation of
sealed history. No source implementation or speed claim is being submitted.

Initial review: independently enumerate the relevant requirements and seams.
No implementer coverage claim or another reviewer's findings are supplied.
Do not execute tests, poker, profiles or experiment owners. Read-only source
inspection and manifest/pin calculations are permitted. Do not modify candidate.

Give severity-ordered must-fix findings with exact file/line and requirement.
Distinguish advisory choices. State defect verdict CLEAN/NOT CLEAN and required
design verdict SOUND/STRAINED/WRONG SHAPE. Bind both to commit and manifest.
Return your complete attributed report to the coordinator; permanent storage is
reviews/review-<name>.md. Coordinator /root is finalizer. No review authorizes
source implementation or a decision commit.
