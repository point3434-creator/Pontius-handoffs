# Pending authorization: v0a-blueprint-artifact-open/r001

This is a request, not a record of user approval.

Candidate: `964ae18a64eccc595526525536d0e53e02293b83`.
Manifest SHA-256: `a6daf28c7bba5d7c531b39d31ea4f2e09c292339996a73baec0edb5bd523da1b`.
Base: `7ee314b443e10896e87a2e194f24eddda31ff77d`.

## Exact requested actions

1. Publish this frozen candidate on
   `refs/heads/review/v0a-blueprint-artifact-open/r001` in
   `https://github.com/point3434-creator/Pontius.git`.
   Publish its five-document adoption packet, identities, issued review, checks
   and dispositions under `v0a-blueprint-artifact-open/r001/` in
   `https://github.com/point3434-creator/Pontius-handoffs.git`, with routine
   navigation and append-only task/program ledger updates.
   This sends internal ADR/design and review material to those GitHub
   repositories; it does not publish any retained experiment payload.
2. After the metadata review is CLEAN, the exact frozen candidate's acceptance
   checks pass, and publication is verified, make the single ceremonial commit
   "Open the portable blueprint artifact source round" on Pontius master from
   the unchanged base, with exactly the five candidate files, and immediately
   push it to origin. Preserve and retire the review ref only under the existing
   archive/reachability predicate. No force push, history rewrite, new candidate
   bytes or different authority is included.

The five files are:

- `docs/decisions/ADR-0490-open-the-portable-blueprint-artifact-source-round.md`.
- Generated `STATUS.md`.
- `docs/architecture/v0a-blueprint-artifact-r002/design.md`.
- `docs/architecture/v0a-blueprint-artifact-r002/source-opening-draft.md`.
- `docs/architecture/v0a-blueprint-artifact-r002/coverage.md`.

The three r002 documents stay byte-identical to their reviewed candidate.
The decision activates only that contract's bounded prospective codec source
opening and its six exact registration exceptions. It does not implement code
in the adoption commit, source-seal a codec, authorize an operational/rehearsal
run, change the sealed runtime, or reopen any parked lane.

If the candidate, base or approved scope changes, return for authorization;
do not transfer an approval to replacement bytes.
