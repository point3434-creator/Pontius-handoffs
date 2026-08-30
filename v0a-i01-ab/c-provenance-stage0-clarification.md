# C helper-provenance Stage 0 clarification

Append-only clarification after an independent design check of the recorded design
and frozen r008 source. This is design feedback, not a cold candidate verdict or
an executed finding. It does not change the two-file implementation ownership,
acceptance requirements, or finalization authority recorded in Stage 0.

Five obligations make the central provenance rule precise:

1. Distinguish a failed callee evaluation from a genuinely dead call. An annotation-only
   or deleted sensitive target that is attempted must leave an explicit blocker.
   Absence from the call snapshot is not proof of unreachability. An actually dead
   branch remains nonexecuting.
2. Capture the callable, not every future member lookup on its receiver. Rebinding
   the root name after selecting a bound method preserves the selected callable.
   An argument that replaces another member used inside that method must not receive
   stale approval from a receiver-wide snapshot.
3. Invalidation covers aliases, called-helper effects and unproved escapes. Member
   writes through an alias cannot retain the original member certificate. Mutation
   of an extracted callable's __code__, __defaults__ or __kwdefaults__ must explicitly
   refuse unless modeled. Extracted callables do retain identity across root-name
   rebinding alone. Conservative refusal is acceptable; silent approval is not.
4. Capture argument values when evaluated. For a call passing module while it is
   'first', followed by a keyword that rebinds module to 'second', derivation must
   preserve the first argument or refuse. Re-evaluating argument AST against the
   post-argument environment may not approve the second value. Reuse evaluated
   source-flow values or explicitly reject unsupported side effects.
5. Keep exact local definition identity, definition-time defaults and late-bound
   closure cells distinct. Saving a callable before redefining its name keeps the
   old callable. A default capturing a class keeps that object; a closure referring
   to the outer class variable observes its current cell value at invocation.

Each obligation receives an independent pure-Python projection and public derivation
control where supported, or a documented explicit refusal. These are discriminators
for the existing category, not authority to build a general Python interpreter or
heap. The implementation remains bounded and metered. Source changes still require
new frozen bytes and two independent cold reviews before broader acceptance gates.
