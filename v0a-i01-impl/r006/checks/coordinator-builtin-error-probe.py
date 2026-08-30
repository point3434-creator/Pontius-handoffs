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

from pontius.v0a.runtime import OperationFailed
from pontius.v0a.replay import chip_depth_settlement
from dataclasses import asdict
rows=[]
for fixture in (FIXTURE_A,FIXTURE_B):
 reference_clock=Clock();reference_host=host(fixture,reference_clock,'canonical-records')
 reference=reference_host.run();assert reference.receipt.passed
 for mode in ('unprintable_builtin','unowned_marker'):
  clock=Clock()
  class BadMessage:
   def __str__(self):raise TypeError('formatting secondary fault')
  def oracle(**kwargs):
   if mode=='unprintable_builtin':raise ValueError(BadMessage())
   raise OperationFailed('unrecorded')
  runner=ReplayHost(fixture,run_id=f'{PROTOCOL_ID}-correctness-message',
    blueprint=ImmutableBlueprintActionSource(source_id='coordinator-policy'),
    clock=clock,settlement_oracle=oracle)
  row=dict(fixture=fixture.name,mode=mode)
  try:
   outcome=runner.run()
   row.update(escaped=None,**details(outcome,runner,clock),
     decisions_equal_reference=tuple(map(asdict,outcome.decisions))==tuple(map(asdict,reference.decisions)))
  except BaseException as error:
   row.update(escaped=type(error).__name__,clock_calls=clock.calls)
  row['mailbox_equal_reference']=runner.mailbox.accepted==reference_host.mailbox.accepted
  row['runtime_count']=runner.runtime.accepted_delivery_count
  row['recorded']=[x.value for x in runner.runtime.closure_failures]
  rows.append(row)
print(json.dumps(dict(candidate='c74b80628a89938ca585ef3240b5c267a7174d0f',
 manifest_sha256='2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f',
 diagnostic_only=True,observations=rows)),flush=True)
