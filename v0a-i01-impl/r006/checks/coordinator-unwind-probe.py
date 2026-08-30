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

from pontius.v0a.replay import chip_depth_settlement
from pontius.v0a.clock import ClockInvalidError, ClockReversedError
rows=[]
for fixture,entry,exit_at in ((FIXTURE_A,134,135),(FIXTURE_B,68,69)):
  for error_type in (ValueError,ZeroDivisionError):
    for position in (None,entry,exit_at):
      for kind in (('exception','invalid','reversed') if position else ('exception',)):
        for writer_refusal in (False,True):
          observed=[]
          class ObservedClock(Clock):
            def __call__(self):
              if self.calls+1==self.fail_at: observed.append('clock_reversed' if self.kind=='reversed' else 'clock_invalid')
              return super().__call__()
          clock=ObservedClock(position,kind)
          def exploding_oracle(**kwargs):
            observed.append('settlement_mismatch')
            raise error_type('coordinator actual oracle exception')
          runner=ReplayHost(fixture,run_id=f'{PROTOCOL_ID}-correctness-unwind',
            blueprint=ImmutableBlueprintActionSource(source_id='coordinator-policy'),
            clock=clock,settlement_oracle=exploding_oracle)
          outcome=runner.run(**(dict(destination=Path('README.md'),run_root=Path.cwd()) if writer_refusal else {}))
          if writer_refusal: observed.append('trace_write_failed')
          actual=([outcome.receipt.failure_reason.value] if outcome.receipt.failure_reason else [])+[x.value for x in outcome.receipt.secondary_failures]
          rows.append(dict(fixture=fixture.name,error=error_type.__name__,fault_at=position,kind=kind,
            writer_refusal=writer_refusal,expected=observed,actual=actual,matches=actual==observed,
            **details(outcome,runner,clock)))
# Existing default oracle controls and explicit exception-only controls above.
for fixture in (FIXTURE_A,FIXTURE_B):
  clock=Clock(); runner=host(fixture,clock,'unwind-healthy-'+fixture.name); outcome=runner.run()
  assert outcome.receipt.passed
  rows.append(dict(control='default_oracle',fixture=fixture.name,**details(outcome,runner,clock)))
print(json.dumps(dict(candidate='c74b80628a89938ca585ef3240b5c267a7174d0f',manifest_sha256='2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f',
 diagnostic_only=True,cases=len(rows),mismatches=sum(not r['matches'] for r in rows if 'matches' in r),
 observations=rows)),flush=True)
