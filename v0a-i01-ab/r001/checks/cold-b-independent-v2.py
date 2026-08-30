"""Cold B independent public-boundary diagnostics; no production mutation."""
import sys
assert sys.implementation.name == 'cpython' and sys.version_info[:3] in ((3,11,15),(3,14,6))
import dataclasses, json, pathlib, tempfile
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import ClockInvalidError, ClockReversedError, MonotonicWitness
from pontius.v0a.model import FailureCode, DecisionRecord
from pontius.v0a.replay import ReplayHost, FIXTURES, PROTOCOL_ID, chip_depth_settlement

rows=[]
class Source:
    def __init__(self, observed):
        self.calls=0
        self.fail_at=None
        self.kind='invalid'
        self.observed=observed
    def __call__(self):
        self.calls += 1
        if self.calls == self.fail_at:
            code='clock_reversed' if self.kind in ('reversed','backwards') else 'clock_invalid'
            self.observed.append(code)
            if self.kind == 'exception': raise OSError('real source failure')
            if self.kind == 'reversed': raise ClockReversedError('real source reversal')
            if self.kind == 'backwards': return 0
            return True
        return self.calls * 1000

class ExistingPath:
    def __init__(self, path, observed): self.path,self.observed=path,observed
    def __fspath__(self):
        self.observed.append('trace_write_failed')
        return str(self.path)

def codes(outcome):
    r=outcome.receipt
    return ([] if r.failure_reason is None else [r.failure_reason.value])+[c.value for c in r.secondary_failures]

def host(fixture, witness, oracle):
    return ReplayHost(fixture,run_id=PROTOCOL_ID+'-correctness-cold-b-'+fixture.name,
        blueprint=ImmutableBlueprintActionSource(source_id='cold-b-reference'),
        clock=witness,settlement_oracle=oracle)

def check(label, fixture, source, witness, oracle=chip_depth_settlement, *, writer=False,
          complete_actions=False, expected_touches=None, touches=None, destination=None):
    h=host(fixture,witness,oracle)
    escaped=None
    with tempfile.TemporaryDirectory() as directory:
        root=pathlib.Path(directory)
        path=root/'occupied.trace'
        if writer: path.write_bytes(b'cold-b-existing-file')
        kwargs=({'destination':ExistingPath(path,source.observed),'run_root':root} if writer else {})
        if destination is not None: kwargs={'destination':destination,'run_root':root}
        try:
            out=h.run(**kwargs)
        except BaseException as error:
            escaped=type(error).__name__
        if escaped:
            row={'label':label,'fixture':fixture.name,'expected':list(source.observed),'escape':escaped,'ok':False}
        else:
            actual=codes(out)
            accepted=h.mailbox.accepted
            preserved=(len(out.decisions)==len(accepted)==h.runtime.accepted_delivery_count)
            for record,envelope in zip(out.decisions,accepted.values()):
                preserved = preserved and type(record) is DecisionRecord
                preserved = preserved and record.selected_action == envelope.action
                preserved = preserved and record.action_index == envelope.action_index
                preserved = preserved and record.hand_id == envelope.hand_id
            if complete_actions: preserved=preserved and len(accepted)==fixture.expected_controlled_actions
            touch_ok=touches is None or touches==expected_touches
            row={'label':label,'fixture':fixture.name,'expected':list(source.observed),
                 'actual':actual,'reads':source.calls,'fail_at':source.fail_at,
                 'accepted':len(accepted),'preserved':bool(preserved),'passed':out.receipt.passed,
                 'accounting_complete':out.receipt.accounting_complete,
                 'touches':touches,'ok':actual==source.observed and preserved and touch_ok
                    and (out.receipt.passed is (not actual))}
            if source.fail_at is not None and source.fail_at <= source.calls:
                row['ok'] = row['ok'] and source.calls==source.fail_at
            if writer: row['ok']=row['ok'] and path.read_bytes()==b'cold-b-existing-file'
        rows.append(row)
    return None if escaped else out

baselines={}
entries={}
for fixture in FIXTURES:
    observed=[]; s=Source(observed)
    def oracle(**kwargs):
        entries[fixture.name]=s.calls
        return chip_depth_settlement(**kwargs)
    check('baseline',fixture,s,MonotonicWitness(s),oracle,complete_actions=True)
    baselines[fixture.name]=s.calls

# Every actual baseline clock sample; only one real source failure can occur.
for fixture in FIXTURES:
    for kind in ('invalid','exception','reversed','backwards'):
        for index in range(1 if kind!='backwards' else 2,baselines[fixture.name]+1):
            for writer in (False,True):
                observed=[]; s=Source(observed); s.fail_at=index; s.kind=kind
                check('sweep/'+kind+'/'+str(index)+'/writer='+str(writer),fixture,s,
                      MonotonicWitness(s),writer=writer)

# Settlement entry, caught body source faults, refused dead reads, independent
# same-code body failures, and real publication refusal are scheduled together.
for fixture in FIXTURES:
    for phase in ('entry','body'):
        for kind in ('invalid','exception','reversed','backwards'):
            for mode in ('echo','caught_return','caught_value','caught_clock','caught_mismatch'):
                for writer in (False,True):
                    observed=[]; s=Source(observed); s.kind=kind; w=MonotonicWitness(s)
                    if phase=='entry': s.fail_at=entries[fixture.name]
                    def oracle(**kwargs):
                        if phase=='body': s.fail_at=s.calls+1
                        if mode=='echo': w()
                        else:
                            try: w()
                            except (ClockInvalidError,ClockReversedError): pass
                            # Repeat refusal more than once; the source must stay dead.
                            for unused in range(3):
                                try: w()
                                except ClockInvalidError: pass
                            if mode=='caught_value':
                                observed.append('settlement_mismatch'); raise ValueError('fresh body')
                            if mode=='caught_clock':
                                observed.append('clock_invalid'); raise ClockInvalidError('independent')
                            result=chip_depth_settlement(**kwargs)
                            if mode=='caught_mismatch':
                                observed.append('settlement_mismatch')
                                return dataclasses.replace(result,final_stacks=tuple(x+1 for x in result.final_stacks))
                            return result
                    check('/'.join(('body',phase,kind,mode,str(writer))),fixture,s,w,oracle,
                          writer=writer,complete_actions=True)

# Arbitrary diagnostic hooks cannot execute while retaining an exception.
def errors(touched):
    class Argument:
        def __str__(self): touched.append('str'); raise RuntimeError('render')
    class ClassSpoof(Exception):
        @property
        def __class__(self): touched.append('class'); return ClockReversedError
    class Metadata(Exception):
        def __getattribute__(self,name): touched.append('get:'+name); raise RuntimeError('metadata')
        def __setattr__(self,name,value): touched.append('set:'+name); raise RuntimeError('metadata')
    class TrueClock(ClockReversedError):
        @property
        def __class__(self): touched.append('clock-class'); return ValueError
        def __str__(self): touched.append('clock-str'); raise RuntimeError('render')
    return [('normal',ValueError('body'),'ordinary'),('argument',ValueError(Argument()),'ordinary'),
            ('spoof',ClassSpoof(),'ordinary'),('all-metadata',Metadata(),'ordinary'),
            ('true-clock',TrueClock(),'clock_reversed'),('stop',StopIteration('body'),'ordinary'),
            ('base',BaseException('body'),'ordinary'),('group',ExceptionGroup('body',[ValueError(Argument())]),'ordinary')]

for fixture in FIXTURES:
    for boundary in ('settlement','publication'):
        for cleanup in ('none','invalid','reversed'):
            for err_index in range(8):
                observed=[]; s=Source(observed); w=MonotonicWitness(s); touched=[]
                name,error,code=errors(touched)[err_index]
                def fail():
                    if cleanup!='none': s.kind=cleanup; s.fail_at=s.calls+1
                    observed.append(('settlement_mismatch' if boundary=='settlement' else 'trace_write_failed') if code=='ordinary' else code)
                    raise error
                def oracle(**kwargs): fail()
                class FailingPath:
                    def __fspath__(self): fail()
                check('/'.join(('hostile',boundary,cleanup,name)),fixture,s,w,
                      oracle if boundary=='settlement' else chip_depth_settlement,
                      destination=FailingPath() if boundary=='publication' else None,
                      complete_actions=True,touches=touched,expected_touches=[])

# Genuine body exceptions precede later clock cleanup, then actual file refusal.
for fixture in FIXTURES:
    for body in ('ordinary','invalid','reversed'):
        for cleanup in ('none','invalid','exception','reversed','backwards'):
            observed=[]; s=Source(observed); w=MonotonicWitness(s)
            def oracle(**kwargs):
                if cleanup!='none': s.kind=cleanup; s.fail_at=s.calls+1
                code={'ordinary':'settlement_mismatch','invalid':'clock_invalid','reversed':'clock_reversed'}[body]
                observed.append(code)
                error={'ordinary':ValueError,'invalid':ClockInvalidError,'reversed':ClockReversedError}[body]
                raise error('fresh independent body failure')
            check('/'.join(('compound',body,cleanup,'writer')),fixture,s,w,oracle,
                  writer=True,complete_actions=True)

failed=[r for r in rows if not r['ok']]
summary={'version':sys.version,'baselines':baselines,'settlement_entry_reads':entries,
         'cases':len(rows),'failed':len(failed),'failures':failed,'rows':rows}
receipt=pathlib.Path(__file__).with_name('cold-b-independent-v2-'+str(sys.version_info.major)+str(sys.version_info.minor)+'.json')
with receipt.open('x',encoding='utf-8',newline='\n') as f:
    json.dump(summary,f,indent=2); f.write('\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'}))
assert not failed, 'independent diagnostic failures; consult JSON without rendering hostile exceptions'
