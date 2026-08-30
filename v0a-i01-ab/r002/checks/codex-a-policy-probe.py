"""Independent cold-A observations; no candidate source or test mutation."""
import json
import sys
from dataclasses import fields, replace
from pathlib import Path

from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import (
    BlueprintActionEntry, BlueprintDecisionKey, ImmutableBlueprintActionSource,
)
from pontius.no_limit_betting import (
    CALL, BettingAction, LegalBettingDecision, NoLimitBettingState, RaiseBounds, raise_to,
)
from pontius.v0a.model import ActionMailbox, HandStartedEvent, FailureCode
from pontius.v0a.replay import FIXTURES, PROTOCOL_ID, ReplayHost
from pontius.v0a.runtime import HandRuntime, InvalidDecisionContextError, select_blueprint_action
import pontius.v0a.runtime as runtime_module

assert sys.flags.safe_path and sys.flags.dont_write_bytecode
assert Path.cwd() == Path(r'D:\Pontius-review-ab-r002-cold-a-20260830')
assert Path(runtime_module.__file__) == Path.cwd() / 'src/pontius/v0a/runtime.py'

class Clock:
    def __init__(self): self.now = 1000
    def __call__(self):
        self.now += 1000
        return self.now

betting = NoLimitBettingState.new_hand(button=0, starting_stacks=(200,) * 6,
                                      small_blind=1, big_blind=2)
cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0, 13))
decision = betting.legal_decision()
key = BlueprintDecisionKey.from_state(cards=cards, betting=betting, decision=decision)
empty = ImmutableBlueprintActionSource('cold-a-empty')
real = ImmutableBlueprintActionSource('cold-a-raise', (BlueprintActionEntry(key, raise_to(6)),))
event = HandStartedEvent(hand_id='cold-a-hand', event_index=0, button=0, controlled_seat=3,
                         starting_stacks=(200,) * 6, small_blind=1, big_blind=2,
                         private_cards=(0, 13))
rows = []

# Ordinary constructed subtype graphs are rejected at both public boundaries.
class Source(ImmutableBlueprintActionSource):
    @property
    def digest(self): raise AssertionError('caller digest ran')
class Canonical(ImmutableBlueprintActionSource):
    def canonical_bytes(self): raise AssertionError('caller canonical bytes ran')
class Lookup(ImmutableBlueprintActionSource):
    def action_for(self, **kwargs): raise AssertionError('caller lookup ran')
class Key(BlueprintDecisionKey): pass
class Entry(BlueprintActionEntry): pass
class Action(BettingAction): pass
class Integer(int): pass
class Text(str): pass
class Tuple(tuple): pass
class Pretender:
    @property
    def __class__(self): raise AssertionError('caller class hook ran')
class Delegate:
    def __getattr__(self, name): raise AssertionError('caller delegate hook ran')

subkey = Key(**{field.name: getattr(key, field.name) for field in fields(key)})
policies = {
    'source-digest': Source(real.source_id, real.entries),
    'source-canonical': Canonical(real.source_id, real.entries),
    'source-lookup': Lookup(real.source_id, real.entries),
    'class-pretender': Pretender(), 'delegate': Delegate(),
    'nested-key': ImmutableBlueprintActionSource('k', (BlueprintActionEntry(subkey, CALL),)),
    'nested-entry': ImmutableBlueprintActionSource('e', (Entry(key, CALL),)),
    'nested-action': ImmutableBlueprintActionSource('a', (BlueprintActionEntry(key, Action(CALL.kind)),)),
    'source-text': ImmutableBlueprintActionSource(Text('t')),
    'entries-tuple': ImmutableBlueprintActionSource('t', Tuple(real.entries)),
    'nested-integer': ImmutableBlueprintActionSource('i', (BlueprintActionEntry(
        replace(key, small_blind=Integer(1)), CALL),)),
}
for name, policy in policies.items():
    for boundary in ('runtime', 'helper'):
        mailbox = ActionMailbox()
        try:
            if boundary == 'runtime':
                HandRuntime(blueprint=policy, mailbox=mailbox, clock=Clock())
            else:
                select_blueprint_action(policy, cards, betting, decision)
        except Exception as error:
            caught = type(error).__name__
        else:
            caught = None
        expected = 'TypeError' if boundary == 'runtime' else 'InvalidDecisionContextError'
        assert caught == expected and not mailbox.accepted, (name, boundary, caught)
        rows.append({'case': name, 'boundary': boundary, 'exception': caught, 'deliveries': 0})

# Complete value typing in unvalidated decision/bounds records.
for field in fields(decision):
    value = getattr(decision, field.name)
    if type(value) is int:
        replacement = bool(value) if value in (0, 1) else float(value)
        bad = replace(decision, **{field.name: replacement})
        try: select_blueprint_action(empty, cards, betting, bad)
        except InvalidDecisionContextError: pass
        else: raise AssertionError(field.name)
        rows.append({'case': 'decision-alias-' + field.name, 'exception': 'InvalidDecisionContextError'})
for field in fields(decision.raise_bounds):
    value = getattr(decision.raise_bounds, field.name)
    replacement = int(value) if type(value) is bool else float(value)
    bad = replace(decision, raise_bounds=replace(decision.raise_bounds, **{field.name: replacement}))
    try: select_blueprint_action(empty, cards, betting, bad)
    except InvalidDecisionContextError: pass
    else: raise AssertionError(field.name)
    rows.append({'case': 'bounds-alias-' + field.name, 'exception': 'InvalidDecisionContextError'})

# Real dispatch and mailbox positive/negative controls.
for name, policy, action, reason, failure in (
    ('hit', real, 'raise', 'table_hit', None),
    ('miss', empty, 'call', 'passive_default', None),
    ('different-state', ImmutableBlueprintActionSource('different', (BlueprintActionEntry(
        replace(key, private_hand=(1, 14)), raise_to(6)),)), 'call', 'passive_default', None),
    ('illegal', ImmutableBlueprintActionSource('illegal', (BlueprintActionEntry(
        key, raise_to(1000)),)), None, None, FailureCode.INVALID_BLUEPRINT_ENTRY),
):
    mailbox = ActionMailbox()
    outcome = HandRuntime(blueprint=policy, mailbox=mailbox, clock=Clock()).dispatch(event)
    if failure is not None:
        assert outcome.status == 'failed' and outcome.failure.code is failure
        assert not mailbox.accepted
    else:
        assert outcome.status == 'decided' and len(mailbox.accepted) == 1
        assert outcome.decision.selected_action.kind == action
        assert outcome.decision.selection_reason.value == reason
        assert outcome.decision.blueprint_sha256 == policy.digest
    rows.append({'case': name, 'status': outcome.status, 'deliveries': len(mailbox.accepted)})

# Observe real sealed methods; no replacement implementations or forged selections.
profile_results = []
for fixture in FIXTURES:
    policy = ImmutableBlueprintActionSource('cold-a-profile')
    ids = {'admission': [], 'digest': [], 'lookup': []}
    def observe(frame, phase, argument):
        if phase != 'call': return
        if frame.f_code is runtime_module._admit_blueprint.__code__:
            ids['admission'].append(id(frame.f_locals['source']))
        elif frame.f_code is ImmutableBlueprintActionSource.digest.fget.__code__:
            ids['digest'].append(id(frame.f_locals['self']))
        elif frame.f_code is ImmutableBlueprintActionSource.action_for.__code__:
            ids['lookup'].append(id(frame.f_locals['self']))
    previous = sys.getprofile()
    sys.setprofile(observe)
    try:
        host = ReplayHost(fixture, run_id=f'{PROTOCOL_ID}-correctness-cold-a-{fixture.name}',
                          blueprint=policy, clock=Clock())
        outcome = host.run()
    finally:
        sys.setprofile(previous)
    assert outcome.receipt.passed
    assert ids['admission'] == [id(policy)]
    assert len(ids['lookup']) == len(outcome.decisions)
    assert len(ids['digest']) == len(outcome.decisions) + 2
    assert len(set(ids['lookup'] + ids['digest'])) == 1
    assert id(policy) not in ids['digest'] + ids['lookup']
    header = json.loads(outcome.trace.splitlines()[0])
    expected_digest = policy.digest
    assert header['blueprint_sha256'] == expected_digest
    assert all(record.blueprint_sha256 == expected_digest for record in outcome.decisions)
    profile_results.append({'fixture': fixture.name, 'passed': True,
                            'admissions': len(ids['admission']), 'actions': len(outcome.decisions),
                            'sealed_digest_calls': len(ids['digest']), 'same_owned_source': True})

# Delay the first real digest during dispatch, after runtime construction.
clock = Clock()
mailbox = ActionMailbox()
runtime = HandRuntime(blueprint=real, mailbox=mailbox, clock=clock)
digest_count = 0
def delay_binding(frame, phase, argument):
    global digest_count
    if phase == 'call' and frame.f_code is ImmutableBlueprintActionSource.digest.fget.__code__:
        digest_count += 1
        if digest_count == 1: clock.now += 16_000_000_000
previous = sys.getprofile()
sys.setprofile(delay_binding)
try: delayed = runtime.dispatch(event)
finally: sys.setprofile(previous)
assert delayed.status == 'failed'
assert delayed.failure.code is FailureCode.ACTION_DEADLINE_EXCEEDED
assert delayed.decision.timing.elapsed_ns >= 16_000_000_000

# Ordinary exact containers, constructor accepted, but invalid decision shape.
# An invalid context must produce the documented typed refusal regardless of depth.
deep = ()
for _ in range(2000): deep = (deep,)
depth_results = []
for name, bad in (
    ('action-kinds-depth-2000', replace(decision, action_kinds=deep)),
    ('raise-bound-depth-2000', replace(decision,
        raise_bounds=replace(decision.raise_bounds, minimum_raise_to=deep))),
):
    try: select_blueprint_action(empty, cards, betting, bad)
    except Exception as error: observed = type(error).__name__
    else: observed = 'accepted'
    depth_results.append({'case': name, 'expected': 'InvalidDecisionContextError',
                          'observed': observed})

print(json.dumps({'version': sys.version, 'rows': rows, 'real_host_profile': profile_results,
                  'measured_initial_binding': {'failure': delayed.failure.code.value,
                    'elapsed_ns': delayed.decision.timing.elapsed_ns, 'digest_calls': digest_count},
                  'invalid_exact_depth': depth_results}, indent=2))
raise SystemExit(0 if all(row['observed'] == row['expected'] for row in depth_results) else 1)
