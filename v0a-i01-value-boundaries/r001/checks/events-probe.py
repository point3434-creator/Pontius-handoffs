import sys
import os
import platform
import json
from pathlib import Path

SNAPSHOT = Path('D:/pontius-snapshots/v0a-values-events-3f1e008be6d04f5c8a99d05d9d8a2ef2/harness')
EXPECTED_EXE = Path(sys.argv[1])
EXPECTED_VERSION = tuple(map(int, sys.argv[2].split('.')))
identity = {
    'executable': sys.executable,
    'implementation': platform.python_implementation(),
    'version': sys.version,
    'version_info': list(sys.version_info),
    'cwd': str(Path.cwd()),
    'PYTHONPATH': os.environ.get('PYTHONPATH'),
    'PONTIUS_GIT': os.environ.get('PONTIUS_GIT'),
    'environment_keys': sorted(os.environ),
    'safe_path': sys.flags.safe_path,
    'dont_write_bytecode': sys.flags.dont_write_bytecode,
}
print(json.dumps({'identity_before_target_imports': identity}), flush=True)
assert Path(sys.executable).is_absolute()
assert Path(sys.executable) == EXPECTED_EXE
assert platform.python_implementation() == 'CPython'
assert sys.version_info[:3] == EXPECTED_VERSION
assert Path.cwd() == SNAPSHOT
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert Path(os.environ['PONTIUS_GIT']).is_absolute()
assert sys.flags.safe_path and sys.flags.dont_write_bytecode

import hashlib
import subprocess
import inspect
import dataclasses

COMMIT = '47d08d8c1556d776358e15811e3e98b859fd6a8b'
MANIFEST = 'cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a'
def git(*args):
    return subprocess.run([os.environ['PONTIUS_GIT'], '-C', str(SNAPSHOT), *args],
                          check=True, capture_output=True).stdout
assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
assert not git('status', '--porcelain')
raw = git('diff-tree', '-r', '-z', '--no-commit-id', '--no-renames',
          '--name-status', COMMIT + '^', COMMIT).decode().split('\0')
rows = []
for i in range(0, len(raw) - 1, 2):
    status, path = raw[i:i+2]
    digest = '0' * 64 if status == 'D' else hashlib.sha256(
        git('cat-file', 'blob', COMMIT + ':' + path)).hexdigest()
    rows.append(f'{digest}  {path}\n')
manifest = ''.join(sorted(rows)).encode()
assert hashlib.sha256(manifest).hexdigest() == MANIFEST
packet = Path('D:/Pontius-handoffs/v0a-i01-value-boundaries/r001')
assert (packet / 'manifest.sha256').read_bytes() == manifest
print(json.dumps({'frozen_identity': {'commit': COMMIT, 'manifest': MANIFEST,
                                     'changed_paths': len(rows)}}), flush=True)

from pontius.v0a import model, runtime
from pontius.v0a.model import (HandAction, HandStartedEvent, OpponentActionEvent,
    StreetRevealedEvent, ShowdownResultEvent, ActionEnvelope, DeliveryReceipt,
    ActionMailbox, MailboxRejectionError, FailureCode)
from pontius.v0a.runtime import HandRuntime
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.legal_decision_spine_v2 import (LegalDecisionSpineV2,
    ControlledDecisionTicketV2, EmittedBettingActionV2)
from pontius.no_limit_betting import CALL
assert Path(model.__file__) == SNAPSHOT / 'src/pontius/v0a/model.py'
assert Path(runtime.__file__) == SNAPSHOT / 'src/pontius/v0a/runtime.py'
print(json.dumps({'target_module_paths': [model.__file__, runtime.__file__]}), flush=True)

# Every candidate value subclass below changes only __post_init__.
class SkipStarted(HandStartedEvent):
    def __post_init__(self):
        pass
class SkipOpponent(OpponentActionEvent):
    def __post_init__(self):
        pass
class SkipReveal(StreetRevealedEvent):
    def __post_init__(self):
        pass
class SkipShowdown(ShowdownResultEvent):
    def __post_init__(self):
        pass
class SkipAction(HandAction):
    def __post_init__(self):
        pass
class SkipEnvelope(ActionEnvelope):
    def __post_init__(self):
        pass
class SkipReceipt(DeliveryReceipt):
    def __post_init__(self):
        pass

HAND = 'events-audit-hand'
CASES = []
def emit(case, **data):
    row = {'case': case, **data}
    CASES.append(row)
    print(json.dumps(row), flush=True)
def refuse_base(cls, **fields):
    try:
        cls(**fields)
    except (TypeError, ValueError) as error:
        return type(error).__name__
    raise AssertionError(f'base unexpectedly accepted {cls.__name__}: {fields}')
def started(cls=HandStartedEvent, **changes):
    fields = dict(hand_id=HAND, event_index=0, button=0, controlled_seat=1,
                  starting_stacks=(200,) * 6, small_blind=1, big_blind=2,
                  private_cards=(0, 13))
    fields.update(changes)
    return cls(**fields)
def opponent(index, seat, kind='fold', cls=OpponentActionEvent, **changes):
    fields = dict(hand_id=HAND, event_index=index, street='preflop', seat=seat,
                  action=HandAction(kind, None))
    fields.update(changes)
    return cls(**fields)
def fresh(mailbox=None):
    box = ActionMailbox() if mailbox is None else mailbox
    return HandRuntime(blueprint=ImmutableBlueprintActionSource(source_id='events-audit'),
                       mailbox=box, clock=lambda: 1000), box

def describe(runtime_obj, box, event):
    before = runtime_obj.state
    try:
        out = runtime_obj.dispatch(event)
        result = dict(status=out.status, failure=None if out.failure is None else
                      out.failure.code.value, escaped=None)
    except Exception as error:
        result = dict(status=None, failure=None, escaped=type(error).__name__,
                      message=str(error))
    result.update(accepted_mailbox_count=len(box.accepted),
                  runtime_delivery_count=runtime_obj.accepted_delivery_count,
                  state_changed=runtime_obj.state != before,
                  complete=runtime_obj.hand_complete)
    return result

def drive_flop(r):
    assert r.dispatch(started()).status == 'accepted'
    for index, seat in enumerate((3, 4, 5, 0), start=1):
        assert r.dispatch(opponent(index, seat)).status in ('accepted', 'decided')
    assert r.dispatch(opponent(5, 2, 'check')).status == 'accepted'
    return 6

def drive_showdown(r):
    index = drive_flop(r)
    for street, cards in [('flop', (1, 2, 3)), ('turn', (4,)), ('river', (5,))]:
        assert r.dispatch(StreetRevealedEvent(HAND, index, street, cards)).status == 'decided'
        index += 1
        assert r.dispatch(opponent(index, 2, 'check', street=street)).status == 'accepted'
        index += 1
    return index

# Baseline and exact top-level event schemas.
r, box = fresh()
normal = describe(r, box, started(controlled_seat=3))
assert normal['status'] == 'decided' and normal['accepted_mailbox_count'] == 1
emit('normal_controlled_hand_start', classification='control_pass', **normal)
for name, changes in [('wrong_schema', {'schema_version': 'not-the-schema'}),
                      ('nonzero_start_index', {'event_index': 7})]:
    event = started(SkipStarted, controlled_seat=3, **changes)
    rejection = refuse_base(HandStartedEvent, **dataclasses.asdict(event))
    r, box = fresh()
    result = describe(r, box, event)
    assert result['status'] == 'decided' and result['accepted_mailbox_count'] == 1
    emit('hand_start_' + name, classification='contract_breach', base_refusal=rejection,
         **result)

# Float index compares equal, then record validation occurs after real delivery.
r, box = fresh()
assert r.dispatch(started()).status == 'accepted'
for index, seat in enumerate((3, 4, 5), start=1):
    assert r.dispatch(opponent(index, seat)).status == 'accepted'
event = opponent(4.0, 0, cls=SkipOpponent)
rejection = refuse_base(OpponentActionEvent, **dataclasses.asdict(event) | {
    'action': event.action})
result = describe(r, box, event)
assert result['escaped'] == 'TypeError' and result['accepted_mailbox_count'] == 1
emit('opponent_float_index_post_delivery_escape', classification='contract_breach',
     base_refusal=rejection, **result)

# A valid outer event still admits a post-init-skipping nested HandAction.
for name, kind, amount, expected_kind in [('unknown_kind', 'bogus', 4, 'raise'),
                                        ('fold_has_amount', 'fold', 900, 'fold')]:
    action = SkipAction(kind, amount)
    rejection = refuse_base(HandAction, kind=kind, raise_to=amount)
    r, box = fresh()
    assert r.dispatch(started()).status == 'accepted'
    result = describe(r, box, opponent(1, 3, action=action))
    observed = r.state.history[-1].action
    assert result['status'] == 'accepted' and observed.kind.value == expected_kind
    emit('nested_action_' + name, classification='contract_breach', base_refusal=rejection,
         input_kind=kind, input_raise_to=amount, applied_kind=observed.kind.value,
         applied_raise_to=observed.raise_to, **result)

# Two lower-kernel invalid action routes remain closed; missing raise amount escapes.
for name, action, expected in [('raise_bool', SkipAction('raise', True), 'invalid_event'),
                               ('raise_below_minimum', SkipAction('raise', 1), 'invalid_event'),
                               ('unknown_no_amount', SkipAction('bogus', None), 'AssertionError')]:
    r, box = fresh()
    assert r.dispatch(started()).status == 'accepted'
    result = describe(r, box, opponent(1, 3, action=action))
    assert result['failure'] == expected or result['escaped'] == expected
    emit('nested_action_' + name, classification=('closed_route' if expected ==
         'invalid_event' else 'contract_breach'), **result)

# Reveal metadata bypass versus independent card validation.
for name, changes, expected in [
    ('wrong_schema', {'schema_version': 'wrong'}, 'decided'),
    ('duplicate_cards', {'cards': (1, 1, 3)}, 'failed'),
    ('private_overlap', {'cards': (0, 2, 3)}, 'failed'),
    ('boolean_card', {'cards': (True, 2, 3)}, 'failed'),
    ('list_cards', {'cards': [1, 2, 3]}, 'failed'),
    ('wrong_count', {'cards': (1, 2)}, 'failed')]:
    r, box = fresh()
    index = drive_flop(r)
    fields = dict(hand_id=HAND, event_index=index, street='flop', cards=(1, 2, 3))
    fields.update(changes)
    rejection = refuse_base(StreetRevealedEvent, **fields)
    before_count = len(box.accepted)
    result = describe(r, box, SkipReveal(**fields))
    assert result['status'] == expected
    if expected == 'failed':
        assert result['failure'] == 'invalid_event'
        assert len(box.accepted) == before_count
    emit('reveal_' + name, classification=('contract_breach' if expected == 'decided'
         else 'closed_route'), base_refusal=rejection, **result)

# Mutable strengths are retained, so public settlement depends on later input mutation.
r, box = fresh()
index = drive_showdown(r)
strengths = [None, 10, 20, None, None, None]
rejection = refuse_base(ShowdownResultEvent, hand_id=HAND, event_index=index,
                       strengths=strengths)
result = describe(r, box, SkipShowdown(HAND, index, strengths))
assert result['status'] == 'accepted' and r.hand_complete
before = r.settle().payouts
strengths[1] = 30  # only caller-owned public input list; no private/slot mutation
changed = r.settle().payouts
assert before == (0, 0, 4, 0, 0, 0) and changed == (0, 4, 0, 0, 0, 0)
emit('showdown_mutable_strengths', classification='contract_breach', base_refusal=rejection,
     payouts_before=before, payouts_after_caller_input_mutation=changed, **result)

r, box = fresh()
index = drive_showdown(r)
result = describe(r, box, SkipShowdown(HAND, index, ()))
assert result['status'] == 'accepted' and r.hand_complete
try:
    r.settle()
except ValueError as error:
    settlement_error = str(error)
else:
    raise AssertionError('empty strength vector unexpectedly settled')
emit('showdown_empty_strengths', classification='contract_breach',
     settlement_error=settlement_error, **result)

# Mailbox admission is a distinct public input even though the runtime builds base envelopes.
for name, changes in [('invalid_seat', {'seat': 99}), ('invalid_street', {'street': 'wrong'})]:
    fields = dict(hand_id=HAND, action_index=1, seat=3, street='preflop',
                  action=HandAction('call', None))
    fields.update(changes)
    rejection = refuse_base(ActionEnvelope, **fields)
    box = ActionMailbox()
    envelope = SkipEnvelope(**fields)
    receipt = box.deliver(envelope)
    assert box.accepted[(HAND, 1)] is envelope
    emit('mailbox_' + name, classification='contract_breach', base_refusal=rejection,
         acknowledgement=dataclasses.asdict(receipt), accepted_count=len(box.accepted))

box = ActionMailbox()
envelope = ActionEnvelope(HAND, 1, 3, 'preflop', SkipAction('bogus', 4))
receipt = box.deliver(envelope)
assert box.accepted[(HAND, 1)].action.kind == 'bogus'
emit('mailbox_nested_action', classification='contract_breach', accepted_count=len(box.accepted),
     acknowledged_index=receipt.action_index, accepted_action_kind=envelope.action.kind)

box = ActionMailbox()
envelope = SkipEnvelope(HAND, True, 3, 'preflop', HandAction('call', None))
try:
    box.deliver(envelope)
except TypeError as error:
    first_error = str(error)
else:
    raise AssertionError('base DeliveryReceipt should refuse True')
assert box.accepted[(HAND, True)] is envelope
try:
    box.deliver(ActionEnvelope(HAND, 1, 3, 'preflop', HandAction('call', None)))
except MailboxRejectionError:
    collision = True
else:
    collision = False
assert collision
emit('mailbox_boolean_index_partial_acceptance', classification='contract_breach',
     first_exception=first_error, accepted_count=len(box.accepted),
     subsequent_exact_index_1_rejected=collision)

# This is a real mailbox subclass. It performs real delivery before returning
# an ordinary receipt subclass; it does not falsely claim an absent delivery.
class ReceiptMailbox(ActionMailbox):
    def __init__(self, index):
        super().__init__()
        self.receipt_index = index
        self.returned_receipt = None
    def deliver(self, envelope):
        receipt = super().deliver(envelope)
        self.returned_receipt = SkipReceipt(receipt.hand_id, self.receipt_index)
        return self.returned_receipt

for name, index, expected in [('bool', True, 'decided'), ('float', 1.0, 'decided'),
                              ('mismatch', 2, 'failed')]:
    box = ReceiptMailbox(index)
    r, _ = fresh(box)
    result = describe(r, box, started(controlled_seat=3))
    assert result['status'] == expected and len(box.accepted) == 1
    if expected == 'failed':
        assert result['failure'] == 'delivery_ambiguous'
    else:
        assert type(box.returned_receipt.action_index) is not int
        assert r.accepted_delivery_count == 1
    emit('receipt_' + name, classification=('contract_breach' if expected == 'decided'
         else 'closed_route'), receipt_index_type=type(index).__name__, **result)

# V2 ticket/output objects are produced from a real spine. Its public emission
# surface accepts actions, not an externally supplied ticket or deadline.
spine = LegalDecisionSpineV2.new_hand(button=0, controlled_seat=3,
    starting_stacks=(200,) * 6, small_blind=1, big_blind=2, clock_ns=lambda: 1000)
ticket = spine.open_controlled_decision()
assert type(ticket) is ControlledDecisionTicketV2
signature = str(inspect.signature(spine.emit_controlled_action))
assert set(inspect.signature(spine.emit_controlled_action).parameters) == {'candidate', 'fallback'}
emitted = spine.emit_controlled_action(candidate=None, fallback=CALL)
assert type(emitted) is EmittedBettingActionV2 and emitted.selected == CALL
emit('v2_ticket_public_surface', classification='closed_route',
     ticket_type=type(ticket).__name__, output_type=type(emitted).__name__,
     emit_signature=signature, reason=emitted.reason.value,
     note='No ticket/deadline admission path; output representability is not a breach.')

assert not git('status', '--porcelain')
print(json.dumps({'summary': {'cases': len(CASES),
    'contract_breach_demonstrations': sum(c['classification'] == 'contract_breach' for c in CASES),
    'closed_routes': sum(c['classification'] == 'closed_route' for c in CASES),
    'snapshot_clean_after': True,
    'interpretation': 'Exit zero verifies expected observations, including defects; not a pass verdict.'}}))
