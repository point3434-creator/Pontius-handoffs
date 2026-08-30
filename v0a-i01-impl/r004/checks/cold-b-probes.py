"""Cold-B public-path closure diagnostics; no production monkeypatches."""
import json
import sys
import tempfile
from dataclasses import replace
from pathlib import Path
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.model import FailureCode
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, chip_depth_settlement

class Clock:
    def __init__(self, fault=None, kind='invalid', record=False):
        self.reads=0
        self.fault=fault
        self.kind=kind
        self.stack=[]
        self.record=record
    def __call__(self):
        self.reads+=1
        if self.record:
            frame=sys._getframe(1)
            names=[]
            for _ in range(6):
                if frame is None:
                    break
                names.append(frame.f_code.co_name)
                frame=frame.f_back
            self.stack.append((self.reads, names))
        if self.reads == self.fault:
            if self.kind == 'source':
                raise OSError('cold-b source failure')
            if self.kind == 'reversed':
                return -1 if self.reads == 1 else 1_000_000+(self.reads-1)*1000-1
            return True
        return 1_000_000+self.reads*1000

def wrong_oracle(**kwargs):
    oracle=chip_depth_settlement(**kwargs)
    return replace(oracle, final_stacks=tuple(v+1 for v in oracle.final_stacks))

def run(fixture, clock, *, destination=None, root=None, mismatch=False):
    kwargs={'settlement_oracle': wrong_oracle} if mismatch else {}
    host=ReplayHost(fixture, run_id=f'{PROTOCOL_ID}-correctness-cold-b', blueprint=ImmutableBlueprintActionSource(source_id='cold-b-empty'), clock=clock, **kwargs)
    outcome=host.run(destination=destination, run_root=root)
    return host, outcome

def observed(host, outcome, clock):
    receipt=outcome.receipt
    terminal=json.loads(outcome.trace.splitlines()[-1])
    return {'reads':clock.reads,'passed':receipt.passed,'accounting_complete':receipt.accounting_complete,'primary':None if receipt.failure_reason is None else receipt.failure_reason.value,'secondary':[c.value for c in receipt.secondary_failures],'accepted':len(host.mailbox.accepted),'decisions':len(outcome.decisions),'terminal':{k:terminal[k] for k in ('complete','passed','failure_reason','accounting_complete')},'runtime_causes':[c.value for c in host.runtime.closure_failures]}

counts={}
for fixture in (FIXTURE_A,FIXTURE_B):
    c=Clock(record=True)
    h,o=run(fixture,c)
    assert o.receipt.passed
    counts[fixture.name]=c.reads
    print(json.dumps({'baseline':fixture.name,'observations':c.reads,'last_seams':c.stack[-5:],'outcome':observed(h,o,c)}))

violations=[]
runs=0
for fixture in (FIXTURE_A,FIXTURE_B):
    for kind in ('invalid','reversed','source'):
        for n in range(1,counts[fixture.name]+1):
            c=Clock(n,kind)
            h,o=run(fixture,c)
            runs+=1
            expected=FailureCode.CLOCK_REVERSED if kind == 'reversed' and n>1 else FailureCode.CLOCK_INVALID
            reported=(o.receipt.failure_reason,*o.receipt.secondary_failures)
            problems=[]
            if o.receipt.passed: problems.append('success_after_clock_fault')
            if expected not in reported: problems.append('missing_typed_clock_cause')
            if c.reads != n: problems.append('source_resampled_after_fault')
            accepted=h.mailbox.accepted
            for d in o.decisions:
                e=accepted.get((d.hand_id,d.action_index))
                if e is None or e.action != d.selected_action or e.seat != d.seat or e.street != d.street:
                    problems.append('decision_envelope_changed')
            if len(accepted) != len(o.decisions): problems.append('missing_accepted_decision')
            if problems:
                violations.append({'fixture':fixture.name,'kind':kind,'fault':n,'problems':problems,'outcome':observed(h,o,c)})
print(json.dumps({'sweep_runs':runs,'violation_count':len(violations),'violations':violations}))
assert not violations

n=counts[FIXTURE_A.name]
for mismatch in (False, True):
    for occupied in (False, True):
        for kind in ('invalid','reversed'):
            for point in (None,n-4,n-3,n-2,n-1,n):
                if point is None and kind == 'reversed': continue
                c=Clock(point,kind)
                with tempfile.TemporaryDirectory(prefix='cold-b-publication-') as raw:
                    root=Path(raw)
                    destination=root/'trace.jsonl'
                    if occupied: destination.write_bytes(b'occupied\n')
                    h,o=run(FIXTURE_A,c,destination=destination,root=root,mismatch=mismatch)
                    if occupied: assert destination.read_bytes() == b'occupied\n'
                    print(json.dumps({'combination':{'mismatch':mismatch,'occupied':occupied,'kind':kind,'fault':point},'outcome':observed(h,o,c)}))

print(json.dumps({'diagnostic_complete':True,'note':'Combination outputs are observations, not pass assertions for disputed failure-order semantics.'}))
