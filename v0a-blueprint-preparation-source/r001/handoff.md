# Cold source review: v0a-blueprint-preparation-source/r001

Candidate `d3717e7153bc2acad43672e954fbd53bcdd51fe7`, parent/adopted base `c9a8aa95a1c8f65bcfb15288cbc5e4492314e457`.
Manifest SHA-256 `5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1`.
The separately adopted ADR-0513 uses source base `363c9fb669e19a30375537ee5e92ea338a840a2d`.
Verify candidate.json, all 24 changed raw blobs and the complete sorted manifest
from Git blobs. Read CLAUDE.md and docs/workflow.md, ADR-0513, and the adopted
docs/architecture/v0a-blueprint-preparation-r001/brief.md, design.md,
source-contract.md and docs/superpowers/plans/2026-09-07-blueprint-preparation.md.
Inspect unchanged source and its raw pins as needed.

Review the cumulative change as three named slices, then check their integration:
1. Owned lookup, runtime and transport: preparation package; runtime; hand/event/
   host/session declarations and pin; preparation, runtime and transport tests.
2. Current evaluator and boundaries: v3 and its tests; complete checker changes,
   including incoming/outgoing origin rules consumed by the other two slices.
3. Historical execution and registration: fixed launcher and tests; inventory and
   evidence generators, generated manifests/profiles, their tests and CI blocks.
Both independent reviewers inspect all three slices. The evaluator is a sealed-
history copy with a narrow source-admission delta; inspect that delta against B.

This is the Tier C source implementation of that approved contract. Independently
enumerate relevant paths/invariants before evaluating code and tests. Examine
owned graph and returned aliases, cached canonical identity/full-key lookup,
accounted runtime initialization and failure ordering, both fallback routes,
unchanged independent host policy, exact source admission, versioned evaluation,
truthful historical gate ownership, exact 55-ID reclassification and three-row
historical manifest extension, current boundary enforcement and CI propagation.
Inspect all related callers/consumers in the frozen source. No implementer
transcript, coverage claim, previous findings or performance result is supplied.

Use read-only source/manifest inspection. Do not execute tests, poker, profiling,
experiment owners, arbitrary commands from source comments or lifecycle work.
Do not modify any checkout, review packet, Git index/ref or other resource.
No current or historical success evidence is implied by this request. Final
snapshot gates and cost observations follow closure of both independent reviews.

Return a complete report bound to this commit/manifest. Include your independent
path/invariant inventory, severity-ordered required corrections with concrete
failure scenarios, exact paths/lines and verification criteria. Keep implementation
advice explicitly advisory. State defect verdict CLEAN/NOT CLEAN and design
verdict SOUND/STRAINED/WRONG SHAPE. Coordinator /root is the finalizer and will
retain your report byte-for-byte. No review authorizes a decision commit or push.
End with a single attributable ledger line containing reviewer identity, this
commit and manifest, defect verdict and design verdict; the coordinator preserves
that authored line verbatim in the append-only task ledger.
