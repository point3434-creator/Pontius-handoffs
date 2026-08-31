# Released authority-transfer matrix tests

Scope: new test class only in the separately authorized C authority FIX.
This release records valid RED against unchanged r010, not production GREEN.

Base: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Released test SHA-256: c7f8d1ada3cdddc413f5074133cdbf2203ae9f62dfbb06798cddb984b1cb237f.
Patch: tests-patch-v2.diff, SHA-256 33615514edec9f31dc035385b1c9f2a580a74762378af6dd386a995ba422672f.
Matrix proof: tests-checks/release-v2-proof.json, SHA-256 3094815a0a0006df09c9c33e08e092664f1c68b4b99d3df882aa6fa15511f620.

The worktree test file and tests-candidate-v2.py have identical bytes. The new
AuthorityTransferMatrixTests class is immediately before the existing main guard.
The original 119 test methods, all old ASTs/constants, and all earlier source
lines remain unchanged. Static AST discovery now finds 126 methods. No census
assertion, generated output, production file or budget was changed by this work.

| Family | Planned/generated/exercised per slot | Required clean | Required refusal | r010 failures |
| --- | ---: | ---: | ---: | ---: |
| capture-route-execution | 64 | 48 | 16 | 14 |
| exception-and-join-successors | 12 | 6 | 6 | 1 |
| issued-witnesses | 16 | 0 | 16 | 16 |
| live-cells-and-activations | 28 | 14 | 14 | 9 |
| mapping-extraction-and-clear | 16 | 8 | 8 | 6 |
| native-alias-mutation | 24 | 12 | 12 | 3 |
| ordered-class-binding | 16 | 8 | 8 | 5 |

All 176 schedules were generated and exercised on each slot, with zero unreachable
cases and zero runtime-oracle or analyzer exceptions. The logs explicitly record
proven unexecuted events within otherwise exercised schedules, rather than calling
these unreachable cases. Four schedules run both boolean runtime choices, making
180 independent harmless runtime projections per slot.

The 274-case suggestion was a planning upper bound, not a required Cartesian
product. The final backbone is 2 capture modes x 8 routes x 4 execution modes =
64 cases. The 24 live-rebind schedules, 4 activation-identity cases, 24 native alias
schedules, 16 dictionary/extraction schedules, 16 ordered-class schedules, 12
exception/join schedules and 16 issued witnesses total 176. Existing positional,
keyword/default/receiver binding, deferred and async matrices remain untouched;
duplicating them in the new transfer backbone would increase cost without
isolating a new transfer relation. The earlier estimate of about 182 was refined
by leaving six deferred combinations to the already-existing focused coverage.

All 80 unsafe schedules require an explicit public blocker; disappearing a row
does not satisfy that assertion. All 96 lawful schedules use represented local
functions/classes, finite native collections, literal writes and supported
completion paths, and require the exact fixed subprocess argv with no blocker.
The selected-callee-before-argument case additionally requires the previously
selected sink row after a later mutation. No schedule demands arbitrary external
call precision or assumes that an absent module-global lookup is known to fail.
There are no permitted-refusal-only cases in this release.

The pure renderer independently supplies an inert sink and event recorder; it
shares the declared operation schedule, not executable sensitive fixture bytes.
Only this harmless projection is compiled/executed. The separately assembled
subprocess source is passed as bytes to real derive_design_review. Expectations
were frozen before production edits were inspected. Logs bind each case to its
source hash, oracle hash, runtime traces, public rows, blockers and classification.

Actual CPython 3.11.15 ran first; actual CPython 3.14.6 ran second. Each ran seven
methods in the same fresh D-local exact-r010 clone with only this released test
overlay. The floor control used -I -S -B -P; payloads used -B -P, scrubbed
environment, snapshot cwd/src PYTHONPATH, D-local temporary paths, exact version
and executable assertions before repository imports, and validated absolute Git.
All 1761 tracked paths retained their before hashes after both runs.

Both slots produced identical case outcomes: 54 assertion failures, comprising
38 missed unsafe blockers and 16 refusals of lawful schedules; 122 cases passed.
All nine A witnesses and all seven B witnesses failed as expected. No setup,
oracle or analyzer exception is counted as product RED. Full logs and receipts
are preserved in tests-checks/red-v2-311* and tests-checks/red-v2-314*.

This is finite contract evidence, not a general Python interpreter claim.
Replacement GREEN, the complete existing suite, 141 prior capability rows, census
regeneration and any later review/acceptance wall remain with the parent/production
owner. Issued v1 draft additions remain untouched and were never applied/executed.
The v2 test bytes are now released and must not be edited by this test author.

New method discovery:
- test_authority_transfer_issued_witnesses (line 31854)
- test_authority_transfer_capture_route_execution_matrix (line 31913)
- test_authority_transfer_live_cells_and_activation_identity (line 31951)
- test_authority_transfer_native_alias_mutation_matrix (line 32000)
- test_authority_transfer_mapping_extraction_and_later_clear (line 32025)
- test_authority_transfer_ordered_class_binding_matrix (line 32060)
- test_authority_transfer_exception_and_join_successors (line 32122)
