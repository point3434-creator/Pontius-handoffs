import json,os,pathlib,platform,subprocess,sys
SNAPSHOT=pathlib.Path('D:/Pontius-review-snapshots/cold-a-v0a-i01-ab-r005-20260830')
CHECKS=pathlib.Path(__file__).parent
if len(sys.argv)==1:
    env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP') if k in os.environ}
    env.update(PYTHONPATH=str(SNAPSHOT/'src'),PYTHONNOUSERSITE='1',PONTIUS_GIT='C:/Program Files/Git/cmd/git.exe')
    for slot,python,version in [('311','D:/Pontius-tools/py311/Scripts/python.exe','3.11.15'),('314','D:/Pontius/.venv/Scripts/python.exe','3.14.6')]:
        cmd=[python,'-B','-P',__file__,'--payload',version]
        result=subprocess.run(cmd,cwd=SNAPSHOT,env=env,capture_output=True,text=True)
        receipt={'command':cmd,'cwd':str(SNAPSHOT),'environment':env,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
        path=CHECKS/f'cold-a-terminal-causes-v2-{slot}.json'
        with path.open('x',encoding='utf-8',newline='\n') as file:json.dump(receipt,file,indent=2);file.write('\n')
        print(json.dumps({'slot':slot,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr}),flush=True)
    raise SystemExit(0)
print(json.dumps({'version':platform.python_version(),'implementation':platform.python_implementation(),'executable':sys.executable,'cwd':os.getcwd(),'flags':str(sys.flags)}),flush=True)
assert platform.python_version()==sys.argv[2] and sys.flags.dont_write_bytecode and sys.flags.safe_path
from dataclasses import replace
from pontius.v0a.clock import MonotonicWitness,ClockInvalidError,ClockReversedError
from pontius.v0a.model import ActionMailbox
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import ReplayHost,FIXTURE_A,PROTOCOL_ID,ScriptedAction,chip_depth_settlement
from pontius.v0a.trace import parse_trace
class Source:
    def __init__(self):self.now=10000;self.kind=None;self.fail_at=None;self.calls=0;self.events=[]
    def __call__(self):
        self.calls+=1
        if self.kind is not None or self.calls==self.fail_at:
            self.events.append('source_'+str(self.kind or 'invalid'))
            if self.kind=='reversed':return self.now-5000
            return True
        self.now+=1000;return self.now
policy=ImmutableBlueprintActionSource('stage0-causes')
def output(label,host,outcome,source,accepted=None):
    parsed=parse_trace(outcome.trace)
    value={'case':label,'source_occurrences':source.events,'terminal':parsed.terminal['failure_reason'],'receipt_primary':str(outcome.receipt.failure_reason),'secondary':list(outcome.receipt.secondary_failures),'failures':[{'code':row['code'],'delivery_status':row['delivery_status'],'timing_status':None if row['timing'] is None else row['timing']['status'],'interruption_reason':None if row['timing'] is None else row['timing']['interruption_reason']} for row in parsed.failures]}
    if accepted is not None:value['real_mailbox_acceptances']=len(accepted.accepted)
    print(json.dumps(value),flush=True)
for kind in ('invalid','reversed'):
    for finish in ('return','raise','reject'):
        source=Source();witness=MonotonicWitness(source);real=ActionMailbox()
        class Mailbox:
            def deliver(self,envelope):
                receipt=real.deliver(envelope) if finish!='reject' else None
                source.kind=kind
                try:witness()
                except (ClockInvalidError,ClockReversedError):pass
                if finish=='raise':raise RuntimeError('body after source')
                if finish=='reject':return real.deliver(replace(envelope,hand_id=''))
                return receipt
        host=ReplayHost(FIXTURE_A,run_id=PROTOCOL_ID+'-correctness-stage0-'+kind+'-'+finish,blueprint=policy,clock=witness,mailbox=Mailbox())
        outcome=host.run();output(kind+'-then-'+finish,host,outcome,source,real)

# Rejected-input cleanup fault: first recorded input cause must stay primary.
fixture=replace(FIXTURE_A,script=(ScriptedAction('preflop',3,'call'),)+FIXTURE_A.script[1:])
source=Source();host=ReplayHost(fixture,run_id=PROTOCOL_ID+'-correctness-stage0-count',blueprint=policy,clock=source);host.run();count=source.calls
for at in range(1,count+1):
    source=Source();source.fail_at=at
    host=ReplayHost(fixture,run_id=PROTOCOL_ID+'-correctness-stage0-rejected-'+str(at),blueprint=policy,clock=source)
    outcome=host.run()
    if outcome.receipt.secondary_failures and str(outcome.receipt.failure_reason)=='event_order':output('input-then-cleanup-'+str(at),host,outcome,source)

# Host-only failures are represented by terminal reason, without a failure row.
for direction in ('source-first','body-first'):
    source=Source();witness=MonotonicWitness(source)
    def oracle(**kwargs):
        source.kind='reversed'
        if direction=='source-first':
            try:witness()
            except (ClockInvalidError,ClockReversedError):pass
        raise ValueError('independent settlement body failure')
    host=ReplayHost(FIXTURE_A,run_id=PROTOCOL_ID+'-correctness-stage0-'+direction,blueprint=policy,clock=witness,settlement_oracle=oracle)
    outcome=host.run();output(direction,host,outcome,source)

# A source reversal before any valid runtime boundary still survives its later invalid refusal.
for kind in ('invalid','reversed'):
    source=Source();witness=MonotonicWitness(source);witness();source.kind=kind
    try:witness()
    except (ClockInvalidError,ClockReversedError):pass
    host=ReplayHost(FIXTURE_A,run_id=PROTOCOL_ID+'-correctness-stage0-prefailed-'+kind,blueprint=policy,clock=witness)
    outcome=host.run();output('no-start-prefailed-'+kind,host,outcome,source)
