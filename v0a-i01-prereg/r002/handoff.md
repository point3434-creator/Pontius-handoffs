# Increment-one preregistration: frozen review handoff r2

Candidate ref: `refs/heads/review/v0a-increment-1-prereg-r2`

Candidate commit: `119411fda2376d61d9ff310bada71f25aa64de70`

Manifest SHA-256: `da3c4ad5290a49f9d6e600b61e3190047ca6221394a4fc4ad06e40af727d799c`

Base: `ca0b2e41bbf5d9fc1649de20379299331de6591a`

Tree: `c7630b5a84b4ab694c7f04469007b9ca4640d024`

The ref is local in D:/Pontius and its linked worktrees. It has not been pushed.
Do not review mutable working files or an implementer conversation. Read the
candidate's git blobs and independently recompute the manifest from every path
changed against its parent, using docs/workflow.md's blob-derived convention.
Any changed byte requires a new round and a fresh ref; r1 and r2 stay immutable.

Scope is exactly:

- `STATUS.md`
- `docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md`

Inputs: the base commit's `docs/briefs/v0a-increment-1-brief.md`,
`docs/workflow.md` checklist v1, `CLAUDE.md`, and the governing ADRs and sealed
APIs those documents identify. This is a source-contract preregistration review,
not a runtime execution or a claim of experimental authority.

Review the entire candidate against the brief. Every Critical/Important finding
must bind to the manifest, cite precise locations, and give a concrete failing
scenario. CLEAN requires that no material finding survives verification. Do not
implement fixes or invoke historical owners. Return an attributed findings
document with the commit/manifest pair; serialize the verdict issuer's single
progress.md ledger append with the coordinator.
