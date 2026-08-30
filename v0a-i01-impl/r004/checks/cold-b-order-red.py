"""Cold-B RED expectation and dead-witness check at the five closure seams."""
import json
import tempfile
from pathlib import Path
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import MonotonicWitness
from pontius.v0a.model import FailureCode
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost

class Source:
    def __init__(self, fail=None):
        self.fail=fail
        self.calls=0
    def __call__(self):
        self.calls+=1
        return True if self.calls == self.fail else self.calls*1000

class ObservedWitness(MonotonicWitness):
    def __init__(self, source):
        super().__init__(source)
        self.queries_after_death=0
    def __call__(self):
        if self.failed:
            self.queries_after_death+=1
        return super().__call__()

def run(fixture, witness, **kwargs):
    host=ReplayHost(fixture, run_id=f'{PROTOCOL_ID}-correctness-cold-b-red', blueprint=ImmutableBlueprintActionSource(source_id='cold-b-empty'), clock=witness)
    return host, host.run(**kwargs)

checks=0
for fixture in (FIXTURE_A,FIXTURE_B):
    baseline=Source()
    _, good=run(fixture,ObservedWitness(baseline))
    assert good.receipt.passed
    for fail in range(baseline.calls-4,baseline.calls+1):
        source=Source(fail)
        witness=ObservedWitness(source)
        host,outcome=run(fixture,witness)
        assert source.calls == fail
        assert witness.queries_after_death == 0
        assert outcome.receipt.failure_reason is FailureCode.CLOCK_INVALID
        assert len(host.mailbox.accepted) == len(outcome.decisions) == fixture.expected_controlled_actions
        checks+=1
print(json.dumps({'closure_witness_cases':checks,'queries_after_death':0}), flush=True)

with tempfile.TemporaryDirectory(prefix='cold-b-order-red-') as raw:
    root=Path(raw)
    target=root/'trace.jsonl'
    target.write_bytes(b'occupied\n')
    source=Source(137)
    witness=ObservedWitness(source)
    host,outcome=run(FIXTURE_A,witness,destination=target,run_root=root)
    receipt=outcome.receipt
    print(json.dumps({'red_case':'trace write fails before publication-stop clock sample 137','actual_primary':receipt.failure_reason,'actual_secondary':receipt.secondary_failures,'expected_primary':'trace_write_failed','expected_secondary':['clock_invalid'],'accepted':len(host.mailbox.accepted),'decisions':len(outcome.decisions),'source_calls':source.calls,'queries_after_death':witness.queries_after_death,'destination_unchanged':target.read_bytes()==b'occupied\n'}), flush=True)
    assert receipt.failure_reason is FailureCode.TRACE_WRITE_FAILED, 'ADR-0485 first cause must remain primary'
    assert receipt.secondary_failures == (FailureCode.CLOCK_INVALID,)
