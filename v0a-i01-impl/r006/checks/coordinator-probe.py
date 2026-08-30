"""Coordinator observations: real host clock faults and real trace refusal ordering."""
import sys, json
from pathlib import Path
expected_executable, expected_version = sys.argv[1:3]
identity=dict(executable=sys.executable,implementation=sys.implementation.name,full_version=sys.version,version=list(sys.version_info[:3]))
assert Path(sys.executable).resolve()==Path(expected_executable).resolve()
assert identity['implementation']=='cpython' and '.'.join(map(str,identity['version']))==expected_version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({'identity_before_payload_import':identity}),flush=True)
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import FIXTURE_A,FIXTURE_B,PROTOCOL_ID,ReplayHost
import pontius.v0a.runtime as runtime_module
assert Path(runtime_module.__file__).resolve()==Path.cwd()/'src/pontius/v0a/runtime.py'
class Clock:
    def __init__(self,fail_at=None,kind='exception'):
        self.now=1000; self.calls=0; self.fail_at=fail_at; self.kind=kind
    def __call__(self):
        self.calls+=1
        if self.calls==self.fail_at:
            if self.kind=='exception': raise OSError('coordinator clock fault')
            if self.kind=='invalid': return True
            if self.kind=='reversed': return self.now-2000
        sample=self.now; self.now+=1000; return sample

def host(fixture,clock,suffix):
    return ReplayHost(fixture,run_id=f'{PROTOCOL_ID}-correctness-coordinator-{suffix}',blueprint=ImmutableBlueprintActionSource(source_id='coordinator-policy'),clock=clock)
def details(outcome,runner,clock):
    receipt=outcome.receipt
    return dict(clock_calls=clock.calls,passed=receipt.passed,accounting_complete=receipt.accounting_complete,reason=receipt.failure_reason.value if receipt.failure_reason else None,secondary=[v.value for v in receipt.secondary_failures],accepted=len(runner.mailbox.accepted),decisions=len(outcome.decisions),runtime_count=runner.runtime.accepted_delivery_count,trace_digest=receipt.trace_sha256)
rows=[]
for fixture in (FIXTURE_A,FIXTURE_B):
    clock=Clock(); runner=host(fixture,clock,'base-'+fixture.name); baseline=runner.run()
    assert baseline.receipt.passed
    total=clock.calls
    rows.append(dict(probe='baseline',fixture=fixture.name,**details(baseline,runner,clock)))
    for kind in ('exception','invalid','reversed'):
        failures=[]; count=0
        for position in range(2 if kind=='reversed' else 1,total+1):
            count+=1; clock=Clock(position,kind); runner=host(fixture,clock,f'{fixture.name}-{kind}-{position}')
            try:
                outcome=runner.run(); item=details(outcome,runner,clock)
                if item['passed'] or item['reason'] is None or item['accepted']!=item['decisions'] or clock.calls!=position:
                    failures.append(dict(position=position,**item))
            except Exception as error: failures.append(dict(position=position,error=type(error).__name__,message=str(error)))
        rows.append(dict(probe='all_observation_faults',fixture=fixture.name,kind=kind,count=count,failures=failures))
# Use the snapshot's existing tracked README as an already-existing destination.
# The real writer must refuse it before any write; source remains untouched.
for position in (None,134,135,136,137,138):
    clock=Clock(position); runner=host(FIXTURE_A,clock,f'write-refusal-{position}')
    outcome=runner.run(destination=Path('README.md'),run_root=Path.cwd())
    rows.append(dict(probe='real_trace_refusal',fault_at=position,**details(outcome,runner,clock)))
print(json.dumps({'candidate':'c74b80628a89938ca585ef3240b5c267a7174d0f','manifest_sha256':'2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f','observations':rows}),flush=True)
