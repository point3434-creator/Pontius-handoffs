# Deferred FIX coverage claim: raw source identity

Read only after the cold reviewer's initial invariant/path inventory.

Fix input: Reviewer B/C1 on r001, candidate
21474e3d5b105c1709205df1eb5543417abb5a0a, manifest
ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9.
Violated invariant: reported source commit/manifest must describe the raw
committed blobs whose matching bytes execute, not a substituted Git view.

Discovery: read every Git identity operation named in r001 design.md and the
installed Git replacement-object documentation, then reproduce replacement
semantics in a synthetic bare repository with two text-only commits. No project
source, test, hand or owner was run. This establishes the metadata mechanism,
not implementation of the proposed adapter or its future refusal control.

Affected sites: initial HEAD/commit/tree resolution, inherited-base comparison,
package inventory, source-blob reads, and final HEAD/source revalidation. The
same invariant also excludes archive attribute transformations and checkout
normalization as raw-byte oracles. No other data/host/policy contract changes.

Planned correction: require --no-replace-objects on every initial/final identity
command after environment scrubbing; derive inventory from raw ls-tree objects
and source bytes from cat-file blob IDs. Do not depend on a scrubbed caller env
flag or an archive/filtered view. The original isolated-clone base is unchanged.

Mandatory future controls: actual CLI with original HEAD O, replacement commit R,
and changed adapter/scenario checkout bytes must refuse before host/trace/success;
also cover a replaced source blob. Ref presence without raw-byte drift is not by
itself the identifying failure. Confirm final revalidation uses the same mode.
The existing source/import and output-negative controls remain mandatory.

Exercised now: synthetic ordinary-read substitution versus raw-read recovery.
Unexercised: every future adapter control; no implementation exists yet.
Limits: no hostile executable Git, object-store corruption, SHA collision,
concurrent-writer, filesystem-completeness or universal Git-hardening proof.
The design remains within its accidental source/import-drift threat model.

Falsifier: an admitted proposed identity/read path can still use substituted,
normalized or archive-transformed bytes while reporting the requested raw commit,
or the required CLI control can execute a hand before detecting raw-byte drift.

Mapping: r001's three document paths become v0a-hand-adapter-r002/* in r002.
Ignoring that version/path update, only design.md's Git identity mechanism and
its mandatory replacement controls change. Brief and opening scope are unchanged.
The original candidate, reports, working draft and metadata control remain retained.
