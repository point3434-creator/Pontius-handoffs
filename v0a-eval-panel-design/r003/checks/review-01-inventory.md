# Reviewer 01 initial independent inventory

Recorded before opening coverage.md or r002 disposition. Reviewer: Codex reviewer 01.
Candidate: 18b7527a3989f7d38830a7881c976385fe9bc4de
Manifest: 2664aca6f857999a4b45036b5cd3c250fbc3d8210b3132510d0e05a57e821975
Base: b378104cd2934f248a9545d7d482b0db25db813c

Inputs so far: handoff first; pinned README, workflow, amendment, roadmap and controller
rulings; whole candidate brief/design; Git tree listing for relevant namespaces.
Candidate parent, tree, two-file scope, manifest bytes/hash and document format verified.
No runtime, solver, host, test, owner, or other r003 reviewer material was invoked/read.

## Invariants and related paths to challenge

1. Teacher truth: per-hero enumeration must preserve opponent law, tie order and exact
   utility of the singleton sealed game. Reachability and static s=4 must leave one hero
   river decision. Inspect legal_river_continuation.py, evaluation.py, no_limit_betting.py,
   holdem_cards.py and legal_decision_spine_v2.py. Deferred T2 must not inherit a false
   per-hand separability claim; cfr.py is relevant only if T2 is opened.
2. Export identity: exact cards, order, history, stacks, blinds and action meaning must
   match the host's replayed root. Inspect immutable_blueprint.py, blueprint_artifact/codec.py,
   blueprint_preparation/lookup.py and the kernel/card/spine paths above. Wire capacity,
   deterministic export, conservative placeholders and off-pool set equality need checks.
3. Acquisition/composition: collision-only conditioning over all twelve private cards,
   no pool-membership rejection, two orientations and all policies of each accepted draw.
   Inspect tools/v0a_seeded_deals.py and tools/v0a_table_session.py, including parse/validation,
   one-hand composition, board order, button and carried stacks. Duplicate sampled pairs
   must remain draws, not be silently deduplicated by unordered-pair identity.
4. Transport and outcome: distinguish session failure from host failure, incomplete or
   unsettled hands, failed event with no decision, unknown/rejected delivery, late timing
   failure, protocol/cleanup failure and truncated capture. Inspect session, table host,
   tools/v0a_event_adapter.py, v0a/runtime.py, v0a/model.py, v0a/trace.py and v0a/clock.py.
   Verify exactly what survives serialization and capture, and what successful status proves.
5. Decision classifier: one controlled-seat river record, reason versus applied action,
   independent lookup for check hits, malformed/missing/duplicate records and pre-river
   reasons. Direct BlueprintProvider is a separate seam. Inspect decision_provider/model.py,
   providers.py, selection.py and codec.py plus runtime, trace, lookup and host validation.
6. Settlement: actual terminal net returns after every completed policy path must feed chip
   comparisons; prefix-diverged controls must survive even when no target river record exists.
   Inspect table host settlement, kernel net_returns and session retention. Agreement-only
   exclusions must not leak into whole-unit chip exclusions.
7. Inference: swap sums use two orientations; exact and empirical values use matching units;
   four fixed strata use equal weights; bounded D and Hoeffding planned denominator agree.
   Any lost cell loses its whole matched unit and withholds unconditional claims. Bounds
   must distinguish the completed planned sample from the population estimand. Restoration
   by retry must preserve original draws and deployed-policy outcome semantics.
8. Lifecycle: one worker/admission, one run record/journal and accurate summary; planned
   budgets need measurement before hard gates. Read-only source identity/lifecycle contracts
   may be relevant through the session/host imports; no execution is authorized here.

## Requirement-to-evidence plan

- Brief 1-3: frozen key, codec, runtime/provider/host contracts; specified negative controls.
- Brief 4-6: dealer law and session replay; hand-count arithmetic and strata normalization.
- Brief 7: range calculation, correlated exclusion counterexample and claim-withholding rule.
- Brief 8: recording boundary and summary requirements; future implementation verification.
- Stage 0/0b: concrete scope, ground truth, dependencies, stop/budget, invariant locations,
  alternatives and unresolved rulings. Tier C is warranted by evidence validity.

This is the initial inventory, not a claim of completed source coverage. Coverage will be
opened only after this file has been written. Differences will be recorded in the review.
