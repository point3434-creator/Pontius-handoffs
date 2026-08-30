"""Diagnostic schedules against frozen public runtime; no candidate edits."""
import json
from unittest.mock import patch
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.holdem_cards import OneSeatCardState
from pontius.v0a.clock import ClockInvalidError
from pontius.v0a.model import ActionMailbox, HandAction, HandStartedEvent, OpponentActionEvent, StreetRevealedEvent, ShowdownResultEvent
from pontius.v0a.runtime import HandRuntime

class Clock:
    def __init__(self): self.now = 1000; self.bad = False
    def __call__(self): return True if self.bad else self.now

def start(controlled=2):
    return HandStartedEvent(hand_id='probe-hand',event_index=0,button=0,controlled_seat=controlled,starting_stacks=(200,)*6,small_blind=1,big_blind=2,private_cards=(0,13))
def runtime(controlled=2, source=None, mailbox=None, clock=None):
    clock = Clock() if clock is None else clock
    mailbox = ActionMailbox() if mailbox is None else mailbox
    source = ImmutableBlueprintActionSource('probe-blueprint') if source is None else source
    hand = HandRuntime(blueprint=source,mailbox=mailbox,clock=clock)
    first = hand.dispatch(start(controlled))
    assert first.status in ('accepted','decided')
    return hand,clock,mailbox,1

def finish_round(hand,index):
    while not hand.state.round_complete and not hand.state.is_terminal:
        state=hand.state
        decision=state.legal_decision()
        kind='check' if decision.can_check else 'call'
        outcome=hand.dispatch(OpponentActionEvent(hand_id='probe-hand',event_index=index,street=state.street.value,seat=state.acting_seat,action=HandAction(kind,None)))
        assert outcome.status in ('accepted','decided'), outcome
        index += 1
    return index

def summarize(outcome):
    return {'status':outcome.status,'code':None if outcome.failure is None else outcome.failure.code.value,
      'delivery':None if outcome.failure is None else outcome.failure.delivery_status.value,
      'elapsed_ns':None if outcome.decision is None else outcome.decision.timing.elapsed_ns,
      'wall_start_ns':None if outcome.decision is None else outcome.decision.timing.wall_start_ns,
      'deadline_crossed':None if outcome.decision is None else outcome.decision.timing.deadline_crossed}

results={}
clock=Clock(); clock.bad=True
hand=HandRuntime(blueprint=ImmutableBlueprintActionSource('initial-clock'),mailbox=ActionMailbox(),clock=clock)
try: results['invalid_initial_clock']=summarize(hand.dispatch(start()))
except Exception as error: results['invalid_initial_clock']={'escaped_exception':type(error).__name__,'message':str(error)}

hand,clock,mailbox,index=runtime(controlled=5)
clock.bad=True
try: results['invalid_later_boundary_clock']=summarize(hand.dispatch(OpponentActionEvent('probe-hand',index,'preflop',3,HandAction('fold',None))))
except Exception as error: results['invalid_later_boundary_clock']={'escaped_exception':type(error).__name__,'message':str(error)}

hand,clock,mailbox,index=runtime(controlled=1)
index=finish_round(hand,index)
arrival=clock.now
real_advance=OneSeatCardState.advance_to
def delayed_advance(self,*args,**kwargs):
    clock.now += 16_000_000_000
    return real_advance(self,*args,**kwargs)
with patch.object(OneSeatCardState,'advance_to',delayed_advance):
    outcome=hand.dispatch(StreetRevealedEvent('probe-hand',index,'flop',(20,21,22)))
results['reveal_work_before_wall']={**summarize(outcome),'event_arrival_ns':arrival,'injected_delay_ns':16_000_000_000,'real_mailbox_acceptances':len(mailbox.accepted)}

hand,clock,mailbox,index=runtime(controlled=2)
for street,cards in [('flop',(20,21,22)),('turn',(30,)),('river',(40,))]:
    index=finish_round(hand,index)
    outcome=hand.dispatch(StreetRevealedEvent('probe-hand',index,street,cards))
    assert outcome.status in ('accepted','decided')
    index += 1
index=finish_round(hand,index)
first=hand.dispatch(ShowdownResultEvent('probe-hand',index,(1,2,3,4,5,6)))
before=hand.settle()
complete_before=hand.hand_complete
second=hand.dispatch(ShowdownResultEvent('probe-hand',index+1,(6,5,4,3,2,1)))
after=hand.settle()
results['repeated_showdown']={'first':summarize(first),'complete_before_second':complete_before,'second':summarize(second),'first_payouts':before.payouts,'second_payouts':after.payouts}

real_mailbox=ActionMailbox()
class ReceiptClockFailure:
    def deliver(self,envelope):
        real_mailbox.deliver(envelope)
        raise ClockInvalidError('injected failure after actual acceptance before acknowledgement')
hand=HandRuntime(blueprint=ImmutableBlueprintActionSource('delivery-clock'),mailbox=ReceiptClockFailure(),clock=Clock())
outcome=hand.dispatch(start(controlled=3))
results['clock_exception_after_acceptance']={**summarize(outcome),'real_mailbox_acceptances':len(real_mailbox.accepted),'delivered_action':None if outcome.failure is None else str(outcome.failure.delivered_action)}

class LostAcknowledgement:
    def deliver(self,envelope): return None
hand=HandRuntime(blueprint=ImmutableBlueprintActionSource('no-ack'),mailbox=LostAcknowledgement(),clock=Clock())
results['missing_delivery_acknowledgement']=summarize(hand.dispatch(start(controlled=3)))

class ReplaceableSource:
    def __init__(self): self.source=ImmutableBlueprintActionSource('bound-at-initialization')
    @property
    def digest(self): return self.source.digest
    def action_for(self,**kwargs): return self.source.action_for(**kwargs)
source=ReplaceableSource(); initial_digest=source.digest
hand,clock,mailbox,index=runtime(controlled=5,source=source)
source.source=ImmutableBlueprintActionSource('replacement-policy')
for actor in (3,4):
    outcome=hand.dispatch(OpponentActionEvent('probe-hand',index,'preflop',actor,HandAction('call',None)))
    index+=1
results['blueprint_identity_swap']={**summarize(outcome),'initial_digest':initial_digest,'record_digest':outcome.decision.blueprint_sha256,'replacement_digest':source.digest}
print(json.dumps(results,indent=2))
