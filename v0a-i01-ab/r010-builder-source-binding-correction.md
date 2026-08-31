# r010 builder source-binding correction

The first read-only preflight refused before any freeze. Its receipt/log are
abc-provenance-v4-r010-preflight01-receipt.json and matching .txt. The tested
snapshot overlays only the declared 17 paths onto exact base d1ed3cbd. Untouched
support/corpus paths come from that base's stored Git blobs, not the working
checkout's bytes. v1 incorrectly compared those census pins to the latter.

tools/generate_dependency_baseline.py illustrates the category: worktree SHA
 e442265d4526877bd867f59fc2bcea2685a946debe0c1851156212a616a9ab31
contains 2,229 checkout CRLF endings. The snapshot, base blob and census all bind
690845a3be276057196fbf86e5c795093c15bb3de54ab0bf413ea5529f8f9397.
Removing CR in CRLF solely for this diagnosis reproduces the base bytes. No
working, sealed, snapshot or receipt file was normalized or rewritten.

v2 uses one candidate-source digest resolver for both census bound inputs and
the complete corpus: overlay paths compare to the exact worktree bytes that will
be frozen; all other paths compare to BASE:path Git blob bytes. Both also compare
to the actually executed snapshot bytes. The two populations follow prepare()'s
source rule. This strengthens the relevant binding rather than accepting arbitrary
line-ending normalization as identity. All other checks, receipt counts, source
pins, preservation and freeze ordering remain unchanged. v1 and its issued note
remain immutable. No production code, final focused source, or test expectations
changed in this correction. The new full validate result must precede freeze.

v2 SHA256 353f01f4111a0a298c20417a1c4fcef1a7b4ae9c553c32b621b57f5a2c076c34
