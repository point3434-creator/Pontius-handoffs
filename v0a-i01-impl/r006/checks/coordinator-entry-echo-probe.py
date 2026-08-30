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

from pontius.v0a.clock import MonotonicWitness
from pontius.v0a.replay import chip_depth_settlement
rows=[]
for fixture,entry in ((FIXTURE_A,134),(FIXTURE_B,68)):
 for kind in ('exception','invalid','reversed'):
  observed=[]
  class RecordingSource(Clock):
   def __call__(self):
    if self.calls+1==self.fail_at:observed.append('clock_reversed' if self.kind=='reversed' else 'clock_invalid')
    return super().__call__()
  source=RecordingSource(entry,kind);witness=MonotonicWitness(source)
  def sampling_oracle(**kwargs):
   witness()
   return chip_depth_settlement(**kwargs)
  runner=ReplayHost(fixture,run_id=f'{PROTOCOL_ID}-correctness-entry-echo',
    blueprint=ImmutableBlueprintActionSource(source_id='coordinator-policy'),clock=witness,
    settlement_oracle=sampling_oracle)
  outcome=runner.run()
  actual=([outcome.receipt.failure_reason.value] if outcome.receipt.failure_reason else [])+[x.value for x in outcome.receipt.secondary_failures]
  rows.append(dict(fixture=fixture.name,kind=kind,expected=observed,actual=actual,
    matches=observed==actual,source_resampled=source.calls!=entry,
    **details(outcome,runner,source)))
print(json.dumps(dict(candidate='c74b80628a89938ca585ef3240b5c267a7174d0f',
 manifest_sha256='2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f',
 diagnostic_only=True,observations=rows)),flush=True)
