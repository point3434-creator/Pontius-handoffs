import sys
expected_executable, expected_version = sys.argv[1:3]
print('executable=' + sys.executable, flush=True)
print('implementation=' + sys.implementation.name, flush=True)
print('full_version=' + sys.version, flush=True)
assert sys.executable.lower().replace('/', '\\') == expected_executable.lower().replace('/', '\\')
assert sys.implementation.name == 'cpython'
assert '.'.join(map(str, sys.version_info[:3])) == expected_version
assert sys.version_info.releaselevel == 'final' and sys.version_info.serial == 0
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
import json
import os
from dataclasses import replace
from pathlib import Path
import traceback
SNAPSHOT = Path(r'D:\pontius-snapshots\v0a-r006-cold-a-98fee7dce06d4fcca2da4475c550b928\harness')
assert Path.cwd() == SNAPSHOT
assert os.environ['PYTHONPATH'] == str(SNAPSHOT / 'src')
assert os.environ['PONTIUS_GIT'] == r'C:\Program Files\Git\cmd\git.exe'
print('cwd=' + str(Path.cwd()))
print('environment=' + json.dumps(dict(os.environ), sort_keys=True))
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.holdem_cards import SixSeatHoldemDeal
from pontius.v0a.model import ActionMailbox, FailureCode
from pontius.v0a.replay import FIXTURE_A, FIXTURE_B, PROTOCOL_ID, ReplayHost, ScriptedAction
from pontius.v0a.trace import canonical_json
import pontius.v0a.replay as replay
import pontius.v0a.runtime as runtime
for module in (replay, runtime):
    assert Path(module.__file__).resolve().is_relative_to(SNAPSHOT / 'src')
    print('module=' + module.__name__ + ':' + module.__file__)

class ClockSource:
    def __init__(self):
        self.now = 1_000
        self.reads = 0
    def __call__(self):
        self.reads += 1
        value = self.now
        self.now += 1_000
        return value

results = []
def execute(name, *, fixture=FIXTURE_A, row=None, showdown_call=None, late=False):
    source = ClockSource()
    host = ReplayHost(fixture, run_id=PROTOCOL_ID + '-correctness-cold-a-' + name,
        blueprint=ImmutableBlueprintActionSource(source_id='cold-a-empty-reference'),
        clock=source, source_commit='c74b80628a89938ca585ef3240b5c267a7174d0f',
        source_manifest_sha256='2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f')
    state = {'injected': 0, 'evaluations': 0, 'delayed': 0}
    def fault_schedule(frame, event, arg):
        # Observe actual production functions. No owner, serializer, evaluator,
        # mailbox or ledger is replaced. One deterministic fault is raised at
        # the selected real execution boundary; the opposing cell uses the same fault.
        if event == 'return' and frame.f_code is ActionMailbox.deliver.__code__ and late and not state['delayed']:
            source.now += 16_000_000_000
            state['delayed'] += 1
        if event == 'call' and frame.f_code is SixSeatHoldemDeal.showdown_strengths.__code__:
            state['evaluations'] += 1
            if state['evaluations'] == showdown_call:
                state['injected'] += 1
                raise MemoryError('cold-a scheduled evaluator allocation failure')
        if event == 'call' and frame.f_code is canonical_json.__code__:
            payload = frame.f_locals.get('payload')
            if isinstance(payload, dict) and payload.get('record_type') == row and row is not None and not state['injected']:
                state['injected'] += 1
                raise MemoryError('cold-a scheduled trace serialization allocation failure')
        return fault_schedule
    outcome = None
    error = None
    location = []
    try:
        sys.settrace(fault_schedule)
        outcome = host.run()
    except BaseException as caught:
        error = type(caught).__name__ + ': ' + str(caught)
        location = traceback.format_tb(caught.__traceback__)
    finally:
        sys.settrace(None)
    result = {'case': name, 'fault_schedule': state, 'escaped': error,
        'receipt': None if outcome is None else {'passed': outcome.receipt.passed,
            'primary': outcome.receipt.failure_reason,
            'secondary': outcome.receipt.secondary_failures,
            'accounting_complete': outcome.receipt.accounting_complete,
            'trace_sha256': outcome.receipt.trace_sha256},
        'accepted_actions': len(host.mailbox.accepted),
        'journal': host.runtime.closure_failures,
        'traceback': location}
    results.append(result)
    print(json.dumps(result, sort_keys=True), flush=True)
    return result

for fixture in (FIXTURE_A, FIXTURE_B):
    clean = execute('clean-' + fixture.name, fixture=fixture)
    assert clean['escaped'] is None and clean['receipt']['passed']
terminal = execute('terminal-serialization', row='terminal')
assert terminal['escaped'] is None and terminal['receipt']['primary'] == FailureCode.TRACE_WRITE_FAILED
assert terminal['accepted_actions'] == FIXTURE_A.expected_controlled_actions
settlement = execute('owned-settlement-evaluation', showdown_call=2)
assert settlement['escaped'] is None and settlement['receipt']['primary'] == FailureCode.SETTLEMENT_MISMATCH
assert settlement['accepted_actions'] == FIXTURE_A.expected_controlled_actions
# Unchanged surrounding call sites are in the declared end-to-end host scope.
decision = execute('decision-serialization', row='decision')
assert decision['escaped'] is not None and decision['receipt'] is None and decision['accepted_actions'] == 1
late = execute('late-failure-serialization', row='failure', late=True)
assert late['escaped'] is not None and late['receipt'] is None and late['accepted_actions'] == 1
assert late['journal'][0] == FailureCode.ACTION_DEADLINE_EXCEEDED
showdown = execute('first-showdown-evaluation', showdown_call=1)
assert showdown['escaped'] is not None and showdown['receipt'] is None
assert showdown['accepted_actions'] == FIXTURE_A.expected_controlled_actions
malformed = replace(FIXTURE_A, name='malformed-action',
    script=(ScriptedAction('preflop', 4, 'raise', True),) + FIXTURE_A.script[1:])
invalid = execute('invalid-script-action', fixture=malformed)
assert invalid['fault_schedule']['injected'] == 0
assert invalid['escaped'] is not None and invalid['receipt'] is None and invalid['accepted_actions'] == 1
print('DIAGNOSTIC CONFIRMED: 2 clean controls, 2 owned-fault controls, 4 escaping host paths')
