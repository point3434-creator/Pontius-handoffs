# Deferred FIX coverage claim: raw identity and formatting replacement

Read only after the reviewer's independent invariant/affected-path inventory.

Substantive FIX input: Reviewer B/C1 on r001, candidate
21474e3d5b105c1709205df1eb5543417abb5a0a, manifest
ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9.
The invariant is that reported source identities describe raw committed blobs
whose matching bytes execute, not a substituted Git view.

Discovery: inventory every Git identity operation named in the original design;
read installed Git replacement-object documentation; reproduce replacement
semantics with two text-only commits in a synthetic bare repository. No project
source, test, hand or owner ran. This exercises metadata mechanics only.

Affected paths: initial HEAD/commit/tree resolution, inherited-base comparison,
package inventory, source-blob reads, and final HEAD/source revalidation. The
same invariant excludes archive-attribute transformations and checkout
normalization as raw-byte oracles. No schema, host, policy or trace change.

The design now requires --no-replace-objects on every initial/final identity
command after environment scrubbing. Inventories use raw ls-tree objects;
source reads use cat-file blob IDs. A scrubbed caller flag or filtered/archive
view cannot establish identity. Required future real-CLI controls cover commit
and source-blob replacement with original HEAD but substituted checkout bytes;
refusal must precede host, trace or success. Final revalidation uses raw mode.
Replacement-ref presence without raw-byte drift is not itself the failure.

The future adapter is not implemented: none of its acceptance controls has run.
No hostile Git executable, object-store corruption, SHA collision, concurrent
writer, universal filesystem or Git-hardening claim is made. The target remains
accidental checkout/import drift. A falsifier is any admitted identity path
using substituted/normalized/archive-transformed bytes while reporting the raw
commit, or a required mismatch being detected only after the hand starts.

Formatting input: r002 candidate
1c2fde7bdb9359436f9c2ff260e324a08439752b, manifest
f2c8c9f8c292585623b06a7f623e6b31f6202199f66c82afd78d765bfcab1b1a,
contains one extra terminal LF in each of the three proposed documents.
Discovery was direct raw-byte inspection and git diff --check at each EOF.
r003 removes only those three LF bytes, with no rename, wording or scope change.
The documents retain their r002 edition labels; r003 is the replacement snapshot.
The controller explicitly approved this one-time budget extension. Earlier
frozen objects, packets, working files and original reviews remain untouched.

Check all three blobs against r002[:-1], recompute raw object/manifest identity,
verify six base pins and run git diff --check before freeze and after extraction.
Any other changed byte/path or content meaning falsifies formatting-only scope.
Two fresh substantive reviews are still required; no old verdict is transferred.
