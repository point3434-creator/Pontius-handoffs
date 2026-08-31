# Class repair proposal challenge v1

Read-only engineering challenge to proposal
6bc11ee035a6388d73b954d1c5e9b6cd24e8815452fc56bb58197d4ae1b6c143.
Source anchors refer to retained engineer-generator-v19.py,
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.
This is not a cold review, implementation lease, executable result, or storage
port change. I read Stage0, the proposal and the relevant source; no analyzer,
fixture or oracle was imported or run. No existing artifact/source/case changed.

Disposition: the proposal correctly treats capture destinations and class exits
as a category, but three details must be explicit before it becomes a source plan.
The following are engineering constraints, not additional executed failures.

1. Preserve lexical destination identity without restoring stale cell contents.

At v19:17634-17644, _with_callable_authority takes enclosing_values from the
definition override, resolves enclosing_values.cell(name), then copies
enclosing_values.authority.cells[cell] into the current values.authority.cells.
The class loop sets that override to its entry-time outer values at 23016-23018;
class execution proceeds on forked authority and eventually adopts at 23025-23026.

Once a class-body setter correctly updates an enclosing cell, a later method
definition can resolve the right cell but copy its old value from that entry
snapshot over the newer class-successor value. Thus an explicit class frame
carrying merely the enclosing environment does not close the category.

Required rule: resolve destination ownership from lexical scope/activation, but
obtain an existing cell's live contents from the current successor authority.
Never replace that live content with an older enclosing projection or store.
A legitimately new capture must initialize from the proper current lexical
binding; a missing retained destination must remain conservative rather than
silently treating its absence as permission to copy old state. Method defaults
and decorators still evaluate in the source-point class namespace; method body
free cells skip the class namespace. Keep those two environments explicit.

Suggested discriminating obligation: class setter changes a captured scalar,
then a later method captures the same name before an outer reader consumes it.
Opposite polarities distinguish lost effects from blanket refusal. A compound-
defined method and nested class exercise the same frame rule. These are case
ideas only; no new expected outcome or execution is authorized here.

2. A retained cell tuple does not by itself prove precise nonlocal/global routing.

_ExecutionState.cell at 14110-14116 allocates a destination for any missing
binding, including unknown global content. _call_environment at 14437-14455
installs cell alternatives from callable records and deliberately avoids some
unresolved-global hydration. _registered_helper_environment at 17918-17934
separately seeds defining-module globals and filters caller locals.

Therefore the proposal's common represented-destination decision must prove
both lexical ownership and retained-store validity. Neither bindings membership
nor presence in the invoked callable's record alone establishes a defining-module
or lexical destination. Do not decide precision from the current value's kind
or whether it happens to contain helper provenance.

Keep the new precise write/delete path limited to destinations whose lexical
activation is represented and proved. Preserve the existing conservative global
and dynamic-namespace behavior, including the Stage0 exclusion of the unsupported
absent-global assumption. The same-spelled caller/global coverage can establish
non-capture or continued refusal without requiring newly precise module writes.
Do not let the inventory's global/declaration rows become an implicit promise
to build a general module state model.

Grandparent forwarding, class-body declarations and comprehension scope are
important boundaries. They need an explicit supported/deliberately-conservative
classification before the general free-name walk is replaced. Simply collecting
all Store/Del, or collecting only a function's own nonlocal declarations, remains
insufficient. Every added lexical traversal must be metered; no repeated dormant
body expansion should be justified merely as capture discovery.

3. Project existing exceptional successors; do not promise recovery of lost correlation.

_flow_statements at 21591-21610 already stops when no normal successor remains.
_flow_expression_statement at 21613-21630 owns an exception collector and restores
it in finally. A class-specific flow path must own that collector/frame for its
body and translate outward states once, preserving exception tag, explicitness
and excluded-handler partition. It must not leak a class name map into the outer
collector or run descriptor/decorator/install completion on a failed body.
Only final outward exits are projected: a class-local catch stays in its class
namespace. Nested classes project one frame at a time.

However _apply_helper_call_effects at 18457-18464 currently merges helper normal,
return and raise states before authority adoption, and at 18489-18496 emits
known throw tags when no normal/return completion exists. A class frame cannot
reconstruct path-specific normal/exception effects already merged there.

Narrow the initial exception promise to preserving the existing exception
partition and correctly translating the direct/supported surfaced successors.
The proposed always-raise helper cases can validate that boundary. Mixed helper
normal/raise precision, arbitrary protocol exceptions, TryStar recovery and a
general exception interpreter are not established by this repair. Unsupported
cases must retain their explicit conservative blockers. Do not change the
exception partition to make new clean expectations pass without another scope
decision and independent specification.

Implementation boundary to freeze

Use one explicit frame/capture argument, not separate ad hoc fixes at each guard:
- classify and retain lexical destination ownership;
- perform writes/deletes only with that proof, retaining strong/weak alternatives;
- execute each admitted class statement through existing successor semantics;
- project each outward successor using its current authority and the enclosing
  name/binding skeleton, with raw hydration rather than semantic reassignment;
- preserve caller observation/result ownership, source-point defaults/callee
  captures, auxiliary resolver contexts and strict nested-frame restoration.

Frame context must not be a shared mutable outer state that branch execution can
silently mutate. Nor should it be a stale authority snapshot used as live truth.
The name/binding skeleton and live successor authority have different lifetimes.
No new whole-state copy is free: source-plan review should identify actual
forks, projection visits and capture traversal charges before the next corpus run.

The proposal's recursive-review obligation remains valid but is not demonstrated
by current zero-entry traces. If included, bind it to the retained call snapshot
without replaying transfer/cell writes or importing unrelated ambient names.
Preserve the original frozen clean/refusal expectations throughout.

v22 storage candidate is still held unchanged. This note supplies no permission
to mix this class repair into the storage candidate or alter any source/cases.
