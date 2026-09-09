# Reviewer 02 independent inventory, recorded before deferred coverage

Reviewer: Codex, r003 cold reviewer 02. Date: 2026-09-08.
Candidate: 18b7527a3989f7d38830a7881c976385fe9bc4de
Manifest: 2664aca6f857999a4b45036b5cd3c250fbc3d8210b3132510d0e05a57e821975
Base: b378104cd2934f248a9545d7d482b0db25db813c

This inventory was recorded after reading the handoff first, both candidate
blobs, pinned rules, and selected frozen dependency definitions and call paths.
Deferred coverage and prior-round disposition have not been opened.

## Independent requirement and risk map

- Identity: candidate parent/tree and only two changed files must match the
  packet. Recompute whole-row sorted manifest from raw candidate blobs.
- Teacher: exact per-hero best response against a fixed passive villain;
  singleton sealed continuation is the independent algorithmic cross-check.
  Exact ties follow legal action order. No T2 export before determinization.
- Reachability: replay legal prefix from new_hand at s=4, button 0, hero 2;
  all other seats except passive seat 1 fold with zero contributions. At the
  river hero can check or bet 2; no subsequent hero decision exists.
- Identity must cover cards and board order, all betting vectors, complete
  history including uncalled returns, action legality, and policy identity.
  Export, preparation, runtime replay, host replay, and direct provider agree.
- Capacity: wire bytes, conservative check placeholders, final recheck,
  strength-blind H, explicit overflow, no codec change.
- Sampling: dealer private cards, board-collision rejection only, account for
  folders by marginalization, off-pool orientations stay in the population.
  Seed and hand-index schedules must respect dealer's index range 0 through 15.
- Composition: one hand per session avoids carried stacks/button rotation;
  every draw supplies both orientations for each policy, with fixed opponents.
- Failure: rejected/unknown/not-attempted delivery may have no decision record;
  accepted delivery can fail timing later. Host validation, terminal closure,
  process exit, capture truncation and cleanup all precede completed status.
- Retention: bounded stdout captures full newline frames only when not
  truncated. Use session hands[*].result status/failure, not an invented flat
  row or a DecisionRecord delivery field. No decision is needed to exclude.
- Classification: one controlled river decision only for agreement; match
  selected action and table_hit against independent lookup. Applied check
  alone cannot distinguish an in-pool hit from a default.
- Provider: direct BlueprintProvider observation/proposal contract is distinct
  from blueprint-v1 runtime, where _provider is None.
- Outcomes: completed prefix-diverged cells retain chip settlements even when
  no river root exists; agreement and chip inclusion must remain separate.
- Settlement: final stack minus initial stack equals kernel net_returns;
  side pots and uncalled returns stay governed by kernel settlement.
- Pairing: whole matched unit includes both orientations across policies;
  repeated sampled hand pairs remain draws rather than silently deduplicating.
- Missingness: failure need not be independent of payoff; withhold any affected
  full-population claim, label survivor statistics conditional, calculate
  missing-unit bounds using planned denominator. Reruns preserve planned units.
- Inference: per-orientation versus unit sum factor 2, range [-4s,4s], fixed
  equal board weights, familywise alpha allocation, planned-unit Hoeffding
  floor, no equivalence inference from an inconclusive interval.
- Recording: one begin/finish and journal record per run, boundary source
  admission, preregistration before holdout, immutable result and family claims.

## Related frozen paths discovered from the requirements and source

Core teacher and oracle:
- src/pontius/legal_river_continuation.py
- src/pontius/evaluation.py
- src/pontius/river.py: RiverDeal, range normalization, hand ranking.
- src/pontius/game.py: shared chance/terminal protocol and action types.
- src/pontius/cfr.py: secondary teacher only; deferred from T1 acceptance.

Key, action and settlement authority:
- src/pontius/immutable_blueprint.py
- src/pontius/blueprint_artifact/codec.py
- src/pontius/blueprint_preparation/lookup.py
- src/pontius/holdem_cards.py
- src/pontius/no_limit_betting.py
- src/pontius/legal_decision_spine_v2.py

Runtime, wire, provider and host envelopes:
- src/pontius/v0a/runtime.py
- src/pontius/v0a/model.py
- src/pontius/v0a/trace.py
- src/pontius/decision_provider/model.py
- src/pontius/decision_provider/providers.py
- src/pontius/decision_provider/selection.py
- src/pontius/decision_provider/codec.py
- tools/v0a_event_adapter.py
- tools/v0a_table_host.py
- tools/v0a_table_session.py
- tools/v0a_seeded_deals.py

Integration and acceptance surfaces:
- tests/test_legal_river_continuation.py: retained prefix fixture.
- tests/cases.json: planned registration surface.
- docs/architecture/v0a-paired-prereg-r001/: retained plan shape.
- execution_journal.jsonl and experiments/bot-validation.md: future output
  surfaces, not inputs to this cold review.
- Source admission and run lifecycle helpers reached by future orchestration
  require review at implementation freeze; no runtime claim is made here.

Initial static results: identity digest matches; session completion subsumes
wire, timing, settlement and cleanup failures; v1 reason lookup cross-check
has a real purpose. Remaining work is deeper oracle/key inspection, comparing
this inventory with deferred coverage, then issuing a whole-candidate verdict.
