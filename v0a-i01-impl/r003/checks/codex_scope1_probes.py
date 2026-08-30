"""Bounded slice-1 host clock matrix and real settlement comparison controls."""
import sys, os, json
from pathlib import Path
expected_executable, expected_version = sys.argv[1:3]
identity=dict(executable=sys.executable,implementation=sys.implementation.name,
              full_version=sys.version,version=list(sys.version_info[:3]))
assert Path(sys.executable).resolve()==Path(expected_executable).resolve()
assert identity['implementation']=='cpython'
assert '.'.join(map(str,identity['version'][:2]))==expected_version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({'identity_before_payload_import':identity}),flush=True)
from dataclasses import replace
from unittest.mock import patch
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.model import PotRecord
import pontius.v0a.runtime as runtime_module
assert Path(runtime_module.__file__).resolve()==Path.cwd()/'src/pontius/v0a/runtime.py'
class Clock:
    def __init__(self, fail_at=None, kind='exception'):
        self.now=1000; self.calls=0; self.fail_at=fail_at; self.kind=kind
    def __call__(self):
        self.calls+=1
        if self.calls==self.fail_at:
            if self.kind=='exception': raise OSError('coordinator clock fault')
            if self.kind=='invalid': return True
            if self.kind=='reversed': return self.now-2000
        sample=self.now; self.now+=1000; return sample

def make_host(fixture,clock,suffix):
    return ReplayHost(fixture,run_id=f'{PROTOCOL_ID}-correctness-coordinator-{suffix}',
                      blueprint=ImmutableBlueprintActionSource(source_id='coordinator-policy'),clock=clock)
rows=[]
for fixture in (FIXTURE_A,FIXTURE_B):
    baseline_clock=Clock(); baseline=make_host(fixture,baseline_clock,'base-'+fixture.name).run()
    assert baseline.receipt.passed
    baseline_count=baseline_clock.calls
    rows.append(dict(probe='baseline',fixture=fixture.name,clock_calls=baseline_count,
                     accepted_decisions=len(baseline.decisions)))
    for kind in ('exception','invalid','reversed'):
        missing_causes=[]; escapes=[]; false_success=[]; lost_decisions=[]; details=[]
        # A reversal needs an earlier accepted observation; other sources cover read 1.
        for position in range(2 if kind=='reversed' else 1,baseline_count+1):
            clock=Clock(position,kind); host=make_host(fixture,clock,f'{fixture.name}-{kind}-{position}')
            try:
                outcome=host.run()
                receipt=outcome.receipt
                reason=None if receipt.failure_reason is None else receipt.failure_reason.value
                secondaries=[reason.value for reason in receipt.secondary_failures]
                item=dict(position=position,clock_calls=clock.calls,passed=receipt.passed,
                          accounting_complete=receipt.accounting_complete,reason=reason,
                          secondary=secondaries,accepted=len(host.mailbox.accepted),
                          decisions=len(outcome.decisions),runtime_count=host.runtime.accepted_delivery_count)
                if receipt.passed: false_success.append(position)
                if reason is None and not secondaries: missing_causes.append(position)
                if len(host.mailbox.accepted)!=len(outcome.decisions): lost_decisions.append(position)
                if reason is None or receipt.passed or len(host.mailbox.accepted)!=len(outcome.decisions): details.append(item)
            except Exception as error:
                escapes.append(dict(position=position,error=type(error).__name__,message=str(error)))
        rows.append(dict(probe='all_observation_faults',fixture=fixture.name,kind=kind,
                         baseline_count=baseline_count,missing_causes=missing_causes,
                         escaped=escapes,false_success=false_success,lost_decisions=lost_decisions,
                         details=details))
real_settle=HandRuntime.settle
for field in ('final_stacks','pot_seats'):
    def altered_settle(self,field=field):
        value=real_settle(self)
        if field=='final_stacks': return replace(value,final_stacks=(0,)*6)
        return replace(value,pots=tuple(PotRecord(amount=p.amount,seats=(0,)) for p in value.pots))
    with patch.object(HandRuntime,'settle',altered_settle):
        outcome=make_host(FIXTURE_A,Clock(),'settlement-'+field).run()
    rows.append(dict(probe='real_settlement_corruption',field=field,passed=outcome.receipt.passed,
                     reason=outcome.receipt.failure_reason.value if outcome.receipt.failure_reason else None))
print(json.dumps({'candidate':'47d08d8c1556d776358e15811e3e98b859fd6a8b',
                  'manifest_sha256':'cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a',
                  'observations':rows}),flush=True)
