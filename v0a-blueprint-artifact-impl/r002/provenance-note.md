# Controller provenance note (not an issuer verdict)

Frozen r002 remains commit 5e56e4454f7b8ccb360d3e36245abc33318349bb,
manifest 6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5.
Do not use authoring working bytes as the candidate.

The implementer declared source edit-stable and the controller froze those bytes.
A subsequent report cited a later test-only revision as if it were part of that
freeze. A raw comparison shows one differing authoring file:
tests/test_blueprint_artifact.py. The later revision shortens astral-ID setup
through the existing helper and wraps the malformed-record loop in subTest so
multiple failures are printed in one rejected-code run. Those edits are not in
r002 and are not adopted. No production, fixture, boundary-test or registration
bytes differ. Preserve the later work as unadopted evidence; do not fold it into
the immutable candidate or create another correction round.

task-1-correction-report.md is retained at task root as the implementer's issued
report, but its final2 and four-subtest-RED statements do not identify r002 tests.
It is excluded from the cold handoff. This note does not rewrite its issuer's
report or claim an issuer retraction.

Applicable frozen r002 codec evidence is the four correction-final-codec-*
receipts named in coverage.md, not correction-final2-codec-*. Controller
comparison matched every one of the twelve packet blobs in all four applicable
snapshots and in correction-registration-write-final-r001-311. Both boundary
GREEN snapshots match the frozen boundary test, checker and all production;
their only differing packet file is an unexecuted earlier main codec test before
the explicit digest assertion. Broad acceptance, if both reviews are CLEAN,
will always use the complete frozen r002 overlay.

The first registered codec RED demonstrates the missing source slot; independent
r001 reviewer B separately demonstrated source/entry/key/action missing slots on
both interpreters. Frozen r002's GREEN tests execute all four required negatives
successfully. Do not present the later four-subtest RED as frozen-r002 test bytes.

Both fresh FIX reviewers were told this limitation before their verdicts.
No source or review identity was changed to resolve this provenance distinction.
