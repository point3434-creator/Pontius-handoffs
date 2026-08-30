"""Public context-admission adversary: no production edits or private mutation."""
from dataclasses import fields, replace
import inspect
import json
import sys

from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import (BlueprintActionEntry, BlueprintDecisionKey,
    ImmutableBlueprintActionSource)
from pontius.no_limit_betting import (CALL, CHECK, FOLD, BettingActionKind, BettingStreet,
    LegalBettingDecision, NoLimitBettingState, RaiseBounds, raise_to)
from pontius.v0a.runtime import (HandRuntime, InvalidBlueprintEntryError,
    InvalidDecisionContextError, select_blueprint_action)

assert tuple(inspect.signature(select_blueprint_action).parameters) == (
    'source', 'cards', 'betting', 'decision')
lookups = []

def profiler(frame, event, arg):
    if event == 'call' and frame.f_code is ImmutableBlueprintActionSource.action_for.__code__:
        lookups.append(dict(frame.f_locals))

sys.setprofile(profiler)
hooks = []

class EvilInt(int):
    def __eq__(self, other):
        hooks.append('int-eq')
        return True
    __hash__ = int.__hash__

class EvilTuple(tuple):
    def __iter__(self):
        hooks.append('tuple-iter')
        return super().__iter__()
    def __len__(self):
        hooks.append('tuple-len')
        return super().__len__()

class EvilText(str):
    def __eq__(self, other):
        hooks.append('str-eq')
        return True
    __hash__ = str.__hash__

class EvilBounds(RaiseBounds):
    def __getattribute__(self, name):
        hooks.append('bounds-attribute')
        return super().__getattribute__(name)

class EvilDecision(LegalBettingDecision):
    def __getattribute__(self, name):
        hooks.append('decision-attribute')
        return super().__getattribute__(name)

class Pretender:
    @property
    def __class__(self):
        hooks.append('pretender-class')
        return LegalBettingDecision
    def __eq__(self, other):
        hooks.append('pretender-eq')
        return True

start = NoLimitBettingState.six_max_100bb(button=0)
no_raise = NoLimitBettingState.new_hand(button=0, starting_stacks=(2,) * 6,
                                       small_blind=1, big_blind=2)
short = NoLimitBettingState.new_hand(button=0, starting_stacks=(200,200,200,3,200,200),
                                    small_blind=1, big_blind=2)
history = start.apply_action(CALL)
check = start
for _ in range(5):
    check = check.apply_action(CALL)
assert check.legal_decision().can_check
states = [('raise', start), ('no-raise', no_raise), ('short-all-in', short),
          ('history', history), ('check', check)]
assert no_raise.legal_decision().raise_bounds is None
assert short.legal_decision().raise_bounds.all_in_only is True
source = ImmutableBlueprintActionSource('cold-a-own-context')
deep = 200
for _ in range(2500):
    deep = (deep,)
results = []
positives = []

def reject(label, state, cards, supplied):
    before = len(lookups)
    hooks.clear()
    observed = None
    try:
        select_blueprint_action(source, cards, state, supplied)
    except BaseException as error:
        observed = type(error).__name__
    assert observed == 'InvalidDecisionContextError', (label, observed)
    assert len(lookups) == before, (label, 'lookup reached')
    assert not hooks, (label, hooks)
    results.append(label)

for state_name, state in states:
    cards = OneSeatCardState.preflop(controlled_seat=state.acting_seat, private_hand=(0,13))
    decision = state.legal_decision()
    for f in fields(decision):
        actual = getattr(decision, f.name)
        variants = [('deep', deep), ('shallow', (7,)), ('foreign', Pretender())]
        if type(actual) is int:
            variants += [('float-alias', float(actual)), ('int-subtype', EvilInt(actual)),
                         ('wrong-int', actual + 1), ('bool', bool(actual))]
        elif type(actual) is BettingStreet:
            variants += [('enum-string', actual.value), ('text-subtype', EvilText(actual.value))]
        elif type(actual) is tuple:
            variants += [('tuple-subtype', EvilTuple(actual)), ('list', list(actual)),
                         ('same-width-deep', (deep, *actual[1:])),
                         ('same-width-string', (actual[0].value, *actual[1:])),
                         ('empty', ())]
        elif type(actual) is RaiseBounds:
            variants += [('missing', None), ('bounds-subtype', EvilBounds(**{
                b.name: getattr(actual, b.name) for b in fields(actual)}))]
        elif actual is None:
            variants += [('unexpected-bounds', start.legal_decision().raise_bounds)]
        for variant, value in variants:
            reject(f'{state_name}.decision.{f.name}.{variant}', state, cards,
                   replace(decision, **{f.name: value}))
    if decision.raise_bounds is not None:
        for f in fields(decision.raise_bounds):
            actual = getattr(decision.raise_bounds, f.name)
            variants = [('deep', deep), ('shallow', (7,)), ('foreign', Pretender())]
            if type(actual) is bool:
                variants += [('int-alias', int(actual)), ('inverted', not actual)]
            else:
                variants += [('float-alias', float(actual)), ('int-subtype', EvilInt(actual)),
                             ('wrong-int', actual + 1), ('bool', bool(actual))]
            for variant, value in variants:
                bounds = replace(decision.raise_bounds, **{f.name: value})
                reject(f'{state_name}.bounds.{f.name}.{variant}', state, cards,
                       replace(decision, raise_bounds=bounds))
    reject(state_name + '.decision-subtype', state, cards,
           EvilDecision(**{f.name: getattr(decision, f.name) for f in fields(decision)}))
    reject(state_name + '.pretender', state, cards, Pretender())
    copied = replace(decision, raise_bounds=(replace(decision.raise_bounds)
                     if decision.raise_bounds is not None else None))
    before = len(lookups)
    result = select_blueprint_action(source, cards, state, copied)
    expected_action = CHECK if state_name == 'check' else CALL
    assert result.action == expected_action and result.table_hit is False
    assert result.source_digest == source.digest
    assert len(lookups) == before + 1
    lookup = lookups[-1]
    assert lookup['self'] is not source and type(lookup['self']) is type(source)
    assert lookup['cards'] is not cards and lookup['betting'] is not state
    assert lookup['decision'] is not copied
    key = BlueprintDecisionKey.from_state(cards=cards, betting=state, decision=decision)
    legal_action = raise_to(decision.raise_bounds.minimum_raise_to) if decision.can_raise else CALL
    hit_source = ImmutableBlueprintActionSource('cold-a-hit', (BlueprintActionEntry(key, legal_action),))
    hit = select_blueprint_action(hit_source, cards, state, copied)
    assert hit.action == legal_action and hit.table_hit is True
    assert hit.source_digest == hit_source.digest
    positives.append(state_name)

cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0,13))
decision = start.legal_decision()
key = BlueprintDecisionKey.from_state(cards=cards, betting=start, decision=decision)
illegal = ImmutableBlueprintActionSource('cold-a-illegal', (BlueprintActionEntry(key, raise_to(999)),))
try:
    select_blueprint_action(illegal, cards, start, decision)
except InvalidBlueprintEntryError:
    pass
else:
    raise AssertionError('illegal hit not typed')

sys.setprofile(None)
assert not any(name == 'cupy' or name.startswith('cupy.') or name == 'torch'
               or name.startswith('torch.') for name in sys.modules)
print(json.dumps({'refusals': len(results), 'all_before_lookup': True, 'caller_hooks': 0,
                  'case_names': results, 'valid_hit_and_miss_contexts': positives,
                  'owned_lookup_arguments': True, 'illegal_hit_typed': True,
                  'four_input_surface': True, 'no_optional_gpu_imports': True}, sort_keys=True))
