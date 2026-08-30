# Independent cold-B invariant and related-path inventory

Reviewer: Codex /root/ab_r002_cold_b. Recorded before opening coverage.md.
Target: 2f4287f68a83fac4225a05a91daffdb3f2977a43; manifest
55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957.
Inputs read: handoff, candidate, manifest rows, current CLAUDE.md and whole
workflow/checklist, frozen ADR-0485 / ADR-0484 brief, permitted R2/R3
outcome dispositions, frozen changed source/test diff and related sealed code.
No coverage, implementer self-report/plan/transcript, or other review opened.

| Invariant / risk | Independent related-path inventory | Observable check |
| --- | --- | --- |
| Actual immutable policy authority owns selection and identity | HandRuntime.__init__, _admit_blueprint, ReplayHost.__init__, select_blueprint_action | Outer delegate, subclass digest/canonical/action hooks and class pretenders rejected before delivery; honest exact source succeeds |
| Nested caller behavior cannot counterfeit key matching or canonical identity | Source.entries; BlueprintActionEntry.key/action; all BlueprintDecisionKey scalars/tuples/history atoms; BettingAction values; _copy_exact_policy_value | Nested subclass/equality/canonical/conversion hooks must never run at admission/selection; both public boundaries refuse them |
| Direct four-input helper validates complete exact current visible context | OneSeatCardState; NoLimitBettingState including nonempty BettingActionRecord history and optional terminal enum; LegalBettingDecision including RaiseBounds; _same_exact_value; BlueprintDecisionKey.from_state | Foreign context top types, nested hooks and equal-but-wrongly-typed decision fields refuse as InvalidDecisionContextError |
| Source admission gives the runtime its own policy graph | _copy_exact_policy_value rebuilds records/tuples; source field storage; header reads runtime.blueprint_sha256; start-hand digest capture | Identity of header/decisions agrees with original honest policy; caller's ordinary input objects cannot change policy behavior through accepted custom values |
| Hit/miss/illegal-entry outcome split survives | _select_admitted_blueprint_action, sealed action_for, _has_illegal_matching_entry, _require_bound_selection, V2 emission and ActionMailbox | Real hit emits legal raise, missing/other-state key uses passive choice, illegal matching entry emits nothing and typed failure; hidden completions preserve decisions |
| Initial identity binding remains measured, without second full-table rehash per action | dispatch -> _start_hand digest -> _finish_boundary; runtime-owned selector -> sealed action_for digest; _require_bound_selection compares captured digest | Delaying real canonicalization at first event affects boundary timing; profile actual calls for table canonicalization once per subsequent action |
| Scope and frozen bytes remain exact | runtime.py, replay.py, two changed tests; sealed immutable_blueprint/no_limit_betting/holdem_cards/V2 untouched | Recompute stored-blob manifest and compare parent/tree/ref; focused floor-first disposable-clone tests only |

Independent discovery method: start from ADR policy-selection inputs, enumerate
public policy entrances and all identity/selection reads, follow dataclass
fields into nested scalar/container/enum/record values, then trace selection
through the real mailbox and ReplayHost header. Tests will challenge public
boundaries with benign controls and normally constructed adversarial values.
Malformed deep exact graphs and constructor validation assumptions need explicit
inspection; broad event/mailbox/receipt admission, trace parsing, publication,
accounting redesign and Slice C remain excluded. No full-table complexity,
operating-limit or performance result is claimed.
