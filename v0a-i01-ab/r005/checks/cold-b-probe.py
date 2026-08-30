import hashlib, json, os, pathlib, platform, sys
from dataclasses import replace
root = pathlib.Path.cwd().resolve()
assert root.drive.upper() == 'D:' and root.name.startswith('v0a-i01-ab-r005-cold-b-')
assert sys.flags.safe_path and sys.flags.dont_write_bytecode
from pontius.v0a import model, replay, trace, runtime
from pontius.v0a.model import ActionMailbox, HandAction, HandStartedEvent
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, Fixture, ScriptedAction, ReplayHost, PROTOCOL_ID
from pontius.no_limit_betting import NoLimitBettingState, BettingStreet
from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import ImmutableBlueprintActionSource, BlueprintDecisionKey, BlueprintActionEntry
assert all(pathlib.Path(m.__file__).resolve().is_relative_to(root/'src') for m in (model,replay,trace,runtime))
class Clock:
    def __init__(self): self.now = 1000; self.fail = False
    def __call__(self):
        if self.fail: return True
        self.now += 1000
        return self.now
policy = ImmutableBlueprintActionSource('cold-b-policy')
def host(fixture=FIXTURE_A, clock=None, mailbox=None, policy=policy):
    opts = dict(blueprint=policy, clock=clock or Clock(), run_id=PROTOCOL_ID+'-correctness-cold-b')
    if mailbox is not None: opts['mailbox'] = mailbox
    return ReplayHost(fixture, **opts).run()
def verify(content, fixture=FIXTURE_A, policy=policy):
    return replay.verify_successful_trace(content,fixture=fixture,blueprint=policy,
        source_commit='0'*40,source_manifest_sha256='0'*64,
        expected_mode='correctness',expected_clock_kind='deterministic_test')
keys = ('hand_id','event_index','action_index','street_action_index','seat','street',
        'state_before_sha256','state_after_sha256','visible_cards_sha256','blueprint_sha256',
        'selected_action','selection_reason','spine_reason','preparation_use')
def encode(rows):
    dumps = lambda x: json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
    for i,row in enumerate(rows): row['record_index']=i
    semantic = {'events':[r['event'] for r in rows if r['record_type']=='event'],
                'decisions':[{k:r[k] for k in keys} for r in rows if r['record_type']=='decision'],
                'settlement':rows[-1]['settlement']}
    rows[-1]['semantic_sha256']=hashlib.sha256(dumps(semantic).encode()).hexdigest()
    rows[-1]['trace_prefix_sha256']=hashlib.sha256((''.join(dumps(r)+'\n' for r in rows[:-1])).encode()).hexdigest()
    return ''.join(dumps(r)+'\n' for r in rows).encode()
def mutate(content, change):
    rows=[json.loads(x) for x in content.splitlines()]
    change(rows)
    return encode(rows)
def result(fn):
    try:
        obj=fn()
        return {'accepted':True}
    except trace.TraceInvalidError as e:
        return {'accepted':False,'type':type(e).__name__,'message':str(e)}
observations=[]
def record(name, content, **extra):
    observations.append({'name':name,'parse':result(lambda:trace.parse_trace(content)),
        'verify':result(lambda:verify(content)),**extra})
    return observations[-1]
base=host()
assert base.receipt.passed
assert verify(base.trace).payouts == (0,0,0,12,0,0)
assert verify(host(FIXTURE_B).trace,FIXTURE_B).payouts == (16,10,24,30,0,0)
record('baseline_A',base.trace)
reverse=mutate(base.trace,lambda rows:rows[1]['event']['private_cards'].reverse())
rows=[json.loads(x) for x in reverse.splitlines()]
event=rows[1]['event']
model_result=None
try: HandStartedEvent(**{k:v if k!='private_cards' and k!='starting_stacks' else tuple(v)
                        for k,v in event.items() if k not in ('kind',)})
except ValueError as e: model_result=str(e)
assert model_result == 'private cards must be two distinct ascending cards'
item=record('descending_private_pair',reverse,private_cards=event['private_cards'],model_rejection=model_result)
assert item['parse']['accepted'] and not item['verify']['accepted']
# Real mailbox acceptance followed by a real witness failure generates an honest failed prefix.
clock=Clock(); mailbox=ActionMailbox()
class BreakAfterAcceptance:
    def deliver(self,envelope):
        receipt=mailbox.deliver(envelope); clock.fail=True; return receipt
failed=host(clock=clock,mailbox=BreakAfterAcceptance())
assert len(mailbox.accepted)==1 and not failed.receipt.passed
parsed=trace.parse_trace(failed.trace)
assert parsed.terminal['interrupted_response_count']==1
record('honest_accepted_interruption',failed.trace,
       terminal=dict(parsed.terminal),known_mailbox_acceptances=len(mailbox.accepted))
for name,change in [
    ('interrupted_claims_complete_accounting',lambda rows:rows[-1].update(complete=True,accounting_complete=True)),
    ('interrupted_erases_primary_reason',lambda rows:rows[-1].update(failure_reason=None)),
    ('interrupted_replaces_primary_reason',lambda rows:rows[-1].update(failure_reason='invalid_event')),
    ('failed_prefix_carries_settlement',lambda rows:rows[-1].update(settlement=json.loads(base.trace.splitlines()[-1])['settlement']))]:
    item=record(name,mutate(failed.trace,change))
    assert item['parse']['accepted'] and not item['verify']['accepted']
# Independent boundary probes with both hashes rebound.
for name,change in [
    ('illegal_first_check',lambda rows:next(r for r in rows if r['record_type']=='decision').update(selected_action={'kind':'check','raise_to':None})),
    ('foreign_source',lambda rows:rows[0].update(source_commit='1'*40)),
    ('false_delivery_count',lambda rows:rows[-1].update(decision_count=0)),
    ('foreign_payout',lambda rows:rows[-1]['settlement']['payouts'].reverse()),
    ('unknown_event_key',lambda rows:rows[1]['event'].update(timestamp=1)),
    ('boolean_record_index',lambda rows:rows[0].update(source_commit=[]))]:
    item=record(name,mutate(base.trace,change))
    assert not item['verify']['accepted']
# Independent complete tied-board host control for the new oracle dependency.
f=replace(FIXTURE_A,name='cold-b-folded-depths',hand_id='cold-b-folded-depths',
    starting_stacks=(20,)*6,board_text=('Tc','Jc','Qc','Kc','Ac'),
    hand_text=('2d 3d','4d 5d','6d 7d','8d 9d','2h 3h','4h 5h'),
    script=(ScriptedAction('preflop',4,'call'),ScriptedAction('preflop',5,'call'),
            ScriptedAction('preflop',0,'fold'),ScriptedAction('preflop',1,'fold'),
            ScriptedAction('preflop',2,'fold'),ScriptedAction('flop',4,'call'),
            ScriptedAction('flop',5,'fold'),ScriptedAction('turn',4,'check'),
            ScriptedAction('river',4,'check')),
    expected_payouts=(0,0,0,19,19,0),expected_pots=(38,),expected_controlled_actions=4)
state=NoLimitBettingState.new_hand(button=0,starting_stacks=(20,)*6,small_blind=1,big_blind=2)
cards=OneSeatCardState.preflop(controlled_seat=3,private_hand=f.deal().hand(3))
def entry(state,cards,amount):
    return BlueprintActionEntry(BlueprintDecisionKey.from_state(cards=cards,betting=state,decision=state.legal_decision()),
                                HandAction('raise',amount).to_betting_action())
entries=[entry(state,cards,5)]
for kind,amount in [('raise',5),('call',None),('call',None),('fold',None),('fold',None),('fold',None)]:
    state=state.apply_action(HandAction(kind,amount).to_betting_action())
state=state.advance_street(); cards=cards.advance_to(BettingStreet.FLOP,f.deal().reveal_for(BettingStreet.FLOP))
entries.append(entry(state,cards,10))
for kind,amount in [('raise',10),('call',None),('fold',None)]:
    state=state.apply_action(HandAction(kind,amount).to_betting_action())
assert state.total_contributions==(0,1,2,15,15,5) and state.live_seats==(3,4)
# Both live players cover every depth. All 38 chips form their single eligibility group.
expected_pots=((sum(state.total_contributions),(3,4)),)
assert expected_pots==((38,(3,4)),)
oracle=replay.chip_depth_settlement(total_contributions=state.total_contributions,folded=state.folded,
    starting_stacks=state.starting_stacks,strengths=(None,None,None,1,1,None),button=0)
assert oracle.pots==expected_pots and oracle.payouts==(0,0,0,19,19,0)
assert oracle.final_stacks==(20,19,18,24,24,15)
tied_policy=ImmutableBlueprintActionSource('cold-b-depth-policy',entries=tuple(entries))
tied=host(f,policy=tied_policy)
assert tied.receipt.passed, tied.failures
seen=[]
forbidden={ReplayHost.run.__code__,runtime.HandRuntime.dispatch.__code__,
           runtime.select_blueprint_action.__code__,runtime._select_admitted_blueprint_action.__code__}
def observe(frame,event,arg):
    if event=='call' and frame.f_code in forbidden: seen.append(frame.f_code.co_name)
sys.setprofile(observe)
try: verified=verify(tied.trace,f,tied_policy)
finally: sys.setprofile(None)
assert seen==[] and verified.pots==expected_pots and verified.payouts==(0,0,0,19,19,0)
observations.append({'name':'real_tied_folded_depth_host_and_checker','accepted':True,
    'payouts':verified.payouts,'final_stacks':verified.final_stacks,'pots':verified.pots,
    'checker_forbidden_producer_calls':seen})
print(json.dumps({'version':platform.python_version(),'executable':sys.executable,'snapshot':str(root),
    'modules':{m.__name__:m.__file__ for m in (trace,replay,model,runtime)},'observations':observations},indent=2))
