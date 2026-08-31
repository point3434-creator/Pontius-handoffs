# Coordinator design reassessment: helper provenance

This records engineering iteration within the still-open C correction; it is not a
cold verdict, a new source candidate, or acceptance. Frozen r008 remains parked.
The scope stays the same two analyzer/test files plus ordinary generated inventory;
accepted A/B, other C boundaries and CI, baseline and capability authority are preserved.

The repeated misses have a shared structural explanation. Historical registry discovery
previously acted as independent callable authority. The first repair added identity proof
but coupled it to old value/return semantics and used invalidation scopes wider than the
actual owner. The second repair restored those semantics and scopes, yet call admission
still considered explicitly supplied arguments while sensitivity pruning skipped a helper
whose only action was mutating an implicitly supplied owner. Defaults, closure cells and
bound receivers were represented on separate paths. More name- or syntax-specific checks
would preserve that split and invite another residual.

Root adopts the bounded redesign in c-provenance-worker-v3-stage0.md: one effective
invocation builder and one effect-admission path, reusing the existing argument binder
and source-ordered resolver. This replaces the incomplete explicit-argument certificate;
it is not another special case for one default spelling. Preserve independent abstract
values, exact captured callee/default/receiver state, late closure lookup, invalid-call
nonexecution, reached effect/exception order and existing finite limits. Unsupported
behavior must refuse. No generic heap or broader interpreter is introduced.

The replacement boundary is helper invocation admission/effects, not the generator's
transaction/Git engine or the whole30k-line test corpus. A full-tool rewrite would mix
unrelated accepted contracts into this correction without addressing the demonstrated
cause more directly. Reusing the existing flow is less duplicated semantics but risks
recursive work, changed completion paths and false owner invalidation. Those risks are
checked by the old deep-budget/exception/return suite, opposite read/dormant/override
controls, real corpus row/edge preservation and fresh cold review after freeze.

Independent root pure projections already reproduce the omitted-input defect in eight
forms: positional/posonly/keyword-only defaults, free global/local/receiver owners,
container defaults and mutation before a caught raise. A bound-method mutation already
refuses; lawful controls include unchanged fields, unused defaults, explicit overrides
and dormant bodies. These are discovery evidence, not an exhaustive language claim.
Worker matrices add saved-callable/default capture, nested calls, invalid bindings and
opposite exception order. The final frozen coverage claim must name actual exercised
cases, exclusions and a falsifier rather than treating green examples as completeness.

No census expectation refresh or final freeze is authorized by this note alone. Require
integrated GREEN, explained source-bound census deltas, two independent cold contexts,
and the permitted acceptance wall. Main finalization remains Claude's checkpoint after
candidate-specific controller authorization.
