import sys
print('PREIMPORT_EXECUTABLE=' + sys.executable, flush=True)
print('PREIMPORT_IMPLEMENTATION=' + sys.implementation.name, flush=True)
print('PREIMPORT_VERSION=' + repr(sys.version), flush=True)
assert sys.executable.replace('\\', '/').lower() == sys.argv[1].replace('\\', '/').lower()
assert sys.implementation.name == 'cpython'
assert sys.version_info[:3] == tuple(int(part) for part in sys.argv[2].split('.'))
assert sys.dont_write_bytecode and sys.flags.safe_path

import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('D:/pontius-snapshots/v0a-values-spine-621bb1725663439baa809b694e3a2f07/harness')
PACKET = Path('D:/Pontius-handoffs/v0a-i01-value-boundaries/r001')
CANDIDATE = '47d08d8c1556d776358e15811e3e98b859fd6a8b'
MANIFEST = 'cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a'
assert Path.cwd() == ROOT
assert os.environ['PYTHONPATH'] == str(ROOT / 'src')
assert os.environ['PONTIUS_GIT'] == 'C:/Program Files/Git/cmd/git.exe'
def git(*args):
    return subprocess.run([os.environ['PONTIUS_GIT'], '-C', str(ROOT), *args], check=True, capture_output=True).stdout
assert git('rev-parse', 'HEAD').decode().strip() == CANDIDATE
assert not git('status', '--porcelain')
parts = git('diff-tree', '--no-renames', '-r', '-z', '--no-commit-id', '--name-status', CANDIDATE + '^', CANDIDATE).decode().split('\0')
rows = []
for i in range(0, len(parts) - 1, 2):
    status, path = parts[i:i+2]
    digest = '0' * 64 if status == 'D' else hashlib.sha256(git('cat-file', 'blob', CANDIDATE + ':' + path)).hexdigest()
    rows.append(digest + '  ' + path + '\n')
manifest_bytes = ''.join(sorted(rows)).encode()
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
assert (PACKET / 'manifest.sha256').read_bytes() == manifest_bytes
print('IDENTITY=' + json.dumps({'candidate': CANDIDATE, 'manifest': MANIFEST, 'cwd': str(ROOT), 'environment_keys': sorted(os.environ)}))

from pontius.action_clock import ActionClockSnapshot
from pontius.legal_decision_spine_v2 import ControlledDecisionTicketV2, EmittedBettingActionV2, LegalDecisionSpineV2
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import CALL, BettingActionKind, LegalBettingDecision
from pontius.v0a.model import (ActionEnvelope, ActionMailbox, DeliveryReceipt, FailureCode, HandAction, HandStartedEvent, MailboxRejectionError, OpponentActionEvent, ShowdownResultEvent, StreetRevealedEvent)
from pontius.v0a.runtime import HandRuntime
for name in ('pontius.action_clock', 'pontius.legal_decision_spine_v2', 'pontius.immutable_blueprint', 'pontius.no_limit_betting', 'pontius.v0a.model', 'pontius.v0a.runtime'):
    path = Path(sys.modules[name].__file__)
    assert path.is_relative_to(ROOT / 'src')
    print('IMPORT=' + name + '=' + str(path))
checks = []
def record(name, **detail):
    checks.append(name)
    print('PROBE=' + json.dumps({'name': name, **detail}, sort_keys=True), flush=True)
def raises(error_type, call):
    try:
        call()
    except error_type as error:
        return type(error).__name__ + ': ' + str(error)
    raise AssertionError('expected ' + repr(error_type))
class StepClock:
    def __init__(self):
        self.now = 1000
    def __call__(self):
        self.now += 1000
        return self.now
class SkippedStart(HandStartedEvent):
    def __post_init__(self): pass
class SkippedOpponent(OpponentActionEvent):
    def __post_init__(self): pass
class SkippedReveal(StreetRevealedEvent):
    def __post_init__(self): pass
class SkippedShowdown(ShowdownResultEvent):
    def __post_init__(self): pass
class SkippedAction(HandAction):
    def __post_init__(self): pass
class SkippedEnvelope(ActionEnvelope):
    def __post_init__(self): pass
class SkippedReceipt(DeliveryReceipt):
    def __post_init__(self): pass
def fields(**changes):
    values = dict(hand_id='spine-probe', event_index=0, button=0, controlled_seat=1,
                  starting_stacks=(200,) * 6, small_blind=1, big_blind=2, private_cards=(0, 13))
    values.update(changes)
    return values
def runtime(mailbox=None):
    return HandRuntime(blueprint=ImmutableBlueprintActionSource(source_id='spine-probe'),
                       mailbox=ActionMailbox() if mailbox is None else mailbox, clock=StepClock())
def opponent(index, seat, kind='fold', street='preflop'):
    return OpponentActionEvent(hand_id='spine-probe', event_index=index, street=street, seat=seat,
                               action=HandAction(kind, None))
def to_flop(rt):
    assert rt.dispatch(HandStartedEvent(**fields())).status == 'accepted'
    for index, seat in enumerate((3, 4, 5, 0), 1):
        assert rt.dispatch(opponent(index, seat)).status == ('decided' if seat == 0 else 'accepted')
    assert rt.dispatch(opponent(5, 2, 'check')).status == 'accepted'
    return 6
def to_showdown(rt):
    index = to_flop(rt)
    for street, cards in (('flop', (1, 2, 3)), ('turn', (4,)), ('river', (5,))):
        assert rt.dispatch(StreetRevealedEvent('spine-probe', index, street, cards)).status == 'decided'
        index += 1
        assert rt.dispatch(opponent(index, 2, 'check', street)).status == 'accepted'
        index += 1
    assert rt.betting_terminal
    return index

assert '__post_init__' not in ControlledDecisionTicketV2.__dict__
assert '__post_init__' not in EmittedBettingActionV2.__dict__
invalid_ticket = ControlledDecisionTicketV2(decision='not a decision', deadline=None)
invalid_emitted = EmittedBettingActionV2(seat=True, candidate=None, fallback=None, selected=None,
                                        reason='not a reason', used_fallback='not bool', deadline=None)
for value in (invalid_ticket, invalid_emitted):
    rejected = runtime().dispatch(value)
    assert rejected.status == 'failed' and rejected.failure.code is FailureCode.INVALID_EVENT
spine = LegalDecisionSpineV2.new_hand(button=0, controlled_seat=3, starting_stacks=(200,) * 6,
                                    small_blind=1, big_blind=2, clock_ns=StepClock())
ticket = spine.open_controlled_decision()
emitted = spine.emit_controlled_action(candidate=None, fallback=CALL)
assert type(ticket) is ControlledDecisionTicketV2 and type(ticket.decision) is LegalBettingDecision
assert type(ticket.deadline) is ActionClockSnapshot and type(emitted) is EmittedBettingActionV2
assert emitted.selected == CALL and spine.state.history[-1].action == CALL
record('spine_outputs_no_skipped_validator_or_runtime_input',
       fabricated_values_rejected='invalid_event', normal_ticket=type(ticket).__name__,
       normal_emission=type(emitted).__name__,
       open_signature=str(inspect.signature(LegalDecisionSpineV2.open_controlled_decision)),
       emit_signature=str(inspect.signature(LegalDecisionSpineV2.emit_controlled_action)))

for changes in ({'schema_version': 'wrong-schema'}, {'event_index': 7}):
    baseline = raises((TypeError, ValueError), lambda: HandStartedEvent(**fields(**changes)))
    rt = runtime()
    outcome = rt.dispatch(SkippedStart(**fields(**changes)))
    assert outcome.status == 'accepted' and rt.state.acting_seat == 3
    record('start_validation_skipped', fields=changes, base_refusal=baseline, runtime_status=outcome.status)
rt = runtime()
assert rt.dispatch(HandStartedEvent(**fields())).status == 'accepted'
baseline = raises(TypeError, lambda: OpponentActionEvent('spine-probe', True, 'preflop', 3, HandAction('fold', None)))
outcome = rt.dispatch(SkippedOpponent('spine-probe', True, 'preflop', 3, HandAction('fold', None)))
assert outcome.status == 'accepted' and rt.state.folded[3]
record('opponent_bool_index_admitted', base_refusal=baseline, runtime_status=outcome.status,
       history_seat=rt.state.history[-1].seat, history_action=rt.state.history[-1].action.kind.value)
rt = runtime()
assert rt.dispatch(HandStartedEvent(**fields())).status == 'accepted'
baseline = raises(ValueError, lambda: HandAction('dance', 4))
invalid_action = SkippedAction('dance', 4)
outcome = rt.dispatch(OpponentActionEvent('spine-probe', 1, 'preflop', 3, invalid_action))
assert outcome.status == 'accepted' and rt.state.history[-1].action.kind is BettingActionKind.RAISE
assert rt.state.history[-1].action.raise_to == 4
record('nested_action_invalid_kind_becomes_real_raise', base_refusal=baseline,
       event_exact=True, runtime_status=outcome.status, history_action='raise', raise_to=4)
rt = runtime()
assert rt.dispatch(HandStartedEvent(**fields())).status == 'accepted'
bad = SkippedOpponent('spine-probe', 1, 'preflop', 3, 'not an action')
escaped = raises(AttributeError, lambda: rt.dispatch(bad))
record('malformed_event_escapes_typed_refusal', exception=escaped)
rt = runtime()
index = to_flop(rt)
baseline = raises(ValueError, lambda: StreetRevealedEvent('spine-probe', index, 'flop', (1, 2, 3), 'wrong-schema'))
outcome = rt.dispatch(SkippedReveal('spine-probe', index, 'flop', (1, 2, 3), 'wrong-schema'))
assert outcome.status == 'decided' and rt.state.street.value == 'flop'
record('reveal_schema_skipped_and_action_delivered', base_refusal=baseline,
       runtime_status=outcome.status, delivered_count=rt.accepted_delivery_count)
rt = runtime()
index = to_showdown(rt)
strengths = [None, 1, 2, None, None, None]
baseline = raises(ValueError, lambda: ShowdownResultEvent('spine-probe', index, strengths))
outcome = rt.dispatch(SkippedShowdown('spine-probe', index, strengths))
assert outcome.status == 'accepted' and rt.hand_complete
before = rt.settle().payouts
strengths[1] = 3
later = rt.settle().payouts
assert before == (0, 0, 4, 0, 0, 0) and later == (0, 4, 0, 0, 0, 0)
record('admitted_mutable_showdown_changes_settlement_without_event', base_refusal=baseline,
       runtime_status=outcome.status, hand_complete=rt.hand_complete, payouts_before=before, payouts_after=later)
rt = runtime()
index = to_showdown(rt)
outcome = rt.dispatch(SkippedShowdown('spine-probe', index, ()))
assert outcome.status == 'accepted' and rt.hand_complete
failure = raises(ValueError, rt.settle)
record('empty_showdown_accepted_then_settlement_fails', runtime_status=outcome.status,
       hand_complete=rt.hand_complete, settlement_exception=failure)
mailbox = ActionMailbox()
baseline = raises(ValueError, lambda: ActionEnvelope('mail', 1, 99, 'preflop', HandAction('call', None)))
invalid = SkippedEnvelope('mail', 1, 99, 'preflop', HandAction('call', None))
receipt = mailbox.deliver(invalid)
assert mailbox.accepted[('mail', 1)] is invalid and receipt.action_index == 1
record('mailbox_admits_unvalidated_envelope', base_refusal=baseline, accepted_seat=99,
       receipt_type=type(receipt).__name__)
mailbox = ActionMailbox()
baseline = raises(TypeError, lambda: ActionEnvelope('alias', True, 1, 'preflop', HandAction('call', None)))
invalid = SkippedEnvelope('alias', True, 1, 'preflop', HandAction('call', None))
escaped = raises(TypeError, lambda: mailbox.deliver(invalid))
assert mailbox.accepted[('alias', 1)] is invalid
collision = raises(MailboxRejectionError, lambda: mailbox.deliver(ActionEnvelope('alias', 1, 1, 'preflop', HandAction('call', None))))
record('mailbox_invalid_identity_stored_before_receipt_failure', base_refusal=baseline,
       delivery_exception=escaped, stored_key_index_type=type(next(iter(mailbox.accepted))[1]).__name__,
       subsequent_valid_delivery_exception=collision)
class ForwardingMailbox:
    def __init__(self):
        self.real = ActionMailbox()
        self.received = []
    def deliver(self, envelope):
        real_receipt = self.real.deliver(envelope)
        # Genuine mailbox acceptance occurs first; this is not a delivery lie.
        returned = SkippedReceipt(real_receipt.hand_id, bool(real_receipt.action_index))
        self.received.append(returned)
        return returned
forwarder = ForwardingMailbox()
rt = runtime(forwarder)
outcome = rt.dispatch(HandStartedEvent(**fields(controlled_seat=3)))
assert outcome.status == 'decided' and outcome.failure is None
assert rt.accepted_delivery_count == 1 and len(forwarder.real.accepted) == 1
assert type(forwarder.received[0].action_index) is bool
baseline = raises(TypeError, lambda: DeliveryReceipt('spine-probe', True))
record('runtime_admits_malformed_receipt_after_genuine_delivery', base_refusal=baseline,
       runtime_status=outcome.status, receipt_index_type='bool', accepted_delivery_count=1,
       real_mailbox_count=len(forwarder.real.accepted))
assert not git('status', '--porcelain')
print('RESULT=' + json.dumps({'diagnostic_assertions': 'passed', 'probe_count': len(checks),
                             'source_worktree_clean': True, 'product_verdict': 'not_clean'}))