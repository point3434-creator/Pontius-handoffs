# Reviewer 02 initial invariant and related-path inventory

Reviewer: Codex, independent cold reviewer 02; 2026-09-08.
Candidate: e39d3b93695bfc601d051e8e71f334eef4d10d19.
Manifest: 4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405.
BASE: 46f45298a405b967976413a4b8e45e7837602316.

Saved before opening parent-disposition.md or checks/author-verification.json.
No other review, task ledger, coordinator notes or sibling material was read.
This is an initial review inventory, not an execution or transitive-closure claim.

## Requirements and independent invariants

1. The frozen change is the two implementation specification documents only.
   Manifest rows must hash raw Git blobs and sort whole rows by bytes.
2. Stage 0/0b and Tier C protect key translation and evidence classification.
   Capacity/preflight must exit before full solving; checkpoints retain the single
   600 production/400 test line budget and two-round Slice A authorization limit.
3. Key equality includes real public history, returned chips, board order, private
   hand, seats, stacks and blinds. Root replay must match actual host events.
4. CHECK/null is three bytes longer than raise/2 in the compact action object.
   Nested distinct-key prefixes with fixed metadata are monotonic. Largest fitting
   conservative prefix is not a universal maximum over solved policies.
5. C(47,2)=1081 hero hands and C(45,2)=990 villains per hero. At s=4 the
   checked-to root permits CHECK or raise_to(2); a called bet is all-in.
   Integer kernel settlements define totals; exact ties choose CHECK first.
6. The singleton reference must explicitly fix villain CALL. Missing policy entries
   are uniform in evaluation.policy_distribution, and are a different opponent.
   Reference construction and evaluation both cost work; stop/interrupt cannot pass.
7. Finite seeded witnesses retain all twelve dealt cards and reject board collisions.
   Required hand coverage cannot be redefined by incomplete witness discovery.
   Correctness-selected witnesses are not a later chip-analysis population.
8. Failure is read from hands[*].result before any river record is requested.
   Completion requires settlement, child closure and usable capture. Nullable v1
   failures can exist without decisions; v1 decisions do not carry delivery_status.
9. Runtime blueprint lookup and direct BlueprintProvider.propose are distinct seams.
   Replayed PreparedBlueprint.action_for must discriminate CHECK hit from default.
   Counts must reconcile scheduled attempts including absent outcomes and failures.
10. Agreement eligibility differs from completed chip eligibility. A baseline that
    diverges before the river must retain its completed chip result for Slice B.
11. One parent owns begin_run/finish_run; inherited contexts suppress child writes.
    Each Session must still prepare schedule/artifact/stacks. Cached host loading
    alone does not initialize a Session or suppress a source scan without context.
12. Real negative controls exercise the claimed public boundaries. Envelope fixtures
    prove classifier behavior only; tests and measurements need distinct receipts.

## Discovery and related frozen paths

Read the whole candidate, BASE README/workflow/amendment and parent specification.
Inspected the frozen tree and traced key construction, reference evaluation,
host/session control flow and their imports. The supplied dependency list was a
navigation aid; additional test/consumer paths require inspection before verdict.

- src/pontius/legal_river_continuation.py: root validation, legal action order,
  dealt-state membership rebuilding, information keys, kernel-backed returns.
- src/pontius/evaluation.py and game.py: policy defaults, reference traversal,
  floating action values and deterministic legal-action tie ordering.
- src/pontius/no_limit_betting.py, holdem_cards.py and river.py: replay, raise
  bounds, board/private normalization, rank and settlement, uniform joint ranges.
- src/pontius/immutable_blueprint.py and blueprint_artifact/codec.py: complete
  keys, duplicate refusal, deterministic wire/canonical distinction and defaults.
- src/pontius/blueprint_preparation/lookup.py: prepared lookup boundary.
- src/pontius/decision_provider/{model,providers,selection,codec}.py: observation
  authority, public proposals, blueprint_hit/default versus v1 retained reasons.
- src/pontius/legal_decision_spine_v2.py: public digest and selection contract.
- src/pontius/v0a/{runtime,model,trace,clock}.py, action_clock.py and
  preparation_bank.py: actual v1 decision/failure shapes, nullable timing,
  accounting closure and retained reason generation.
- tools/v0a_event_adapter.py: source context, framed event/hand/session writers.
- tools/v0a_table_host.py: real scripted prefix, input cap, child process owner,
  WireConsumer validation, action application and completed settlement/closure.
- tools/v0a_table_session.py: Admission cache, prepare, nested result wrapper,
  one-hand session constraint, failed capture and outer-session finalization.
- tools/v0a_seeded_deals.py: seed syntax, index 0..15, fixed twelve-card draws.
- tools/v0a_blueprint_workload.py: maintained worker/resource/context example.
- src/pontius/execution.py and status_generation.py: run result writer, journal
  append and generated STATUS consumer, inherited context and output directory.
- tests/cases.json and tests/test_pontius.py: maintained suite registration.
- tests/test_legal_river_continuation.py and adjacent blueprint/provider/runtime,
  host/session/execution suites: independent assertions and usable boundary seams.
- experiments/research-roadmap.md and experiments/bot-validation.md: downstream
  dependency limits and retained interpretation consumer; no historical run opened.

## Initial questions to resolve

- Does frozen kernel control flow establish one hero node without a full chance tree?
- Does exact tie arithmetic align with the floating singleton reference for the
  declared zero control, while avoiding any invented action-tie tolerance?
- Are genuine public controls and complete accounting required across all phases?
- Does the planned worker preserve completed observations on interruption while
  keeping one parent result and allowing each session preparation?
- Is the shared line/round budget credible and are future decisions explicit gates?

No runtime, solver, host, historical owner or test was executed for this inventory.
