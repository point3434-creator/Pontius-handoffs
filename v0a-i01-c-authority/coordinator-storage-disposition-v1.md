# Coordinator disposition: bounded name-storage replacement

2026-08-31. Engineering decision within the existing C authority FIX. This is
not a cold verdict, capability approval, frozen candidate, or main-integration
authorization. Accepted A/B and the other three C paths remain preserved.

The exact predecessor is v19 generator
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.
Its completed evidence is backed up by handoff commit
b15edb4d748356389cf00fb825d0a10a9da78817. All original reviews and failures remain
immutable. Main remains d1ed3cbda6107d61ea8e77133871720af04970cd.

## Evidence and scope decision

Gen06 still fails ordinary generation under the unchanged 262144-unit cap.
The diagnostic proves that v19 saved 15780 units across the measured merge
operations; it did not close the corpus failure. Diagnostic report SHA-256:
ff3a6a04e274215ce45c781039d60627a30f88d522150a502e9ec68dec0be1b5.

The independent structural family demonstrates repeated ambient-name work in
all four zero-change comparisons. On each actual interpreter, all 24 semantic
expectations and 58 harmless runtime projections pass; structural RED is the
only failure. This is not a claim of a new public false negative. Plan SHA-256
969b3acb781cca11ccd10b26eddaab300a5af7a24b4199ae235136a68f4f62ef;
case-pack SHA-256 d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c;
report SHA-256 d33c6d08ceeef8ea9f34e93fc5f7104469dee08e643b87270bb8cbbe83c30e9b.
Coordinator receipt SHA-256
27eeb29362e5e4da1edd9faeb5e1a547269647afcdbff3be0d394f54695017b1
independently verifies the receipts, sources, oracles and ten cross-slot counters.

Accept the conditional storage design in
engineer-environment-implementation-plan-v1.md, SHA-256
07461b792b5d86cf8e3c02d43e4ed12fd3e14ee116cd4a141150ad5d3a72c6d7,
with the narrower certificate below replacing its store-lineage optimization.
An isolated storage prototype may proceed. Production integration of that
prototype requires the coordinator to inspect its compatibility results first.
This replaces repeated name reconstruction; it does not expand the supported
Python language or replace the object/cell authority model.

## Narrow certificate

The name entry may record a reusable no-work proof only after an actual,
completed, enabled, top-level transfer with retained=False. The returned value
must be the identical input object, have no authority_refs, and have no
helper_provenance. The last exclusion also removes the retained-mode hazard.
The exact transfer implementation must continue to support the branch proof:
recursive reconstruction uses replace; registration changes the object or adds
refs; unresolved-reference handling rebuilds the value; disabled early return
cannot certify. A future transfer change requires reassessing this proof.

Every ref-bearing value, rebuilt value, disabled-origin value, and raw projection
remains pending. Raw installation clears certification even if it installs the
same object. Pending entries receive full transfer at the next existing transfer
boundary, never at a newly invented eager-read boundary. A certificate says
nothing about safe consumption: sensitive qnames may still require blockers.
It cannot bypass recursion, retained transfers, consumer analysis or cell writes.

No object-store ancestry graph or root-reference certificate is included in this
increment. The restricted certificate makes no store-membership claim, so it can
survive authority adoption; pending live-authority entries cannot borrow that
proof. Preserve all existing constructor/adoption timing and full fallback paths.
Initial alias transfers remain; their aggregate later savings are unmeasured.
The independent branch-partition inspection is recorded in
tests-checks/name-environment-transfer-proof-v1.md, SHA-256
21f0b8ca53d113a05e2121c2dc6b2162d1a863d958e2663d88af592142090478.

## Required implementation properties

- Persistent AVL name lookup/update and immutable versions; no first-write full
  dictionary copy. Charge allocations, node/reference copies, comparisons,
  traversals, history discovery, cache work and fallback work honestly.
- Exact legacy order recipes, including set-union order, deletion/reinsertion,
  and existing first-matching-alias behavior. Ordered reads may cost N times S;
  deferred work must be included in measurement. Partial order caches cannot
  survive a failed materialization.
- Keep all full transfers for changed/pending entries, every object/cell join,
  and every participating strong/weak cell write. Preserve original ordered
  fallback for overlapping or missing cells. Opaque numeric IDs may change;
  alias structure, distinct activations, source points and alternatives may not.
- The four identity-None alias-search guards may avoid searches that cannot
  match. Non-None searches and other full traversals retain their behavior.
- Route semantic assignment/deletion separately from projection and adoption.
  Preserve raw hydration, parameter injection, class/helper completion and the
  existing clear/update overlay-versus-replacement distinction.
- Retire v19's planner only when the new merge replaces it. Retain the shared
  cell-write helper, v15-v18 corrections, all five caps and all existing tests.

## Prototype and continuation gates

First verify the storage primitive against ordinary Python dictionaries and the
actual legacy set-union algorithm. Include retained fork snapshots, overwrite,
delete/reinsert, unrelated roots, repeated ordered reads, failed materialization,
and terminal ordered reads after multiple merges. Use finite deterministic
operation schedules on 3.11.15 first, then 3.14.6; supplementary order checks use
explicit per-child hash seeds 0, 1 and 17. No host configuration is changed.

Then integrate only the named storage/projection/merge seams in the isolated
worktree and run the frozen public family, existing design53, matrix192/212 and
the required supplemental authority controls. Adapt structural counters to the
actual representation; never label an O(1) fork a full copy by its API name, and
never omit terminal order materialization from the new cost report. Only ordinary
corpus generation under the unchanged caps can establish the corpus leg.

If exact ordering, honest lookup/history costs, or normalization proof make this
replacement ineffective, record that result and reassess. Do not add another
independent map rewrite or raise a cap to rescue it. A/B, generated outputs,
controller documents and preserved paths remain outside prototype edits.

Final order remains corpus/census and focused verification, a new frozen ref and
manifest, two fresh mutually blind cold reviews, the permitted CPU wall, then
candidate-specific controller authorization for Claude's finalization.
