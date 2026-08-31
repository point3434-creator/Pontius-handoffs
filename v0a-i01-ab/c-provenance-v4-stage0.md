# Stage0: helper provenance roots and callable escapes

Status: planning before production edits. r009 remains frozen. This is one
residual of the existing helper-identity contract, not new Python callback support.
The same bounded FIX allowlist applies: generator, contract tests, ordinary
inventory/profile pair. Accepted A/B, other C, baseline, finite budgets, capability
authority and main are preserved.

Invariant: an invocation or escape cannot gain trusted helper authority by omitting
an incidental source reference. A callable may retain helper owners through its
definition-time defaults, bound receiver and invocation-time free cells, including
nested value/forwarding paths. When that reachable authority or execution is
unsupported, refuse explicitly; never borrow a historical registry name for a
later literal sink. Dormant supported bodies must not execute effects. Preserve
existing value, return and exception semantics independently from identity proof.

Discovery follows every construction/merge/traversal of callable FlowValues;
module/helper provenance environment roots; lexical-shadow/unbound handling;
effective-call binding; direct calls, opaque escapes, modeled callback/protocol
execution, and deferred consumption. Search by those API/data surfaces, not just
map/sorted spellings. The current witnesses exercise opaque callback escape and
missing default/free-owner proof. Other paths are inventory obligations, not claims
of demonstrated defects until reproduced.

Before implementation, isolate the two mechanisms with metamorphic controls:
change only final self versus class-qualified call or add an inert owner load;
compare explicit/default/free/global/receiver forwarding and readonly counterparts.
Run direct, returned/forwarded and consumed callback paths; retain dormant/lazy
controls and existing tests. Use independent pure-return/exception projections,
never execute inspected subprocess/CuPy bodies. New abstract-language support is
not required: unsupported callback invocation may be refused honestly.

Reassess the bounded design using the finished source inventory. Prefer a complete
provenance-root lookup and one reachable-callable-authority traversal/admission
boundary over callback-name patches. Preserve capture time versus lookup time and
avoid whole-module/name poisoning. Do not implement until the inventory identifies
why v3's effective-input correction did not cover these paths. No budget increases,
generic heap/reflection implementation or unrelated generator/native engine rewrite.

GREEN requires the old analyzer contracts plus new class-derived/metamorphic
controls, all affected tests both actualslots, original capability row/edge
preservation with source-attributed census changes, a new frozen pair and two fresh
cold passes. Current broad wall remains unopened.
