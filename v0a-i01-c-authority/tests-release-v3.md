# Released authority-transfer matrix tests v3

This release corrects only the fifteen classifications accepted in
tests-scope-addendum-v1.md. All issued v2 files, addendum and evidence remain
unchanged. The v3 worktree test file is released; this author has stopped editing.

Base: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Candidate: tests-candidate-v3.py.
Tests SHA-256: 59a7698d9dcf564a54cb98be2c5893f2c58e9d8adea1d03daf8ea0a38eef33db.
Patch: tests-patch-v3.diff, SHA-256 2fc411afe4825e64121369b0bb5b4716e530e2e48c0247eaa7d9ae31d40c2992.
Proof: tests-checks/release-v3-proof.json, SHA-256 e592af6fa848607c805e90a3252fb9b8f6b71e090f6f170468129934a4573655.

Only two classification keyword expressions changed from v2. The exact fifteen
case-ID changes are recorded individually in the proof, each with before/after
classification and unchanged sensitive-source/oracle hashes. All 176 emitted case
records match v2 exactly after removing classification: schedules, source bytes,
pure projections, runtime traces, public argv, blockers and unreachable events are
identical. All 80 required-refuse and remaining 81 required-clean expectations stay
binding, including construction-failure/decorator/True.

| Family | Planned/generated/exercised per slot | Required clean | Required refuse | Permitted refusal |
| --- | ---: | ---: | ---: | ---: |
| capture-route-execution | 64 | 36 | 16 | 12 |
| exception-and-join-successors | 12 | 6 | 6 | 0 |
| issued-witnesses | 16 | 0 | 16 | 0 |
| live-cells-and-activations | 28 | 11 | 14 | 3 |
| mapping-extraction-and-clear | 16 | 8 | 8 | 0 |
| native-alias-mutation | 24 | 12 | 12 | 0 |
| ordered-class-binding | 16 | 8 | 8 | 0 |

There are seven new methods and 176 finite schedules, with 180 harmless runtime
projections per slot. No schedule is unreachable; logs separately record unexecuted
events within exercised schedules. All old 119 methods, ASTs, constants and source
prefix remain unchanged; static method discovery remains 126. The only new-test
AST changes are the two approved classification expressions. Parent handles all
census/generated outputs; no generator, budget or production path was edited here.

The exact permitted set is capture-route-execution
{default,cell}/{return,returned-nest,flat-store}/{readonly,raise-before} (12),
plus live-cells-and-activations
cell/False/{callback,(callback,)[0],{"cb": callback}["cb"]}/False (3).
These accept explicit blockers; without blockers they still require the exact
fixed sink argv. Runtime safety alone does not mandate optional effective-result
precision. No dormant control, unsafe witness or proved decorator nonexecution
expectation was weakened.

RED was run on a fresh disposable D-local r010 clone, overlaid only with v3 test
bytes; unchanged frozen generator SHA-256
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.
Actual CPython 3.11.15 ran first and actual CPython 3.14.6 second. The control used
-I -S -B -P, payloads -B -P, exact executable/patch identity before repository
imports, scrubbed environment, snapshot cwd/src PYTHONPATH, D-local temporary
paths, and validated absolute Git. All 1761 tracked paths retained their hashes.

Both runs produced exactly 39 assertion failures: 38 missing unsafe blockers and
the one required clean decorator-nonexecution case. All A9+B7 witnesses remain
RED. The other 137 schedules pass the corrected expectations. All 176 schedules
were exercised, with zero oracle errors or analyzer exceptions. No infrastructure
error is counted as product RED. Full logs and receipts:
tests-checks/red-v3-311.txt and red-v3-311-receipt.json;
tests-checks/red-v3-314.txt and red-v3-314-receipt.json.

This is corrected test release and frozen-r010 RED evidence, not replacement
GREEN. No production implementation was inspected or executed. The full old suite,
141 original capability rows, generated census/profile preservation, later cold
reviews and any acceptance wall remain separate parent-owned gates.

Method discovery:
- test_authority_transfer_issued_witnesses (line 31854)
- test_authority_transfer_capture_route_execution_matrix (line 31913)
- test_authority_transfer_live_cells_and_activation_identity (line 31956)
- test_authority_transfer_native_alias_mutation_matrix (line 32009)
- test_authority_transfer_mapping_extraction_and_later_clear (line 32034)
- test_authority_transfer_ordered_class_binding_matrix (line 32069)
- test_authority_transfer_exception_and_join_successors (line 32131)
