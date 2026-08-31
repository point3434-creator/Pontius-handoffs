# Scope correction to the released authority-transfer test expectations

This corrects classification in tests-release-v2.md and the interpretation of
tests-checks/release-v2-proof.json. Their issued bytes, test file, patch and raw
logs remain immutable. No test was edited or rerun, and no replacement production
source was inspected during this read-only audit.

Release test SHA-256:
c7f8d1ada3cdddc413f5074133cdbf2203ae9f62dfbb06798cddb984b1cb237f.
Original matrix proof SHA-256:
3094815a0a0006df09c9c33e08e092664f1c68b4b99d3df882aa6fa15511f620.

## Correction

The 54 observed assertions are real test failures, but I overclaimed that every
clean expectation was a binding product requirement. Fifteen runtime-lawful
schedules cross an effective-result precision boundary that the acceptance
expressly permits to refuse. They must be treated as permitted-refusal cases.
The pure oracle establishes Python behavior, not a requirement that the static
analyzer resolve every transferred callable sufficiently to prove that behavior.

The binding RED count is therefore 39: the unchanged 38 missing unsafe blockers
plus one refusal after proved decorator nonexecution. The other 15 failures
demonstrate optional precision, not additional required defects. Of 176 schedules,
the corrected expectation categories are 80 required refusal, 81 required clean,
and 15 permitted refusal. All raw recorded outcomes remain valid. No claim that
the unchanged v2 assertions now pass is made; the integrating owner must explicitly
reconcile these fifteen assertions in a later version before treating the suite
as a binding GREEN gate.

## Exact fifteen permitted-refusal case IDs

In family capture-route-execution:

- default/return/readonly
- default/return/raise-before
- default/returned-nest/readonly
- default/returned-nest/raise-before
- default/flat-store/readonly
- default/flat-store/raise-before
- cell/return/readonly
- cell/return/raise-before
- cell/returned-nest/readonly
- cell/returned-nest/raise-before
- cell/flat-store/readonly
- cell/flat-store/raise-before

In family live-cells-and-activations:

- cell/False/callback/False
- cell/False/(callback,)[0]/False
- cell/False/{"cb": callback}["cb"]/False

The six readonly transfer cases and three downward cell-rebind cases have exact
oracle trace [body, sink], result fixed. The six raise-before transfer cases have
trace [body, caught, sink], result fixed, with write proved absent. On both slots,
all fifteen public results have argv [] and explicit blockers
"helper namespace escape is dynamically unresolved", followed by
"helper namespace identity was mutated". The first blocker is an explicit
unresolved-proof refusal. The second is not independent runtime evidence that a
write occurred; no such occurrence is claimed by this addendum.

For return/returned-nest, the effective callback passes through a local function
return (and, for returned-nest, a literal mapping/tuple projection). For flat-store,
it passes through append then indexed extraction. For the last three, the
callback is returned while the cell still contains ReviewTests, then the cell
is rebound to None before invocation. All are safe in the harmless runtime
projection, but retaining unresolved authority and refusing its consumption
meets the existing fallback instead of requiring exact callable-result execution.

The frozen acceptance explicitly permits unsupported effective shapes and says
forwarding/escape must preserve OR explicitly refuse relevant authority. It also
states that no general callback interpreter or new capability support is required.
Old test_callable_authority_escape_is_independent_of_incidental_owner_loads
(source line 21138) requires unsafe returned-callback refusals, not successful
readonly result resolution. Old test_callable_authority_native_storage_retains_
without_invoking (21459) requires dormant storage to remain clean and consumed
mutators to refuse; it does not establish consumed readonly append precision.
Old direct/forwarded readonly and raise-before controls (21187, 21248, 21634)
remain required unchanged, but do not imply closure of mandatory support across
every additional result-transfer composition. My release summary treated that
implication as established when it was not.

## One required clean case among the sixteen

Family ordered-class-binding:
construction-failure/decorator/True.

The decorators are direct local names, with @callback above @abort. abort
unconditionally raises the literal ValueError before the outer callback can be
applied. The exception is caught. The recorded oracle is exactly
[abort, caught, sink], result fixed, with body and write absent. Both public
results already retain argv [[-m, fixed]], but add
"helper namespace decorator effects are dynamically unresolved" at line 17.

Clean is required here because the failure and remaining application order are
proved in the already-supported construction path: no returned/native-extracted
effective callback or optional async behavior is needed. Acceptance requires
actual source-ordered construction and proved nonexecution. Existing frozen
decorator contracts at lines 11003 and 11023 explicitly distinguish the inner
application failure from the unreachable outer application. Stage0 reiterates
that a decorator failure must not execute a later construction effect. The
expected fixed row with no invented unresolved outer effect remains binding.

## Preservation and limitations

No unsafe expectation, including all A9+B7 witnesses, changes. All original 119
methods remain preserved. Dormant storage/return and already-proved readonly or
failed-before-body paths must not be blanket-refused. This correction permits
explicit refusal only for the fifteen listed effective-transfer schedules; it
does not authorize removing dormant controls or weakening old tests.

This is a requirements audit based on the exact public receipts, oracle traces,
r010 acceptance and frozen old tests. It adds no execution, production verdict,
async support, budget increase or acceptance-wall authorization.

