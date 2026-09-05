# Adoption result: v0a-blueprint-artifact-open/r001

Issued 2026-09-05 by the Codex controller after observed execution.

## Outcome

ADOPTED AND PUSHED. ADR-0490 opens the bounded portable-blueprint codec source
round from the exact independently reviewed r002 design. It does not implement
or source-seal the codec and grants no operating or rehearsal authority.

- Decision commit: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`.
- Title: "Open the portable blueprint artifact source round".
- Parent: `7ee314b443e10896e87a2e194f24eddda31ff77d`.
- Tree: `5f7d7ec8b289db58dc84ab2e0d5f168254b62dd0`.
- Reviewed candidate: `964ae18a64eccc595526525536d0e53e02293b83`.
- Manifest SHA-256:
  `a6daf28c7bba5d7c531b39d31ea4f2e09c292339996a73baec0edb5bd523da1b`.

The committed tree is exactly the reviewed candidate's tree. Only ADR-0490,
generated STATUS and the three byte-identical r002 design documents changed.
Both local master and origin/master resolve to the decision commit.

## Review, authorization and verification

The independent Tier A review remains CLEAN, Spec PASS, Quality PASS,
C/I/M 0/0/0 and SOUND; its SHA-256 remains
`3c6657bc44972d59fe064472afd840d7e8cd42105146806297c20ca8b30c5811`.
The user's explicit "Yes" to both exact publication/adoption actions is recorded
in authorization-record.md. The prior hold and request remain historical inputs,
not current blockers and not records to overwrite.

Fresh precommit checks passed on CPython 3.11.15 first, then 3.14.6. After the
commit, two new D-local snapshots ran the same unchanged metadata scope:
the status generator check and all 12 status tests passed on each interpreter,
in 0.207s and 0.217s respectively. Both snapshots remained clean. The exact
executables, isolated environments, argv, provenance and exits are in
checks/postcommit-acceptance.json. No poker-runtime or scientific payload ran.

## Publication and preservation

Initial permanent packet publication:
`d69bd0f7d896b67c218a150107613d02b325c8f6`, verified on Pontius-handoffs
main before the decision commit. The packet contains the five documents,
manifest, candidate, independent review, issuer-authored task-ledger line,
authority records and focused/post-CLEAN/precommit checks. Later integration
receipts and this result are appended separately; no issued report was edited.

The original candidate was pushed and verified under
`archive/v0a-blueprint-artifact-open/r001` before retiring its matching
review ref. The candidate remains recoverable by its original commit and
archive ref. No file or other review ref was deleted; old r001/r002 design
packets, failed history and prior authorization-hold records remain unchanged.

Primary tracked tree and index are clean. Existing unrelated untracked files
in both repositories were preserved. The final coordination update records
this result in navigation and appends one program-disposition line for r001.

## Active next and unchanged limits

Implement only the adopted two-operation codec, two tests, two JSON fixtures
and six exact registration exceptions, within the reviewed budgets and stop
rules. Preserve the sealed runtime and require both Tier C implementation
reviews and the reviewed real-consumer acceptance before any source seal.

This turn ends at adoption. No codec/test/registration/CI implementation has
started. Operational runs, strategy research, H32, campaign, compiled work,
Gate 13 and analyzer repair remain parked. No strength or capacity result is
claimed.
