# Released authority-transfer matrix tests v4

This adds one joined-activation category method and preserves all v3 tests and
expectations. Issued v2/v3/addendum/raw evidence remain immutable. The worktree
test file equals this released artifact; this author has stopped editing.

Candidate: tests-candidate-v4.py.
Tests SHA-256: 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd.
Patch: tests-patch-v4.diff, SHA-256 9238d7470b88aa151d0c96cc635340ed73c526a3163de3095e843bf0c39582c4.
Proof: tests-checks/release-v4-proof.json, SHA-256 ca3118004fb1ffc61d08858552b2af6c82475e6ee30ce19b1eb58343b326febd.

New method: test_authority_transfer_joined_activation_alternatives (line 32209).

The finite matrix is capture (cell/default) x allocation order (unsafe-first,
safe-first, both-safe, both-unsafe) x selection (statement if/conditional
expression): 16 schedules, each with both runtime choices, 32 pure projections.
Twelve schedules have a feasible unsafe selected callback and require explicit
blockers. Four both-safe schedules permit explicit refusal for optional effective
result precision; without a blocker they require the fixed sink row. They do not
require general callback or async interpretation.

The existing independent _program/_exercise helpers are unchanged. Pure projections
record body/write/sink and expected TypeError/fixed outcomes. Sensitive fixture
source bytes are passed only to derive_design_review, never executed. The two
factory activations use the same lexical callback body but distinct captured
owners; both selection forms must retain every feasible authority alternative.

| Verification baseline | Focus | Schedules / projections per slot | Fail / pass |
| --- | --- | ---: | ---: |
| Immutable iteration05 generator overlay | New family only | 16 / 32 | 2 / 14 |
| Frozen r010 generator | All eight matrix methods | 192 / 212 | 39 / 153 |

Iteration05 generator SHA-256:
33f944158ca20df62724d83d44a680440c455653100ba28d67b69954849cd8a5.
Frozen r010 commit: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Frozen r010 generator SHA-256:
29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692.

Both baselines ran actual CPython 3.11.15 first, then actual 3.14.6. Within each
baseline, the two slots produced identical per-case records. Iteration05 fails
cell/unsafe-first/statement and cell/unsafe-first/conditional: the unsafe runtime
valuation writes then raises TypeError, but public analysis emits fixed argv
without a blocker. The other fourteen category cases pass. The new sixteen cases
all pass their assertions on r010; its combined 39 failures are exactly v3's prior
39 failures. These results must not be conflated into one source baseline.

The proof records all 176 preserved v3 IDs individually. Their source hashes,
oracle hashes, classifications, traces and entire public result records match
the corresponding v3 r010 records exactly. Removing only the new method makes
the v4 AST identical to v3; its earlier source prefix is byte-identical. All old
119 methods, seven prior matrix methods, helpers, constants and original source
lines are unchanged. Static discovery now has 127 methods. Combined expectations
are 92 required-refuse, 81 required-clean and 19 permitted-refusal, totaling 192.

Every planned schedule was generated and exercised; no schedule was unreachable.
The logs separately record proved unexecuted write events in both-safe cases.
There were zero runtime-oracle or analyzer exceptions. The failed first wrapper
derivation is recorded as infrastructure only: no test payload ran then.

Each baseline used its own fresh D-local disposable r010 clone. For iteration05,
only hash-verified immutable coordinator-snapshot generator bytes and v4 tests
were overlaid; source was copied and hashed, not inspected. For r010, only v4 tests
were overlaid. Controls used -I -S -B -P; payloads used -B -P, exact executable and
patch assertions before repository imports, snapshot cwd/src PYTHONPATH, scrubbed
environment, D-local temporary files and validated absolute Git. All 1761 tracked
paths retained their before hashes after each run. Logs and receipts are under
tests-checks/red-v4-iteration05-{311,314}* and red-v4-r010-{311,314}*.

This release is bounded regression evidence, not replacement GREEN or permission
for a broader wall. Parent retains census/generated-output work, preservation of
the prior 141 capability rows, full-suite gates and later cold reviews. No
production source, budget, ledger or generated output was modified by this author.
