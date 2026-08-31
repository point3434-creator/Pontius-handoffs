# Adopted bounded design after r009 discovery

The pre-edit Stage0 is c-provenance-v4-stage0.md. The completed read-only source
inventory identifies two independent obligations: complete provenance at relevant
binding loads, and retained helper authority across callable/execution boundaries.
There is one explicit-call effect-hook site, before specialized call returns;
the callback default witness is not an ast.Call early-return bug. _review_body
omits bare default-only names from its helper provenance seed set. A captured
default retains a qname with no proof, so the escape walk correctly sees nothing.
Free-cell/global callback reachability is separately absent.

Adopt a bounded correction of those proof/obligation boundaries using the existing
flow, lexical bindings and finite budgets. Model support does not expand to a
general Python heap, map/filter/reduce interpreter, or arbitrary callback engine.
For relevant unsupported execution/escape, explicitly refuse. Preserve capture
versus lookup timing and deferred/nonexecuting states. Helper identity is sidecar
proof; it must not replace or globally poison legacy values/returns/exceptions.

Discovery inventory: explicit calls; opaque callbacks and retained/forwarded
callables; sorted/list.sort keys; restricted max/min projections; implicit callable,
constructor/destructor, descriptor/attribute/item/truth/arithmetic/comparison/hash,
format/conversion/iteration/context/async protocols; decorator application;
generator-expression/local-generator consumption and nonrecording return
projections. Existing reached generator bodies already route through normal
statements; do not classify them as blanket bypasses. Additional inventory rows
are test/discovery obligations, not established defects. Do not claim unsupported
callbacks executed when the result is only inability to prove their safety.

Before accepting a repair, make metamorphic cases insensitive to an inert owner
reference, final self/class lookup spelling, and binding/forwarding placement.
Exercise actual namespace effects through relevant callable families and pair them
with read-only, unrelated-store, dormant/lazy and invalid-binding controls. Extend
only the bounded proof/admission mechanism needed to close reproduced classes.
A broader architectural redesign beyond this boundary requires a new explicit
assessment rather than silently expanding the fix.

Preserve all existing analyzer tests, especially budgets, defaults/receiver binding,
exact exceptions, deferred execution and return values. Run all current analyzer
methods from AST (not an old hardcoded subset) on actual3.11.15 first then3.14.6;
retain every failure as evidence. Parent owns corpus attribution, census literals,
ordinary generation, final focused suites, freeze and fresh reviews. Never widen
caps or change baseline/CI/A/B to produce GREEN.
