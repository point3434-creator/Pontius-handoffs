# Timing r002: local adoption

Date: 2026-09-09. Finalizer: Codex.
Controller authorization: "Let's adopt and commit if ready" following the r002
CLEAN / SOUND disposition and completed focused, cold-review and broad gates.

Adoption commit: beb84be566aa28029284bd35c526d33cd27af369.
Branch: codex/eval-panel-timing.
Reviewed candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968.
Parent: 9fce4bfba3acf1c34938aa47f37f9743e5011cea.
Exact reviewed and adopted tree: d26c3fb14959562a03b10e09fd746e317009d91b.
Manifest: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2.

Status: ADOPTED LOCALLY. I-01 is resolved on the adopted tree. Both cold reviews
are CLEAN / SOUND with no required corrections. The retained Python 3.14.6
focused gate passed 40 cases with zero skips; the post-review broad gate passed
583 cases with 10 optional SciPy skips, exit 0 and source_verified true.

Before adoption, the finalizer independently recomputed the manifest and all
16 dependency pins, verified both review digests and every closure-manifest
entry, and matched the actual retained broad-result digest. The staged tree
equaled the exact reviewed tree before committing. After committing, the tree
and sole parent were checked again and the adoption worktree was clean.
No source changes after review or additional test run were needed for this
byte-identical adoption. The existing test receipts remain bound to the review
candidate; tree equality carries that evidence to the adoption commit.

Automatic approval review rejected the attempted commit with auto-push because
the export to origin lacked sufficiently destination-specific authorization.
The rejected command did not run. The approved safer alternative made the
local commit with core.hooksPath overridden to an empty directory for that
command only. No persistent hook configuration was changed; no push occurred.
The handoff publication commit likewise disables its auto-push for that command.

Remote publication is pending explicit destination approval. Review refs remain
intact until the retirement predicate is satisfied by a verified remote archive.
The main checkout and its existing STATUS/journal changes remain untouched.
Earlier candidates, failed receipts and original rulings retain their identities.

This source adoption does not perform the retained capacity/preflight run or
the controller's measured resource decision required before design steps 4-7.
