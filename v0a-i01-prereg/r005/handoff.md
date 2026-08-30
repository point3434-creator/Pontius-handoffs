# Cold review: v0a-i01-prereg/r005

Candidate ref: `refs/heads/review/v0a-i01-prereg/r005`
Candidate commit: `98328440d4425fed1dbc7eb30b26b5f785709f05`
Manifest SHA-256: `d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17`
Base commit: `ca0b2e41bbf5d9fc1649de20379299331de6591a`
Tree: `f13e21e07721bb97ff4e6308229c724dd8ce16a0`
Tier: C specification review; no runtime implementation exists in this candidate.

The full commit and manifest bind identity; this path and the index only locate it.
The ref is local in D:/Pontius and its linked worktrees, not yet pushed.
Independently verify the exact candidate/base and blob-derived manifest. Read
candidate Git blobs, not mutable working files. Changed bytes or scope require
a new round. Never invoke a runtime, historical owner, or test from this packet.

## Scope

- STATUS.md
- docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md
- docs/workflow-amendment-2026-08-30.md

## Pinned inputs

At BASE: CLAUDE.md; docs/briefs/v0a-increment-1-brief.md (blob
8ef19c830eb929037c9cdd99e52cb0f0b56ddb28); governing ADRs and public APIs these
documents identify. The original base workflow remains retained; the controller
adopted the newer handoff structure captured in `inputs/workflow.md` at SHA-256
`c70581f35cc1b424a1734c9dbbdb17bea530622461225cd54ca23297c1db4e4a`. Its specific overrides are captured in
`inputs/controller-rulings.md` at SHA-256 `98b371e8a11bc4a0cea00c4cc41737ff4ca46652ccc4a98ae47db61874cc34f8` and the candidate amendment.
The adopted workflow capture is review input, not a modification included in this
evidence-repository candidate. The controller owns the separate primary edit.

## Review contract

Review the whole candidate against the brief and checklist v1: exact API feasibility,
action/clock/delivery boundaries, typed failure and replay contracts, public-ledger
accounting, hidden-card isolation, claims limits, and authority. No implementer
transcript, prior findings, disposition, or other reviewer's output is a cold input.
Do not read those files before issuing your independent verdict. No tests/owners or
candidate edits are requested; verification receipts are separate coordinator work.

CLEAN requires that no material finding survive verification. Every Critical or
Important finding binds to this pair, cites exact frozen locations, states a concrete
failing scenario, and gives the smallest correction. Return attributed findings to
your assigned `reviews/review-<NN>-<reviewer>.md`, and coordinate the verdict issuer's
single task-ledger append. A corrected finding/report is a new record, never overwrite.

The controller retired CodeRabbit and authorized the coherent bootstrap sequence;
do not resurrect those approval questions. Specific ceremonial-commit authorization
and any experiment invocation remain separate, ungranted gates.
