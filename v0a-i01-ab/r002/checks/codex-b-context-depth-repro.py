from dataclasses import replace
import json
from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import NoLimitBettingState
from pontius.v0a.runtime import InvalidDecisionContextError, select_blueprint_action

cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0,13))
betting = NoLimitBettingState.six_max_100bb(button=0)
decision = betting.legal_decision()
source = ImmutableBlueprintActionSource("cold-b-depth-control")
rows = []
for field in ("stack", "action_kinds", "raise_bounds"):
    for depth in (1, 600):
        value = 200
        for _ in range(depth):
            value = (value,)
        supplied = replace(decision, **{field: value})
        try:
            select_blueprint_action(source, cards, betting, supplied)
        except Exception as error:
            observed = type(error).__name__
        else:
            observed = "returned-selection"
        expected = "InvalidDecisionContextError" if depth == 1 else "RecursionError"
        assert observed == expected, (field, depth, observed)
        rows.append({"field": field, "depth": depth, "observed": observed,
                     "contract_result": "fail" if observed == "RecursionError" else "pass"})
print(json.dumps({"observations":rows,"note":"zero exit confirms the documented defect; it is not a passing candidate verdict"},indent=2))
