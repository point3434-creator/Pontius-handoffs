# Correction: helper1050 permits a budget refusal

Engineering clarification only. Exact frozen-test, diagnostic-manifest and
receipt hashes are in coordinator-helper1050-contract-clarification-v1.json.

The original helper1050 assertion at4949 allows `analysis.*(?:depth|budget)`.
The existing work-cap error is `analysis work units exceed 262144`; a separate
original assertion at20585 requires that exact canonical wording. The retained
v26 diagnostic observes precisely this bounded refusal, with unchanged caps.
The first regex nevertheless rejects it because it contains neither literal
`depth` nor `budget`.

Root and an independent engineering reviewer confirm that this is an assertion/
error-category wording inconsistency. It is not evidence that1050definitions
must all be registered before a helper-depth refusal. Earlier descriptions
treating all three design failures as exact-depth obligations were too broad.

The helper65 and generator70 tests do require their exact depth refusals; their
premature work-budget failures remain substantive. The actual v26 suite outcome
is still50/53, with3failed assertions and0errors. No failed evidence becomes green.

No source, error message, test, label or cap is changed by this note. A future
expectation reconciliation could recognize the already canonical work-budget
category while retaining the exact allowed depth category. It must be explicit,
reviewed and issued as a new candidate, not hidden inside an optimization or
applied retroactively. The v28 freeze optimization still targets measured waste;
it must not be justified as a requirement that helper1050 reach depth specifically.
