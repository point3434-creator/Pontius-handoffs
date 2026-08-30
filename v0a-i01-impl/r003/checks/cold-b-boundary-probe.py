from __future__ import annotations
import dataclasses
import json
import os
import pathlib
import sys
ROOT = pathlib.Path(r'D:\pontius-snapshots\v0a-i01-r003-f7c260aed2044b2280e1cedd64516064\harness')
expected = {'311': (r'D:\Pontius-tools\py311\Scripts\python.exe', (3,11,15)),
            '314': (r'D:\Pontius\.venv\Scripts\python.exe', (3,14,6))}[sys.argv[1]]
identity = {'executable':sys.executable, 'implementation':sys.implementation.name,
            'full_version':sys.version, 'version':list(sys.version_info[:3]),
            'cwd':os.getcwd(), 'PYTHONPATH':os.environ.get('PYTHONPATH'),
            'environment_keys':sorted(os.environ)}
assert os.path.normcase(sys.executable) == os.path.normcase(expected[0])
assert sys.implementation.name == 'cpython' and sys.version_info[:3] == expected[1]
assert pathlib.Path.cwd() == ROOT and pathlib.Path(os.environ['PYTHONPATH']) == ROOT/'src'
assert sys.flags.safe_path and sys.dont_write_bytecode
assert os.environ['PONTIUS_GIT'] == r'C:\Program Files\Git\cmd\git.exe'
assert not any(name.startswith('pontius') for name in sys.modules)
print(json.dumps({'identity_before_payload_import':identity}), flush=True)
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import (ReplayHost, FIXTURE_A, FIXTURE_B, ActionMailbox,
    PROTOCOL_ID, chip_depth_settlement)
from pontius.v0a.runtime import HandRuntime
from pontius.v0a.model import HandStartedEvent
import pontius.v0a.runtime as runtime_module
assert pathlib.Path(runtime_module.__file__) == ROOT/'src/pontius/v0a/runtime.py'
assert not any(name in sys.modules for name in ('cupy','torch'))
print(json.dumps({'runtime_import':runtime_module.__file__, 'no_cupy_or_torch':True}))

class Clock:
    def __init__(self, fail_at=None, jump_at=None, jump_ns=0):
        self.reads = 0
        self.now = 0
        self.fail_at = fail_at
        self.jump_at = jump_at
        self.jump_ns = jump_ns
    def __call__(self):
        self.reads += 1
        if self.reads == self.fail_at:
            raise ValueError('deterministic cold-b fault')
        self.now += 1000000
        if self.reads == self.jump_at:
            self.now += self.jump_ns
        return self.now

fixture=FIXTURE_A
for label, jump_at, jump_ns, fail_at in (
    ('boundary_deadline',6,16000000000,7),
    ('ready_cutoff',9,14000000001,10),
    ('ready_deadline_postaccept',9,16000000000,14)):
    mailbox=ActionMailbox()
    runtime=HandRuntime(blueprint=ImmutableBlueprintActionSource('cold-b-empty'),
                        mailbox=mailbox,clock=Clock(fail_at,jump_at,jump_ns))
    event=HandStartedEvent(hand_id='cold-b-boundary',event_index=0,button=fixture.button,
        controlled_seat=fixture.controlled_seat,starting_stacks=fixture.starting_stacks,
        small_blind=fixture.small_blind,big_blind=fixture.big_blind,
        private_cards=tuple(fixture.deal().hand(fixture.controlled_seat)))
    outcome=runtime.dispatch(event)
    print(json.dumps({'outer_flag_case':label,'status':outcome.status,
        'cutoff':outcome.failure.timing.work_cutoff_crossed,
        'deadline':outcome.failure.timing.deadline_crossed,
        'delivery_count':runtime.accepted_delivery_count,
        'delivery_status':outcome.failure.delivery_status,
        'decision_retained':outcome.decision is not None}),flush=True)

def wrong_stacks(**kwargs):
    oracle=chip_depth_settlement(**kwargs)
    stacks=list(oracle.final_stacks)
    stacks[0]+=1
    stacks[3]-=1
    return dataclasses.replace(oracle,final_stacks=tuple(stacks))

def wrong_eligibility(**kwargs):
    oracle=chip_depth_settlement(**kwargs)
    amount,eligible=oracle.pots[0]
    return dataclasses.replace(oracle,pots=((amount,eligible[1:]),*oracle.pots[1:]))

for label,fixture,clock,oracle in (
    ('fixture_a',FIXTURE_A,Clock(),chip_depth_settlement),
    ('fixture_b',FIXTURE_B,Clock(),chip_depth_settlement),
    ('conserving_stack_mismatch',FIXTURE_B,Clock(),wrong_stacks),
    ('eligibility_only_mismatch',FIXTURE_B,Clock(),wrong_eligibility),
    ('clock_before_mismatch',FIXTURE_A,Clock(134),wrong_stacks),
    ('clock_after_mismatch',FIXTURE_A,Clock(136),wrong_stacks)):
    host=ReplayHost(fixture,run_id=f'{PROTOCOL_ID}-correctness-cold-b-{label}',
        blueprint=ImmutableBlueprintActionSource('cold-b-empty'),clock=clock,
        settlement_oracle=oracle)
    outcome=host.run()
    print(json.dumps({'host_case':label,'read_count':clock.reads,
        'passed':outcome.receipt.passed,'reason':outcome.receipt.failure_reason,
        'secondary':list(outcome.receipt.secondary_failures),
        'accounting_complete':outcome.receipt.accounting_complete,
        'failure_codes':[failure.code for failure in outcome.failures],
        'settlement':dataclasses.asdict(outcome.settlement) if outcome.settlement else None}),
        flush=True)

clock=Clock()
real=ActionMailbox()
class LateMailbox:
    def deliver(self,envelope):
        receipt=real.deliver(envelope)
        clock.now += 16000000000
        return receipt
host=ReplayHost(FIXTURE_A,run_id=f'{PROTOCOL_ID}-correctness-cold-b-late',
    blueprint=ImmutableBlueprintActionSource('cold-b-empty'),clock=clock,mailbox=LateMailbox())
outcome=host.run()
terminal=json.loads(outcome.trace.splitlines()[-1])
print(json.dumps({'late_delivery':{'passed':outcome.receipt.passed,
    'reason':outcome.receipt.failure_reason,'actual_accepted':len(real.accepted),
    'runtime_accepted':host.runtime.accepted_delivery_count,
    'terminal_count':terminal['decision_count']}}),flush=True)
