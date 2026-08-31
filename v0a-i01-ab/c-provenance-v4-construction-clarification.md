# Pre-edit construction clarification: annotation effects

This supplements the v4 Stage0 and adopted design. The frozen r009 pair remains
8d240db477b8c141e6142e055dbfbedc75c6a2f8 /
4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51.
No new source or capability surface is authorized.

The callable-construction inventory includes decorators, defaults and annotations.
Source inspection found that the current function-definition flow visits the first
two but neither evaluates annotations nor gives a relevant annotation-effect
refusal. Root seeding alone cannot establish execution admission. At this point
the annotation-local-mutator case is a hypothesis, not a reproduced defect.
Demonstrate RED against r009 before changing production for this case.

Adopt the existing fail-closed rule at this unsupported boundary: relevant
unresolved annotation effects must explicitly refuse. Do not add a general
annotation interpreter or claim that merely constructing a callable executes an
annotation on every supported interpreter. Use actual per-slot harmless runtime
projections to establish execution/deferment and never execute sensitive fixture
bodies. A portable conservative refusal can be appropriate even when one slot
defers the effect; state that limitation instead of pretending it ran.

Reuse the bounded provenance/effect mechanism. Do not speculatively mutate live
analysis state. Preserve ordinary literal/bare type annotations, readonly controls,
source ordering, finite budgets and the old analyzer contracts. The correction
remains within generator and its contract suite; root owns generated pair, measured
census, final focused tests, new freeze and two independent cold reviews.
