# Independent invariant and related-path inventory (Claude, r002 cold pass)
Recorded before opening inputs/parent-disposition.md and inputs/prior-disposition.md.
Sequencing deviation: coverage.md and checks/*.json were opened before this inventory.

## Invariant under review (FIX target)
Every per-hand teacher decision and every per-hand reference acceptance must be a
function of exact integer settlement totals only. A rounded floating value or a
rounded argmax may neither veto a validated exact tie nor admit a wrong non-tie
action; a wrong integer total must fail through an independent exact check.

## Members discovered from frozen source (base 46f45298), by stage
1. Domain: no_limit_betting._raise_bounds/legal_decision/apply_action/settle at s=4:
   root actions (CHECK, raise_to(2)); after raise: (FOLD, CALL); terminals +/-2, +/-4, 0.
   Structural identity: J_bet == 2*J_check for every hand (same showdown, doubled pot).
2. Sealed construction: legal_river_continuation.__post_init__ -> river._normalized_joint_weights
   (raw 1.0 x 990 -> total 990.0 exact -> one rounding of 1/990 per deal);
   LegalHeadsUpRiverState.__post_init__ dict(self.game.deals) membership per state.
3. Policy: evaluation.policy_distribution (missing key -> uniform default; explicit
   {CALL:1.0} -> exact 1.0/0.0); hero key string via information_state_key / collect_information_sets.
4. Accumulation A: evaluation.expected_utilities_from_state chance loop `values[i] += p*v`
   (990 sequential roundings; p*v exact; zero-probability branches still walked).
5. Accumulation B: evaluation.best_response action_values via built-in sum() and
   continuation_value sum() (interpreter-dependent: naive on 3.11, Neumaier on >=3.12);
   selection by max() -> tie label is floating; returned value re-evaluated via expected_utilities.
6. Integer validation: caller-side rational check (as_integer_ratio); lattice J/990; E=2^-40.
7. Tie/action rule: production CHECK-first; export rows; agreement compare in section 5.
8. Export: codec.encode_blueprint (wire JSON, sorted by key canonical bytes, monotone in
   nested prefixes; private_hand digits vary row size by <=2 bytes; check/null vs raise/2 = +3 bytes).
9. Host path: v0a_table_session.Session.prepare -> Admission(Path.cwd()) -> host.Source ->
   execution.begin_run(inherited=PONTIUS_RUN_CONTEXT) root equality; host.ChildConnection
   env + cwd=source.repo; OwnedInput blueprint limit 1048576 (session and host main).
10. Records: v0a.model.DecisionRecord (selection_reason table_hit/passive_default, no
    delivery_status), FailureRecord.delivery_status; event adapter event_result/hand_result/
    session_result frames; session hands[*].result with capture_truncated/child_stdout_base64.
11. Witnesses: v0a_seeded_deals.deal_for_hand (index 0..15, 12 private cards, board deck[12:17]
    replaced by declared board; collision-only rejection); host TableInput board order preserved,
    not canonicalized (OneSeatCardState/_canonical_board keep order).
12. Run record: execution.finish_run (inherited -> no-op; output_directory; STATUS render).

## Planned discriminating cases I expect to see covered
- all-zero tie (royal board), nonzero cancellation both signs (W=L>0), wrong total, false
  production tie, wrong non-tie action, NaN/inf/malformed map, missing villain policy,
  domain change (deal count / weights / extra chance node), interpreter dependence of sum().

## Falsifiers I would add
- Assert J_bet == 2*J_check on validated totals (domain/policy misconfiguration detector).
- Assert len(game.deals)==990 and all probabilities identical before applying n=990.
- Assert villain policy keys == collect_information_sets(game, 1) keys.
