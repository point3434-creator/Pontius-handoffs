# Codex cold review 01: pre-check inventory

Recorded before opening checks/, after the handoff, pinned rulings, adopted brief/design,
and the two frozen production blobs. No implementer transcript or other review was read.

Candidate: b1fdacf157649ca92d1aee3e39b7b0471edbcd5d
Base: f647a7989394f084875a040b20c41891168163ed
Manifest: 376dff405c15301a489ea3fde84abc3a41c2afa4c33c6ee67423477ca9e08b8e

## Independent invariants and evidence map

- Identity: parent, tree and exactly seven changed paths agree with Git; SHA-256 rows derive
  from raw Git blob bytes and sort as entire rows. Pinned input identities must also agree.
- Replay and keys: public kernel replay reaches the declared s=4 river state and actor;
  history, contributions, legal actions and card ordering survive actual key serialization.
- Ranges: exactly 1,081 distinct hero hands and 990 distinct compatible villains per hero;
  no duplicate, blocked or malformed hand may pass as a legitimate preflight observation.
- Capacity: nested prefix wire sizes are monotone for the actual codec; fixed metadata and
  conservative actions preserve the bound; boundary key sets and in-domain sizes reconcile.
- Production: both forced lines settle through the kernel; integer utility totals use the
  actual enumeration count, maximize exactly, and CHECK on equality without joint games.
- Reference: explicit unit-weight singleton game and CALL law; all assumptions supporting
  the dyadic error bound hold in the actual continuation/evaluator, including terminal
  integer bounds, action domain, chance structure and unique hero information set.
- Comparison: forced values independently reconstruct both totals; nonfinite, false ties,
  wrong non-tie action, invalid selected map and smallest signed gaps cannot pass.
- Plan admission: every mandatory identity/input is explicit before launch; runtime, finite
  resource limits, ordered universe/permutation, fixed prefix, sample and controls are bound.
- Cost report: separate production, reference construction, forced calls, best response and
  comparison costs; meaningful cache order, work counts, memory labels and estimate limits.
- Ownership: one admitted parent/run root, inherited worker context, Job before resume,
  bounded launch/execution/cleanup, retained completed observations and failure reasons.
- Failure: budget, disagreement, interruption, malformed input, worker setup/exit and result
  publication cannot become success or lose the invocation's retained result/journal line.
- Tests/receipts: map test predicates to real boundaries; mock triggers cannot prove native
  cleanup or ownership. Check 3.14-only receipt identity, failures, skips and evidence limits.
- Scope: steps 1-3 only; sealed paths unchanged; read-only cache inspection is not a source
  modification. Later bridge work and the controller's budget increase are distinct gates.

## Related-path inventory to inspect at frozen base

- Governing parent design, workflow/checklist, amendment, README and runtime configuration.
- no_limit_betting.py, holdem_cards.py, river.py, game.py, legal_river_continuation.py and
  evaluation.py, including their true imports/terminal/range and policy behavior.
- immutable_blueprint.py, blueprint_artifact/codec.py and their internal model/validation
  dependencies; key and wire encoding, source ordering, root legal-decision spine.
- execution.py, status_generation.py and their actual writers/source identity consumers.
- tools/v0a_table_host.py Job/Source and its source/cache/admission dependencies;
  tools/v0a_table_session.py Session.prepare and worker-root context behavior.
- Existing transport/execution/host tests relevant to changed failure boundaries;
  tests/test_pontius.py, tests/cases.json and both complete candidate suites/fixtures.
- Listed provider/v0a/dealer dependencies where they bear on inherited contracts, while
  recognizing export/agreement is deferred and the supplied list is not transitive closure.

Read-only static review only. No project code, tests, owners, tools, solvers, hosts or
measurements will run. Only this inventory and my attributed report/ledger may be written.
