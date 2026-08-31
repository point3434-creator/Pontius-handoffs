# No-work entry certificate addendum v1

2026-08-31. Read-only engineering refinement of engineer-environment-implementation-plan-v1.md; no implementation or payload authorized here. Exact generator SHA-256:3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.

Accept the narrower certificate. It removes the need for store-ancestry metadata or reference-validity caching from the first name-map design. Certify only an entry that has actually completed an ENABLED, top-level transfer with retained=False, returned the identical input object, and has empty authority_refs. All other entries remain pending for the existing transfer boundary. Every raw projection starts pending, even when its value resembles a certified value.

## Branch proof against14034-14083

The disabled-store early return14044 performs no analysis and cannot establish the certificate. An enabled call consumes work and reaches the value branches. Its existing-reference identity return14048 requires nonempty authority_refs and is excluded. The missing-reference branch replaces the input and retains the refusal obligation, so it cannot certify.

Every nested sequence/slice/maybe_unbound, mapping/mapping_keys or FlowValue-starred branch adds an update entry. Defaults, receiver and obligations do the same. Any nonempty updates dictionary causes dataclasses.replace at14073, returning a fresh FlowValue even when a child or empty tuple is unchanged. Therefore an identical return proves none of these update branches ran; empty maybe_unbound still fails certification. Every registration branch allocates and replaces with nonempty refs. A no-ref identical return therefore proves that neither nested rewriting nor registration remains in the current top-level operation.

This proof covers the exact existing function control flow, not a prediction from kind names. It avoids repeating a dozen field checks after every assignment. The implementation can retain the pre-call enabled flag and input reference, run the full transfer, then inspect result identity and its refs. Charge these actual new metadata/check operations. Review/test the proof whenever transfer changes; adding an in-place operation or another identity-return shortcut would require re-establishing it.

The certificate is exclusively for top-level retained=False name normalization. A qname with helper_provenance can be a no-work top-level value while requiring registration under retained=True. Recursive transfer never consults this entry certificate. Sensitive=True, namespace spelling, callable_scope/free-value metadata and mutable_collection_identity are not proofs of harmlessness; only current transfer behavior is being certified. All ordinary semantic consumers and cell writes still run.

## Ownership and invalidation

FlowValue fields are frozen at9018-9037. The certificate belongs to the immutable entry/value association. Semantic replacement performs full transfer again; delete/reinsert, copied raw projections and uncertain external entries cannot borrow a certificate from another equal-looking value. A structural fork or exact entry reuse may retain it. A changed merge candidate performs full transfer even if its output compares equal to an earlier value.

No-work certification makes no claim that any authority ID exists. It survives object-store fork, join and authority-only adoption, including18463/23026, without a lineage walk: the certified top-level operation never reads the object store. Preserve raw-projection invalidation at14453/18407/18471 and projection-only deletion18404. Context-independent certification does not authorize dropping pending names or any historical object/cell state.

All entries carrying refs remain pending and retain their real membership validation and missing-reference behavior. Rebuilt maybe_unbound/starred values remain pending. Disabled-origin entries remain pending until a later actual enabled transfer establishes the certificate; alternatively an explicit full-shape proof would be needed, which this first design intentionally omits. Every bound-name strong/weak cell write remains required even for a certified entry.

## Expected coverage and its limits

Gen06 diagnosis SHA-256:ff3a6a04e274215ce45c781039d60627a30f88d522150a502e9ec68dec0be1b5. It records65875 transfer-entry charges, including40200 optimized merge transfers and2238 fallback merge transfers. The selected492 merges contain79-82 projected names each. Avoiding repeated normalization of shared no-work entries directly targets that measured mechanism.

There are377 retained-reference validation units and795 recursive transfers, but neither is a count of uncertifiable top-level values: one call can validate several refs, recursion can be nested, and empty rebuilding branches can recurse zero times. Do not subtract these numbers from65875 or claim a percentage certified. The trace does not record value kinds or entry certificates.

A concrete eligible producer is registered helper alias installation17921: all8551 traced assignments call _flow_qname, whose12430-12435 result has no registration/update fields. Enabled full transfer returns that same qname, so those entries can be certified afterward. Their initial8551 transfers still execute; this proposal saves only later repeated joins/reuse. It does not remove alias construction, registered seeding, constructor traversal or generic update work. Scalar/unknown/unbound projections are plausible additional coverage, but no exact count is established.

The narrower certificate is consequently a sound simplification with plausible coverage, not a measured assurance that most65875 charges disappear or the corpus clears. Record actual certified/pending counts and complete-path cost in structural RED/GREEN. This can remove lineage complexity from the proposed design while retaining the AVL/order costs and explicit N*S ordered-demand no-go criteria.

## Required falsifiers before production acceptance

Include enabled plain and sensitive qnames; helper-provenance qnames at top level versus retained child use; empty and nonempty maybe_unbound/starred/sequence/mapping values; defaults/receiver/obligations; missing and present root refs; raw projection of a previously certified value; disabled-to-enabled transition; authority-only adoption; and unchanged certified names whose joined binding cells still need strong/weak reinstallation. Pair source-structure checks with public analyzer rows/blockers and independent harmless behavior, not only metadata assertions. No production edits, tests or performance claims follow from this note.
