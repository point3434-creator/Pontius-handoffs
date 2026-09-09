# Reviewer 02 independent inventory — recorded before deferred coverage

Identity target: 61a1ce0ce964dc56b67636ff71a613e5525ab0ae, base
b378104cd2934f248a9545d7d482b0db25db813c; manifest to recompute independently. Scope is two added
documents only.

Initial invariants and falsifying paths:
1. Complete observable outcome classification at the real v1 host boundary. Inventory includes
  ordinary table-hit/default records, completed cutoff/deadline records, interrupted records after
  accepted delivery, and failures before publication or before record construction. A missing
  DecisionRecord or delivery metadata living on a FailureRecord must not disappear or be interpreted
  as a policy outcome. Pre-river defaults and river off-pool defaults have different meanings.
2. Exact key identity: scripted prefix, stacks, board order, visible hero cards, history and betting
  fields agree across export, host and direct provider check. Off-pool support is set complement,
  teacher action ties follow evaluator order.
3. Teacher partition: fixed villain law, one hero root at s=4, per-hand kernel settlements,
  singleton-hero evaluator reference. No claim that the partition supports jointly adapting T2.
  Capacity and computation preflight before expensive work.
4. Accepted population: only twelve-private-card/board collision rejection; both orientations even
  with mixed pool membership; uniform marginal hero/villain population after marginalizing folded
  hands. Exclusion must preserve pairing, and outcome-dependent exclusion must not silently change
  full-population calibration/estimand.
5. Units and inference: sum of two orientation differences versus per-cell expectation requires
  explicit scaling; equal fixed board strata; independent deal draws; bound [-4s,4s];
  loss/confidence/floor set before holdout and no invalid precision substitution by a plug-in
  variance.
6. Acceptance and scope: weak dominance may equal zero, calibration proves instrument arithmetic
  only; one run record, measured cost stop, sealed sources unchanged, no execution authorization
  inferred.

Related frozen paths independently discovered from contract and git grep:
- src/pontius/v0a/runtime.py, model.py: _decide_inner, _decision_record, _publish, _from_failure,
  _reject, DecisionRecord, FailureRecord, DispatchOutcome, TimingRecord.
- tools/v0a_table_host.py, v0a_table_session.py, v0a_event_adapter.py: scripted opponent/prefix,
  one-hand session, wire outcome and settlement.
- src/pontius/immutable_blueprint.py, blueprint_preparation/lookup.py, blueprint_artifact/codec.py:
  key, passive fallback, lookup and wire capacity.
- src/pontius/decision_provider/{model,providers,selection,codec}.py: direct observation/proposal
  boundary versus runtime record.
- src/pontius/legal_river_continuation.py, no_limit_betting.py, holdem_cards.py, river.py,
  legal_decision_spine_v2.py, evaluation.py: legal tree, raise bounds, showdown/settlement, key
  binding and independent evaluator.
- tools/v0a_seeded_deals.py: sampling/marginalization; tests/test_legal_river_continuation.py and
  tests/cases.json: fixture/reference and registration; frozen prerequisite preregistration document
  and roadmap.

Coverage has NOT been opened at this point. This is a discovery inventory, not a claim that each
listed source has already been fully inspected.
