import copy,json,sys
from dataclasses import replace
from hashlib import sha256
from pontius.immutable_blueprint import ImmutableBlueprintActionSource, BlueprintDecisionKey, BlueprintActionEntry
from pontius.holdem_cards import OneSeatCardState
from pontius.no_limit_betting import NoLimitBettingState, BettingStreet
from pontius.v0a.model import ActionMailbox, HandAction
from pontius.v0a.replay import FIXTURE_A,FIXTURE_B,PROTOCOL_ID,ReplayHost,ScriptedAction,verify_successful_trace,chip_depth_settlement
from pontius.v0a.trace import parse_trace,TraceInvalidError

class Clock:
    def __init__(self,fail_at=None): self.now=1000;self.calls=0;self.fail_at=fail_at;self.armed=False
    def __call__(self):
        self.calls+=1
        if self.calls==self.fail_at or self.armed: return True
        self.now+=1000
        return self.now

policy=ImmutableBlueprintActionSource('cold-a-independent')
def run(fixture=FIXTURE_A,**kw):
    return ReplayHost(fixture,run_id=PROTOCOL_ID+'-correctness-cold-a',blueprint=kw.pop('blueprint',policy),clock=kw.pop('clock',Clock()),**kw).run()
def verify(content,fixture=FIXTURE_A,blueprint=policy):
    return verify_successful_trace(content,fixture=fixture,blueprint=blueprint,source_commit='0'*40,source_manifest_sha256='0'*64,expected_mode='correctness',expected_clock_kind='deterministic_test')

KEYS=('hand_id','event_index','action_index','street_action_index','seat','street','state_before_sha256','state_after_sha256','visible_cards_sha256','blueprint_sha256','selected_action','selection_reason','spine_reason','preparation_use')
def rows(content): return [json.loads(x) for x in content.splitlines()]
def encode(values):
    dump=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    for i,row in enumerate(values):row['record_index']=i
    sem={'events':[r['event'] for r in values if r['record_type']=='event'],'decisions':[{k:r[k] for k in KEYS} for r in values if r['record_type']=='decision'],'settlement':values[-1]['settlement']}
    values[-1]['semantic_sha256']=sha256(dump(sem)).hexdigest()
    values[-1]['trace_prefix_sha256']=sha256(b''.join(dump(r)+b'\n' for r in values[:-1])).hexdigest()
    return b''.join(dump(r)+b'\n' for r in values)

def attempt(label,content,checker=parse_trace):
    try:
        value=checker(content)
        detail={'accepted':True}
        if hasattr(value,'terminal'):detail['terminal']=value.terminal
    except TraceInvalidError as error: detail={'accepted':False,'error':str(error)}
    except BaseException as error: detail={'escaped':type(error).__name__,'error':str(error)}
    print(json.dumps({'case':label,**detail}),flush=True)
    return detail

a=run();b=run(FIXTURE_B)
assert a.receipt.passed and b.receipt.passed
assert verify(a.trace).payouts==FIXTURE_A.expected_payouts
assert verify(b.trace,FIXTURE_B).payouts==FIXTURE_B.expected_payouts
print(json.dumps({'case':'real-controls','A':a.receipt.passed,'B':b.receipt.passed}),flush=True)

# All changes begin with real host bytes. Both digests are independently rebound.
for label,mut in [
 ('source',lambda r:r[0].update(source_commit='1'*40)),
 ('illegal-check',lambda r:r[2].update(selected_action={'kind':'check','raise_to':None})),
 ('wrong-hit',lambda r:r[2].update(selection_reason='table_hit')),
 ('out-of-turn-decision',lambda r:r.insert(4,r.pop(2))),
 ('null-timing',lambda r:r[2].update(timing=None)),
 ('bad-payout',lambda r:r[-1]['settlement']['payouts'].reverse()),
 ('bad-count',lambda r:r[-1].update(decision_count=3))]:
    data=rows(a.trace);mut(data);result=attempt(label,encode(data),verify);assert result.get('accepted') is False

# Exact event ordering is an explicit schema requirement, before legal replay.
data=rows(a.trace);data[1]['event']['private_cards'].reverse()
attempt('descending-private-pair-parser',encode(data))
attempt('descending-private-pair-verifier',encode(data),verify)

# Real mailbox acceptance followed immediately by a failing witness.
clock=Clock();real=ActionMailbox()
class InterruptAfterAcceptance:
    def deliver(self,envelope):
        receipt=real.deliver(envelope);clock.armed=True;return receipt
interrupted=run(clock=clock,mailbox=InterruptAfterAcceptance())
assert len(real.accepted)==1 and not interrupted.receipt.passed
original=parse_trace(interrupted.trace)
assert original.terminal['interrupted_response_count']==1
attempt('real-interrupted-control',interrupted.trace)
for label,mut in [
 ('interrupted-claims-complete',lambda r:r[-1].update(complete=True,accounting_complete=True,preparation_compute_seconds=0.0,post_terminal_compute_seconds=0.0)),
 ('interrupted-claims-settlement',lambda r:r[-1].update(settlement=rows(a.trace)[-1]['settlement'])),
 ('terminal-forgets-hand',lambda r:r[-1].update(hand_id=None)),
 ('terminal-replaces-primary',lambda r:r[-1].update(failure_reason='invalid_event')),
 ('terminal-erases-primary',lambda r:r[-1].update(failure_reason=None))]:
    data=rows(interrupted.trace);mut(data);attempt(label,encode(data));attempt(label+'-verifier',encode(data),verify)

# A real unknown delivery preserves the accepted mailbox but loses its acknowledgement.
real_unknown=ActionMailbox()
class UnknownAfterAcceptance:
    def deliver(self,envelope):
        real_unknown.deliver(envelope);raise RuntimeError('lost acknowledgement')
unknown=run(mailbox=UnknownAfterAcceptance())
assert len(real_unknown.accepted)==1 and not unknown.receipt.passed
u=parse_trace(unknown.trace)
assert u.failures[0]['delivery_status']=='unknown'
attempt('real-unknown-control',unknown.trace)
for label,mut in [
 ('unknown-claims-complete',lambda r:r[-1].update(complete=True,accounting_complete=True,preparation_compute_seconds=0.0,post_terminal_compute_seconds=0.0)),
 ('unaccepted-failure-code-disagrees-with-timing',lambda r:next(x for x in r if x['record_type']=='failure').update(code='invalid_event'))]:
    data=rows(unknown.trace);mut(data);attempt(label,encode(data))

# Every clock fault in a real normal hand remains parseable if it yields trace bytes.
clock=Clock();run(clock=clock);count=clock.calls;errors=[];retained=0
for index in range(1,count+1):
    result=run(clock=Clock(fail_at=index))
    if result.trace:
        retained+=1
        try:parse_trace(result.trace)
        except BaseException as error:errors.append((index,type(error).__name__,str(error)))
print(json.dumps({'case':'clock-fault-prefix-parsing','observations':count,'retained_traces':retained,'errors':errors}),flush=True)

# Full real host/checker path for the independently specified dead-money/tied pot.
fixture=replace(FIXTURE_A,name='cold-a-tie-dead-money',starting_stacks=(20,)*6,
 board_text=('Tc','Jd','Qh','Ks','Ac'),hand_text=('2d 3d','4d 5d','6d 7d','8d 9d','2h 3h','4h 5h'),
 script=tuple([ScriptedAction('preflop',s,'call') for s in (4,5)]+[ScriptedAction('preflop',s,'fold') for s in (0,1,2)]+[ScriptedAction('flop',4,'call'),ScriptedAction('flop',5,'fold'),ScriptedAction('turn',4,'check'),ScriptedAction('river',4,'check')]),
 expected_payouts=(0,0,0,19,19,0),expected_pots=(38,),expected_controlled_actions=4)
state=NoLimitBettingState.new_hand(button=0,starting_stacks=(20,)*6,small_blind=1,big_blind=2)
cards=OneSeatCardState.preflop(controlled_seat=3,private_hand=fixture.deal().hand(3))
entries=[BlueprintActionEntry(BlueprintDecisionKey.from_state(cards=cards,betting=state,decision=state.legal_decision()),HandAction('raise',5).to_betting_action())]
for kind,amount in [('raise',5),('call',None),('call',None),('fold',None),('fold',None),('fold',None)]:state=state.apply_action(HandAction(kind,amount).to_betting_action())
state=state.advance_street();cards=cards.advance_to(BettingStreet.FLOP,fixture.deal().reveal_for(BettingStreet.FLOP))
entries.append(BlueprintActionEntry(BlueprintDecisionKey.from_state(cards=cards,betting=state,decision=state.legal_decision()),HandAction('raise',10).to_betting_action()))
for kind,amount in [('raise',10),('call',None),('fold',None)]:state=state.apply_action(HandAction(kind,amount).to_betting_action())
assert state.total_contributions==(0,1,2,15,15,5)
expected=chip_depth_settlement(total_contributions=state.total_contributions,folded=state.folded,starting_stacks=state.starting_stacks,strengths=(None,None,None,1,1,None),button=0)
assert expected.pots==((38,(3,4)),) and expected.payouts==(0,0,0,19,19,0)
policy_tie=ImmutableBlueprintActionSource('cold-a-tie',tuple(entries))
result=run(fixture,blueprint=policy_tie)
assert result.receipt.passed,(result.receipt,result.failures)
accepted=verify(result.trace,fixture,policy_tie)
assert accepted.pots==((38,(3,4)),) and accepted.payouts==(0,0,0,19,19,0) and accepted.final_stacks==(20,19,18,24,24,15)
print(json.dumps({'case':'real-host-independent-tied-dead-money','contributions':state.total_contributions,'payouts':accepted.payouts,'pots':accepted.pots,'final_stacks':accepted.final_stacks}),flush=True)
print(json.dumps({'case':'optional-imports','gpu_modules':[m for m in sys.modules if m=='cupy' or m.startswith('cupy.') or m=='torch' or m.startswith('torch.')]}),flush=True)
