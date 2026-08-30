# C receiver-context clarification before source correction

Root adopts receiver context as part of the existing Stage 0 descriptor contract.
Valid Python may name an ordinary instance receiver cls or a classmethod receiver
self. Such spelling must not decide binding. Add opposing real derivation / pure
Python descriptor cases plus invalid-call fixed-argv blocker controls before edits.

Use the registry's proven caller descriptor and declared first parameter to seed
known instance/class receiver context. Propagate lexical context through local
helper closures, remove shadowed names, and give invoked class helpers only the
receiver context justified by their actual argument binding. Explicit unbound
receiver arguments are not proof of an instance. Unknown contexts fail closed.
The binder still computes binding once. No general object or alias inference,
unittest-entry preflight expansion, non-owned file change, generation or broad
suite is authorized by this clarification.

Earlier c-binding-report.md and c-binding-hashes.json describe the green03 checkpoint
only and are superseded by the final receiver-context report to follow. Their
exclusion of receiver-spelling ambiguity is not the completed contract.
