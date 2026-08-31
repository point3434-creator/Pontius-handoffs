# Final R1 static verifier handoff v1

Authoring only. Root must inspect the retained verifier before any invocation.
The author parsed the verifier's syntax but invoked none of its functions and
read no final candidate. No analyzer/test/fixture/Model/controller payload ran.

The verifier requires actual3.11.15 with -I -S -B -P and these explicit inputs:
--candidate-path (retained T .py), --candidate-sha256,
--worktree-sha256 (the exact core-v1 generator watch), --verifier-sha256,
and --output (a fresh create-exclusive .json beneath T).

It hashes the retained r010 base, candidate, verifier, worktree generator and16
protected worktree files before inspection and again before writing the report.
It checks the2500 raw added+deleted line ceiling, exact caps/budget source,
original top-level AST/order, exact discovery of the renamed old public body,
and normalized binder preservation with pinned14guards/15consume/6wrappers.
New _c/_C names are discovered from additions rather than final-name guesses.

It inventories direct _c calls, budget construction owners, budgeted binder
callers, existing dependencies, old-live references, terminal policy calls and
indirect/attribute calls. Terminal -c exclusion, empty visitor evidence,
expansion preconditions, operation-owner semantics and full transitive behavior
remain source-review obligations. structural_checks_passed never means analyzer
acceptance; acceptance_proved/transitive_engine_exclusion_proved remain false.
Input or AST failures produce an explicit failed report where output admission
has succeeded. No directories are created and no existing output is overwritten.

Verifier SHA-256: e0a45ca46d5b1a66e1907655b2c43b704250f9d24521a908d0826f4646a5d32a
Authoring record SHA-256: 75c0b3fbb46d5049f812590312b9660337c1c0cc95e2d7607fa1298dd754487e
