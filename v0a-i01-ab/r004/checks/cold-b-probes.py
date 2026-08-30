import dataclasses, json, os, pathlib, platform, subprocess, sys
root=pathlib.Path.cwd()
assert platform.python_implementation()=='CPython'
assert platform.python_version()==os.environ['COLD_B_EXPECTED_VERSION']
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert os.environ['PYTHONPATH']==str(root/'src') and os.environ['PATH']==''
print(json.dumps({'identity':platform.python_version(),'executable':sys.executable,'cwd':str(root)}))
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a import model, runtime as runtime_module
from pontius.v0a.model import (ActionEnvelope,ActionMailbox,DeliveryReceipt,DeliveryStatus,
 FailureCode,HandAction,HandStartedEvent,MailboxRejectionError,OpponentActionEvent,
 ShowdownResultEvent,StreetRevealedEvent)
from pontius.v0a.runtime import HandRuntime
for module in (model,runtime_module):
 assert pathlib.Path(module.__file__).is_relative_to(root/'src')
print(json.dumps({'origins':{m.__name__:m.__file__ for m in (model,runtime_module)}}))
H='cold-b-hand'
C=HandAction('call',None)
K=HandAction('check',None)
class Clock:
 def __init__(self, bad_at=None):
  self.reads=[]
  self.bad_at=bad_at
 def __call__(self):
  value=(len(self.reads)+1)*1_000_000
  if len(self.reads)+1==self.bad_at: value=True
  self.reads.append(value)
  return value

def make(clock=None,mailbox=None):
 box=ActionMailbox() if mailbox is None else mailbox
 runtime=HandRuntime(blueprint=ImmutableBlueprintActionSource('cold-b-empty'),mailbox=box,
                     clock=Clock() if clock is None else clock)
 return runtime,box

def start(**changes):
 values=dict(hand_id=H,event_index=0,button=0,controlled_seat=3,starting_stacks=(100,)*6,
             small_blind=1,big_blind=2,private_cards=(0,13))
 values.update(changes)
 return HandStartedEvent(**values)

def unchecked(value,**changes):
 kind=type(value)
 subtype=type('Unchecked'+kind.__name__,(kind,),{'__post_init__':lambda self:None})
 values={field.name:getattr(value,field.name) for field in dataclasses.fields(kind)}
 values.update(changes)
 return subtype(**values)

def frame(runtime,box):
 state=runtime.state
 if state is not None:
  assert sum(state.stacks)+sum(state.total_contributions)==600
 return {'street':None if state is None else state.street.value,
         'history':0 if state is None else len(state.history),
         'chips':None if state is None else sum(state.stacks)+sum(state.total_contributions),
         'physical_deliveries':len(box.accepted),'known':runtime.accepted_delivery_count,
         'complete':runtime.hand_complete}

def advance_round(runtime,index,fold=False):
 while not runtime.state.round_complete and not runtime.state.is_terminal:
  state=runtime.state
  assert state.acting_seat!=3
  action=(HandAction('fold',None) if fold and state.street.value=='preflop'
          and state.acting_seat==4 else K if state.legal_decision().can_check else C)
  event=OpponentActionEvent(H,index,state.street.value,state.acting_seat,action)
  out=runtime.dispatch(event)
  assert out.status in ('accepted','decided'),out
  index+=1
 return index

def prepared(kind,fold=False):
 runtime,box=make()
 if kind=='start': return runtime,box,start()
 assert runtime.dispatch(start()).status=='decided'
 if kind=='opponent': return runtime,box,OpponentActionEvent(H,1,'preflop',4,C)
 index=advance_round(runtime,1,fold=fold)
 if kind=='reveal': return runtime,box,StreetRevealedEvent(H,index,'flop',(20,21,22))
 for street,cards in (('flop',(20,21,22)),('turn',(30,)),('river',(40,)):
  out=runtime.dispatch(StreetRevealedEvent(H,index,street,cards))
  assert out.status in ('accepted','decided'),out
  index=advance_round(runtime,index+1,fold=fold)
 ranks=tuple(None if seat not in runtime.state.live_seats else seat for seat in range(6))
 return runtime,box,ShowdownResultEvent(H,index,ranks)

observations=[]
def note(name,**values):
 observations.append({'case':name,**values})
 print(json.dumps(observations[-1],sort_keys=True))

def reject(name,runtime,box,event,code=FailureCode.INVALID_EVENT,admitted=False):
 state_before=runtime.state
 accepted_before=box.accepted
 before=frame(runtime,box)
 outcome=runtime.dispatch(event)
 assert outcome.status=='failed',outcome
 assert outcome.failure.code is code,outcome
 assert outcome.failure.delivery_status is DeliveryStatus.NOT_ATTEMPTED
 assert outcome.decision is None
 assert outcome.failure.event_index==(event.event_index if admitted else None)
 assert runtime.state==state_before
 assert box.accepted==accepted_before
 assert not runtime.hand_complete
 after=frame(runtime,box)
 assert before==after,(before,after)
 note(name,outcome=outcome.status,code=outcome.failure.code.value,
      failure_event=outcome.failure.event_index,before=before,after=after)

for kind in ('start','opponent','reveal','showdown'):
 for label,changes in (('valid-subclass',{}),('wrong-schema',{'schema_version':'wrong'}),
                       ('bool-index',{'event_index':True}),('float-index',{'event_index':1.0}),
                       ('bad-id',{'hand_id':[]}),('negative-index',{'event_index':-1})):
  r,b,event=prepared(kind)
  reject(kind+'/'+label,r,b,unchecked(event,**changes))

for label,action in (('bad-kind',unchecked(C,kind='pay')),('bool-raise',
 unchecked(HandAction('raise',6),raise_to=True)),('float-raise',
 unchecked(HandAction('raise',6),raise_to=6.0)),('valid-subclass',unchecked(C))):
 r,b,event=prepared('opponent')
 reject('opponent/exact-outer/'+label,r,b,dataclasses.replace(event,action=action))

r,b,event=prepared('start')
reject('start/exact-insufficient-stack',r,b,dataclasses.replace(event,starting_stacks=(1,)*6),
       admitted=True)
for kind,label,changes in (('opponent','wrong-actor',{'seat':5}),
 ('opponent','wrong-street',{'street':'turn'}),('opponent','wrong-id',{'hand_id':'other'}),
 ('opponent','skipped-index',{'event_index':9}),('reveal','known-card-overlap',{'cards':(0,21,22)})):
 r,b,event=prepared(kind)
 reject(kind+'/exact/'+label,r,b,dataclasses.replace(event,**changes),
        code=FailureCode.INVALID_EVENT if label=='known-card-overlap' else FailureCode.EVENT_ORDER,
        admitted=True)

for label,ranks in (('list',list(range(6))),('empty',()),('empty-rank',(0,1,2,3,4,())),
 ('bool-rank',(0,1,2,3,4,True)),('float-rank',(0,1,2,3,4,5.0))):
 r,b,event=prepared('showdown')
 reject('showdown/'+label,r,b,unchecked(event,strengths=ranks))
 if type(ranks) is list:
  ranks[0]=10000
  assert not r.hand_complete
  try: r.settle()
  except RuntimeError: pass
  else: raise AssertionError('rejected mutable ranks settled')
for label,ranks in (('mixed-domains',(0,1,2,3,4,(5,))),
 ('missing-live',(0,1,2,3,4,None))):
 r,b,event=prepared('showdown')
 reject('showdown/exact/'+label,r,b,dataclasses.replace(event,strengths=ranks),admitted=True)
r,b,event=prepared('showdown',fold=True)
reject('showdown/exact/folded-has-rank',r,b,dataclasses.replace(event,strengths=tuple(range(6))),
       admitted=True)

for fold in (False,True):
 for domain in ('int','tuple','tuple-prefix','tied'):
  r,b,event=prepared('showdown',fold=fold)
  ranks=tuple(None if seat not in r.state.live_seats else
              seat if domain=='int' else (seat,) if domain=='tuple' else
              (1,)* (seat+1) if domain=='tuple-prefix' else 9 for seat in range(6))
  before=frame(r,b)
  assert r.dispatch(dataclasses.replace(event,strengths=ranks)).status=='accepted'
  assert r.hand_complete
  first=r.settle()
  # Every live seat contributes two, folded seat 4 contributes zero. No side pots.
  pot=10 if fold else 12
  if domain=='tied': expected=tuple(0 if fold and i==4 else 2 for i in range(6))
  else: expected=(0,0,0,0,0,pot)
  assert first.payouts==expected,(first,expected)
  assert sum(first.payouts)==pot and sum(first.final_stacks)==600
  assert r.settle()==first
  assert len(b.accepted)==before['physical_deliveries']
  note('showdown/control/'+str(fold)+'/'+domain,payouts=first.payouts,
       final_stacks=first.final_stacks,total_chips=sum(first.final_stacks),
       deliveries=len(b.accepted),repeat_stable=True)

for bad_at,expected in ((None,['invalid_event']),(1,['clock_invalid']),
                         (2,['clock_invalid']),(3,['invalid_event','clock_invalid'])):
 clock=Clock(bad_at=bad_at)
 r,b=make(clock=clock)
 out=r.dispatch(unchecked(start(),hand_id=[]))
 assert out.status=='failed' and out.failure.event_index is None
 codes=[x.value for x in r.closure_failures]
 assert codes==expected,(bad_at,codes)
 assert r.state is None and not b.accepted and not r.hand_complete
 if bad_at is None:
  assert clock.reads==[1_000_000,2_000_000,3_000_000]
  assert r.accounting().preparation_compute_seconds==0.001
 note('clock/invalid-admission/'+str(bad_at),reads=clock.reads,cause_order=codes,
      accounting_complete=r.accounting().complete)

class Hostile:
 hits=0
 @property
 def event_index(self):
  type(self).hits+=1
  raise AssertionError('unadmitted event index touched')
 @property
 def hand_id(self):
  type(self).hits+=1
  raise AssertionError('unadmitted hand id touched')
for mode in ('fresh','dead','complete','clock'):
 if mode=='complete':
  r,b,event=prepared('showdown')
  assert r.dispatch(event).status=='accepted'
 else:
  r,b=make(clock=Clock(bad_at=1) if mode=='clock' else None)
  if mode=='dead': r.dispatch(object())
 state_before=r.state
 accepted_before=b.accepted
 out=r.dispatch(Hostile())
 assert out.status=='failed' and out.failure.event_index is None
 assert r.state==state_before and b.accepted==accepted_before and Hostile.hits==0
 note('metadata/'+mode,code=out.failure.code.value,callback_hits=Hostile.hits)

good=ActionEnvelope(H,1,3,'preflop',C)
for label,changes in (('valid-subclass',{}),('bool-index',{'action_index':True}),
 ('float-index',{'action_index':1.0}),('negative-index',{'action_index':-1}),
 ('bool-seat',{'seat':True}),('float-seat',{'seat':3.0}),('bad-seat',{'seat':8}),
 ('bad-street',{'street':'wrong'}),('bad-id',{'hand_id':[]}),
 ('bad-action',{'action':unchecked(C,kind='invalid')})):
 b=ActionMailbox()
 try: b.deliver(unchecked(good,**changes))
 except MailboxRejectionError: pass
 else: raise AssertionError(label)
 assert b.accepted=={}
 receipt=b.deliver(good)
 assert type(receipt) is DeliveryReceipt and receipt.action_index==1
 assert b.accepted=={(H,1):good}
 try: b.deliver(good)
 except MailboxRejectionError: pass
 else: raise AssertionError('duplicate accepted')
 assert b.accepted=={(H,1):good}
 note('envelope/'+label,rejected_before_insert=True,valid_reuse=True,accepted_count=1,
      duplicate_refused=True)
for label,nested in (('bad',unchecked(C,kind='x')),('valid-subclass',unchecked(C))):
 b=ActionMailbox()
 try: b.deliver(dataclasses.replace(good,action=nested))
 except MailboxRejectionError: pass
 else: raise AssertionError('nested admitted')
 assert b.accepted=={}
 b.deliver(good)
 note('envelope/exact-outer/'+label,rejected_before_insert=True,valid_reuse=True)

factories=(('subclass',lambda r:unchecked(r)),('bool',lambda r:unchecked(r,action_index=True)),
 ('float',lambda r:unchecked(r,action_index=1.0)),('bad-id',lambda r:unchecked(r,hand_id=[])),
 ('wrong-exact-index',lambda r:DeliveryReceipt(H,2)),
 ('wrong-exact-id',lambda r:DeliveryReceipt('other',1)),('foreign',lambda r:Hostile()),
 ('none',lambda r:None),('valid',lambda r:r))
for label,factory in factories:
 real=ActionMailbox()
 class Forward:
  def __init__(self): self.calls=0
  def deliver(self,envelope):
   self.calls+=1
   receipt=real.deliver(envelope)
   return factory(receipt)
 forward=Forward()
 r,_=make(mailbox=forward)
 out=r.dispatch(start())
 assert len(real.accepted)==1 and forward.calls==1
 assert len(r.state.history)==1 and r.state.history[0].seat==3
 assert r.state.total_contributions==(0,1,2,2,0,0)
 assert sum(r.state.stacks)+sum(r.state.total_contributions)==600
 if label=='valid':
  assert out.status=='decided' and r.accepted_delivery_count==1
  note('receipt/'+label,physical=1,attempts=1,known=1,state_history=1,total_chips=600)
 else:
  assert out.status=='failed' and out.failure.code is FailureCode.DELIVERY_AMBIGUOUS
  assert out.failure.delivery_status is DeliveryStatus.UNKNOWN
  assert out.failure.delivered_action is None and r.accepted_delivery_count==0
  state_before=r.state
  second=r.dispatch(OpponentActionEvent(H,1,'preflop',4,C))
  assert second.status=='failed' and r.state==state_before and forward.calls==1
  note('receipt/'+label,physical=1,attempts=1,known=0,status='unknown',
       state_history=1,total_chips=600,no_retry=True)

# Known real acceptance followed by a clock fault keeps known count and action.
real=ActionMailbox()
clock=Clock()
class KillAfter:
 def deliver(self,envelope):
  receipt=real.deliver(envelope)
  clock.bad_at=len(clock.reads)+1
  return receipt
r,_=make(clock=clock,mailbox=KillAfter())
out=r.dispatch(start())
assert out.status=='failed' and out.failure.code is FailureCode.CLOCK_INVALID
assert out.failure.delivery_status is DeliveryStatus.ACCEPTED
assert out.decision is not None and out.failure.delivered_action==C
assert len(real.accepted)==1 and r.accepted_delivery_count==1
note('receipt/known-then-clock-fault',physical=1,known=1,full_decision=True,
     cause_order=[x.value for x in r.closure_failures])

git=os.environ['PONTIUS_GIT']
clean=subprocess.run([git,'-C',str(root),'status','--porcelain=v1'],check=True,
                     capture_output=True).stdout
assert clean==b'',clean
print(json.dumps({'result':'PASS','observations':len(observations),'snapshot_clean':True}))
