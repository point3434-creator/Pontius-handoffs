import sys
import platform
sys.stdout.reconfigure(encoding="utf-8", newline="\n")
sys.stderr.reconfigure(encoding="utf-8", newline="\n")
assert sys.executable == sys.argv[1]
assert platform.python_version() == sys.argv[2]
assert platform.python_implementation() == "CPython"
print("BOOTSTRAP", repr(sys.executable), platform.python_implementation(), platform.python_version(), flush=True)
import os
import json
import tempfile
from pathlib import Path
from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import patch
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import MonotonicWitness
from pontius.v0a.model import ActionMailbox, HandStartedEvent
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, ScriptedAction
from pontius.v0a.trace import TraceBuilder
import pontius.v0a.replay as replay_module
assert Path.cwd() == Path(r"D:\pontius-snapshots\v0a-r005-cold-b-e6ac13a682804562a53621e8fab883e1\harness")
assert os.environ["PYTHONPATH"] == str(Path.cwd()/"src")
assert os.environ["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
assert Path(replay_module.__file__) == Path.cwd()/"src/pontius/v0a/replay.py"
print("PAYLOAD_MODULE", replay_module.__file__)
results=[]

class GateClock:
    def __init__(self, observed):
        self.observed=observed
        self.now=1_000_000
        self.armed=None
        self.faulted=False
        self.after_fault_calls=0
    def __call__(self):
        if self.faulted:
            self.after_fault_calls += 1
            raise AssertionError("broken source queried again")
        if self.armed:
            kind=self.armed
            self.armed=None
            self.faulted=True
            code="clock_reversed" if kind=="reversed" else "clock_invalid"
            self.observed.append(code)
            if kind == "reversed":
                return self.now-2_000
            if kind == "source":
                raise OSError("independent source failure")
            return True
        value=self.now
        self.now+=1_000
        return value

def host_for(name, fixture=FIXTURE_A, **kwargs):
    return ReplayHost(fixture, run_id=PROTOCOL_ID+"-correctness-cold-b-"+name,
                      blueprint=ImmutableBlueprintActionSource(source_id="cold-b-independent"), **kwargs)

def codes(outcome):
    return [str(x) for x in (outcome.receipt.failure_reason,*outcome.receipt.secondary_failures) if x is not None]

def record(name, observed, reported, **details):
    row={"case":name,"observed_order":observed,"reported_order":reported,"contract_satisfied":observed==reported,**details}
    results.append(row)
    print(json.dumps(row,sort_keys=True),flush=True)

# No-fault and action conservation controls use literal independently frozen counts/payouts.
for fixture,count,payouts in [(FIXTURE_A,4,(0,0,0,12,0,0)),(FIXTURE_B,2,(16,10,24,30,0,0))]:
    observed=[]
    clock=GateClock(observed)
    host=host_for(fixture.name,fixture,clock=clock)
    out=host.run()
    assert out.receipt.passed and out.receipt.accounting_complete
    assert len(out.decisions)==len(host.mailbox.accepted)==count
    assert out.settlement.payouts==payouts
    assert sum(out.settlement.final_stacks)==sum(fixture.starting_stacks)
    record("success-"+fixture.name,[],codes(out),accepted=count,passed=out.receipt.passed)

# Body failure is deliberately observed before arming an independent source failure.
# No ledger subclass, private observation hook, or implementation call index is used.
for kind in ("invalid","reversed","source"):
    observed=[]
    clock=GateClock(observed)
    def failing_oracle(**kwargs):
        observed.append("settlement_mismatch")
        clock.armed=kind
        raise ValueError("oracle arithmetic failed before context cleanup")
    host=host_for("body-then-"+kind,clock=clock,settlement_oracle=failing_oracle)
    out=host.run()
    assert len(host.mailbox.accepted)==len(out.decisions)==4
    assert not out.receipt.passed and not out.receipt.accounting_complete
    assert clock.after_fault_calls==0
    record("oracle-exception-then-"+kind,list(observed),codes(out),accepted=len(out.decisions),passed=out.receipt.passed,accounting_complete=out.receipt.accounting_complete,after_fault_calls=clock.after_fault_calls)

# A semantic mismatch returned normally is the opposing control for exception unwinding.
for kind in ("invalid","reversed"):
    observed=[]
    clock=GateClock(observed)
    def wrong_oracle(**kwargs):
        observed.append("settlement_mismatch")
        clock.armed=kind
        return SimpleNamespace(payouts=(0,)*6,final_stacks=(200,)*6,pots=())
    host=host_for("mismatch-then-"+kind,clock=clock,settlement_oracle=wrong_oracle)
    out=host.run()
    assert not out.receipt.passed and clock.after_fault_calls==0
    assert codes(out)==observed
    record("returned-mismatch-then-"+kind,list(observed),codes(out),accepted=len(out.decisions))

# A real supplied witness fails inside permitted host oracle work, before interval closure.
for kind in ("invalid","reversed"):
    observed=[]
    clock=GateClock(observed)
    witness=MonotonicWitness(clock)
    def timed_oracle(**kwargs):
        clock.armed=kind
        witness()
        raise AssertionError("unreachable")
    host=host_for("host-witness-"+kind,clock=witness,settlement_oracle=timed_oracle)
    out=host.run()
    assert not out.receipt.passed and not out.receipt.accounting_complete
    assert clock.after_fault_calls==0
    record("real-witness-failure-inside-oracle-"+kind,list(observed),codes(out),accepted=len(out.decisions),passed=out.receipt.passed,accounting_complete=out.receipt.accounting_complete,after_fault_calls=clock.after_fault_calls)

# Pure production writer path: a malformed local path raises after all real deliveries.
with tempfile.TemporaryDirectory(prefix="cold-b-") as raw:
    host=host_for("nul-path",clock=GateClock([]))
    try:
        out=host.run(destination=Path("bad\x00trace.jsonl"),run_root=Path(raw))
    except Exception as error:
        record("writer-nul-path",["trace_write_failed"],[],escaped_type=type(error).__name__,escaped_message=str(error),accepted=len(host.mailbox.accepted),receipt_returned=False)
    else:
        record("writer-nul-path",["trace_write_failed"],codes(out),accepted=len(out.decisions),receipt_returned=True)

# Production event construction with an invalid declared action, no monkeypatch.
bad_fixture=replace(FIXTURE_A,script=(ScriptedAction("preflop",4,"dance"),)+FIXTURE_A.script[1:])
host=host_for("invalid-script",bad_fixture,clock=GateClock([]))
try:
    out=host.run()
except Exception as error:
    record("event-construction-invalid-script",["invalid_event"],[],escaped_type=type(error).__name__,escaped_message=str(error),accepted=len(host.mailbox.accepted),receipt_returned=False)
else:
    record("event-construction-invalid-script",["invalid_event"],codes(out),receipt_returned=True)

# Terminal construction failure uses one bounded seam fault; the entire preceding hand is real.
host=host_for("terminal-builder",clock=GateClock([]))
with patch.object(TraceBuilder,"close",side_effect=OSError("terminal serialization failed")):
    try:
        out=host.run()
    except Exception as error:
        record("terminal-construction-exception",["trace_write_failed"],[],escaped_type=type(error).__name__,accepted=len(host.mailbox.accepted),receipt_returned=False)
    else:
        record("terminal-construction-exception",["trace_write_failed"],codes(out),receipt_returned=True)

# Real mailbox acceptance, then source failure: known delivered action must retain full record.
for kind in ("invalid","reversed"):
    observed=[]
    clock=GateClock(observed)
    class AcceptanceThenClock:
        def __init__(self): self.real=ActionMailbox(); self.calls=0
        def deliver(self,envelope):
            self.calls+=1
            receipt=self.real.deliver(envelope)
            clock.armed=kind
            return receipt
    mailbox=AcceptanceThenClock()
    host=host_for("accepted-then-"+kind,clock=clock,mailbox=mailbox)
    out=host.run()
    assert mailbox.calls==len(mailbox.real.accepted)==len(out.decisions)==1
    assert out.decisions[0].selected_action==next(iter(mailbox.real.accepted.values())).action
    assert out.decisions[0].timing.emission_observed_ns is None
    assert out.failures[0].timing==out.decisions[0].timing
    assert out.failures[0].delivery_status.value=="accepted"
    assert not out.receipt.passed and not out.receipt.accounting_complete
    assert clock.after_fault_calls==0
    assert codes(out)==observed
    record("accepted-action-preserved-"+kind,list(observed),codes(out),accepted=1,after_fault_calls=0)

print("INDEPENDENT_CASE_COUNT",len(results))
print("COUNTEREXAMPLE_COUNT",sum(not row["contract_satisfied"] for row in results))
# Observation run: nonzero contract counterexamples are reported rather than hidden behind an early abort.
assert len(results)==14
assert sum(not row["contract_satisfied"] for row in results)>=3
print("OBSERVATION_CAPTURE_COMPLETE")
